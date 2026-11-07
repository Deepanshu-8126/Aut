#!/usr/bin/env python3
# DBC STYLES SAMPLE TEST — 6 unused drawn-by-code styles (MIT) demoed on OUR
# channel's subjects (gufa/mandir/naag), Hindi VO voice-06. 60s @ 30fps.
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/dbcdemo"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
DBC = os.path.join(ASSETS, "dbc")
FONTS = os.path.join(ASSETS, "fonts")
PR = os.path.join(ASSETS, "props")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FPS = 30
W, H = 1920, 1080
SEG = 9.5
NSEG = 6
TOTAL = SEG * NSEG + 3.0  # 60.0

SR = 44100
def _n(d): return int(d * SR)
def box(x, w):
    if w < 2: return x
    c = np.cumsum(np.concatenate(([0.0], x)))
    y = (c[w:] - c[:-w]) / w
    return np.concatenate((y, np.zeros(len(x) - len(y))))
def tone(d, f0, f1=None, a=0.3):
    t = np.arange(_n(d)) / SR; f1 = f1 or f0
    return a * np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * d)))
def envad(x, a, r):
    n = len(x); e = np.ones(n)
    na, nr = max(1, _n(a)), max(1, _n(r))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
    return x * e
def noise(d, seed=7): return np.random.RandomState(seed).standard_normal(_n(d)) * 0.4
def whoosh(d, a, seed=5):
    x = noise(d, seed); bp = box(x, 10) - box(x, 120)
    t = np.arange(len(bp)) / len(bp)
    return a * bp * np.sin(np.pi * t) ** 2 * 6
def pop(a=0.5): return envad(tone(0.12, 420, 880, a), 0.004, 0.06)
def thud(a):
    d = 0.4
    x = tone(d, 85, 38, a) * np.exp(-np.arange(_n(d)) / SR * 9)
    nz = envad(box(noise(0.12, 9), 24) * 2.2, 0.004, 0.1)
    x[:len(nz)] += nz * a
    return x
def bell(f, a, d=2.2):
    t = np.arange(_n(d)) / SR
    x = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2.76*t))
    return a * x * np.exp(-t * 2.1)

