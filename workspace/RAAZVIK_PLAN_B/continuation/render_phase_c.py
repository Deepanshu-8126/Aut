from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,cv2,math
P=Path('/home/user/RAAZVIK_PLAN_B/continuation');A=P/'assets';O=P/'phase_a_work';O.mkdir(exist_ok=True);W,H=1280,720;START=650.625;D=196.625;N=4719;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),40);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),26);enbig=ImageFont.truetype(str(F/'Inter-Bold.ttf'),35)
def txt(d,p,s,f=hi,fill='#f8f5e9'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#07151a')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,235));txt(d,(38,666),s,small)
def bg(p):return ImageEnhance.Brightness(ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(.82).convert('RGBA')
imgs={n:bg(A/(n+'.png')) for n in ['route_team','camp','storm','cache','return','search','testwater','recording','water','emptybox']}
imgs['nanda']=bg('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_north_1980.jpg');imgs['camp95']=bg('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_camp_1995.jpg');imgs['kohli']=bg('/home/user/RAAZVIK_PLAN_B/chapter01/assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/cold_war_chapter/assets/kohli_2015.jpg')
imgs['kot']=bg(A/'nanda_kot_1992.jpg');imgs['desai']=bg(A/'desai_carter_1978.jpg')
V={'river':str(A/'pexels_river_13979212.mp4'),'climb':'/home/user/RAAZVIK_PLAN_B/chapter07/assets/climber_clip.mp4','climbers':'/home/user/RAAZVIK_PLAN_B/chapter04/assets/trekkers_2023_extract.mp4','weather':'/home/user/RAAZVIK_PLAN_B/chapter01/pexels_weather_11686252.mp4'}
caps={k:cv2.VideoCapture(v) for k,v in V.items()};last=None
def video(key):
 global last
 c=caps[key]
 if last!=key:c.set(cv2.CAP_PROP_POS_FRAMES,0)
 last=key;ok,b=c.read()
 if not ok:c.set(cv2.CAP_PROP_POS_FRAMES,0);ok,b=c.read()
 assert ok,key
 return ImageOps.fit(Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)),(W,H)).convert('RGBA')
def pic(name,caption,text='',real=False):
 global last;last=None
 im=imgs[name].copy();d=ImageDraw.Draw(im)
 if text:txt(d,(45,55),text,mid)
 foot(d,caption);return im
def vid(name,text=''):
 im=video(name);d=ImageDraw.Draw(im)
 if text:txt(d,(45,55),text,mid)
 foot(d,'संदर्भ फुटेज  नदी का स्थान स्थापित नहीं' if name=='river' else 'आधुनिक फुटेज  वास्तविक मिशन नहीं');return im
def source_aac():
 im=imgs['camp95'].copy();d=ImageDraw.Draw(im);d.rounded_rectangle((40,55,835,215),radius=12,fill=(9,25,30,230));txt(d,(60,75),'अमेरिकन अल्पाइन जर्नल',mid);txt(d,(60,125),'२००४ में प्रकाशित पुस्तक समीक्षा',small,fill='#efc793');foot(d,'तस्वीर: नंदा देवी कैंप १९९५  मिशन नहीं');return im
