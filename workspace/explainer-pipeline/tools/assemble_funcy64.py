#!/usr/bin/env python3
# FUNCYOUS VIDEO 64 — SHOPPING CART INVISIBLE WHEEL-LOCK FENCE
# Clone of assemble_funcy63.py recipe. No CTA (loop ender law, <1K subs).
import os, sys, math, wave, struct, subprocess
sys.path.insert(0, '/var/tmp/pydeps')
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from PIL import Image, ImageDraw, ImageFont
from funcy_retention import (draw_hook_card, draw_captions_pro,
                             draw_callout, draw_subscribe_tap)

FF   = '/var/tmp/ffstatic/ffmpeg'
A    = '/home/user/explainer-pipeline/assets/fun64'
FR   = '/var/tmp/fr64'
CMP  = '/var/tmp/comp64'
OUT  = '/home/user/outputs/64-cart-wheel-funcyous.mp4'
SRT  = '/home/user/outputs/64-cart-wheel-funcyous.srt'
FD   = '/home/user/explainer-pipeline/assets/fonts'
MUS  = '/var/tmp/assets/music/538.mp3'

FPS, DUR, N = 30, 36.5, 1095
VOSPEED = 1.15

# VO chunks: (file, delay, raw_dur)
VO = [('vo_1.mp3', 0.30, 5.808),
      ('vo_2.mp3', 5.95, 6.216),
      ('vo_3.mp3', 11.75, 7.488),
      ('vo_4.mp3', 19.55, 7.152),
      ('vo_5.mp3', 27.00, 5.592)]
TEXTS = [
 "Try pushing a shopping cart past the edge of the parking lot. One wheel will slam its own brakes.",
 "Look inside that wheel. A radio receiver, a tiny motor, and a plastic shell that clamps around the hub.",
 "Buried under the asphalt, there's a loop of wire broadcasting one code, in a circle around the store. An invisible fence.",
 "Roll across that line, and the wheel hears it. It locks solid in half a second. Only the store's remote can wake it up again.",
 "So next time you see a cart frozen in the middle of nowhere, it didn't break. It crossed the line."]

# ---------- caption timing: per-chunk char-weighted ----------
def weight(w): return len(w) + 1.2
times = []
for (fn, dly, raw), txt in zip(VO, TEXTS):
    dur = raw / VOSPEED
    t0, t1 = dly + 0.05, dly + dur - 0.05
    lw = txt.split()
    tot = sum(weight(w) for w in lw)
    acc = 0.0
    for w in lw:
        s = t0 + (t1 - t0) * acc / tot
        acc += weight(w)
        e = t0 + (t1 - t0) * acc / tot
        times.append((w, s, e))
words_all = [w for w, _, _ in times]

# ---------- LABEL chips ----------
F_CHIP = ImageFont.truetype(f'{FD}/JetBrainsMono-Bold.ttf', 30)
LABELS = [(0.55, 5.30, 'WHEEL-LOCK SYSTEM'),
          (6.10, 11.30, 'INSIDE THE WHEEL'),
          (11.95, 18.20, 'BURIED WIRE LOOP'),
          (19.70, 25.70, 'LOCKED IN 0.5 SEC'),
          (27.20, 31.80, 'IT CROSSED THE LINE')]

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

# ---------- composite ----------
os.makedirs(CMP, exist_ok=True)
print('compositing', N, 'frames...')
for f in range(N):
    dst = f'{CMP}/f{f:05d}.jpg'
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        continue
    tt = f / FPS
    im = Image.open(f'{FR}/f{f:05d}.jpg').convert('RGB')
    dr = ImageDraw.Draw(im, 'RGBA')
    for yy in range(1500, 1920, 4):
        aa = int(((yy - 1500) / 420.0) ** 1.5 * 185)
        dr.rectangle([0, yy, 1080, yy + 4], fill=(0, 0, 0, aa))
    draw_chip(im, tt)
    # callouts during S2 component tour (world->out approx, verified on probes)
    draw_callout(im, tt, 7.10, 8.45, 580, 900, 78, 'RADIO RECEIVER', 'left')
    draw_callout(im, tt, 8.75, 9.90, 590, 1330, 70, 'MICRO MOTOR', 'left')
    draw_callout(im, tt, 10.10, 11.30, 390, 1140, 130, 'LOCKING CLAMP', 'right')
    draw_subscribe_tap(im, tt, 23.40)
    draw_captions_pro(im, tt, times, words_all)
    draw_hook_card(im, tt, 'INVISIBLE FENCE', 'IT HEARS YOU')
    im.save(dst, quality=90)
    if f % 300 == 0:
        print('comp', f, flush=True)
