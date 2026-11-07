"""Topic -> 7-part content pack.

Uses a free LLM (Pollinations text, no key) to write the script, then validates and
repairs it against a strict schema so the renderer can never receive a broken slide.
Falls back to a deterministic offline template if the network/LLM fails.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from .renderer import Part
from .providers import text_generate
from . import style as S

ROOT = Path(__file__).resolve().parents[2]

SYSTEM = """You are FACTSHORTS ENGINE, a Vox + Johnny Harris + Kurzgesagt style shorts writer.
You output ONE minified JSON object and nothing else. No markdown, no commentary.

Schema (exact keys):
{
 "episode": int, "category": "BRAIN FACTS"|"SCIENCE FACTS"|"WORLD FACTS"|"MIND FACTS",
 "topic": str, "disclaimer": short factual caveat string,
 "parts": [ 7 items, each:
   { "idx":1..7, "badge":"HOOK"|"FACT 1".."FACT 5"|"PAYOFF",
     "title": <=46 chars, punchy, no period,
     "subtitle": <=34 chars, the mechanism in plain words,
     "layout": "hook"|"diagram"|"chart"|"timeline"|"payoff",
     "art": "brain_hero"|"brain_glow"|"brain_flat"|"brain_dark"|"brain_cut"|"eye"|"clock_brain"|"chip"|"sleep"|"shield_brain",
     "art2": optional same key list,
     "bottom": "PART tail text, e.g. 'HOOK • 97% people feel it' (<=44 chars)",
     "metric": {"value":"97%","label":"experience it","count":97,"suffix":"%","icon":"people"},
     "bars": [{"label":"Well-Rested","value":50,"color":"gray"},{"label":"Tired","value":100,"display":"2x","color":"yellow"}],
     "columns": [{"icon":"clock","head":"10-30 sec","sub":"average"} x3],
     "headline": str,
     "footnote": str, "cta": str
   } ] }
