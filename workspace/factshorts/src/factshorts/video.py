"""Video + audio: compose frames at fixed fps, then encode with ffmpeg (static build)."""
from __future__ import annotations

import math
import os
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

from .renderer import Part, compose
from . import motion2


def ffmpeg_exe(autoboot: bool = True) -> str:
    """System ffmpeg -> bundled static binary -> one automatic `pip install` attempt.

    Keeps the pipeline runnable on a fresh machine with a single command.
    """
    exe = os.environ.get("FFMPEG_BIN") or shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                                          # noqa: BLE001
        if not autoboot:
            raise RuntimeError("ffmpeg not found: set FFMPEG_BIN or `pip install imageio-ffmpeg`")
    print("  [setup] installing a static ffmpeg binary (one time, ~30 MB)…")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=False)
    try:
        import importlib
        import imageio_ffmpeg
        importlib.reload(imageio_ffmpeg)
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:                                     # noqa: BLE001
        raise RuntimeError("ffmpeg unavailable. Set FFMPEG_BIN or run: "
                           "pip install imageio-ffmpeg") from e


def render_frames(part: Part, out_dir: Path, fps: int = 30, scale: int = 2,
                  duration: float | None = None) -> Path:
    """Render every animation frame of one part to out_dir/f_%04d.png."""
    out_dir.mkdir(parents=True, exist_ok=True)
    dur = duration or part.duration
    n = max(2, int(round(dur * fps)))
    for i in range(n):
        t = i / fps
        img = compose(part, t)
        img = motion2.apply_camera(img, t, dur, getattr(part, 'idx', 1))
        if scale > 1:
            img = img.resize((img.width // scale, img.height // scale))
        img.save(out_dir / f"f_{i:04d}.png", optimize=False)
    return out_dir


def encode_mp4(frame_dir: Path, out_mp4: Path, fps: int = 30, audio: Path | None = None,
               seconds: float | None = None, crf: int = 19, preset: str = "medium") -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    exe = ffmpeg_exe()
    cmd = [exe, "-y", "-loglevel", "error", "-framerate", str(fps),
           "-i", str(frame_dir / "f_%04d.png")]
    if audio and Path(audio).exists():
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    filt = "scale=1080:1920:flags=lanczos,format=yuv420p"
    cmd += ["-vf", filt, "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
            "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(out_mp4)]
    subprocess.run(cmd, check=True)
    return out_mp4


def concat(parts: list[Path], out: Path, tmp_dir: Path) -> Path:
    exe = ffmpeg_exe()
    lst = tmp_dir / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    subprocess.run([exe, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(out)], check=True)
    return out


# ------------------------------------------------------------------ audio bed
def write_wav(path: Path, samples: list[float], sr: int = 44100):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767))))
                               for s in samples))


def _env(i: int, start: int, length: int, attack: int, release: int) -> float:
    x = i - start
    if x < 0 or x > length:
        return 0.0
    if x < attack:
        return x / attack
    if x > length - release:
        return max(0.0, (length - x) / release)
    return 1.0


def sfx_bed(duration: float, events: list[tuple[str, float]], sr: int = 44100) -> list[float]:
    """Procedural SFX (no external assets, no copyright): whoosh, pop, ding, tick, glitch."""
    n = int(duration * sr)
    buf = [0.0] * n

    def add(start_s: float, samples):
        s0 = int(start_s * sr)
        for k, v in enumerate(samples):
            i = s0 + k
            if 0 <= i < n:
                buf[i] += v

    for kind, at in events:
        if kind == "whoosh2":                                 # motionmaxxing sweep
            add(at, motion2.whoosh_sweep(sr))
            continue
        if kind == "tick2":                                   # 1480 Hz UI tick
            add(at, motion2.label_tick(sr))
            continue
        if kind == "whoosh":                                  # filtered noise sweep
            L = int(0.5 * sr)
            add(at, [0.10 * _env(i, 0, L, 400, L - 400) *
                     math.sin(2 * math.pi * (200 + 900 * i / L) * i / sr) for i in range(L)])
        elif kind == "pop":                                   # short sine burst
            L = int(0.10 * sr)
            add(at, [0.16 * _env(i, 0, L, 30, L - 30) *
                     math.sin(2 * math.pi * 620 * i / sr) for i in range(L)])
        elif kind == "expop":                                 # bigger box pop
            L = int(0.16 * sr)
            add(at, [0.18 * _env(i, 0, L, 40, L - 40) *
                     math.sin(2 * math.pi * (420 + 260 * i / L) * i / sr) for i in range(L)])
        elif kind == "tick":                                  # typewriter
            L = int(0.03 * sr)
            add(at, [0.07 * _env(i, 0, L, 4, L - 4) *
                     math.sin(2 * math.pi * 1700 * i / sr) for i in range(L)])
        elif kind == "glitch":                                # digital blip
            L = int(0.22 * sr)
            add(at, [0.12 * _env(i, 0, L, 20, L - 60) *
                     math.sin(2 * math.pi * (900 + 500 * math.sin(i / 220)) * i / sr)
                     for i in range(L)])
        elif kind == "ding":                                  # payoff
            L = int(0.9 * sr)
            add(at, [0.16 * _env(i, 0, L, 60, L - 200) *
                     (math.sin(2 * math.pi * 880 * i / sr) +
                      0.5 * math.sin(2 * math.pi * 1320 * i / sr)) for i in range(L)])

    # low ambient pad (root + fifth, slow tremolo) — very low level
    for i in range(n):
        t = i / sr
        pad = (0.022 * math.sin(2 * math.pi * 110 * t) +
               0.016 * math.sin(2 * math.pi * 165 * t) +
               0.012 * math.sin(2 * math.pi * 220 * t))
        fade = min(1.0, t / 0.6) * min(1.0, max(0.0, (duration - t) / 0.6))
        buf[i] += pad * fade * (0.75 + 0.25 * math.sin(2 * math.pi * 0.15 * t))
    return buf


def default_events(part: Part) -> list[tuple[str, float]]:
    ev: list[tuple[str, float]] = [("whoosh2", 0.02), ("expop", 0.55), ("glitch", 1.25)]
    for i in range(len(part.callouts)):
        ev.append(("expop", 1.3 + 0.16 * i))
        ev.append(("tick2", 1.32 + 0.16 * i))
        for k in range(3):
            ev.append(("tick", 1.45 + 0.16 * i + k * 0.08))
    ev.append(("pop", 2.1))
    if part.cta:
        ev.append(("ding", 3.0))
    return ev


def write_sfx(path: Path, part: Part, duration: float):
    write_wav(path, sfx_bed(duration, default_events(part)))
