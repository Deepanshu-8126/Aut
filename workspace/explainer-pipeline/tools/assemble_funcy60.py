# FUNCYOUS 60 - "The Pump That Feels" gas pump auto-shutoff (HYBRID: 2 LTX clips + 16.8s code cutaway)
import subprocess, os, glob
from PIL import Image, ImageDraw, ImageFont

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/f60'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
OUT = '/home/user/outputs/60-gas-pump-funcyous.mp4'
VO = '/var/tmp/funcy60/vo60.mp3'
SRC = '/var/tmp/funcy60/out/outputs'
CODE_FR = '/var/tmp/funcy60/code_frames'   # 504 pre-rendered frames
CTA = '/var/tmp/f59/cta_seg.mp4'

def clip_for(seed):
    g = sorted(glob.glob(f'{SRC}/ltx25_*_seed{seed}.mp4'))
    assert g, f'missing clip seed {seed}'
    return g[0]
CL = {'f1':clip_for(501),'f2':clip_for(502)}
FPS = 30
VOSPEED = 1.18
VODUR = 43.66/VOSPEED          # 37.00

# cuts: (clip|'CODE', ss, dur, zoom, stretch)
CUTS = [
 ('f1', 0.00, 5.40, 1.00, 1.08),
 ('f2', 0.00, 4.20, 1.00, 1.0),
 ('f2', 1.40, 3.20, 1.30, 1.0),
 ('CODE',0.0, 16.80, 1.00, 1.0),
 ('f2', 2.00, 3.00, 1.32, 1.0),
 ('f1', 0.20, 4.80, 1.10, 1.0),
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
            im = Image.open(fr)
            im.save(f'{AF}/{n_all:05d}.jpg', quality=92)
        print(f'cut {i} CODE {nf}fr', flush=True)
        continue
    cd = f'{W}/c{i}'; os.makedirs(cd, exist_ok=True)
    for f in glob.glob(f'{cd}/*.jpg'): os.remove(f)
    vf = []
    if stretch > 1.0:
        vf.append(f'setpts={stretch}*PTS')
        vf.append(f'minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1')
        src_t = dur/stretch
    else:
        vf.append(f'fps={FPS}')
        src_t = dur
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
        # loop f1 ambience for code section
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

# ---- captions ----
SCRIPT = ("Every gas pump knows the exact second your tank is full. No sensor. No chip. Not even a battery. "
 "The secret is a tiny hole, hidden right at the tip of the nozzle. While fuel flows, that hole quietly "
 "breathes air — holding a small vacuum behind a spring-loaded diaphragm. But the instant fuel rises high "
 "enough to swallow the hole... the breathing stops. The vacuum spikes. The diaphragm snaps backward — and "
 "CLICK. The handle shuts itself off. Pure suction. A spring. A sixty-year-old physics trick. The pump never "
 "measured your tank... it felt the fuel touch its lips.")
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

FD = '/home/user/explainer-pipeline/assets/fonts'
F_CAP  = ImageFont.truetype(f'{FD}/Inter-SemiBold.ttf',56)
F_CAPB = ImageFont.truetype(f'{FD}/Montserrat-Black.ttf',58)
F_MONO = ImageFont.truetype(f'{FD}/JetBrainsMono-Bold.ttf',30)

LABELS = [
 ('SENSING HOLE',    (255,191,64), 13.3, 18.1),
 ('AIR: FLOWING',    (80,220,255), 15.0, 18.1),
 ('FUEL RISING',     (255,150,60), 18.4, 21.2),
 ('HOLE BLOCKED',    (255,80,80),  20.9, 24.1),
 ('VACUUM SPIKE',    (255,80,80),  23.0, 24.4),
 ('CLICK: SHUTOFF',  (90,230,120), 24.5, 29.4),
 ('NO ELECTRONICS',  (200,210,222),29.8, 32.4),
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
    wi = next((k for k,(w,s,e) in enumerate(times) if s<=tt<e), None)
    if wi is not None:
        c = wi//3; chunk = words[c*3:(c+1)*3]; base = c*3
        meas = [(dr.textlength(w+' ',font=(F_CAPB if (base+k)==wi else F_CAP))) for k,w in enumerate(chunk)]
        x = (1080-sum(meas))/2; y = 1700
        for k,wd in enumerate(chunk):
            active = (base+k)==wi
            f = F_CAPB if active else F_CAP
            col = (255,196,64,255) if active else (255,255,255,235)
            dr.text((x+1,y+2), wd, font=f, fill=(0,0,0,160))
            dr.text((x,y), wd, font=f, fill=col)
            x += meas[k]
    ly = 150
    for text,col,s,e in LABELS:
        if s<=tt<e:
            a = min(1.0,(tt-s)/0.25) * min(1.0,(e-tt)/0.25)
            w2 = dr.textlength(text, font=F_MONO)
            dr.rounded_rectangle([48,ly,48+w2+74,ly+52], 12, fill=(8,10,14,int(200*a)))
            dr.ellipse([70,ly+19,84,ly+33], fill=col+(int(255*a),))
            dr.text((100,ly+10), text, font=F_MONO, fill=(240,244,248,int(255*a)))
            ly += 66
    im.save(f'{AF}/{fi:05d}.jpg', quality=90)
    if fi % 300 == 0: print('composited', fi, flush=True)
print('composite done')

# ---- mux + CTA concat ----
MAIN = f'{W}/main.mp4'
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]volume=0.30,afade=t=out:st={DUR-1.0:.2f}:d=1.0[amb];"
      f"[vo][amb]amix=inputs=2:duration=longest:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',f'{W}/amb.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.06:saturation=1.1,noise=alls=4:allf=t,unsharp=5:5:0.3:3:3:0',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','28','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{DUR:.2f}','-movflags','+faststart', MAIN], check=True)
print('main mux ok')
subprocess.run([FF,'-nostdin','-y','-i',MAIN,'-i',CTA,
    '-filter_complex','[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]',
    '-map','[v]','-map','[a]',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','28','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-movflags','+faststart', OUT], check=True)
print('concat ok')

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
    n+=1
    f.write(f"{n}\n{fmt(DUR+0.25)} --> {fmt(DUR+3.05)}\nFollow for more hidden machines.\n\n")
print('=== FUNCY 60 DONE ===', OUT)
