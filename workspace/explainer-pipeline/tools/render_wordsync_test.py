#!/usr/bin/env python3
# WORD-SYNC PAPER-CUT TEST — proves: (1) VO word bolte hi uska visual pop,
# (2) torn-paper cutout chits (photos/engravings), (3) dynamic map route anim,
# (4) real-video B-roll underneath. ~21s @ 1920x1080.
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/wtest"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
PR = os.path.join(ASSETS, "props")
PT = os.path.join(ASSETS, "patal")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
FPS = 30
W, H = 1920, 1080
LEAD = 0.5
VODUR = 19.01
TOTAL = round(LEAD + VODUR + 1.5, 2)

TEXT = ("मान लो कहानी में आया… एक पुराना नक्शा। नक्शा बोलते ही… नक्शा सामने। "
        "फिर आया मंदिर… तो मंदिर की असली तस्वीर। और जैसे ही बोला… खज़ाना। "
        "सोना सीधा स्क्रीन पर। हर शब्द के साथ उसका विज़ुअल — यही है अपना नया स्टाइल।")
WORDS = TEXT.split()

def word_times():
    wts = []
    cl = [len(w) + 1 for w in WORDS]
    tot = float(sum(cl)); acc = 0
    for w, c in zip(WORDS, cl):
        s = LEAD + VODUR * acc / tot
        e = LEAD + VODUR * (acc + c) / tot
        wts.append({"w": w, "s": round(s, 3), "e": round(e, 3)})
        acc += c
    return wts

def strip_p(w): return w.strip("।…—,.?!")

def find_time(wts, key, occ=1):
    k = 0
    for wt in wts:
        if strip_p(wt["w"]) == key:
            k += 1
            if k == occ: return wt["s"]
    raise ValueError(key)

def b64(p): return base64.b64encode(open(p, "rb").read()).decode()

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
def thud(a):
    d = 0.4
    x = tone(d, 85, 38, a) * np.exp(-np.arange(_n(d)) / SR * 9)
    nz = envad(box(noise(0.12, 9), 24) * 2.2, 0.004, 0.1)
    x[:len(nz)] += nz * a
    return x
def paper(a=0.5):  # paper rustle snap
    x = noise(0.16, 23); hp = x - box(x, 18)
    return envad(hp * 2.2, 0.004, 0.1) * a
def ping(f, a, d=0.5):
    t = np.arange(_n(d)) / SR
    return a * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)

