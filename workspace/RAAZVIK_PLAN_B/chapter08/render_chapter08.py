from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter08');A=P/'assets';O=P/'render_work';O.mkdir(exist_ok=True);W,H=1280,720;N=1146;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),42);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);latin=ImageFont.truetype(str(F/'Inter-Bold.ttf'),40)
def txt(d,p,s,f=hi,fill='#f8f5e9'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0b171c')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,235));txt(d,(38,666),s,small)
def bg(p):return ImageEnhance.Brightness(ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(.84).convert('RGBA')
replacement=bg(A/'replacement.png');warm=bg(A/'warmth_hands.png');nanda=bg('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_north_1980.jpg')
pioneer=Image.open(A/'pioneer10_1972.jpg').convert('RGB');pioneer.thumbnail((625,640));
def progress_arrow(d,x1,x2,y,t,c='#d69a52'):
 d.line((x1,y,x2,y),fill=c,width=5);d.polygon([(x2,y),(x2-15,y-10),(x2-15,y+10)],fill=c)
 z=x1+int((x2-x1-15)*((t*0.6)%1));d.ellipse((z-7,y-7,z+7,y+7),fill='#fff0bd')
def diagram(t):
 im=Image.new('RGBA',(W,H),(13,31,38));d=ImageDraw.Draw(im)
 # This schematic makes no claim about the device's dimensions or internal layout.
 txt(d,(48,45),'गर्मी से बिजली',hi)
 d.rounded_rectangle((55,190,360,445),radius=28,fill='#304450',outline='#8da7ac',width=3)
 d.rounded_rectangle((120,265,295,345),radius=38,fill='#ab7046',outline='#e7b572',width=4)
 txt(d,(91,467),'रेडियोधर्मी पदार्थ',mid)
 if t>=2.6 or t>=40:
  for k in range(3):
   yy=250+60*k;phase=(t*40+k*23)%48;d.arc((307+phase,yy-20,348+phase,yy+20),270,90,fill='#f0ad63',width=4)
  txt(d,(415,247),'गर्मी',mid,fill='#f2c18b')
 if t>=4.45 or t>=40:
  progress_arrow(d,370,548,345,t);d.rounded_rectangle((555,195,825,445),radius=22,fill='#38545c',outline='#8da7ac',width=3)
  for x in range(575,805,24):d.line((x,224,x,411),fill='#92adb0',width=5)
  txt(d,(566,469),'थर्मोइलेक्ट्रिक',mid);txt(d,(611,509),'कन्वर्टर',mid)
 if t>=5.4 or t>=40:
  progress_arrow(d,835,1003,345,t,'#eed497');d.rounded_rectangle((1010,235,1200,390),radius=18,outline='#e7d49d',width=4,fill='#253e49')
  d.polygon([(1113,261),(1079,321),(1102,321),(1087,364),(1130,305),(1106,305)],fill='#f4d68b');txt(d,(1047,468),'बिजली',mid,fill='#f2d697')
 foot(d,'सांकेतिक चित्र  असली मशीन का कटाव नहीं');return im
def frame(t):
 if t<6.62:return diagram(t)
 if t<11.32:
  im=replacement.copy();d=ImageDraw.Draw(im)
  if t>=9.9:txt(d,(45,55),'बार-बार बदलने की जरूरत नहीं',mid)
  foot(d,'एआई दृश्य  सामान्य उदाहरण  मिशन नहीं');return im
 if t<16.32:
  im=Image.new('RGBA',(W,H),(16,33,41));im.alpha_composite(pioneer.convert('RGBA'),(620,38));d=ImageDraw.Draw(im)
  if t>=12.0:txt(d,(48,115),'नासा में भी',hi)
  if t>=14.9:txt(d,(48,177),'अंतरिक्ष मिशनों में',mid,fill='#efc793')
  foot(d,'पायनियर १०  १९७२  अलग मिशन');return im
 if t<20.9:
  im=nanda.copy();d=ImageDraw.Draw(im)
  if t>=19.3:txt(d,(45,55),'हिमालय की मशीन अलग थी',mid)
  foot(d,'नंदा देवी  संदर्भ तस्वीर  १९८०');return im
 if t<26.64:
  im=Image.new('RGBA',(W,H),(15,31,37));d=ImageDraw.Draw(im)
  d.rounded_rectangle((365,250,930,380),radius=65,fill='#526d75',outline='#b5c9c7',width=5);d.line((445,260,445,370),fill='#a6b7b5',width=4);d.line((850,260,850,370),fill='#a6b7b5',width=4)
  if t>=21.5:txt(d,(50,55),'प्लूटोनियम',hi,fill='#efc793')
  if t>=25.15:txt(d,(450,430),'कैप्सूल में बंद',mid)
  foot(d,'सांकेतिक चित्र  संख्या और डिजाइन नहीं दिखाए गए');return im
 if t<34.02:
  im=Image.new('RGBA',(W,H),(15,31,37));d=ImageDraw.Draw(im)
  for x,y in [(160,235),(445,220),(730,235)]:
   d.rounded_rectangle((x,y,x+220,y+200),radius=8,fill='#d2d0bd',outline='#e4d7b7',width=2)
   for q in range(3):d.line((x+24,y+50+q*23,x+195-q*20,y+50+q*23),fill='#718084',width=6)
   d.ellipse((x+68,y+120,x+142,y+194),outline='#886f54',width=3);d.text((x+93,y+117),'?',font=latin,fill='#5d6563')
  if t>=28.5:txt(d,(50,55),'मात्रा पर अलग-अलग दावे',hi,fill='#efc793')
  if t>=31.7:txt(d,(50,510),'साफ पुष्टि जरूरी',mid)
  foot(d,'प्रतीकात्मक चित्र  कोई निश्चित मात्रा नहीं');return im
 if t<40.46:
  im=warm.copy();d=ImageDraw.Draw(im)
  if t>=35.0:txt(d,(45,55),'बाद के विवरणों में गर्मी का जिक्र',mid)
  foot(d,'एआई दृश्य  काल्पनिक उदाहरण');return im
 if t<43.6:return diagram(t)
 im=nanda.copy();d=ImageDraw.Draw(im)
 if t>=44.7:txt(d,(45,55),'गायब होने के बाद चिंता',mid)
 foot(d,'नंदा देवी  संदर्भ तस्वीर  १९८०');return im
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1430',.1,.4,3.6,.03),('mk1530',0,.5,11.32,.025),('mk1489',.12,1.2,16.32,.025),('mk1157',.3,4,40.46,.02)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','276.875','-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=['[1:a]atrim=duration=47.75,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER08_EXPLAINER_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','47.75','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER08_EXPLAINER_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