Part plan: 1 HOOK, 2 FACT 1, 3 FACT 2, 4 FACT 3, 5 FACT 4, 6 FACT 5, 7 PAYOFF.
Layout map: 1->hook, 2->diagram, 3->diagram, 4->timeline, 5->chart, 6->hook, 7->payoff.
Rules: be factually careful, no invented precise statistics - if a number is uncertain use a
qualitative one ("most babies", "1 in 3 people report"). Keep every string SHORT so it fits
1080x1920 without cropping. Include "cta":"Follow for more facts" ONLY in part 7.
Return ONLY the JSON.
"""

FALLBACK = {
    "episode": 43,
    "category": "BRAIN FACTS",
    "topic": "{topic}",
    "parts": [
        {"idx": 1, "badge": "HOOK", "title": "{topic}", "subtitle": "The strange thing your brain does",
         "layout": "hook", "art": "brain_hero", "bottom": "HOOK • most people notice it",
         "metric": {"value": "97%", "label": "experience it", "count": 97, "suffix": "%", "icon": "people"}},
        {"idx": 2, "badge": "FACT 1", "title": "The 200ms Delay", "subtitle": "Your senses run late",
         "layout": "diagram", "art": "brain_flat", "art2": "eye", "bottom": "FACT 1 • 200ms lag",
         "metric": {"value": "200ms", "label": "signal delay", "icon": "eye"},
         "columns": [{"icon": "eye", "head": "200ms", "sub": "eye to brain"},
                     {"icon": "clock", "head": "10-30s", "sub": "the feeling lasts"},
                     {"icon": "people", "head": "97%", "sub": "report it"}]},
        {"idx": 3, "badge": "FACT 2", "title": "Memory Collision", "subtitle": "New feels like old",
         "layout": "diagram", "art": "brain_cut", "bottom": "FACT 2 • signals collide",
         "metric": {"value": "1 in 3", "label": "notice weekly", "icon": "pulse"}},
        {"idx": 4, "badge": "FACT 3", "title": "It Lasts Seconds", "subtitle": "The glitch timeline",
         "layout": "timeline", "art": "clock_brain", "bottom": "FACT 3 • 10-30 sec",
         "columns": [{"icon": "brain", "head": "97%", "sub": "experience"},
                     {"icon": "clock", "head": "10-30 sec", "sub": "average"},
                     {"icon": "people", "head": "then gone", "sub": "feeling fades"}],
         "footnote": "The sensation usually fades before you can hold on to it"},
        {"idx": 5, "badge": "FACT 4", "title": "Tired Brains Get It", "subtitle": "Sleep debt shows up",
         "layout": "chart", "art": "sleep", "bottom": "FACT 4 • tired = more",
         "headline": "Lack of sleep makes it more likely",
         "bars": [{"label": "Well-Rested", "value": 50, "color": "gray"},
                  {"label": "Tired", "value": 100, "display": "2x", "color": "yellow"}],
         "footnote": "Sleep-deprivation studies report roughly double the frequency"},
        {"idx": 6, "badge": "FACT 5", "title": "It's Actually Normal", "subtitle": "Your memory checking itself",
         "layout": "hook", "art": "shield_brain", "bottom": "FACT 5 • normal sign",
         "metric": {"value": "Normal", "label": "healthy process", "icon": "check"}},
        {"idx": 7, "badge": "PAYOFF", "title": "Not Magic, Just Brain", "subtitle": "Your brain updating reality",
         "layout": "payoff", "art": "brain_glow", "bottom": "PAYOFF • not magic",
         "headline": "Just your brain double-checking reality",
         "columns": [{"icon": "clock", "head": "200ms", "sub": "perception delay"},
                     {"icon": "pulse", "head": "collision", "sub": "old + new blend"},
                     {"icon": "check", "head": "healthy", "sub": "self-correcting"}],
         "cta": "Follow for more brain glitches"},
    ],
}


def _balance(fragment: str) -> str:
    """Close any brackets/braces left open by a truncated model reply."""
    out, stack, in_str, esc = [], [], False, False
    for ch in fragment:
        out.append(ch)
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "{[(":
            stack.append({"(": ")", "[": "]", "{": "}"}[ch])
        elif ch in "}])" and stack and stack[-1] == ch:
            stack.pop()
    if in_str:
        out.append('"')
    for closer in reversed(stack):
        out.append(closer)
    return "".join(out).replace(",}", "}").replace(",]", "]")


def _salvage_parts(raw: str) -> list[dict]:
    """Recover whatever complete part objects exist inside a truncated reply."""
    parts = []
    for m in re.finditer(r"\{[^{}]*\"idx\"\s*:\s*(\d+)[^{}]*\}", raw):
        frag = m.group(0)
        try:
            parts.append(json.loads(_balance(frag)))
        except Exception:                                        # noqa: BLE001
            try:
                parts.append(json.loads(re.sub(r",\s*([}\]])", r"\1", _balance(frag))))
            except Exception:                                    # noqa: BLE001
                continue
    seen, uniq = set(), []
    for p in parts:
        if p.get("idx") not in seen:
            seen.add(p.get("idx"))
            uniq.append(p)
    return sorted(uniq, key=lambda d: d.get("idx", 99))


def _unwrap_message(raw: str) -> str:
    """Free-tier reasoning models sometimes return the whole chat message object:
    {"role":"assistant","reasoning":"We need to output…","content":"{…}"}. Dig out content."""
    t = raw.strip()
    try:
        d = json.loads(t)
        if isinstance(d, dict):
            for key in ("content", "text", "response", "message"):
                v = d.get(key)
                if isinstance(v, str) and v.strip():
                    return v
                if isinstance(v, dict) and isinstance(v.get("content"), str):
                    return v["content"]
            if "choices" in d:
                return d["choices"][0]["message"]["content"]
    except Exception:                                            # noqa: BLE001
        pass
    if '"content"' in t:
        m = re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"', t, re.S)
        if m:
            try:
                return json.loads('"' + m.group(1) + '"')
            except Exception:                                    # noqa: BLE001
                return m.group(1)
    if '"reasoning"' in t and "{" not in t.split('"reasoning"')[0][-80:]:
        # the model spent the whole budget thinking and never emitted an answer
        raise ValueError("reasoning-only reply (no content field) — retry with a terser prompt")
    return raw


def _extract_json(raw: str) -> dict:
    """Understands clean JSON, fenced JSON, message-wrapper JSON and half-finished output."""
    raw = _unwrap_message(raw).strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    i = raw.find("{")
    if i < 0:
        raise ValueError("no JSON object in model output")
    body = raw[i:]
    for candidate in (body, body[:body.rfind("}") + 1] if "}" in body else body,
                      _balance(body)):
        if not candidate.strip():
            continue
        try:
            return json.loads(candidate)
        except Exception:                                        # noqa: BLE001
            continue
    salvaged = _salvage_parts(body)
    if salvaged:
        topic = "Unknown"
        m = re.search(r"\"topic\"\s*:\s*\"([^\"]+)", body)
        if m:
            topic = m.group(1)
        return {"topic": topic, "parts": salvaged, "_salvaged": True}
    raise ValueError("could not parse model output as JSON (even after repair)")


def _clean_part(p: dict, idx: int) -> dict:
    p = dict(p or {})
    p["idx"] = idx
    default_badges = ["HOOK"] + [f"FACT {i}" for i in range(1, 6)] + ["PAYOFF"]
    p.setdefault("badge", default_badges[max(0, min(len(default_badges) - 1, idx - 1))])
    p["badge"] = str(p["badge"])[:18]
    p["title"] = str(p.get("title") or "Untitled")[:60].strip()
    p["subtitle"] = str(p.get("subtitle") or "")[:48].strip()
    p["art"] = sanitize_art(p.get("art"), str(p.get("layout") or "hook"))
    if p.get("art2"):
        p["art2"] = sanitize_art(p.get("art2"), "diagram")
    p["bottom"] = str(p.get("bottom") or "")[:48].strip()
    for key in ("headline", "footnote", "cta", "chart_label"):
        v = clean_str(p.get(key))
        if v:
            p[key] = v[:70]
        else:
            p.pop(key, None)
    if p.get("layout") not in {"hook", "hero", "diagram", "chart", "timeline", "payoff"}:
        p["layout"] = "hook"
    m = p.get("metric")
    if isinstance(m, dict):
        m["value"] = clean_str(m.get("value"), 12)
        m["label"] = clean_str(m.get("label"), 24)
        m["count"] = m.get("count") if isinstance(m.get("count"), (int, float)) else None
        m["suffix"] = str(m.get("suffix") or "")[:4]
        m["icon"] = sanitize_icon(m.get("icon"))
        # a metric with no value or no label is not a metric — drop it
        if not m["value"] or not m["label"]:
            p.pop("metric", None)
    cols = p.get("columns") or []
    p["columns"] = [{"icon": sanitize_icon(c.get("icon")), "head": clean_str(c.get("head"), 16),
                     "sub": clean_str(c.get("sub"), 22)} for c in cols[:4]
                    if isinstance(c, dict) and clean_str(c.get("head"))]
    rl = p.get("ruler_labels") or []
    p["ruler_labels"] = [str(x)[:10] for x in rl[:2]]
    bars = p.get("bars") or []
    if p.get("layout") == "chart" and len([b for b in bars if isinstance(b, dict)]) < 2:
        p["layout"] = "hook"        # single-bar "chart" looks broken; hook layout still works
    p["bars"] = [{"label": clean_str(b.get("label"), 18),
                  "value": float(b.get("value", 1) or 1),
                  "display": clean_str(b.get("display"), 6),
                  "color": b.get("color", "yellow")} for b in bars[:3] if isinstance(b, dict)]
    for k in ("headline", "footnote", "cta", "chart_label"):
        if p.get(k):
            p[k] = str(p[k])[:60]
    if idx != 7:
        p.pop("cta", None)
    p.setdefault("duration", float(os.environ.get("FACTSHORTS_PART_SECONDS", 4.5)))
    return p


def build_pack(topic: str, episode: int | None = None, category: str | None = None,
               offline: bool = False, provider: str | None = None) -> dict:
    used_template = False
    if not offline:
        prompt = (f"TOPIC = {topic!r}\nEPISODE = {episode or 43}\nCATEGORY = {category or 'BRAIN FACTS'}\n"
                  f"Write the 7-part FACTSHORTS pack as JSON now. Call to action part only: "
                  f'"Follow for more facts".')
        try:
            pack = _extract_json(text_generate(prompt, SYSTEM, provider=provider, temperature=0.8))
        except Exception as e:                                  # noqa: BLE001
            print(f"  [warn] single-shot script failed ({str(e)[:120]})")
            print("  [info] falling back to 7 small chunked requests…")
            try:
                pack = build_pack_chunked(topic, episode or 43, category or "BRAIN FACTS",
                                          provider=provider)
            except Exception as e2:                             # noqa: BLE001
                used_template = True
                print(f"  [warn] chunked mode failed too ({str(e2)[:120]})")
                print("  [warn] -> built-in example pack. Edit script.json, or:")
                print("  [warn]    python run.py bridge      # copy prompt -> free chat -> paste")
                pack = json.loads(json.dumps(FALLBACK).replace("{topic}", topic[:52]))
    else:
        used_template = True
        pack = json.loads(json.dumps(FALLBACK).replace("{topic}", topic[:52]))

    pack["episode"] = int(episode or pack.get("episode") or 43)      # explicit CLI wins
    pack["category"] = category or pack.get("category") or "BRAIN FACTS"
    pack.setdefault("disclaimer", "")
    fb_texts = {p["title"] for p in json.loads(json.dumps(FALLBACK)
                                               .replace("{topic}", topic[:52]))["parts"]}
    parts = pack.get("parts") or []
    if pack.get("_salvaged"):
        print(f"  [info] repaired a truncated model reply ({len(parts)}/7 parts recovered)")
    if len(parts) != 7:
        fb = json.loads(json.dumps(FALLBACK).replace("{topic}", topic[:52]))["parts"]
        # keep whatever the model produced, fill the gaps with the template
        have = {p.get("idx") for p in parts}
        parts = parts + [f for f in fb if f.get("idx") not in have]
        parts = sorted(parts, key=lambda d: d.get("idx", 99))[:7]
    placeholder = {"", "untitled", "none", "null", "n/a", "unknown"}
    for d in parts:
        if isinstance(d, dict):
            if d.get("title", "").strip().lower() in {t.lower() for t in fb_texts | placeholder}:
                d["_src"] = "template"
            else:
                d.setdefault("_src", "llm")
    pack["parts"] = parts
    pack = fill_derived(pack)
    out = {
        "topic": topic,
        "_generated_by": "builtin-template" if used_template else "llm",
        "episode": int(pack.get("episode", 43)),
        "category": str(pack.get("category", "BRAIN FACTS")),
        "disclaimer": pack.get("disclaimer", ""),
        "parts": [_clean_part(p, i + 1) for i, p in enumerate(parts)],
    }
    return out


def to_parts(pack: dict) -> list[Part]:
    parts = []
    for d in pack["parts"]:
        d = dict(d)
        d["total"] = len(pack["parts"])
        d["episode"] = pack["episode"]
        d["category"] = pack["category"]
        d.setdefault("bottom", "")
        # normalise metrics list from the single-metric schema
        if isinstance(d.get("metric"), dict):
            d["metrics"] = [d["metric"]]
        else:
            d.setdefault("metrics", [])
        d.pop("metric", None)
        d.setdefault("callouts", [])
        parts.append(Part.from_dict(d))
    return parts


def save_pack(pack: dict, out_dir: Path) -> Path:
    """Accepts either a run folder or a direct path to script.json."""
    out_dir = Path(out_dir)
    if out_dir.suffix == ".json":          # caller passed the file itself
        out_dir.parent.mkdir(parents=True, exist_ok=True)
        p = out_dir
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        p = out_dir / "script.json"
    p.write_text(json.dumps(pack, indent=2, ensure_ascii=False))
    return p


# --------------------------------------------------------- derived content
ICON_FOR = {"%": "chart", "x": "pulse", "ms": "clock", "sec": "clock", "min": "clock",
            "off": "warning", "new": "pulse", "rem": "moon", "normal": "check"}

# models sometimes echo the schema ("brain_hero|brain_glow|…") — always pick one real key
VALID_ART = ["brain_hero", "brain_glow", "brain_flat", "brain_dark", "brain_cut",
             "eye", "clock_brain", "chip", "sleep", "shield_brain", "world_map", "suez"]
VALID_ICONS = ["clock", "people", "check", "warning", "brain", "shield", "moon", "chart",
               "eye", "pulse", "delta"]
LAYOUT_ART = {"hook": "brain_hero", "diagram": "brain_cut", "chart": "sleep",
              "timeline": "clock_brain", "payoff": "brain_glow"}

# world/history topics get a world map or the canal illustration instead of brains
WORLD_HINTS = ("canal", "ship", "trade", "route", "map", "empire", "war", "city", "country",
               "sea", "ocean", "river", "railway", "border", "conquest")


def theme_art(topic: str, category: str) -> str | None:
    t, c = (topic or "").lower(), (category or "").lower()
    if any(k in t for k in ("canal", "ship", "trade", "harbour", "harbor", "port")):
        return "suez"
    if any(k in t for k in WORLD_HINTS) or "world" in c or "geo" in c or "history" in c:
        return "world_map"
    return None


def sanitize_art(value, layout: str = "hook") -> str:
    """'brain_hero|brain_glow|…' -> 'brain_hero'; anything unknown -> layout default."""
    if isinstance(value, (list, tuple)):
        value = next((v for v in value if isinstance(v, str)), "")
    for token in str(value or "").replace(",", "|").split("|"):
        token = token.strip().lower()
        if token in VALID_ART:
            return token
    return LAYOUT_ART.get(layout, "brain_hero")


def sanitize_icon(value) -> str:
    token = str(value or "").strip().lower()
    return token if token in VALID_ICONS else "pulse"


def fact_metrics(facts: list[str]) -> list[dict]:
    """Turn '163 km - canal length' lines into metric dicts: value + label + icon."""
    out = []
    for f in facts or []:
        m = re.match(r"^([\d.,]+\s*(?:%|(?:[A-Za-z]{1,12}\s*){0,3}))\s*[-–:]\s*(.{3,140})$", f.strip(), re.I)
        if not m:
            continue
        value, label = m.group(1).strip(), m.group(2).strip().rstrip(".")
        if len(value) > 14:                      # keep the big yellow number short
            value = " ".join(value.split()[:2])
        if len(label) > 40:                      # long fact prose -> tight caption
            label = label[:40].rsplit(" ", 1)[0].rstrip(",;:")
        if not value:
            continue
        icon = "clock"
        low = (value + " " + label).lower()
        if any(k in low for k in ("km", "m ", "mi", "mile", "long", "wide", "deep")):
            icon = "chart"
        elif any(k in low for k in ("%", "percent")):
            icon = "chart"
        elif any(k in low for k in ("worker", "people", "men")):
            icon = "people"
        elif any(k in low for k in ("year", "18", "19", "20", "month", "day")):
            icon = "clock"
        out.append({"value": value[:12], "label": label[:24], "icon": icon})
    return out


def _icon_for(metric: dict) -> str:
    v = str(metric.get("value", "")).lower()
    suf = str(metric.get("suffix", "")).lower()
    for key, icon in ICON_FOR.items():
        if suf == key or v.endswith(key):
            return icon
    return metric.get("icon") or "pulse"


def derive_columns(pack: dict, target_idx: int, count: int = 3) -> list[dict]:
    """Build summary columns from the metrics/bars/footnotes the script already has.

    Free reasoning models choke on the 3-column payoff schema, so we derive it instead of
    asking: the payoff slide ends up describing THIS topic's own numbers.
    """
    cols: list[dict] = []
    for p in pack.get("parts", []):
        if int(p.get("idx", 0)) == int(target_idx):
            continue
        m = p.get("metric") or {}
        if m.get("value"):
            sub = str(m.get("label") or p.get("subtitle") or "")[:20]
            cols.append({"icon": _icon_for(m), "head": str(m["value"])[:14], "sub": sub})
        elif p.get("bars"):
            b = max(p["bars"], key=lambda x: float(x.get("value") or 0))
            cols.append({"icon": "chart", "head": str(b.get("display") or b.get("label", ""))[:14],
                         "sub": str(p.get("subtitle") or p.get("title", ""))[:20]})
        elif p.get("columns"):
            cols.append(dict(p["columns"][0]))
        if len(cols) >= count:
            break
    filler = [{"icon": "brain", "head": "your brain", "sub": "doing its job"},
              {"icon": "pulse", "head": "day to day", "sub": "nothing broken"},
              {"icon": "check", "head": "totally normal", "sub": "no fix needed"}]
    while len(cols) < count:
        cols.append(filler[len(cols) % len(filler)])
    # de-duplicate heads so the three columns never read the same
    seen: set[str] = set()
    for c in cols:
        base = c["head"]
        i = 1
        while c["head"].lower() in seen:
            i += 1
            c["head"] = f"{base} {i}"
        seen.add(c["head"].lower())
    return cols


TITLE_FALLBACKS = {
    "payoff": "So Next Time You Notice It",
    "timeline": "How Long It Lasts",
    "chart": "What Makes It Worse",
    "diagram": "What Is Really Happening",
    "hook": "What Your Brain Is Doing",
}


def _is_placeholder_title(title: str) -> bool:
    return str(title or "").strip().lower() in {"", "untitled", "none", "null", "n/a", "unknown"}


PLACEHOLDER_TEXT = {"short tail", "short metric tail", "<=44 chars", "<=40 chars", "tail",
                    "metric tail", "your metric here", "n/a", "todo", "tbd"}


TAIL_STOP = {"of", "the", "a", "an", "in", "during", "for", "at", "on", "by", "to",
             "and", "its", "it", "is", "was", "were", "with", "from", "into", "per"}
TAIL_MOD = {"maximum", "minimum", "total", "estimated", "average", "approx", "approximately",
            "overall", "about", "around", "roughly", "entire", "whole", "full",
            "new", "more", "fewer", "less", "number", "amount", "value", "level", "number"}


def short_tail(value, label, limit: int = 32) -> str:
    """'120.7 km' + 'length of the Suez Canal' -> '120.7 km length' (bar-friendly)."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", clean_str(label))
    head = next((w for w in words if w.lower() not in TAIL_MOD and w.lower() not in TAIL_STOP), "")
    tail = " ".join(x for x in (clean_str(value), head.lower()) if x)
    return (tail or clean_str(value) or clean_str(label))[:limit]


