"""Kokoro Hindi TTS with exact word timings (per-word synthesis).

Kokoro word-level timestamps nahi deta, isliye har word alag synth hota hai.
Timing = clip ki asli duration, isliye narration aur popup/typing sync exact rehte hain.

Pronunciation: Hindi G2P English words ko Devanagari mein achha bolta hai.
GLOSSARY mein English technical terms ko Devanagari spelling di gayi hai
(sirf bolne ke liye; on-screen text original rehta hai).

Model: kokoro-v1.0.onnx + voices-v1.0.bin (Apache 2.0). Path env KOKORO_DIR
(default /tmp/kokoro). Files na ho to GitHub release se download hoti hain.

Usage (test): python3 pipeline/tts_kokoro_hi.py "text" out.wav
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 24000
VOICE = "hf_beta"       # female Hindi (hf_alpha bhi available)
SPEED = 0.95
WORD_GAP = 0.06         # sec, words ke beech chhota gap
RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL_DIR = Path(os.environ.get("KOKORO_DIR", "/tmp/kokoro"))

# English term -> Devanagari (bolne ke liye). Naya term aaye to yahan add karo.
GLOSSARY = {
    "python": "पाइथन", "list": "लिस्ट", "lists": "लिस्ट्स", "tuple": "ट्पल", "tuples": "ट्पल्स",
    "value": "वैल्यू", "values": "वैल्यूज़", "index": "इंडेक्स", "print": "प्रिंट",
    "loop": "लूप", "for": "फॉर", "code": "कोड", "function": "फंक्शन", "string": "स्ट्रिंग",
    "variable": "वेरिएबल", "data": "डेटा", "array": "ऐरे", "dictionary": "डिक्शनरी",
    "append": "अपेंड", "example": "एग्ज़ाम्पल", "output": "आउटपुट", "input": "इनपुट",
    "class": "क्लास", "object": "ऑब्जेक्ट", "algorithm": "एल्गोरिदम", "python's": "पाइथन्स",
    "store": "स्टोर", "numbers": "नंबर्स", "number": "नंबर", "strings": "स्ट्रिंग्स",
    "string's": "स्ट्रिंग्स", "list's": "लिस्ट्स",
}

_kokoro = None


def _ensure_model() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for name in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        p = MODEL_DIR / name
        if not p.exists() or p.stat().st_size < 1000:
            urllib.request.urlretrieve(RELEASE + name, p)


def _get():
    global _kokoro
    if _kokoro is None:
        _ensure_model()
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"), str(MODEL_DIR / "voices-v1.0.bin"))
    return _kokoro


def release() -> None:
    global _kokoro
    _kokoro = None


def _spoken(word: str) -> str:
    """English token ko Devanagari se badlo (punctuation same rakho)."""
    m = re.search(r"[A-Za-z']+", word)
    if not m:
        return word
    core = m.group(0).lower()
    if core not in GLOSSARY:
        return word
    return word[:m.start()] + GLOSSARY[core] + word[m.end():]


def synth_with_words(text: str, out: Path, rate: str = "") -> tuple[float, list]:
    """Pipeline contract: (duration_sec, [{word, start, end}]). Output WAV."""
    k = _get()
    tokens = text.split()
    parts, words, t = [], [], 0.0
    gap = np.zeros(int(SR * WORD_GAP), dtype=np.float32)
    for tok in tokens:
        spoken = _spoken(tok)
        # punctuation-only ya empty words skip nahi, lekin text ko TTS ke liye saaf karo
        audio, sr = k.create(spoken, voice=VOICE, speed=SPEED, lang="hi")
        audio = np.asarray(audio, dtype=np.float32)
        d = len(audio) / sr
        words.append({"word": tok, "start": round(t, 3), "end": round(t + d, 3)})
        parts += [audio, gap]
        t += d + WORD_GAP
    wav = np.concatenate(parts) if parts else np.zeros(SR, dtype=np.float32)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out.with_suffix(".wav")), wav, SR)
    dur = len(wav) / SR
    return round(dur, 3), words


if __name__ == "__main__":
    text, out = sys.argv[1], Path(sys.argv[2])
    dur, words = synth_with_words(text, out)
    print(json.dumps({"duration": dur, "words": words}, ensure_ascii=False))
