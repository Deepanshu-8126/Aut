from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,cv2,math
P=Path('/home/user/RAAZVIK_PLAN_B/continuation');A=P/'assets';O=P/'phase_a_work';O.mkdir(exist_ok=True);W,H=1280,720;START=433.625;D=217;N=5208;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),40);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),26);enbig=ImageFont.truetype(str(F/'Inter-Bold.ttf'),35)
def txt(d,p,s,f=hi,fill='#f8f5e9'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#07151a')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,235));txt(d,(38,666),s,small)
def bg(p):return ImageEnhance.Brightness(ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(.82).convert('RGBA')
imgs={n:bg(A/(n+'.png')) for n in ['route_team','camp','storm','cache','return','search','testwater','recording','water']}
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
def frame(t):
 global last
 a=START+t
 if a<439.55:return pic('search','एआई दृश्य  काल्पनिक खोज','खोज शुरू हुई' if a>=434.2 else '')
 if a<443.08:return vid('climbers')
 if a<446.62:return pic('search','एआई दृश्य  काल्पनिक ग्लेशियर')
 if a<452.46:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','मशीन कहाँ गई  पता नहीं' if a>=450.8 else '')
 if a<459.06:return vid('climb')
 if a<465.5:return pic('search','एआई दृश्य  काल्पनिक ग्लेशियर')
 if a<470.25:return pic('camp95','नंदा देवी कैंप १९९५  वास्तविक खोज नहीं')
 if a<476.4:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','भारी सामान कहाँ गया  स्पष्ट नहीं' if a>=471 else '')
 if a<482.2:return pic('search','एआई दृश्य  काल्पनिक खोज')
 if a<486.55:return pic('cache','एआई दृश्य  काल्पनिक सामान','सुरक्षा भी जरूरी' if a>=484.3 else '')
 if a<494.76:return pic('search','एआई दृश्य  उपकरण काल्पनिक')
 if a<497.56:return pic('return','एआई दृश्य  काल्पनिक खोज','सटीक ठिकाना नहीं मिला')
 if a<504.62:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','गर्मी से बर्फ पिघलने का अनुमान' if a>=500.1 else '')
 if a<509.5:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','संभावना  साबित तस्वीर नहीं')
 if a<516.38:return pic('search','एआई दृश्य  स्थान काल्पनिक','कहाँ रुकी  हम नहीं जानते' if a>=509.5 else '')
 if a<524.85:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','एक दूसरी मशीन भी थी' if a>=519 else '')
 if a<529.28:return pair(a)
 if a<537.47:last=None;return memo_second()
 if a<552.54:return pair(a)
 if a<557.64:last=None;return memo_awareness()
 if a<564.61:return pic('desai','कार्टर और देसाई  जून १९७८  अन्य अवसर')
 if a<572.25:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन','किसे क्या पता था?' if a>=565.4 else '')
 if a<576.28:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर')
 if a<585.45:return pic('recording','एआई दृश्य  काल्पनिक अध्ययन','१९७८  खबर सामने आई' if a>=577 else '')
 if a<588.78:return pic('desai','कार्टर और देसाई  जून १९७८  अन्य अवसर')
 if a<600.12:last=None;return memo_report()
 if a<605.61:return pic('desai','कार्टर और देसाई  जून १९७८  संसद की तस्वीर नहीं','मोरारजी देसाई' if a>=600.3 else '')
 if a<614.76:return vid('river')
 if a<620.83:return pic('water','एआई दृश्य  काल्पनिक जलधारा','कैप्सूल टूटे तो क्या होगा?' if a>=615 else '')
 if a<626.62:return vid('river','चिंता और साबित प्रदूषण अलग हैं' if a>=623 else '')
 if a<632.71:return pic('testwater','एआई दृश्य  काल्पनिक जल परीक्षण','जांच किए नमूनों में प्रदूषण नहीं मिला' if a>=630.5 else '')
 if a<640.85:return pic('testwater','एआई दृश्य  काल्पनिक जल परीक्षण','कैप्सूल की वर्तमान हालत अज्ञात' if a>=638 else '')
 if a<650.625:return vid('river','नतीजा उसी नमूने और समय का' if a>=642.8 else '')
 raise RuntimeError(a)
out=O/'picture_b.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%480==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
for c in caps.values():c.release()
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1489',.12,1.5,6.4,.02),('mk1430',.1,.4,82.7,.025),('mk1530',0,.5,119,.025),('mk1430',.1,.4,172,.025)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss',str(START),'-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=[f'[1:a]atrim=duration={D},asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CONTINUATION_B_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t',str(D),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CONTINUATION_B_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
