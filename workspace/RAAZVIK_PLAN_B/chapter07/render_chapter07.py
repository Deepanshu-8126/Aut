from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,cv2,math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter07');A=P/'assets';O=P/'render_work';O.mkdir(exist_ok=True);W,H=1280,720;N=882;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),42);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),31);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);latin=ImageFont.truetype(str(F/'Inter-Bold.ttf'),47)
def txt(d,p,s,f=hi,fill='#f9f6e9'): d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0a171b')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,225));txt(d,(38,666),s,small)
def bg(name):return ImageEnhance.Brightness(ImageOps.fit(Image.open(A/name).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(.84).convert('RGBA')
imgs={n:bg(n) for n in ['electronics_expert.png','porter_2014.jpg','support_team.png','safety_concept.png','generic_rtg.png']}
cap=cv2.VideoCapture(str(A/'climber_clip.mp4'))
def frame(t):
 if t<2.1:
  ok,b=cap.read(); assert ok
  im=Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)).resize((W,H)).convert('RGBA');d=ImageDraw.Draw(im);foot(d,'आधुनिक फुटेज  वास्तविक मिशन नहीं');return im
 if t<3.78:
  im=imgs['electronics_expert.png'].copy();d=ImageDraw.Draw(im);foot(d,'एआई दृश्य  काल्पनिक विशेषज्ञ');return im
 if t<7.24:
  im=imgs['porter_2014.jpg'].copy();d=ImageDraw.Draw(im);foot(d,'नेपाल, २०१४  संदर्भ तस्वीर  मिशन नहीं');return im
 if t<15.18:
  im=imgs['support_team.png'].copy();d=ImageDraw.Draw(im)
  if t>9.0:txt(d,(45,55),'कई लोगों की मेहनत',mid)
  foot(d,'एआई दृश्य  असली टीम नहीं');return im
 if t<19.1:
  im=imgs['safety_concept.png'].copy();d=ImageDraw.Draw(im)
  if t>16.0:txt(d,(45,55),'सुरक्षित वापसी भी जरूरी',mid)
  foot(d,'एआई दृश्य  काल्पनिक उदाहरण');return im
 im=imgs['generic_rtg.png'].copy();d=ImageDraw.Draw(im)
 if 22.9<=t<27.14:txt(d,(45,55),'यह बम नहीं था',hi,fill='#f3d69c')
 if 27.14<=t<30.98:
  txt(d,(45,55),'दूसरे उपकरणों को बिजली',mid,fill='#f3d69c')
  # Conceptual arrow overlays (not a claim about the actual physical circuit).
  d.line((665,320,860,320),fill='#f4d989',width=3);d.polygon([(860,320),(844,311),(844,329)],fill='#f4d989')
  phase=((t-27.14)*.65)%1;x=665+int(180*phase);d.ellipse((x-7,313,x+7,327),fill='#fff4d1')
 if 30.98<=t<33.64:txt(d,(45,50),'RTG',latin,fill='#f3d69c')
 if t>=33.64:txt(d,(45,55),'नाम से ज्यादा काम समझिए',mid,fill='#f3d69c')
 foot(d,'एआई कल्पना  असली मशीन नहीं');return im
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0;cap.release()
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1489',.12,1.2,.05,.025),('mk1430',.1,.4,7.24,.03),('mk1530',0,.5,19.1,.028),('mk1157',.3,4,27.14,.025)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','240.125','-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=['[1:a]atrim=duration=36.75,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER07_SITUATION_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','36.75','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER07_SITUATION_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
