# CHRONIC #02 - "D.B. Cooper" - 100% code visuals (defencesquad-style), no LTX
import subprocess, os, glob, sys, wave, struct, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from funcy_retention import draw_captions_pro

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
FR = '/var/tmp/dbc02fr'
W = '/var/tmp/dbc02'; os.makedirs(W, exist_ok=True)
OUT = '/home/user/outputs/c02-dbcooper-chronic.mp4'
VO = '/home/user/explainer-pipeline/assets/dbc02/vo_fixed.wav'
MUSIC = '/var/tmp/music605loop.wav'
FPS = 30; DUR = 59.9; VOSPEED = 1.15
N = int(DUR*30)+1

# ---- SFX ----
SR = 44100
TN = int(DUR*SR); mix = [0.0]*TN
def add(at, samples, g=1.0):
    s0 = int(at*SR)
    for k, v in enumerate(samples):
        i = s0+k
        if 0 <= i < TN: mix[i] += v*g
def thud():      # stamp slam: low punch + noise snap
    L = int(0.30*SR); out = []
    for i in range(L):
        x = i/L
        env = math.exp(-7*x)
        out.append(0.55*env*math.sin(2*math.pi*(95-40*x)*i/SR) + 0.22*env*math.sin(2*math.pi*2950*i/SR)*math.exp(-30*x))
    return out
def paper():     # soft paper whoosh
    import random
    random.seed(7)
    L = int(0.4*SR); out = []; lp = 0.0
    for i in range(L):
        x = i/L
        n = random.uniform(-1,1)
        lp = lp + 0.12*(n-lp)
        out.append(0.30*math.sin(math.pi*x)*lp)
    return out
def braam():   # deep cinematic hit at hook
    L = int(2.6*SR); out = []
    for i in range(L):
        x = i/L
        env = min(1.0, x/0.06) * math.exp(-2.2*x)
        v = 0.0
        for f,g in ((52,0.30),(78,0.18),(104,0.14),(156,0.07)):
            v += g*math.sin(2*math.pi*f*i/SR + 0.8*math.sin(2*math.pi*0.7*i/SR))
        out.append(env*v)
    return out
def riser():   # 1.1s noise sweep INTO a stamp
    import random
    random.seed(11)
    L = int(1.1*SR); out = []; lp = 0.0
    for i in range(L):
        x = i/L
        n = random.uniform(-1,1)
        k = 0.04 + 0.5*x*x
        lp = lp + k*(n-lp)
        out.append(0.26*x*x*lp)
    return out
def heart():   # lub-dub
    L = int(0.42*SR); out = [0.0]*L
    for st,g in ((0,0.5),(int(0.16*SR),0.34)):
        for i in range(int(0.12*SR)):
            if st+i < L:
                out[st+i] += g*math.exp(-16*i/SR*8)*math.sin(2*math.pi*54*i/SR)
    return out
TH = thud(); PA = paper(); BR = braam(); RI = riser(); HB = heart()
add(0.55, BR, 1.0)                                                 # hook braam
for at in (10.4, 14.6, 17.4, 27.0, 38.0):
    add(at-1.05, RI, 1.0)                                          # riser into stamp
    add(at, TH, 1.0)                                               # stamp thud
tpos = 45.6
while tpos < 56.2:
    add(tpos, HB, 1.0)                                             # heartbeat under A/B/C
    tpos += 1.0