def source_memo(t):
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'अमेरिकी विदेश विभाग का नोट',hi);txt(d,(55,116),'१४ अप्रैल १९७८',mid,fill='#efc793')
 d.rounded_rectangle((55,195,1225,495),radius=12,fill='#e5e2d6');d.text((90,220),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#27363a')
 d.text((90,305),'“One of these devices was lost in an avalanche',font=en,fill='#27363a');d.text((90,355),'and never functioned...”',font=en,fill='#27363a')
 txt(d,(60,540),'नोट का दावा  घटना का वीडियो नहीं',mid,fill='#efc793');foot(d,'स्रोत: इतिहास विभाग  नोट का टेक्स्ट, अखबार नहीं');return im
def pair(t):
 global last;last=None
 im=Image.new('RGBA',(W,H),(14,31,38,255));a=ImageOps.fit(imgs['nanda'].convert('RGB'),(580,380));b=ImageOps.fit(imgs['kot'].convert('RGB'),(580,380));im.paste(a,(35,145));im.paste(b,(665,145));d=ImageDraw.Draw(im)
 txt(d,(50,70),'नंदा देवी',mid)
 if t>=524.85:txt(d,(680,70),'नंदा कोट',mid,fill='#efc793')
 if t>=549.3:txt(d,(140,555),'दो अलग पहाड़  दो अलग मशीनें',hi,fill='#efc793')
 foot(d,'नंदा देवी  बाद की तस्वीर  |  नंदा कोट  १९९२');return im
def memo_second():
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'अमेरिकी विदेश विभाग का नोट',hi);txt(d,(55,116),'१४ अप्रैल १९७८',mid,fill='#efc793')
 d.rounded_rectangle((55,195,1225,495),radius=12,fill='#e5e2d6');d.text((90,220),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#27363a')
 d.text((90,305),'“the second did function for several years',font=en,fill='#27363a');d.text((90,355),'and was later removed.”',font=en,fill='#27363a')
 txt(d,(60,540),'दूसरी मशीन बाद में हटाई गई',mid,fill='#efc793');foot(d,'स्रोत: इतिहास विभाग  नोट का टेक्स्ट, अखबार नहीं');return im
def memo_report():
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'अमेरिकी विदेश विभाग का नोट',hi);txt(d,(55,116),'१४ अप्रैल १९७८',mid,fill='#efc793')
 d.rounded_rectangle((55,195,1225,495),radius=12,fill='#e5e2d6');d.text((90,220),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#27363a')
 d.text((90,305),'“Recent press stories ... are correct',font=en,fill='#27363a');d.text((90,355),'in major respects.”',font=en,fill='#27363a')
 foot(d,'स्रोत: इतिहास विभाग  नोट का टेक्स्ट, अखबार नहीं');return im
def memo_awareness():
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'अमेरिकी विदेश विभाग का नोट',hi);txt(d,(55,116),'१४ अप्रैल १९७८',mid,fill='#efc793')
 d.rounded_rectangle((55,195,1225,495),radius=12,fill='#e5e2d6');d.text((90,220),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#27363a')
 d.text((90,305),'“Assertions ... that the Indian Government was',font=en,fill='#27363a');d.text((90,355),'not informed ... are incorrect”',font=en,fill='#27363a')
 foot(d,'स्रोत: इतिहास विभाग  नोट का टेक्स्ट, अखबार नहीं');return im
def comparison(t):
 global last;last=None
 im=Image.new('RGBA',(W,H),(14,31,38,255));d=ImageDraw.Draw(im)
 d.rounded_rectangle((80,180,550,470),radius=18,fill='#314951',outline='#799297',width=3)
 d.rounded_rectangle((150,270,490,400),radius=8,fill='#77898b',outline='#a6b5b0',width=3);d.line((150,310,490,310),fill='#a6b5b0',width=3)
 txt(d,(108,510),'संभावित बाहरी हिस्सा',mid)
 d.rounded_rectangle((720,180,1190,470),radius=18,fill='#314951',outline='#799297',width=3)
 d.rounded_rectangle((775,285,1125,368),radius=42,fill='#7a8990',outline='#a6b5b0',width=3)
 txt(d,(840,510),'कैप्सूल',mid)
 if t>=682.1:
  txt(d,(582,300),'≠',enbig,fill='#f0cc98')
  txt(d,(723,570),'मिलने की पुष्टि नहीं',mid,fill='#f0cc98')
 foot(d,'सांकेतिक चित्र  असली वस्तुएं नहीं');return im
def source_week():
 global last;last=None
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'एक रिपोर्ट  एक संभावित सुराग',hi)
 d.rounded_rectangle((55,170,1225,490),radius=12,fill='#e5e2d6');d.text((90,220),'THE WEEK',font=enbig,fill='#27363a')
 txt(d,(95,310),'अभियान से जुड़े लोगों के बयान',mid,fill='#27363a');txt(d,(95,365),'पहचान स्वतंत्र रूप से पक्की नहीं',mid,fill='#27363a')
 foot(d,'स्रोत सारांश  असली अखबार की कतरन नहीं');return im
