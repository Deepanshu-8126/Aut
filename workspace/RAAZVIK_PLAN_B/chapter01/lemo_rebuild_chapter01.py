#!/usr/bin/env python3
"""Source-led Chapter 1 review; deterministic time, real source plates, no AI footage. NOT FINAL."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,imageio_ffmpeg,math
D=Path('/home/user/RAAZVIK_PLAN_B/chapter01'); A=D/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi'; B=D/'assets/nanda_search_images';O=D/'lemo_chapter_rebuild';O.mkdir(exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1920,1080;F='/home/user/explainer-pipeline/assets/fonts/'
h1=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',68);h2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',44);h3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',33); en=ImageFont.truetype(F+'Inter-Black.ttf',105); mono=ImageFont.truetype(F+'Inter-Medium.ttf',23)
nanda=A/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg';gorson=B/'site-commons-wikimedia-org-nanda-devi-pe-4.jpg';ranikhet=B/'site-commons-wikimedia-org-nanda-devi-fi-4.jpg'; kohli=A/'cold_war_chapter/assets/kohli_2015.jpg';port=A/'cold_war_chapter/assets/nepal_porters_1997_john_pavelka.jpg';rtg=A/'sync_fix/doe_cutaway.png';doc=A/'visual_upgrade/FRUS_1978_official_page_capture.png';nasa=D/'assets/nasa_blue_marble_himalaya.jpg';large=D/'assets/nasa_india_wide.jpg'
panch=D/'RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/visual_upgrade/assets/panchachuli_pexels_36907717.mp4';cloud=A/'visual_upgrade/assets/machhapuchchhre_pexels_14372030.mp4';climber=A/'visual_upgrade/assets/climber_pexels_12050237.mp4'
for f in [nanda,gorson,ranikhet,kohli,port,rtg,doc,nasa,large,panch,cloud,climber]:
 if not f.exists():raise FileNotFoundError(f)
img={p:Image.open(p).convert('RGB') for p in [nanda,gorson,ranikhet,kohli,port,rtg,doc,nasa,large]}
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def backdrop(path,t,brightness=.72):
 im=ImageOps.fit(img[path],(W,H),Image.Resampling.LANCZOS,centering=(.5,.5)); z=1+.025*ease(t/5);cw=int(W/z);ch=int(H/z);im=im.crop(((W-cw)//2,(H-ch)//2,(W+cw)//2,(H+ch)//2)).resize((W,H),Image.Resampling.BICUBIC);return ImageEnhance.Brightness(im).enhance(brightness).convert('RGBA')
def text(d,xy,s,font,fill='#f6f3ed',stroke=2):d.text(xy,s,font=font,fill=fill,stroke_width=stroke,stroke_fill='#091319')
def lbl(d,s):text(d,(64,1010),s,mono,fill='#eef0e9',stroke=3)
def line(d,xy,w):x,y=xy;d.line((x,y,x+w,y),fill='#deab5f',width=5)
def fitpanel(path, maxsize):
 im=img[path].copy();im.thumbnail(maxsize,Image.Resampling.LANCZOS);return im.convert('RGBA')
portrait=fitpanel(kohli,(480,640));porters=fitpanel(port,(1000,620));device=fitpanel(rtg,(1000,780));official=img[doc].crop((0,0,1232,530)).convert('RGBA');official.thumbnail((1160,560),Image.Resampling.LANCZOS)
# Traceable scene schedule; both names and timing are provisional to human ear.
# Durations are in frames at 24 fps and sum to exactly 1776.
scenes=[('opening',77),('map1',67),('team',72),('support',120),('peak',96),('map2',144),('power',216),('weather',144),('retreat',72),('cache',144),('evidence',150),('clue',152),('unknown',96),('closing',226)]
assert sum(n for _,n in scenes)==1776

def draw_scene(name,t):
 if name in ('map1','map2'):
  path=large if name=='map1' else nasa;base=img[path];z=1+(.08 if name=='map1' else .04)*ease(t/(2.8 if name=='map1' else 6));cw=int(W/z);ch=int(H/z)
  if name=='map1':px=(79.97012-60)/46*W;py=(37.875-30.37608)/25.875*H
  else:px=(79.97012-70)/25*W;py=(38.0625-30.37608)/14.0625*H
  x=max(0,min(W-cw,int(W/2-cw/2+(px-W/2)*.12)));y=max(0,min(H-ch,int(H/2-ch/2+(py-H/2)*.12)));im=base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA');im=Image.alpha_composite(im,Image.new('RGBA',(W,H),(8,15,19,75)));d=ImageDraw.Draw(im);mx=(px-x)*W/cw;my=(py-y)*H/ch;d.ellipse((mx-11,my-11,mx+11,my+11),fill='#ffca80');prog=ease((t-.15)/.7);d.arc((mx-32,my-32,mx+32,my+32),-90,-90+360*prog,fill='#ffca80',width=4);text(d,(mx+45,my-67),'नंदा देवी',h3)
  if name=='map1':text(d,(80,110),'एक सीक्रेट मिशन',h1);text(d,(83,215),'उत्तराखंड',h2,fill='#eecb98')
  else:
   text(d,(80,110),'मशीन पहाड़ पर' if t<3 else 'चीन के मिसाइल सिग्नल',h1);text(d,(83,215),'प्लान' if t<3 else 'सुनने की कोशिश',h2,fill='#eecb98')
   if t>=3:
    for k in range(2):
     a=(t-3+k*.65)%1.7;r=44+a*85;d.arc((mx-r,my-r,mx+r,my+r),-60,80,fill='#eab26b',width=4)
  lbl(d,'NASA / GIBS  ·  MODERN SATELLITE IMAGERY  ·  MARKER APPROXIMATE');return im
 if name=='team':
  im=backdrop(nasa,t,.26);u=ease(t/.65); x=int(130-(1-u)*100);im.alpha_composite(portrait,(x,180));d=ImageDraw.Draw(im);text(d,(760,175),'भारतीय और अमेरिकी',h1);text(d,(760,270),'climbers',ImageFont.truetype(F+'Inter-Bold.ttf',52),fill='#efc384');line(d,(760,390),int(300*ease((t-.45)/.65)));text(d,(760,435),'एम. एस. कोहली',h2);text(d,(762,505),'मिशन लीडर',h3,fill='#e1c696');lbl(d,'PMO / PIB  ·  PORTRAIT PHOTOGRAPHED IN 2015');return im
 if name=='support':
  im=backdrop(nasa,t,.25);u=ease(t/.75);x=int(160-(1-u)*90);im.alpha_composite(porters,(x,200));d=ImageDraw.Draw(im);text(d,(1230,285),'टीम के',h1);text(d,(1230,385),'सहयोगी',h1);line(d,(1235,490),int(180*ease(t)));lbl(d,'ILLUSTRATIVE PORTERS  ·  NEPAL 1997  ·  NOT THE 1965 TEAM');return im
 if name=='peak':
  im=backdrop(gorson,t,.79);d=ImageDraw.Draw(im);text(d,(95,115),'नंदा देवी',h1);text(d,(97,220),'मशीन पहाड़ की ओर',h2,fill='#f1d3a5');lbl(d,'NANDA DEVI  ·  MODERN PHOTOGRAPH');return im
 if name=='power':
  im=Image.new('RGBA',(W,H),(13,25,31,255));off=ease(t/.7);x=int(840+(1-off)*130);im.alpha_composite(device,(x,150));d=ImageDraw.Draw(im);line(d,(90,120),140);text(d,(90,170),'पावर का सोर्स',h1);text(d,(95,280),'RTG',ImageFont.truetype(F+'Inter-Bold.ttf',54),fill='#f0c27e');
  if t>=5.6: text(d,(95,445),'प्लूटोनियम',h1,fill='#ffcf8b');text(d,(96,540),'रेडियोएक्टिव मटेरियल',h3)
  # Conceptual visual callout appears only when plutonium is mentioned; it does not label an exact 1965 component.
  if t>=5.6:
   p=ease((t-5.6)/.8);d.line((780,585,780+int(120*p),585),fill='#e9bc79',width=5);d.ellipse((x+device.width//2-38,505,x+device.width//2+38,581),outline='#e9bc79',width=4)
   inset=img[rtg].crop((320,150,850,500)).convert('RGBA'); inset.thumbnail((530,320)); im.alpha_composite(inset,(95,650));d=ImageDraw.Draw(im);d.rectangle((94,649,96+inset.width,651+inset.height),outline='#e9bc79',width=3)
  lbl(d,'DOE RTG EXAMPLE  ·  DIFFERENT MODEL  ·  GRAPHIC IS EXPLANATORY');return im
 if name=='cache':
  im=backdrop(nanda,t,.4);d=ImageDraw.Draw(im);text(d,(95,110),'मशीन बाँधकर छोड़ी',h1);text(d,(95,220),'टीम लौट गई',h2,fill='#f1d0a0');
  if t>2.4:
   line(d,(98,425),int(510*ease((t-2.4)/1)));text(d,(98,465),'वापस आने का इरादा था',h2)
  lbl(d,'CONTEXT: AMERICAN ALPINE CLUB ACCOUNT  ·  MODERN NANDA DEVI PHOTO');return im
 if name=='evidence':
  im=backdrop(nasa,t,.31);d=ImageDraw.Draw(im);text(d,(85,110),'अगले साल टीम लौटी',h1);text(d,(88,215),'मशीन नहीं मिली',h1,fill='#f3cc91'); u=ease((t-.3)/.8);x=int(680+(1-u)*120);y=340;panel=official.copy();mark=Image.new('RGBA',panel.size);w=int(485*ease((t-2)/.8));
  if w>0:ImageDraw.Draw(mark).rectangle((545,297,545+w,331),fill=(255,202,105,75))
  im.alpha_composite(Image.alpha_composite(panel,mark),(x,y));d=ImageDraw.Draw(im);text(d,(x,y-55),'US STATE DEPARTMENT  ·  14 APRIL 1978',mono);text(d,(x,y+panel.height+22),'OFFICIAL WEBSITE TRANSCRIPTION  ·  NOT ORIGINAL PAPER',mono);return im
 if name=='clue':
  im=backdrop(ranikhet,t,.35);d=ImageDraw.Draw(im);text(d,(96,120),'1993 में एक सुराग?',h1);text(d,(100,230),'कुछ बाहरी हिस्सों का दावा',h2,fill='#f2ce9c');line(d,(100,350),int(520*ease((t-.3)/1))); 
  if t>1.6:text(d,(100,395),'पहचान अभियान से जुड़े लोगों के अनुसार',h3)
  if t>3.4:text(d,(100,480),'पक्की पहचान अलग सवाल है',h3)
  lbl(d,'SOURCE: THE WEEK  ·  REPORTED IN 2026  ·  NO OBJECT PHOTO SHOWN');return im
 if name=='unknown':
  im=backdrop(nasa,t,.22);d=ImageDraw.Draw(im);text(d,(100,140),'क्या मिला?',h1);text(d,(105,280),'बाहरी हिस्सों का दावा',h2,fill='#edcc96');d.line((100,390,1050,390),fill='#8a9a94',width=3);text(d,(105,455),'फ्यूल कैप्सूल',h1);text(d,(105,560),'मिलने की पुष्टि नहीं',h2,fill='#efcb94');lbl(d,'PARTICIPANT ACCOUNTS  ·  CAPSULE RECOVERY NOT ESTABLISHED');return im
 if name=='closing':
  im=backdrop(nanda,t,.58);d=ImageDraw.Draw(im);text(d,(90,125),'मशीन यहाँ पहुँची कैसे?',h1);line(d,(95,260),int(270*ease(t/.8)));
  if t>3.0:text(d,(95,320),'पूरी कहानी',h2,fill='#f1ca8e')
  lbl(d,'NANDA DEVI  ·  MODERN PHOTOGRAPH');return im
 raise ValueError(name)

def overlay_video_frame(name,raw,t):
 im=Image.frombytes('RGB',(W,H),raw).convert('RGBA');d=ImageDraw.Draw(im)
 if name=='opening':
  text(d,(85,110),'1965',en);text(d,(90,245),'भारत के हिमालय में',h1);lbl(d,'ILLUSTRATIVE MODERN VIDEO  ·  PANCHACHULI, UTTARAKHAND')
 elif name=='weather':
  text(d,(85,110),'मौसम बिगड़ गया',h1);lbl(d,'ILLUSTRATIVE MODERN WEATHER  ·  NEPAL  ·  NOT THE 1965 STORM')
 else:
  text(d,(85,110),'टीम को लौटना पड़ा',h1);lbl(d,'ILLUSTRATIVE MODERN CLIMBER  ·  NOT THE 1965 TEAM')
 return im

def render_scene(name,n):
 out=O/(name+'.mp4');encoder=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 source={'opening':panch,'weather':cloud,'retreat':climber}.get(name);decoder=None
 if source:decoder=subprocess.Popen([ff,'-v','error','-i',str(source),'-vf','scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24','-frames:v',str(n),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
 try:
  for i in range(n):
   if decoder:
    data=decoder.stdout.read(W*H*3)
    if len(data)!=W*H*3:raise RuntimeError('video source ended early '+name+' '+str(i))
    frame=overlay_video_frame(name,data,i/24)
   else:frame=draw_scene(name,i/24)
   encoder.stdin.write(frame.convert('RGB').tobytes())
  encoder.stdin.close();assert encoder.wait()==0
  if decoder:decoder.stdout.close();assert decoder.wait()==0
 except BaseException:
  encoder.kill()
  if decoder:decoder.kill()
  raise
 print('scene',name,'frames',n,flush=True);return out
parts=[render_scene(name,n) if name in ('power','cache') or not (O/(name+'.mp4')).exists() else O/(name+'.mp4') for name,n in scenes];(O/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts));pic=O/'picture.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy',str(pic)],check=True)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';out=D/'RAAZVIK_CHAPTER01_LEMO_EVIDENCE_REVIEW_NOT_FINAL.mp4';subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',voice,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True);print('DONE',out,flush=True)
