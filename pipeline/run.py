"""Orchestrator: pick next topic in a series -> script (Gemini) -> TTS -> HyperFrames render.

Usage:
  python pipeline/run.py --series dsa --lang en            # next topic, English
  python pipeline/run.py --series ai_ml --lang both        # next topic, English + Hindi
  python pipeline/run.py --series dsa --lang hi --topic "Heap"   # custom topic
  python pipeline/run.py --script-file my.json --series dsa --lang en  # skip Gemini (testing)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compose import build_html  # noqa: E402
from script_gen import generate_script  # noqa: E402
from tts import release_kokoro, split_sentences, synth_lang  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config" / "series.json").read_text(encoding="utf-8"))
STATE_FILE = ROOT / "state.json"
OUT = ROOT / "output"
RENDER_TMP = Path(os.environ.get("RENDER_TMPDIR", tempfile.gettempdir())) / "render-tmp"
NODE = shutil.which("node") or os.environ.get("NODE_BIN", "node")

SERIES_ALIASES = {
    "dsa": "dsa-30-days",
    "dsa-30-days": "dsa-30-days",
    "python": "python-100-days",
    "python-100-days": "python-100-days",
    "python-shorts": "python-shorts",
    "shorts": "python-shorts",
    "shorts_tips": "python-shorts",
    "java": "java-100-days",
    "java-100-days": "java-100-days",
    "ai_ml": "python-100-days",
    "ai-ml": "python-100-days",
}

DEFAULT_LANGUAGES = {
    "en": {"engine": "edge", "voice": "en-US-ChristopherNeural", "label": "English"},
    "hi": {"engine": "edge", "voice": "hi-IN-SwaraNeural", "label": "Hindi"},
}


def get_series_config(series_key: str) -> dict:
    resolved_id = SERIES_ALIASES.get(series_key.lower(), series_key)
    raw_series = CONFIG.get("series", [])
    if isinstance(raw_series, dict):
        if series_key in raw_series:
            return raw_series[series_key]
        if resolved_id in raw_series:
            return raw_series[resolved_id]
    elif isinstance(raw_series, list):
        for s in raw_series:
            if s.get("id") == resolved_id or s.get("id") == series_key:
                return s
    return {
        "id": resolved_id,
        "name": resolved_id.replace("-", " ").replace("_", " ").title(),
        "format": "short" if "short" in resolved_id else "long",
    }


def get_lang_config(lang: str) -> dict:
    languages = CONFIG.get("languages", DEFAULT_LANGUAGES)
    if isinstance(languages, dict) and lang in languages:
        return languages[lang]
    return DEFAULT_LANGUAGES.get(lang, {"engine": "edge", "voice": "en-US-ChristopherNeural", "label": lang})


def prerender_code(script: dict) -> dict[int, dict]:
    """Run Shiki (code highlight) + KaTeX (formulas) via pipeline/render_code.mjs."""
    payload = [
        {"id": s["id"], "code": s.get("code"), "code_lang": s.get("code_lang") or "python",
         "diff": bool(s.get("diff")), "formula": s.get("formula")}
        for s in script["scenes"]
    ]
    res = subprocess.run([NODE, str(ROOT / "pipeline" / "render_code.mjs")],
                         input=json.dumps(payload), capture_output=True, text=True,
                         cwd=ROOT, check=True)
    return {item["id"]: item for item in json.loads(res.stdout)}


def render_manim(scene: dict, work: Path, dur: float) -> str:
    """Render a 3b1b-style Manim scene and fit it to the narration length. Returns relative clip path."""
    spec = scene["manim"]
    src = ROOT / "pipeline" / "manim_scenes" / spec["file"]
    media = work / "manim"
    # scale beat lengths so they add up exactly to the scene's narration length
    beats = scene.get("_beats") or [dur]
    total = sum(beats) or 1.0
    beats = [b * dur / total for b in beats]
    env = {**os.environ, "MANIM_BEATS": json.dumps(beats)}
    res = subprocess.run(["python3", "-m", "manim", "-qm", "--fps", "30", "-r", "1920,1080",
                          "--media_dir", str(media), str(src), spec["cls"]],
                         cwd=src.parent, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        tail = "\n".join((res.stdout + res.stderr).splitlines()[-25:])
        raise RuntimeError(f"Manim failed for {spec['cls']}:\n{tail}")
    raw = next(media.rglob(f"{spec['cls']}.mp4"))
    clip_rel = f"clips/s{scene['id']}.mp4"
    out = work / clip_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    # freeze last frame if animation is shorter than narration, trim if longer
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf",
                    "tpad=stop_mode=clone:stop_duration=60", "-t", f"{dur:.3f}", "-an",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)], check=True)
    return clip_rel


def load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"next_index": {}, "done": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def pick_topic(series_key: str, state: dict) -> str:
    series = get_series_config(series_key)
    raw_topics = []
    if "topics" in series and isinstance(series["topics"], list) and series["topics"]:
        raw_topics = series["topics"]
    elif "curriculum" in series:
        curr_path = ROOT / series["curriculum"]
        if curr_path.exists():
            try:
                curr_data = json.loads(curr_path.read_text(encoding="utf-8"))
                raw_topics = curr_data.get("topics", [])
            except Exception:
                raw_topics = []

    topics = []
    for t in raw_topics:
        if isinstance(t, dict):
            topics.append(t.get("topic", str(t)))
        elif isinstance(t, str):
            topics.append(t)

    if not topics:
        return f"{series.get('name', series_key)} Lesson"

    idx = state.get("next_index", {}).get(series_key, 0)
    if idx >= len(topics):
        idx = 0
    return topics[idx]


def build_one(series_key: str, lang: str, topic: str, script: dict | None) -> Path:
    series = get_series_config(series_key)
    fmt = series.get("format", "long")
    sid = series.get("id", series_key)
    slug = f"{sid}_{datetime.now():%Y%m%d_%H%M%S}_{lang}"
    work = ROOT / "work" / slug
    (work / "audio").mkdir(parents=True, exist_ok=True)

    if script is None:
        print(f"[{lang}] Gemini se script bana raha hoon: {topic}")
        script = generate_script(series["name"], fmt, topic, lang)
    (work / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2))

    lang_cfg = get_lang_config(lang)
    durations, audio_files = [], []
    for scene in script["scenes"]:
        rel = f"audio/scene{scene['id']}.mp3"
        print(f"[{lang}] TTS scene {scene['id']} ({lang_cfg['voice']})")
        durations.append(synth_lang(lang_cfg, scene["narration"], work / rel))
        audio_files.append(rel)
        if scene.get("manim"):
            # per-sentence audio lengths drive the Manim animation beats (sync)
            beats = []
            for k, sent in enumerate(split_sentences(scene["narration"])):
                bp = work / "audio" / f"scene{scene['id']}_beat{k}.mp3"
                beats.append(synth_lang(lang_cfg, sent, bp))
            scene["_beats"] = beats

    # small tail so the last word is not clipped
    durations = [d + 0.3 for d in durations]
    rendered = prerender_code(script)
    for scene, dur in zip(script["scenes"], durations):
        if scene.get("manim"):
            scene["_clip"] = render_manim(scene, work, dur)
    series_label = f"{series['name']}  ·  {'Hindi' if lang == 'hi' else 'English'}"
    release_kokoro()  # free RAM before Manim + Chrome rendering
    day_label = script.get("day_label") or ""
    (work / "index.html").write_text(
        build_html(script, durations, audio_files, fmt, lang, series_label, rendered, day_label),
        encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json"}, indent=2))

    out_dir = OUT / sid / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slug}.mp4"
    print(f"[{lang}] Render ho raha hai -> {out_file}")
    RENDER_TMP.mkdir(parents=True, exist_ok=True)
    cache_dir = Path.home() / ".hf-extract-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "TMPDIR": str(RENDER_TMP), "HYPERFRAMES_SKIP_SKILLS": "1",
           "HYPERFRAMES_EXTRACT_CACHE_DIR": str(cache_dir)}
    subprocess.run(
        ["npx", "-y", "hyperframes@0.8.143", "render", "--output", str(out_file.resolve())],
        cwd=work, env=env, check=True,
    )
    meta = {"title": script.get("title"), "description": script.get("description"),
            "tags": script.get("tags", []), "series": sid, "language": lang, "topic": topic}
    out_file.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return out_file


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", required=True, help="Series identifier (e.g. dsa, python-100-days, python-shorts)")
    ap.add_argument("--lang", default="en", choices=["en", "hi", "both"])
    ap.add_argument("--topic", help="custom topic (default: next topic from series)")
    ap.add_argument("--script-file", help="pre-written script JSON (Gemini skip)")
    args = ap.parse_args()

    state = load_state()
    topic = args.topic or pick_topic(args.series, state)
    langs = ["en", "hi"] if args.lang == "both" else [args.lang]
    fixed_script = json.loads(Path(args.script_file).read_text(encoding="utf-8")) if args.script_file else None

    for lang in langs:
        out = build_one(args.series, lang, topic, fixed_script)
        print(f"✔ Done: {out}")

    if not args.topic:
        state.setdefault("next_index", {})[args.series] = state.get("next_index", {}).get(args.series, 0) + 1
    state.setdefault("done", []).append({"series": args.series, "topic": topic, "langs": langs,
                                         "at": datetime.now().isoformat(timespec="seconds")})
    save_state(state)


if __name__ == "__main__":
    main()
