# CHRONIC #01 - "UVB-76 THE BUZZER" (STILL HAPPENING pillar)
# hybrid + full retention armor + real-photo dossier + synth buzzer SFX
import subprocess, os, glob, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from funcy_retention import draw_hook_card, draw_captions_pro, draw_callout, draw_subscribe_tap

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/c01'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
OUT = '/home/user/outputs/c01-uvb76-buzzer-chronic.mp4'
VO = '/var/tmp/chronic01/vo01.mp3'
SRC = '/var/tmp/chronic01/out/outputs'
CODE_FR = '/var/tmp/chronic01/code_frames'
REAL = sorted(glob.glob('/home/user/image-search/uvb-76*2.jpg'))[0]

def clip_for(seed):
    g = sorted(glob.glob(f'{SRC}/ltx25_*seed{seed}.mp4'))
    assert g, f'missing clip seed {seed}'
    return g[0]
CL = {'c1':clip_for(621),'c2':clip_for(622)}
FPS = 30
VOSPEED = 1.18
VODUR = 32.62/VOSPEED        # 27.64

CUTS = [
 ('c1', 0.00, 5.00, 1.00, 1.0),   # fog towers push-in (hook)
 ('c2', 0.00, 3.40, 1.00, 1.0),   # radio dial macro
 ('c2', 1.90, 1.80, 1.30, 1.0),   # ZOOM needle
 ('CODE',0.0, 12.00, 1.00, 1.0),  # spectrum/scope/map
 ('c1', 2.00, 2.80, 1.28, 1.0),   # ZOOM bunker "no one comes out"
 ('c1', 0.40, 3.80, 1.06, 1.0),   # ender = opener -> LOOP
]
DUR = sum(c[2] for c in CUTS)    # 28.8
print('main video', round(DUR,2))
for clip,ss,dur,zoom,stretch in CUTS:
    if clip!='CODE': assert ss + dur/stretch <= 5.02, f'overrun {clip} {ss} {dur}'

n_all = 0
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    nf = int(round(dur*FPS))
    if clip=='CODE':
        frames = sorted(glob.glob(f'{CODE_FR}/f*.jpg'))[:nf]
        assert len(frames)==nf, f'code frames {len(frames)} != {nf}'
        for fr in frames:
            n_all += 1
            Image.open(fr).save(f'{AF}/{n_all:05d}.jpg', quality=92)
        print(f'cut {i} CODE {nf}fr', flush=True); continue
    cd = f'{W}/c{i}'; os.makedirs(cd, exist_ok=True)
    for f in glob.glob(f'{cd}/*.jpg'): os.remove(f)
    vf = [f'fps={FPS}']
    if zoom > 1.0:
        zw, zh = int(1080*zoom)//2*2, int(1920*zoom)//2*2
        vf.append(f'scale={zw}:{zh}:flags=lanczos')
        vf.append(f'crop=1080:1920:{(zw-1080)//2}:{(zh-1920)//2}')
    else:
        vf.append('scale=1080:1920:flags=lanczos')
    subprocess.run([FF,'-nostdin','-y','-ss',f'{ss:.3f}','-t',f'{dur+0.25:.3f}','-i',CL[clip],
        '-vf',','.join(vf),'-qscale:v','3','-vframes',str(nf), f'{cd}/%05d.jpg'],
        check=True, capture_output=True)
    frames = sorted(glob.glob(f'{cd}/*.jpg'))[:nf]
    assert len(frames)==nf, f'cut {i} got {len(frames)}'
    for fr in frames:
        n_all += 1
        os.rename(fr, f'{AF}/{n_all:05d}.jpg')
    print(f'cut {i} {clip} {len(frames)}fr', flush=True)
N = n_all
print('ALLFRAMES', N)

# ---- ambience (LTX audio) ----
alist = []
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    seg = f'{W}/a{i}.wav'
    src = CL['c1'] if clip=='CODE' else CL[clip]
    ss2 = 0.0 if clip=='CODE' else ss
    loop = ['-stream_loop','3'] if clip=='CODE' else []
    subprocess.run([FF,'-nostdin','-y',*loop,'-ss',f'{ss2:.3f}','-i',src,'-vn',
        '-af',f'atrim=0:{dur:.3f},asetpts=PTS-STARTPTS','-ar','44100','-ac','2',seg],
        check=True, capture_output=True)
    alist.append(seg)
