#!/usr/bin/env python3
# FUNCYOUS VIDEO 63 — CAR KEY ROLLING CODE (MODE 2B + RETENTION ARMOR)
# Clone of assemble_funcy62.py recipe; frames are pure-code (scene63.html), no clip CUTS.
import os, sys, math, wave, struct, subprocess, json
sys.path.insert(0, '/var/tmp/pydeps')
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from PIL import Image, ImageDraw, ImageFont
from funcy_retention import (draw_hook_card, draw_captions_pro,
                             draw_callout, draw_subscribe_tap)

FF   = '/var/tmp/ffstatic/ffmpeg'
FP   = '/var/tmp/ffstatic/ffprobe'
A    = '/home/user/explainer-pipeline/assets/fun61'
FR   = '/var/tmp/fr63'
CMP  = '/var/tmp/comp63'
OUT  = '/home/user/outputs/63-car-key-funcyous.mp4'
SRT  = '/home/user/outputs/63-car-key-funcyous.srt'
FD   = '/home/user/explainer-pipeline/assets/fonts'

FPS, DUR, N = 30, 45.0, 1350
VOSPEED     = 1.18
RAW_VO      = 47.699592
VODUR       = RAW_VO / VOSPEED          # 40.42
CTA_T0      = 40.76

SCRIPT = ("Every time you press your car key, it sends a secret code, and it will never send that code again. "
"Here's why that matters: a thief with a cheap radio can record your signal from across a parking lot. "
"Play it back... and nothing happens. "
"Because inside your fob, a tiny chip burns through codes like one-time passwords. "
"Every press runs a secret formula, and the exact same formula runs inside your car, counting up in perfect sync. "
"The recorded code? Already used. Dead on arrival. "
"Pressed the button away from your car? No problem. It accepts any of the next 256 codes in line. "
"So that little click you just heard... was a code being born, and dying, in the same second.")
CTA_TXT = "One hidden machine, every day... subscribe for tomorrow's."

# ---------- caption timing: PER-LINE char-weighted (word-sync fix) ----------
def weight(w): return len(w) + 1.2
LINES = [
 ("Every time you press your car key, it sends a secret code, and it will never send that code again.", 0.12, 4.97),
 ("Here's why that matters: a thief with a cheap radio can record your signal from across a parking lot.", 5.10, 10.08),
 ("Play it back... and nothing happens.", 10.20, 12.32),
 ("Because inside your fob, a tiny chip burns through codes like one-time passwords.", 12.44, 17.40),
 ("Every press runs a secret formula, and the exact same formula runs inside your car, counting up in perfect sync.", 17.52, 24.25),
 ("The recorded code? Already used. Dead on arrival.", 24.38, 27.82),
 ("Pressed the button away from your car? No problem. It accepts any of the next 256 codes in line.", 27.94, 34.22),
 ("So that little click you just heard... was a code being born, and dying, in the same second.", 34.35, 40.51)]
times = []
for (txt, ls, le) in LINES:
    lw = txt.split()
    tot = sum(weight(w) for w in lw)
    t0, t1 = ls + 0.05, le - 0.03
    acc = 0.0
    for w in lw:
        s = t0 + (t1 - t0) * acc / tot
        acc += weight(w)
        e = t0 + (t1 - t0) * acc / tot
        times.append((w, s, e))