NULLISH = {"none", "null", "nil", "n/a", "na", "undefined", "nan", "-", "—"}


def clean_str(value, limit: int = 0) -> str:
    """Model output -> safe string: None/'None'/'null' all collapse to ''."""
    v = str(value if value is not None else "").strip()
    if v.lower() in NULLISH:
        v = ""
    return v[:limit] if limit else v


def _is_placeholder_text(value) -> bool:
    v = str(value or "").strip().lower()
    return (not v) or v in PLACEHOLDER_TEXT or "<=" in v or v.startswith("your ") \
        or "chars" in v


def fill_derived(pack: dict) -> dict:
    """Give every layout the content it needs, without another model request.

    Uses the topic's real facts (pack['_facts']) so a metric is never a made-up digit.
    """
    parts = pack.get("parts", [])
    topic = str(pack.get("topic") or "").strip()
    if not pack.get("_facts"):
        try:                                     # self-heal: never render a pack without real numbers
            pack["_facts"] = topic_facts(str(pack.get("topic") or ""),
                                         str(pack.get("category") or ""))
        except Exception:                        # noqa: BLE001
            pass
    fm = fact_metrics(pack.get("_facts") or [])
    used: set[str] = {clean_str((q.get("metric") or {}).get("value")) for q in parts}
    used.discard("")                    # seed from already-assigned metrics: never repeat a number
    theme = theme_art(topic, str(pack.get("category") or ""))
    if theme:
        secondary = "world_map" if theme in ("suez", "world_map") else "eye"
        for p_ in parts:
            art = str(p_.get("art") or "")
            if art.startswith("brain") or not art or art == "eye":
                p_["art"] = theme
            a2 = str(p_.get("art2") or "")
            if not a2 or a2.startswith("brain") or a2 == "eye":
                p_["art2"] = secondary
    for p in parts:
        layout = p.get("layout")
        if _is_placeholder_title(p.get("title")):
            base = TITLE_FALLBACKS.get(layout, "What Is Happening")
            p["title"] = base if not topic else base
            p["_src"] = "derived"
        if not str(p.get("subtitle") or "").strip():
            p["subtitle"] = str(pack.get("category") or "Brain facts").title()[:40]
        if _is_placeholder_text(p.get("bottom")):
            m = p.get("metric") or {}
            tail = " ".join(x for x in (str(m.get("value") or ""), str(m.get("label") or "")) if x)
            if not tail and p.get("headline"):
                tail = str(p["headline"])[:34]
            if not tail and p.get("bars"):
                tail = str(p["bars"][-1].get("display") or p["bars"][-1].get("label") or "")[:34]
            p["bottom"] = f"{p.get('badge', 'PART')}" + (f" • {tail}" if tail else "")
        if _is_placeholder_text(p.get("subtitle")):
            p["subtitle"] = str(pack.get("category") or "Explained").title()[:40]
        if layout == "payoff" and not p.get("headline"):
            p["headline"] = f"{topic} — not magic, just your brain"[:56]
        # real-number metrics from the facts list for any hook/diagram/timeline part
        if layout in ("hook", "diagram", "timeline"):
            if not (p.get("metric") or {}).get("value") or weak_metric(p):
                pick = next((f for f in fm if f["value"] not in used), None) if fm else None
                if pick:
                    used.add(pick["value"])
                    p["metric"] = dict(pick, count=None, suffix="")
                    p["bottom"] = short_tail(pick["value"], pick["label"])
                    if p.get("_src") == "template":
                        p["_src"] = "derived"
                else:
                    p.pop("metric", None)      # honest: no number beats a made-up number
        if layout in ("payoff", "hook") and not p.get("columns"):
            p["columns"] = derive_columns(pack, int(p.get("idx", 0)))
        if layout == "timeline" and not p.get("columns"):
            p["columns"] = derive_columns(pack, int(p.get("idx", 0)))
        if layout == "payoff":
            p.setdefault("cta", "Follow for more facts")
            if not p.get("headline"):
                p["headline"] = f"{pack.get('topic', 'It')} — not magic, just your brain"
        if layout == "chart" and len(p.get("bars") or []) < 2:
            other = next((q for q in parts if q is not p and (q.get("metric") or {}).get("value")), None)
            p["bars"] = [{"label": "Normal", "value": 50, "display": "normal", "color": "gray"},
                         {"label": "Triggered", "value": 100, "display": "2x", "color": "yellow"}]
            if other:
                p["footnote"] = p.get("footnote") or f"Compared with a normal {other['badge'].lower()}"
    pack["parts"] = parts
    return pack


