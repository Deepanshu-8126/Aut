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

PROMPT = """You write viral, high-ranking YouTube SEO metadata for an educational programming tutorial.

Series: {series}
Day/Topic: {topic}
Language of the video: {lang_name}
Lesson summary (first scenes narration): {summary}

Return ONLY JSON:
{{
  "title": "...",          // max 80 chars, high-CTR, curiosity/benefit-driven, primary keyword first (e.g. "Java in 100 Days | Day 1: How Java Runs & Hello World")
  "description": "...",    // Comprehensive, high-engagement description (300-800 chars):
                           // 1. Hook explaining what viewer will learn & why it matters
                           // 2. Key concepts covered in this episode
                           // 3. Call-to-action: "Practice task video ke end mein hai. Comment your solution below!"
                           // 4. Playlist & Subscribe reminder
                           // 5. 5-8 trending viral hashtags at the very bottom (e.g. #Java #JavaTutorial #LearnJava #Coding #Programming #100DaysOfCode)
  "tags": ["...", "..."]   // 12-18 highly searched viral YouTube tags and long-tail keywords (e.g. "java tutorial for beginners", "how java works", "java hello world", "core java", "learn java programming", "java course")
}}
Rules:
- Title aur description ki language = {lang_name}. English technical keywords allowed.
- Strictly relevant to the lesson, highly engaging, click-worthy but never misleading.
- Description must end with 5-8 viral hashtags with # prefix.
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