def build_audio():
    n = _n(TOTAL); sfx = np.zeros(n); vo = np.zeros(n)
    def put(dst, x, at, g=1.0):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); dst[i:i + L] += x[:L] * g
    for i in range(NSEG):
        put(sfx, whoosh(0.6, 0.3), i * SEG)
        put(sfx, pop(0.45), i * SEG + 0.9)
    put(sfx, thud(0.6), 0 * SEG + 2.6)            # comic panel slam
    put(sfx, thud(0.5), 0 * SEG + 5.4)            # sfx burst
    put(sfx, pop(0.4), 2 * SEG + 3.0)             # clay squash
    put(sfx, thud(0.5), 4 * SEG + 1.2)            # melt title drop
    put(sfx, bell(587, 0.16), NSEG * SEG + 0.3)   # end card
    for i in range(NSEG):
        wv = os.path.join(ROOT, "dvo_%d.wav" % (i + 1))
        if not os.path.exists(wv):
            subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(PR, "dvo_%d.mp3" % (i + 1)),
                            "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
        wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
        wf.close()
        i0 = _n(i * SEG + 0.35); L = min(len(dat), n - i0)
        vo[i0:i0 + L] += dat[:L] * 1.3
    t = np.arange(n) / SR
    mus = 0.035 * (np.sin(2 * np.pi * 73.42 * t) + np.sin(2 * np.pi * 73.75 * t + 0.8)) \
        + 0.006 * np.sin(2 * np.pi * 293.66 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t))
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    mus *= (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.8 + mus
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok")

def b64(p): return base64.b64encode(open(p, "rb").read()).decode()

def build_html():
    kits = ["core.js", "comic.js", "riso.js", "clay.js", "line.js", "groovy.js", "liquid.js", "kaleido.js"]
    scripts = "\n".join("<script>%s</script>" % open(os.path.join(DBC, k)).read() for k in kits)
    ff = """
@font-face{font-family:'Bangers';src:url('file://%s/Bangers-Regular.ttf');}
@font-face{font-family:'Comic Neue';src:url('file://%s/ComicNeue-Bold.ttf');font-weight:700;}
@font-face{font-family:'Shrikhand';src:url('file://%s/Shrikhand-latin.woff2');}
@font-face{font-family:'Hand';src:url('file://%s/PatrickHand-Regular.ttf');}
@font-face{font-family:'Mono';src:url('file://%s/JetBrainsMono-Bold.ttf');}
@font-face{font-family:'InterB';src:url('file://%s/Inter-Black.ttf');}
@font-face{font-family:'Deva';src:url('file:///var/tmp/ujjain/TiroDeva.ttf');}
""" % (DBC, DBC, DBC, DBC, FONTS, FONTS)
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body>
KITSCRIPTS
<script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,SEG=9.5,TOTAL=__TOT__;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const env={W:W,H:H,k:1,px:[W,H]};
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const LOGOIM=new Image();let logoOk=0;LOGOIM.onload=()=>logoOk=1;
LOGOIM.src='data:image/png;base64,LOGO64';
let press=null;
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
const LAB=[['01 \u00b7 COMIC','\u0915\u0925\u093e \u0914\u0930 \u090f\u0915\u094d\u0936\u0928 \u092a\u0948\u0928\u0932'],
 ['02 \u00b7 RISOGRAPH','\u0930\u0947\u091f\u094d\u0930\u094b \u092a\u094d\u0930\u093f\u0902\u091f \u0921\u093e\u092f\u0917\u094d\u0930\u093e\u092e'],
 ['03 \u00b7 CLAY','\u092a\u094d\u0932\u093e\u0938\u094d\u091f\u093f\u0938\u093f\u0928 \u0930\u0940\u0915\u0902\u0938\u094d\u091f\u094d\u0930\u0915\u094d\u0936\u0928'],
 ['04 \u00b7 LINE ART','\u0939\u093e\u0925 \u0915\u0940 \u0921\u094d\u0930\u0949\u0907\u0902\u0917 \u00b7 \u0928\u0915\u094d\u0936\u0947'],
 ['05 \u00b7 70s POSTER','\u091f\u093e\u0907\u091f\u0932 \u0915\u093e\u0930\u094d\u0921'],
 ['06 \u00b7 LIQUID + KALEIDO','\u091f\u094d\u0930\u093e\u0902\u095b\u093f\u0936\u0928 \u00b7 \u0921\u094d\u0930\u0940\u092e \u0938\u0940\u0928']];
function band(si,lt){
 g.save();g.globalAlpha=Math.min(1,lt*3);
 g.fillStyle='rgba(7,5,10,0.92)';g.fillRect(0,H-96,W,96);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-96,W,3);
 T(60,H-46,LAB[si][0],'Mono',34,'#ff8c3b','left',1,2);
 T(620,H-46,LAB[si][1],'Deva',34,'#eef2f8','left');
 T(W-60,H-46,'drawn-by-code \u00b7 MIT KIT','Mono',22,'rgba(238,242,248,0.55)','right',1,2);
 g.restore();}