def normalize_pack(pack: dict) -> dict:
    """Make ANY script.json safe to render: hand-written, half-edited or repaired.

    Guarantees: 7 parts, every required key present with the right type, no "None" strings.
    """
    pack = dict(pack or {})
    topic = str(pack.get("topic") or "Untitled Topic")
    fb = json.loads(json.dumps(FALLBACK).replace("{topic}", topic[:52]))["parts"]
    raw_parts = pack.get("parts") or []
    fixed: list[dict] = []
    for i, d in enumerate(raw_parts, 1):
        if not isinstance(d, dict):
            continue
        try:
            fixed.append(_clean_part(d, int(d.get("idx") or i)))
        except Exception:                                        # noqa: BLE001
            fixed.append(_clean_part(fb[min(i, 7) - 1], i))
    have = {p["idx"] for p in fixed}
    fixed += [f for f in fb if f["idx"] not in have]
    fixed = sorted({p["idx"]: p for p in fixed}.values(), key=lambda p: p["idx"])[:7]
    PLACEHOLDER_TITLES = {"", "untitled", "none", "null", "n/a", "unknown"}
    fb_titles = {f["title"] for f in fb} | PLACEHOLDER_TITLES
    for p_ in fixed:
        # the title is the source of truth: if it is still example/empty text, it IS a placeholder
        p_["_src"] = "template" if p_["title"].strip().lower() in {t.lower() for t in fb_titles} \
            else p_.get("_src", "llm")
    pack["topic"] = topic
    pack["parts"] = fixed
    pack.setdefault("episode", 43)
    pack.setdefault("category", "BRAIN FACTS")
    return fill_derived(pack)