# CTA phrase words
cta_dur_raw = float(subprocess.check_output(
    [FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{A}/cta63.mp3']).strip())
CTA_SP = max(1.06, cta_dur_raw / (44.85 - CTA_T0))
cta_len = cta_dur_raw / CTA_SP
cw = CTA_TXT.split()
ctot = sum(weight(w) for w in cw)
acc = 0.0
for w in cw:
    s = CTA_T0 + 0.10 + (cta_len - 0.2) * acc / ctot
    acc += weight(w)
    e = CTA_T0 + 0.10 + (cta_len - 0.2) * acc / ctot
    times.append((w, s, e))
words_all = [w for w, _, _ in times]

# ---------- LABELS chips (JBM 30 @ x48 y150) ----------
F_CHIP = ImageFont.truetype(f'{FD}/JetBrainsMono-Bold.ttf', 30)
LABELS = [(0.40, 4.90, 'ROLLING CODE'),
          (5.20, 10.00, 'REPLAY ATTACK'),
          (10.30, 12.30, 'SIGNAL REJECTED'),
          (12.60, 17.30, 'INSIDE THE FOB'),
          (17.70, 24.20, 'SYNCED COUNTERS'),
          (24.50, 27.70, 'CODE EXPIRED'),
          (28.10, 34.10, '256-CODE WINDOW'),
          (34.50, 40.40, 'BORN + DIES IN 1 SEC')]

def draw_chip(im, tt):
    for (s, e, txt) in LABELS:
        if not (s <= tt < e):
            continue
        a = min(1.0, (tt - s) / 0.25, (e - tt) / 0.25)
        a = max(0.0, a)
        dr = ImageDraw.Draw(im, 'RGBA')
        tw = dr.textlength(txt, font=F_CHIP)
        x, y, h = 48, 150, 54
        w = int(tw + 76)
        dr.rounded_rectangle([x, y, x + w, y + h], 16,
                             fill=(8, 10, 14, int(200 * a)),
                             outline=(70, 80, 95, int(160 * a)), width=2)
        dr.ellipse([x + 20, y + h/2 - 7, x + 34, y + h/2 + 7],
                   fill=(255, 182, 61, int(255 * a)))
        dr.text((x + 50, y + h/2 - 19), txt, font=F_CHIP,
                fill=(255, 255, 255, int(255 * a)))
        break

# ---------- composite pass ----------
os.makedirs(CMP, exist_ok=True)
print('compositing', N, 'frames...')
for f in range(N):
    dst = f'{CMP}/f{f:05d}.jpg'
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        continue
    tt = f / FPS
    im = Image.open(f'{FR}/f{f:05d}.jpg').convert('RGB')
    dr = ImageDraw.Draw(im, 'RGBA')
    # bottom gradient 1500->1920
    for yy in range(1500, 1920, 4):
        aa = int(((yy - 1500) / 420.0) ** 1.5 * 185)
        dr.rectangle([0, yy, 1080, yy + 4], fill=(0, 0, 0, aa))
    draw_chip(im, tt)
    draw_callout(im, tt, 13.00, 14.10, 494, 700, 75, 'ONE PRESS = ONE CODE', 'right')
    draw_callout(im, tt, 14.40, 15.70, 540, 960, 95, 'CODE ENGINE', 'left')
    draw_subscribe_tap(im, tt, 25.00)
    draw_subscribe_tap(im, tt, 41.20)
    draw_captions_pro(im, tt, times, words_all)
    draw_hook_card(im, tt, 'YOUR CAR KEY', 'NEVER REPEATS')
    im.save(dst, quality=90)
    if f % 200 == 0:
        print('comp', f, flush=True)
print('composite done')

# ---------- SFX synth (pure python, deterministic) ----------
SR = 44100
buf = [0.0] * int(SR * DUR)
_seed = [12345]
def rnd():
    _seed[0] = (_seed[0] * 1103515245 + 12345) & 0x7fffffff
    return _seed[0] / 0x7fffffff * 2 - 1

def place(samples, at, gain):
    i0 = int(at * SR)
    for i, v in enumerate(samples):
        j = i0 + i
        if 0 <= j < len(buf):
            buf[j] += v * gain

def whoosh(dur=0.5):
    n = int(dur * SR); out = []; lp = 0.0
    for i in range(n):
        u = i / n
        cut = 0.04 + 0.25 * math.sin(math.pi * u)
        lp += cut * (rnd() - lp)
        out.append(lp * math.sin(math.pi * u))
    return out

def click():
    n = int(0.05 * SR); out = []
    for i in range(n):
        u = i / n
        out.append((rnd() * 0.5 + math.sin(2 * math.pi * 1700 * i / SR) * 0.6) * (1 - u) ** 3)
    return out

def thud(dur=0.32, f0=76.0):
    n = int(dur * SR); out = []
    for i in range(n):
        u = i / n
        out.append(math.sin(2 * math.pi * f0 * (1 - 0.3 * u) * i / SR) * (1 - u) ** 2)
    return out

def ding():
    n = int(0.45 * SR); out = []
    for i in range(n):
        u = i / n
        out.append((math.sin(2 * math.pi * 880 * i / SR) * 0.6 +
                    math.sin(2 * math.pi * 1318 * i / SR) * 0.4) * (1 - u) ** 2.4)
    return out

CUTS_T = [2.6, 5.03, 7.6, 10.14, 12.38, 14.2, 15.8, 17.46, 19.8, 21.8,
          24.31, 26.0, 27.88, 30.5, 32.3, 34.28, 37.4, 40.76]
for ct in CUTS_T:
    place(whoosh(), max(0, ct - 0.25), 0.5)
for pt in [13.28, 14.88, 16.28, 18.76, 20.76, 22.76, 35.18, 41.66, 43.36]:
    place(click(), pt, 0.55)
place(thud(), 25.61, 0.85)
for dt in [29.18, 32.68]:
    place(ding(), dt, 0.4)

with wave.open(f'{A}/sfx63.wav', 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    frames = bytearray()
    for v in buf:
        s = int(max(-1, min(1, v)) * 32000)
        frames += struct.pack('<hh', s, s)
    wf.writeframes(frames)
print('sfx done')

# ---------- mux ----------
cta_ms = int(CTA_T0 * 1000)
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120[vo];"
      f"[2:a]atrim=0:{DUR},volume=0.20,afade=t=in:d=0.6,afade=t=out:st={DUR-1.5}:d=1.4[mus];"
      f"[3:a]volume=0.9[sfx];"
      f"[4:a]atrim=0.02:{cta_dur_raw:.2f},asetpts=PTS-STARTPTS,atempo={CTA_SP:.4f},"
      f"adelay={cta_ms}|{cta_ms}[cta];"
      f"[vo][mus][sfx][cta]amix=inputs=4:duration=longest:normalize=0,alimiter=limit=0.9[mix]")
cmd = [FF, '-nostdin', '-y',
       '-framerate', str(FPS), '-i', f'{CMP}/f%05d.jpg',
       '-i', f'{A}/vo63.mp3', '-i', f'{A}/music538.mp3',
       '-i', f'{A}/sfx63.wav', '-i', f'{A}/cta63.mp3',
       '-filter_complex', fc, '-map', '0:v', '-map', '[mix]',
       '-vf', 'eq=contrast=1.05:saturation=1.08,noise=alls=4:allf=t,unsharp=5:5:0.3:3:3:0',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '160k', '-ar', '44100',
       '-movflags', '+faststart', '-t', str(DUR), OUT]
subprocess.run(cmd, check=True)
print('mux done ->', OUT)

# ---------- srt (3-word chunks) ----------
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = int(x % 60); ms = int(x % 1 * 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
lines = []
for c in range(0, len(times), 3):
    ch = times[c:c+3]
    lines.append(f"{c//3+1}\n{ts(ch[0][1])} --> {ts(ch[-1][2])}\n{' '.join(w for w,_,_ in ch)}\n")
open(SRT, 'w').write('\n'.join(lines))
print('srt done ->', SRT)
