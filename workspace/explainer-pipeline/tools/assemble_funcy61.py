# FUNCYOUS 61 - "ATM Bill Counter" (HYBRID + FULL RETENTION ARMOR)
# hook card frame-1 | pro captions (stroke) | callouts on LTX | loop ending, NO CTA
import subprocess, os, glob, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from funcy_retention import draw_hook_card, draw_captions_pro, draw_callout, draw_subscribe_tap

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/f61'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
OUT = '/home/user/outputs/61-atm-counter-funcyous.mp4'
VO = '/var/tmp/funcy61/vo61.mp3'
SRC = '/var/tmp/funcy61/out/outputs'
CODE_FR = '/var/tmp/funcy61/code_frames'

def clip_for(seed):
    g = sorted(glob.glob(f'{SRC}/ltx25_*_seed{seed}.mp4'))
    assert g, f'missing clip seed {seed}'
    return g[0]
CL = {'f1':clip_for(601),'f2':clip_for(602)}
FPS = 30
VOSPEED = 1.18
VODUR = 40.34/VOSPEED          # 34.19

CUTS = [
 ('f1', 0.00, 5.40, 1.00, 1.08),   # bright ATM push-in (hook)
 ('f2', 0.00, 3.80, 1.00, 1.0),    # bills macro - roller
 ('f2', 1.60, 2.20, 1.30, 1.0),    # ZOOM roller grabs note
 ('CODE',0.0, 16.80, 1.00, 1.0),   # X-ray: counter machine
 ('f2', 2.40, 2.40, 1.32, 1.0),    # ZOOM - "never trusts"
 ('f1', 0.50, 4.00, 1.10, 1.0),    # ender = same as opener -> LOOP
]
DUR = sum(c[2] for c in CUTS)
print('main video', round(DUR,2))
for clip,ss,dur,zoom,stretch in CUTS:
    if clip!='CODE': assert ss + dur/stretch <= 5.02, f'overrun {clip}'

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
    vf = []
    if stretch > 1.0:
        vf.append(f'setpts={stretch}*PTS')
        vf.append(f'minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1')
        src_t = dur/stretch
    else:
        vf.append(f'fps={FPS}'); src_t = dur
    if zoom > 1.0:
        zw, zh = int(1080*zoom)//2*2, int(1920*zoom)//2*2
        vf.append(f'scale={zw}:{zh}:flags=lanczos')
        vf.append(f'crop=1080:1920:{(zw-1080)//2}:{(zh-1920)//2}')
    else:
        vf.append('scale=1080:1920:flags=lanczos')
    subprocess.run([FF,'-nostdin','-y','-ss',f'{ss:.3f}','-t',f'{src_t+0.25:.3f}','-i',CL[clip],
        '-vf',','.join(vf),'-qscale:v','3','-vframes',str(nf), f'{cd}/%05d.jpg'],
        check=True, capture_output=True)
    frames = sorted(glob.glob(f'{cd}/*.jpg'))[:nf]
    for fr in frames:
        n_all += 1
        os.rename(fr, f'{AF}/{n_all:05d}.jpg')
    print(f'cut {i} {clip} {len(frames)}fr', flush=True)
N = n_all
print('ALLFRAMES', N)

# ---- ambience ----
alist = []
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    seg = f'{W}/a{i}.wav'
    if clip=='CODE':
        subprocess.run([FF,'-nostdin','-y','-stream_loop','3','-i',CL['f1'],'-vn',
            '-af',f'atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume=0.8','-ar','44100','-ac','2',seg],
            check=True, capture_output=True)
    else:
        af = f'atempo={1/stretch:.4f},' if stretch>1.0 else ''
        src_t = dur/stretch if stretch>1.0 else dur
        subprocess.run([FF,'-nostdin','-y','-ss',f'{ss:.3f}','-t',f'{src_t:.3f}','-i',CL[clip],
            '-vn','-af',f'{af}atrim=0:{dur:.3f},asetpts=PTS-STARTPTS','-ar','44100','-ac','2',seg],
            check=True, capture_output=True)
    alist.append(seg)
