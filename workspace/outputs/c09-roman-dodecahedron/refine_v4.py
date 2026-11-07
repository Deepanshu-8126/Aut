from pathlib import Path
from PIL import Image, ImageDraw, ImageFont,ImageOps,ImageFilter,ImageEnhance
import json,math,subprocess,random,os
import imageio_ffmpeg
P=Path('/home/user/outputs/c09-roman-dodecahedron');A=P/'assets';F=Path('/home/user/explainer-pipeline/assets/fonts');ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=540,960;fps=30;dur=31.8
font=lambda name,size:ImageFont.truetype(str(F/name),size)
head=font('Inter-Black.ttf',40);hsmall=font('Inter-Black.ttf',30);body=font('Inter-Bold.ttf',22);tiny=font('JetBrainsMono-Bold.ttf',14);micro=font('JetBrainsMono-Bold.ttf',11);capfont=font('Inter-Black.ttf',31)
thumb=Image.open(P/'thumbnail.jpg').convert('RGB');imgs={n:Image.open(A/(n+'_cc0.jpg')).convert('RGB') for n in ['lyon','bronze','vienne','tongeren']};imgs['knitting']=Image.open(A/'knitting_context.png').convert('RGB');imgs['dig']=Image.open(A/'archaeology_context.png').convert('RGB')
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


def cover_zoom(photo,t,ratio=1.0,fx=.5,fy=.5):
 scale=max(W/photo.width,H/photo.height)*ratio;pic=photo.resize((int(photo.width*scale),int(photo.height*scale)),Image.Resampling.BILINEAR);maxx=pic.width-W;maxy=pic.height-H;return pic.crop((int(maxx*fx),int(maxy*fy),int(maxx*fx)+W,int(maxy*fy)+H))
def overlay_black(im,a=85):
 q=Image.new('RGBA',im.size,(5,9,10,a));return Image.alpha_composite(im.convert('RGBA'),q).convert('RGB')