def load_pack(path: Path, normalize: bool = True) -> dict:
    pack = json.loads(Path(path).read_text())
    return normalize_pack(pack) if normalize else pack


# ---------------------------------------------------------------- chunked mode
PLAN = [
    ("HOOK",   "hook",     "the hook: a mystery question that stops the scroll"),
    ("FACT 1", "diagram",  "the first mechanism, a signal path with blue arrows"),
    ("FACT 2", "diagram",  "the second mechanism, what misfires inside"),
    ("FACT 3", "timeline", "how long it lasts, a 0-to-N ruler bar"),
    ("FACT 4", "chart",    "the trigger, a two-bar comparison (normal vs triggered)"),
    ("FACT 5", "hook",     "the twist: why it is actually normal or useful"),
    ("PAYOFF", "payoff",   "three icon takeaways plus a call to action"),
]

PART_SCHEMA = ('{"idx":%d,"badge":"%s","title":"<=44 chars, punchy, no period",'
               '"subtitle":"<=30 chars","layout":"%s","art":"brain_hero|brain_glow|brain_flat|'
               'brain_dark|brain_cut|eye|clock_brain|chip|sleep|shield_brain",'
               '"bottom":"BADGE - short metric tail, <=40 chars",'
               '"metric":{"value":"<=10 chars","label":"<=22 chars","count":number|null,'
               '"suffix":"%%|x|ms|sec|","icon":"clock|people|brain|check|warning|pulse|eye|chart|moon|shield"},'
               '"bars":[{"label":"<=16 chars","value":number,"display":"<=5 chars","color":"gray|yellow"}],'
               '"columns":[{"icon":"clock","head":"<=14 chars","sub":"<=20 chars"}],'
               '"headline":"<=48 chars","footnote":"<=70 chars","cta":"only for part 7"}')


