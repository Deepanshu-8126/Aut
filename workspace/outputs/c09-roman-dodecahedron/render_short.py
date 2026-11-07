from pathlib import Path
from PIL import Image, ImageDraw, ImageFont,ImageOps,ImageFilter,ImageEnhance
import json,math,subprocess,random,os
import imageio_ffmpeg
P=Path('/home/user/outputs/c09-roman-dodecahedron');A=P/'assets';F=Path('/home/user/explainer-pipeline/assets/fonts');ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=540,960;fps=30;dur=31.8
font=lambda name,size:ImageFont.truetype(str(F/name),size)
head=font('Inter-Black.ttf',40);hsmall=font('Inter-Black.ttf',30);body=font('Inter-Bold.ttf',22);tiny=font('JetBrainsMono-Bold.ttf',14);micro=font('JetBrainsMono-Bold.ttf',11);capfont=font('Inter-Black.ttf',31)
thumb=Image.open(P/'thumbnail.jpg').convert('RGB');imgs={n:Image.open(A/(n+'_cc0.jpg')).convert('RGB') for n in ['lyon','bronze','vienne','tongeren']}
GOLD='#e9c07c';WHITE='#f7efdd';RED='#b54031';INK='#181c1b'
# Data-driven European map, Natural Earth 1:110m. Regional village marker only, not dig-site.
geo=json.loads(Path('/home/user/explainer-pipeline/assets/world_110m.geojson').read_text());
def map_image(region='europe'):
 im=Image.new('RGB',(W,620),'#172a2b');d=ImageDraw.Draw(im)
 if region=='europe':extent=(-15,35,35,64)
 else:extent=(-9,3,49,59)
 lon0,lon1,lat0,lat1=extent
 def xy(pt):return ((pt[0]-lon0)/(lon1-lon0)*W,(lat1-pt[1])/(lat1-lat0)*620)
 for ft in geo['features']:
  g=ft['geometry']; coords=[g['coordinates']] if g['type']=='Polygon' else g['coordinates'] if g['type']=='MultiPolygon' else []
  for poly in coords:
   if not poly:continue
   pts=[xy(a) for a in poly[0]]
   if len(pts)>2 and max(x for x,y in pts)-min(x for x,y in pts)<W*4:d.polygon(pts,fill='#597571',outline='#a9b0a0',width=1)
 if region!='europe':
  x,y=xy((-.67294,53.12155));d.ellipse((x-6,y-6,x+6,y+6),fill='#f2553d',outline=WHITE,width=2);d.line((x,y,x+58,y-43),fill='#efb883',width=2);d.text((x+60,y-61),'NORTON DISNEY',font=micro,fill=WHITE)
 return im
maps={'europe':map_image(),'england':map_image('england')}
# Words from audio-anchored Whisper alignment; text checked against the spoken script, not assumed perfect.
words=json.loads((P/'whisper_word_draft.json').read_text()); groups=[]
part=[]
for i,w in enumerate(words):
 part.append(w)
 boundary=len(part)==3 or w['word'].strip().endswith(('.', '?', '!')) or (i+1<len(words) and words[i+1]['start']-w['end']>.32)
 if boundary:
  groups.append((part[0]['start']+.22,part[-1]['end']+.22,part));part=[]
if part:groups.append((part[0]['start']+.22,part[-1]['end']+.22,part))
def fit(im,size):return ImageOps.fit(im,size,Image.Resampling.LANCZOS)
def textcenter(d,s,y,f,fill=WHITE,stroke=1):
 b=d.textbbox((0,0),s,font=f,stroke_width=stroke);d.text(((W-(b[2]-b[0]))/2,y),s,font=f,fill=fill,stroke_width=stroke,stroke_fill='#101919')
def bg(t):
 im=Image.new('RGB',(W,H),'#111b1b');d=ImageDraw.Draw(im)
 for y in range(0,H,5):
  c=17+int(5*math.sin(y/100));d.line((0,y,W,y),fill=(c,c+6,c+5),width=3)
 for x in range(25,W,35):d.line((x,0,x,H),fill='#283332',width=1)
 # film edges / not too dark
 for y in range(15,H,45):
  d.rounded_rectangle((5,y,15,y+23),radius=3,fill='#536058');d.rounded_rectangle((W-15,y,W-5,y+23),radius=3,fill='#536058')
 return im

