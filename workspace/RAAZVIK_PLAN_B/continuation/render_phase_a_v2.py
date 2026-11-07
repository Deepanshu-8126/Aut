from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,cv2,math
P=Path('/home/user/RAAZVIK_PLAN_B/continuation');A=P/'assets';O=P/'phase_a_work';O.mkdir(exist_ok=True);W,H=1280,720;START=324.625;D=109;N=2616;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts')
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),40);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),30);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),26);enbig=ImageFont.truetype(str(F/'Inter-Bold.ttf'),35)
def txt(d,p,s,f=hi,fill='#f8f5e9'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#07151a')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,235));txt(d,(38,666),s,small)
def bg(p):return ImageEnhance.Brightness(ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(.82).convert('RGBA')
imgs={n:bg(A/(n+'.png')) for n in ['route_team','camp','storm','cache','return','route_supply_new','descent_new','winter_weather_new']}
imgs['nanda']=bg('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_north_1980.jpg');imgs['camp95']=bg('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_camp_1995.jpg');imgs['kohli']=bg('/home/user/RAAZVIK_PLAN_B/chapter01/assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/cold_war_chapter/assets/kohli_2015.jpg')
V={'climb':'/home/user/RAAZVIK_PLAN_B/chapter07/assets/climber_clip.mp4','climbers':'/home/user/RAAZVIK_PLAN_B/chapter04/assets/trekkers_2023_extract.mp4','weather':'/home/user/RAAZVIK_PLAN_B/chapter01/pexels_weather_11686252.mp4'}
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
 foot(d,'आधुनिक फुटेज  वास्तविक मिशन नहीं');return im
def source_aac():
 im=imgs['camp95'].copy();d=ImageDraw.Draw(im);d.rounded_rectangle((40,55,835,215),radius=12,fill=(9,25,30,230));txt(d,(60,75),'अमेरिकन अल्पाइन जर्नल',mid);txt(d,(60,125),'२००४ में प्रकाशित पुस्तक समीक्षा',small,fill='#efc793');foot(d,'तस्वीर: नंदा देवी कैंप १९९५  मिशन नहीं');return im
def source_memo(t):
 im=Image.new('RGBA',(W,H),(16,34,42,255));d=ImageDraw.Draw(im)
 txt(d,(55,55),'अमेरिकी विदेश विभाग का नोट',hi);txt(d,(55,116),'१४ अप्रैल १९७८',mid,fill='#efc793')
 d.rounded_rectangle((55,195,1225,495),radius=12,fill='#e5e2d6');d.text((90,220),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#27363a')
 d.text((90,305),'“One of these devices was lost in an avalanche',font=en,fill='#27363a');d.text((90,355),'and never functioned...”',font=en,fill='#27363a')
 txt(d,(60,540),'नोट का दावा  घटना का वीडियो नहीं',mid,fill='#efc793');foot(d,'स्रोत: इतिहास विभाग  नोट का टेक्स्ट, अखबार नहीं');return im
def frame(t):
 global last
 a=START+t
 if a<328.8:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर')
 if a<331.38:return pic('route_supply_new','एआई दृश्य  असली टीम नहीं')
 if a<333.64:return pic('camp','एआई दृश्य  काल्पनिक कैंप')
 if a<337.38:return pic('camp95','नंदा देवी कैंप १९९५  वास्तविक मिशन नहीं')
 if a<341:return vid('weather')
 if a<347.37:return pic('storm','एआई दृश्य  काल्पनिक मौसम','मौसम बिगड़ने लगा' if a>=341.5 else '')
 if a<349.87:last=None;return source_aac()
 if a<352.62:return pic('camp','एआई दृश्य  काल्पनिक कैंप','चौथे कैंप से आगे की तैयारी' if a>=350.6 else '')
 if a<353.76:return pic('storm','एआई दृश्य  वास्तविक तूफान नहीं')
 if a<356.17:return pic('kohli','कोहली  बाद की तस्वीर  १९६५ नहीं')
 if a<360.08:return pic('descent_new','एआई दृश्य  काल्पनिक वापसी')
 if a<366.67:return pic('cache','एआई दृश्य  काल्पनिक उदाहरण','सामान बांधकर छोड़ा' if a>=364.28 else '')
 if a<370.62:return pic('route_team','एआई दृश्य  काल्पनिक उदाहरण','वापस आने की योजना' if a>=367.5 else '')
 if a<374.47:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर')
 if a<377:return vid('climb')
 if a<381.85:return pic('winter_weather_new','एआई दृश्य  काल्पनिक सर्दी')
 if a<384.62:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर')
 if a<387.06:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','उस वक्त क्या हुआ  किसी ने नहीं देखा')
 if a<393.43:return pic('return','एआई दृश्य  काल्पनिक खोज')
 if a<402.56:return pic('return','एआई दृश्य  काल्पनिक खोज','१९६६  टीम लौटी' if a>=393.8 else '')
 if a<405:return pic('return','एआई दृश्य  काल्पनिक खोज','सामान नहीं मिला' if a>=402.7 else '')
 if a<409.75:return pic('camp95','नंदा देवी कैंप १९९५  खोज की तस्वीर नहीं')
 if a<417.7:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','हिमस्खलन  एक संभावना' if a>=410.2 else '')
 if a<423.06:last=None;return source_memo(a)
 if a<428.02:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','गायब होने का पल किसी ने नहीं देखा' if a>=423.8 else '')
 if a<433.625:return pic('nanda','नंदा देवी  बाद की संदर्भ तस्वीर','यह कैमरे में दर्ज सबूत नहीं' if a>=431.7 else '')
 raise RuntimeError(a)
out=O/'picture_a_v2.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 enc.stdin.write(frame(i/24).convert('RGB').tobytes())
 if i%240==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0
for c in caps.values():c.release()
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1489',.12,1.5,13,.022),('mk1430',.1,.4,36,.025),('mk1530',0,.5,93.1,.025)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss',str(START),'-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=[f'[1:a]atrim=duration={D},asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CONTINUATION_A_V2_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t',str(D),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CONTINUATION_A_V2_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