print('composite done')

# ---------- SFX synth ----------
SR = 44100
buf = [0.0] * int(SR * DUR)
_seed = [777]
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
def buzz(dur=0.8, f0=96.0):
    # motor whirr: saw-ish + tremolo
    n = int(dur * SR); out = []
    for i in range(n):
        u = i / n
        ph = (i * f0 / SR) % 1.0
        v = (ph * 2 - 1) * 0.5 + math.sin(2 * math.pi * f0 * 2 * i / SR) * 0.3
        env = math.sin(math.pi * u) * (0.75 + 0.25 * math.sin(2 * math.pi * 27 * i / SR))
        out.append(v * env)
    return out

CUTS_T = [2.80, 5.70, 8.60, 11.50, 14.60, 16.90, 19.30, 21.70, 23.60, 26.60, 29.60, 33.00]
for ct in CUTS_T:
    place(whoosh(), max(0, ct - 0.25), 0.5)
# callout + chip ticks
for pt in [7.15, 8.80, 10.15, 12.00, 16.95, 27.25]:
    place(click(), pt, 0.5)
# S4 lock sequence: motor buzz then SNAP
place(buzz(), 21.60, 0.5)
place(click(), 22.30, 0.9)
place(thud(0.34, 72), 22.32, 0.95)
# hook-card pop
place(click(), 0.12, 0.4)

with wave.open(f'{A}/sfx64.wav', 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    frames = bytearray()
    for v in buf:
        s = int(max(-1, min(1, v)) * 32000)
        frames += struct.pack('<hh', s, s)
    wf.writeframes(frames)
print('sfx done')

# ---------- music slice (offset for freshness vs 62) ----------
MUSB = '/var/tmp/assets/music/538b64.mp3'
subprocess.run([FF, '-nostdin', '-y', '-ss', '38', '-t', str(DUR + 2), '-i', MUS,
                '-c:a', 'libmp3lame', '-q:a', '4', MUSB], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ---------- mux ----------
ins = [FF, '-nostdin', '-y', '-framerate', str(FPS), '-i', f'{CMP}/f%05d.jpg']
for fn, _, _ in VO:
    ins += ['-i', f'{A}/{fn}']
ins += ['-i', MUSB, '-i', f'{A}/sfx64.wav']
fc = []
for i, (fn, dly, raw) in enumerate(VO):
    ms = int(dly * 1000)
    fc.append(f"[{i+1}:a]atempo={VOSPEED},adelay={ms}|{ms}[vo{i}]")
fc.append(f"[6:a]atrim=0:{DUR},volume=0.22,afade=t=in:d=0.6,afade=t=out:st={DUR-1.6}:d=1.5[mus]")
fc.append("[7:a]volume=0.9[sfx]")
fc.append("[vo0][vo1][vo2][vo3][vo4][mus][sfx]amix=inputs=7:duration=longest:normalize=0,alimiter=limit=0.82:level=0[mix]")
cmd = ins + ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[mix]',
       '-vf', 'eq=contrast=1.05:saturation=1.08,noise=alls=4:allf=t,unsharp=5:5:0.3:3:3:0',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '160k', '-ar', '44100',
       '-movflags', '+faststart', '-t', str(DUR), OUT]
subprocess.run(cmd, check=True)
print('mux done ->', OUT)

# ---------- srt ----------
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = int(x % 60); ms = int(x % 1 * 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
lines = []
for c in range(0, len(times), 3):
    ch = times[c:c+3]
    lines.append(f"{c//3+1}\n{ts(ch[0][1])} --> {ts(ch[-1][2])}\n{' '.join(w for w,_,_ in ch)}\n")
open(SRT, 'w').write('\n'.join(lines))
print('srt done ->', SRT)
