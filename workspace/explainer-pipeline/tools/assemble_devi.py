# DEVI REEL 56 - beat-cut editorial assembler (10 clips -> ~15 cuts on music beats)
# Style: 90s Kodak film - warm grade, grain, halation feel. No captions (pure cinematic).
import subprocess, os, glob, json
import numpy as np

FF = glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
MUS = '/var/tmp/devimusic/677.mp3'   # Mixkit "Epical Drums 02" (free license)
W = '/var/tmp/devasm'
os.makedirs(W, exist_ok=True)
OUT = '/home/user/outputs/56-devi-reel.mp4'

LTX = '/var/tmp/devi/ltx/outputs'
H3 = '/var/tmp/devi/h3/outputs'
C = {
 'city':   f'{LTX}/ltx25_20261022_205311_seed101.mp4',
 'flag':   f'{LTX}/ltx25_20261022_205541_seed102.mp4',
 'shrine': f'{LTX}/ltx25_20261022_205810_seed103.mp4',
 'hand':   f'{LTX}/ltx25_20261022_210040_seed104.mp4',
 'bell':   f'{LTX}/ltx25_20261022_210309_seed105.mp4',
 'lion':   f'{H3}/h3_20261022_205447_seed201.mp4',
 'lioncu': f'{H3}/h3_20261022_205804_seed202.mp4',
 'devi':   f'{H3}/h3_20261022_210121_seed203.mp4',
 'eyes':   f'{H3}/h3_20261022_210437_seed204.mp4',
 'multi':  f'{H3}/h3_20261022_210753_seed205.mp4',
}

# ---- 1) beat detection on music (energy-flux peaks) ----
raw = subprocess.run([FF,'-nostdin','-i',MUS,'-ac','1','-ar','22050','-f','s16le','-t','60','-'],
                     capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768.0
hop = 512
n = len(x)//hop
rms = np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(n)])
flux = np.maximum(0, np.diff(rms))
t_per = hop/22050.0
thr = flux.mean() + 1.1*flux.std()
onsets = []
last = -10
for i, f in enumerate(flux):
    if f > thr and (i-last)*t_per > 0.55:
        onsets.append(i*t_per); last = i
onsets = [o for o in onsets if o > 0.1]
print('onsets found:', len(onsets), [round(o,2) for o in onsets[:20]])

# music starts video at first strong onset
T0 = onsets[0]
beats = [o - T0 for o in onsets]           # beat times relative to video t=0
beats = [b for b in beats if b >= 0]

# ---- 2) build cut list: order like the reference reel ----
order = [('city',0.4),('flag',0.7),('lioncu',0.7),('bell',0.7),('eyes',0.5),
         ('hand',0.8),('devi',0.3),('lion',0.7),('shrine',0.4),('multi',0.4),
         ('eyes',2.9),('devi',2.7),('lioncu',2.9),('flag',2.8),('multi',2.6)]
TARGET = 23.0
cuts = []   # (name, src_start, dur)
bi = 0
t = 0.0
for k,(name,ss) in enumerate(order):
    # duration = to next beat that is 1.1-2.2s away
    dur = 1.45
    while bi < len(beats)-1 and beats[bi] <= t+0.05: bi += 1
    # find next beat >= t+1.1
    cand = [b for b in beats if t+1.05 <= b <= t+2.3]
    if cand: dur = cand[0]-t
    if k == len(order)-1: dur = max(dur, 2.2)   # ender holds
    dur = min(dur, 4.9-ss)
    cuts.append((name, ss, dur)); t += dur
    if t >= TARGET and k >= 12: break
DUR = sum(d for _,_,d in cuts)
print('cuts:', len(cuts), 'total', round(DUR,2))
for c in cuts: print('  ', c[0], round(c[1],2), round(c[2],2))

# ---- 3) extract segments (1080x1920, 24fps, own ambience audio) ----
segs = []
for i,(name,ss,dur) in enumerate(cuts):
    seg = f'{W}/seg{i:02d}.mp4'
    subprocess.run([FF,'-nostdin','-y','-i',C[name],'-ss',f'{ss:.3f}','-t',f'{dur:.3f}',
        '-vf','scale=1080:1920:flags=lanczos,fps=24','-c:v','libx264','-preset','veryfast',
        '-threads','2','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',
        '-ar','44100','-ac','2', seg], check=True, capture_output=True)
    segs.append(seg)
    print('seg', i, name, 'ok')

with open(f'{W}/list.txt','w') as f:
    for s in segs: f.write(f"file '{s}'\n")

# ---- 4) final pass: concat + film grade + grain + vignette + music mix ----
grade = ("eq=contrast=1.07:saturation=1.22:brightness=0.012,"
         "colorbalance=rs=0.05:bs=-0.06:rm=0.03:bm=-0.04:rh=0.02:bh=-0.02,"
         "vignette=PI/4.3,noise=alls=6:allf=t+u,unsharp=5:5:0.25:3:3:0")
fc = (f"[0:v]{grade}[v];"
      f"[0:a]volume=0.30[amb];"
      f"[1:a]atrim=start={T0:.3f}:end={T0+DUR:.3f},asetpts=PTS-STARTPTS,"
      f"afade=t=in:st=0:d=0.15,afade=t=out:st={DUR-1.3:.3f}:d=1.3,volume=0.95[mus];"
      f"[amb][mus]amix=inputs=2:duration=first:normalize=0[a]")
subprocess.run([FF,'-nostdin','-y','-f','concat','-safe','0','-i',f'{W}/list.txt','-i',MUS,
    '-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast',
    '-threads','2','-crf','28','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',
    '-movflags','+faststart', OUT], check=True)
print('=== DEVI REEL DONE ===', OUT)
