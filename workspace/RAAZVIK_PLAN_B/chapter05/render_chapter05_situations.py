from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,math,json
P=Path('/home/user/RAAZVIK_PLAN_B/chapter05');A=P/'assets';O=P/'situation_render';O.mkdir(exist_ok=True);W,H=1280,720;N=732;ff=imageio_ffmpeg.get_ffmpeg_exe();F=Path('/home/user/explainer-pipeline/assets/fonts');hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),43);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),31);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),29)
def txt(d,p,s,f=hi,fill='#faf7ed'):d.text(p,s,font=f,fill=fill,stroke_width=2,stroke_fill='#0c1720')
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((30,665,min(1240,b[2]+55),704),radius=4,fill=(7,22,27,220));txt(d,(38,668),s,small)
def fit(p):return ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.Resampling.LANCZOS)
sherpa=fit(A/'sherpas_nepal_2015.jpg');peak=fit(A/'nanda_outer_1980.jpg');porter=fit(A/'porter_nepal_2007.jpg');loadimg=fit(A/'generated_equipment_load.png');camera=fit(A/'generated_camera.png');station=fit(A/'generated_generic_station.png');battery=fit(A/'generated_battery_climb.png');world=json.load(open('/home/user/explainer-pipeline/assets/world_110m.geojson'))
# Draw real Natural Earth land geometry, equirectangular view, not a literal journey path.
# Geographic relief from NASA GIBS; full-world 2:1 layer letterboxed without stretching.
rawmap=Image.open(A/'nasa_world_bluemarble.jpg').convert('RGB').resize((1280,640),Image.Resampling.LANCZOS)
mapim=Image.new('RGB',(1280,720),(8,23,31));mapim.paste(ImageEnhance.Brightness(rawmap).enhance(.76),(0,40))
def moved(im,t,dur):
 # No per-frame crop rounding or jitter on still photos.
 return im
def frame(t,raw):
 if t<4.88:
  im=ImageEnhance.Brightness(Image.frombytes('RGB',(W,H),raw)).enhance(.76).convert('RGBA');d=ImageDraw.Draw(im);
  if t<2.85:txt(d,(48,60),'पर्वतारोही और तकनीकी लोग',mid)
  else:txt(d,(48,60),'टीम में भारतीय पर्वतारोही भी',mid)
  foot(d,'लोबुचे, नेपाल  2023  सांकेतिक दृश्य');return im
 if t<7.5:
  im=ImageEnhance.Brightness(moved(sherpa,t-3.5,4)).enhance(.75).convert('RGBA');d=ImageDraw.Draw(im);
  if t>=4.88:txt(d,(48,63),'शेरपा और स्थानीय पोर्टर',mid)
  foot(d,'नेपाल  2015  मिशन की तस्वीर नहीं');return im
 if t<17.2:
  im=mapim.convert('RGBA');d=ImageDraw.Draw(im)
  # Captions follow the spoken words; first is source, then training in America, then return to India.
  if t<10.5:
   txt(d,(50,510),'अमेरिकी अल्पाइन जर्नल',hi);txt(d,(50,566),'एक प्रकाशित विवरण',mid,fill='#efc795')
  elif t<11.8:
   txt(d,(50,510),'दोनों देशों के लोग',hi);txt(d,(50,566),'साथ प्रशिक्षण',mid,fill='#efc795')
  elif t<14.46:
   x,y=103,136;d.ellipse((x-11,y-11,x+11,y+11),fill='#f0c48c');d.ellipse((x-19,y-19,x+19,y+19),outline='#f0c48c',width=2);txt(d,(x+20,y-25),'अमेरिका',mid)
   txt(d,(50,510),'अमेरिका में',hi);txt(d,(50,566),'साथ ट्रेनिंग',mid,fill='#efc795')
  else:
   x,y=921,287;d.ellipse((x-11,y-11,x+11,y+11),fill='#f0c48c');d.ellipse((x-19,y-19,x+19,y+19),outline='#f0c48c',width=2);txt(d,(x+20,y-25),'भारत',mid)
   txt(d,(50,510),'इसके बाद भारत लौटे',hi);txt(d,(50,566),'मिशन की तैयारी',mid,fill='#efc795')
  foot(d,'स्रोत  अमेरिकी अल्पाइन जर्नल  2004  पुस्तक समीक्षा');return im
 if t<21.04:
  q=t-17.2;im=ImageEnhance.Brightness(loadimg).enhance(.8).convert('RGBA');d=ImageDraw.Draw(im)
  if t>=18.34:txt(d,(48,60),'अलग-अलग हिस्से',mid)
  if t>=19.72:txt(d,(48,116),'पहाड़ तक पहुँचाने थे',mid,fill='#edc591')
  foot(d,'एआई से बना सांकेतिक दृश्य  असली टीम नहीं');return im
 if t<24.05:
  im=ImageEnhance.Brightness(camera).enhance(.72).convert('RGBA');d=ImageDraw.Draw(im)
  if t>=21.68:txt(d,(45,70),'सिर्फ एक तस्वीर',hi);txt(d,(45,132),'लेने के लिए नहीं',mid,fill='#edc591')
  foot(d,'एआई से बना सांकेतिक दृश्य');return im
 if t<27.98:
  im=ImageEnhance.Brightness(station).enhance(.72).convert('RGBA');d=ImageDraw.Draw(im)
  if t>=24.5:txt(d,(760,65),'लंबे समय तक',mid);txt(d,(760,112),'अकेले काम',mid,fill='#edc591')
  # A short timeline adds the passage-of-time idea; no claim about exact operating duration.
  if t>=25.24:
   u=ease((t-25.24)/2.3);d.line((760,215,1180,215),fill=(125,150,153),width=3);d.line((760,215,int(760+420*u),215),fill=(237,196,146),width=5)
  foot(d,'एआई सांकेतिक दृश्य  असली मशीन नहीं');return im
 q=t-27.98;im=ImageEnhance.Brightness(battery).enhance(.72).convert('RGBA');d=ImageDraw.Draw(im)
 if t>=28.68:txt(d,(48,62),'बैटरी बदलने जाना',hi);txt(d,(48,125),'इस ऊँचाई पर मुश्किल',mid,fill='#edc591')
 foot(d,'एआई से बना सांकेतिक दृश्य  वास्तविक घटना नहीं');return im
clip=A/'lobuche_2023_clip.mp4';dec=subprocess.Popen([ff,'-v','error','-i',str(clip),'-vf','fps=24,scale=1280:720','-frames:v','118','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
out=O/'picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
for i in range(N):
 raw=dec.stdout.read(W*H*3) if i<118 else None
 if i<118 and len(raw)!=W*H*3:raise ValueError('short input')
 enc.stdin.write(frame(i/24,raw).convert('RGB').tobytes())
 if i%120==0:print('frame',i,'/',N,flush=True)
enc.stdin.close();assert enc.wait()==0;dec.stdout.close();assert dec.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';S=Path('/home/user/explainer-pipeline/assets/sfx');cues=[('mk1157',.3,6,0,.035),('mk1489',.12,1.2,7.5,.05),('mk1530',0,.5,17.2,.05),('mk1430',.1,.4,21.04,.05)];cmd=[ff,'-v','error','-y','-i',str(out),'-ss','169.625','-i',voice]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=['[1:a]atrim=duration=30.5,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]');final=P/'RAAZVIK_CHAPTER05_SITUATION_HD.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','30.5','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER05_SITUATION_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',flush=True)
