"""Kokoro-82M (hf_beta, hm_omega) and Edge-TTS synthesis with word-level timing.

Returns: (duration_sec, [{"word","start","end"}]) and writes mp3.
Primary Engine: Kokoro-82M neural voices:
  - Female: hf_beta (Warm, soothing, human Indian accent)
  - Male: hm_omega (Deep baritone, authoritative)
Fallback: Edge-TTS natural neural voices (en-IN-NeerjaNeural, en-IN-PrabhatNeural).
"""
import asyncio
import os
import re
import subprocess
from pathlib import Path

KOKORO_VOICES = {"hf_beta", "hm_omega", "hf_alpha", "hm_psi", "am_michael", "am_adam", "af_heart"}


def _synth_kokoro(text: str, voice: str, out: Path):
    try:
        from kokoro import KPipeline
        import soundfile as sf
        import numpy as np

        lang_code = 'h' if voice.startswith('h') and any(ord(c) > 127 for c in text) else 'a'
        pipeline = KPipeline(lang_code=lang_code)
        generator = pipeline(text, voice=voice, speed=1.05)

        all_audios = []
        words = []
        curr_time = 0.0

        for res in generator:
            chunk_audio = getattr(res, "audio", None)
            if chunk_audio is None and isinstance(res, (tuple, list)):
                chunk_audio = res[-1]
                graphemes = res[0] if len(res) > 1 else ""
            else:
                graphemes = getattr(res, "graphemes", "")

            if chunk_audio is None:
                continue

            chunk_dur = len(chunk_audio) / 24000.0
            all_audios.append(chunk_audio)

            cwords = [w for w in re.split(r'\s+', graphemes) if w.strip()]
            if not cwords:
                cwords = [w for w in re.split(r'\s+', text) if w.strip()]

            total_chars = sum(len(w) for w in cwords)
            chunk_t = curr_time
            for w in cwords:
                w_dur = max(0.12, (len(w) / max(total_chars, 1)) * chunk_dur)
                words.append({
                    "word": w,
                    "start": round(chunk_t, 3),
                    "end": round(chunk_t + w_dur, 3),
                })
                chunk_t += w_dur
            curr_time += chunk_dur

        if all_audios:
            combined = np.concatenate(all_audios)
            out_wav = out.with_suffix(".wav")
            sf.write(str(out_wav), combined, 24000)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out_wav),
                            "-codec:a", "libmp3lame", "-q:a", "3", str(out)], check=True)
            if out_wav.exists() and out_wav != out:
                out_wav.unlink(missing_ok=True)
            total_dur = round(curr_time, 3)
            return total_dur, words
    except Exception as e:
        print(f"⚠️ [TTS] Kokoro-82M notice: {e}, falling back to edge-tts...")
    return None


async def _run_edge(text: str, voice: str, out: Path, rate: str):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words = []
    with out.open("wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 1e7
                dur = chunk["duration"] / 1e7
                words.append({"word": chunk["text"], "start": round(start, 3), "end": round(start + dur, 3)})
    return words


def synth_with_words(text: str, voice: str, out: Path, rate: str = "+0%"):
    out.parent.mkdir(parents=True, exist_ok=True)
    voice_lower = (voice or "am_michael").lower()

    # 1. Try Kokoro-82M if requested or default
    if voice_lower in KOKORO_VOICES or voice_lower.startswith(("hf_", "hm_", "af_", "am_")):
        res = _synth_kokoro(text, voice_lower, out)
        if res is not None:
            return res

    # 2. Edge-TTS Fallback (USA English for American voices, Indian English for Indian voices)
    if any(m in voice_lower for m in ["michael", "guy", "christopher", "us_male"]):
        edge_voice = "en-US-GuyNeural"
    elif any(f in voice_lower for f in ["bella", "heart", "jenny", "us_female"]):
        edge_voice = "en-US-JennyNeural"
    elif any(m in voice_lower for m in ["omega", "prabhat"]):
        edge_voice = "en-IN-PrabhatNeural"
    elif any(f in voice_lower for f in ["beta", "female", "neerja"]):
        edge_voice = "en-IN-NeerjaNeural"
    elif voice.startswith("hi-") or voice.startswith("en-"):
        edge_voice = voice
    else:
        edge_voice = "en-US-GuyNeural"

    words = asyncio.run(_run_edge(text, edge_voice, out, rate))
    end = words[-1]["end"] if words else 0.0
    return end, words
