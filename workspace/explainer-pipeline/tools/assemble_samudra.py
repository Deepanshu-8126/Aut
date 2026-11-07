# SAMUDRA MANTHAN 26s short assembler - factshorts hybrid (LTX-2.5 clips + VO + wordpop + CTA)
import os, sys, subprocess, math, random
sys.path.insert(0,'/var/tmp/pydeps')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

FF='/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
SRC='/var/tmp/sam/enh/outputs'
CL=['enh_ltx25_20261022_172135_seed101.mp4','enh_ltx25_20261022_172421_seed202.mp4','enh_ltx25_20261022_172708_seed303.mp4','enh_ltx25_20261022_172954_seed404.mp4']
ASM='/var/tmp/asm'; os.makedirs(ASM,exist_ok=True)
W,H,FPS=1080,1920,30
TIRO=lambda s: ImageFont.truetype('/var/tmp/fonts/tiro.ttf',s)
MONT=lambda s: ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/Montserrat-Black.ttf',s)
INT=lambda s: ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/Inter-SemiBold.ttf',s)
F_WP,F_WP_HI,F_TAG,F_PILL=TIRO(62),TIRO(72),INT(26),TIRO(40)
GOLD=(242,177,53); BLACK=(17,17,17); RED=(226,59,46)

# 1) stretch clips -> frames
for i,c in enumerate(CL):
    d=f'{ASM}/c{i}'; 
    if os.path.isdir(d) and len(os.listdir(d))>150: continue
    os.makedirs(d,exist_ok=True)
    subprocess.run([FF,'-nostdin','-y','-i',f'{SRC}/{c}','-vf',
      "setpts=1.102*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale=1080:1920:flags=lanczos",
      '-q:v','3',f'{d}/%04d.jpg','-loglevel','error'],check=True)
    print('stretched',c,len(os.listdir(d)),flush=True)
counts=[len(os.listdir(f'{ASM}/c{i}')) for i in range(4)]
print('counts',counts,flush=True)
CTA_N=110
N=sum(counts)+CTA_N
VO_LEN=25.61; VO_DELAY=0.12

# 2) word timing (char-weighted)
SEGS=["समुद्र मंथन। देव और असुर — एक ही रस्सी के दो छोर।",
"मंदराचल पर्वत बनी मथनी, और वासुकी नाग बनी रस्सी।",
"हज़ार साल के मंथन से पहले निकला हलाहल विष — इतना ज़हरीला कि सृष्टि काँप उठी।",
"और फिर निकला — अमृत कलश। कहते हैं, उसी एक कलश की चार बूँदों से... आज भी कुंभ लगता है।"]
tot=sum(len(s) for s in SEGS)
words=[]; t=VO_DELAY; seg_times=[]
for s in SEGS:
    dur=VO_LEN*len(s)/tot; st=t
    ws=[w for w in s.split() if w not in ('—',)]
    wtot=sum(len(w)+1 for w in ws)
    for w in ws:
        wd=dur*(len(w)+1)/wtot
        words.append((w,t,t+wd)); t+=wd
    seg_times.append((st,t))
print('seg_times',[(round(a,2),round(b,2)) for a,b in seg_times],flush=True)

# grouping: chunks of 3 words
chunks=[]; cur=[]
for w in words:
    cur.append(w)
    if len(cur)==3: chunks.append(cur); cur=[]
if cur: chunks.append(cur)

# 3) helpers
def pill_top(dr):
    txt='समुद्र मंथन'
    w=dr.textlength(txt,font=F_PILL)
    x0,y0=(W-w)/2-42,70
    dr.rounded_rectangle([x0,y0,x0+w+84,y0+78],39,fill=BLACK)
    dr.text(((W-w)/2,y0+12),txt,font=F_PILL,fill=(255,255,255))
def tag_ai(dr):
    txt='AI RECREATION'
    w=dr.textlength(txt,font=F_TAG)
    x0,y0=W-w-120,190
    dr.rounded_rectangle([x0,y0,x0+w+64,y0+52],26,fill=(17,17,17,220))
    dr.ellipse([x0+22,y0+19,x0+36,y0+33],fill=GOLD)
    dr.text((x0+46,y0+11),txt,font=F_TAG,fill=(255,255,255))
def wordpop(dr,tt):
    ch=None
    for c in chunks:
        if c[0][1]<=tt<c[-1][2]+0.12: ch=c; break
    if not ch: return
    ws=[]; tw=0
    for (w,a,b) in ch:
        act=a<=tt<b
        f=F_WP_HI if act else F_WP
        wl=dr.textlength(w,font=f); ws.append((w,f,wl,act,a)); tw+=wl+26
    x=(W-tw+26)/2; y=1560
    for (w,f,wl,act,a) in ws:
        fill=GOLD if act else (255,255,255)
        pop=max(0,1-(tt-a)*9) if act else 0
        yy=y-(8*pop)-(6 if act else 0)
        dr.text((x,yy),w,font=f,fill=fill,stroke_width=7,stroke_fill=(10,10,10))
        x+=wl+26
