"""Daily autopilot: series ka agla din -> Gemini script -> lint -> Remotion video -> metadata -> (optional) YouTube upload.

Usage:
  python3 pipeline/autopilot.py --series python-100-days --lang en,hi            # next day, dono languages
  python3 pipeline/autopilot.py --series python-100-days --day 5 --dry-run       # plan dikhao, kuch mat banao
  python3 pipeline/autopilot.py --series python-100-days --upload                 # render + YouTube upload

State: state/autopilot.json (next_index per series). Ek din ka lesson fail ho to index nahi badhta.
Env (Gemini): GEMINI_API_KEY. Env (upload): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
"""
import argparse
import json
import re
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_to_lesson import build_prompt, gemini_json, lint, lint_short, slugify  # noqa: E402
from seo_meta import build_seo  # noqa: E402

CONFIG = ROOT / "config" / "series.json"
STATE = ROOT / "state" / "autopilot.json"
TESTS = ROOT / "tests"
META = ROOT / "output" / "meta"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"next_index": {}, "done": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def get_series(sid: str) -> dict:
    for s in json.loads(CONFIG.read_text(encoding="utf-8"))["series"]:
        if s["id"] == sid:
            return s
    raise SystemExit(f"series '{sid}' config mein nahi mili")


def lesson_path(sid: str, day: int, lang: str) -> Path:
    return TESTS / f"lesson_{sid.replace('-', '_')}_d{day:03d}_{lang}.json"


def make_lesson(series: dict, day: int, topic: str, lang: str, key: str) -> Path:
    path = lesson_path(series["id"], day, lang)
    if path.exists():
        print(f"  lesson pehle se hai: {path.name}")
        return path
    if not key:
        raise SystemExit("GEMINI_API_KEY nahi hai. Script generate nahi ho sakti.")
    fmt = series.get("format", "long")
    lesson = gemini_json(build_prompt(topic, series["name"], lang, day, fmt), key)
    if fmt == "short":
        lesson["aspectRatio"] = "9:16"
        errs = lint_short(lesson)
    else:
        errs = lint(lesson, lang)
    if errs:
        raise SystemExit("LINT FAILED:\n  " + "\n  ".join(errs))
    path.write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  script saved: {path.name}")
    return path


def render(series: dict, day: int, lang: str, lesson: Path) -> Path:
    name = f"{series['id'].replace('-', '_')}_d{day:03d}_{lang}"
    cmd = [sys.executable, str(ROOT / "pipeline" / "build_video.py"), str(lesson),
           "--name", name, "--lang", lang, "--theme", series["theme"]]
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        raise SystemExit(f"render fail: {name}")
    return ROOT / "output" / "remotion" / f"{name}.mp4"


def make_thumb(series: dict, day: int, lang: str, lesson: Path) -> Path | None:
    """Lesson se thumbnail PNG (make_thumbnail.py). Fail ho to video block nahi hota."""
    cmd = [sys.executable, str(ROOT / "pipeline" / "make_thumbnail.py"), "--lesson", str(lesson),
           "--series", series["id"], "--day", str(day), "--total", str(series.get("total", 100)), "--lang", lang]
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        print("  [warn] thumbnail fail (video chalu hai)")
        return None
    return ROOT / "output" / "thumbs" / f"{series['id'].replace('-', '_')}_d{day:03d}_{lang}_thumb.png"


def write_meta(series: dict, day: int, lang: str, lesson: Path, mp4: Path, thumb: Path | None = None, seo: dict | None = None) -> Path:
    data = json.loads(lesson.read_text(encoding="utf-8"))
    raw = re.sub(r"^.*?Day\s*\d+\s*[:\-|]\s*", "", data.get("title", ""), flags=re.I).strip()
    title = f"{series['name']} | Day {day}: {raw}"[:100]
    first = data["scenes"][0]["narration"]
    desc = (f"{first}\n\n{series['name']} - Day {day}.\n"
            "Practice task video ke end mein hai. Agla episode subscribe karke dekho.")
    tags = [series["name"].split(" in ")[0], "programming", "beginner", "tutorial"]
    if seo:  # Gemini SEO metadata (title/description/tags) basic ki jagah
        title, desc, tags = seo["title"], seo["description"], seo["tags"]
    META.mkdir(parents=True, exist_ok=True)
    out = META / f"{mp4.stem}.json"
    out.write_text(json.dumps({
        "video": str(mp4.relative_to(ROOT)), "thumbnail": (str(thumb.relative_to(ROOT)) if thumb else None), "title": title, "description": desc,
        "tags": tags, "lang": lang, "series": series["id"], "day": day,
        "playlist_id": series["youtube_playlist"].get(lang),
        "privacy": series.get("privacy", "unlisted"), "created": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", required=True)
    ap.add_argument("--lang", default=None, help="en, hi ya dono (comma). Default: series ki languages")
    ap.add_argument("--day", type=int, help="specific day; default = agla din")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--manual", action="store_true", help="disabled series ko bhi sirf manual run ke liye chalao")
    ap.add_argument("--notify", action="store_true", help="Telegram par video bhejo (TELEGRAM_* env)")
    a = ap.parse_args()

    series = get_series(a.series)
    if not series.get("enabled") and not a.day and not a.manual:
        raise SystemExit("series enabled nahi hai (config mein enabled: true karo)")

    curriculum = json.loads((ROOT / series["curriculum"]).read_text(encoding="utf-8"))["topics"]
    st = load_state()
    idx = st["next_index"].get(series["id"], 0)
    day = a.day or idx + 1
    if day > len(curriculum):
        raise SystemExit("curriculum khatam")
    topic = curriculum[day - 1]["topic"]
    langs = (a.lang or ",".join(series["langs"])).split(",")

    print(f"series={series['id']} day={day} topic='{topic}' langs={langs}")
    if a.dry_run:
        for lang in langs:
            print(f"  would build: {lesson_path(series['id'], day, lang).name} -> render -> meta")
        return

    key = os.environ.get("GEMINI_API_KEY", "")
    ok = True
    for lang in langs:
        print(f"\n[{lang}] script")
        lesson = make_lesson(series, day, topic, lang, key)
        print(f"[{lang}] render")
        mp4 = render(series, day, lang, lesson)
        thumb = make_thumb(series, day, lang, lesson)
        seo = build_seo(series["name"], topic, lang, lesson, key) if key else None
        meta = write_meta(series, day, lang, lesson, mp4, thumb, seo)
        print(f"[{lang}] meta: {meta.name}")
        if a.notify:
            from telegram_notify import send_video  # noqa: E402
            m = json.loads(meta.read_text(encoding="utf-8"))
            from telegram_notify import send_photo  # noqa: E402
            send_video(mp4, m["title"], m["description"])
            print(f"[{lang}] telegram: video sent")
            if m.get("thumbnail") and (ROOT / m["thumbnail"]).exists():
                send_photo(ROOT / m["thumbnail"], f"Thumbnail: {m['title']} (privacy: {m['privacy']})")
                print(f"[{lang}] telegram: thumbnail sent")
        if a.upload:
            from youtube_upload import upload_one  # noqa: E402
            vid = upload_one(meta)
            print(f"[{lang}] uploaded: {vid}")
        st["done"].append({"series": series["id"], "day": day, "lang": lang, "video": mp4.name,
                           "at": datetime.now().isoformat(timespec="seconds")})
    if ok and not a.day:
        st["next_index"][series["id"]] = day  # agla run agla din lega
    save_state(st)
    print("\nDONE")


if __name__ == "__main__":
    main()
