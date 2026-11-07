from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter06');A=P/'assets';O=P/'render_work';O.mkdir(exist_ok=True);W,H=1280,720;N=960;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),42);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);latin=ImageFont.truetype(str(F/'Inter-Bold.ttf'),31)
def txt(d,p,s,f=hi,fill='#f9f6e9'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0a171b')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,225));txt(d,(38,666),s,small)
def bg(name,brightness=.79):return ImageEnhance.Brightness(ImageOps.fit(Image.open(A/name).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(brightness).convert('RGBA')
imgs={n:bg(n) for n in ['team_prepare.png','practice_concept.png','assembly_concept.png','heavy_carry.png','missing_part.png','connection_concept.png','storm_concept.png','different_roles.png','denali_nps.jpg']}
# Separate model as contextual evidence, never the mission hardware.
rtg=Image.open(A/'cassini_rtg.jpg').convert('RGB');rtg.thumbnail((440,640),Image.Resampling.LANCZOS)
def frame(t):
 if t<3.45:
  im=Image.new('RGBA',(W,H),(15,35,42,255));pic=rtg.convert('RGBA');im.alpha_composite(pic,(775+(440-pic.width)//2,35));d=ImageDraw.Draw(im)
  if t>=1.24:txt(d,(60,140),'बिजली बनाने का',hi);txt(d,(60,200),'अलग तरीका',hi,fill='#ecc895')
  txt(d,(60,470),'अलग मिशन का मॉडल',mid);foot(d,'नासा कैसिनी  1997  नंदा देवी की मशीन नहीं');return im
 if t<6.62:
  im=imgs['team_prepare.png'].copy();d=ImageDraw.Draw(im)
  if t>=4.76:txt(d,(45,62),'मिशन से पहले तैयारी',hi)
  foot(d,'एआई सांकेतिक दृश्य  असली टीम नहीं');return im
 if t<15.25:
  im=imgs['denali_nps.jpg'].copy();d=ImageDraw.Draw(im)
  if t<9.54:
   txt(d,(55,58),'अमेरिकी अल्पाइन जर्नल',hi);txt(d,(55,120),'प्रकाशित विवरण',mid,fill='#edc591')
  elif t<12.16:txt(d,(55,58),'भारतीय और अमेरिकी पर्वतारोही',mid)
  elif t<13.10:txt(d,(55,58),'अमेरिका में प्रशिक्षण',hi)
  else:txt(d,(55,58),'अलास्का में साथ ट्रेनिंग',hi)
  foot(d,'संदर्भ तस्वीर  वास्तविक प्रशिक्षण नहीं' if t<13.10 else 'डेनाली, अलास्का  संदर्भ तस्वीर  वास्तविक प्रशिक्षण नहीं');return im
 if t<18.7:
  im=imgs['practice_concept.png'].copy();d=ImageDraw.Draw(im)
  if t>=17.08:txt(d,(45,55),'ऊँचाई पर चढ़ने का अभ्यास',mid)
  foot(d,'एआई सांकेतिक दृश्य  वास्तविक प्रशिक्षण नहीं');return im
 if t<23.58:
  im=imgs['assembly_concept.png'].copy();d=ImageDraw.Draw(im)
  if t>=19.3:txt(d,(45,55),'मशीन जोड़ने की ट्रेनिंग',mid)
  if t>=21.7:txt(d,(45,112),'सिर्फ चढ़ाई नहीं',mid,fill='#edc591')
  foot(d,'एआई दृश्य  उपकरण और लोग काल्पनिक');return im
 if t<28.58:
  im=imgs['heavy_carry.png'].copy();d=ImageDraw.Draw(im)
  if t>=24.18:txt(d,(45,55),'भारी सामान पहुँचाना',hi)
  if t>=26.52:txt(d,(45,115),'हर कदम पर मेहनत',mid,fill='#edc591')
  foot(d,'एआई सांकेतिक दृश्य  वास्तविक घटना नहीं');return im
 if t<31.1:
  im=imgs['missing_part.png'].copy();d=ImageDraw.Draw(im)
  if t>=29.28:txt(d,(45,55),'कोई हिस्सा पीछे छूट जाए?',mid)
  foot(d,'एआई दृश्य  काल्पनिक उदाहरण');return im
 if t<35.46:
  im=imgs['connection_concept.png'].copy();d=ImageDraw.Draw(im)
  if t>=31.12:txt(d,(45,55),'तार सही से न जुड़े?',mid)
  if t>=33.24:txt(d,(45,110),'पहाड़ पर ठीक करना मुश्किल',mid,fill='#edc591')
  foot(d,'एआई दृश्य  काल्पनिक उदाहरण');return im
 if t<37.7:
  im=imgs['storm_concept.png'].copy();d=ImageDraw.Draw(im)
  if t>=35.82:txt(d,(45,55),'खराब मौसम में इंतजार',mid)
  foot(d,'एआई दृश्य  काल्पनिक उदाहरण');return im
 im=imgs['different_roles.png'].copy();d=ImageDraw.Draw(im)
 if t>=38.78:txt(d,(45,55),'टीम में काम अलग-अलग',mid)
 foot(d,'एआई सांकेतिक दृश्य  असली टीम नहीं');return im
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1430',.1,.4,1.24,.04),('mk1530',0,.5,3.45,.04),('mk1489',.12,1.2,6.62,.04),('mk1530',0,.5,19.3,.035),('mk1157',.3,6,23.58,.04),('mk1430',.1,.4,29,.035)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','200.125','-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=['[1:a]atrim=duration=40,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER06_SITUATION_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','40','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER06_SITUATION_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
