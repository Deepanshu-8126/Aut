#!/usr/bin/env python3
"""Cold War chapter; real period context, matched to continuous approved master. Review only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import imageio_ffmpeg,subprocess,math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter02');A=P/'assets';O=P/'render_work';O.mkdir(exist_ok=True);F=Path('/home/user/explainer-pipeline/assets/fonts');ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1280,720;FPS=24;N=999
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),42);med=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),31);sm=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),21);num=ImageFont.truetype(str(F/'Inter-Black.ttf'),85);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),32)
images={k:Image.open(A/f).convert('RGB') for k,f in [('asia','asia_nasa_map.jpg'),('cold','john_nikita_1961.jpg'),('lop','lop_nur_20oct1964.png'),('india','nehru_galbraith_1962.jpg'),('camera','corona_camera.jpg')]}
def fit(im,size):return ImageOps.fit(im,size,Image.Resampling.LANCZOS)
base=fit(images['asia'],(W,H));base=ImageEnhance.Brightness(base).enhance(.51)
def ease(x):x=max(0.,min(1.,x));return x*x*(3-2*x)
def txt(d,xy,s,font,fill='#f7f5eb',stroke=1):d.text(xy,s,font=font,fill=fill,stroke_width=stroke,stroke_fill='#0a1519')
def foot(d,s):
 bb=d.textbbox((0,0),s,font=sm,stroke_width=1);d.rounded_rectangle((33,665,55+bb[2],704),radius=5,fill=(8,18,22,215));txt(d,(42,670),s,sm,stroke=1)
def backdrop(z=1.0):
 im=base
 if z>1:
  cw=int(W/z);ch=int(H/z);im=im.crop(((W-cw)//2,(H-ch)//2,(W+cw)//2,(H+ch)//2)).resize((W,H),Image.Resampling.BILINEAR)
 return im.convert('RGBA')
def card(img,box,t):
 x,y,w,h=box; im=fit(img,(w,h)).convert('RGBA');p=ease(t/.65);x=int(x+(1-p)*65);return im,(x,y)
# Photos are genuinely dated context; no visual asserts 1961 leaders were leaders in Oct 1964.
def frame(t):
 if t<3:
  im=backdrop(1+.03*ease(t/3));d=ImageDraw.Draw(im);txt(d,(78,105),'कहानी की शुरुआत',med);txt(d,(75,190),'1964',num,fill='#f2cd95');d.line((80,320,80+int(300*ease(t/1.0)),320),fill='#dfb273',width=4);foot(d,'आधुनिक सैटेलाइट तस्वीर');return im
 if t<13:
  q=t-3;im=backdrop(1.02);photo,pos=card(images['cold'],(90,145,750,555),q);im.alpha_composite(photo,pos);d=ImageDraw.Draw(im);txt(d,(890,150),'कोल्ड वॉर',hi);txt(d,(890,245),'अमेरिका',med,fill='#ecc894');
  if q>1.0:txt(d,(890,325),'सोवियत संघ',med,fill='#ecc894')
  if q>5.5:txt(d,(890,470),'हथियारों की',med);txt(d,(890,520),'दौड़',med)
  foot(d,'केनेडी और ख्रुश्चेव  वियना, 1961');return im
 if t<17:
  q=t-13;im=backdrop(1+.04*ease(q/4));d=ImageDraw.Draw(im);txt(d,(75,90),'16 अक्टूबर 1964',hi,fill='#efcd96');
  if q>.7:txt(d,(75,165),'चीन का पहला',hi);txt(d,(75,220),'परमाणु परीक्षण',hi)
  # Broad Lop Nur marker on NASA plate; no precise blast point asserted.
  x=(88.5-60)/50*W;y=(48.125-42.58)/28.125*H;d.ellipse((x-6,y-6,x+6,y+6),fill='#edbf7e');r=25+14*ease(q);d.ellipse((x-r,y-r,x+r,y+r),outline='#edbf7e',width=3);txt(d,(x+35,y-32),'लोप नूर क्षेत्र',sm,fill='#ffdeac');foot(d,'आधुनिक सैटेलाइट तस्वीर  स्थान लगभग');return im
 if t<24:
  q=t-17;im=Image.new('RGBA',(W,H),(13,25,30,255));# historic satellite image in its own frame, then focus movement, not simulated explosion
  photo=fit(images['lop'],(995,625));z=1+.04*ease(q/7);cw=int(995/z);ch=int(625/z);photo=photo.crop(((995-cw)//2,(625-ch)//2,(995+cw)//2,(625+ch)//2)).resize((995,625),Image.Resampling.BILINEAR).convert('RGBA');x=int(45-(1-ease(q/.7))*60);im.alpha_composite(photo,(x,47));d=ImageDraw.Draw(im);txt(d,(1062,130),'लोप',med);txt(d,(1062,176),'नूर',med);txt(d,(1060,255),'1964',en,fill='#edc58c');
  if q>1:
   u=ease((q-1)/.8);xx=x+720;yy=260;d.line((xx-28,yy,xx+int(135*u),yy),fill='#e1b679',width=3);d.ellipse((xx-8,yy-8,xx+8,yy+8),outline='#e1b679',width=3)
  foot(d,'परीक्षण क्षेत्र की सैटेलाइट तस्वीर  20 अक्टूबर 1964');return im
 if t<33:
  q=t-24;im=backdrop(1.02);photo,pos=card(images['india'],(70,100,770,600),q);im.alpha_composite(photo,pos);d=ImageDraw.Draw(im);txt(d,(885,130),'भारत और चीन',hi);txt(d,(885,210),'1962 का युद्ध',med,fill='#edc58c');
  if q>3.5:txt(d,(885,340),'भारत की',med);txt(d,(885,390),'अपनी चिंता',med)
  foot(d,'नेहरू और अमेरिकी राजदूत गैलब्रेथ  1962');return im
 if t<38:
  q=t-33;im=backdrop(1+.05*ease(q/5));d=ImageDraw.Draw(im);txt(d,(75,100),'जानकारी जुटाना',hi);txt(d,(75,170),'आसान नहीं था',hi,fill='#edc58c');
  # broad labels only, no disputed boundary or claimed line-of-sight
  txt(d,(430,490),'भारत',med,fill='#f3d09b');txt(d,(870,175),'चीन',med,fill='#f3d09b');foot(d,'आधुनिक सैटेलाइट तस्वीर');return im
 q=t-38;im=Image.new('RGBA',(W,H),(13,25,30,255));photo,pos=card(images['camera'],(95,75,570,570),q);im.alpha_composite(photo,pos);d=ImageDraw.Draw(im);txt(d,(735,125),'उस दौर की',hi);txt(d,(735,190),'सैटेलाइट तकनीक',hi);txt(d,(735,315),'कोरोना कैमरा',med,fill='#eac48d');foot(d,'कैमरा सिस्टम का चित्र  1963–69');return im

out=O/'picture.mp4';cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(N):
 proc.stdin.write(frame(i/FPS).convert('RGB').tobytes())
 if i%240==0:print('frame',i,'/',N,flush=True)
proc.stdin.close();assert proc.wait()==0
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';sfx=Path('/home/user/explainer-pipeline/assets/sfx')
# name, leading trim, duration, chapter-time, gain; quiet, intentionally no boom.
cues=[('mk1489',.12,1.4,0,.09),('mk1104',0,.38,3,.075),('mk1143',.19,1.1,13,.065),('mk1430',.10,.40,17,.08),('mk1530',0,.5,24,.08),('mk1489',.12,1.4,33,.075)]
cmd=[ff,'-v','error','-y','-i',str(out),'-ss','74','-i',voice]
for n,*_ in cues:cmd+=['-i',str(sfx/(n+'.mp3'))]
f=['[1:a]atrim=duration=41.625,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for i,(n,tr,dur,at,g) in enumerate(cues):
 f.append(f'[{i+2}:a]atrim=start={tr}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={g},afade=t=out:st={dur-.15}:d=0.15,adelay={int(at*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]')
final=P/'RAAZVIK_CHAPTER02_COLD_WAR_REVIEW.mp4';cmd+=['-filter_complex',';'.join(f),'-map','0:v','-map','[mix]','-t','41.625','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)];subprocess.run(cmd,check=True)
mobile=P/'RAAZVIK_CHAPTER02_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(final),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)],check=True);print('DONE',final,mobile,flush=True)
