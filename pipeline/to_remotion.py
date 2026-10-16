import re
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
import tts_parler_hi  # noqa: E402  (Hindi: Indic Parler-TTS, female)
from keyboard_sfx import keys_track, save_wav  # noqa: E402
import random  # noqa: E402

FPS = 30
VOICE_RATE = "-8%"   # thoda slow, teacher jaisa pace
TYPE_TAIL = 0.4      # typing narration khatam hone se 0.4s pehle khatam
VOICE = {"en": "hf_beta", "hi": "hf_beta"}


def key_events(props: dict) -> list:
    """Har character ka time = typing progress ka same linear mapping jo TypingCode use karta hai."""
    if props.get("diff"):
        text = "".join(d["text"] + "\n" for d in props["diff"] if d["type"] == "add")
    else:
        text = props.get("code", "")
    n = max(1, len(text))
    start = props.get("startFrame", 0) / FPS
    span = props.get("typeFrames", 0) / FPS
    rnd = random.Random(5)
    ev = []
    for i, ch in enumerate(text):
        t = start + (i + 1) * span / n + rnd.uniform(-0.008, 0.008)
        kind = "enter" if ch == "\n" else "space" if ch == " " else "key"
        if ch.strip():  # bina visible char ke keystroke nahi
            ev.append((max(0.0, t), kind))
    return ev


def find_word_time(words: list, anchor: str, default: float = 0.0) -> float:
    """Narration ke word ka start time (sync anchor). Pehla match jo anchor se shuru ho."""
    for w in words:
        if w["word"].strip(",.!?").lower().startswith(anchor.strip(",.!?").lower()):
            return w["start"]
    return default


# Step-based visuals: steps[] ka har item narration ke saath sync hota hai
STEP_TYPES = {"BrowserSteps", "ArrayViz", "TreeViz", "GraphViz", "StackQueueViz", "DiagramFlow"}


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


def build(script_path: Path, lang: str, out: Path, theme: str, clips: dict, voice: str = "hf_beta") -> None:
    script = json.loads(script_path.read_text(encoding="utf-8"))
    pub = ROOT / "remotion" / "public"
    (pub / "audio").mkdir(parents=True, exist_ok=True)
    scenes = []
    selected_voice = voice or VOICE.get(lang, "hf_beta")
    for s in script["scenes"]:
        # lesson ka naam prefix: do lessons ki audio/sfx kabhi overwrite na hon
        sid = f"{script_path.stem}_{lang}_s{s['id']}"
        if lang == "hi" and not selected_voice.startswith(("hf_", "hm_")):
            audio_rel = f"audio/{sid}.wav"
            dur, words = tts_parler_hi.synth_with_words(s["narration"], pub / audio_rel)
        else:
            audio_rel = f"audio/{sid}.mp3"
            dur, words = synth_with_words(s["narration"], selected_voice, pub / audio_rel, rate=VOICE_RATE)
        if s.get("manim") and s["id"] in clips:
            s["_clip"] = clips[s["id"]]
        typ, props = scene_props(s)
        if typ in STEP_TYPES:  # BrowserSteps + DSA visuals: step ka start narration ke "at" word se
            st = props.get("steps", [])
            n = max(1, len(st))
            times = []
            for i, step in enumerate(st):
                at = step.get("at")
                times.append(find_word_time(words, at, -1.0) if at else -1.0)
            stepat = [t_i if t_i >= 0 else i * dur / n for i, t_i in enumerate(times)]
            for i in range(1, len(stepat)):
                stepat[i] = max(stepat[i], stepat[i - 1] + 1.0)
            props["stepAt"] = [round(x, 3) for x in stepat]
        # ArchitectureFlow: har step ka start time narration ke step-title word se (warna barabar baant)
        if typ == "ArchitectureFlow" and not props.get("stepAt"):
            dur_s = dur
            steps = props.get("steps", [])
            n = max(1, len(steps))
            times = []
            for i, st in enumerate(steps):
                words_in = [w for w in re.findall(r"[A-Za-z]+", st.get("title", "")) if len(w) > 2]
                t_i = find_word_time(words, words_in[0], -1.0) if words_in else -1.0
                times.append(t_i)
            fallback = [i * dur_s / n for i in range(n)]
            stepat = []
            for i, t_i in enumerate(times):
                stepat.append(t_i if t_i >= 0 else fallback[i])
            for i in range(1, len(stepat)):
                stepat[i] = max(stepat[i], stepat[i - 1] + 0.5)
            props["stepAt"] = [round(x, 3) for x in stepat]
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
            props["typeFrames"] = max(30, round((dur - start - TYPE_TAIL) * FPS))
        popups = []
        for pp in r.get("popups", []):
            popups.append({**pp, "at": round(find_word_time(words, pp["anchor"], 0.0), 3)})
        # Camera keyframes: {"at": "word in narration" | "t": sec, "zoom", "x", "y"}
        camera = []
        for k in (r.get("camera") or s.get("camera") or []):
            t = k.get("t")
            if t is None:
                t = find_word_time(words, k.get("at", ""), 0.0)
            camera.append({"t": round(float(t), 3), "zoom": k.get("zoom", 1.0),
                           "x": k.get("x", 50), "y": k.get("y", 50)})
        camera.sort(key=lambda c: c["t"])
        keys_file = None
        if typ == "TypingCode":
            keys_file = f"sfx/keys_{sid}.wav"
            save_wav(pub / keys_file, keys_track(key_events(props), dur + 0.6))
        frames = math.ceil((dur + 0.6) * FPS)  # 0.6s hold after narration
        scenes.append({"id": sid, "type": typ, "props": props, "narration": s["narration"],
                       "audioFile": audio_rel, "durationSec": round(dur, 3),
                       "durationInFrames": frames, "words": words, "popups": popups, "keysFile": keys_file, "camera": camera,
                       "stepAt": props.get("stepAt"), "chapter": r.get("chapter") or s.get("chapter"),
                       "keyIdea": r.get("keyIdea") or s.get("keyIdea")})
        print(f"scene {s['id']}: {typ} {dur:.2f}s {len(words)} words", flush=True)
    # Background music: config/music.json se track (lesson mein "bgm" key se override)
    mcfg = json.loads((ROOT / "config" / "music.json").read_text(encoding="utf-8"))
    track = script.get("bgm") or mcfg["default"]
    if track not in mcfg["tracks"]:
        raise SystemExit(f"bgm track '{track}' config/music.json mein nahi hai")
    project = {"title": script.get("title", ""), "aspectRatio": script.get("aspectRatio", "16:9"), "theme": theme,
               "dayLabel": script.get("dayLabel"), "bgm": mcfg["tracks"][track]["file"],
               "bgmVolume": mcfg["volume"], "scenes": scenes}
    print(f"bgm: {track} @ {mcfg['volume']}", flush=True)
    out.write_text(json.dumps({"project": project}, ensure_ascii=False, indent=1), encoding="utf-8")  # Remotion input props
    print("props:", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("lang", choices=["en", "hi"])
    ap.add_argument("out")
    ap.add_argument("--theme", default="light-grid")
    ap.add_argument("--voice", default="hf_beta", help="Kokoro voice (hf_beta, hm_omega)")
    ap.add_argument("--clip", action="append", default=[], help="scene_id=path/in/public.mp4")
    a = ap.parse_args()
    clips = {int(k): v for k, v in (c.split("=", 1) for c in a.clip)}
    build(Path(a.script), a.lang, Path(a.out), a.theme, clips, a.voice)