STRICT_SUFFIX = ("\nIMPORTANT: reply with ONE line of minified JSON only. It must start with "
                 "{ and end with }. No prose, no markdown, no code fences, no explanation.")


def topic_facts(topic: str, category: str = "", provider: str | None = None) -> list[str]:
    """One small ask for real, checkable numbers about the topic (year / distance / count).

    These get injected into the per-part prompts so metrics are actual facts instead of
    whatever number the model felt like inventing.
    """
    prompt = (f'Topic: "{topic}". List the 5 most verifiable numbers about it '
              f'(years, distances, counts, percentages). Format: one per line, '
              f'"number - what it is". No prose, no markdown.')
    def _parse(raw: str) -> list[str]:
        facts = []
        for line in (raw or "").splitlines():
            line = line.strip(" -*•\t")
            if 4 <= len(line) <= 90 and any(ch.isdigit() for ch in line):
                facts.append(line)
        return facts[:5]

    try:
        facts = _parse(text_generate(prompt, "Answer with plain lines only.",
                                     provider=provider, temperature=0.4, max_tokens=400))
        if not facts:            # cached/soft reply had no numbers -> ask once, fresh, rephrased
            os.environ["FACTSHORTS_NOCACHE"] = "1"
            try:
                facts = _parse(text_generate(
                    f'Give 5 real numbers about "{topic}" (e.g. "163 km - canal length"). '
                    f'One per line: number, dash, what it is.', "Plain lines only, no prose.",
                    provider=provider, temperature=0.3, max_tokens=300))
            finally:
                os.environ.pop("FACTSHORTS_NOCACHE", None)
        if facts:
            print(f"  [facts] {len(facts)} real numbers: {facts[0][:44]}")
        else:
            print("  [facts] model returned no usable numbers")
        return facts
    except Exception as e:                                       # noqa: BLE001
        print(f"  [facts] unavailable ({str(e)[:60]})")
        return []


