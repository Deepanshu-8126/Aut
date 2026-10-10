"""Gemini se SEO metadata: title, description, tags (en/hi).

Usage (test):  GEMINI_API_KEY=... python3 pipeline/seo_meta.py <lesson.json> "Python in 100 Days" en
Fail hone par None return karta hai, taaki autopilot purane (basic) metadata se chal jaye.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_to_lesson import gemini_json  # noqa: E402

TITLE_MAX = 90
DESC_MIN = 200
TAGS_MAX = 15
TAGS_CHARS = 450  # YouTube ki tags limit ke andar

PROMPT = """You write YouTube SEO metadata for an educational video.

Series: {series}
Day/Topic: {topic}
Language of the video: {lang_name}
Lesson summary (first scenes narration): {summary}

Return ONLY JSON:
{{
  "title": "...",          // max 80 chars, primary keyword pehle, clickable, clickbait nahi (misleading nahi)
  "description": "...",    // 3-4 short paragraphs, pehle 2 lines mein main keyword, 200-600 chars, ends with a line: "Practice task video ke end mein hai."
  "tags": ["...", "..."]   // 10-15 relevant search keywords (short phrases), same language
}}
Rules:
- Title aur description ki language = {lang_name}. English keywords chalenge agar tech terms hain.
- Gibberish ya fake claims mat likho. Sirf lesson ke content se related.
- Hashtags description ke end mein 3 tak.
"""


def _summary(lesson: dict) -> str:
    parts = [s.get("narration", "") for s in lesson.get("scenes", [])[:3]]
    return " ".join(p for p in parts if p)[:600]


def build_seo(series_name: str, topic: str, lang: str, lesson_path: Path, key: str) -> dict | None:
    lesson = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
    prompt = PROMPT.format(series=series_name, topic=topic,
                           lang_name="Hindi (Devanagari)" if lang == "hi" else "English",
                           summary=_summary(lesson))
    try:
        data = gemini_json(prompt, key)
    except Exception as e:  # network / quota / bad JSON -> fallback
        print(f"  [seo] Gemini fail, basic metadata use hoga: {e}")
        return None
    return validate_seo(data, series_name)


def validate_seo(data: dict, series_name: str) -> dict | None:
    title = str(data.get("title", "")).strip()
    desc = str(data.get("description", "")).strip()
    tags = [str(t).strip() for t in data.get("tags", []) if str(t).strip()]

    problems = []
    if not title:
        problems.append("title khali")
    if len(desc) < DESC_MIN:
        problems.append(f"description chhota ({len(desc)} chars)")
    if len(tags) < 5:
        problems.append(f"tags kam ({len(tags)})")
    if problems:
        print("  [seo] validation fail: " + "; ".join(problems) + " -> basic metadata")
        return None

    title = f"{series_name} | {title}"[:TITLE_MAX]
    out_tags, total = [], 0
    for t in tags:
        if len(out_tags) >= TAGS_MAX or total + len(t) > TAGS_CHARS:
            break
        out_tags.append(t)
        total += len(t)
    return {"title": title, "description": desc, "tags": out_tags}


if __name__ == "__main__":
    import os
    if len(sys.argv) < 4:
        sys.exit("usage: seo_meta.py <lesson.json> <series name> <en|hi> [topic]")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY set nahi hai")
    res = build_seo(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 else sys.argv[2], sys.argv[3],
                    Path(sys.argv[1]), key)
    print(json.dumps(res, ensure_ascii=False, indent=2) if res else "FALLBACK (basic metadata)")
