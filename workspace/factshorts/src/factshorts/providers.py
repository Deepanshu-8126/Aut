"""Free-first provider chain — retries, model rotation, disk cache, graceful failover.

Nothing here scrapes a web UI. Everything is a public API endpoint or your own key.
The default chain is free and key-less; if a stage is rate limited the next one takes over.

    stage 1  pollinations POST /openai      free, key-less, GPT-OSS 20B   (primary)
    stage 2  pollinations GET /<prompt>     free, key-less, short prompts
    stage 3  any OpenAI-compatible key      Gemini / Groq / OpenRouter / Cerebras / Ollama
    stage 4  offline template               never fails, ships the channel anyway

Set FACTSHORTS_TEXT_PROVIDER / FACTSHORTS_IMAGE_PROVIDER to force one stage,
FACTSHORTS_NOCACHE=1 to bypass the disk cache.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

UA = "factshorts-pipeline/1.1 (+local)"
TIMEOUT = float(os.environ.get("FACTSHORTS_TIMEOUT", 120))
RATE_LIMIT_WAIT = float(os.environ.get("FACTSHORTS_RATE_WAIT", 18.0))  # first backoff, seconds
ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "assets" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

TEXT_MODELS = ["openai", "openai-fast"]           # POST stage, anonymous free tier
GET_MODELS = ["openai-fast", "openai"]            # GET stage often outlives POST
IMAGE_MODELS = ["flux", "turbo"]
VERBOSE = os.environ.get("FACTSHORTS_VERBOSE", "1") != "0"


def log(msg: str):
    if VERBOSE:
        print(f"  [providers] {msg}", flush=True)


# ------------------------------------------------------------------ transport
def _req(url: str, data: bytes | None = None, headers: dict | None = None,
         timeout: float | None = None) -> bytes:
    req = urllib.request.Request(url, data=data,
                                 headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout or TIMEOUT) as r:
        return r.read()


# A 402 on the free tier is a *time-window* limit, not a transient blip: short backoffs just
# burn the window. These factors give the limiter room to reset.
RATE_LIMIT_WAITS = (RATE_LIMIT_WAIT, RATE_LIMIT_WAIT * 2.5, RATE_LIMIT_WAIT * 4)


def _retry(fn: Callable[[], Any], attempts: int = 3, base: float = 2.0, what: str = "") -> Any:
    last: Exception | None = None
    rl = 0
    for i in range(attempts):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            last = e
            body = ""
            try:
                body = e.read()[:160].decode("utf-8", "ignore")
            except Exception:                                    # noqa: BLE001
                pass
            if e.code in (402, 429):
                wait = RATE_LIMIT_WAITS[min(rl, len(RATE_LIMIT_WAITS) - 1)] * (
                    1 + 0.25 * (time.time() % 1))                # small jitter
                rl += 1
                log(f"{what}: rate limited (HTTP {e.code}) — waiting {wait:.0f}s "
                    f"({i + 1}/{attempts})")
                if i < attempts - 1:
                    time.sleep(wait)
                continue
            log(f"{what}: HTTP {e.code} {body} — retry {i + 1}/{attempts}")
        except Exception as e:                                   # noqa: BLE001
            last = e
            log(f"{what}: {type(e).__name__} {e} — retry {i + 1}/{attempts}")
        if i < attempts - 1:
            time.sleep(base * (i + 1))
    raise RuntimeError(f"{what} failed after {attempts} attempts: {last}")


# --------------------------------------------------------------------- cache
def _cache_key(*parts: str) -> Path:
    h = hashlib.sha1("|".join(parts).encode()).hexdigest()[:20]
    return CACHE / f"{h}.txt"


def _cached(key: str, producer: Callable[[], str]) -> str:
    if os.environ.get("FACTSHORTS_NOCACHE") == "1":
        return producer()
    p = _cache_key(*key.split("|"))
    if p.exists():
        log(f"cache hit for {key[:48]}…")
        return p.read_text()
    out = producer()
    if out and len(out.strip()) >= 8:          # never persist an empty/failed reply
        p.write_text(out)
    return out


# ---------------------------------------------------------------------- text
def _pollinations_post(prompt: str, system: str, temperature: float,
                       max_tokens: int | None) -> str:
    last_err: Exception | None = None
    for model in TEXT_MODELS:
        body = {"model": model,
                "messages": ([{"role": "system", "content": system}] if system else []) +
                            [{"role": "user", "content": prompt}],
                "temperature": temperature}
        if max_tokens:
            body["max_tokens"] = max_tokens
        try:
            raw = _retry(lambda: _req("https://text.pollinations.ai/openai",
                                      json.dumps(body).encode(),
                                      {"Content-Type": "application/json"}),
                         attempts=2, what=f"pollinations POST ({model})")
            data = json.loads(raw)
            txt = data["choices"][0]["message"]["content"]
            fin = data["choices"][0].get("finish_reason")
            log(f"pollinations POST ok ({model}, finish={fin}, {len(txt)} chars)")
            return txt
        except Exception as e:                                   # noqa: BLE001
            last_err = e
            continue
    raise RuntimeError(f"pollinations POST exhausted: {last_err}")


def _pollinations_get(prompt: str, system: str) -> str:
    """GET stage with model rotation — in practice `openai-fast` survives when POST is 402."""
    last: Exception | None = None
    for model in GET_MODELS:
        url = ("https://text.pollinations.ai/" + urllib.parse.quote(prompt[:1500]) +
               f"?model={model}")
        if system:
            url += "&system=" + urllib.parse.quote(system[:600])
        try:
            txt = _retry(lambda u=url: _req(u), attempts=2, base=3.0,
                         what=f"pollinations GET ({model})").decode("utf-8", "ignore")
            if len(txt.strip()) < 2:
                raise RuntimeError("empty reply")
            log(f"pollinations GET ok ({model}, {len(txt)} chars)")
            return txt
        except Exception as e:                                   # noqa: BLE001
            last = e
            continue
    raise RuntimeError(f"pollinations GET exhausted: {last}")


def _resolve_openai_backend() -> tuple[str, str, str]:
    """Pick the backend from whichever free key is present (see FREE_KEYS.md)."""
    if os.environ.get("GROQ_API_KEY"):
        return ("https://api.groq.com/openai/v1", os.environ["GROQ_API_KEY"],
                os.environ.get("FACTSHORTS_TEXT_MODEL", "llama-3.3-70b-versatile"))
    if os.environ.get("OPENROUTER_API_KEY"):
        return ("https://openrouter.ai/api/v1", os.environ["OPENROUTER_API_KEY"],
                os.environ.get("FACTSHORTS_TEXT_MODEL", "deepseek/deepseek-chat-v3.1:free"))
    if os.environ.get("GEMINI_API_KEY"):
        return ("https://generativelanguage.googleapis.com/v1beta/openai",
                os.environ["GEMINI_API_KEY"],
                os.environ.get("FACTSHORTS_TEXT_MODEL", "gemini-2.5-flash"))
    return (os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            os.environ.get("OPENAI_API_KEY", ""),
            os.environ.get("FACTSHORTS_TEXT_MODEL", "gpt-4o-mini"))


def _openai_compatible(prompt: str, system: str, temperature: float,
                       max_tokens: int | None) -> str:
    base, key, model = _resolve_openai_backend()
    body: dict[str, Any] = {
        "model": model, "temperature": temperature,
        "messages": ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]}
    if max_tokens:
        body["max_tokens"] = max_tokens
    raw = _retry(lambda: _req(base.rstrip("/") + "/chat/completions",
                              json.dumps(body).encode(),
                              {"Content-Type": "application/json",
                               **({"Authorization": f"Bearer {key}"} if key else {})}),
                 attempts=2, what=f"openai-compatible ({model})")
    data = json.loads(raw)
    log(f"openai-compatible ok ({model})")
    return data["choices"][0]["message"]["content"]


def text_generate(prompt: str, system: str = "", provider: str | None = None,
                  model: str | None = None, temperature: float = 0.85,
                  max_tokens: int | None = 2000, use_cache: bool = True) -> str:
    """Run the chain until one stage answers. Raises only if every stage fails."""
    forced = (provider or os.environ.get("FACTSHORTS_TEXT_PROVIDER") or "auto").lower()
    stages: list[tuple[str, Callable[[], str]]] = []

    if forced not in ("auto",):
        table = {
            "pollinations": ("pollinations-post", lambda: _pollinations_post(prompt, system, temperature, max_tokens)),
            "pollinations-get": ("pollinations-get", lambda: _pollinations_get(prompt, system)),
            "openai": ("openai-compatible", lambda: _openai_compatible(prompt, system, temperature, max_tokens)),
            "groq": ("openai-compatible", lambda: _openai_compatible(prompt, system, temperature, max_tokens)),
            "openrouter": ("openai-compatible", lambda: _openai_compatible(prompt, system, temperature, max_tokens)),
            "gemini": ("openai-compatible", lambda: _openai_compatible(prompt, system, temperature, max_tokens)),
            "ollama": ("openai-compatible", lambda: _openai_compatible(prompt, system, temperature, max_tokens)),
        }
        if forced not in table:
            raise ValueError(f"unknown text provider: {forced}")
        return table[forced][1]()

    stages = [
        ("pollinations-post", lambda: _pollinations_post(prompt, system, temperature, max_tokens)),
        ("pollinations-get", lambda: _pollinations_get(prompt, system)),
    ]
    if any(os.environ.get(k) for k in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY",
                                       "OPENROUTER_API_KEY")) or os.environ.get("OPENAI_BASE_URL"):
        stages.append(("openai-compatible",
                       lambda: _openai_compatible(prompt, system, temperature, max_tokens)))

    errors = []
    for name, fn in stages:
        try:
            call = (lambda f=fn: _cached(f"{name}|{prompt}|{system}", f)) if use_cache else fn
            return call()
        except Exception as e:                                   # noqa: BLE001
            errors.append(f"{name}: {e}")
            log(f"stage '{name}' failed -> next stage")
    raise RuntimeError("all text stages failed:\n  " + "\n  ".join(errors))


# --------------------------------------------------------------------- image
def _pollinations_image(prompt: str, width: int, height: int, seed: int | None) -> bytes:
    last: Exception | None = None
    for model in IMAGE_MODELS:
        url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt[:1500]) +
               f"?width={width}&height={height}&model={model}&nologo=true&safe=false")
        if seed is not None:
            url += f"&seed={seed}"
        try:
            b = _retry(lambda: _req(url, timeout=max(TIMEOUT, 150)), attempts=3,
                       base=3.0, what=f"pollinations image ({model})")
            if len(b) < 2000:
                raise RuntimeError(f"suspiciously small image: {len(b)} bytes")
            log(f"pollinations image ok ({model}, {len(b)//1024} KB)")
            return b
        except Exception as e:                                   # noqa: BLE001
            last = e
    raise RuntimeError(f"pollinations image exhausted: {last}")


def _openai_image(prompt: str, width: int, height: int) -> bytes:
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    key = os.environ.get("OPENAI_API_KEY", "")
    body = {"model": os.environ.get("FACTSHORTS_IMAGE_API_MODEL", "gpt-image-1"),
            "prompt": prompt, "size": f"{width}x{height}", "n": 1}
    raw = _retry(lambda: _req(base.rstrip("/") + "/images/generations",
                              json.dumps(body).encode(),
                              {"Content-Type": "application/json",
                               "Authorization": f"Bearer {key}"}),
                 attempts=2, what="openai image")
    return base64.b64decode(json.loads(raw)["data"][0]["b64_json"])


def generate_image_bytes(prompt: str, width: int = 1024, height: int = 1024,
                         model: str | None = None, seed: int | None = None,
                         provider: str | None = None):
    forced = (provider or os.environ.get("FACTSHORTS_IMAGE_PROVIDER") or "auto").lower()
    try:
        if forced in ("auto", "pollinations"):
            return _pollinations_image(prompt, width, height, seed)
    except Exception as e:                                       # noqa: BLE001
        log(f"pollinations image failed ({e})")
        if forced != "auto":
            raise
    if os.environ.get("OPENAI_API_KEY"):
        return _openai_image(prompt, width, height)
    raise RuntimeError("no image provider available (see README: FREE_KEYS.md)")


# ---------------------------------------------------------------------- probe
def probe(deep: bool = False) -> dict[str, Any]:
    """`python run.py doctor [--deep]` — shows exactly which free stage is alive."""
    out: dict[str, Any] = {}
    try:
        t0 = time.time()
        r = text_generate("Reply with the single word: ok", use_cache=False)
        out["text: free chain"] = f"ok ({time.time()-t0:.1f}s) -> {r.strip()[:24]!r}"
    except Exception as e:                                       # noqa: BLE001
        out["text: free chain"] = f"FAIL {str(e)[:110]}"
    if deep:
        for model in TEXT_MODELS:
            try:
                t0 = time.time()
                _pollinations_post("Reply with: ok", "", 0.2, 16)
                out[f"text: pollinations {model}"] = f"ok ({time.time()-t0:.1f}s)"
            except Exception as e:                               # noqa: BLE001
                out[f"text: pollinations {model}"] = f"FAIL {str(e)[:80]}"
    try:
        t0 = time.time()
        b = generate_image_bytes("a gray sphere on a white background", 512, 512)
        out["image: free chain"] = f"ok ({len(b)//1024} KB, {time.time()-t0:.1f}s)"
    except Exception as e:                                       # noqa: BLE001
        out["image: free chain"] = f"FAIL {str(e)[:110]}"
    for k in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY"):
        out[f"env:{k}"] = "set" if os.environ.get(k) else "-"
    return out


def models() -> dict:
    """Live model list from the free endpoint (handy when they rotate models)."""
    raw = _req("https://text.pollinations.ai/models")
    return json.loads(raw)
