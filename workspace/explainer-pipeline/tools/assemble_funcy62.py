# FUNCYOUS 62 - "Gas Pump Auto-Stop" (HYBRID + RETENTION ARMOR + MUSIC BED per VIRAL LAW)
import subprocess, os, glob, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/user/explainer-pipeline/tools')
from funcy_retention import draw_hook_card, draw_captions_pro, draw_callout, draw_subscribe_tap

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
W = '/var/tmp/f62'; os.makedirs(W, exist_ok=True)
AF = f'{W}/allfr'; os.makedirs(AF, exist_ok=True)
for f in glob.glob(f'{AF}/*.jpg'): os.remove(f)
OUT = '/home/user/outputs/62-gas-pump-funcyous.mp4'
VO = '/home/user/explainer-pipeline/assets/funcy62/vo62.mp3'
MUSIC = '/home/user/explainer-pipeline/assets/funcy62/music538.mp3'
CTA = '/home/user/explainer-pipeline/assets/funcy62/cta62.mp3'
CTA_T0 = 31.15
SRC = '/var/tmp/f62clips'
CODE_FR = '/var/tmp/f62code'
CODE2_FR = '/var/tmp/f62code2'

def clip_for(seed):
    g = sorted(glob.glob(f'{SRC}/ltx25_*_seed{seed}.mp4'))
    assert g, f'missing clip seed {seed}'
    return g[0]
CL = {'f1':clip_for(661),'f2':clip_for(662)}
FPS = 30
VOSPEED = 1.18
VODUR = 36.41/VOSPEED          # 30.86

CUTS = [
 ('f1', 0.00, 5.40, 1.00, 1.08),   # hook: nozzle POV push-in
 ('f2', 0.00, 4.20, 1.00, 1.0),    # macro: tiny hole intro
 ('f2', 1.00, 3.90, 1.28, 1.0),    # ZOOM: air sneaks in
 ('CODE',0.0, 10.50, 1.00, 1.0),   # X-ray venturi mechanism -> CLICK
 ('CODE2',0.0, 3.70, 1.00, 1.0),   # patent stamp + world pumps
 ('f1', 0.00, 7.80, 1.00, 1.60),   # ender slow-mo = opener -> LOOP + CTA room
]
DUR = sum(c[2] for c in CUTS)
print('main video', round(DUR,2))
for clip,ss,dur,zoom,stretch in CUTS:
    if clip!='CODE': assert ss + dur/stretch <= 5.02, f'overrun {clip}'

n_all = 0
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    nf = int(round(dur*FPS))
    if clip in ('CODE','CODE2'):
        srcdir = CODE_FR if clip=='CODE' else CODE2_FR
        frames = sorted(glob.glob(f'{srcdir}/f*.jpg'))[:nf]
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
    assert len(frames)>=nf-6, f'cut {i}: {len(frames)} != {nf}'
    while len(frames)<nf: frames.append(frames[-1])   # pad w/ last frame
    for fr in frames:
        n_all += 1
        if os.path.abspath(fr)!=f'{AF}/{n_all:05d}.jpg':
            Image.open(fr).save(f'{AF}/{n_all:05d}.jpg',quality=92)
    print(f'cut {i} {clip} {len(frames)}fr', flush=True)
N = n_all
print('ALLFRAMES', N)

