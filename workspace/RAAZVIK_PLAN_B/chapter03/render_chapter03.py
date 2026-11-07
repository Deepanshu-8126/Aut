#!/usr/bin/env python3
"""RAAZVIK Chapter 3; contextual real evidence and conceptual motion; REVIEW."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,math,imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter03');C=Path('/home/user/RAAZVIK_PLAN_B/chapter01');O=P/'render_work';O.mkdir(exist_ok=True);A=C/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi';F=Path('/home/user/explainer-pipeline/assets/fonts');ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1280,720;N=510
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),42);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),31);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),21);latin=ImageFont.truetype(str(F/'Inter-Bold.ttf'),40)

def txt(d,xy,s,f,fill='#f5f4eb',stroke=1):d.text(xy,s,font=f,fill=fill,stroke_width=stroke,stroke_fill='#0a141a')
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def foot(d,s):
 bb=d.textbbox((0,0),s,font=small);d.rounded_rectangle((32,665,54+bb[2],703),radius=4,fill=(5,17,22,210));txt(d,(41,669),s,small,stroke=1)
def fit(im,size):return ImageOps.fit(im,size,Image.Resampling.LANCZOS)
peak=fit(Image.open(C/'assets/nanda_search_images/site-commons-wikimedia-org-nanda-devi-pe-4.jpg').convert('RGB'),(W,H));doc=Image.open(A/'visual_upgrade/FRUS_1978_official_page_capture.png').convert('RGB').crop((0,0,1232,540));doc.thumbnail((740,400),Image.Resampling.LANCZOS);doc=doc.convert('RGBA');base=ImageEnhance.Brightness(fit(Image.open(C/'assets/nasa_blue_marble_himalaya.jpg').convert('RGB'),(W,H))).enhance(.22)
def frame(t,raw=None):
 if t<5.375:
  im=base.convert('RGBA');u=ease(t/.8);im.alpha_composite(doc,(int(510+(1-u)*75),250));d=ImageDraw.Draw(im);txt(d,(70,95),'साथ मिलकर',hi);txt(d,(70,190),'CIA',latin,fill='#e9c08a');txt(d,(70,270),'भारतीय खुफिया',hi,fill='#e9c08a');txt(d,(70,325),'विभाग',hi,fill='#e9c08a');
  if t>2.3:
   # Highlight actual words on State Dept transcription; not an original physical document.
   x=int(510+(1-u)*75);d.line((x+60,444,x+int(60+250*ease((t-2.3)/.8)),444),fill='#d99559',width=4)
  foot(d,'अमेरिकी सरकारी रिकॉर्ड का ऑनलाइन टेक्स्ट  1978');return im
 if t<9.375:
  q=t-5.375;z=1+.035*ease(q/4);cw=int(W/z);ch=int(H/z);im=peak.crop(((W-cw)//2,(H-ch)//2,(W+cw)//2,(H+ch)//2)).resize((W,H),Image.Resampling.BILINEAR);im=ImageEnhance.Brightness(im).enhance(.78).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(55,70),'ऊँचे पहाड़ पर',hi);txt(d,(55,127),'मशीन लगाने का प्लान',mid,fill='#edc591');foot(d,'नंदा देवी  आधुनिक तस्वीर');return im
 if t<13.375:
  q=t-9.375;im=ImageEnhance.Brightness(peak).enhance(.52).convert('RGBA');d=ImageDraw.Draw(im);d.rounded_rectangle((50,115,605,575),radius=10,fill=(9,26,33,230));txt(d,(85,150),'रेडियो सिग्नल',hi);txt(d,(87,220),'सुनने की कोशिश',mid,fill='#edc591');cx,cy=210,466;d.line((cx,cy,cx,cy-100),fill='#e8bd7f',width=5);d.ellipse((cx-9,cy-110,cx+9,cy-92),fill='#efc68e');txt(d,(cx-45,cy+20),'रिसीवर',small,fill='#f0d3a6')
  # Animated packets travel towards the conceptual receiver, not a real geographic signal route.
  for k in range(3):
   age=q-.35-k*.6
   if age>0:
    progress=min(1,age/1.3);x=520-int(295*progress);y=cy-101;radius=5+int(4*(1-progress));d.ellipse((x-radius,y-radius,x+radius,y+radius),fill='#f2c586')
  if q>1.7:
   r=23+4*math.sin(q*4);d.ellipse((cx-r,cy-101-r,cx+r,cy-101+r),outline='#e5b775',width=3)
  foot(d,'समझाने के लिए चित्र  असली मशीन नहीं');return im
 # Real modern moving footage, explicitly illustrative, not the expedition.
 im=Image.frombytes('RGB',(W,H),raw).convert('RGBA');d=ImageDraw.Draw(im)
 if t<17.375:foot(d,'केदारकंठा  आधुनिक दृश्य');
 else:foot(d,'सांकेतिक दृश्य  असली टीम नहीं')
 return im

files=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/visual_upgrade/assets';sources=[files/'kedarkantha_pexels_19983625.mp4',files/'climber_pexels_12050237.mp4'];decs=[]
for v,n in zip(sources,[96,93]):
 decs.append(subprocess.Popen([ff,'-v','error','-i',str(v),'-vf','fps=24,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720','-frames:v',str(n),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE))
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 t=i/24;raw=None
 if i>=321:
  di=0 if i<417 else 1;raw=decs[di].stdout.read(W*H*3)
  if len(raw)!=W*H*3:raise RuntimeError(f'stock footage incomplete frame {i}')
 enc.stdin.write(frame(t,raw).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
for d in decs:d.stdout.close();assert d.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';sfx=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1530',0,.5,0,.075),('mk1489',.12,1.4,5.375,.085),('mk1430',.10,.4,9.375,.065),('mk1157',.32,7.6,13.375,.065)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','115.625','-i',voice]
for n,*_ in cues:cmd+=['-i',str(sfx/(n+'.mp3'))]
f=['[1:a]atrim=duration=21.25,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 fade=',afade=t=in:st=0:d=1,afade=t=out:st=6.6:d=1' if n=='mk1157' else f',afade=t=out:st={dur-.15}:d=0.15'
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g}{fade},adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER03_PLAN_REVIEW.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','21.25','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER03_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',final,mobile,flush=True)
