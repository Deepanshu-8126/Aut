from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import math,json,subprocess,os
P=Path('/home/user/outputs/fcy-fingers');W,H=1080,1920;fps=30;D=25.6
F=Path('/home/user/explainer-pipeline/assets/fonts');ff='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg'
font=lambda sz:ImageFont.truetype(str(F/'Inter-Black.ttf'),sz)
CAP=font(61); MIC=font(27)
C=(96,231,230); GOLD=(255,211,74);WHITE=(247,250,250)
raw={n:ImageOps.fit(Image.open(P/'assets'/f'{n}.png').convert('RGB'),(W,H),Image.Resampling.LANCZOS) for n in ['sink','sink_blink','sink_reaction','tip','finger_cutaway','grip','grip_lift']}
words=json.loads((P/'words.json').read_text());groups=[];cur=[]
for w in words:
 cur.append(w)
 if len(cur)>=3 or w['word'].strip().endswith(('.','?','!')):groups.append(cur);cur=[]
if cur:groups.append(cur)
def st(t):
 n=round(max(0,t)*1000);return f'{n//3600000:02}:{(n//60000)%60:02}:{(n//1000)%60:02},{n%1000:03}'
subs=[]
for i,g in enumerate(groups):
 s=g[0]['start']+.12;e=g[-1]['end']+.20
 if i+1<len(groups):e=min(e,groups[i+1][0]['start']+.12)
 subs.append(f"{i+1}\n{st(s)} --> {st(e)}\n"+''.join(w['word'] for w in g).strip())
(P/'DRAFT.srt').write_text('\n\n'.join(subs)+'\n')
def clamp(v):return max(0,min(1,v))
def smooth(v):v=clamp(v);return v*v*(3-2*v)
def shot(im,z=1.,cx=.5,cy=.5):
 cw=int(W/z);ch=int(H/z);left=int((W-cw)*cx);top=int((H-ch)*cy);return im.crop((left,top,left+cw,top+ch)).resize((W,H),Image.Resampling.LANCZOS)
