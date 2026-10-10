"""Edge TTS se audio + word-level timing ek saath lo (sync ke liye).

Returns: (duration_sec, [{"word","start","end"}]) and writes mp3.
edge-tts ke WordBoundary events se exact word timing milti hai (offset 100ns units).
"""
import asyncio
from pathlib import Path
import edge_tts


async def _run(text: str, voice: str, out: Path, rate: str):
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
    words = asyncio.run(_run(text, voice, out, rate))
    end = words[-1]["end"] if words else 0.0
    return end, words
