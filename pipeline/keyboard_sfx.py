"""Realistic mechanical keyboard track. Har keystroke ka sound code ke typing time par bajta hai.

Sound design: short transient (key ka plastic 'tick') + body resonance (keycap ka 'tok')
+ bottom-out 'thock'. Har key par pitch, volume aur timing mein thoda random variation,
taaki loop jaisa na lage. Space aur Enter ka sound alag (bade keys).
"""
from pathlib import Path
import numpy as np
import wave

SR = 44100


def _key(rng, kind: str) -> np.ndarray:
    n = int(0.10 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    transient = np.diff(noise, prepend=0.0) * np.exp(-t / 0.0012)  # tick
    f0 = rng.uniform(900, 1400) if kind == "key" else rng.uniform(550, 750)
    body = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in
               [(f0, 0.5, 0.014), (f0 * 1.93, 0.22, 0.008), (f0 * 2.71, 0.10, 0.005)])
    thock_f = rng.uniform(150, 200) if kind == "key" else rng.uniform(90, 120)
    thock_amp = 0.55 if kind == "key" else 0.9
    thock = np.sin(2 * np.pi * thock_f * t) * np.exp(-t / (0.022 if kind == "key" else 0.05)) * thock_amp
    x = 0.8 * transient + 0.45 * body + thock
    # soft "room": 2-pole lowpass ko hata kar simple smoothing, digital harshness kam
    x = np.convolve(x, np.ones(2) / 2, mode="same")
    x *= rng.uniform(0.7, 1.0) / (np.max(np.abs(x)) + 1e-9)
    return x


BANK_DIR = Path(__file__).resolve().parent.parent / "remotion" / "public" / "sfx" / "keys"


def _load_bank() -> list[np.ndarray]:
    """Real keyboard recordings (Freesound CC0, mccreery/509171, individual key clips). Fallback: synth."""
    if not BANK_DIR.exists():
        return []
    bank = []
    for f in sorted(BANK_DIR.glob("*.wav")):
        with wave.open(str(f), "rb") as w:
            bank.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768)
    return bank


def keys_track(events: list[tuple[float, str]], duration: float, seed: int = 11) -> np.ndarray:
    rng = np.random.default_rng(seed)
    total = int((duration + 0.5) * SR)
    track = np.zeros(total)
    bank = _load_bank()
    for t, kind in events:
        if bank:
            click = bank[rng.integers(len(bank))] * rng.uniform(0.85, 1.0)
            if kind != "key":
                click = click * 0.8  # space/enter thoda dheemi
        else:
            click = _key(rng, kind)
        i = int(t * SR)
        if i >= total:
            continue
        m = min(len(click), total - i)
        track[i:i + m] += click[:m] * (0.45 if kind == "key" else 0.6)
    return track


def save_wav(path: Path, x: np.ndarray):
    x = np.clip(x, -1, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
