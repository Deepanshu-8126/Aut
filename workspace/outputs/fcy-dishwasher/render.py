from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import json,math,subprocess,os,cv2,numpy as np
from pathlib import Path
P=Path('/home/user/outputs/fcy-dishwasher'); F=Path('/home/user/explainer-pipeline/assets/fonts'); W,H=1080,1920; FPS=30; D=32
font=lambda name,size:ImageFont.truetype(str(F/name),size)
head=font('Inter-Black.ttf',70);small=font('Inter-Black.ttf',45);label=font('Inter-Bold.ttf',32);micro=font('Inter-Bold.ttf',26);cap=font('Inter-Black.ttf',55)
CY=(62,223,239);G=(255,210,76);WHITE=(246,248,248);MUT=(150,177,194);bg=(6,16,30)
words=json.loads((P/'word_times.json').read_text()); groups=[]; part=[]
for i,w in enumerate(words):
 part.append(w)
 if len(part)>=3 or w['word'].strip().endswith(('.','?','!')) or (i+1<len(words) and words[i+1]['start']-w['end']>.38):groups.append(part);part=[]
if part:groups.append(part)

def timestamp(t):
 m=max(0,round(t*1000));return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
subs=[]
for i,g in enumerate(groups):
 s=g[0]['start']+.12;e=g[-1]['end']+.22
 if i+1<len(groups):e=min(e,groups[i+1][0]['start']+.12)
 subs.append(f"{i+1}\n{timestamp(s)} --> {timestamp(e)}\n"+''.join(w['word'] for w in g).strip())
(P/'DISHWASHER_DRAFT.srt').write_text('\n\n'.join(subs)+'\n')

