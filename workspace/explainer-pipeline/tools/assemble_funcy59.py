# FUNCYOUS 59 - "The Road Is Reading Your Car" traffic inductive loop short
# 9 cuts (6 base + 3 zoom variants) + English wordpop + label chips + VO 1.18x + CTA ender concat
import subprocess, os, glob
from PIL import Image, ImageDraw, ImageFont

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/f59'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
OUT = '/home/user/outputs/59-traffic-loop-funcyous.mp4'
VO = '/var/tmp/funcy59/vo59.mp3'
SRC = '/var/tmp/funcy59/out/outputs'
CTA = f'{W}/cta_seg.mp4'   # rebuilt from assets/funcy58 recipe

def clip_for(seed):
    g = sorted(glob.glob(f'{SRC}/ltx25_*_seed{seed}.mp4'))
    assert g, f'missing clip seed {seed}'
    return g[0]
CL = {'f1':clip_for(401),'f2':clip_for(402),'f3':clip_for(403),
      'f4':clip_for(404),'f5':clip_for(405),'f6':clip_for(406)}
FPS = 30
VOSPEED = 1.18
VODUR = 39.34/VOSPEED          # 33.34

# cuts: (clip, src_start, dur, zoom, stretch)  -- RULE: ss + dur/stretch <= 5.0
CUTS = [
 ('f1', 0.00, 5.40, 1.00, 1.10),   # aerial hook (stretched 1.10x, src 4.91)
 ('f2', 0.00, 4.00, 1.00, 1.0),    # asphalt macro - "thin black lines"
 ('f2', 2.00, 2.20, 1.30, 1.0),    # asphalt ZOOM - "it's an antenna"
 ('f3', 0.00, 4.00, 1.00, 1.0),    # cutaway coil - "buried coil of wire"
 ('f3', 1.20, 3.60, 1.30, 1.0),    # cutaway ZOOM - "pulsing magnetic field"
 ('f4', 0.00, 4.20, 1.00, 1.0),    # car on loop - "two tons of steel"
 ('f5', 0.00, 4.20, 1.00, 1.0),    # cabinet - "box on the corner"
 ('f4', 2.60, 1.80, 1.32, 1.0),    # car ZOOM - "no camera ever saw you"
 ('f6', 0.00, 4.80, 1.00, 1.0),    # green light ender
]
DUR = sum(c[2] for c in CUTS)
print('main video', round(DUR,2))

for clip,ss,dur,zoom,stretch in CUTS:
    assert ss + dur/stretch <= 5.02, f'cut overrun {clip} {ss} {dur}'

# ---- extract frames per cut ----
n_all = 0
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
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
        '-vf',','.join(vf),'-qscale:v','3','-vframes',str(int(round(dur*FPS))),
        f'{cd}/%05d.jpg'], check=True, capture_output=True)
    frames = sorted(glob.glob(f'{cd}/*.jpg'))[:int(round(dur*FPS))]
    for fr in frames:
        n_all += 1
        os.rename(fr, f'{AF}/{n_all:05d}.jpg')
    print(f'cut {i} {clip} {len(frames)}fr', flush=True)
N = n_all
print('ALLFRAMES', N)

# ---- ambience audio per cut ----
alist = []
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    seg = f'{W}/a{i}.wav'
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
SCRIPT = ("Every time you stop at a red light... the road is reading your car. "
 "See those thin black lines cut into the asphalt? That's not a crack repair. It's an antenna. "
 "Buried inches under your tires sits a giant coil of wire — pulsing an invisible magnetic field, "
 "thousands of times every second. When two tons of steel rolls on top... the field bends. The pulse shifts. "
 "And a box on the corner feels it instantly. Your car just got counted. No camera ever saw you. "
 "The light turns green... because the street itself felt you arrive.")
words = [w for w in SCRIPT.replace('—',' ').split() if w.strip()]
weights = [len(w)+1.2 for w in words]
total_w = sum(weights)
T0c, T1c = 0.30+0.12, VODUR-0.15+0.12
times = []
acc = 0.0
for w, wt in zip(words, weights):
    st = T0c + (T1c-T0c)*acc/total_w
    acc += wt
    en = T0c + (T1c-T0c)*acc/total_w
    times.append((w, st, en))

FD = '/home/user/explainer-pipeline/assets/fonts'
def pick(*names, size=54):
    for n in names:
        p = f'{FD}/{n}'
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
F_CAP  = pick('Inter-SemiBold.ttf', size=56)
F_CAPB = pick('Montserrat-Black.ttf', size=58)
F_MONO = pick('JetBrainsMono-Bold.ttf','Inter-SemiBold.ttf', size=30)

LABELS = [
 ('INDUCTIVE LOOP',   (255,191,64), 11.8, 19.0),
 ('FIELD: PULSING',   (80,220,255), 15.7, 19.0),
 ('VEHICLE DETECTED', (255,150,60), 19.5, 23.3),
 ('PULSE SHIFTED',    (255,80,80),  21.6, 23.3),
 ('CAR COUNTED',      (255,191,64), 23.7, 27.4),
 ('NO CAMERA NEEDED', (200,210,222),27.7, 29.3),
 ('SIGNAL: GREEN',    (90,230,120), 29.6, 33.6),
]

def chunk_of(idx):
    c = idx//3
    return words[c*3:(c+1)*3], c*3

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
        chunk, base = chunk_of(wi)
        meas = [(dr.textlength(w+' ',font=(F_CAPB if (base+k)==wi else F_CAP))) for k,w in enumerate(chunk)]
        tw = sum(meas)
        x = (1080-tw)/2; y = 1700
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
            w = dr.textlength(text, font=F_MONO)
            x0,y0 = 48, ly
            dr.rounded_rectangle([x0,y0,x0+w+74,y0+52], 12, fill=(8,10,14,int(200*a)))
            dr.ellipse([x0+22,y0+19,x0+36,y0+33], fill=col+(int(255*a),))
            dr.text((x0+52,y0+10), text, font=F_MONO, fill=(240,244,248,int(255*a)))
            ly += 66
    im.save(f'{AF}/{fi:05d}.jpg', quality=90)
    if fi % 300 == 0: print('composited', fi, flush=True)
print('composite done')

# ---- mux main part ----
MAIN = f'{W}/main.mp4'
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]volume=0.32,afade=t=out:st={DUR-1.0:.2f}:d=1.0[amb];"
      f"[vo][amb]amix=inputs=2:duration=longest:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',f'{W}/amb.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.06:saturation=1.1,noise=alls=5:allf=t,unsharp=5:5:0.3:3:3:0',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','27','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{DUR:.2f}','-movflags','+faststart', MAIN], check=True)
print('main mux ok')

# ---- concat with CTA ender ----
subprocess.run([FF,'-nostdin','-y','-i',MAIN,'-i',CTA,
    '-filter_complex','[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]',
    '-map','[v]','-map','[a]',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','27','-pix_fmt','yuv420p',
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
print('=== FUNCY 59 DONE ===', OUT)