for at in (6.8, 11.6, 15.6, 18.3, 28.8, 44.9, 57.0): add(at-0.15, PA, 1.0)  # scene cuts
w = wave.open(f'{W}/sfx.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(b''.join(struct.pack('<hh', int(max(-1,min(1,v))*32767), int(max(-1,min(1,v))*32767)) for v in mix)); w.close()
print('sfx ok', flush=True)

# ---- captions ----
SCRIPT = ("November 24th, 1971. A man in a black tie boards Flight 305 out of Portland. He orders a "
 "bourbon — then hands the flight attendant a note. I have a bomb. He asks for two hundred thousand "
 "dollars... and four parachutes. In Seattle, he releases every passenger. Then the plane takes off "
 "again — flying low, and slow. Somewhere over the dark forests of Washington... he lowers the rear "
 "stairs of the Boeing 727... and steps into the night. In 1980, a boy digging on a riverbank found "
 "three bundles of his cash. Nothing else. No body. No parachute. No name. The FBI closed the case in "
 "2016 — it's still America's only unsolved hijacking. So what happened to him? A — he died in the "
 "jump. B — he escaped clean. C — he's been hiding in plain sight. Comment your verdict.")
SENT = [
 ("November 24th, 1971.", 0.33, 3.01),
 ("A man in a black tie boards Flight 305 out of Portland.", 3.47, 7.40),
 ("He orders a bourbon", 7.85, 8.64),
 ("then hands the flight attendant a note.", 9.08, 10.85),
 ("I have a bomb.", 11.53, 12.41),
 ("He asks for two hundred thousand dollars...", 13.13, 15.39),
 ("and four parachutes.", 15.73, 16.97),
 ("In Seattle, he releases every passenger.", 17.68, 20.37),
 ("Then the plane takes off again flying low, and slow.", 20.81, 24.01),
 ("Somewhere over the dark forests of Washington...", 24.77, 27.08),
 ("he lowers the rear stairs of the Boeing 727...", 27.37, 30.25),
 ("and steps into the night.", 30.79, 31.98),
 ("In 1980, a boy digging on a riverbank found three bundles of his cash.", 32.91, 37.76),
 ("Nothing else.", 38.43, 39.02),
 ("No body.", 39.61, 40.16),
 ("No parachute.", 40.65, 41.43),
 ("No name.", 42.00, 42.60),
 ("The FBI closed the case in 2016, it's still America's only unsolved hijacking.", 43.46, 50.92),
 ("So what happened to him?", 51.67, 53.40),
 ("A, he died in the jump.", 54.09, 55.81),
 ("B, he escaped clean.", 56.52, 58.87),
 ("C, he's been hiding in plain sight.", 59.98, 62.84),
 ("Comment your verdict.", 63.37, 64.42),
]
words = []; times = []
for txt, n0, n1 in SENT:
    ws = [x for x in txt.split() if x.strip()]
    wts = [len(x)+1.2 for x in ws]; tot = sum(wts); acc = 0.0
    T0s, T1s = n0/VOSPEED+0.25, n1/VOSPEED+0.25
    for x, wt in zip(ws, wts):
        st = T0s+(T1s-T0s)*acc/tot; acc += wt; en = T0s+(T1s-T0s)*acc/tot
        words.append(x); times.append((x, st, en))

gr = Image.new('L',(1,360),0)
for y in range(360): gr.putpixel((0,y), int(150*(y/360)**1.5))
grad = gr.resize((1080,360))
for fi in range(1, N+1):
    tt = (fi-0.5)/FPS
    fp = f'{FR}/f{fi-1:05d}.jpg'
    im = Image.open(fp).convert('RGB')
    black = Image.new('RGBA',(1080,360),(0,0,0,255)); black.putalpha(grad)
    im.paste(Image.alpha_composite(im.crop((0,1560,1080,1920)).convert('RGBA'), black).convert('RGB'),(0,1560))
    draw_captions_pro(im, tt, times, words)
    im.save(f'{W}/{fi:05d}.jpg', quality=90)
    if fi % 400 == 0: print('composited', fi, flush=True)
print('composite done', flush=True)

# ---- mux ----
fc = (f"[1:a]atempo={VOSPEED},adelay=250|250,volume=1.0[vo];"
      f"[2:a]atrim=0:{DUR:.2f},volume=0.26,afade=t=in:st=0:d=0.8,afade=t=out:st={DUR-1.5:.2f}:d=1.5[mus];"
      f"[3:a]volume=0.9[sfx];"
      f"[vo][mus][sfx]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.9[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{W}/%05d.jpg',
    '-i',VO,'-i',MUSIC,'-i',f'{W}/sfx.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.04:saturation=1.05,noise=alls=3:allf=t,unsharp=5:5:0.3:3:3:0',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','26','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{DUR:.2f}','-movflags','+faststart', OUT], check=True)
print('mux ok', flush=True)

# ---- srt ----
chunks = [words[i:i+3] for i in range(0,len(words),3)]
def fmt(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x%1*1000):03d}"
with open(OUT.replace('.mp4','.srt'),'w') as f:
    n = 0
    for c in range(len(chunks)):
        ws = times[c*3:(c+1)*3]
        if not ws: break
        n += 1
        f.write(f"{n}\n{fmt(ws[0][1])} --> {fmt(ws[-1][2])}\n{' '.join(chunks[c])}\n\n")
print('=== DBC02 DONE ===', OUT)