def card(im,photo,box,t,offset=0):
 x,y,w,h=box;d=ImageDraw.Draw(im);d.rounded_rectangle((x+7,y+9,x+w+7,y+h+9),radius=5,fill='#050909');d.rounded_rectangle((x,y,x+w,y+h),radius=4,fill='#e5d7b9')
 # fixed-size picture with subtle pan and no repeating zoom
 inner=(w-20,h-48);pic=fit(photo,(inner[0]+20,inner[1]+20));xx=10+int(5*math.sin(t*.35+offset));yy=10+int(3*math.sin(t*.26+offset));pic=pic.crop((xx,yy,xx+inner[0],yy+inner[1]));im.paste(pic,(x+10,y+10));return x+10,y+10

def top(d,label):
 d.rounded_rectangle((35,48,505,94),radius=4,fill='#e4d5b6');d.text((49,60),label,font=tiny,fill='#202b2b')
def ribbon(d,s,y=725):
 d.rounded_rectangle((35,y,505,y+52),radius=3,fill='#c7ac79');d.text((49,y+15),s,font=tiny,fill='#1d2827')
def stamp(im,s,t,y=645):
 if t<0:return
 sc=1+max(0,0.3-t)*1.6; f=hsmall
 # font size remains stable on arrival; compact red file stamp
 d=ImageDraw.Draw(im);bb=d.textbbox((0,0),s,font=f);w=min(475,bb[2]-bb[0]+50);x=(W-w)//2
 d.rectangle((x,y,x+w,y+62),outline=RED,width=4);d.text((x+24,y+13),s,font=f,fill=RED,stroke_width=1)
def applycaps(im,t):
 for start,end,part in groups:
  if start<=t<end+0.12:
   ds=ImageDraw.Draw(im,'RGBA');txt=' '.join(z['word'].strip().upper() for z in part)
   bb=ds.textbbox((0,0),txt,font=capfont,stroke_width=2);tw=bb[2]-bb[0];f=capfont
   if tw>455:f=font('Inter-Black.ttf',max(20,int(31*455/tw)));bb=ds.textbbox((0,0),txt,font=f,stroke_width=2);tw=bb[2]-bb[0]
   x=(W-tw)//2;y=819;ds.rounded_rectangle((max(25,x-12),y-4,min(W-25,x+tw+12),y+50),radius=7,fill=(8,13,14,218))
   x0=x
   for z in part:
    token=z['word'].strip().upper();col=GOLD if z['start']+.22<=t<=z['end']+.22 else WHITE
    ds.text((x0,y),token,font=f,fill=col,stroke_width=1,stroke_fill='#080b0a');x0+=ds.textlength(token+' ',font=f)
   break