def weak_metric(p: dict) -> bool:
    """'7' with no label is not a fact — flag metrics that carry no information."""
    m = p.get("metric") or {}
    if not m:
        return False
    val = str(m.get("value") or "").strip()
    lab = str(m.get("label") or "").strip()
    if not val:
        return True
    if len(lab) < 3:
        return True
    # a bare 1-2 digit number ("7", "8%") is noise, whatever suffix the model invented
    if val.isdigit() and len(val) <= 2:
        return True
    return False


def _one_part(topic: str, idx: int, category: str, provider: str | None,
              attempts: int = 2) -> dict | None:
    badge, layout, desc = PLAN[idx - 1]
    schema = PART_SCHEMA % (idx, badge, layout)
    base_prompt = (f'Topic: "{topic}" (category {category}). Write part {idx} of 7: {desc}.\n'
                   f"Return ONLY this JSON object, filled in, nothing else:\n{schema}\n"
                   f"Do not explain, do not think out loud — output the JSON immediately.")
    example = ('{"idx":%d,"badge":"%s","title":"Your Clock Runs Slow","subtitle":"It is not you",'
               '"layout":"%s","art":"clock_brain","bottom":"%s - 2x faster",'
               '"metric":{"value":"2x","label":"feels faster","count":2,"suffix":"x","icon":"clock"},'
               '"bars":[],"columns":[{"icon":"clock","head":"1 year","sub":"feels like 6 months"}],'
               '"headline":"","footnote":""}' % (idx, badge, layout, badge))
    for a in range(attempts):
        # retries must NOT read the cache: a cached bad reply would be replayed forever
        prompt = base_prompt if a == 0 else (
            f"Example of the exact shape (use your own words for \"{topic}\"):\n{example}\n"
            + base_prompt + STRICT_SUFFIX)
        try:
            prov = provider or os.environ.get("FACTSHORTS_CHUNK_PROVIDER", "pollinations-get")
            raw = text_generate(prompt, "Output one minified JSON object. No prose.",
                                provider=prov, temperature=0.85 if a == 0 else 0.45,
                                max_tokens=1600, use_cache=(a == 0))
            obj = _extract_json(raw)
            if isinstance(obj.get("parts"), list) and obj["parts"]:
                obj = obj["parts"][0]
            obj["idx"] = idx
            obj.setdefault("badge", badge)
            obj.setdefault("layout", layout)
            title = str(obj.get("title") or "").strip()
            usable = (len(title) >= 4 and title.lower() not in ("none", "null", "untitled")
                      and "<=" not in title                       # not a schema echo
                      and (any(obj.get(k) for k in ("metric", "bars", "columns", "headline"))
                           or obj.get("layout") in ("hook", "diagram")))
            if not usable:
                raise ValueError(f"reply had no usable content (title={title[:24]!r})")
            obj["_src"] = "llm"
            return obj
        except Exception as e:                                   # noqa: BLE001
            print(f"  [warn] part {idx} attempt {a + 1}/{attempts} failed ({str(e)[:70]})")
            time.sleep(float(os.environ.get("FACTSHORTS_CHUNK_BACKOFF", 8)) * (a + 1))
    return None


# --- lite schemas: only the fields that the part's layout actually renders.
# Reasoning models burn their whole budget "thinking" about the big schema, so the last
# attempt asks for the smallest possible object.
LITE_SCHEMA = {
    "timeline": ('{{"idx":{idx},"badge":"{badge}","title":"<=44 chars","subtitle":"<=30 chars",'
                 '"bottom":"short tail","columns":[{{"icon":"clock","head":"<=14","sub":"<=20"}},'
                 '{{"icon":"brain","head":"<=14","sub":"<=20"}},{{"icon":"people","head":"<=14",'
                 '"sub":"<=20"}}],"ruler_labels":["0","N"],"footnote":"<=70 chars"}}'),
    "chart": ('{{"idx":{idx},"badge":"{badge}","title":"<=44 chars","subtitle":"<=30 chars",'
              '"bottom":"short tail","headline":"<=48 chars","bars":[{{"label":"<=16","value":50,'
              '"display":"low","color":"gray"}},{{"label":"<=16","value":100,"display":"high",'
              '"color":"yellow"}}],"footnote":"<=70 chars"}}'),
    "payoff": ('{{"idx":{idx},"badge":"{badge}","title":"<=44 chars","subtitle":"<=30 chars",'
               '"bottom":"short tail","headline":"<=48 chars","columns":[{{"icon":"clock",'
               '"head":"<=14","sub":"<=20"}},{{"icon":"pulse","head":"<=14","sub":"<=20"}},'
               '{{"icon":"check","head":"<=14","sub":"<=20"}}],"cta":"Follow for more"}}'),
    "hook": ('{{"idx":{idx},"badge":"{badge}","title":"<=44 chars","subtitle":"<=30 chars",'
             '"bottom":"short tail","metric":{{"value":"<=10","label":"<=22","count":null,'
             '"suffix":"%","icon":"clock"}}}}'),
    "diagram": ('{{"idx":{idx},"badge":"{badge}","title":"<=44 chars","subtitle":"<=30 chars",'
                '"bottom":"short tail","metric":{{"value":"<=10","label":"<=22","count":null,'
                '"suffix":"%","icon":"brain"}}}}'),
}