def title(d,s,y,color=WHITE,fs=70):
 f=font('Inter-Black.ttf',fs); box=d.textbbox((0,0),s,font=f);width=box[2]-box[0]
 if width>960:f=font('Inter-Black.ttf',max(34,int(fs*960/width)));box=d.textbbox((0,0),s,font=f);width=box[2]-box[0]
 d.text(((W-width)//2,y),s,font=f,fill=color,stroke_width=3,stroke_fill=(3,9,18))
def pill(d,s,x,y,col=WHITE):
 width=int(d.textlength(s,font=label))+40;d.rounded_rectangle((x,y,x+width,y+54),radius=12,fill=(8,21,36),outline=(43,88,102),width=2);d.text((x+20,y+9),s,font=label,fill=col)
def rounded(d,box,fill,outline=None,width=1,r=25):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
# Use the actual dishwasher as a low-key contextual background under diagrams.
cap_bg=cv2.VideoCapture(str(P/'assets/dishwasher_vertical.mp4'));cap_bg.set(cv2.CAP_PROP_POS_MSEC,6000);ok,bgf=cap_bg.read();assert ok;BG_STILL=ImageEnhance.Brightness(Image.fromarray(cv2.cvtColor(bgf,cv2.COLOR_BGR2RGB))).enhance(.16);cap_bg.release()
CONCEPT=ImageOps.fit(Image.open(P/'assets/cutaway.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
ARM=ImageOps.fit(Image.open(P/'assets/spray_arm.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
def base(t):
 im=BG_STILL.copy();d=ImageDraw.Draw(im)
 for i in range(22):
  x=i*62;d.line((x,0,x,H),fill=(9,26,41),width=2)
 for i in range(28):
  y=i*76;d.line((0,y,W,y),fill=(8,23,37),width=1)
 d.rounded_rectangle((28,28,190,76),radius=18,fill=(17,28,37));d.text((48,37),'FUNCYOUS',font=micro,fill=G)
 return im

def arrow(d,p0,p1,color=CY,width=12,headsize=25):
 x,y=p0;X,Y=p1;d.line((x,y,X,Y),fill=color,width=width);a=math.atan2(Y-y,X-x);p=[(X,Y),(X-headsize*math.cos(a-.58),Y-headsize*math.sin(a-.58)),(X-headsize*math.cos(a+.58),Y-headsize*math.sin(a+.58))];d.polygon(p,fill=color)
def particles(d,x0,y0,x1,y1,t,col=CY,n=5):
 for i in range(n):
  v=(t*.48+i/n)%1;x=x0+(x1-x0)*v;y=y0+(y1-y0)*v;d.ellipse((x-9,y-9,x+9,y+9),fill=col)
def caption(im,t):
 for g in groups:
  if g[0]['start']+.12<=t<g[-1]['end']+.22:
   d=ImageDraw.Draw(im);s=' '.join(x['word'].strip().upper() for x in g);f=cap;bb=d.textbbox((0,0),s,font=f);wid=bb[2]-bb[0]
   if wid>960:f=font('Inter-Black.ttf',int(55*960/wid));bb=d.textbbox((0,0),s,font=f);wid=bb[2]-bb[0]
   x=(W-wid)//2;y=1600;rounded(d,(x-25,y-12,x+wid+25,y+80),(4,13,23),r=14)
   for w in g:
    q=w['word'].strip().upper();col=G if w['start']+.12<=t<=w['end']+.12 else WHITE;d.text((x,y),q,font=f,fill=col,stroke_width=2,stroke_fill=(0,0,0));x+=d.textlength(q+' ',font=f)
   break

def sim(t,scene):
 im=base(t);d=ImageDraw.Draw(im);pill(d,'SIMPLIFIED ANIMATION',45,1440,MUT)
 if scene=='sump':
  im=ImageEnhance.Brightness(shotcrop(CONCEPT,1.0 if t<6.15 else 1.22,.49,.75)).enhance(.75);d=ImageDraw.Draw(im)
  title(d,'A SHALLOW POOL',160,G,66);title(d,'NOT A FULL TUB',240,WHITE,51)
  # Pulse at the water collection in the generic illustration.
  # No fixed overlay: the rebuilt conceptual image has a different water layout.
  if t>=7.22:pill(d,'HEAT + DETERGENT',275,1510,G)
  else:pill(d,'WATER AT THE BASE',265,1510,CY)
  pill(d,'AI CONCEPT / LAYOUT VARIES',60,1430,MUT)
 elif scene=='pump':
  title(d,'THE PUMP',160,G);title(d,'MOVES WATER',242,WHITE,55)
  rounded(d,(95,1060,555,1220),(20,91,115),(64,201,226),5);d.text((175,1100),'SUMP',font=head,fill=WHITE)
  d.line((555,1140,655,1140),fill=(122,146,153),width=60);d.ellipse((580,965,900,1285),fill=(51,67,77),outline=(200,214,217),width=10)
  cx,cy=740,1125;d.ellipse((cx-100,cy-100,cx+100,cy+100),fill=(15,34,47),outline=CY,width=7)
  for k in range(4):
   a=t*4+k*math.pi/2;x=cx+75*math.cos(a);y=cy+75*math.sin(a);d.line((cx,cy,x,y),fill=G,width=16)
  d.line((740,965,740,640,860,640),fill=(120,148,156),width=55);d.line((740,965,740,640,860,640),fill=(13,48,62),width=28)
  particles(d,370,1140,650,1140,t);particles(d,740,950,740,660,t);particles(d,740,640,860,640,t)
  arrow(d,(750,740),(750,650));pill(d,'CIRCULATION',290,1260,CY)
 elif scene=='jets':
  title(d,'ANGLED JETS',160,G);title(d,'MAKE IT SPIN',240,WHITE,55)
  cx,cy=540,900;a=(t-13.2)*1.35;ux,uy=math.cos(a),math.sin(a);r=320
  d.ellipse((220,580,860,1220),outline=(38,79,93),width=5)
  for i in range(12):
   a1=i*math.pi/6;xx=cx+340*math.cos(a1);yy=cy+340*math.sin(a1);d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=(45,91,105))
  d.line((cx-r*ux,cy-r*uy,cx+r*ux,cy+r*uy),fill=(165,184,187),width=65);d.line((cx-r*ux,cy-r*uy,cx+r*ux,cy+r*uy),fill=(51,77,87),width=32);d.ellipse((cx-46,cy-46,cx+46,cy+46),fill=(16,40,53),outline=G,width=8)
  for sign in [-1,1]:
   xx=cx+sign*240*ux;yy=cy+sign*240*uy;dx=-sign*uy;dy=sign*ux
   d.ellipse((xx-15,yy-15,xx+15,yy+15),fill=CY);arrow(d,(xx,yy),(xx+dx*145,yy+dy*145),CY,10,26)
   for j in range(4):
    u=((t*1.7+j*.25)%1)*155;px=xx+dx*u;py=yy+dy*u;d.ellipse((px-8,py-8,px+8,py+8),fill=(161,246,255))
  d.arc((160,520,920,1280),210,325,fill=G,width=12);pill(d,'TOP VIEW  /  CONCEPT',240,1290,MUT)
 elif scene=='wash':
  title(d,'SPRAY HITS DISHES',160,G,63)
  for i,x in enumerate([300,540,780]):
   d.ellipse((x-100,490,x+100,940),fill=(220,227,225),outline=(252,252,242),width=10)
   d.ellipse((x-58,545,x+58,885),outline=(157,178,182),width=6)
   for j in range(4):
    phase=(t*2.4+j*.3+i*.15)%1;y=1100-phase*500;xx=x+math.sin(t*3+i+j)*22;d.line((xx,y,xx-20,y+48),fill=CY,width=8)
  d.rounded_rectangle((150,1120,930,1172),radius=26,fill=(117,147,155),outline=(222,236,238),width=4);d.ellipse((496,1096,584,1184),fill=(43,104,118),outline=G,width=6)
  pill(d,'PRESSURIZED WATER',278,1250,CY)
 elif scene=='filter':
  title(d,'WATER RETURNS',160,G,66);title(d,'THROUGH A FILTER',242,WHITE,52)
  rounded(d,(200,540,880,1025),(37,55,66),(132,163,168),8,30)
  for x in range(240,860,70):d.line((x,550,x,1010),fill=(104,130,135),width=8)
  for y in range(590,990,70):d.line((210,y,870,y),fill=(104,130,135),width=8)
  for i in range(15):
   x=230+i*43; yy=430+((t*160+i*63)%180);d.ellipse((x-8,yy-8,x+8,yy+8),fill=CY)
  for x,y in [(295,570),(495,540),(700,575),(810,565)]:d.ellipse((x-14,y-14,x+14,y+14),fill=(235,173,82))
  arrow(d,(540,1040),(540,1185),CY,14);pill(d,'DEBRIS IS CAUGHT',264,1260,G)
 else:
  title(d,'DRAIN THE WASH',160,G,62);title(d,'THEN FRESH RINSE',240,WHITE,54)
  rounded(d,(135,610,945,1100),(25,51,62),(135,163,170),7,30)
  if t<27.24:
   level=960+int(115*max(0,min(1,(t-25.65)/1.45)));d.rectangle((150,level,930,1080),fill=(81,104,83));particles(d,540,1080,540,1270,t,G,4);arrow(d,(540,1080),(540,1270),G,16);pill(d,'DIRTY WATER OUT',280,1330,G)
  else:
   d.rectangle((150,1020,930,1080),fill=(30,113,143));arrow(d,(780,450),(780,600),CY,16);pill(d,'FRESH WATER IN',290,1250,CY)
   for i in range(15):
    x=205+i*48;y=620+((t*230+i*48)%350);d.ellipse((x-6,y-6,x+6,y+6),fill=CY)
 return im

stock=cv2.VideoCapture(str(P/'assets/dishwasher_vertical.mp4'));last_idx=-10
still=ImageOps.fit(Image.open(P/'assets/cutaway.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS)
def stockframe(i):
 global last_idx
 if i!=last_idx+1:stock.set(cv2.CAP_PROP_POS_FRAMES,i)
 ok,f=stock.read();last_idx=i
 if not ok: raise RuntimeError(f'stock fail {i}')
 return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
def shotcrop(im,z,fx=.5,fy=.5):
 if z<=1:return im
 ww=int(W/z);hh=int(H/z);left=int((W-ww)*fx);top=int((H-hh)*fy)
 return im.crop((left,top,left+ww,top+hh)).resize((W,H),Image.Resampling.LANCZOS)
def frame(t):
 if t<4.96:
  im=stockframe(min(620,int((1+t*.88)*30)))
  if t<.55:z=1.0
  elif t<1.1:z=1.42
  elif t<1.65:z=1.06
  elif t<2.3:z=1.36
  elif t<3.7:z=1.07
  else:z=1.30
  im=shotcrop(im,z,.53,.62);im=ImageEnhance.Brightness(im).enhance(.66);d=ImageDraw.Draw(im)
  if t<2.3:title(d,'NOT A FULL TUB',170,G,77)
  else:title(d,'SO HOW DOES IT CLEAN?',170,WHITE,60)
  d.rounded_rectangle((28,28,190,76),radius=18,fill=(17,28,37));d.text((48,37),'FUNCYOUS',font=micro,fill=G)
 elif t<7.25:im=sim(t,'sump')
 elif t<9.52:
  im=shotcrop(CONCEPT,1.55+.18*(t-7.25)/2.27,.49,.82);im=ImageEnhance.Brightness(im).enhance(.72);d=ImageDraw.Draw(im);title(d,'HEAT + DETERGENT',160,G,63);pill(d,'AI CONCEPT / LAYOUT VARIES',50,1390,MUT)
 elif t<11.5:im=sim(t,'pump')
 elif t<13.20:
  im=ImageEnhance.Brightness(shotcrop(ARM,1.0+.17*(t-11.5)/1.7,.64,.39)).enhance(.85);d=ImageDraw.Draw(im);title(d,'HOLLOW SPRAY ARM',160,G,62);pill(d,'AI CONCEPT / LAYOUT VARIES',55,1320,MUT)
 elif t<15.9:
  im=ImageEnhance.Brightness(shotcrop(ARM,(1.04+.14*(t-13.20)/1.20) if t<14.4 else (1.28+.18*(t-14.4)/1.5),.64,.39)).enhance(.85);d=ImageDraw.Draw(im);title(d,'ANGLED WATER JETS',160,G,62);pill(d,'AI CONCEPT / LAYOUT VARIES',55,1320,MUT)
  for j in range(4):
   a=(t*1.4+j*.25)%1;x=600+a*120;y=630-a*115;d.ellipse((x-9,y-9,x+9,y+9),fill=CY)
 elif t<17.84:im=sim(t,'jets')
 elif t<19.94:im=sim(t,'wash')
 elif t<22.52:im=sim(t,'filter')
 elif t<24.40:
  im=sim(t,'pump');d=ImageDraw.Draw(im);rounded(d,(170,145,910,320),bg,r=18);title(d,'PUMPED AROUND AGAIN',160,G,55)
 elif t<29.48:im=sim(t,'drain')
 else:
  im=stockframe(30 if t>=31.6 else min(620,int((11+(t-29.48)*1.2)*30)));im=ImageEnhance.Brightness(im).enhance(.66);d=ImageDraw.Draw(im);title(d,'NOT A FULL TUB',170,G,77);d.rounded_rectangle((28,28,190,76),radius=18,fill=(17,28,37));d.text((48,37),'FUNCYOUS',font=micro,fill=G)
 caption(im,t);return im

if os.environ.get('PROBE')=='1':
 checks=[0,.5,2.8,5.2,7.4,9.8,11.8,13.4,15.8,18.2,20.2,22.4,24.6,26.5,27.8,30];out=Image.new('RGB',(1080,1920),'#101818');d=ImageDraw.Draw(out)
 for i,t in enumerate(checks):
  im=frame(t);im.thumbnail((270,450));x=i%4*270;y=i//4*480;out.paste(im,(x,y));d.text((x+5,y+453),str(t),fill='white')
 out.save(P/'PROBE_SHEET.jpg',quality=90);print('probe ready');raise SystemExit
FF='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg';cmd=[FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-threads','4',str(P/'picture_rebuilt.mp4')];p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(int(D*FPS)):
 p.stdin.write(frame(i/FPS).tobytes())
 if i%150==0:print('frame',i,flush=True)
p.stdin.close();assert p.wait()==0
print('picture done')