// ---------------- SEG 0 : COMIC ----------------
function segComic(t){
 const C=Comic,K=C.COL,E=Ease,tt=C.onTwos(t);
 C.paper(g,env);
 const A={x:60,y:60,w:860,h:850},B={x:960,y:60,w:900,h:400},P={x:960,y:500,w:900,h:410};
 const pop=(r,at,fn,seed)=>{const e=C.enter(t,at);if(!e.on)return;
  g.save();g.translate(r.x+r.w/2,r.y+r.h/2);g.scale(e.s,e.s);g.rotate((1-e.u)*0.05);
  g.translate(-(r.x+r.w/2),-(r.y+r.h/2));C.panel(g,r,fn,{seed});g.restore();};
 // A: gufa + naag rising
 pop(A,0.2,(c)=>{
  C.halftone(c,C.pathOf(C.rect(A.x,A.y,A.w,A.h)),{color:K.sky,spacing:16,r0:1,r1:6.5,dir:[0,1],box:A});
  // cave arch
  C.shape(c,[[A.x+80,A.y+850],[A.x+80,A.y+420],[A.x+240,A.y+220],[A.x+620,A.y+220],[A.x+780,A.y+430],[A.x+780,A.y+850]],
   {fill:'#3c3350',w:8,seed:'cave',smooth:false,shade:(cc,p)=>C.dots(cc,p,{color:'#2a2340',spacing:13,r:2.6})});
  c.fillStyle='#17122a';c.beginPath();c.ellipse(A.x+430,A.y+620,250,230,0,0,7);c.fill();
  // naag rises from cave mouth on the beat
  const up=E.out(E.seg(tt,1.2,2.2));
  if(up>0){const bx=A.x+430,by=A.y+760-up*330;
   C.ink(c,[[bx-10,A.y+800],[bx-60,A.y+740-up*120],[bx+40,by+140],[bx,by+60]],{w:34,taper:[0.1,0],seed:'body',wobble:0.06});
   C.shape(c,C.ellipse(bx,by,86,100,36),{fill:'#2f7d4f',w:7,seed:'hood',smooth:false,
    shade:(cc,p)=>C.dots(cc,p,{color:'#225c3a',spacing:10,r:2})});
   C.shape(c,C.ellipse(bx,by+10,34,52,24),{fill:'#d8c25a',w:5,seed:'belly',smooth:false});
   for(const ex of[-26,26]){c.fillStyle=K.ink;c.beginPath();c.arc(bx+ex,by-18,8,0,7);c.fill();}
   C.ink(c,[[bx,by+56],[bx,by+86],[bx-14,by+104]],{w:5,seed:'tongue',color:K.red});
   C.speedLines(c,bx,by+40,{n:10,r0:160,r1:260,seed:'sl'});
  }
  if(tt>2.6)C.balloon(c,{x:A.x+660,y:A.y+180,rx:120,ry:80,tail:[A.x+520,A.y+330],kind:'shout',text:'NAAG!',size:52,seed:'bal'});
 },'A');
 // B: mandir + sun
 pop(B,0.9,(c)=>{
  c.fillStyle=K.yellow;c.fillRect(B.x,B.y,B.w,B.h);
  C.dots(c,C.pathOf(C.rect(B.x,B.y,B.w,B.h)),{color:'#e2b43a',spacing:15,r:3});
  C.shape(c,C.ellipse(B.x+180,B.y+120,70,70,30),{fill:K.orange,w:6,seed:'sun',smooth:false});
  const mx=B.x+560,my=B.y+360;
  C.shape(c,[[mx-200,my],[mx+200,my],[mx+170,my-60],[mx-170,my-60]],{fill:K.white,w:7,seed:'base',smooth:false});
  C.shape(c,[[mx-130,my-60],[mx+130,my-60],[mx,my-300]],{fill:K.white,w:7,seed:'shikhar',smooth:false,
   shade:(cc,p)=>C.halftone(cc,p,{color:K.orange,spacing:11,r0:0,r1:4,dir:[1,0.3],box:{x:mx-140,y:my-310,w:280,h:260}})});
  C.shape(c,C.ellipse(mx,my-320,22,26,20),{fill:K.red,w:5,seed:'kalash',smooth:false});
 },'B');
 // C: SFX burst
 pop(P,2.6,(c)=>{
  c.fillStyle=K.red;c.fillRect(P.x,P.y,P.w,P.h);
  C.dots(c,C.pathOf(C.rect(P.x,P.y,P.w,P.h)),{color:'#b72c22',spacing:14,r:4});
  const s=1+0.06*Math.sin(C.drawing(t)*1.9);
  C.burst(c,P.x+P.w/2,P.y+P.h/2,300*s,{ry:170*s,points:14,fill:K.yellow,seed:'r'});
  C.sfx(c,'RAHASYA!',P.x+P.w/2,P.y+P.h/2,{size:120,rot:-0.08,seed:'r2',fill:K.white,shade:K.blue});
 },'C');
 Comic.grainPost(g,env);
}
// ---------------- SEG 1 : RISO ----------------
function segRiso(t){
 const R=Riso,Tn=R.tone,d=Math.floor(t*12+1e-6);
 press.begin(d);
 const pinkS=press.plate('pink','screen'),yellow=press.plate('yellow'),
       blueS=press.plate('blue','screen'),navy=press.plate('navy');
 pinkS.fillStyle=R.ramp(pinkS,0,0,0,760,0.08,0.55);pinkS.fillRect(0,0,W,760);
 const sy=430-d*3;
 yellow.fillStyle=Tn(1);yellow.beginPath();yellow.arc(1380,sy,190,0,7);yellow.fill();
 blueS.fillStyle=R.ramp(blueS,0,640,0,H,0.35,0.9);
 blueS.beginPath();blueS.moveTo(0,760);blueS.quadraticCurveTo(480,580,960,730);
 blueS.quadraticCurveTo(1440,860,1920,700);blueS.lineTo(1920,1080);blueS.lineTo(0,1080);blueS.fill();
 // navy temple on a hill
 navy.fillStyle=Tn(0.92);
 navy.beginPath();navy.moveTo(300,840);navy.lineTo(980,840);navy.lineTo(940,760);navy.lineTo(340,760);navy.closePath();navy.fill();
 navy.beginPath();navy.moveTo(420,760);navy.lineTo(860,760);navy.lineTo(640,350);navy.closePath();navy.fill();
 navy.beginPath();navy.arc(640,330,26,0,7);navy.fill();
 const p=Math.min(1,Math.max(0,(d-10)/22));
 R.ring(navy,640,620,330,8,'ring',{p:p});
 R.line(navy,[[1180,900],[1760,900]],6,'gline',{});
 press.print(g,{key:d,register:{pink:[Math.sin(t*0.9)*5,2],blue:[-4,Math.cos(t*0.7)*4]}});
}
// ---------------- SEG 2 : CLAY ----------------
function segClay(t){
 const C=Clay,E=Ease,tq=Math.floor(t*12+1e-6)/12,v=C.boil(t);
 g.fillStyle='#cfe0d6';g.fillRect(0,0,W,H);
 C.draw(g,'wall',C.lumpy(C.roundRect(-40,-40,2000,820,30),'wall',3,4),'#cfe0d6',{bevel:14,shine:0.2,shadow:false,prints:6,marks:30});
 C.draw(g,'table',C.lumpy(C.roundRect(-40,720,2000,420,40),'table',4,4),'#d9a36c',{bevel:16,shine:0.3,shadowOffset:[0,-6],prints:5,marks:40});
 // clay mandir
 const mx=640,my=740;
 C.shadow(g,mx,my+16,300,30,0.35);
 C.draw(g,'mbase',C.lumpy(C.roundRect(mx-280,my-120,560,120,18),'mb'+v,3),'#c96f4a',{variant:v,bevel:12,shine:0.5});
 C.draw(g,'mshik',C.lumpy([[mx-190,my-120],[mx+190,my-120],[mx,my-430]],'ms'+v,4),'#e0b154',{variant:v,bevel:12,shine:0.6});
 C.draw(g,'mkal',C.lumpy(C.ellipse(mx,my-452,30,34,10),'mk'+v,2),'#d2563f',{variant:v,bevel:10,shine:0.8});
 // clay naag hops in
 const hx=Math.min(1500,1780-E.out(E.seg(tq,0.6,2.0))*280);
 const hop=Math.abs(Math.sin(tq*Math.PI*1.5))*90*(tq<3?1:0.2);
 C.shadow(g,hx,my+10,130,20,0.35);
 const seg1=[[hx+150,my-20],[hx+70,my-60],[hx-10,my-30],[hx-60,my-90-hop*0.4]];
 C.draw(g,'snbody',C.capsule(seg1,34),'#5f9e62',{variant:v,bevel:10,shine:0.5});
 C.draw(g,'snhood',C.lumpy(C.ellipse(hx-70,my-150-hop,52,62,12),'sh'+v,2.4),'#4c8a50',{variant:v,bevel:10,shine:0.7});
 g.fillStyle='#1d1d24';
 g.beginPath();g.arc(hx-88,my-160-hop,7,0,7);g.fill();
 g.beginPath();g.arc(hx-52,my-160-hop,7,0,7);g.fill();
 if(t>2.4)C.text(g,'ttl','PATAL',960,330,170,'#1f3a8a',{font:'Shrikhand',align:'center',variant:v,tilt:-0.03});
}
// ---------------- SEG 3 : LINE ----------------
function segLine(t){
 const L=LineArt;
 L.paper(g,env);
 // hill profile + shaft + chamber: hand-drawn cross-section
 L.stroke(g,[[80,420],[420,300],[700,210],[1100,240],[1500,330],[1840,420]],{t,seed:'hill',width:6,jitter:3});
 L.stroke(g,[[80,420],[80,980],[1840,980],[1840,420]],{t,seed:'frame',width:4,jitter:2});
 // descending shaft steps
 const steps=[[900,240],[900,420],[840,470],[900,520],[840,580],[900,640],[860,700]];
 L.stroke(g,steps,{t,seed:'shaft',width:6,jitter:2.5});
 L.stroke(g,L.circle(880,810,120),{t,seed:'chamber',width:6,jitter:3,closed:true});
 // explorer descends with progress
 const p=Math.min(1,t/6),ex=900-40*Math.sin(p*9),ey=250+p*430;
 L.stroke(g,L.circle(ex,ey-36,16),{t,seed:'head',width:4,closed:true});
 L.stroke(g,[[ex,ey-20],[ex,ey+16]],{t,seed:'bod',width:4});
 L.stroke(g,[[ex,ey+16],[ex-12,ey+42]],{t,seed:'l1',width:4});
 L.stroke(g,[[ex,ey+16],[ex+12,ey+42]],{t,seed:'l2',width:4});
 // arrow + labels
 L.stroke(g,[[1060,300],[1060,760],[1040,730]],{t,seed:'arrow',width:5,jitter:2});
 L.stroke(g,[[1060,760],[1080,730]],{t,seed:'arrow2',width:5,jitter:2});
 g.font='46px Hand';g.fillStyle=L.INK;g.textAlign='left';
 const d=Math.floor(t*12);
 g.fillText('90 FT NEECHE',1120,560+(d%3-1)*1.5);
 g.fillText('GUFA',700,860+(d%3-1)*1.5);
 g.fillText('PAHAAD',360,260+(d%3-1)*1.5);
 if(t>4){g.font='40px Hand';g.fillText('SHESHNAG KI PEETH \u2192',1120,830+(d%3-1)*1.5);}
}
// ---------------- SEG 4 : GROOVY ----------------
function segGroovy(t){
 const P=Groovy.PAL.sunset,E=Ease;
 g.fillStyle='#2a0a18';g.fillRect(0,0,W,H);
 Groovy.sunburst(g,env,960,470,26,t*0.22,[P.c[0],P.c[3]]);
 Groovy.rings(g,960,470,6,62,t,[P.c[1],P.c[2],P.c[4],P.c[0]]);
 const beat=Motion.pulse(t,120);
 const blob=Groovy.wavy(Groovy.ellipse(960,470,230*(1+beat*0.05),200,96),14,6,t*2.6);
 Groovy.shape(g,blob,P.c[2],{ink:P.ink,width:8,echoes:[P.c[1],P.c[0]],echoStep:11});
 const drop=E.out(E.seg(t,0.5,1.2));
 Groovy.melt(g,env,'RAHASYA',960,-140+(470+10)*drop,190,{t,melt:E.inOut(E.seg(t,2.2,6.5)),wave:9,fill:P.c[4],echo:P.c[1],ink:P.ink});
}
// ---------------- SEG 5 : LIQUID + KALEIDO ----------------
function segLiquid(t){
 const blobs=Liquid.drift('pataldemo',9,t,env,{rMin:80,rMax:170,speed:0.32,hues:[300,20,190,40,260]});
 Liquid.field(g,env,blobs,{hueShift:t*22,res:340});
 const ks=ss(3.2,4.6,t);
 if(ks>0){
  const cols=['#ff2e88','#ffd23f','#18d6c4','#7a2cff','#c6ff2e'];
  Kaleido.draw(g,env,{n:10,rot:t*0.4,hue:t*35,scale:ks,
   source:(s)=>{const r=Motion.rng('pz');
    for(let i=0;i<24;i++){const a=r()*0.7,d2=((r()*560+t*110)%620)+30;
     s.fillStyle=cols[i%cols.length];s.beginPath();
     s.ellipse(960+Math.cos(a)*d2,540+Math.sin(a)*d2,16+r()*42,9+r()*20,a+t,0,Math.PI*2);s.fill();}},});
  Kaleido.beads(g,960,540,100,16,10,t,cols);
 }
}
function endCard(lt){
 g.fillStyle='#07050a';g.fillRect(0,0,W,H);
 const a=ss(0,0.5,lt);
 if(logoOk){const s2=380;g.save();g.globalAlpha=a;
  g.drawImage(LOGOIM,960-s2/2,180,s2,s2);g.restore();}
 T(960,660,'6 \u0928\u090f \u0938\u094d\u091f\u093e\u0907\u0932 \u2014 \u0915\u093f\u091f \u0924\u0948\u092f\u093e\u0930','Deva',56,'#eef2f8','center',a);
 T(960,740,'COMIC \u00b7 RISO \u00b7 CLAY \u00b7 LINE \u00b7 70s \u00b7 LIQUID+KALEIDO','Mono',30,'#ff8c3b','center',a,2);
 T(960,810,'drawn-by-code (MIT) \u00d7 CHRONIC OF HISTORIC pipeline','Mono',22,'rgba(238,242,248,0.6)','center',a*ss(0.4,0.9,lt),1);
 const out=ss(2.0,2.9,lt);
 if(out>0){g.save();g.globalAlpha=out;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
const SEGS=[segComic,segRiso,segClay,segLine,segGroovy,segLiquid];
function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 if(t>=NSEGxSEG){endCard(t-NSEGxSEG);return;}
 const si=Math.min(NSEG-1,Math.floor(t/SEG)),lt=t-si*SEG;
 SEGS[si](lt);
 band(si,lt);
 const fl=1-ss(0,0.12,lt);
 if(fl>0&&si>0){g.save();g.globalAlpha=fl*0.5;g.fillStyle='#fff';g.fillRect(0,0,W,H);g.restore();}
 g.save();g.fillStyle='rgba(255,255,255,0.25)';g.fillRect(0,H-4,W,4);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
}
const NSEG=6,NSEGxSEG=NSEG*SEG;
window.renderAt=function(t){draw(t);return cv.toDataURL('image/jpeg',0.85);};
window.renderBatch=function(ts){const out=[];for(const t of ts){draw(t);out.push(cv.toDataURL('image/jpeg',0.85));}return out;};
document.fonts.ready.then(()=>{try{
 ['Bangers','Comic Neue','Shrikhand','Hand','Mono','InterB','Deva'].forEach(f=>{g.font='30px "'+f+'"';g.fillText('Ag \u0905',-100,-100);});
 press=Riso.press(env);
 draw(1);draw(12);draw(25);draw(40);draw(52);draw(58.5);
 window.__ready=true;
}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff).replace("KITSCRIPTS", scripts)
    html = html.replace("__TOT__", str(TOTAL)).replace("LOGO64", b64(LOGO))
    hp = os.path.join(ROOT, "page.html")
    open(hp, "w").write(html)
    return hp

def run(mode):
    os.makedirs(ROOT, exist_ok=True)
    hp = build_html()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True,
                                    args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 200, "height": 200})
        page.goto("file://" + hp)
        try:
            page.wait_for_function("window.__ready === true || window.__err", timeout=120000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            chk = os.environ.get("CHK_TIMES", "2,5,12,16,21,25,31,35,40,45,50,54,58.5")
            TSL = [float(x) for x in chk.split(",")]
            ims = []
            for st in TSL:
                d = page.evaluate("window.renderAt(%f)" % st)
                ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))))
            tw, th = 480, 270
            cols = 3; rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw, rows * th), "black")
            for i, im in enumerate(ims):
                sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
            sheet.save(os.path.join(ROOT, "preview_sheet.jpg"), quality=86)
            browser.close(); print("preview ->", os.path.join(ROOT, "preview_sheet.jpg")); return
        FR = os.path.join(ROOT, "frames"); os.makedirs(FR, exist_ok=True)
        n = int(round(TOTAL * FPS)); t0 = time.time(); i = 0
        while i < n:
            batch = [k for k in range(i, min(i + 10, n))
                     if not os.path.exists(os.path.join(FR, "%05d.jpg" % k))]
            if batch:
                urls = page.evaluate("ts => window.renderBatch(ts)", [k / FPS for k in batch])
                for k, d in zip(batch, urls):
                    open(os.path.join(FR, "%05d.jpg" % k), "wb").write(base64.b64decode(d.split(",", 1)[1]))
            i += 10
            if (i // 10) % 30 == 0:
                print("frame %d/%d (%.1f fps)" % (i, n, i / max(0.01, time.time() - t0)), flush=True)
        browser.close()
    build_audio()
    print("FRAMES+AUDIO DONE n=%d" % n)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
