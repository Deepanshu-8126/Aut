from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math, os, sys, subprocess, re, glob, shutil
from pathlib import Path

BASE=Path(os.environ.get('FINGER_INPUT','/kaggle/input'))
if not (BASE/'finger.png').exists():
    matches=glob.glob(str(BASE/'**/finger.png'),recursive=True)
    assert len(matches)==1, matches
    BASE=Path(matches[0]).parent
OUT=Path(os.environ.get('FINGER_OUTPUT','/kaggle/working')); OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1920; FPS=30; D=8.08
photo=ImageOps.fit(Image.open(BASE/'finger.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
black=ImageFont.truetype(str(BASE/'Inter-Black.ttf'),58)
head=ImageFont.truetype(str(BASE/'Inter-Black.ttf'),57)
med=ImageFont.truetype(str(BASE/'Inter-Bold.ttf'),32)
small=ImageFont.truetype(str(BASE/'Inter-Bold.ttf'),24)
# Machine-aligned captions from original master; written manually from source SRT timing.
groups=[(5.78,6.58,'YOUR NERVOUS SYSTEM'),(6.58,7.74,'SIGNALS TINY BLOOD'),(7.74,8.44,'VESSELS IN YOUR'),(8.44,9.56,'FINGERTIPS TO NARROW.'),(10.16,11.00,'THAT REDUCES THE'),(11.00,12.44,'VOLUME UNDERNEATH, PULLING'),(12.44,13.18,'THE SKIN INTO'),(13.18,13.70,'FOLDS.')]
def sm(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def centered(d,text,y,font,fill,stroke=0):
 bb=d.textbbox((0,0),text,font=font,stroke_width=stroke); x=(W-(bb[2]-bb[0]))/2
 d.text((int(x),y),text,font=font,fill=fill,stroke_width=stroke,stroke_fill=(4,12,19))
def glowline(draw, pts, col, width):
 draw.line(pts,fill=(*col,45),width=width+24,joint='curve');draw.line(pts,fill=(*col,100),width=width+9,joint='curve');draw.line(pts,fill=(*col,235),width=width,joint='curve')
def frame(t):
 # Stable real-looking fingertip image; lighting and labels sit above it.
 im=photo.copy().convert('RGBA')
 over=Image.new('RGBA',(W,H));d=ImageDraw.Draw(over)
 d.rounded_rectangle((158,94,922,191),radius=25,fill=(4,14,22,190),outline=(145,189,198,100),width=2)
 title='NERVE SIGNAL' if t<2.68 else ('VESSELS NARROW' if t<5.30 else 'LESS VOLUME BELOW')
 centered(d,title,110,head,(250,215,92,255),2)
 # Simplified graphic signal, deliberately stylized rather than claiming to trace real nerves.
 if t<3.4:
  pts=[]
  for i in range(81):
   u=i/80;pts.append((int(232+245*u+28*math.sin(u*5)),int(320+790*u)))
  glowline(d,pts,(84,222,225),4)
  for k in range(5):
   u=(t*.32-k*.16)%1.; x=232+245*u+28*math.sin(u*5);y=320+790*u
   r=13+3*math.sin(t*8-k);d.ellipse((x-r*2,y-r*2,x+r*2,y+r*2),fill=(68,227,225,55));d.ellipse((x-r,y-r,x+r,y+r),fill=(180,255,245,255))
  d.rounded_rectangle((70,1360,375,1415),radius=13,fill=(5,19,28,205))
  d.text((87,1372),'SIGNAL • CONCEPT',font=small,fill=(194,236,232,255))
 if t>=2.68:
  alpha=round(255*sm((t-2.68)/.35))
  panel=Image.new('RGBA',(W,H));p=ImageDraw.Draw(panel)
  # Detailed, deliberately schematic magnified cross-section of a vessel.
  px,py=710,1032;R=280
  p.line([(510,790),(px-R+35,py-150)],fill=(131,226,231,200),width=4)
  p.ellipse((px-R-15,py-R-15,px+R+15,py+R+15),fill=(2,13,23,205),outline=(144,222,226,230),width=6)
  # Soft radial concentric gradients create tissue and vessel-wall depth.
  for rr in range(R-7,8,-4):
   q=rr/R
   if q>.77: color=(int(90+80*(1-q)),int(47+31*(1-q)),int(59+25*(1-q)),255)
   else: color=(int(145+55*(1-q)),int(63+23*(1-q)),int(73+20*(1-q)),255)
   p.ellipse((px-rr,py-rr,px+rr,py+rr),fill=color)
  contraction=sm((t-3.2)/1.55);rad=170-92*contraction
  for rr in range(int(rad)+24,0,-3):
   q=rr/(rad+24);col=(int(115+92*q),int(27+45*q),int(37+48*q),255)
   p.ellipse((px-rr,py-rr,px+rr,py+rr),fill=col)
  p.ellipse((px-rad*.72,py-rad*.66,px+rad*.72,py+rad*.66),fill=(88,16,32,255))
  for k in range(5):
   ang=k*2*math.pi/5+t*.32;rx=rad*.42*math.cos(ang);ry=rad*.36*math.sin(ang)
   p.ellipse((px+rx-10,py+ry-7,px+rx+10,py+ry+7),fill=(232,92,100,215))
  p.arc((px-R+18,py-R+18,px+R-18,py+R-18),195,315,fill=(255,211,200,160),width=6)
  # Direction arrows emphasize the change in diameter.
  if contraction>.05:
   for s in [-1,1]:
    ax=px+s*(rad+84);bx=px+s*(rad+30)
    p.line((ax,py,bx,py),fill=(244,246,211,240),width=7)
    p.polygon([(bx,py),(bx+s*19,py-12),(bx+s*19,py+12)],fill=(244,246,211,240))
  p.rounded_rectangle((478,1318,944,1372),radius=15,fill=(3,14,23,230))
  lab='BLOOD VESSEL' if t<5.5 else 'VESSEL NARROWS'
  bb=p.textbbox((0,0),lab,font=med);p.text((710-(bb[2]-bb[0])/2,1326),lab,font=med,fill=(229,249,245,255))
  if alpha<255: panel.putalpha(panel.getchannel('A').point(lambda a: a*alpha//255))
  over=Image.alpha_composite(over,panel);d=ImageDraw.Draw(over)
 # Animated surface folds as a separate labelled schematic, not a literal anatomical scan.
 if t>=5.45:
  fold=sm((t-5.45)/1.45)
  d.rounded_rectangle((80,1435,1000,1533),radius=18,fill=(4,17,24,220),outline=(128,198,198,120),width=2)
  points=[]
  for x in range(115,624,3):
   envelope=math.sin(math.pi*(x-115)/509)**2
   y=1485+fold*13*math.sin((x-115)*math.pi/49)*envelope
   points.append((x,int(y)))
  d.line(points,fill=(255,197,161,255),width=11,joint='curve')
  d.text((665,1464),'SKIN FOLDS',font=med,fill=(250,216,106,255))
 # Consistent captions in the lower safe area.
 global_t=t+5.78
 for a,b,text in groups:
  if a<=global_t<b:
   bb=d.textbbox((0,0),text,font=black); width=bb[2]-bb[0]; f=black
   if width>930: f=ImageFont.truetype(str(BASE/'Inter-Black.ttf'),int(58*930/width));bb=d.textbbox((0,0),text,font=f);width=bb[2]-bb[0]
   x=(W-width)//2;y=1600
   d.rounded_rectangle((x-20,y-6,x+width+20,y+76),radius=12,fill=(5,15,24,230))
   d.text((x,y),text,font=f,fill=(250,250,246,255),stroke_width=1,stroke_fill=(0,0,0,255))
   break
 d.rounded_rectangle((38,1800,335,1846),radius=9,fill=(4,18,26,190))
 d.text((51,1807),'SIMPLIFIED AI CONCEPT',font=small,fill=(212,231,233,255))
 return Image.alpha_composite(im,over).convert('RGB')
if os.environ.get('PROBE'):
 sheet=Image.new('RGB',(4*270,480));
 for i,t in enumerate([.5,3.3,5.0,7.1]):sheet.paste(frame(t).resize((270,480)),(i*270,0))
 sheet.save(OUT/'probe.png');print('probe saved');sys.exit(0)
# Pipe full-resolution generated frames into H.264; no source audio is discarded in the final edit.
clip=OUT/'finger_coded_animation.mp4'
ff='ffmpeg'
cmd=[ff,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(clip)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(D*FPS)):
 p.stdin.write(frame(i/FPS).tobytes())
 if i%60==0: print('ANIMATION FRAME',i,flush=True)
p.stdin.close()
if p.wait()!=0:raise RuntimeError('animation encode failed')
# Existing master includes final voice, music, SFX and captions; replace ONLY 5.78–13.86 seconds.
final=OUT/'Fingers_Short_Coded_Animation_1080p_REVIEW.mp4'
filt='[0:v]trim=start=0:end=5.78,setpts=PTS-STARTPTS[a];[1:v]trim=duration=8.08,setpts=PTS-STARTPTS[b];[0:v]trim=start=13.86:end=25.6,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]'
subprocess.run([ff,'-y','-v','warning','-filter_complex_threads','1','-i',str(BASE/'prior.mp4'),'-i',str(clip),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-t','25.6','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json',str(final)],check=True)
print('COMPLETE: full decode passed',flush=True)
