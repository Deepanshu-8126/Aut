"""Apne sound effects generate karta hai (numpy). Koi external copyright nahi.

Output: remotion/public/sfx/*.wav
 - key.wav     : ek keyboard click
 - typing.wav  : 12 sec ka typing loop (random clicks)
 - pop.wav     : popup pop (upar sweep)
 - whoosh.wav  : scene transition
 - ding.wav    : "correct / done" chime
 - bgm.wav     : 60 sec soft ambient pad loop (background music)
"""
from pathlib import Path
import numpy as np
import wave

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "remotion" / "public" / "sfx"


def save(name: str, x: np.ndarray):
    x = np.clip(x, -1, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def env(n, attack=0.002, decay=0.05):
    t = np.arange(n) / SR
    return np.exp(-t / decay) * np.minimum(1, t / attack)


def click(rng):
    n = int(0.05 * SR)
    noise = rng.uniform(-1, 1, n)
    body = np.sin(2 * np.pi * rng.uniform(1500, 2600) * np.arange(n) / SR)
    return (0.6 * noise + 0.4 * body) * env(n, 0.001, 0.012)


def key():
    return click(np.random.default_rng(1)) * 0.8


def typing():
    rng = np.random.default_rng(7)
    total = int(12 * SR)
    x = np.zeros(total)
    t = 0.0
    while t < 12:
        c = click(rng) * rng.uniform(0.5, 0.9)
        i = int(t * SR)
        x[i:i + len(c)] += c[: total - i]
        t += rng.uniform(0.09, 0.22)  # typing ka rhythm
    return x


def pop():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 500 + 1400 * t / 0.25  # upar sweep
    phase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(phase) * env(n, 0.003, 0.08)


def whoosh():
    rng = np.random.default_rng(3)
    n = int(0.6 * SR)
    noise = rng.uniform(-1, 1, n)
    k = np.linspace(0, 1, n)
    lp = np.convolve(noise, np.ones(40) / 40, mode="same")
    return lp * np.sin(np.pi * k) * 0.7


def ding():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 880 * t) + 0.4 * np.sin(2 * np.pi * 1760 * t)) * env(n, 0.002, 0.35) * 0.6


def bgm():
    n = int(60 * SR)
    t = np.arange(n) / SR
    chord = [220.0, 277.18, 329.63]  # A minor pad
    pad = sum(np.sin(2 * np.pi * f * t) for f in chord) / len(chord)
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * t / 8)
    x = pad * (0.5 + 0.2 * swell) * 0.25
    fade = np.minimum(1, np.minimum(t / 2, (t[-1] - t) / 2))
    return x * fade


if __name__ == "__main__":
    save("key.wav", key())
    save("typing.wav", typing())
    save("pop.wav", pop())
    save("whoosh.wav", whoosh())
    save("ding.wav", ding())
    save("bgm.wav", bgm())
    print("sfx ->", OUT, sorted(p.name for p in OUT.iterdir()))
