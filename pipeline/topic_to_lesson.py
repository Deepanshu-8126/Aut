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
PROMPT = ROOT / "prompts" / "gemini_teacher_prompt.md"
TESTS = ROOT / "tests"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
API = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"

ALLOWED_TYPES = {"TitleCard", "TypingCode", "TerminalRun", "ComparisonCard", "SummaryList", "StatChart"}
BANNED = ["in this video", "let's dive in", "delve", "unlock", "game-changer", "game changer",
          "seamlessly", "robust", "leverage", "moreover", "furthermore", "fast-paced"]
WPS_MIN, WPS_MAX = 1.6, 3.2   # words per second (spoken English/Hinglish)
SCENE_SEC_MIN, SCENE_SEC_MAX = 4, 30


def gemini_json(prompt: str, key: str) -> dict:
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.6}}
    req = urllib.request.Request(API.format(m=MODEL, k=key), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


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


def build_prompt(topic: str, series: str, lang: str, day: int | None) -> str:
    tpl = PROMPT.read_text(encoding="utf-8")
    lang_name = {"en": "English", "hi": "Hindi (Hinglish-Devanagari, English tech words in Latin)"}[lang]
    golden = (ROOT / "prompts" / "examples" / "golden_lesson.json").read_text(encoding="utf-8")
    tpl = tpl + "\n\nGOLDEN EXAMPLE (quality bar, different topic):\n" + golden
    return (tpl.replace("{LANG}", lang_name).replace("{TOPIC}", topic)
            .replace("{SERIES}", series or "standalone").replace("{DAY}", str(day or "n/a")))


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
    if len(scenes) < 4:
        errs.append(f"scenes kam hain ({len(scenes)}), kam se kam 4 chahiye")
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
        if words < 6:
            warns.append(f"{tag}: narration bahut chhota ({words} words)")
        if lo < SCENE_SEC_MIN or hi > SCENE_SEC_MAX:
            warns.append(f"{tag}: narration length ~{lo:.0f}-{hi:.0f}s (target {SCENE_SEC_MIN}-{SCENE_SEC_MAX}s)")
        for p in (s.get("popups") or rem.get("popups") or []):
            a = p.get("anchor", "")
            if a and a.lower() not in low:
                errs.append(f"{tag}: popup anchor '{a}' narration mein nahi hai")
        ta = rem.get("type_anchor")
        if ta and ta.lower() not in low:
            errs.append(f"{tag}: type_anchor '{ta}' narration mein nahi hai")
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
    if errs:
        print("LINT FAILED:\n  " + "\n  ".join(errs))
        sys.exit(4)
    out = TESTS / f"lesson_{slugify(topic)}_{a.lang}.json"
    out.write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {out.relative_to(ROOT)}  ({len(lesson['scenes'])} scenes)")


if __name__ == "__main__":
    main()
