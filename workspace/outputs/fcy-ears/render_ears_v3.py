import os,glob,sys,math,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import cv2,numpy as np
root=Path(os.environ.get('EAR_INPUT','/kaggle/input'))
if not (root/'ear_cutaway.png').exists():
 matches=glob.glob(str(root/'**/ear_cutaway.png'),recursive=True);assert len(matches)==1,matches;root=Path(matches[0]).parent
out=Path(os.environ.get('EAR_OUTPUT','/kaggle/working'));out.mkdir(parents=True,exist_ok=True)
W,H=768,1366;FPS=30;D=35.4
feather=Image.new('L',(W,890));fd=ImageDraw.Draw(feather)
for y in range(890):
 a=round(255*min(1,y/90,(889-y)/90));fd.line((0,y,W,y),fill=max(0,a))
font=ImageFont.truetype(str(root/'Inter-Black.ttf'),43);small=ImageFont.truetype(str(root/'Inter-Bold.ttf'),27);head=ImageFont.truetype(str(root/'Inter-Black.ttf'),43)
source=ImageOps.fit(Image.open(root/'ear_cutaway.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
# Build true spatial deformation of a small membrane region, while retaining the AI image as background.
arr=np.array(source); xx,yy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32));weight=np.exp(-(((xx-394)/74)**2+((yy-704)/100)**2)*2.0).astype('float32');variants=[]
for j in range(13):
 mx=xx-weight*(j*1.5);v=cv2.remap(arr,mx,yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE);variants.append(Image.fromarray(v))