def unknown(t):
 global last;last=None
 im=imgs['nanda'].copy();d=ImageDraw.Draw(im)
 if t>=785.1:txt(d,(45,55),'कहाँ हैं?',hi,fill='#f2d294')
 if t>=787.5:txt(d,(45,115),'सुरक्षा परत किस हालत में है?',mid)
 if t>=790.0:txt(d,(45,170),'पदार्थ बाहर निकला या नहीं?',mid)
 foot(d,'नंदा देवी  बाद की संदर्भ तस्वीर');return im
def risk():
 global last;last=None
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(45,60),'प्लूटोनियम के कण',hi)
 d.rounded_rectangle((90,205,565,440),radius=18,outline='#91a9a9',width=3,fill='#314951');txt(d,(170,290),'सांस से अंदर',hi)
 d.rounded_rectangle((715,205,1190,440),radius=18,outline='#91a9a9',width=3,fill='#314951');txt(d,(815,290),'खाने से अंदर',hi)
 txt(d,(95,505),'शरीर के अंदर जाना चिंता का विषय',mid,fill='#efc793');foot(d,'सामान्य स्वास्थ्य जानकारी  वास्तविक संपर्क नहीं दिखाया गया');return im
def frame(t):
 global last
 a=START+t
 if a<654.35:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर')
 if a<660.62:return source_week()
 if a<666.73:return pic('emptybox','एआई दृश्य  वास्तविक खोज की वस्तु नहीं','१९९३  संभावित धातु के हिस्से' if a>=661.3 else '')
 if a<671.61:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन','पहचान  अभियान से जुड़े लोगों का अनुमान' if a>=668.7 else '')
 if a<675.61:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं')
 if a<688.45:return comparison(a)
 if a<699.38:return source_week()
 if a<704.52:return pic('testwater','एआई दृश्य  काल्पनिक जल परीक्षण','कुछ नमूनों में प्रदूषण नहीं मिला' if a>=701 else '')
 if a<708.88:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','कैप्सूलों का ठिकाना तय नहीं')
 if a<713.88:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं','यदि हिस्से उसी मशीन के हों' if a>=709.4 else '')
 if a<719.84:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन')
 if a<725.32:return source_week()
 if a<731.34:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं','बयान में खाली बक्सों का जिक्र' if a>=729 else '')
 if a<734.8:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं')
 if a<741.34:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन','पुराने जनरेटर से जुड़े होने का अनुमान' if a>=738.8 else '')
 if a<748.56:return source_week()
 if a<759.66:return comparison(682.5)
 if a<767.12:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं','तस्वीर अंतिम सबूत नहीं' if a>=763 else '')
 if a<776.5:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','संभावित सुराग  पूरा जवाब नहीं')
 if a<785.08:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','आज कितना खतरा?' if a>=778 else '')
 if a<793.92:return unknown(a)
 if a<801.9:return risk()
 if a<810.96:return vid('river','न प्रदूषण साबित  न बाढ़ की वजह' if a>=807 else 'बिना सबूत पानी जहरीला नहीं कह सकते' if a>=805 else '')
 if a<818.3:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन','पता है और नहीं पता  अलग रखें' if a>=814 else '')
 if a<821.74:return pic('route_team','एआई दृश्य  असली टीम नहीं')
 if a<824.6:return pic('storm','एआई दृश्य  वास्तविक तूफान नहीं')
 if a<827.48:return pic('return','एआई दृश्य  काल्पनिक खोज')
 if a<830.1:return pair(a)
 if a<833.48:return pic('emptybox','एआई दृश्य  वास्तविक वस्तु नहीं')
 if a<839.22:return comparison(682.5)
 if a<847.25:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','वो गई कहाँ?' if a>=845.76 else '')
 raise RuntimeError(a)
out=O/'picture_c.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%480==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
for c in caps.values():c.release()
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1530',0,.5,4,.025),('mk1430',.1,.4,26,.025),('mk1530',0,.5,98,.025)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss',str(START),'-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=[f'[1:a]apad=pad_dur=0.1,atrim=duration={D},asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CONTINUATION_C_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t',str(D),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CONTINUATION_C_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