def build_audio(evts):
    n = _n(TOTAL)
    sfx = np.zeros(n)
    def put(x, at, g=1.0):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); sfx[i:i + L] += x[:L] * g
    put(whoosh(0.6, 0.3), 0.05)
    put(whoosh(0.4, 0.2), 10.0 - 0.12)
    for e in evts:
        put(paper(0.7), e["t"] - 0.04); put(thud(0.5), e["t"])
    put(ping(880, 0.2, 1.0), evts[-1]["t"] + 0.1)
    wv = os.path.join(ROOT, "tvo.wav")
    if not os.path.exists(wv):
        subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(PR, "tvo_demo.mp3"),
                        "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
    wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
    wf.close()
    vo = np.zeros(n); i0 = _n(LEAD); L = min(len(dat), n - i0)
    vo[i0:i0 + L] += dat[:L] * 1.3
    t = np.arange(n) / SR
    drone = 0.028 * (np.sin(2 * np.pi * 73.42 * t) + np.sin(2 * np.pi * 73.75 * t + 0.8))
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    drone *= (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.8 + drone
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok %.1fs" % TOTAL)

def build_html(wts, evts):
    fonts = {"Anton": FONTS + "/Anton-Regular.ttf", "InterB": FONTS + "/Inter-Black.ttf",
             "Mono": FONTS + "/JetBrainsMono-Bold.ttf", "Deva": "/var/tmp/ujjain/TiroDeva.ttf"}
    ff = "\n".join("@font-face{font-family:'%s';src:url('file://%s');}" % (k, v) for k, v in fonts.items())
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body><script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,TOTAL=__TOT__,WTS=WTSJ,EVTS=EVTSJ;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const ov=x=>{x=clamp(x,0,1);const c=1.7,u=x-1;return 1+u*u*((c+1)*u+c)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
const CYAN='#4dd8ff',ORG='#ff8c3b',PAPER='#eef2f8',RED='#e8503a',GOLD='#e8b24a';
const IMGS={};let nimg=0,want=3;
function ld(k,s){const im=new Image();im.onload=()=>nimg++;im.src=s;IMGS[k]=im;}
ld('map','data:image/jpeg;base64,MAP64');
ld('temple','data:image/jpeg;base64,TEMPLE64');
ld('khz','data:image/jpeg;base64,KHZ64');
const VIDS={};let nvid=0;const wantvid=2;
function lv(k,b){const v=document.createElement('video');v.muted=true;v.preload='auto';
 v.addEventListener('loadeddata',()=>nvid++);v.src='data:video/mp4;base64,'+b;VIDS[k]=v;}
lv('rock','VROCK64');lv('valley','VVALLEY64');
function seekV(v,t){return new Promise(r=>{const tt=Math.max(0.04,Math.min(t,v.duration-0.06));
 if(Math.abs(v.currentTime-tt)<0.001)return r();
 const h=()=>{v.removeEventListener('seeked',h);r();};v.addEventListener('seeked',h);v.currentTime=tt;});}
function coverV(v,zoom,cx,cy,dim){
 const vw=v.videoWidth,vh=v.videoHeight;if(!vw)return;
 const sc=Math.max(W/vw,H/vh)*zoom;
 g.drawImage(v,W*cx-vw*sc*cx,H*cy-vh*sc*cy,vw*sc,vh*sc);
 if(dim>0){g.save();g.globalAlpha=dim;g.fillStyle='#050308';g.fillRect(0,0,W,H);g.restore();}}
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
function rrect(x,y,w2,h2,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w2,y,x+w2,y+h2,r);g.arcTo(x+w2,y+h2,x,y+h2,r);g.arcTo(x,y+h2,x,y,r);g.arcTo(x,y,x+w2,y,r);g.closePath();}
// ---- torn paper-cut edge path ----
function tornPath(w2,h2,seed,m){
 const r=rng(seed);const pts=[];
 const step=46;
 for(let x=-w2/2;x<w2/2;x+=step)pts.push([x+r()*10,-h2/2-m+(r()-0.5)*14]);
 for(let y=-h2/2;y<h2/2;y+=step)pts.push([w2/2+m+(r()-0.5)*14,y+r()*10]);
 for(let x=w2/2;x>-w2/2;x-=step)pts.push([x-r()*10,h2/2+m+(r()-0.5)*14]);
 for(let y=h2/2;y>-h2/2;y-=step)pts.push([-w2/2-m+(r()-0.5)*14,y-r()*10]);
 g.beginPath();g.moveTo(pts[0][0],pts[0][1]);
 for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);
 g.closePath();}
// paper-cut chit: torn white paper border + image + tape + label
function papercut(t,t0,im,x,y,wpx,rot,labL,labR,labCol,seed,route){
 const p=ss(t0,t0+0.38,t);if(p<=0)return;
 const hpx=wpx*im.height/im.width;
 const drop=(1-ov(p))*-90;
 g.save();g.globalAlpha=Math.min(1,p*1.2);
 g.translate(x,y+drop);g.rotate(rot+0.01*Math.sin(t*1.1+seed));
 const sc=0.92+0.08*ov(p);g.scale(sc,sc);
 g.shadowColor='rgba(0,0,0,0.65)';g.shadowBlur=34;g.shadowOffsetY=14;
 g.fillStyle='#f3eee0';tornPath(wpx,hpx,seed,20);g.fill();
 g.shadowColor='transparent';
 g.save();tornPath(wpx,hpx,seed+1,2);g.clip();
 g.drawImage(im,-wpx/2,-hpx/2,wpx,hpx);g.restore();
 if(route){ // animated dashed route + moving dot over map
  const q=ss(t0+0.5,t0+2.6,t);
  if(q>0){const P=[[-wpx*0.26,hpx*0.02],[-wpx*0.05,-hpx*0.12],[wpx*0.18,-hpx*0.05],[wpx*0.30,-hpx*0.20]];
   g.save();g.strokeStyle='#b8401e';g.lineWidth=6;g.setLineDash([16,12]);
   g.lineDashOffset=-t*40;
   g.beginPath();g.moveTo(P[0][0],P[0][1]);
   const seg=q*(P.length-1);
   for(let i=1;i<P.length;i++){
    const f=clamp(seg-(i-1),0,1);if(f<=0)break;
    const a=P[i-1],b2=P[i];
    g.lineTo(a[0]+(b2[0]-a[0])*f,a[1]+(b2[1]-a[1])*f);}
   g.stroke();g.setLineDash([]);
   const si=Math.floor(clamp(seg,0,P.length-1.001)),f2=seg-si;
   const dx=P[si][0]+(P[Math.min(si+1,P.length-1)][0]-P[si][0])*f2;
   const dy=P[si][1]+(P[Math.min(si+1,P.length-1)][1]-P[si][1])*f2;
   g.fillStyle=ORG;g.beginPath();g.arc(dx,dy,10,0,6.29);g.fill();
   if(q>=1){g.strokeStyle=RED;g.lineWidth=7;
    const X=P[3];g.beginPath();g.moveTo(X[0]-16,X[1]-16);g.lineTo(X[0]+16,X[1]+16);
    g.moveTo(X[0]+16,X[1]-16);g.lineTo(X[0]-16,X[1]+16);g.stroke();}
   g.restore();}}
 // tape strip
 g.fillStyle='rgba(232,226,200,0.55)';g.strokeStyle='rgba(180,170,140,0.4)';g.lineWidth=1;
 g.save();g.rotate(-0.06);g.fillRect(-70,-hpx/2-34,140,36);g.strokeRect(-70,-hpx/2-34,140,36);g.restore();
 // labels
 g.fillStyle='#2a2318';g.font='26px Mono';g.textAlign='left';g.textBaseline='middle';
 g.fillText(labL,-wpx/2+6,hpx/2+44);
 g.font='19px Mono';g.fillStyle=labCol;g.textAlign='right';
 g.fillText(labR,wpx/2-4,hpx/2+44);
 g.restore();}
