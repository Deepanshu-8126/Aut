from pathlib import Path
import subprocess, json, re

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
SFX = ROOT / "explainer-pipeline" / "assets" / "sfx"
FFMPEG = "ffmpeg"
DUR = 30.0

music_bed = P / "mixkit_871.mp3"
voice_file = P / "voice_clean.wav"

# 1. Prepare music bed: atrim duration=30, fade in/out
music_proc = P / "music_bed.wav"
cmd_music = [
    FFMPEG, "-v", "error", "-y",
    "-ss", "28", "-i", str(music_bed),
    "-af", f"atrim=duration={DUR},asetpts=PTS-STARTPTS,aresample=48000,volume=0.15,afade=t=in:st=0:d=0.5,afade=t=out:st=28.5:d=1.5",
    "-c:a", "pcm_s24le", str(music_proc)
]
subprocess.run(cmd_music, check=True)
print("Music bed prepared.")

# 2. SFX Cues (time, file, gain, trim, duration)
cues = [
    {"time": 0.65, "file": "mk788", "gain": 0.80, "trim": 0.55, "dur": 1.5},
    {"time": 3.50, "file": "mk1492", "gain": 0.50, "trim": 0.0, "dur": 1.0},
    {"time": 3.60, "file": "mk677", "gain": 0.40, "trim": 0.0, "dur": 0.8},
    {"time": 8.50, "file": "mk1486", "gain": 0.55, "trim": 0.0, "dur": 1.2},
    {"time": 13.00, "file": "mk685", "gain": 0.70, "trim": 0.0, "dur": 2.0},
    {"time": 18.00, "file": "mk677", "gain": 0.40, "trim": 0.0, "dur": 0.8},
    {"time": 21.00, "file": "mk790", "gain": 0.60, "trim": 0.0, "dur": 1.1},
    {"time": 22.10, "file": "mk1143", "gain": 0.80, "trim": 0.19, "dur": 1.5},
    {"time": 25.00, "file": "mk494", "gain": 0.45, "trim": 0.43, "dur": 4.0},
    {"time": 28.50, "file": "mk492", "gain": 0.50, "trim": 0.0, "dur": 1.5}
]

cmd_mix = [
    FFMPEG, "-v", "error", "-y",
    "-i", str(voice_file),
    "-i", str(music_proc)
]

for c in cues:
    cmd_mix += ["-i", str(SFX / f"{c['file']}.mp3")]

filters = [
    f"[0:a]aresample=48000,adelay=700:all=1,apad,atrim=duration={DUR},volume=0.92[voice]",
    f"[1:a]aresample=48000,asetpts=PTS-STARTPTS[music]"
]
inputs = "[voice][music]"

for idx, c in enumerate(cues):
    t_ms = int(c["time"] * 1000)
    filters.append(
        f"[{idx+2}:a]aresample=48000,atrim=start={c['trim']}:duration={c['dur']},asetpts=PTS-STARTPTS,volume={c['gain']},adelay={t_ms}:all=1[s{idx}]"
    )
    inputs += f"[s{idx}]"

filters.append(f"{inputs}amix=inputs={len(cues)+2}:duration=first:normalize=0[mixed]")

mix_pre = P / "mix_pre.wav"
cmd_mix += ["-filter_complex", ";".join(filters), "-map", "[mixed]", "-c:a", "pcm_s24le", str(mix_pre)]
subprocess.run(cmd_mix, check=True)
print("Audio mixed.")

# 3. Loudness Normalization (-16 LUFS, TP -1.5)
master_wav = P / "master_audio.wav"
flt_loud = "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"
cmd_loud = [
    FFMPEG, "-v", "error", "-y",
    "-i", str(mix_pre),
    "-af", flt_loud,
    "-c:a", "pcm_s24le", str(master_wav)
]
subprocess.run(cmd_loud, check=True)
print(f"Master audio generated: {master_wav}")