def title(d,s,y,size=42,color=WHITE):
 f=font('Inter-Black.ttf',size);b=d.textbbox((0,0),s,font=f,stroke_width=2)
 if b[2]>480:f=font('Inter-Black.ttf',max(22,int(size*480/b[2])));b=d.textbbox((0,0),s,font=f,stroke_width=2)
 d.text(((W-b[2])//2,y),s,font=f,fill=color,stroke_width=3,stroke_fill='#101313')
def locator(photo,px,py,ratio,fx,fy):
 scale=max(W/photo.width,H/photo.height)*ratio;pw=int(photo.width*scale);ph=int(photo.height*scale)
 return (int(px*scale-(pw-W)*fx),int(py*scale-(ph-H)*fy))
def source_chip(d,lines,y=725):
 f=font('Inter-Bold.ttf',17);width=min(492,max(int(d.textlength(line,font=f)) for line in lines)+26);height=12+len(lines)*23
 d.rounded_rectangle((20,y,20+width,y+height),radius=4,fill=(9,15,16));
 for i,line in enumerate(lines):d.text((31,y+4+23*i),line,font=f,fill='#f4ead6')
def case_cover():
 im=Image.new('RGB',(W,H),'#d9ccb0');d=ImageDraw.Draw(im);d.rectangle((17,17,W-17,H-17),outline='#604e3f',width=3);d.rectangle((28,28,W-28,H-28),outline='#9b8570',width=1)
 d.rectangle((32,98,W-32,156),fill='#251c18');d.text((76,116),'CLASSIFIED  /  FIELD DOSSIER',font=tiny,fill='#eee1c8');d.text((67,218),'CASE FILE 09',font=font('Inter-Black.ttf',46),fill='#261e18');d.text((111,282),'THE ROMAN OBJECT',font=font('JetBrainsMono-Bold.ttf',23),fill='#584334')
 p=ImageOps.contain(thumb,(320,480));im.paste(p,((W-p.width)//2,335));d=ImageDraw.Draw(im);d.text((55,853),'EXHIBIT A   /   ILLUSTRATED COVER',font=micro,fill='#34261e');return im
COVER=case_cover()
def frame(t):
 im=bg(t);d=ImageDraw.Draw(im)
 if t<1.1 or t>=31.18:
  # Same physical cover at the start and loop end. Opening punch comes after the first frame.
  z=1 if t>=31.18 else 1+(.21*math.sin(math.pi*min(t,1.1)/1.1));im=cover_zoom(COVER,t,z)
 elif t<3.2:
  im=overlay_black(cover_zoom(imgs['lyon'],t,1.02+0.12*(t-1.1)/2.1,.48,.53),35);d=ImageDraw.Draw(im);title(d,'12 SIDES',130,54);d.text((25,758),'LYON MUSEUM EXAMPLE  /  CC0',font=micro,fill=WHITE,stroke_width=2,stroke_fill='#101010')
 elif t<5.98:
  z=1.26+0.08*(t-3.2)/2.78;im=overlay_black(cover_zoom(imgs['lyon'],t,z,.47,.55),55);d=ImageDraw.Draw(im);title(d,'HOLES & KNOBS',125,44);cx,cy=locator(imgs['lyon'],451,603,z,.47,.55);r=48;u=max(0,min(1,(t-3.2)/.65));d.arc((cx-r,cy-r,cx+r,cy+r),-90,-90+int(u*360),fill='#e7b771',width=4);d.line((cx+r,cy,cx+r+72,cy-57),fill='#e7b771',width=3);d.text((cx+r+3,cy-82),'OPENING',font=tiny,fill=WHITE,stroke_width=2,stroke_fill='#101010');source_chip(d,['LYON MUSEUM EXAMPLE  /  CC0'],745)
 elif t<8.18:
  im=overlay_black(cover_zoom(imgs['bronze'],t,1.08+0.06*(t-5.98)/2.2,.5,.45),125);d=ImageDraw.Draw(im);title(d,'WHAT WAS IT FOR?',240,45);stamp(im,'UNKNOWN',t-6.4,530)
 elif t<10.68:
  im=bg(t);im.paste(maps['europe'],(0,110));d=ImageDraw.Draw(im);title(d,'OVER 100 FOUND',130,43);source_chip(d,['EXAMPLES ACROSS EUROPE'],745)
 elif t<13.22:
  im=overlay_black(cover_zoom(imgs['vienne'],t,1.05+0.14*(t-10.68)/2.54,.5,.5),100);d=ImageDraw.Draw(im);title(d,'PURPOSE',160,45);title(d,'STILL A MYSTERY',218,43,GOLD);d.text((25,765),'VIENNE MUSEUM EXAMPLE  /  CC0',font=micro,fill=WHITE,stroke_width=2,stroke_fill='#101010')
 elif t<15.42:
  im=overlay_black(cover_zoom(imgs['tongeren'],t,1.14+0.09*(t-13.22)/2.2,.47,.5),100);d=ImageDraw.Draw(im);title(d,'A MEASURING TOOL?',160,42);source_chip(d,['THEORY  /  NOT ESTABLISHED','TONGEREN MUSEUM EXAMPLE'],705)
 elif t<17.06:
  im=overlay_black(cover_zoom(imgs['knitting'],t,1.05+0.04*(t-15.42)/1.64,.5,.5),85);d=ImageDraw.Draw(im);title(d,'FOR KNITTING?',130,44);source_chip(d,['AI ILLUSTRATION  /  THEORY ONLY'],745)
 elif t<18.72:
  im=overlay_black(cover_zoom(imgs['bronze'],t,1.12+0.1*(t-17.06)/1.66,.5,.5),100);d=ImageDraw.Draw(im);title(d,'A RITUAL OBJECT?',170,42);d.text((30,735),'THEORY  /  NOT ESTABLISHED',font=tiny,fill=GOLD,stroke_width=2,stroke_fill='#101010');d.text((30,768),'HUNT MUSEUM EXAMPLE  /  CC0',font=micro,fill=WHITE,stroke_width=2,stroke_fill='#101010')
 elif t<20.72:
  im=overlay_black(cover_zoom(imgs['tongeren'],t,1.2,.5,.5),150);d=ImageDraw.Draw(im);title(d,'NONE ARE PROVEN',190,46);stamp(im,'NOT PROVEN',t-18.72,510)
 elif t<23.5:
  im=bg(t);im.paste(maps['england'],(0,110));d=ImageDraw.Draw(im);title(d,'ENGLAND  /  2023',125,44);q=(t-20.72)%1.7;r=10+q*23;x,y=374,474;d.ellipse((x-r,y-r,x+r,y+r),outline='#f0bf76',width=3);d.text((25,765),'NORTON DISNEY VILLAGE  /  APPROX.',font=micro,fill=WHITE,stroke_width=2,stroke_fill='#101010')
 elif t<25.15:
  im=overlay_black(cover_zoom(imgs['bronze'],t,1.07+.10*(t-23.5)/1.65,.5,.5),90);d=ImageDraw.Draw(im);title(d,'FOUND INTACT',135,46);source_chip(d,['MUSEUM EXAMPLE','NOT THE 2023 FIND'],710)
 elif t<28.18:
  im=overlay_black(cover_zoom(imgs['dig'],t,1.05+.05*(t-25.15)/3.03,.5,.5),80);d=ImageDraw.Draw(im);title(d,'THE SITE IS A CLUE',145,39);source_chip(d,['AI ILLUSTRATION','NOT THE ACTUAL EXCAVATION'],710)
 else:
  im=overlay_black(cover_zoom(imgs['vienne'],t,1.12+.10*(t-28.18)/3,.5,.5),135);d=ImageDraw.Draw(im);title(d,'WHAT DO YOU THINK?',190,39);title(d,'WHAT WAS IT FOR?',245,42,GOLD)
 if 1.1<=t<31.18:
  d=ImageDraw.Draw(im);d.rounded_rectangle((12,899,340,930),radius=2,fill='#d9ccb3');d.text((20,907),'CASE FILE 09  /  ROMAN OBJECT',font=micro,fill='#211b16')
 applycaps(im,t)
 # small film grain, consistent with C08, keyed to the one frame clock
 d=ImageDraw.Draw(im,'RGBA');r=random.Random(int(t*fps));
 for i in range(80):
  x=r.randrange(W);y=r.randrange(H);d.point((x,y),fill=(255,255,255,25))
 return im.convert('RGB')

checks=[.5,1.8,3.8,6.6,8.9,11.1,13.8,15.8,17.5,19.6,21.5,23.9,25.6,27,29,31.5];sheet=Image.new('RGB',(270*4,500*4),'#101818');sd=ImageDraw.Draw(sheet)
for i,t in enumerate(checks):
 q=frame(t);q.thumbnail((270,480));x=i%4*270;y=i//4*500;sheet.paste(q,(x,y));sd.text((x+5,y+481),str(t),fill='white')
sheet.save(P/'c09_v4_contact.jpg',quality=90)
if os.environ.get('PROBE')=='1': print('V4 probe ready');raise SystemExit
out=P/'picture_refined_v4.mp4';cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','3',str(out)];enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(dur*fps)):
 enc.stdin.write(frame(i/fps).tobytes())
 if i%150==0:print('frame',i,flush=True)
enc.stdin.close();assert enc.wait()==0
print('V3 PICTURE COMPLETE',flush=True)