// kinetic word pop above prop
function kword(t,t0,txt,x,y,col){
 const p=ss(t0,t0+0.2,t);if(p<=0)return;
 const a=p*(1-ss(t0+1.6,t0+2.1,t));if(a<=0)return;
 const sc=1.7-0.7*ov(p);
 g.save();g.globalAlpha=a;g.translate(x,y);g.scale(sc,sc);g.rotate(-0.03);
 g.font='64px Deva';g.textAlign='center';g.textBaseline='middle';
 g.lineWidth=10;g.strokeStyle='rgba(5,3,8,0.85)';g.strokeText(txt,0,0);
 g.fillStyle=col;g.fillText(txt,0,0);g.restore();}
function stamp(t,t0,x,y,txt,color,size){
 const p=ss(t0,t0+0.22,t);if(p<=0)return;
 const s=2.0-1.0*ov(p);
 g.save();g.translate(x,y);g.rotate(-0.06);g.scale(s,s);g.globalAlpha=p*0.95;
 g.strokeStyle=color;g.fillStyle=color;g.lineWidth=6;
 g.font=size+'px Deva';g.textAlign='center';g.textBaseline='middle';
 const tw=g.measureText(txt).width;
 rrect(-tw/2-28,-size*0.88,tw+56,size*1.76,10);g.stroke();g.fillText(txt,0,3);g.restore();}
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=13;}nc.putImageData(id,0,0);}
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.4,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(4,2,6,0.58)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
function captions(t){
 let cur=-1;
 for(let i=0;i<WTS.length;i++)if(t>=WTS[i].s&&t<WTS[i].e)cur=i;
 if(cur<0&&t>=WTS[WTS.length-1].e)return;
 // sliding window of 7 words centered on current
 const a=Math.max(0,cur-3),b2=Math.min(WTS.length,a+8);
 g.save();g.font='40px Deva';g.textBaseline='middle';
 let tw=0;const meas=[];
 for(let i=a;i<b2;i++){const m=g.measureText(WTS[i].w+' ').width;meas.push(m);tw+=m;}
 let x=W/2-tw/2;const y=1004;
 g.shadowColor='rgba(0,0,0,0.8)';g.shadowBlur=10;
 for(let i=a;i<b2;i++){
  const on=i===cur, past=i<cur;
  g.fillStyle=on?ORG:'#ffffff';
  g.globalAlpha=on?1:(past?0.85:0.35);
  g.textAlign='left';g.fillText(WTS[i].w,x,y);
  if(on){g.fillRect(x,y+30,g.measureText(WTS[i].w).width,4);}
  x+=meas[i-a];}
 g.restore();}