def frame(t):
 im=bg(t);d=ImageDraw.Draw(im)
 if t<2.7 or t>=28.1:
  # Selected illustrated cover breathes into the story; no simulated historical provenance.
  p=min(1,t/0.36) if t<2.7 else min(1,(t-28.1)/.4);z=.82+.18*p if t<2.7 else 1.0
  raw=ImageOps.contain(thumb,(W,810));w=int(raw.width*z);h=int(raw.height*z);raw=raw.resize((w,h));im.paste(raw,((W-w)//2,46+(810-h)//2));d=ImageDraw.Draw(im,'RGBA');d.text((35,873),'ILLUSTRATION  /  CASE FILE',font=micro,fill=(255,248,227,225))
 elif t<5.8:
  top(d,'EVIDENCE 01  /  ROMAN PERIOD');card(im,imgs['lyon'],(42,135,456,590),t);d=ImageDraw.Draw(im)
  # examine the original artifact closely with a tracked inspection ring
  r=28+7*math.sin(t*3);cx,cy=275,465;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#f2be73',width=3);d.line((cx+r,cy,cx+r+58,cy-65),fill='#f2be73',width=2);d.text((cx+r+25,cy-84),'HOLES',font=micro,fill=WHITE)
  ribbon(d,'LYON MUSEUM EXAMPLE  /  CC0',735)
 elif t<8:
  top(d,'THE QUESTION  /  CASE FILE');card(im,imgs['bronze'],(45,130,450,520),t);d=ImageDraw.Draw(im);stamp(im,'PURPOSE UNKNOWN',t-5.8,680)
 elif t<12.8:
  top(d,'EVIDENCE 02  /  EUROPE');im.paste(maps['europe'],(0,116));d=ImageDraw.Draw(im);d.rounded_rectangle((55,160,485,265),radius=5,fill='#e5d7b9');d.text((76,174),'100+',font=font('Inter-Black.ttf',62),fill=INK);d.text((255,196),'EXAMPLES',font=body,fill=INK)
  # Gentle scanning ring over region; not a specific discovery marker.
  q=(t-8)%2.5;r=20+q*25;d.ellipse((288-r,425-r,288+r,425+r),outline='#e5ad70',width=2)
  ribbon(d,'EUROPE  /  LOCATIONS VARY',735)
 elif t<18.72:
  top(d,'WORKING THEORIES  /  NOT PROVEN');
  if t<15.4:n='vienne';label='A  /  MEASURING TOOL'
  elif t<16.9:n='tongeren';label='B  /  KNITTING'
  else:n='bronze';label='C  /  RITUAL OBJECT'
  card(im,imgs[n],(42,130,456,520),t);d=ImageDraw.Draw(im);d.rounded_rectangle((35,676,505,744),radius=5,fill='#e8d8bb');d.text((48,691),label,font=body,fill=INK);d.text((48,716),'HYPOTHESIS ONLY',font=micro,fill='#a73c2b')
 elif t<20.68:
  top(d,'THE VERDICT  /  CASE FILE');card(im,imgs['tongeren'],(42,130,456,470),t);stamp(im,'NOT PROVEN',t-18.72,650)
 elif t<24.5:
  top(d,'2023  /  ENGLAND');im.paste(maps['england'],(0,116));d=ImageDraw.Draw(im);q=(t-20.68)%2;r=12+q*24;x,y=374,480;d.ellipse((x-r,y-r,x+r,y+r),outline='#e9b879',width=2);d.rounded_rectangle((32,562,508,683),radius=5,fill='#e8d9bd');d.text((49,579),'AN INTACT FIND',font=hsmall,fill=INK);d.text((49,627),'NORTON DISNEY REGION',font=tiny,fill=INK);ribbon(d,'MAP PIN = VILLAGE, NOT DIG SITE',735)
 elif t<27.6:
  top(d,'WHY THE LOCATION MATTERS');card(im,imgs['lyon'],(42,130,456,430),t);d=ImageDraw.Draw(im);d.rounded_rectangle((35,595,505,700),radius=4,fill='#e7d8b9');d.text((49,611),'ARCHAEOLOGICAL',font=body,fill=INK);d.text((49,648),'CONTEXT',font=hsmall,fill=INK);ribbon(d,'MUSEUM EXAMPLE  /  NOT THE FIND',735)
 else:
  top(d,'THE QUESTION REMAINS');card(im,imgs['lyon'],(42,130,456,520),t);stamp(im,'WHAT WAS IT?',t-27.6,680)
 applycaps(im,t);return im

# Previews from the real frame function, for continuity, overflow and factual-label QC.
checks=[.4,2.9,5.9,8.8,11.2,13.8,15.8,17.4,19.1,21.2,24,27,29.3,31];sheet=Image.new('RGB',(270*4,500*4),'#101818');sd=ImageDraw.Draw(sheet)
for i,t in enumerate(checks):
 q=frame(t);q.thumbnail((270,480));x=(i%4)*270;y=(i//4)*500;sheet.paste(q,(x,y));sd.text((x+5,y+481),str(t),fill='white')
sheet.save(P/'frame_contact.jpg',quality=90)
if os.environ.get('PROBE')=='1':print('probe ready');raise SystemExit
out=P/'picture_c09.mp4';cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','3',str(out)];enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(dur*fps)):
 enc.stdin.write(frame(i/fps).tobytes())
 if i%150==0:print('frame',i,flush=True)
enc.stdin.close();assert enc.wait()==0
print('PICTURE COMPLETE',flush=True)
