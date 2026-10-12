"""Any coding / AI-tools topic -> teacher-style lesson JSON (Gemini), with checks.

Flow:
  1. Topic gate  : Gemini se check: kya ye real, teachable topic hai? (gibberish reject)
  2. Generate    : prompts/gemini_teacher_prompt.md + topic -> lesson JSON
  3. Lint        : schema, anchors narration mein hain, banned phrases, narration length
  4. Save        : tests/lesson_<slug>.json  (phir build_video.py se video)

Usage:
  export GEMINI_API_KEY=...
  python3 pipeline/topic_to_lesson.py "Python dictionaries" --series python-100-days --lang en --day 3
  python3 pipeline/topic_to_lesson.py "dsksjha"                 # gate pe reject hoga
  python3 pipeline/topic_to_lesson.py "Git branches" --dry-run  # key ke bina: prompt file banao

Gemini model: env GEMINI_MODEL (default gemini-2.5-flash). Verify karo ki aapke account par ye model available hai.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def _load_dotenv():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

_load_dotenv()

PROMPT = ROOT / "prompts" / "gemini_teacher_prompt.md"
TESTS = ROOT / "tests"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")


API = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"


ALLOWED_TYPES = {"TitleCard", "TypingCode", "TerminalRun", "ComparisonCard", "SummaryList", "StatChart", "ArchitectureFlow", "OutroCard", "CodeExplainer", "BrowserSteps",
                 "ArrayViz", "TreeViz", "GraphViz", "StackQueueViz", "DiagramFlow"}
BANNED = ["in this video", "let's dive in", "delve", "unlock", "game-changer", "game changer",
          "seamlessly", "robust", "leverage", "moreover", "furthermore", "fast-paced"]
WPS_MIN, WPS_MAX = 1.6, 3.2   # words per second (spoken English/Hinglish)
SCENE_SEC_MIN, SCENE_SEC_MAX = 10, 30   # slow teaching: scene 10-30 sec
MIN_SCENES = 12
MIN_WORDS = 20      # isse kam narration = jaldi bolna (error)
TARGET_WORDS = 25   # isse kam = warning


def gemini_json(prompt: str, key: str) -> dict:
    import time
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.6}}
    models_to_try = [MODEL, "gemini-3.1-flash-lite-preview", "gemini-3-flash-preview"]
    last_err = None
    for m in models_to_try:
        for attempt in range(3):
            try:
                url = API.format(m=m, k=key)
                req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                             headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = json.loads(r.read())
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code in (503, 429):
                    time.sleep(2 * (attempt + 1))
                    continue
                break
            except Exception as e:
                last_err = e
                time.sleep(1)
    raise last_err or RuntimeError("Gemini API calls failed.")



GATE_PROMPT = """You check whether a text is a real, teachable topic for a coding or AI-tools
YouTube lesson (programming languages, libraries, algorithms, git, AI/ML tools, etc.).

Return JSON only:
{"valid": true|false, "reason": "short reason in English",
 "normalized_topic": "clean English title, e.g. 'Python dictionaries'",
 "category": "coding|ai_tools|other", "level": "beginner|intermediate|advanced"}

Mark valid=false for random characters, gibberish, non-topics, or anything not teachable.
Topic: """


def gate(topic: str, key: str) -> dict:
    return gemini_json(GATE_PROMPT + topic, key)


def build_prompt(topic: str, series: str, lang: str, day: int | None, fmt: str = "long") -> str:
    tpl = PROMPT.read_text(encoding="utf-8")
    lang_name = {"en": "English", "hi": "Hindi (Hinglish-Devanagari, English tech words in Latin)"}[lang]
    golden = (ROOT / "prompts" / "examples" / "golden_lesson.json").read_text(encoding="utf-8")
    tpl = tpl + "\n\nGOLDEN EXAMPLE (quality bar, different topic):\n" + golden
    if fmt == "short":
        tpl = tpl + SHORT_NOTE
    return (tpl.replace("{LANG}", lang_name).replace("{TOPIC}", topic)
            .replace("{SERIES}", series or "standalone").replace("{DAY}", str(day or "n/a")))


SHORT_NOTE = """