with open(f'{W}/alist.txt','w') as f:
    for s in alist: f.write(f"file '{s}'\n")
subprocess.run([FF,'-nostdin','-y','-f','concat','-safe','0','-i',f'{W}/alist.txt',
    '-c:a','pcm_s16le', f'{W}/amb.wav'], check=True, capture_output=True)

# ---- synth BUZZER SFX (the star) ----
# REAL shortwave buzzer feel: raspy sawtooth (rich harmonics) + pitch drift
# + breathing static between bursts (AGC pump) + radio bandpass. v2.
import wave, struct, random
random.seed(76)
SR = 44100
nsamp = int(DUR*SR)
F0 = 112.0
HARM = [(h, 1.0/h) for h in range(1, 26)]
raw = bytearray()
agc = 1.0
for i in range(nsamp):
    t = i/SR
    burst_on = (t % 2.4) < 0.8 and not (15.7 <= t <= 18.7)
    ph = t % 2.4
    env = (min(1.0, ph/0.05) * min(1.0, (0.8-ph)/0.09)) if burst_on else 0.0
    env = max(0.0, env)
    v = 0.0
    if env > 0:
        drift = 1.0 + 0.006*math.sin(2*math.pi*0.37*t) + 0.002*math.sin(2*math.pi*3.1*t)
        f = F0*drift
        for h, a in HARM:
            v += a*math.sin(2*math.pi*f*h*t)
        v *= 0.035*env
        v *= (0.9 + 0.1*math.sin(2*math.pi*50*t))        # mains-hum roughness
    # breathing static: louder in gaps (radio AGC), quieter under buzz
    target = 0.5 if env > 0.3 else 1.6
    agc += (target-agc)*0.00012                            # ~50ms smoothing at 44k
    v += (random.random()-0.5)*0.022*agc
    if t >= 25.2: v *= 1.8
    s = max(-0.95, min(0.95, v))
    pk = struct.pack('<h', int(s*32767))
    raw += pk + pk