# ---- ambience (clip audio under everything) ----
alist = []
for i,(clip, ss, dur, zoom, stretch) in enumerate(CUTS):
    seg = f'{W}/a{i}.wav'
    if clip in ('CODE','CODE2'):
        subprocess.run([FF,'-nostdin','-y','-stream_loop','3','-i',CL['f1'],'-vn',
            '-af',f'atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume=0.7','-ar','44100','-ac','2',seg],
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

# ---- SFX track (whooshes at cuts + CLICK at snap + end click) ----
import wave, struct, math
SR=44100
def rd(p):
    w=wave.open(p,'rb');n=w.getnframes();d=w.readframes(n);w.close()
    s=struct.unpack(f'<{n*2}h',d)
    return [(s[i*2]/32768,s[i*2+1]/32768) for i in range(n)]
TN=int(DUR*SR); mix=[[0.0,0.0] for _ in range(TN)]
def place(p,at,g=1.0):
    s=rd(p); st=int(at*SR)
    for i,(l,r) in enumerate(s):
        j=st+i
        if j>=TN: break
        mix[j][0]+=l*g; mix[j][1]+=r*g
for ct in (5.4, 9.6, 13.5, 24.0, 27.7):
    place('/var/tmp/sfx62_whoosh.wav', ct-0.25, 0.55)
place('/var/tmp/sfx62_click.wav', 13.5+7.6, 1.0)     # mechanism CLICK (t=21.4)
place('/var/tmp/sfx62_click.wav', 30.35, 0.75)
place('/var/tmp/sfx62_click.wav', 24.55, 0.5)     # 1940s stamp slam     # ender click ("that's physics")
w=wave.open(f'{W}/sfx.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
w.writeframes(b''.join(struct.pack('<hh',int(max(-1,min(1,l))*32767),int(max(-1,min(1,r))*32767)) for l,r in mix));w.close()
print('sfx ok')

# ---- captions timing ----
SCRIPT = ("The gas pump stops itself at the exact perfect moment. No sensor. No chip. "
 "Nothing electronic at all. Look inside the nozzle — there's a tiny hole, right at the tip. "
 "While fuel flows, air sneaks through that hole and keeps a vacuum line open. But the moment "
 "rising fuel covers it — the airflow dies. Vacuum builds behind a rubber diaphragm... it trips "
 "a spring — CLICK. The handle shuts itself down. This trick was invented in the nineteen forties — "
 "and it still guards every pump on Earth. That click? That's not a computer. That's physics.")
words = [w0 for w0 in SCRIPT.replace('—',' ').split() if w0.strip()]
weights = [len(w0)+1.2 for w0 in words]
total_w = sum(weights)
T0c, T1c = 0.30+0.12, VODUR-0.15+0.12
times = []; acc = 0.0
for w0, wt in zip(words, weights):
    st = T0c + (T1c-T0c)*acc/total_w
    acc += wt
    en = T0c + (T1c-T0c)*acc/total_w
    times.append((w0, st, en))

# ---- CTA caption words (phrase-level timing, trim0.28/atempo1.08 mapped) ----
cta_phr = [("One hidden machine,", 0.042, 1.325), ("every day...", 1.810, 2.296), ("subscribe for tomorrow's.", 2.883, 4.037)]
for ph, ps, pe in cta_phr:
    pw = ph.split(); wts=[len(x)+1.2 for x in pw]; tot=sum(wts); acc=0.0
    for x, wt in zip(pw, wts):
        st = CTA_T0+ps+(pe-ps)*acc/tot; acc+=wt; en = CTA_T0+ps+(pe-ps)*acc/tot
        words.append(x); times.append((x, st, en))

F_MONO = ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf',30)
LABELS = [
 ('NO ELECTRONICS',   (80,220,255), 3.4, 6.1),
 ('THE TINY HOLE',    (255,191,64), 7.0, 10.0),
 ('AIR INTAKE',       (80,220,255), 10.6, 13.4),
 ('VENTURI SYSTEM',   (255,191,64), 13.9, 16.9),
 ('FUEL RISING',      (255,150,60), 17.6, 19.9),
 ('VACUUM BUILDING',  (255,80,80),  19.6, 21.5),
 ('SPRING: TRIPPED',  (255,191,64), 21.5, 23.6),
 ('FLOW: STOPPED',    (90,230,120), 23.6, 25.8),
 ('EST. 1940s',       (255,191,64), 26.5, 29.4),
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
    draw_callout(im, tt, 6.1, 9.3, 540, 700, 170, 'THE TINY HOLE', side='right')
    draw_callout(im, tt, 10.2, 13.0, 540, 660, 150, 'AIR GOES IN', side='left')
    # subscribe tap mid-video high-retention beat
    draw_subscribe_tap(im, tt, 19.8)
    draw_subscribe_tap(im, tt, 32.9)
    draw_captions_pro(im, tt, times, words)
    draw_hook_card(im, tt, 'THE GAS PUMP', 'HAS NO BRAIN')
    im.save(f'{AF}/{fi:05d}.jpg', quality=90)
    if fi % 300 == 0: print('composited', fi, flush=True)
print('composite done')

# ---- mux: VO + ambience + MUSIC BED (new law) + SFX ----
fc = (f"[1:a]atempo={VOSPEED},adelay=120|120,volume=1.0[vo];"
      f"[2:a]atrim=0:{DUR:.2f},volume=0.20,afade=t=in:st=0:d=0.6,afade=t=out:st={DUR-1.4:.2f}:d=1.4[mus];"
      f"[3:a]volume=0.9[sfx];"
      f"[4:a]atrim=0.28:4.72,asetpts=PTS-STARTPTS,atempo=1.08,adelay={int(CTA_T0*1000)}|{int(CTA_T0*1000)},volume=1.0[cta];"
      f"[vo][mus][sfx][cta]amix=inputs=4:duration=longest:normalize=0,alimiter=limit=0.9[a]")
subprocess.run([FF,'-nostdin','-y','-framerate',str(FPS),'-i',f'{AF}/%05d.jpg',
    '-i',VO,'-i',MUSIC,'-i',f'{W}/sfx.wav','-i',CTA,'-filter_complex',fc,
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
print('=== FUNCY 62 DONE ===', OUT)