SHORT FORMAT (YouTube Short, 9:16, 40 to 45 seconds total):
- Exactly 4 or 5 scenes. Total narration 100 to 125 words across all scenes.
- Scene 1 is a hook: a question or surprising fact in the first 3 seconds. Use TitleCard or a DSA/diagram visual.
- One single idea only. No long setup. Each scene 8 to 14 seconds.
- Last scene: OutroCard with a short call to action ("Full lesson ke liye link dekho"). Keep it English.
- Use only the allowed scene types. Visuals stay simple (big text, one diagram).
"""


def lint_short(lesson: dict) -> list[str]:
    """Shorts ke liye lint: 4-5 scenes, total 100-125 words, allowed types, banned phrases."""
    errs = []
    scenes = lesson.get("scenes") or []
    if not 4 <= len(scenes) <= 5:
        errs.append(f"short: scenes {len(scenes)} (4 ya 5 chahiye)")
    total = sum(len((x.get("narration") or "").split()) for x in scenes)
    if not 100 <= total <= 125:
        errs.append(f"short: total narration {total} words (100-125 chahiye, ~40-45 sec)")
    for i, x in enumerate(scenes, 1):
        rem = x.get("remotion") or {}
        if rem.get("type") not in ALLOWED_TYPES:
            errs.append(f"short scene {i}: unknown type '{rem.get('type')}'")
        low = (x.get("narration") or "").lower()
        for b in BANNED:
            if b in low:
                errs.append(f"short scene {i}: banned phrase '{b}'")
    return errs


def looks_like_gibberish(topic: str) -> bool:
    """Gemini se pehle sasta check: 6+ consonants lagatar wala word = gibberish (jaise 'dsksjh')."""
    words = re.findall(r"[A-Za-z]+", topic)
    if not words:
        return True
    for w in words:
        for run in re.findall(r"[^aeiouy]+", w.lower()):
            if len(run) >= 6:
                return True
    return False


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:60]


def lint(lesson: dict, lang: str) -> list[str]:
    errs, warns = [], []
    if not lesson.get("title"):
        errs.append("title missing")
    scenes = lesson.get("scenes") or []
    if len(scenes) < MIN_SCENES:
        errs.append(f"scenes kam hain ({len(scenes)}), kam se kam {MIN_SCENES} chahiye (slow teaching)")
    # Concept pehle, code baad mein: pehle 2 scenes mein code/terminal nahi
    for i, s0 in enumerate(scenes[:2], 1):
        if (s0.get("remotion") or {}).get("type") in ("TypingCode", "TerminalRun"):
            errs.append(f"scene {i}: pehle concept samjhao, code/terminal scene pehle 2 mein nahi")
    for i, s in enumerate(scenes, 1):
        tag = f"scene {i}"
        narr = (s.get("narration") or "").strip()
        if not narr:
            errs.append(f"{tag}: narration khali")
            continue
        rem = s.get("remotion") or {}
        if rem.get("type") not in ALLOWED_TYPES:
            errs.append(f"{tag}: unknown type '{rem.get('type')}'")
        if not isinstance(rem.get("props"), dict):
            errs.append(f"{tag}: props object chahiye")
        low = narr.lower()
        for b in BANNED:
            if b in low:
                errs.append(f"{tag}: banned phrase '{b}' (AI jaisa lagega)")
        words = len(narr.split())
        lo, hi = words / WPS_MAX, words / WPS_MIN   # seconds range
        if words < MIN_WORDS:
            errs.append(f"{tag}: narration bahut chhota ({words} words, kam se kam {MIN_WORDS}) - slow samjhao")
        elif words < TARGET_WORDS:
            warns.append(f"{tag}: narration thoda chhota ({words} words)")
        for cam in (rem.get("camera") or []):
            ca = cam.get("at")
            if ca and ca.lower() not in low:
                errs.append(f"{tag}: camera anchor '{ca}' narration mein nahi hai")
        if lo < SCENE_SEC_MIN or hi > SCENE_SEC_MAX:
            warns.append(f"{tag}: narration length ~{lo:.0f}-{hi:.0f}s (target {SCENE_SEC_MIN}-{SCENE_SEC_MAX}s)")
        for p in (s.get("popups") or rem.get("popups") or []):
            a = p.get("anchor", "")
            if a and a.lower() not in low:
                errs.append(f"{tag}: popup anchor '{a}' narration mein nahi hai")
        ta = rem.get("type_anchor")
        if ta and ta.lower() not in low:
            errs.append(f"{tag}: type_anchor '{ta}' narration mein nahi hai")
    for i, x in enumerate(scenes, 1):
        rem = x.get("remotion") or {}
        if rem.get("type") == "BrowserSteps":
            st = (rem.get("props") or {}).get("steps") or []
            if len(st) < 2:
                errs.append(f"scene {i}: BrowserSteps mein kam se kam 2 steps chahiye")
            for j, step in enumerate(st, 1):
                if step.get("type") == "click" and not step.get("label"):
                    errs.append(f"scene {i} step {j}: click step ko label chahiye")
                if step.get("type") == "navigate" and not step.get("url"):
                    warns.append(f"scene {i} step {j}: navigate step mein url nahi")
    # DSA visuals: steps zaroori, aur har step ka label
    dsa_req = {"ArrayViz": ["values"], "TreeViz": ["root", "nodes"], "GraphViz": ["nodes", "edges"], "StackQueueViz": ["kind"]}
    for i, x in enumerate(scenes, 1):
        rem = x.get("remotion") or {}
        typ = rem.get("type")
        if typ not in dsa_req:
            continue
        props = rem.get("props") or {}
        st = props.get("steps") or []
        if len(st) < 2:
            errs.append(f"scene {i}: {typ} mein kam se kam 2 steps chahiye (har step ek state)")
        for j, step in enumerate(st, 1):
            if not step.get("label"):
                errs.append(f"scene {i} step {j}: {typ} step ko label chahiye")
        for key in dsa_req[typ]:
            if not props.get(key):
                errs.append(f"scene {i}: {typ} mein '{key}' missing")
    # DiagramFlow (boxes + arrows): nodes/edges valid, arrow index edges ke andar, step label
    for i, x in enumerate(scenes, 1):
        rem = x.get("remotion") or {}
        if rem.get("type") != "DiagramFlow":
            continue
        props = rem.get("props") or {}
        nodes = props.get("nodes") or []
        edges = props.get("edges") or []
        ids = {n.get("id") for n in nodes}
        if len(nodes) < 2:
            errs.append(f"scene {i}: DiagramFlow mein kam se kam 2 nodes chahiye")
        if not edges:
            errs.append(f"scene {i}: DiagramFlow mein edges (arrows) chahiye")
        for j, e in enumerate(edges):
            if e.get("from") not in ids or e.get("to") not in ids:
                errs.append(f"scene {i}: edge {j} ke from/to node id exist nahi karte")
        st = props.get("steps") or []
        if len(st) < 2:
            errs.append(f"scene {i}: DiagramFlow mein kam se kam 2 steps chahiye")
        for j, step in enumerate(st, 1):
            if not step.get("label"):
                errs.append(f"scene {i} step {j}: DiagramFlow step ko label chahiye")
            if "arrow" in step and not (isinstance(step["arrow"], int) and 0 <= step["arrow"] < len(edges)):
                errs.append(f"scene {i} step {j}: arrow index galat hai")
    # Visual recommendations (warning): chapter label + key idea cards
    if not any(((x.get("remotion") or {}).get("chapter") or x.get("chapter")) for x in scenes):
        warns.append("chapter label kisi scene mein nahi (module ka naam dikhao)")
    if not any(((x.get("remotion") or {}).get("keyIdea") or x.get("keyIdea")) for x in scenes):
        warns.append("keyIdea kisi scene mein nahi (2-3 key takeaway cards daalo)")
    for i, x in enumerate(scenes, 1):
        ki = (x.get("remotion") or {}).get("keyIdea") or x.get("keyIdea")
        if ki and len(ki.split()) > 10:
            warns.append(f"scene {i}: keyIdea 10 words se bada ({len(ki.split())})")
    if warns:
        print("WARN:\n  " + "\n  ".join(warns))
    return errs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--series", default="")
    ap.add_argument("--lang", default="en", choices=["en", "hi"])
    ap.add_argument("--day", type=int)
    ap.add_argument("--dry-run", action="store_true", help="API call nahi, sirf prompt file")
    a = ap.parse_args()

    if looks_like_gibberish(a.topic):
        print("REJECTED: topic gibberish lag raha hai. Koi real topic do (jaise 'Python dictionaries').")
        sys.exit(3)

    key = os.environ.get("GEMINI_API_KEY", "")
    if a.dry_run or not key:
        if not key and not a.dry_run:
            print("GEMINI_API_KEY set nahi hai. Prompt file ban raha hai (--dry-run jaisa).")
        out = ROOT / "output" / "prompts" / f"{slugify(a.topic)}_{a.lang}.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_prompt(a.topic, a.series, a.lang, a.day), encoding="utf-8")
        print(f"prompt: {out.relative_to(ROOT)}  (Gemini mein paste karke JSON le sakte ho)")
        return

    g = gate(a.topic, key)
    print(f"gate: valid={g.get('valid')} category={g.get('category')} reason={g.get('reason')}")
    if not g.get("valid"):
        print("REJECTED: ye topic teachable nahi hai. Koi real topic do.")
        sys.exit(3)

    topic = g.get("normalized_topic") or a.topic
    lesson = gemini_json(build_prompt(topic, a.series, a.lang, a.day), key)
    errs = lint(lesson, a.lang)
    # Auto-repair: lint fail hone par error Gemini ko wapas bhejo, max 2 baar
    for attempt in range(1, 3):
        if not errs:
            break
        print(f"auto-repair {attempt}: {len(errs)} error(s) -> Gemini se fix karwa rahe hain")
        fix = (build_prompt(topic, a.series, a.lang, a.day)
               + "\n\nPichla JSON ye errors ke saath reject hua:\n- " + "\n- ".join(errs)
               + "\n\nPichla JSON:\n" + json.dumps(lesson, ensure_ascii=False)
               + "\n\nSirf corrected full lesson JSON do. Upar wale errors fix karo, baaki sab same rakho.")
        lesson = gemini_json(fix, key)
        errs = lint(lesson, a.lang)
    if errs:
        print("LINT FAILED (auto-repair ke baad bhi):\n  " + "\n  ".join(errs))
        sys.exit(4)
    out = TESTS / f"lesson_{slugify(topic)}_{a.lang}.json"
    out.write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {out.relative_to(ROOT)}  ({len(lesson['scenes'])} scenes)")


if __name__ == "__main__":
    main()
