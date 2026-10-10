"""Run one Kokoro synthesis in its own process so RAM is fully released afterwards.
Usage: python kokoro_one.py <text_file> <voice> <out.wav>
"""
import sys
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
text_file, voice, out = sys.argv[1], sys.argv[2], sys.argv[3]
text = Path(text_file).read_text(encoding="utf-8")
k = Kokoro(str(Path("/opt/kokoro/kokoro-v1.0.onnx")), str(Path("/opt/kokoro/voices-v1.0.bin")))
samples, sr = k.create(text, voice=voice, speed=0.95, lang="en-us")
sf.write(out, samples, sr)