async function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 const first=t<10.0;
 const v=first?VIDS.rock:VIDS.valley;
 const since=first?t:(t-10.0);
 if(v&&v.duration)await seekV(v,(0.3+since*0.85)%(v.duration-0.12));
 const punch=1+0.05*Math.exp(-since*4);
 if(v&&v.videoWidth)coverV(v,(first?1.12:1.08)*punch,0.5,0.5,first?0.42:0.3);
 else{g.fillStyle='#07050a';g.fillRect(0,0,W,H);}
 // header
 const ha=ss(0.3,0.9,t);
 if(ha>0){g.save();g.globalAlpha=ha;g.strokeStyle='rgba(222,234,248,0.6)';g.lineWidth=2;
  g.beginPath();g.moveTo(140,86);g.lineTo(1780,86);g.stroke();
  g.font='26px Mono';g.textBaseline='bottom';
  g.fillStyle=GOLD;g.textAlign='left';g.fillText('UPGRADE TEST \u00b7 WORD-SYNC PAPER-CUT',140,76);
  g.fillStyle='rgba(222,234,248,0.6)';g.textAlign='right';g.fillText('CHRONIC JOURNAL',1780,76);g.restore();}
 // events
 for(const e of EVTS){
  if(e.k==='map'){
   papercut(t,e.t,IMGS.map,540,520,640,-0.04,'PURANA NAKSHA','AI ART','#7a5a20',11,true);
   kword(t,e.t,'\u0928\u0915\u094d\u0936\u093e',540,218,ORG);}
  if(e.k==='temple'){
   papercut(t,e.t,IMGS.temple,1250,480,400,0.05,'GUFA MANDIR','REAL PHOTO','#2a6a3a',22,false);
   kword(t,e.t,'\u092e\u0902\u0926\u093f\u0930',1250,212,CYAN);}
  if(e.k==='khz'){
   papercut(t,e.t,IMGS.khz,1560,760,480,-0.06,'KHAZANA','AI ART','#7a5a20',33,false);
   kword(t,e.t,'\u0916\u095b\u093e\u0928\u093e',1560,478,GOLD);}
  if(e.k==='stamp'){
   stamp(t,e.t,960,310,'\u0939\u0930 \u0936\u092c\u094d\u0926 \u0915\u093e \u0935\u093f\u095b\u0941\u0905\u0932',ORG,46);}}
 captions(t);
 g.save();g.fillStyle='rgba(255,255,255,0.18)';g.fillRect(0,H-4,W,4);
 g.fillStyle=ORG;g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
 g.save();g.globalAlpha=0.4;
 g.drawImage(noiseCv,-(Math.floor(t*13)%19),-(Math.floor(t*7)%23),W+40,H+40);g.restore();
 g.drawImage(vig,0,0);
 const fi=ss(0,0.5,t);
 if(fi<1){g.save();g.globalAlpha=1-fi;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
 const out=ss(TOTAL-0.8,TOTAL-0.1,t);
 if(out>0){g.save();g.globalAlpha=out;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}}
window.renderAt=async function(t){await draw(t);return cv.toDataURL('image/jpeg',0.84);};
window.renderBatch=async function(ts){const out=[];
 for(const t of ts){await draw(t);out.push(cv.toDataURL('image/jpeg',0.84));}return out;};
document.fonts.ready.then(()=>{try{
 ['Anton','InterB','Mono','Deva'].forEach(f=>{g.font='30px '+f;g.fillText('Ag \u0905',-100,-100);});
 const wait=()=>{if(nimg>=want&&nvid>=wantvid){
  Promise.resolve().then(async()=>{await draw(1);await draw(8);await draw(15);window.__ready=true;}).catch(e=>{window.__err=''+(e.stack||e);});
 }else setTimeout(wait,60);};
 wait();}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff)
    html = html.replace("__TOT__", str(TOTAL))
    html = html.replace("WTSJ", json.dumps(wts)).replace("EVTSJ", json.dumps(evts))
    html = html.replace("MAP64", b64(PR + "/prop_map.jpg"))
    html = html.replace("TEMPLE64", b64(PT + "/photo_shrine.jpg"))
    html = html.replace("KHZ64", b64(PR + "/prop_khazana.jpg"))
    html = html.replace("VROCK64", b64("/var/tmp/stock/9758.mp4"))
    html = html.replace("VVALLEY64", b64("/var/tmp/stock/15919.mp4"))
    hp = os.path.join(ROOT, "page.html")
    open(hp, "w").write(html)
    return hp

def run(mode):
    os.makedirs(ROOT, exist_ok=True)
    wts = word_times()
    evts = [
        {"k": "map", "t": find_time(wts, "नक्शा", 1)},
        {"k": "temple", "t": find_time(wts, "मंदिर", 1)},
        {"k": "khz", "t": find_time(wts, "खज़ाना", 1)},
        {"k": "stamp", "t": find_time(wts, "विज़ुअल", 1)},
    ]
    print("events:", [(e["k"], round(e["t"], 2)) for e in evts])
    hp = build_html(wts, evts)
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
            chk = os.environ.get("CHK_TIMES", "2,5,8,11,14,17")
            ims = []
            for st in [float(x) for x in chk.split(",")]:
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
            if (i // 10) % 20 == 0:
                print("frame %d/%d (%.1f fps)" % (i, n, i / max(0.01, time.time() - t0)), flush=True)
        browser.close()
    build_audio(evts)
    print("FRAMES+AUDIO DONE n=%d" % n)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