with open(f'{W}/alist.txt','w') as f:
    for s in alist: f.write(f"file '{s}'\n")
subprocess.run([FF,'-nostdin','-y','-f','concat','-safe','0','-i',f'{W}/alist.txt',
    '-c:a','pcm_s16le', f'{W}/amb.wav'], check=True, capture_output=True)
print('amb ok')

# ---- captions timing ----
SCRIPT = ("Every time an ATM counts your cash... it's running a physics exam — at ten bills per second. "
 "Inside, a spinning friction wheel grabs exactly one note. Too thick? Two bills stuck together? "
 "A thickness sensor feels it instantly — and flicks the pair into a secret reject bin. Every single "
 "note is scanned by light... measured... timed... as it flies through at highway speed. Wrong thickness? "
 "Wrong magnetism? Rejected. The machine never trusts a single bill. That's why your cash is never wrong. "
 "A hundred decisions... in one second flat.")
words = [w for w in SCRIPT.replace('—',' ').split() if w.strip()]
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
LABELS = [
 ('FEED: 10/SEC',     (255,191,64), 11.9, 15.0),
 ('THICKNESS CHECK',  (80,220,255), 14.7, 17.7),
 ('DOUBLE DETECTED',  (255,80,80),  16.3, 19.3),
 ('REJECT BIN',       (255,150,60), 18.1, 21.0),
 ('OPTICAL SCAN',     (80,220,255), 21.2, 24.2),
 ('MAGNETIC TEST',    (255,191,64), 22.6, 25.8),
 ('COUNT: VERIFIED',  (90,230,120), 25.9, 28.1),
 ('100 DECISIONS/SEC',(255,191,64), 31.0, 34.1),
]
gr = Image.new('L',(1,420),0)
for y in range(420): gr.putpixel((0,y), int(170*(y/420)**1.5))
grad = gr.resize((1080,420))

for fi in range(1, N+1):
    tt = (fi-0.5)/FPS
    im = Image.open(f'{AF}/{fi:05d}.jpg').convert('RGB')
    black = Image.new('RGBA',(1080,420),(0,0,0,255)); black.putalpha(grad)
    im.paste(Image.alpha_composite(im.crop((0,1500,1080,1920)).convert('RGBA'), black).convert('RGB'),(0,1500))
    dr = ImageDraw.Draw(im,'RGBA')
    # chips
    ly = 150
    for text,col,s,e in LABELS:
        if s<=tt<e:
            a = min(1.0,(tt-s)/0.25) * min(1.0,(e-tt)/0.25)
            w2 = dr.textlength(text, font=F_MONO)
            dr.rounded_rectangle([48,ly,48+w2+74,ly+52], 12, fill=(8,10,14,int(200*a)))
            dr.ellipse([70,ly+19,84,ly+33], fill=col+(int(255*a),))
            dr.text((100,ly+10), text, font=F_MONO, fill=(240,244,248,int(255*a)))
            ly += 66
    # callouts on real footage
    draw_callout(im, tt, 2.4, 4.9, 540, 1340, 170, 'DISPENSER', side='right')
    draw_callout(im, tt, 6.0, 8.9, 830, 820, 160, 'FRICTION WHEEL', side='left')
    # subscribe tap - mid-video, high-retention beat (loop stays intact)
    draw_subscribe_tap(im, tt, 20.2)
    # pro captions
    draw_captions_pro(im, tt, times, words)
    # hook card (on top of everything)
    draw_hook_card(im, tt, '10 BILLS. 1 SECOND.', 'ZERO MISTAKES.')
    im.save(f'{AF}/{fi:05d}.jpg', quality=90)
    if fi % 300 == 0: print('composited', fi, flush=True)
print('composite done')

# ---- mux (NO CTA - loop ending) ----
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]volume=0.30,afade=t=out:st={DUR-0.6:.2f}:d=0.6[amb];"
      f"[vo][amb]amix=inputs=2:duration=longest:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',f'{W}/amb.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.05:saturation=1.08,noise=alls=4:allf=t,unsharp=5:5:0.3:3:3:0',
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
print('=== FUNCY 61 DONE ===', OUT)
