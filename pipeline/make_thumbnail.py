"""Lesson JSON se YouTube thumbnail (1280x720 PNG) banata hai. Theme: white grid.

Usage:
  python3 pipeline/make_thumbnail.py --lesson tests/lesson_java_100_days_d001_en.json \
      --series java-100-days --day 1 --total 100

Data source (automatic):
  - title, subtitle: scene 1 TitleCard ke props (ya lesson.thumbnail override)
  - code card: pehla TypingCode scene ka code (max 6 lines)
  - highlight word: series config mein "keyword" (jaise "Java"), ya lesson.thumbnail.highlight
  - badge: "DAY n • <SERIES SHORT NAME>"
Output: output/thumbs/<name>.png (+ .props.json)
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "series.json"
REMOTION = ROOT / "remotion"
OUT = ROOT / "output" / "thumbs"


def series_cfg(sid: str) -> dict:
    for s in json.loads(CONFIG.read_text(encoding="utf-8"))["series"]:
        if s["id"] == sid:
            return s
    raise SystemExit(f"series '{sid}' config mein nahi mili")


def build_props(lesson: dict, series: dict, day: int, total: int) -> dict:
    scenes = lesson.get("scenes", [])
    ov = lesson.get("thumbnail", {}) or {}

    title_props = {}
    for s in scenes:
        rem = s.get("remotion") or {}
        if rem.get("type") == "TitleCard":
            title_props = rem.get("props", {})
            break
    raw_title = lesson.get("title", "")
    if not title_props.get("title") and ":" in raw_title:
        raw_title = raw_title.split(":", 1)[1].strip()   # "Java Day 1: X" -> "X"
    title = ov.get("title") or title_props.get("title") or raw_title
    subtitle = ov.get("subtitle") or title_props.get("subtitle") or ""

    code, code_title = None, None
    for s in scenes:
        rem = s.get("remotion") or {}
        if rem.get("type") in ("TypingCode", "CodeExplainer"):
            p = rem.get("props", {})
            code = p.get("code")
            code_title = p.get("filename")
            break
    code_lines = code.split("\n")[:6] if code else []
    hl_line = 1
    for i, line in enumerate(code_lines, 1):
        if "class " in line or "def " in line or "function " in line:
            hl_line = i
            break

    keyword = ov.get("highlight") or series.get("keyword") or ""
    short = series.get("short_name") or series["name"].split(" in ")[0].upper()
    props = {
        "title": title,
        "highlight": keyword if keyword and keyword.lower() in title.lower() else "",
        "badge": f"DAY {day} • {short.upper()}",
        "subtitle": subtitle,
        "code": "\n".join(code_lines) if code_lines else "",
        "codeTitle": code_title or "main.py",
        "codeHighlightLine": hl_line,
        "footer": f"Progress • Day {day} / {total}",
        "accent": series.get("accent", "#2563eb"),
        "motif": series.get("thumb_motif", "none"),
    }
    return props


def render(props: dict, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    props_file = OUT / f"{name}.props.json"
    props_file.write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8")
    png = OUT / f"{name}.png"
    cmd = ["npx", "remotion", "still", "src/index.ts", "Thumbnail", str(png),
           f"--props={props_file}", "--overwrite", "--log=warn"]
    res = subprocess.run(cmd, cwd=REMOTION, shell=sys.platform == "win32")
    if res.returncode != 0 or not png.exists():
        raise SystemExit("thumbnail render fail")
    return png


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--series", required=True)
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--total", type=int, default=100)
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()

    lesson = json.loads(Path(a.lesson).read_text(encoding="utf-8"))
    series = series_cfg(a.series)
    props = build_props(lesson, series, a.day, a.total)
    name = f"{a.series.replace('-', '_')}_d{a.day:03d}_{a.lang}_thumb"
    png = render(props, name)
    print(f"thumbnail: {png.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
