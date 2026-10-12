"""Free local/neural TTS.
- English: Kokoro-82M (local ONNX, same model family vdo uses). Voices: am_michael, af_heart, ...
- Hindi:   edge-tts Microsoft neural voices (Kokoro does not support Hindi).
"""
import asyncio
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
_kokoro = None


def _get_kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(str(Path("/opt/kokoro/kokoro-v1.0.onnx")), str(Path("/opt/kokoro/voices-v1.0.bin")))
    return _kokoro


def release_kokoro() -> None:
    """Free the ~500MB Kokoro model before heavy rendering (RAM is tight on this machine)."""
    global _kokoro
    _kokoro = None
    import gc
    gc.collect()


def _to_mp3(wav: Path, out: Path) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-codec:a", "libmp3lame",
                    "-q:a", "3", str(out)], check=True)
    wav.unlink(missing_ok=True)


def synth_kokoro(text: str, voice: str, out: Path) -> float:
    """Kokoro runs in a fresh process per clip, so its ~500MB is returned to the OS each time."""
    out.parent.mkdir(parents=True, exist_ok=True)
    txt = out.with_suffix(".txt")
    txt.write_text(text, encoding="utf-8")
    wav = out.with_suffix(".wav")
    subprocess.run([sys.executable, str(ROOT / "pipeline" / "kokoro_one.py"), str(txt), voice, str(wav)],
                   check=True)
    txt.unlink(missing_ok=True)
    _to_mp3(wav, out)
    return audio_duration(out)


async def _edge(text: str, voice: str, out: Path) -> None:
    await edge_tts.Communicate(text, voice, rate="+0%").save(str(out))


def synth_edge(text: str, voice: str, out: Path) -> float:
    out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_edge(text, voice, out))
    return audio_duration(out)


def synth_lang(lang_cfg: dict, text: str, out: Path) -> float:
    """Dispatch by the language's configured engine with automatic fallback to edge-tts."""
    if lang_cfg.get("engine") == "kokoro" and Path("/opt/kokoro/kokoro-v1.0.onnx").exists():
        try:
            return synth_kokoro(text, lang_cfg["voice"], out)
        except Exception as e:
            print(f"[TTS] Kokoro unavailable ({e}), falling back to edge-tts.")
    voice = lang_cfg.get("voice", "")
    if not voice or "am_" in voice or "af_" in voice:
        voice = "en-US-ChristopherNeural"
    return synth_edge(text, voice, out)


def split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?।])\s+", text) if p.strip()]
    return parts or [text]


def audio_duration(path: Path) -> float:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(res.stdout.strip())
