#!/usr/bin/env python3
"""Evidence-driven explanatory revision, distinct original look, not Vox layouts."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import subprocess,math,imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01');S=P/'lemo_chapter_rebuild';O=P/'vox_explainer_work';O.mkdir(exist_ok=True);A=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi';F='/home/user/explainer-pipeline/assets/fonts/';ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1920,1080
hi=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',68);h2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',46);h3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',34);en=ImageFont.truetype(F+'Inter-Bold.ttf',52);serif=ImageFont.truetype(F+'IMFellEnglish-Italic.ttf',67);small=ImageFont.truetype(F+'Inter-Medium.ttf',23)
rtg=A/'sync_fix/doe_cutaway.png';peak=A/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg'; img=Image.open(rtg).convert('RGBA');plate=img.copy();plate.thumbnail((1030,715),Image.Resampling.LANCZOS);detail=img.crop((320,150,850,500));detail.thumbnail((580,370),Image.Resampling.LANCZOS)
peakbg=ImageOps.fit(Image.open(peak).convert('RGB'),(W,H),Image.Resampling.LANCZOS).convert('RGBA');peakbg=Image.alpha_composite(peakbg,Image.new('RGBA',(W,H),(7,17,21,175)))
def ease(x):x=min(1,max(0,x));return x*x*(3-2*x)
def label(d,s):d.text((68,1010),s,font=small,fill='#f0f0e8',stroke_width=2,stroke_fill='#091116')
def trace(d,points,progress,col='#eec173',width=5):
 q=ease(progress)*(len(points)-1)
 for i in range(len(points)-1):
  n=max(0,min(1,q-i));a,b=points[i],points[i+1]
  if n:d.line((a[0],a[1],a[0]+(b[0]-a[0])*n,a[1]+(b[1]-a[1])*n),fill=col,width=width)

def frame_power(t):
 im=Image.new('RGBA',(W,H),(12,24,29,255));slide=ease(t/.65);x=int(830+110*(1-slide));im.alpha_composite(plate,(x,145));d=ImageDraw.Draw(im);d.line((100,112,230,112),fill='#e7bb75',width=5)
 title='एक और चीज़' if t<2.9 else 'बिजली का सोर्स';d.text((100,165),title,font=hi,fill='#faf7ef');
 if t>=2.9:d.text((104,275),'RTG',font=en,fill='#e9bd7b')
 if t>=5.6:
  q=ease((t-5.6)/.6);d.text((102,395),'प्लूटोनियम',font=hi,fill=(255,210,139,int(255*q)));d.text((105,500),'रेडियोएक्टिव मटेरियल',font=h3,fill=(240,243,234,int(255*q)))
  im.alpha_composite(detail,(100,610));d=ImageDraw.Draw(im);d.rectangle((99,609,101+detail.width,611+detail.height),outline='#e7bb75',width=3);trace(d,[(x+plate.width*.52,570),(x+plate.width*.52,795),(100+detail.width,795)],(t-5.6)/1.1)
 label(d,'DOE CUTAWAY  ·  DIFFERENT RTG MODEL  ·  EXPLANATORY, NOT 1965 EQUIPMENT');return im

def frame_cache(t):
 im=peakbg.copy();d=ImageDraw.Draw(im);d.text((95,130),'मशीन बाँधकर छोड़ी',font=hi,fill='#fbf8ef',stroke_width=3,stroke_fill='#071116');
 if t>=2.1:d.text((100,245),'लौटने का इरादा था',font=h2,fill='#ebc894',stroke_width=2,stroke_fill='#071116')
 # Source quotation is typeset on a legible panel; not represented as an original scan.
 u=ease((t-.8)/.8);x=int(118+(1-u)*-90);d.rounded_rectangle((x,470,x+1250,725),radius=6,fill=(225,226,214,int(245*u)));d.text((x+45,500),'“lashed to the mountain”',font=serif,fill=(24,35,38,int(255*u)));d.text((x+48,630),'AMERICAN ALPINE CLUB  ·  ACCOUNT REVIEW',font=small,fill=(62,73,68,int(255*u)))
 if t>2.1:trace(d,[(x+45,596),(x+540,596)],(t-2.1)/.65,col='#a64d37',width=5)
 label(d,'MODERN NANDA DEVI PHOTOGRAPH  ·  QUOTATION TYPESET FROM SOURCE');return im

def frame_clue(t):
 im=Image.new('RGBA',(W,H),(15,27,33,255));d=ImageDraw.Draw(im);d.text((95,120),'1993 में एक सुराग?',font=hi,fill='#faf7ef');d.text((100,230),'कुछ हिस्से मिलने का दावा',font=h2,fill='#efd0a3');u=ease((t-.5)/.8);x=int(100+(1-u)*-80);d.rounded_rectangle((x,380,x+1430,700),radius=6,fill=(230,228,215,int(255*u)));d.text((x+55,425),'“only one aluminium box”',font=serif,fill=(26,35,37,int(255*u)));d.text((x+56,565),'THE WEEK  ·  PARTICIPANT ACCOUNT  ·  2026 REPORT',font=small,fill=(62,72,72,int(255*u)))
 if t>2:trace(d,[(x+55,525),(x+730,525)],(t-2)/.8,col='#b14d3c',width=6)
 if t>3.3:d.text((100,770),'पहचान का दावा, पक्का सबूत नहीं',font=h3,fill='#f1d5aa')
 label(d,'QUOTE FROM REPORT  ·  TYPESET  ·  NO PHOTOGRAPH OF THE RECOVERED OBJECT');return im

def frame_unknown(t):
 im=Image.new('RGBA',(W,H),(15,27,33,255));d=ImageDraw.Draw(im);d.text((95,120),'दो अलग बातें',font=hi,fill='#f7f5ec');
 d.text((115,340),'बाहरी हिस्सा',font=hi,fill='#f1d0a2');d.text((120,445),'मिलने का दावा',font=h3,fill='#e4e7dc')
 p=ease((t-.5)/.9);d.line((935,300,935,300+int(450*p)),fill='#afbeb4',width=3)
 if t>=1.25:
  d.text((1030,340),'फ्यूल कैप्सूल',font=hi,fill='#f1d0a2');d.text((1035,445),'मिलने की पुष्टि नहीं',font=h3,fill='#e4e7dc')
 label(d,'REPORTED EXTERNAL PARTS  ≠  CONFIRMED FUEL CAPSULE RECOVERY');return im

def make(name,n,func):
 out=O/(name+'.mp4');cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',str(out)];p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(n):p.stdin.write(func(i/24).convert('RGB').tobytes())
 p.stdin.close();assert p.wait()==0;print('completed',name,n,flush=True);return out
repl={'power':make('power',216,frame_power),'cache':make('cache',144,frame_cache),'clue':make('clue',152,frame_clue),'unknown':make('unknown',96,frame_unknown)}
order=['opening','map1','team','support','peak','map2','power','weather','retreat','cache','evidence','clue','unknown','closing'];parts=[repl.get(name,S/(name+'.mp4')) for name in order]
for p in parts:
 if not p.exists():raise FileNotFoundError(p)
(O/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts));pic=O/'picture.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy',str(pic)],check=True)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';out=P/'RAAZVIK_CHAPTER01_VISUAL_EXPLAINER_REVIEW.mp4';subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',voice,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True);print('DONE',out,flush=True)