def _lite_reply(topic: str, idx: int, category: str, provider: str | None,
                facts: list[str] | None = None) -> dict | None:
    badge, layout, desc = PLAN[idx - 1]
    tpl = LITE_SCHEMA.get(layout, LITE_SCHEMA["hook"]).format(idx=idx, badge=badge)
    fact_line = ("\nUse only these real numbers (pick the one that fits):\n"
                 + "\n".join(f"- {f}" for f in (facts or [])[:5])) if facts else ""
    prompt = (f'Topic: "{topic}". Write the {badge} slide ({desc}) of a 7-part short.{fact_line}\n'
              f"Fill this JSON with your own short words and return it on ONE line:\n{tpl}")
    try:
        raw = text_generate(prompt, "Output one minified JSON object. No prose, no thinking.",
                            provider=provider or os.environ.get("FACTSHORTS_CHUNK_PROVIDER",
                                                               "pollinations-get"),
                            temperature=0.5, max_tokens=2000, use_cache=False)
        obj = _extract_json(raw)
        obj["idx"], obj["badge"], obj["layout"] = idx, badge, layout
        if not str(obj.get("title") or "").strip():
            raise ValueError("empty title")
        obj["_src"] = "llm"
        print(f"  [fill] part {idx} recovered via lite schema")
        return obj
    except Exception as e:                                       # noqa: BLE001
        print(f"  [warn] part {idx} lite attempt failed ({str(e)[:80]})")
        return None


def build_pack_chunked(topic: str, episode: int = 43, category: str = "BRAIN FACTS",
                       provider: str | None = None) -> dict:
    """Seven small prompts instead of one large one — survives low token limits."""
    parts, delay = [], float(os.environ.get("FACTSHORTS_CHUNK_DELAY", 5))
    for i in range(1, 8):
        # small ask first: reasoning models answer compact schemas far more reliably
        p = _lite_reply(topic, i, category, provider) or _one_part(topic, i, category, provider)
        if p:
            parts.append(p)
        else:
            fb = json.loads(json.dumps(FALLBACK).replace("{topic}", topic[:52]))["parts"][i - 1]
            fb["_src"] = "template"
            parts.append(fb)
        src = "llm" if (p and p.get("_src") == "llm") else "template"
        print(f"  [chunk] {len(parts)}/7 parts ready ({src} for part {i})")
        if i < 7:
            time.sleep(delay)                                    # be polite to the free tier
    return {"topic": topic, "episode": episode, "category": category,
            "_generated_by": "llm-chunked", "parts": parts, "disclaimer": ""}


def stale_parts(pack: dict) -> list[int]:
    """Parts that are placeholders, broken, or carry a meaningless metric."""
    """Which parts still carry placeholder content (need regenerating or hand-editing)."""
    fb = json.loads(json.dumps(FALLBACK).replace("{topic}", pack.get("topic", "")[:52]))["parts"]
    fb_titles = {p["title"] for p in fb}
    fm = fact_metrics(pack.get("_facts") or [])
    used = {clean_str((q.get("metric") or {}).get("value")) for q in pack.get("parts", [])}
    pack["_fm_unused"] = [f for f in fm if f["value"] not in used]   # real numbers nobody used yet
    out = []
    for p in pack.get("parts", []):
        title = str(p.get("title") or "").strip()
        broken = (not title) or title.lower() in ("untitled", "none", "n/a")
        no_number = p.get("layout") in ("hook", "diagram", "timeline") and \
            not clean_str((p.get("metric") or {}).get("value")) and \
            bool([f for f in pack.get("_fm_unused") or []])
        caps = title.isupper() and len(title) > 15          # model shouting = unfinished copy
        if p.get("_src") == "template" or broken or title in fb_titles or weak_metric(p) \
                or no_number or caps:
            out.append(int(p.get("idx", 0)))
    return sorted(out)


def repair_pack(pack: dict, only: list[int] | None = None, save_path: Path | None = None) -> dict:
    """Re-generate just the stale parts, one small request each. Used by `run.py fill`.

    Saves after EVERY part (when save_path is given), so an interrupted run keeps its progress
    instead of losing the whole repair pass.
    """
    topic, category = pack.get("topic", ""), pack.get("category", "BRAIN FACTS")
    idxs = only or stale_parts(pack)
    if not idxs:
        print("  nothing stale — every part is LLM-written")
        return pack
    print(f"  repairing parts: {idxs}")
    by_idx = {int(p["idx"]): p for p in pack["parts"]}
    if not pack.get("_facts"):
        pack["_facts"] = topic_facts(topic, category)
    facts = pack.get("_facts") or []
    for i in idxs:
        new = (_lite_reply(topic, i, category, None, facts)
               or _one_part(topic, i, category, None, attempts=2))
        if new:
            new = _clean_part(new, i)          # same validation the normal path uses
            new["_src"] = "llm"
            new["idx"] = i
            by_idx[i] = new
            print(f"  [fill] part {i} refreshed: {new.get('title','?')[:40]!r}")
        else:
            print(f"  [fill] part {i} still unavailable — edit it by hand in script.json")
        pack["parts"] = [by_idx[j] for j in sorted(by_idx)]
        if save_path:
            save_pack(fill_derived(dict(pack, parts=[dict(x) for x in pack["parts"]])), Path(save_path))
        time.sleep(float(os.environ.get("FACTSHORTS_CHUNK_DELAY", 5)))
    pack["parts"] = [by_idx[i] for i in sorted(by_idx)]
    pack = fill_derived(pack)
    pack["_generated_by"] = "llm+repair"
    pack["parts"] = [dict(p, _src=("llm" if str(p.get("title", "")).strip().lower()
                                   not in {"", "untitled", "none"} else "template")) for p in pack["parts"]]
    return pack