def title(d,s,y,size=65,col=WHITE):
 f=font(size);bb=d.textbbox((0,0),s,font=f);wid=bb[2]-bb[0]
 if wid>960:f=font(int(size*960/wid));bb=d.textbbox((0,0),s,font=f);wid=bb[2]-bb[0]
 d.text(((W-wid)//2,y),s,font=f,fill=col,stroke_width=4,stroke_fill=(3,9,15))
def pill(d,s,x,y,color=(170,217,218)):
 f=MIC;bb=d.textbbox((0,0),s,font=f);ww=bb[2]+30;d.rounded_rectangle((x,y,x+ww,y+45),radius=10,fill=(5,23,33),outline=(63,105,112),width=2);d.text((x+15,y+6),s,font=f,fill=color)
def caption(im,t):
 for g in groups:
  if g[0]['start']+.12 <= t < g[-1]['end']+.20:
   d=ImageDraw.Draw(im);s=' '.join(w['word'].strip().upper() for w in g);f=CAP;wid=d.textlength(s,font=f)
   if wid>930:f=font(int(61*930/wid));wid=d.textlength(s,font=f)
   x=(W-wid)/2;y=1600;d.rounded_rectangle((int(x-20),y-8,int(x+wid+20),y+78),radius=14,fill=(5,15,24))
   for w in g:
    ss=w['word'].strip().upper();co=GOLD if w['start']+.12<=t<=w['end']+.12 else WHITE
    d.text((int(x),y),ss,font=f,fill=co,stroke_width=2,stroke_fill=(0,0,0));x+=d.textlength(ss+' ',font=f)
   break
# Local facial-region mask prevents full-frame ghosting across AI edits.
mask=Image.new('L',(W,H),0);md=ImageDraw.Draw(mask);md.ellipse((500,380,850,830),fill=255)
def character(t,end=False):
 base=raw['sink'].copy(); reaction=smooth((t-.25)/.55) if not end else 0.35
 base=Image.composite(Image.blend(raw['sink'],raw['sink_reaction'],reaction),base,mask)
 blink=max(0,1-abs(t-1.45)/.11) if not end else max(0,1-abs(t-23.0)/.11)
 if blink:base=Image.composite(Image.blend(base,raw['sink_blink'],blink),base,mask)
 # Slight changing perspective coupled to reaction, not a substitute for pose animation.
 base=shot(base,1.03+(min(1,max(0,t))/1)*.08 if not end else 1.03,.58,.35)
 return base

def diagram(t):
 im=Image.new('RGB',(W,H),(9,24,37));d=ImageDraw.Draw(im)
 title(d,'UNDER YOUR SKIN',145,70,GOLD);pill(d,'SIMPLIFIED DIAGRAM',45,1470)
 # Incoming nervous signal, vessels then reduced volume and skin folds.
 if t<8.75:
  title(d,'NERVE SIGNAL',300,57,C)
  d.line((130,690,460,690,460,980,800,980),fill=(86,184,186),width=19,joint='curve')
  for i in range(6):
   x=130+((t*230+i*120)%330);d.ellipse((x-12,678,x+12,702),fill=(229,255,174))
  d.ellipse((310,850,755,1300),fill=(100,45,56),outline=(242,128,122),width=12)
  d.ellipse((387,930,678,1220),fill=(216,82,78),outline=(253,172,146),width=10)
  title(d,'TINY BLOOD VESSELS',1350,47,WHITE)
 else:
  p=smooth((t-8.75)/1.1);q=smooth((t-11.8)/1.0)
  title(d,'VESSELS NARROW',300,57,C)
  outer=(190,880,890,1180);d.rounded_rectangle(outer,radius=145,fill=(111,50,56),outline=(252,163,137),width=8)
  rh=int(90-52*p);d.rounded_rectangle((210,1030-rh,870,1030+rh),radius=max(15,rh),fill=(220,81,82))
  # Folds are generated dynamically along a surface, as volume decreases.
  y0=690+int(q*52);pts=[]
  for x in range(145,936,8):
   envelope=math.sin(math.pi*(x-145)/790)**2; y=y0+q*30*math.sin((x-145)*math.pi/115)*envelope;pts.append((x,int(y)))
  d.polygon(pts+[(935,850),(145,850)],fill=(225,171,141));d.line(pts,fill=(251,210,172),width=12)
  title(d,'LESS VOLUME BELOW',1300,50,WHITE)
  if q>.45:title(d,'SKIN FOLDS',1370,45,GOLD)
 return im

def frame(t):
 if t<1.35:
  im=character(t);d=ImageDraw.Draw(im);title(d,'WHY WRINKLE?',125,70,GOLD)
 elif t<2.65:
  im=shot(raw['tip'],1.0+.08*(t-1.35),.5,.45);d=ImageDraw.Draw(im);title(d,'WHY WRINKLE?',125,70,GOLD);pill(d,'AI ILLUSTRATION',38,1480)
 elif t<5.78:
  im=shot(raw['tip'],1.02+.12*(t-2.65)/3.13,.51,.45);d=ImageDraw.Draw(im);title(d,'NOT JUST WATER',130,65,GOLD);pill(d,'AI ILLUSTRATION',38,1480)
 elif t<8.75:
  im=shot(raw['finger_cutaway'],1.01+.14*(t-5.78)/2.97,.5,.58);d=ImageDraw.Draw(im);title(d,'UNDER YOUR SKIN',130,65,GOLD);title(d,'NERVE SIGNAL',225,47,C);pill(d,'AI CONCEPT / SIMPLIFIED',38,1480)
  for i in range(6):
   x=160+((t*210+i*110)%640);d.ellipse((x-10,1250,x+10,1270),fill=C)
 elif t<13.86:im=diagram(t)
 elif t<19.0:
  z=1.01+.14*((t-13.86)/8);im=shot(raw['grip'] if t<16.70 else raw['grip_lift'],z,.47,.65);d=ImageDraw.Draw(im)
  if t<18.35:title(d,'MAY HELP WET GRIP',130,56,GOLD)
  else:title(d,'WHY? STILL STUDIED',130,54,GOLD)
  pill(d,'AI ILLUSTRATION',38,1480)
 elif t<21.85:
  im=character(t,True);d=ImageDraw.Draw(im);title(d,'WHY? STILL STUDIED',130,54,GOLD)
 else:
  im=character(t,True);d=ImageDraw.Draw(im);title(d,'YOUR BODY REACTS',130,65,GOLD)
 caption(im,t);return im
if os.environ.get('PROBE'):
 times=[0,.6,1.45,2.7,4,5.9,7,8.8,9.7,11.3,12.8,14.2,16.4,18.6,22.2,24.4];out=Image.new('RGB',(864,1536),'#101010')
 for i,t in enumerate(times):
  a=frame(t).resize((216,384));out.paste(a,((i%4)*216,(i//4)*384))
 out.save(P/'probe.jpg',quality=90);print('probe complete');raise SystemExit
cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'picture.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(D*fps)):
 p.stdin.write(frame(i/fps).tobytes())
 if i%150==0:print('frame',i,flush=True)
p.stdin.close();assert p.wait()==0
print('render complete')