with wave.open(f'{W}/buzz_raw.wav','wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes(bytes(raw))
# radio speaker voicing: narrow bandpass kills synthy lows/highs
subprocess.run([FF,'-nostdin','-y','-i',f'{W}/buzz_raw.wav',
    '-af','highpass=f=260,highpass=f=260,lowpass=f=2600,lowpass=f=2600,volume=2.2',
    '-ar','44100','-ac','2', f'{W}/buzz.wav'], check=True, capture_output=True)
print('amb+buzz ok')

# ---- captions timing ----
SCRIPT = ("In 1982, a lonely radio signal began to buzz. Twenty-five buzzes a minute. Every hour, of every day... "
 "for more than forty years. Nobody has ever claimed it. A few times a year, the buzzing stops... and a human "
 "voice reads out strange names, and numbers. Then the buzzer returns. Signal hunters traced it to a locked "
 "tower outside Moscow. No one ever comes out. And somewhere on the shortwave band... it is buzzing, right now.")
words = [w for w in SCRIPT.split() if w.strip()]
weights = [len(w)+1.2 for w in words]
total_w = sum(weights)
T0c, T1c = 0.30+0.12, VODUR-0.15+0.12
times = []; acc = 0.0
for w, wt in zip(words, weights):
    st = T0c + (T1c-T0c)*acc/total_w
    acc += wt
    en = T0c + (T1c-T0c)*acc/total_w
    times.append((w, st, en))

F_MONO = ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf',30)
F_TAG  = ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf',26)
LABELS = [
 ('LIVE SIGNAL',        (255,80,80),  10.7, 13.7),
 ('VOICE DETECTED',     (255,80,80),  15.7, 18.7),
 ('SOURCE LOCATED',     (90,230,120), 19.8, 22.2),
 ('STILL BROADCASTING', (255,80,80),  25.2, 28.4),
]
gr = Image.new('L',(1,420),0)
for y in range(420): gr.putpixel((0,y), int(170*(y/420)**1.5))
grad = gr.resize((1080,420))

# dossier prep: real photo polaroid
ph = Image.open(REAL).convert('RGB')
ph.thumbnail((560,560), Image.LANCZOS)
card = Image.new('RGB',(ph.width+28, ph.height+74),(236,236,230))
card.paste(ph,(14,14))
cd_d = ImageDraw.Draw(card)
cd_d.text((16, ph.height+26), 'SITE FOUND - ABANDONED', font=F_TAG, fill=(40,40,44))
card = card.rotate(-3.5, expand=True, resample=Image.BICUBIC, fillcolor=None)
mask = Image.new('L', card.size, 0)
md = ImageDraw.Draw(Image.new('RGB',(1,1)))  # placeholder
mask = Image.new('L',(ph.width+28, ph.height+74),255).rotate(-3.5, expand=True, resample=Image.BICUBIC)
DOS0, DOS1 = 19.2, 22.1

for fi in range(1, N+1):
    tt = (fi-0.5)/FPS
    im = Image.open(f'{AF}/{fi:05d}.jpg').convert('RGB')
    black = Image.new('RGBA',(1080,420),(0,0,0,255)); black.putalpha(grad)
    im.paste(Image.alpha_composite(im.crop((0,1500,1080,1920)).convert('RGBA'), black).convert('RGB'),(0,1500))
    dr = ImageDraw.Draw(im,'RGBA')
    ly = 150
    for text,col,s,e in LABELS:
        if s<=tt<e:
            a = min(1.0,(tt-s)/0.25) * min(1.0,(e-tt)/0.25)
            w2 = dr.textlength(text, font=F_MONO)
            dr.rounded_rectangle([48,ly,48+w2+74,ly+52], 12, fill=(8,10,14,int(200*a)))
            dr.ellipse([70,ly+19,84,ly+33], fill=col+(int(255*a),))
            dr.text((100,ly+10), text, font=F_MONO, fill=(240,244,248,int(255*a)))
            ly += 66
    # dossier real-photo slide-in during map segment
    if DOS0 <= tt < DOS1:
        k_in  = min(1.0,(tt-DOS0)/0.4); k_in = 1-(1-k_in)**3
        k_out = min(1.0,(DOS1-tt)/0.3)
        px = int(1080 - (card.width+40)*k_in) + int((1-k_out)*200)
        im.paste(card,(px, 560), mask)
    # callouts on real footage
    draw_callout(im, tt, 5.8, 8.2, 640, 760, 190, '4625 kHz', side='right')
    draw_callout(im, tt, 22.5, 24.7, 260, 1500, 150, 'THE LOCKED SITE', side='right')
    # subscribe tap mid-video
    draw_subscribe_tap(im, tt, 18.8)
    draw_captions_pro(im, tt, times, words)
    draw_hook_card(im, tt, 'BUZZING SINCE 1982.', 'NOBODY KNOWS.')
    im.save(f'{AF}/{fi:05d}.jpg', quality=90)
    if fi % 300 == 0: print('composited', fi, flush=True)
print('composite done')

# ---- mux (NO CTA - loop ending) ----
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]volume=0.26,afade=t=out:st={DUR-0.6:.2f}:d=0.6[amb];"
      f"[3:a]volume=0.85,afade=t=out:st={DUR-0.4:.2f}:d=0.4[bz];"
      f"[vo][amb][bz]amix=inputs=3:duration=longest:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',f'{W}/amb.wav','-i',f'{W}/buzz.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.06:saturation=1.05,noise=alls=4:allf=t,unsharp=5:5:0.3:3:3:0',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','27','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{DUR:.2f}','-movflags','+faststart', OUT], check=True)
print('mux ok')

# ---- srt ----
chunks = [words[i:i+3] for i in range(0,len(words),3)]
def fmt(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x%1*1000):03d}"
with open(OUT.replace('.mp4','.srt'),'w') as f:
    n=0
    for c in range(len(chunks)):
        ws = times[c*3:(c+1)*3]
        if not ws: break
        n+=1
        f.write(f"{n}\n{fmt(ws[0][1])} --> {fmt(ws[-1][2])}\n{' '.join(chunks[c])}\n\n")
print('=== CHRONIC 01 DONE ===', OUT)