del xx,yy,weight,arr
# Matched detail shots, with actual local image deformation rather than a still-only zoom.
macro=ImageOps.fit(Image.open(root/'eardrum_macro.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
tube=ImageOps.fit(Image.open(root/'tube_macro.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
xx,yy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32));ma=np.array(macro)
w=np.exp(-(((xx-350)/130)**2+((yy-740)/205)**2)*1.6).astype('float32');macro_variants=[]
for j in range(25):macro_variants.append(Image.fromarray(cv2.remap(ma,xx-w*(j*1.75),yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)))
ta=np.array(tube);line=330+(yy-570)*.55;dist=xx-line;active=np.exp(-((dist/100)**2))*np.exp(-(((yy-760)/320)**4));tube_variants=[]
for j in range(25):tube_variants.append(Image.fromarray(cv2.remap(ta,xx-np.sign(dist)*active*(j*1.4),yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)))
del xx,yy,ma,ta,w,line,dist,active
words=json.loads((root/'words.json').read_text());groups=[];g=[]
for w in words:
 g.append(w)
 if len(g)>=3 or w['word'].strip().endswith(('.',',','?','!')):groups.append(g);g=[]
if g:groups.append(g)
def clamp(x):return max(0,min(1,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def image_frames(name):
 cap=cv2.VideoCapture(str(root/name));v=[]
 while True:
  ok,fr=cap.read()
  if not ok:break
  v.append(Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)))
 cap.release();assert v,name;return v
A=image_frames('hook.mp4'); B=image_frames('relief.mp4')
def fromclip(clip,t):
 im=clip[min(len(clip)-1,max(0,int(t*24)))];return ImageOps.fit(im,(W,H),Image.Resampling.LANCZOS)
def caption(im,t):
 for g in groups:
  if g[0]['start']+.12<=t<g[-1]['end']+.20:
   d=ImageDraw.Draw(im);text=' '.join(w['word'].strip().upper() for w in g);f=font
   wid=d.textlength(text,font=f)
   if wid>690:f=ImageFont.truetype(str(root/'Inter-Black.ttf'),int(43*690/wid));wid=d.textlength(text,font=f)
   x=(W-wid)/2;y=1120;d.rounded_rectangle((int(x-13),y-5,int(x+wid+13),y+58),radius=10,fill=(3,13,21))
   for w in g:
    s=w['word'].strip().upper();col=(255,213,95) if w['start']+.12<=t<w['end']+.12 else (255,255,255)
    d.text((int(x),y),s,font=f,fill=col,stroke_width=1,stroke_fill=(0,0,0));x+=d.textlength(s+' ',font=f)
   break
 return im
def arrow(d,x,y,tx,ty,color,width=5):
 d.line((x,y,tx,ty),fill=color,width=width);ang=math.atan2(ty-y,tx-x);r=13
 d.polygon([(tx,ty),(tx-r*math.cos(ang-.55),ty-r*math.sin(ang-.55)),(tx-r*math.cos(ang+.55),ty-r*math.sin(ang+.55))],fill=color)
def label(d,text,x,y):
 box=d.textbbox((0,0),text,font=small);w=box[2]-box[0];d.rounded_rectangle((x-9,y-4,x+w+12,y+34),radius=8,fill=(4,17,24,220),outline=(99,153,159,120),width=1);d.text((x,y),text,font=small,fill=(222,246,246,255))
def frame(t):
 if t<5.0:
  im=fromclip(A,t);d=ImageDraw.Draw(im);d.rounded_rectangle((85,66,683,137),radius=15,fill=(3,16,26));d.text((112,77),'WHY DO EARS POP?',font=head,fill=(255,213,87));return caption(im,t)
 # 2.5D anatomical illustration; geometry and tube are simplified, not a validated 3D model.
 if 22.65<=t<24.35:
  im=fromclip(B,min(t-22.65,1.6));return caption(im,t)
 if t>=31.4:
  im=fromclip(B,min(4.85,max(0,t-31.4)));return caption(im,t)
 push=smooth((t-10.2)/2.7)*(1-smooth((t-28.8)/2.1));ind=min(12,max(0,int(push*12)))
 is_macro=(10.2<=t<16.0 or 28.8<=t<31.4)
 is_tube=(20.0<=t<22.65 or 24.35<=t<28.8)
 if is_macro: im=macro_variants[min(24,int(push*24))].copy().convert('RGBA')
 elif is_tube:
  tube_open=smooth((t-25.2)/1.5) if t>=24.35 else 0
  im=tube_variants[min(24,int(24*tube_open))].copy().convert('RGBA')
 else: im=variants[ind].copy().convert('RGBA')
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 d.rounded_rectangle((138,55,630,116),radius=12,fill=(4,15,25,208),outline=(128,179,195,90),width=1)
 title='AIR PRESSURE CHANGES' if t<10.5 else ('EARDRUM MOVES INWARD' if t<16.0 else ('A TINY PASSAGE' if t<22.65 else ('AIR CAN MOVE IN' if t<29.0 else 'PRESSURE BALANCES')))
 b=d.textbbox((0,0),title,font=small);d.text(((W-(b[2]-b[0]))/2,72),title,font=small,fill=(255,221,139,255))
 # A moving trace marks the actual eardrum surface, not the ossicles or the ear canal.
 if is_macro:
  contour=[(266,550),(245,600),(242,665),(251,733),(275,804),(315,875),(374,937),(445,966)]
  strength=round(110+75*(.5+.5*math.sin(t*3.2)))
  d.line(contour,fill=(255,194,100,55),width=16,joint='curve')
  d.line(contour,fill=(255,223,155,strength),width=5,joint='curve')
  if 10.35<t<15.9: label(d,'EARDRUM',437,900)
 if 6.0<=t<16.0:
  for k in range(4):
   phase=(t*.22+k*.24)%1.;x=80+phase*230;y=590+k*43
   d.ellipse((x-15,y-15,x+15,y+15),fill=(103,205,244,35));d.ellipse((x-5,y-5,x+5,y+5),fill=(155,228,255,210))
  if t>=10.3:
   for k in range(3):
    x=195+(t*27+k*53)%120;y=620+k*60;arrow(d,x,y,x+45,y,(140,224,255,230),5)
   label(d,'HIGHER CABIN PRESSURE',25,495)
 if 16.0<=t<28.8:
  pts=([(625,1090),(585,1010),(535,925),(485,845),(440,770),(395,690),(340,580)] if is_tube else [(638,1090),(605,1030),(575,971),(545,909),(519,850),(491,803),(468,774)])
  # At rest mark the tube's boundary rather than depicting a glowing open airway.
  if t<24.35:
   d.line(pts,fill=(255,204,123,65),width=18,joint='curve')
   d.line(pts,fill=(255,221,160,170),width=4,joint='curve')
   label(d,'EUSTACHIAN TUBE',225,995)
  else:
   progress=smooth((t-25.2)/1.4)
   d.line(pts,fill=(31,187,205,45),width=34,joint='curve')
   d.line(pts,fill=(108,234,235,210),width=int(3+12*progress),joint='curve')
   label(d,'AIR TO MIDDLE EAR',225,995)
   if t>=26.65:
    for k in range(4):
     u=((t-26.65)*.35-k*.18)%1.;seg=u*(len(pts)-1);i=min(len(pts)-2,int(seg));a=seg-i;x=pts[i][0]*(1-a)+pts[i+1][0]*a;y=pts[i][1]*(1-a)+pts[i+1][1]*a
     d.ellipse((x-16,y-16,x+16,y+16),fill=(142,238,243,60));d.ellipse((x-7,y-7,x+7,y+7),fill=(196,255,252,250))
    # The arrow tracks up the tube, from the nose end toward the middle ear.
    phase=((t-26.65)*.4)%1.;seg=phase*(len(pts)-1);i=min(len(pts)-2,int(seg));a=seg-i;x=pts[i][0]*(1-a)+pts[i+1][0]*a;y=pts[i][1]*(1-a)+pts[i+1][1]*a
    arrow(d,x+18,y+29,x-7,y-18,(194,255,255,220),5)
 label(d,'SIMPLIFIED CONCEPT',22,1285)
 im=Image.alpha_composite(im,layer).convert('RGB')
 # Camera reframing stays on the anatomy and follows the mechanism, not the subtitles.
 if is_macro or is_tube:
  x0,y0,x1,y1=0,180,W,1070;roi=im.crop((x0,y0,x1,y1))
  phase=(t-10.2)/5.8 if is_macro and t<16 else (t-20)/2.65 if is_tube and t<22.65 else (t-24.35)/4.45 if is_tube else (t-28.8)/2.6
  z=1.035+0.075*smooth(phase);cw=int(W/z);ch=int((y1-y0)/z)
  cx=355 if is_macro else 450;cy=540 if is_macro else 580
  left=max(0,min(W-cw,int(cx-cw/2)));top=max(0,min(y1-y0-ch,int(cy-ch/2)))
  roi=roi.crop((left,top,left+cw,top+ch)).resize((W,y1-y0),Image.Resampling.LANCZOS);im.paste(roi,(0,y0),feather)
 return caption(im,t)
if os.environ.get('EAR_PROBE'):
 ts=[0.5,5.5,8.5,11.8,15.5,17.5,21,24.6,26,29.8,32.8,34.5];sheet=Image.new('RGB',(4*192,3*365))
 for i,t in enumerate(ts):sheet.paste(frame(t).resize((192,341)),((i%4)*192,(i//4)*365+24));ImageDraw.Draw(sheet).text(((i%4)*192,(i//4)*365),str(t),fill='white')
 sheet.save(out/'probe.jpg');print('PROBE COMPLETE');sys.exit(0)
ff='ffmpeg';silent=out/'Ears_silent_1080p.mp4'
cmd=[ff,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-vf','scale=1080:1920:flags=lanczos','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(silent)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(D*FPS)):
 p.stdin.write(frame(i/FPS).tobytes())
 if i%150==0:print('rendered',i,'/',round(D*FPS),flush=True)
p.stdin.close();assert p.wait()==0
final=out/'Ears_Pop_Full_Story_1080p_REVIEW.mp4'
subprocess.run([ff,'-y','-v','error','-i',str(silent),'-i',str(root/'audio_master.wav'),'-t',str(D),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)],check=True)
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
print('FINAL DECODE PASSED',flush=True)
