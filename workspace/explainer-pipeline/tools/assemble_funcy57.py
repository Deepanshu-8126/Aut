# FUNCYOUS 57 - "Radioactive Guardian" smoke detector short
# 8 cuts (5 base + zoom variants) + English wordpop + Zack-style label chips + VO 1.18x
import subprocess, os, glob, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/f57'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
OUT = '/home/user/outputs/57-smoke-detector-funcyous.mp4'
VO = '/home/user/explainer-pipeline/assets/funcy57/vo.mp3'
SRC = '/var/tmp/funcy/out/outputs'
CL = {
 'f1': f'{SRC}/ltx25_20261023_021444_seed301.mp4',
 'f2': f'{SRC}/ltx25_20261023_021732_seed302.mp4',
 'f3': f'{SRC}/ltx25_20261023_022020_seed303.mp4',
 'f4': f'{SRC}/ltx25_20261023_022308_seed304.mp4',
 'f5': f'{SRC}/ltx25_20261023_022557_seed305.mp4',
}
FPS = 30
VOSPEED = 1.18
VODUR = 38.62/VOSPEED          # 32.73

# cuts: (clip, src_start, dur, zoom)  zoom=1.0 normal, >1 = static push crop
CUTS = [
 ('f1', 0.00, 6.20, 1.00, 1.23),   # hook (stretched 1.23x)
 ('f2', 0.00, 4.20, 1.00, 1.0),    # cutaway rotate
 ('f3', 0.00, 4.10, 1.00, 1.0),    # chamber wide
 ('f3', 1.00, 4.00, 1.30, 1.0),    # chamber ZOOM - current
 ('f4', 0.00, 3.80, 1.00, 1.0),    # smoke enters
 ('f4', 1.90, 3.10, 1.32, 1.0),    # smoke ZOOM - current drops
 ('f5', 0.00, 4.70, 1.00, 1.0),    # alarm
 ('f1', 1.70, 3.30, 1.12, 1.0),    # ender loop
]
DUR = sum(c[2] for c in CUTS)
print('total video', round(DUR,2))

# ---- extract frames per cut ----
n_all = 0
cut_bounds = []   # (t_start, t_end) per cut
t = 0.0
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
    cut_bounds.append((t, t+dur)); t += dur
    print(f'cut {i} {clip} {len(frames)}fr')
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

# ---- captions: char-weighted wordpop ----
SCRIPT = ("Right now, there's radioactive metal in your ceiling... and it's saving your life. "
 "Inside every smoke detector sits a tiny chamber, holding Americium two-forty-one — firing invisible particles, "
 "twenty-four hours a day. Those particles electrify the air — creating an invisible electric current between two metal plates. "
 "But when smoke sneaks in... it blocks the particles. The current drops. And that's what triggers the alarm. "
 "Not the smoke. The silence of a broken circuit. A radioactive guardian. Watching. Every second.")
words = SCRIPT.replace('—',' ').split()
weights = [len(w)+1.2 for w in words]
total_w = sum(weights)
T0c, T1c = 0.30, VODUR-0.15
times = []
acc = 0.0
for w, wt in zip(words, weights):
    st = T0c + (T1c-T0c)*acc/total_w
    acc += wt
    en = T0c + (T1c-T0c)*acc/total_w
    times.append((w.strip('—'), st, en))

FD = '/home/user/explainer-pipeline/assets/fonts'
def pick(*names, size=54):
    for n in names:
        p = f'{FD}/{n}'
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
F_CAP  = pick('Inter-SemiBold.ttf','Montserrat-Black.ttf', size=56)
F_CAPB = pick('Montserrat-Black.ttf','Inter-SemiBold.ttf', size=58)
F_MONO = pick('JetBrainsMono-Regular.ttf','JetBrainsMono-Bold.ttf','Inter-SemiBold.ttf', size=30)

# label chips: (text, color, t_start, t_end)
LABELS = [
 ('AMERICIUM-241',        (255,191,64),  10.5, 18.5),
 ('CURRENT: NORMAL',      (80,220,255),  14.6, 18.5),
 ('SMOKE DETECTED',       (255,120,70),  18.6, 25.3),
 ('CURRENT: DROPPED',     (255,80,80),   22.3, 25.3),
 ('ALARM TRIGGERED',      (255,60,60),   25.4, 30.0),
]

def chunk_of(idx):
    c = idx//3
    return words[c*3:(c+1)*3], c*3

for fi in range(1, N+1):
    tt = (fi-0.5)/FPS
    im = Image.open(f'{AF}/{fi:05d}.jpg').convert('RGB')
    dr = ImageDraw.Draw(im, 'RGBA')
    # bottom caption gradient
    gr = Image.new('L',(1,420),0)
    for y in range(420): gr.putpixel((0,y), int(170*(y/420)**1.5))
    grad = gr.resize((1080,420))
    black = Image.new('RGBA',(1080,420),(0,0,0,255)); black.putalpha(grad)
    im.paste(Image.alpha_composite(im.crop((0,1500,1080,1920)).convert('RGBA'), black).convert('RGB'),(0,1500))
    dr = ImageDraw.Draw(im,'RGBA')
    # wordpop (3-word chunks)
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
    # label chips (top-left stack)
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
    if fi % 300 == 0: print('composited', fi)
print('composite done')

# ---- mux: frames + (VO 1.18x + amb 0.32) ----
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]volume=0.32,afade=t=out:st={DUR-1.0:.2f}:d=1.0[amb];"
      f"[vo][amb]amix=inputs=2:duration=longest:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',f'{W}/amb.wav','-filter_complex',fc,
    '-map','0:v','-map','[a]',
    '-vf','eq=contrast=1.06:saturation=1.1,noise=alls=5:allf=t,unsharp=5:5:0.3:3:3:0',
    '-c:v','libx264','-preset','veryfast','-threads','2','-crf','27','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-t',f'{DUR:.2f}','-movflags','+faststart', OUT], check=True)

# ---- srt ----
srt = []
chunks = [words[i:i+3] for i in range(0,len(words),3)]
ci = 0
with open(OUT.replace('.mp4','.srt'),'w') as f:
    for c in range(len(chunks)):
        ws = times[c*3:(c+1)*3]
        if not ws: break
        st, en = ws[0][1], ws[-1][2]
        def fmt(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x%1*1000):03d}"
        f.write(f"{c+1}\n{fmt(st)} --> {fmt(en)}\n{' '.join(chunks[c])}\n\n")
print('=== FUNCY 57 DONE ===', OUT)
