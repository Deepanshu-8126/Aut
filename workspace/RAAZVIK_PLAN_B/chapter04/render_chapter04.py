from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import math,subprocess,imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter04');A=P/'assets';O=P/'render_work';O.mkdir(exist_ok=True);F=Path('/home/user/explainer-pipeline/assets/fonts'); ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1280,720;N=786
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),44);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),21);latin=ImageFont.truetype(str(F/'Inter-Bold.ttf'),52)
def txt(d,xy,s,f,fill='#f9f5e9'):d.text(xy,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0c1920')
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((34,666,min(1235,56+b[2]),705),radius=5,fill=(7,20,25,220));txt(d,(42,670),s,small)
def fit(im):return ImageOps.fit(im,(W,H),Image.Resampling.LANCZOS)
base=ImageEnhance.Brightness(fit(Image.open('/home/user/RAAZVIK_PLAN_B/chapter01/assets/nasa_blue_marble_himalaya.jpg').convert('RGB'))).enhance(.32)
group=Image.open(A/'everest_reunion_2015.jpg').convert('RGB');peak=ImageEnhance.Brightness(fit(Image.open(A/'nanda_1936.jpg').convert('RGB'))).enhance(.85);camp=ImageEnhance.Brightness(fit(Image.open(A/'nanda_camp_1995.jpg').convert('RGB').crop((25,30,1250,850)))).enhance(.8)
def frame(t):
 if t<5.1:
  im=base.convert('RGBA');d=ImageDraw.Draw(im);txt(d,(75,85),'मिशन के लिए टीम',hi)
  u=ease((t-.45)/1.1);d.rounded_rectangle((int(75-100*(1-u)),230,int(540-100*(1-u)),413),radius=12,fill=(24,50,55,235),outline=(122,157,150),width=2);txt(d,(115,270),'भारत',hi,fill='#ebc192');
  v=ease((t-1)/1.1);d.rounded_rectangle((int(740+100*(1-v)),230,int(1205+100*(1-v)),413),radius=12,fill=(24,50,55,235),outline=(122,157,150),width=2);txt(d,(785,270),'अमेरिका',hi,fill='#ebc192')
  if t>1.8:
   end=560+int(160*ease((t-1.8)/1));d.line((560,322,end,322),fill='#e4bd86',width=5)
  txt(d,(75,495),'अनुभवी पर्वतारोही',hi);foot(d,'सांकेतिक ग्राफिक  टीम की तस्वीर नहीं');return im
 if t<13.1:
  q=t-5.1
  # Distinct 2015 reunion group image; subject identified by comparing same-event PIB portrait.
  zoom=1+1.45*ease((q-.8)/2.5);cw=int(1280/zoom);ch=int(643/zoom);cx=int(640+(875-640)*ease((q-.8)/2.5));cy=int(322+(260-322)*ease((q-.8)/2.5));l=max(0,min(1280-cw,cx-cw//2));top=max(0,min(643-ch,cy-ch//2));im=ImageOps.fit(group.crop((l,top,l+cw,top+ch)),(W,H),Image.Resampling.BILINEAR).convert('RGBA');d=ImageDraw.Draw(im)
  if q>1:txt(d,(45,75),'कैप्टन एम. एस. कोहली',hi)
  if q>4.1:txt(d,(45,143),'1965 एवरेस्ट अभियान के लीडर',mid,fill='#edc591')
  foot(d,'एवरेस्ट अभियान की मुलाकात  2015');return im
 if t<15.1:
  im=ImageEnhance.Brightness(peak).enhance(.54).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(65,260),'अब एक नया मिशन',hi,fill='#edc591');return im
 if t<21.2:
  q=t-15.1;z=1+.05*ease(q/6);cw=int(W/z);ch=int(H/z);im=peak.crop(((W-cw)//2,(H-ch)//2,(W+cw)//2,(H+ch)//2)).resize((W,H),Image.Resampling.BILINEAR).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(55,65),'नंदा देवी',hi);txt(d,(55,125),'उत्तराखंड',mid,fill='#edc591')
  if q>3.5:txt(d,(55,180),'लगभग 7,800 मीटर',mid)
  foot(d,'नंदा देवी की तस्वीर  1936');return im
 if t<27.0:
  q=t-21.2;z=1+.05*ease(q/5.8);cw=int(W/z);ch=int(H/z);im=camp.crop(((W-cw)//2,(H-ch)//2,(W+cw)//2,(H+ch)//2)).resize((W,H),Image.Resampling.BILINEAR).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(55,67),'बर्फ और कठिन ढलान',hi);foot(d,'नंदा देवी का कैंप  1995  मिशन की तस्वीर नहीं');return im
 q=t-27;im=Image.new('RGBA',(W,H),(12,31,39,255));d=ImageDraw.Draw(im);txt(d,(65,68),'ऊँचाई पर हवा पतली',hi)
 # Conceptual animation: dots spread out as altitude increases; not a numerical simulation.
 d.rectangle((100,198,1180,565),outline=(124,153,151,255),width=3);d.line((150,505,1120,505),fill=(109,143,145),width=2);d.line((150,505,150,245),fill=(109,143,145),width=2)
 pts=[(175+i*54,480-int(i*10+30*math.sin(i*.35))) for i in range(17)];n=max(1,int(len(pts)*ease(q/2)))
 if n>1:d.line(pts[:n],fill='#e4bd86',width=5)
 for i in range(5):
  x=210+i*50; y=370+(i%2)*45;d.ellipse((x-6,y-6,x+6,y+6),fill=(191,217,209))
 for i in range(3):
  x=900+i*65;y=277+(i%2)*57;d.ellipse((x-6,y-6,x+6,y+6),fill=(191,217,209))
 txt(d,(190,530),'नीचे',mid);txt(d,(980,530),'ऊपर',mid);foot(d,'सांकेतिक ग्राफिक  हवा के अणुओं का पैमाना नहीं');return im
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';sfx=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1489',.12,1.4,5.1,.06),('mk1530',0,.5,15.1,.06),('mk1157',.32,9,21.2,.045),('mk1430',.1,.4,27,.05)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','136.875','-i',voice]
for n,*_ in cues:cmd+=['-i',str(sfx/(n+'.mp3'))]
f=['[1:a]atrim=duration=32.75,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER04_HD_REVIEW.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','32.75','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER04_MOBILE_REVIEW.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',final,mobile,flush=True)
