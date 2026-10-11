"""Original ambient background loops (no beats, no copyright issue). Seamless loop: sab frequencies
L (loop length) mein exact integer cycles dete hain, isliye end aur start jud jaate hain.

Run: python3 pipeline/make_bgm.py   -> remotion/public/music/bgm_*.wav
"""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "remotion" / "public" / "music"
SR = 22050
L = 32.0                      # loop length (sec)
N = int(SR * L)
t = np.arange(N) / SR

def f(freq):                  # frequency ko exact loop-fit karo
    return round(freq * L) / L

def pad(freqs, detune=0.4, lfo=0.0625):
    out = np.zeros(N)
    for fr in freqs:
        for d in (-detune, detune):
            out += np.sin(2 * np.pi * f(fr + d) * t) * (0.6 + 0.4 * np.sin(2 * np.pi * f(lfo) * t + fr))
    return out / len(freqs) / 2

def soft_plucks(freqs, every=4.0):
    out = np.zeros(N)
    step = int(SR * every)
    for k, start in enumerate(range(0, N, step)):
        fr = freqs[k % len(freqs)]
        n = min(int(SR * 3.0), N - start)
        env = np.exp(-np.linspace(0, 6, n))
        out[start:start + n] += np.sin(2 * np.pi * fr * np.arange(n) / SR) * env * 0.5
    return out

def breath(level=0.03, seed=1):
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(N)
    # simple lowpass via FFT mask, loop-safe
    spec = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(N, 1 / SR)
    spec[freqs > 600] = 0
    sig = np.fft.irfft(spec, N)
    sig /= np.max(np.abs(sig)) + 1e-9
    return sig * level * (0.5 + 0.5 * np.sin(2 * np.pi * f(0.125) * t))

TRACKS = {
    "bgm_calm": {"label": "Calm pad (C major)", "sig": pad([130.81, 164.81, 196.00, 261.63]) + breath(0.02, 1)},
    "bgm_soft": {"label": "Soft plucks (A minor)", "sig": pad([110.0, 130.81, 164.81], lfo=0.03125) * 0.6 + soft_plucks([440.0, 523.25, 659.25, 523.25])},
    "bgm_warm": {"label": "Warm drone (low, shimmer)", "sig": pad([65.41, 98.0], detune=0.8, lfo=0.09375) + pad([196.0, 293.66], detune=0.3, lfo=0.0625) * 0.35},
    "bgm_night": {"label": "Night air (slow, breathy)", "sig": pad([146.83, 174.61, 220.0], lfo=0.03125) * 0.7 + breath(0.05, 7)},
}

def norm(x, peak=0.5):
    x = x - np.mean(x)
    return x / (np.max(np.abs(x)) + 1e-9) * peak

manifest = {}
for name, tr in TRACKS.items():
    sig = norm(tr["sig"])
    wavfile.write(OUT / f"{name}.wav", SR, (sig * 32767).astype(np.int16))
    manifest[name] = {"file": f"music/{name}.wav", "label": tr["label"], "loop_sec": L}
    print("wrote", name, tr["label"])

(ROOT / "config" / "music.json").write_text(json.dumps({
    "default": "bgm_calm",
    "volume": 0.12,
    "tracks": manifest,
    "note": "Original generated ambient loops (no beats). Series ke liye 'music' key se track chuno.",
}, indent=2) + "\n", encoding="utf-8")
print("manifest: config/music.json")
