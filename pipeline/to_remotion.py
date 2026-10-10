"""Script JSON -> Remotion project JSON (+ narration mp3 with word timings).

Usage:
  python3 pipeline/to_remotion.py <script.json> <lang> <out_props.json> [--theme light-grid|dark-vdo]
Audio + clips remotion/public/ mein jaate hain (staticFile se load hote hain).
"""
import argparse
import difflib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts_words import synth_with_words  # noqa: E402

FPS = 30
VOICE = {"en": "en-US-AndrewNeural", "hi": "hi-IN-SwaraNeural"}


def find_word_time(words: list, anchor: str, default: float = 0.0) -> float:
    """Narration ke word ka start time (sync anchor). Pehla match jo anchor se shuru ho."""
    for w in words:
        if w["word"].strip(",.!?").lower().startswith(anchor.strip(",.!?").lower()):
            return w["start"]
    return default


def scene_props(s: dict) -> tuple[str, dict]:
    if s.get("remotion"):
        r = s["remotion"]
        return r["type"], dict(r.get("props", {}))
    if s.get("manim") and s.get("_clip"):
        return "ManimClip", {"src": s.get("_clip", ""), "heading": s.get("heading")}
    if s.get("formula"):
        return "MathVisualizer", {"title": s.get("heading"), "formula": s["formula"]}
    if s.get("code"):
        return "CodeExplainer", {"code": s["code"], "language": s.get("code_lang") or "python",
                                 "filename": s.get("code_title") or "main.py", "highlightLines": []}
    if not s.get("bullets") and not s.get("tip") and s["id"] == 1:
        return "TitleCard", {"title": s.get("heading"), "subtitle": s.get("narration", ""), "badge": "DSA"}
    items = list(s.get("bullets") or [])
    if s.get("tip"):
        items.append("Tip: " + s["tip"])
    return "SummaryList", {"title": s.get("heading"), "items": items or [s.get("narration", "")]}


def build(script_path: Path, lang: str, out: Path, theme: str, clips: dict) -> None:
    script = json.loads(script_path.read_text(encoding="utf-8"))
    pub = ROOT / "remotion" / "public"
    (pub / "audio").mkdir(parents=True, exist_ok=True)
    scenes = []
    for s in script["scenes"]:
        sid = f"{lang}_s{s['id']}"
        mp3 = pub / "audio" / f"{sid}.mp3"
        dur, words = synth_with_words(s["narration"], VOICE[lang], mp3)
        if s.get("manim") and s["id"] in clips:
            s["_clip"] = clips[s["id"]]
        typ, props = scene_props(s)
        r = s.get("remotion") or {}
        if typ == "TypingCode" and r.get("previous_code"):
            old_lines = r["previous_code"].split("\n")
            new_lines = props["code"].split("\n")
            diff = []
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=old_lines, b=new_lines).get_opcodes():
                if tag == "equal":
                    diff += [{"type": "same", "text": x} for x in old_lines[i1:i2]]
                else:
                    diff += [{"type": "del", "text": x} for x in old_lines[i1:i2]]
                    diff += [{"type": "add", "text": x} for x in new_lines[j1:j2]]
            props["diff"] = diff
        if typ == "TypingCode":
            start = find_word_time(words, r.get("type_anchor", ""), 0.0) if r.get("type_anchor") else 0.0
            props["startFrame"] = round(start * FPS)
            props["typeFrames"] = max(30, round((dur - start) * FPS * 0.85))
        popups = []
        for pp in r.get("popups", []):
            popups.append({**pp, "at": round(find_word_time(words, pp["anchor"], 0.0), 3)})
        frames = math.ceil((dur + 0.6) * FPS)  # 0.6s hold after narration
        scenes.append({"id": sid, "type": typ, "props": props, "narration": s["narration"],
                       "audioFile": f"audio/{sid}.mp3", "durationSec": round(dur, 3),
                       "durationInFrames": frames, "words": words, "popups": popups})
        print(f"scene {s['id']}: {typ} {dur:.2f}s {len(words)} words", flush=True)
    project = {"title": script.get("title", ""), "aspectRatio": "16:9", "theme": theme,
               "dayLabel": script.get("dayLabel"), "bgm": "sfx/bgm.wav", "bgmVolume": 0.08, "scenes": scenes}
    out.write_text(json.dumps({"project": project}, ensure_ascii=False, indent=1), encoding="utf-8")  # Remotion input props
    print("props:", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("lang", choices=["en", "hi"])
    ap.add_argument("out")
    ap.add_argument("--theme", default="light-grid")
    ap.add_argument("--clip", action="append", default=[], help="scene_id=path/in/public.mp4")
    a = ap.parse_args()
    clips = {int(k): v for k, v in (c.split("=", 1) for c in a.clip)}
    build(Path(a.script), a.lang, Path(a.out), a.theme, clips)
