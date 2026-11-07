from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,math,json
P=Path('/home/user/RAAZVIK_PLAN_B/chapter05');A=P/'assets';O=P/'stable_map_render';O.mkdir(exist_ok=True);W,H=1280,720;N=732;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts');hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),43);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),31);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),29)
def txt(d,p,s,f=hi,fill='#faf7ed'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0c1720')
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,665,min(1240,b[2]+55),704),radius=4,fill=(7,22,27,220));txt(d,(38,668),s,small)
def fit(p):return ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)
sherpa=fit(A/'sherpas_nepal_2015.jpg');peak=fit(A/'nanda_outer_1980.jpg');porter=fit(A/'porter_nepal_2007.jpg');world=json.load(open('/home/user/explainer-pipeline/assets/world_110m.geojson'))
# Draw real Natural Earth land geometry, equirectangular view, not a literal journey path.
# Geographic relief from NASA GIBS; full-world 2:1 layer letterboxed without stretching.
rawmap=Image.open(A/'nasa_world_bluemarble.jpg').convert('RGB').resize((1280,640),Image.Resampling.LANCZOS)
mapim=Image.new('RGB',(1280,720),(8,23,31));mapim.paste(ImageEnhance.Brightness(rawmap).enhance(.76),(0,40))
def moved(im,t,dur):
 # No per-frame crop rounding or jitter on still photos.
 return im
def frame(t,raw):
 if t<3.5:
  im=ImageEnhance.Brightness(Image.frombytes('RGB',(W,H),raw)).enhance(.76).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(48,60),'पर्वतारोही और तकनीकी लोग',mid);foot(d,'लोबुचे, नेपाल  2023  सांकेतिक दृश्य');return im
 if t<7.5:
  im=ImageEnhance.Brightness(moved(sherpa,t-3.5,4)).enhance(.75).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(48,63),'शेरपा और स्थानीय पोर्टर',mid);foot(d,'नेपाल  2015  मिशन की तस्वीर नहीं');return im
 if t<15.75:
  q=t-7.5;im=mapim.convert('RGBA');d=ImageDraw.Draw(im);txt(d,(50,510),'भारत और अमेरिका की टीम',hi);txt(d,(50,566),'साथ ट्रेनिंग',mid,fill='#efc795')
  # Locations only: no invented flight, path, historical training footage, or expedition route.
  for x,y,name,delay in [(103,136,'अलास्का',.6),(921,287,'भारत',2.0)]:
   u=ease((q-delay)/.5)
   if u>0:
    r=int(7+u*4);d.ellipse((x-r,y-r,x+r,y+r),fill='#f0c48c');d.ellipse((x-19,y-19,x+19,y+19),outline='#f0c48c',width=2);txt(d,(x+20,y-25),name,mid)
  if q>4:txt(d,(50,615),'अमेरिका में प्रशिक्षण',small)
  foot(d,'स्रोत  अमेरिकी अल्पाइन जर्नल  2004  पुस्तक समीक्षा');return im
 if t<21.4:
  q=t-15.75;im=ImageEnhance.Brightness(moved(porter,q,5.65)).enhance(.70).convert('RGBA');d=ImageDraw.Draw(im);txt(d,(48,68),'अलग-अलग हिस्से',hi);txt(d,(48,128),'पहाड़ पर पहुँचाने थे',mid,fill='#edc591')
  # Animated three component labels denote separate loads, not actual mission hardware.
  labels=['उपकरण','सप्लाई','टीम']
  for i,label in enumerate(labels):
   u=ease((q-.6-i*.5)/.55)
   if u:
    x=45+i*285;y=int(470+35*(1-u));d.line((x,y,x+220,y),fill=(240,198,146,255),width=3);txt(d,(x,y+6),label,mid)
  foot(d,'नेपाल  2007  पोर्टर की संदर्भ तस्वीर');return im
 q=t-21.4;im=ImageEnhance.Brightness(moved(peak,5.65+q,15)).enhance(.48).convert('RGBA');d=ImageDraw.Draw(im)
 txt(d,(48,65),'लंबे समय तक काम',hi);txt(d,(48,128),'बिना बार-बार बैटरी बदले',mid,fill='#f0c99c')
 # Progress line represents continuous operation, not a claimed measurement of duration.
 d.line((80,370,1190,370),fill=(111,143,140),width=3);u=ease((q-1)/5);d.line((80,370,int(80+1110*u),370),fill=(239,199,151),width=6)
 for i in range(5):
  x=80+i*277;d.ellipse((x-5,365,x+5,375),fill=(241,217,188))
 if q>3:txt(d,(49,435),'पहाड़ पर बार-बार लौटना मुश्किल',mid)
 foot(d,'नंदा देवी  1980  समय-रेखा सांकेतिक');return im
clip=A/'lobuche_2023_clip.mp4';dec=subprocess.Popen([ff,'-v','error','-i',str(clip),'-vf','fps=24,scale=1280:720','-frames:v','84','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 raw=dec.stdout.read(W*H*3) if i<84 else None
 if i<84 and len(raw)!=W*H*3:raise ValueError('short input')
 enc.stdin.write(frame(i/24,raw).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0;dec.stdout.close();assert dec.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1157',.3,6,0,.035),('mk1489',.12,1.2,7.5,.05),('mk1530',0,.5,15.75,.05),('mk1430',.1,.4,21.4,.05)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','169.625','-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=['[1:a]atrim=duration=30.5,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER05_STABLE_MAP_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','30.5','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER05_STABLE_MAP_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