VIG=None
def post(im,fi):
    global VIG
    a=np.asarray(im,dtype=np.int16)
    rng=np.random.RandomState(fi)
    noise=rng.randint(-3,4,(H//4,W//4,1),dtype=np.int16)
    noise=np.repeat(np.repeat(noise,4,axis=0),4,axis=1)
    a=np.clip(a+noise,0,255).astype(np.uint8)
    im=Image.fromarray(a)
    if VIG is None:
        yy,xx=np.mgrid[0:H,0:W]
        d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
        VIG=np.clip(1-0.14*np.clip(d-0.55,0,1)**1.6,0,1)[...,None]
    a=(np.asarray(im)*VIG).astype(np.uint8)
    return Image.fromarray(a)

# 4) composite clip frames
OUT=f'{ASM}/fr'; os.makedirs(OUT,exist_ok=True)
gi=0
for ci in range(4):
    d=f'{ASM}/c{ci}'; fs=sorted(os.listdir(d))
    for k,fn in enumerate(fs):
        tt=gi/FPS
        im=Image.open(f'{d}/{fn}').convert('RGB')
        dr=ImageDraw.Draw(im,'RGBA')
        pill_top(dr); wordpop(dr,tt)  # tag_ai removed per user order 2026-10-22
        post(im,gi).save(f'{OUT}/{gi:05d}.jpg',quality=90)
        gi+=1
    print('composited clip',ci,flush=True)

# 5) CTA (dynamic, no static hold)
def dotgrid(dr):
    for yy in range(0,H,54):
        for xx in range(0,W,54):
            dr.ellipse([xx-2,yy-2,xx+2,yy+2],fill=(216,216,216))
for k in range(CTA_N):
    tt=gi/FPS; p=k/CTA_N
    im=Image.new('RGB',(W,H),(255,255,255))
    dr=ImageDraw.Draw(im,'RGBA')
    dotgrid(dr)
    s=1+0.35*math.exp(-4*p*3)*math.sin(12*p*3) if p<0.4 else 1.0
    s*= (0.2+0.8*min(1,p*5)) 
    txt1,txt2='FACT','SHORTS'
    f=MONT(int(92*s)) if s>0.05 else MONT(10)
    w1=dr.textlength(txt1,font=f); w2=dr.textlength(txt2,font=f)
    pw=max(w1+w2+60,10)+160
    x0,y0=(W-pw)/2,840
    dr.rounded_rectangle([x0,y0,x0+pw,y0+200],100,fill=BLACK)
    dr.text(((W-w1-w2-60)/2,y0+100-f.size*0.62),txt1,font=f,fill=(255,255,255))
    dr.text(((W-w1-w2-60)/2+w1+60,y0+100-f.size*0.62),txt2,font=f,fill=GOLD)
    if p>0.35:
        q=min(1,(p-0.35)/0.2)
        sub='SUBSCRIBE KARO — ROZ EK FACT'
        fs2=INT(34); w3=dr.textlength(sub,font=fs2)
        dr.text(((W-w3)/2,1120),sub,font=fs2,fill=(60,60,60,int(255*q)))
        dr.rectangle([(W-w3)/2,1180,(W-w3)/2+w3*q,1186],fill=GOLD)
    for di in range(3):
        pulse=1+0.3*math.sin(tt*6+di*1.1)
        r=int(7*pulse)
        cx=W/2-40+di*40
        dr.ellipse([cx-r,1760-r,cx+r,1760+r],fill=BLACK)
    # wordpop tail (VO ends inside CTA)
    wordpop(dr,tt)
    zoom=1+0.035*p
    im=im.resize((int(W*zoom),int(H*zoom)),Image.LANCZOS)
    L=( (im.width-W)//2,(im.height-H)//2 )
    im=im.crop((L[0],L[1],L[0]+W,L[1]+H))
    post(im,gi).save(f'{OUT}/{gi:05d}.jpg',quality=90)
    gi+=1
print('ALLFRAMES',gi,flush=True)

# 6) audio mix
DUR=gi/FPS
cmd=[FF,'-nostdin','-y']
for c in CL: cmd+=['-i',f'{SRC}/{c}']
cmd+=['-i','/home/user/explainer-pipeline/assets/samudra/vo.mp3']
fc=''.join(f'[{i}:a]atempo=0.9074[a{i}];' for i in range(4))
fc+='[a0][a1][a2][a3]concat=n=4:v=0:a=1,apad[bed];'
fc+=f'[bed]atrim=0:{DUR:.2f},volume=0.42,afade=t=out:st={DUR-1.2:.2f}:d=1.2[b];'
fc+=f'[4:a]adelay=120|120,apad,atrim=0:{DUR:.2f}[v];[b][v]amix=inputs=2:duration=first:dropout_transition=0,aresample=44100'
cmd+=['-filter_complex',fc,'-c:a','aac','-b:a','128k',f'{ASM}/mix.m4a','-loglevel','error']
subprocess.run(cmd,check=True); print('mix done',flush=True)

# 7) mux
subprocess.run([FF,'-nostdin','-y','-framerate','30','-i',f'{OUT}/%05d.jpg','-i',f'{ASM}/mix.m4a',
 '-vf','eq=contrast=1.05:saturation=1.12,unsharp=5:5:0.35:3:3:0',
 '-c:v','libx264','-preset','veryfast','-threads','2','-crf','27','-pix_fmt','yuv420p',
 '-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',
 '/home/user/outputs/50-samudra-manthan.mp4','-loglevel','error'],check=True)

# 8) srt
def ts(x):
    hh=int(x//3600);mm=int(x%3600//60);ss=int(x%60);ms=int((x-int(x))*1000)
    return f'{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}'
with open('/home/user/outputs/50-samudra-manthan.srt','w') as f:
    for i,((a,b),s) in enumerate(zip(seg_times,SEGS),1):
        f.write(f'{i}\n{ts(a)} --> {ts(min(b,DUR))}\n{s}\n\n')
print('=== SAMUDRA DONE ===',flush=True)
