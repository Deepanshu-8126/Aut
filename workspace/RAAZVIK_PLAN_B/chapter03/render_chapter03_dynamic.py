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
peak=fit(Image.open(P/'new_assets/nanda_2016.jpg').convert('RGB'),(W,H));doc=Image.open(A/'visual_upgrade/FRUS_1978_official_page_capture.png').convert('RGB').crop((0,0,1232,540));doc.thumbnail((740,400),Image.Resampling.LANCZOS);doc=doc.convert('RGBA');base=ImageEnhance.Brightness(fit(Image.open(C/'assets/nasa_blue_marble_himalaya.jpg').convert('RGB'),(W,H))).enhance(.22)
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
  q=t-9.375;im=Image.new('RGBA',(W,H),(13,27,33,255));d=ImageDraw.Draw(im)
  txt(d,(65,70),'रेडियो सिग्नल सुनने की योजना',hi)
  # Two explicitly conceptual objects, not a mapped path or historical equipment likeness.
  d.rounded_rectangle((65,250,410,495),radius=10,fill=(30,50,55,255),outline=(115,139,133,255),width=2)
  d.rounded_rectangle((865,250,1210,495),radius=10,fill=(30,50,55,255),outline=(115,139,133,255),width=2)
  txt(d,(104,280),'मिसाइल टेस्ट',mid,fill='#eac58f');txt(d,(910,280),'रिसीवर',mid,fill='#eac58f')
  d.line((170,415,170,375),fill='#efd4aa',width=4);d.ellipse((164,368,176,380),fill='#efd4aa')
  for k in range(2):
   r=17+k*12;d.arc((170-r,375-r,170+r,375+r),-70,70,fill='#e3bf8f',width=3)
  d.line((1010,423,1010,370),fill='#efd4aa',width=4);d.ellipse((1003,363,1017,377),fill='#efd4aa')
  prog=ease((q-.55)/1.4);x2=430+int(410*prog);d.line((430,370,x2,370),fill='#e7bb80',width=4)
  if prog>.98:
   d.polygon(((836,361),(856,370),(836,379)),fill='#e7bb80')
   # The incoming signal becomes a moving waveform at the receiver.
   pts=[];length=int(120*ease((q-2)/1))
   for x in range(length):pts.append((925+x,455+int(10*math.sin(x*.22-q*5))))
   if len(pts)>1:d.line(pts,fill='#efc990',width=3)
  foot(d,'सांकेतिक ग्राफिक  असली रूट या मशीन नहीं');return im
 if t>=17.375:
  q=t-17.375;im=base.convert('RGBA');photo=fit(Image.open(P/'new_assets/porter_nepal_2006.jpg').convert('RGB'),(500,615)).convert('RGBA');im.alpha_composite(photo,(int(110-80*(1-ease(q/.8))),55));d=ImageDraw.Draw(im);txt(d,(700,200),'सामान ऊपर',hi);txt(d,(700,260),'कौन ले जाएगा?',hi,fill='#edc591');foot(d,'नेपाल 2006  लकड़ी ले जाते पोर्टर');return im
 # Real modern moving footage, explicitly illustrative, not the expedition.
 im=Image.frombytes('RGB',(W,H),raw).convert('RGBA');d=ImageDraw.Draw(im)
 if t<17.375:foot(d,'केदारकंठा  आधुनिक दृश्य');
 else:foot(d,'केदारकंठा के ट्रेकर्स  2025  सांकेतिक दृश्य')
 return im

files=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/visual_upgrade/assets';sources=[P/'new_assets/trek_aerial_2024.mp4',P/'new_assets/trek_group_2025.mp4'];decs=[]
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
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER03_DYNAMIC_REVIEW.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','21.25','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER03_DYNAMIC_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',final,mobile,flush=True)
