#!/usr/bin/env python3
# UJJAIN: TIME KA ZERO POINT — 16:9 long-form (~3:11), CHRONIC JOURNAL grammar.
# 9 FIG chapters, one evolving canvas each, VO-lockstep pulses, generative music bed
# with VO ducking, illustrated world assets + code motion. Hindi VO (voice-06).
import os, sys, io, json, base64, time, subprocess, wave, re
import numpy as np
from PIL import Image

ROOT = "/var/tmp/ulong"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
U10 = os.path.join(ASSETS, "u10")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FPS = 30
W, H = 1920, 1080
ORDER = ["s1", "s1b", "s2", "s2b", "s3", "s4", "s3b", "s5", "s6"]
DUR = [18.76, 16.32, 27.84, 19.12, 20.64, 16.96, 19.92, 19.24, 16.2]
LEAD, GAP = 0.5, 1.0
BEATS = []
_t = 0.0
for d in DUR:
    BEATS.append(round(_t, 2)); _t += LEAD + d + GAP
TOTAL = round(_t + 2.5, 2)  # 191.0

CAPTXT = [
 ["1884 se pehle... duniya ki ghadi London se nahi chalti thi.",
  "Hazaron saal tak time ka center tha ek Bharatiya shehar — UJJAIN.",
  "Mahakal ki nagri — jahan KAAL ka matlab hi hai... SAMAY.",
  "Lekin poori duniya ka time... yahin se KYON?"],
 ["Ye sirf khagolshastra nahi tha.",
  "12 jyotirlingon mein akela DAKSHINMUKHI — Mahakaleshwar.",
  "Kaal ke devta ki nagri mein... samay ki rekha.",
  "Ye sanyog nahi tha... ye SOCH thi."],
 ["Chauthi shatabdi ka granth — SURYA SIDDHANTA.",
  "Dharti gol hai... aur us par ek rekha — MADHYAREKHA.",
  "Ujjain se nikli... Rohtak se guzri...",
  "Bhumadhya rekha par jis bindu se mili — uska naam tha... LANKA.",
  "Aryabhat se Brahmagupta, Bhaskaracharya tak — har ganit yahin se shuru."],
 ["Lekin ye jagah chuni kyon gayi?",
  "Surya Siddhanta ke anusar — yahan 0 aur KARK REKHA ek dusre ko kaatti thin.",
  "Aasman naapne ke liye isse behtar jagah thi hi nahi.",
  "Isiliye Ujjain ban gaya... PRACHEEN duniya ka GREENWICH."],
 ["San 530 ke aaspaas — VARAHAMIHIRA ne likh diya:",
  "Ujjain se poorab ho toh time GHATAO. Paschim ho toh BADHAO.",
  "Har 53 yojan par... ek naadi.",
  "Ye TIME ZONES hain. Europe se 1300 saal pehle."],
 ["Phir aaya 1884. Washington mein 25 deshon ki baithak.",
  "INTERNATIONAL MERIDIAN CONFERENCE.",
  "Ek vote hua... aur shunya rekha GREENWICH chali gayi.",
  "2000 saal purani rekha... ek din mein itihas ban gayi."],
 ["Is virasat ko marne nahi diya gaya.",
  "1725 ke aaspaas — Sawai Jai Singh ne banayi VEDH SHALA.",
  "Patthar ke vishal yantra... bina kisi lens ke, grahon ki chaal.",
  "Aur ye vedhshala AAJ BHI ZINDA hai."],
 ["Aaj bhi har PANCHANG, har kundali, har muhurat...",
  "Ujjain ke samay par hi banta hai.",
  "IST se 29 MINUTE peechhe.",
  "Ghadi badal gayi... CENTER nahi badla."],
 ["Ab sawaal tumhara hai —",
  "Kya shunya rekha wapas UJJAIN aani chahiye?",
  "COMMENT mein likho: 1 HAAN \u00b7 2 NAHIN.",
  "Case... abhi bhi khula hai."],
]
HI = set(("UJJAIN KAAL SAMAY KYON DAKSHINMUKHI SOCH SURYA SIDDHANTA MADHYAREKHA LANKA "
          "KARK REKHA PRACHEEN GREENWICH VARAHAMIHIRA GHATAO BADHAO TIME ZONES 1300 530 "
          "1884 25 2000 VEDH SHALA 1725 ZINDA PANCHANG 29 MINUTE CENTER COMMENT HAAN NAHIN 0 12").split())


def make_caps():
    caps = []
    for i, chunks in enumerate(CAPTXT):
        wcounts = [len(c.split()) for c in chunks]
        tot = sum(wcounts)
        t0 = BEATS[i] + LEAD
        acc = 0
        for c, wc in zip(chunks, wcounts):
            s = t0 + DUR[i] * acc / tot
            e = t0 + DUR[i] * (acc + wc) / tot
            caps.append({"start": round(s, 2), "end": round(min(e + 0.2, t0 + DUR[i] + 0.8), 2),
                         "words": c.split()})
            acc += wc
    return caps


def geo_segments():
    india, world = [], []
    cl = json.load(open(os.path.join(ASSETS, "world_110m.geojson")))
    bd = json.load(open(os.path.join(ASSETS, "world_borders_110m.geojson")))
    def rings(gj):
        for ft in gj["features"]:
            g = ft["geometry"]
            if g["type"] == "LineString": yield g["coordinates"]
            elif g["type"] == "MultiLineString":
                for r in g["coordinates"]: yield r
            elif g["type"] == "Polygon":
                for r in g["coordinates"]: yield r
            elif g["type"] == "MultiPolygon":
                for poly in g["coordinates"]:
                    for r in poly: yield r
    def clip(ring, lo0, lo1, la0, la1, step):
        seg, out = [], []
        for i in range(0, len(ring), step):
            lon, lat = ring[i][0], ring[i][1]
            if lo0 <= lon <= lo1 and la0 <= lat <= la1:
                seg.append([round(lon, 2), round(lat, 2)])
            else:
                if len(seg) > 2: out.append(seg)
                seg = []
        if len(seg) > 2: out.append(seg)
        return out
    for src in (cl, bd):
        for r in rings(src):
            india += clip(r, 67.5, 98.0, 5.5, 37.5, 1)
    for r in rings(cl):
        world += clip(r, -32, 102, -12, 62, 2)
    return india, world


def b64(p): return base64.b64encode(open(p, "rb").read()).decode()


# ================= AUDIO =================
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
def bell(d, base, a):
    t = np.arange(_n(d)) / SR; x = np.zeros(_n(d))
    for m, gn, dk in [(1, 1, 1.1), (2.01, .6, 1.7), (2.74, .45, 2.3), (3.76, .3, 3.1)]:
        x += gn * np.sin(2 * np.pi * base * m * t) * np.exp(-dk * t / d * 3)
    return a * x / 3 * np.exp(-t * 1.1)
def thud(a):
    d = 0.4
    x = tone(d, 85, 38, a) * np.exp(-np.arange(_n(d)) / SR * 9)
    nz = envad(box(noise(0.12), 24) * 2.2, 0.004, 0.1)
    x[:len(nz)] += nz * a
    return x
def whoosh(d, a):
    x = noise(d); bp = box(x, 10) - box(x, 120)
    t = np.arange(len(bp)) / len(bp)
    return a * bp * np.sin(np.pi * t) ** 2 * 6
def click(a=0.5):
    x = noise(0.02); return a * (x - box(x, 40)) * np.exp(-np.arange(len(x)) / 90.0)
def tickk(f=1500, a=0.33, d=0.05):
    return envad(tone(d, f, f * 0.7, a), 0.002, 0.03)
def pop(a=0.5):
    return envad(tone(0.12, 420, 880, a), 0.004, 0.06)

def music_bed(n):
    t = np.arange(n) / SR
    m = np.zeros(n)
    # section intensity envelope
    inten = np.zeros(n)
    I = [0.55, 0.62, 0.58, 0.62, 0.66, 0.78, 0.60, 0.72, 0.85]
    for i, b in enumerate(BEATS):
        e = BEATS[i + 1] if i + 1 < len(BEATS) else TOTAL
        i0, i1 = _n(b), min(_n(e), n)
        inten[i0:i1] = I[i]
    k = _n(2.0)
    inten = box(inten, k)  # smooth 2s crossfades
    # tanpura-ish drone: A2+E3+A3 with detune chorus
    for f, g in [(110.0, 1.0), (164.81, 0.55), (220.0, 0.38)]:
        m += g * (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.0035 * t + 1.3)) * 0.5
    m *= 0.045 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t + 1.0))
    # dawn shimmer (last two chapters): C#4 + E4 soft tremolo
    shim = (np.sin(2 * np.pi * 277.18 * t) * 0.6 + np.sin(2 * np.pi * 329.63 * t) * 0.5)
    senv = np.zeros(n)
    senv[_n(BEATS[7]):] = 1.0
    senv = box(senv, _n(4.0))
    m += shim * senv * 0.016 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.9 * t))
    m *= inten
    # soft pulse 78bpm during FIG03..FIG07
    pul = np.zeros(n)
    bt = BEATS[2]
    step = 60.0 / 78.0
    kbeat = 0
    while bt < BEATS[7]:
        i0 = _n(bt)
        ln = _n(0.12)
        if i0 + ln < n:
            tt = np.arange(ln) / SR
            pul[i0:i0 + ln] += np.sin(2 * np.pi * 58 * tt) * np.exp(-tt * 34) * 0.42
            if kbeat % 2 == 1:
                ck = click(0.12)
                pul[i0:i0 + len(ck)] += ck
        bt += step; kbeat += 1
    pe = np.zeros(n); pe[_n(BEATS[2]):_n(BEATS[7])] = 1.0
    pul *= box(pe, _n(1.5))
    m += pul
    # risers before each chapter
    for b in BEATS[1:]:
        r = envad(box(noise(1.2, 11), 8) - box(noise(1.2, 11), 100), 1.0, 0.18) * 1.6
        i0 = _n(b - 1.2)
        if i0 >= 0:
            ln = min(len(r), n - i0); m[i0:i0 + ln] += r[:ln] * 0.16
    # final resolve: A major swell over last 7s
    fin = np.zeros(n)
    f0 = _n(TOTAL - 7)
    tt = np.arange(n - f0) / SR
    chord = (np.sin(2 * np.pi * 220 * tt) + 0.7 * np.sin(2 * np.pi * 277.18 * tt)
             + 0.6 * np.sin(2 * np.pi * 329.63 * tt))
    env = np.minimum(tt / 3.0, 1.0) * np.exp(-np.maximum(tt - 4.5, 0) * 0.9)
    fin[f0:] = chord * env * 0.030
    m += fin
    return m

def build_audio():
    n = _n(TOTAL)
    sfx = np.zeros(n)
    def put(x, at, g=1.0):
        i = _n(at)
        if 0 <= i < n:
            mlen = min(len(x), n - i); sfx[i:i + mlen] += x[:mlen] * g
    B = BEATS
    # chapter transition whooshes
    for b in B[1:]:
        put(whoosh(0.6, 0.35), b - 0.3)
    # FIG01: typewriter + UJJAIN slam + bell + question type
    put(bell(3.2, 392, 0.3), 0.4)
    for k in range(16): put(click(0.35), 0.9 + k * 0.1)
    put(thud(0.95), B[0] + 5.0); put(bell(2.4, 523, 0.22), B[0] + 5.05)
    for k in range(22): put(click(0.3), B[0] + 15.2 + k * 0.09)
    # FIG02: bell + 12 dot ticks + slam
    put(bell(2.8, 440, 0.3), B[1] + 0.4)
    for k in range(12): put(tickk(1100 + (60 if k == 11 else 0), 0.3, 0.04), B[1] + 4.4 + k * 0.38)
    put(thud(0.7), B[1] + 9.3)
    # FIG03: map shimmer + line + lanka pulse + 3 pills
    put(envad(tone(1.8, 620, 1500, 0.11), 0.2, 0.5), B[2] + 7.6)
    put(tickk(900, 0.3), B[2] + 10.4)
    put(tickk(980, 0.3), B[2] + 13.3)
    put(bell(1.6, 660, 0.18), B[2] + 17.4)
    for k in range(3): put(thud(0.45), B[2] + 21.5 + k * 1.1)
    # FIG04: kark line + X slam + stamp
    put(envad(tone(1.4, 500, 1100, 0.11), 0.2, 0.5), B[3] + 5.6)
    put(thud(0.85), B[3] + 8.0)
    put(thud(0.9), B[3] + 14.6); put(bell(1.8, 587, 0.2), B[3] + 14.65)
    # FIG05: clock ticks + stamps
    for k in range(18): put(tickk(1200 if k % 2 else 800, 0.13, 0.03), B[4] + 4.0 + k * 0.55)
    put(thud(0.6), B[4] + 7.9); put(thud(0.6), B[4] + 10.6)
    for k in range(14): put(click(0.28), B[4] + 12.9 + k * 0.1)
    put(thud(1.0), B[4] + 17.3); put(bell(1.6, 660, 0.2), B[4] + 17.35)
    # FIG06: card drop + slide whoosh + stamps
    put(thud(0.5), B[5] + 3.9)
    put(whoosh(1.5, 0.5), B[5] + 10.3)
    put(envad(tone(1.5, 900, 300, 0.13), 0.1, 0.6), B[5] + 10.35)
    put(thud(0.6), B[5] + 13.0); put(thud(0.9), B[5] + 13.7)
    put(thud(0.9), B[5] + 15.3)
    # FIG07: yantra draw + sun sweep + stamp
    put(envad(tone(1.6, 420, 900, 0.10), 0.3, 0.5), B[6] + 4.6)
    for k in range(10): put(tickk(1000 + k * 40, 0.2, 0.035), B[6] + 9.0 + k * 0.5)
    put(thud(0.9), B[6] + 16.4); put(bell(2.0, 523, 0.22), B[6] + 16.45)
    # FIG08: 29 ticks + slams
    for k in range(29):
        q = k / 28.0
        put(tickk(1400 + 500 * q, 0.3, 0.04), B[7] + 8.2 + 2.4 * (q ** 0.8))
    put(thud(0.8), B[7] + 14.9); put(thud(1.0), B[7] + 16.9)
    # FIG09: riser + bell + pops + stamp
    put(bell(3.0, 490, 0.35), B[8] + 0.4)
    put(pop(0.5), B[8] + 6.4); put(pop(0.55), B[8] + 7.0)
    put(pop(0.5), B[8] + 9.6)
    put(thud(1.0), B[8] + 12.6); put(bell(2.4, 587, 0.25), B[8] + 12.65)
    # VO
    vo = np.zeros(n)
    for i, f in enumerate(ORDER):
        wv = os.path.join(ROOT, "vo_%s.wav" % f)
        if not os.path.exists(wv):
            subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(ROOT, "vo_%s.mp3" % f),
                            "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
        wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
        wf.close()
        i0 = _n(BEATS[i] + LEAD)
        mlen = min(len(dat), n - i0)
        vo[i0:i0 + mlen] += dat[:mlen] * 1.3
    # music with VO ducking
    mus = music_bed(n)
    env = box(np.abs(vo), _n(0.25))
    env = env / (env.max() + 1e-9)
    mus *= (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.8 + mus
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok %.1fs" % TOTAL)


# ================= HTML =================
def build_html():
    india, world = geo_segments()
    caps = make_caps()
    fonts = {"Anton": FONTS + "/Anton-Regular.ttf", "InterB": FONTS + "/Inter-Black.ttf",
             "InterS": FONTS + "/Inter-SemiBold.ttf", "Mono": FONTS + "/JetBrainsMono-Bold.ttf",
             "Yatra": "/var/tmp/ujjain/YatraOne.ttf", "Deva": "/var/tmp/ujjain/TiroDeva.ttf"}
    ff = "\n".join("@font-face{font-family:'%s';src:url('file://%s');}" % (k, v) for k, v in fonts.items())
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body><script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,TOTAL=__TOT__,B=BEATSJ,DUR=DURJ,LEAD=0.5,CAPS=CAPSJ,HI=HIJ;
const INDIA=INDIAJ, WORLD=WORLDJ;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const ov=x=>{x=clamp(x,0,1);const c=1.7,u=x-1;return 1+u*u*((c+1)*u+c)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
const IMGS={}; let nimg=0, wantimg=4;
function ld(k,src){const im=new Image();im.onload=()=>nimg++;im.src=src;IMGS[k]=im;}
ld('night','data:image/jpeg;base64,NIGHT64');
ld('dawn','data:image/jpeg;base64,DAWN64');
ld('astr','data:image/jpeg;base64,ASTR64');
ld('conf','data:image/jpeg;base64,CONF64');
const logo=new Image(); logo.onload=()=>nimg++; wantimg++;
logo.src='data:image/png;base64,LOGO64';
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=15;}nc.putImageData(id,0,0);}
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.4,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(8,5,2,0.5)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
const FIRE=[];const rf=rng(21);
for(let i=0;i<18;i++)FIRE.push([rf()*W,560+rf()*440,rf()*6.28,0.4+rf()*0.8]);
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
function rrect(x,y,w2,h2,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w2,y,x+w2,y+h2,r);g.arcTo(x+w2,y+h2,x,y+h2,r);g.arcTo(x,y+h2,x,y,r);g.arcTo(x,y,x+w2,y,r);g.closePath();}
function cover(im,zoom,cx,cy,panx){
 const sc=Math.max(W/im.width,H/im.height)*zoom;
 const dx=W*(cx||0.5)-im.width*sc*(cx||0.5)+(panx||0);
 const dy=H*(cy||0.5)-im.height*sc*(cy||0.5);
 g.drawImage(im,dx,dy,im.width*sc,im.height*sc);}
function figbar(lt,left,right,dark){
 const a=ss(0.2,0.8,lt); if(a<=0)return;
 const c=dark?'rgba(240,233,220,0.72)':'rgba(26,32,58,0.75)';
 const oc=dark?'#e8a33d':'#c9601e';
 g.save();g.globalAlpha=a;g.strokeStyle=c;g.lineWidth=2;
 g.beginPath();g.moveTo(140,86);g.lineTo(140+1640*ss(0.2,1.1,lt),86);g.stroke();
 g.font='26px Mono';g.textBaseline='bottom';
 g.fillStyle=oc;g.textAlign='left';g.fillText(left,140,76);
 g.fillStyle=c;g.textAlign='right';g.fillText(right,1780,76);g.restore();}
function stamp(lt,t0,x,y,txt,color,size,rot){
 const p=ss(t0,t0+0.22,lt); if(p<=0)return;
 const s=2.0-1.0*ov(p);
 g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);g.globalAlpha=p*0.95;
 g.strokeStyle=color;g.fillStyle=color;g.lineWidth=6;
 g.font=size+'px Mono';g.textAlign='center';g.textBaseline='middle';
 const tw=g.measureText(txt).width;
 rrect(-tw/2-28,-size*0.88,tw+56,size*1.76,10);g.stroke();
 g.fillText(txt,0,3);g.restore();
 const q=ss(t0+0.18,t0+0.8,lt);
 if(q>0&&q<1){g.save();g.globalAlpha=(1-q)*0.6;g.strokeStyle=color;g.lineWidth=3;
 g.beginPath();g.arc(x,y,70+300*q,0,6.29);g.stroke();g.restore();}}
function typew(lt,t0,txt,cps,x,y,font,size,color,align){
 if(lt<t0)return;const nch=Math.floor((lt-t0)*cps);const s=txt.slice(0,nch);
 const caret=(nch<txt.length)&&(Math.floor(lt*3)%2===0);
 T(x,y,s+(caret?'_':''),font,size,color,align||'left',Math.min(1,(lt-t0)*4));}
function kicker(lt,t0,small,big,ghostT){
 const p=ss(t0,t0+0.4,lt); if(p<=0)return;
 const gh=ghostT!=null?ss(ghostT,ghostT+0.4,lt):0;
 g.save();g.globalAlpha=p*(1-gh*0.82);
 T(140,176-20*gh,small,'Mono',32,'#e8a33d','left',1,6);
 g.globalAlpha=p*(1-gh*0.85);
 T(140,252-20*gh,big,'Anton',86,'#f3eee2','left');
 g.restore();}
function fireflies(t,alpha){
 for(const f of FIRE){const a=(alpha==null?1:alpha)*(0.2+0.5*Math.abs(Math.sin(t*f[3]+f[2])));
  const fx=f[0]+10*Math.sin(t*0.5+f[2]), fy=f[1]+6*Math.sin(t*0.33+f[2]*2);
  g.save();g.globalAlpha=a*0.75;g.fillStyle='#ffb14e';g.shadowColor='#ffb14e';g.shadowBlur=8;
  g.beginPath();g.arc(fx,fy,2.6,0,6.29);g.fill();g.restore();}}
function polaroid(lt,t0,im,x,y,wpx,rot,labL,labR,extra){
 const p=ss(t0,t0+0.45,lt); if(p<=0)return;
 const drop=(1-ov(p))*-70;
 const hpx=wpx*im.height/im.width;
 g.save();g.globalAlpha=p;
 g.translate(x,y+drop);g.rotate(rot+0.008*Math.sin(lt*0.9));
 g.shadowColor='rgba(0,0,0,0.55)';g.shadowBlur=32;g.shadowOffsetY=14;
 g.fillStyle='#efe6d2';g.fillRect(-wpx/2-12,-hpx/2-12,wpx+24,hpx+76);
 g.shadowColor='transparent';
 g.drawImage(im,-wpx/2,-hpx/2,wpx,hpx);
 g.fillStyle='#1a2030';g.font='34px Deva';g.textAlign='left';g.textBaseline='middle';
 g.fillText(labL,-wpx/2+6,hpx/2+34);
 g.font='20px Mono';g.fillStyle='rgba(26,32,48,0.72)';g.textAlign='right';
 g.fillText(labR,wpx/2-2,hpx/2+34);
 if(extra)extra(wpx,hpx);
 g.restore();}
// blueprint helpers
function blueprint(lt){
 g.fillStyle='#0c1733';g.fillRect(0,0,W,H);
 const gp=ss(0,1.0,lt);
 g.save();g.strokeStyle='rgba(110,150,220,0.13)';g.lineWidth=1;
 for(let x=0;x<=W;x+=60){if(x/W>gp)break;g.beginPath();g.moveTo(x,0);g.lineTo(x,H);g.stroke();}
 for(let y=0;y<=H;y+=60){if(y/H>gp)break;g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke();}
 g.restore();}
const MX=l=>1150+(l-68)*22.0, MY=l=>842-(l-6)*22.0;
function indiaMap(lt,t0){
 const mp=ss(t0,t0+2.4,lt); if(mp<=0)return 0;
 g.save();g.strokeStyle='rgba(140,180,255,0.75)';g.lineWidth=2.2;g.lineJoin='round';
 INDIA.forEach((seg,si)=>{
  const su=clamp(mp*INDIA.length-si,0,1);if(su<=0)return;
  const nn=Math.max(2,Math.floor(seg.length*su));
  g.beginPath();
  for(let i=0;i<nn;i++){const x=MX(seg[i][0]),y=MY(seg[i][1]);i?g.lineTo(x,y):g.moveTo(x,y);}
  g.stroke();});
 g.restore();return mp;}
// ---------------- chapters ----------------
function fig1(t,lt){
 cover(IMGS.night,1.06+0.08*ss(0,DUR[0]+1.5,lt),0.5,0.52);
 fireflies(t,1);
 figbar(lt,'RAAT \u00b7 AVANTIKA','FIG. 01 \u00b7 CHRONIC JOURNAL',true);
 typew(lt,0.8,'1884 SE PEHLE...',13,140,176,'Mono',34,'rgba(240,233,220,0.92)','left');
 const p2=ss(4.9,5.15,lt);
 if(p2>0){g.save();g.globalAlpha=p2;const sc=1.12-0.12*ov(p2);
  g.translate(140,0);g.scale(sc,sc);
  T(0,330/sc,'\u0909\u091c\u094d\u091c\u0948\u0928','Yatra',58,'#e8a33d','left');
  T(-4,448/sc,'UJJAIN','Anton',170,'#f3eee2','left');g.restore();}
 const p3=ss(9.2,9.9,lt);
 if(p3>0){const txt='MAHAKAL KI NAGRI \u00b7 KAAL = SAMAY';
  const nn=Math.ceil(txt.length*p3);
  T(140,560,txt.slice(0,nn),'Mono',34,'#e8a33d','left',1,6);}
 typew(lt,15.2,'POORI DUNIYA KA TIME... YAHIN SE KYON?',11,140,660,'Anton',58,'#f3eee2','left');
}
function fig2(t,lt){
 cover(IMGS.night,1.28+0.06*ss(0,DUR[1]+1.5,lt),0.78,0.42);
 fireflies(t,0.7);
 figbar(lt,'MAHAKALESHWAR \u00b7 JYOTIRLINGA','FIG. 02',true);
 kicker(lt,0.5,'KAAL KE DEVTA KI NAGRI','MAHAKAL');
 const p=ss(2.2,2.6,lt);
 if(p>0)T(140,350,'\u092e\u0939\u093e\u0915\u093e\u0932 \u00b7 \u0915\u093e\u0932 = \u0938\u092e\u092f','Deva',46,'#e8a33d','left',p);
 // 12 jyotirlinga dots panel
 const pb=ss(4.0,4.5,lt);
 if(pb>0){g.save();g.globalAlpha=pb;
  g.fillStyle='rgba(8,8,14,0.66)';rrect(120,430,760,210,16);g.fill();
  g.font='26px Mono';g.fillStyle='rgba(240,233,220,0.8)';g.textAlign='left';g.textBaseline='middle';
  g.fillText('12 JYOTIRLINGA',160,480);
  for(let k=0;k<12;k++){
   const pk=ss(4.4+k*0.38,4.6+k*0.38,lt);if(pk<=0)continue;
   const x=170+k*56,y=548;
   g.save();g.globalAlpha=pb*pk;
   if(k===11){g.fillStyle='#ffb14e';g.shadowColor='#ffb14e';g.shadowBlur=14;
    g.translate(x,y);g.rotate(Math.PI/4);g.fillRect(-13,-13,26,26);g.setTransform(1,0,0,1,0,0);
    g.shadowBlur=0;}
   else{g.fillStyle='rgba(205,216,242,0.6)';g.translate(x,y);g.rotate(Math.PI/4);g.fillRect(-9,-9,18,18);}
   g.restore();}
  const pa=ss(9.2,9.6,lt);
  if(pa>0){g.globalAlpha=pb*pa;
   g.strokeStyle='#ffb14e';g.lineWidth=4;
   const ax=170+11*56;
   g.beginPath();g.moveTo(ax,576);g.lineTo(ax,614);g.stroke();
   g.beginPath();g.moveTo(ax-10,602);g.lineTo(ax,616);g.lineTo(ax+10,602);g.stroke();
   g.font='28px Mono';g.fillStyle='#ffb14e';g.textAlign='left';
   g.fillText('SIRF YE \u2014 DAKSHINMUKHI',ax+26,600);}
  g.restore();}
 typew(lt,12.2,'SANYOG NAHI... SOCH.',12,140,730,'Anton',54,'#f3eee2','left');
}
function fig3(t,lt){
 blueprint(lt);
 figbar(lt,'SURYA SIDDHANTA \u00b7 4TH C. CE','FIG. 03',true);
 kicker(lt,0.9,'SHUNYA DESHANTAR','MADHYAREKHA');
 const p=ss(1.6,2.0,lt);
 if(p>0)T(140,330,'\u092e\u0927\u094d\u092f\u0930\u0947\u0916\u093e','Deva',44,'#e8a33d','left',p);
 polaroid(lt,2.6,IMGS.astr,330,640,330,-0.05,'\u091c\u094d\u092f\u094b\u0924\u093f\u0937\u0940','AI ART');
 indiaMap(lt,3.2);
 const lp=ss(7.6,9.0,lt);
 if(lp>0){const x=MX(75.78);
  g.save();g.strokeStyle='#ffb14e';g.lineWidth=5;g.shadowColor='#ffb14e';g.shadowBlur=16;
  g.beginPath();g.moveTo(x,140);g.lineTo(x,140+760*lp);g.stroke();g.restore();}
 const cp=ss(10.2,10.7,lt);
 if(cp>0){const ux=MX(75.78),uy=MY(23.18);
  g.save();g.globalAlpha=cp;
  g.fillStyle='#ffb14e';g.beginPath();g.arc(ux,uy,9,0,6.29);g.fill();
  g.strokeStyle='#ffb14e';g.lineWidth=2.5;
  g.beginPath();g.arc(ux,uy,19+6*Math.sin(t*4),0,6.29);g.stroke();
  g.font='28px Mono';g.fillStyle='#fff';g.textAlign='left';g.textBaseline='middle';
  g.fillText('UJJAIN \u00b7 23.1\u00b0N',ux+30,uy+2);g.restore();}
 const rp=ss(13.1,13.5,lt);
 if(rp>0){const rx=MX(76.6),ry=MY(28.9);
  g.save();g.globalAlpha=rp;g.fillStyle='#cdd8f2';g.beginPath();g.arc(rx,ry,7,0,6.29);g.fill();
  g.font='28px Mono';g.textAlign='left';g.textBaseline='middle';g.fillText('ROHTAK',rx+22,ry+2);g.restore();}
 const lk=ss(17.2,17.8,lt);
 if(lk>0){const lx=MX(75.78),ly=974;
  g.save();g.globalAlpha=lk;g.setLineDash([10,10]);g.strokeStyle='rgba(255,177,78,0.8)';g.lineWidth=3;
  g.beginPath();g.moveTo(lx,MY(6));g.lineTo(lx,ly);g.stroke();g.setLineDash([]);
  g.strokeStyle='#ffb14e';g.beginPath();g.arc(lx,ly,13+7*Math.sin(t*5),0,6.29);g.stroke();
  g.font='28px Mono';g.fillStyle='#ffb14e';g.textAlign='left';g.fillText('LANKA \u00b7 0\u00b0 EQUATOR',lx+30,ly);
  g.restore();}
 ['ARYABHATA','BRAHMAGUPTA','BHASKARA II'].forEach((nm,i)=>{
  const pp=ss(21.4+i*1.1,21.7+i*1.1,lt);if(pp<=0)return;
  const x=140,y=800+0; const bx=x+i*330;
  g.save();g.globalAlpha=pp;const sc=1.4-0.4*ov(pp);
  g.translate(bx+150,y+28);g.scale(sc,sc);g.translate(-(bx+150),-(y+28));
  g.fillStyle='rgba(10,18,40,0.92)';rrect(bx,y,300,56,28);g.fill();
  g.strokeStyle='rgba(140,180,255,0.8)';g.lineWidth=2;g.stroke();
  g.font='25px Mono';g.fillStyle='#f3eee2';g.textAlign='center';g.textBaseline='middle';
  g.fillText(nm,bx+150,y+30);g.restore();});
}
function fig4(t,lt){
 blueprint(3);
 figbar(lt,'0\u00b0 \u00d7 KARK REKHA','FIG. 04',true);
 indiaMap(3,0);
 // meridian stays
 const x=MX(75.78);
 g.save();g.strokeStyle='rgba(255,177,78,0.85)';g.lineWidth=4;
 g.beginPath();g.moveTo(x,140);g.lineTo(x,974);g.stroke();g.restore();
 kicker(lt,0.6,'YE JAGAH HI KYON?','DO REKHAON KA MILAN');
 // kark rekha draws
 const kp=ss(5.4,6.8,lt);
 if(kp>0){const y=MY(23.44);
  g.save();g.strokeStyle='#ff7a4e';g.lineWidth=4;g.shadowColor='#ff7a4e';g.shadowBlur=14;
  g.beginPath();g.moveTo(1120,y);g.lineTo(1120+700*kp,y);g.stroke();g.restore();
  g.save();g.globalAlpha=kp;g.font='26px Mono';g.fillStyle='#ff7a4e';g.textAlign='left';g.textBaseline='bottom';
  g.fillText('KARK REKHA \u00b7 23.4\u00b0N',1128,y-10);g.restore();}
 // X pulse
 const xp=ss(7.9,8.3,lt);
 if(xp>0){const ux=MX(75.78),uy=MY(23.44);
  g.save();g.globalAlpha=xp;
  g.strokeStyle='#ffb14e';g.lineWidth=3;
  g.beginPath();g.arc(ux,uy,26+10*Math.sin(t*5),0,6.29);g.stroke();
  g.beginPath();g.arc(ux,uy,52+14*Math.sin(t*5+1),0,6.29);g.globalAlpha=xp*0.5;g.stroke();
  g.restore();
  g.save();g.globalAlpha=xp;g.fillStyle='rgba(8,8,14,0.7)';rrect(1210,560,360,110,12);g.fill();
  g.font='40px InterB';g.fillStyle='#ffb14e';g.textAlign='center';g.textBaseline='middle';
  g.fillText('0\u00b0 \u00d7 23.4\u00b0',1390,605);
  g.font='20px Mono';g.fillStyle='rgba(240,233,220,0.7)';
  g.fillText('SURYA SIDDHANTA KE ANUSAR',1390,645);g.restore();}
 const gh=ss(13.9,14.3,lt);
 if(gh>0){g.save();const sc=1.5-0.5*ov(gh);g.globalAlpha=gh;
  g.translate(140,0);g.scale(sc,sc);
  T(0,640/sc,'PRACHEEN DUNIYA KA','Mono',34,'#e8a33d','left',1,4);
  T(-3,724/sc,'GREENWICH','Anton',110,'#f3eee2','left');g.restore();
  stamp(lt,14.5,560,850,'0\u00b0 \u00b7 UJJAIN','#e0503a',40,-0.1);}
}
function fig5(t,lt){
 g.fillStyle='#efe6d2';g.fillRect(0,0,W,H);
 g.save();g.strokeStyle='rgba(60,90,140,0.13)';g.lineWidth=1.5;
 for(let y=150;y<H;y+=58){g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke();}
 g.strokeStyle='rgba(200,80,60,0.3)';g.lineWidth=2;
 g.beginPath();g.moveTo(110,0);g.lineTo(110,H);g.stroke();g.restore();
 figbar(lt,'PANCHA SIDDHANTIKA \u00b7 9\u201310','FIG. 05',false);
 const navy='#1a2a4a',orange='#c9601e';
 const tp=ss(0.7,1.0,lt);
 if(tp>0){g.save();const sc=1.7-0.7*ov(tp);g.globalAlpha=tp;g.translate(170,0);g.scale(sc,sc);
  T(0,220/sc,'TIME ZONES','Anton',110,navy,'left');g.restore();
  T(172,310,'1300 SAAL PEHLE','Mono',40,orange,'left',tp,8);}
 const cp=ss(2.1,2.5,lt);
 if(cp>0){g.save();g.globalAlpha=cp;
  T(430,430,'\u0935\u0930\u093e\u0939\u092e\u093f\u0939\u093f\u0930','Deva',62,navy);
  T(430,496,'VARAHAMIHIRA \u00b7 505\u2013587 CE \u00b7 UJJAIN','Mono',24,'rgba(26,42,74,0.72)','center',1,2);
  g.restore();}
 [['POORAB','\u2212 GHATAO',1050,-1,7.8],['PASCHIM','+ BADHAO',1500,1,10.5]].forEach(cfg=>{
  const kp=ss(3.6,4.2,lt);if(kp<=0)return;
  const cx=cfg[2],cy=430,dir=cfg[3],hot=ss(cfg[4],cfg[4]+0.3,lt);
  g.save();g.globalAlpha=kp;
  g.strokeStyle=navy;g.lineWidth=4;g.beginPath();g.arc(cx,cy,130,0,6.29);g.stroke();
  for(let k=0;k<12;k++){const a=k*Math.PI/6;g.beginPath();
   g.moveTo(cx+Math.cos(a)*114,cy+Math.sin(a)*114);g.lineTo(cx+Math.cos(a)*128,cy+Math.sin(a)*128);g.stroke();}
  if(hot>0){g.strokeStyle=orange;g.lineWidth=7;g.globalAlpha=kp*(0.5+0.5*hot);
   g.beginPath();g.arc(cx,cy,139,0,6.29*hot);g.stroke();}
  g.strokeStyle=orange;g.lineWidth=7;g.globalAlpha=kp;
  const ha=t*2.0*dir-Math.PI/2;
  g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(ha)*92,cy+Math.sin(ha)*92);g.stroke();
  g.strokeStyle=navy;g.lineWidth=4;
  const ma=t*0.37*dir-Math.PI/2;
  g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(ma)*60,cy+Math.sin(ma)*60);g.stroke();
  g.font='30px Mono';g.fillStyle=navy;g.textAlign='center';g.textBaseline='middle';
  g.fillText(cfg[0],cx,cy+185);
  g.fillStyle=orange;g.font='42px InterB';g.fillText(cfg[1],cx,cy+240);
  g.restore();});
 typew(lt,12.8,'1 NADI / 53 YOJANA \u2014 DOORI SE TIME SUDHARO',14,170,760,'Mono',32,'rgba(26,42,74,0.85)','left');
 const cmp=ss(15.5,15.9,lt);
 if(cmp>0){g.save();g.globalAlpha=cmp;
  g.font='34px Mono';g.textAlign='left';g.textBaseline='middle';
  g.fillStyle='rgba(26,42,74,0.55)';g.fillText('EUROPE \u00b7 1884',170,850);
  g.strokeStyle='rgba(180,67,44,0.9)';g.lineWidth=4;
  g.beginPath();g.moveTo(165,850);g.lineTo(430,850);g.stroke();
  g.fillStyle='#1a2a4a';g.fillText('UJJAIN \u00b7 530 CE',560,850);g.restore();}
 stamp(lt,17.2,1620,820,'530 CE','#b4432c',54,-0.14);
}
function fig6(t,lt){
 g.fillStyle='#0a1228';g.fillRect(0,0,W,H);
 const rs=rng(42);
 g.save();for(let i=0;i<70;i++){const a=0.3+0.5*Math.abs(Math.sin(t*1.1+i));
  g.globalAlpha=a*0.5;g.fillStyle='#e8ecff';
  g.beginPath();g.arc(rs()*W,rs()*500,1+rs()*1.3,0,6.29);g.fill();}g.restore();
 figbar(lt,'WASHINGTON D.C. \u00b7 OCT 1884','FIG. 06',true);
 kicker(lt,0.5,'INTERNATIONAL MERIDIAN CONFERENCE','1884');
 const mp=ss(0.8,2.4,lt);
 const WX=l=>240+(l+30)*8.6, WY=l=>330+(60-l)*8.6;
 g.save();g.strokeStyle='rgba(120,160,230,0.5)';g.lineWidth=1.8;
 WORLD.forEach((seg,si)=>{
  const su=clamp(mp*WORLD.length-si,0,1);if(su<=0)return;
  const nn=Math.max(2,Math.floor(seg.length*su));
  g.beginPath();
  for(let i=0;i<nn;i++){const x=WX(seg[i][0]),y=WY(seg[i][1]);i?g.lineTo(x,y):g.moveTo(x,y);}
  g.stroke();});
 g.restore();
 polaroid(lt,3.6,IMGS.conf,1560,460,460,0.045,'1884','WASHINGTON \u00b7 AI ART');
 const pl=ss(6.8,7.2,lt);
 if(pl>0){g.save();g.globalAlpha=pl;
  g.fillStyle='rgba(8,8,14,0.7)';rrect(140,560,420,64,32);g.fill();
  g.font='30px Mono';g.fillStyle='#ffb14e';g.textAlign='center';g.textBaseline='middle';
  g.fillText('25 DESH \u00b7 1 VOTE',350,594);g.restore();}
 const sp=ss(10.4,12.0,lt);
 const lon=75.78+(0-75.78)*sp;
 g.save();
 for(let gh=5;gh>=0;gh--){
  const gl=75.78+(0-75.78)*clamp(sp-gh*0.06,0,1);
  g.globalAlpha=gh===0?1:0.12*(6-gh)/6;
  g.strokeStyle=gh===0?'#ffb14e':'#c9884e';g.lineWidth=gh===0?5:3;
  if(gh===0){g.shadowColor='#ffb14e';g.shadowBlur=14;}
  g.beginPath();g.moveTo(WX(gl),300);g.lineTo(WX(gl),930);g.stroke();g.shadowBlur=0;}
 g.restore();
 g.save();
 const ux=WX(75.78),gx=WX(0);
 g.fillStyle='rgba(205,216,242,0.85)';g.beginPath();g.arc(ux,WY(23.18),7,0,6.29);g.fill();
 g.font='26px Mono';g.textAlign='center';g.fillStyle='rgba(205,216,242,0.9)';
 g.fillText('UJJAIN',ux,965);
 g.fillStyle='#ffb14e';g.beginPath();g.arc(gx,WY(51.5),7,0,6.29);g.fill();
 g.fillText('GREENWICH',gx,965);g.restore();
 stamp(lt,12.9,ux,860,'\u2717','#8b94ab',40,-0.15);
 stamp(lt,13.6,gx,860,'0\u00b0 \u2713','#ffb14e',40,0.12);
 typew(lt,15.1,'EK VOTE. 2000 SAAL KA CENTER... GAYA.',13,140,760,'Anton',52,'#f3eee2','left');
}
function fig7(t,lt){
 g.fillStyle='#efe6d2';g.fillRect(0,0,W,H);
 g.save();g.strokeStyle='rgba(60,90,140,0.13)';g.lineWidth=1.5;
 for(let y=150;y<H;y+=58){g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke();}g.restore();
 figbar(lt,'VEDH SHALA \u00b7 UJJAIN','FIG. 07',false);
 const navy='#1a2a4a',orange='#c9601e';
 kickerCream(lt,0.6,'1725 \u00b7 SAWAI JAI SINGH II','VEDH SHALA',navy,orange);
 const p=ss(2.0,2.4,lt);
 if(p>0)T(170,330,'\u0935\u0947\u0927 \u0936\u093e\u0932\u093e','Deva',48,orange,'left',p);
 // Samrat Yantra: gnomon triangle + quadrant arcs + sun sweep
 const yp=ss(4.4,6.2,lt);
 if(yp>0){const bx=1250,by=760,s=380;
  g.save();g.strokeStyle=navy;g.lineWidth=5;g.lineJoin='round';
  // gnomon (right triangle) draws
  const path=[[bx-s*0.52,by],[bx+s*0.3,by-s*0.78],[bx+s*0.3,by],[bx-s*0.52,by]];
  g.beginPath();
  const segs=path.length-1;
  for(let i=0;i<segs;i++){
   const u=clamp(yp*segs-i,0,1);if(u<=0)break;
   const a=path[i],b2=path[i+1];
   if(i===0)g.moveTo(a[0],a[1]);
   g.lineTo(a[0]+(b2[0]-a[0])*u,a[1]+(b2[1]-a[1])*u);}
  g.stroke();
  // steps on hypotenuse
  const st=ss(6.0,7.0,lt);
  if(st>0){g.lineWidth=3;
   for(let k=1;k<7;k++){const u=k/7;if(u>st)break;
    const x1=bx-s*0.52+(s*0.82)*u, y1=by-(s*0.78)*u;
    g.beginPath();g.moveTo(x1,y1);g.lineTo(x1+18,y1);g.stroke();}}
  // quadrant arcs
  const qa=ss(6.6,8.0,lt);
  if(qa>0){g.strokeStyle=orange;g.lineWidth=4;
   g.beginPath();g.arc(bx+s*0.3,by,s*0.55,Math.PI*0.5,Math.PI*(0.5+0.48*qa));g.stroke();
   g.beginPath();g.arc(bx-s*0.52,by,s*0.4,Math.PI*0.52,Math.PI*(0.52+0.44*qa));g.stroke();}
  // sun arc + moving sun + shadow line
  const su=ss(8.8,14.0,lt);
  if(su>0){const ang=Math.PI*(1.05-su*0.75);
   const sx=bx-80+Math.cos(ang)*s*1.05, sy=by-60+Math.sin(ang)*-s*0.62;
   g.save();g.fillStyle='#e8a33d';g.shadowColor='#e8a33d';g.shadowBlur=24;
   g.beginPath();g.arc(sx,sy,20,0,6.29);g.fill();g.restore();
   // shadow from gnomon tip
   const tipx=bx+s*0.3,tipy=by-s*0.78;
   const dx2=tipx-sx,dy2=tipy-sy;
   const m2=(by-tipy)/ (dy2||1e-4);
   const shx=clamp(tipx+dx2*m2,bx-s*0.7,bx+s*0.75);
   g.save();g.strokeStyle='rgba(26,42,74,0.55)';g.lineWidth=6;
   g.beginPath();g.moveTo(tipx,tipy);g.lineTo(shx,by);g.stroke();g.restore();
   g.save();g.font='24px Mono';g.fillStyle=navy;g.textAlign='center';g.fillText('CHHAYA = SAMAY',bx-90,by+44);g.restore();}
  g.restore();}
 typew(lt,9.4,'PATTHAR KE YANTRA \u00b7 0 LENS \u00b7 GRAHON KI CHAAL',14,170,560,'Mono',30,'rgba(26,42,74,0.85)','left');
 typew(lt,13.6,'2 MIN TAK SAHI SAMAY \u2014 SIRF CHHAYA SE',14,170,640,'Mono',30,'rgba(26,42,74,0.85)','left');
 stamp(lt,16.3,420,850,'AAJ BHI ZINDA','#b4432c',44,-0.1);
}
function kickerCream(lt,t0,small,big,navy,orange){
 const p=ss(t0,t0+0.4,lt);if(p<=0)return;
 g.save();g.globalAlpha=p;
 T(170,176,small,'Mono',30,orange,'left',1,6);
 T(170,252,big,'Anton',86,navy,'left');g.restore();}
function fig8(t,lt){
 cover(IMGS.dawn,1.06+0.07*ss(0,DUR[7]+1.5,lt),0.45,0.5);
 figbar(lt,'PANCHANG \u00b7 AAJ BHI','FIG. 08',true);
 kicker(lt,0.5,'GREENWICH JEETA... PAR','UJJAIN ZINDA HAI');
 // clock ring
 const cp=ss(2.6,3.6,lt),cx=560,cy=600,R1=240;
 if(cp>0){g.save();g.globalAlpha=cp;
  g.fillStyle='rgba(8,8,14,0.45)';g.beginPath();g.arc(cx,cy,R1+54,0,6.29);g.fill();
  g.strokeStyle='rgba(243,239,228,0.92)';g.lineWidth=4;
  g.beginPath();g.arc(cx,cy,R1,0,6.29*cp);g.stroke();
  for(let k=0;k<60;k++){const a=k*Math.PI/30-Math.PI/2;if(k/60>cp)break;
   g.lineWidth=k%5?2:4;
   g.beginPath();g.moveTo(cx+Math.cos(a)*(R1-(k%5?12:22)),cy+Math.sin(a)*(R1-(k%5?12:22)));
   g.lineTo(cx+Math.cos(a)*(R1-3),cy+Math.sin(a)*(R1-3));g.stroke();}
  const base=-Math.PI/2+t*0.33;
  const off=-(29/60)*2*Math.PI*ss(8.2,10.8,lt);
  g.strokeStyle='rgba(255,177,78,0.9)';g.lineWidth=14;
  g.beginPath();g.arc(cx,cy,R1-38,base+off,base);g.stroke();
  g.lineWidth=6;g.strokeStyle='#f3efe4';
  g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(base)*(R1-58),cy+Math.sin(base)*(R1-58));g.stroke();
  g.strokeStyle='#ffb14e';
  g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(base+off)*(R1-58),cy+Math.sin(base+off)*(R1-58));g.stroke();
  const cnt=Math.round(29*ss(8.2,10.8,lt));
  T(cx,cy-12,'\u2212'+cnt+' MIN','InterB',64,'#ffb14e');
  T(cx,cy+40,'UJJAIN MEAN TIME','Mono',22,'rgba(243,239,228,0.85)','center',1,3);
  g.restore();}
 // panchang strip
 const pp=ss(3.4,4.0,lt);
 if(pp>0){g.save();g.globalAlpha=pp;
  const px=1080+((1-ov(pp))*400),py=430;
  g.translate(px,py);g.rotate(-0.015);
  g.fillStyle='#efe6d2';g.shadowColor='rgba(0,0,0,0.4)';g.shadowBlur=22;
  g.fillRect(0,0,640,190);g.shadowColor='transparent';
  g.fillStyle='#1a2a4a';g.font='52px Deva';g.textAlign='left';g.textBaseline='middle';
  g.fillText('\u092a\u0902\u091a\u093e\u0902\u0917',28,62);
  g.font='24px Mono';g.fillStyle='rgba(26,42,74,0.8)';
  g.fillText('HAR KUNDALI \u00b7 HAR MUHURAT',28,122);
  g.fillText('UJJAIN TIME \u00b7 IST \u2212 00:29',28,158);
  g.restore();}
 const t1=ss(14.6,14.9,lt);
 if(t1>0){g.save();const sc=1.5-0.5*ov(t1);g.globalAlpha=t1;g.translate(1080,0);g.scale(sc,sc);
  T(0,740/sc,'GHADI BADAL GAYI.','Anton',64,'#f3eee2','left');g.restore();}
 const t2=ss(16.7,17.0,lt);
 if(t2>0){g.save();const sc=1.7-0.7*ov(t2);g.globalAlpha=t2;g.translate(1080,0);g.scale(sc,sc);
  T(0,830/sc,'CENTER NAHI.','Anton',84,'#ffb14e','left');g.restore();}
}
function fig9(t,lt){
 cover(IMGS.dawn,1.16+0.05*ss(0,DUR[8]+2,lt),0.62,0.42);
 g.save();g.globalAlpha=0.25+0.08*Math.sin(t*1.2);
 const gr=g.createRadialGradient(1420,330,60,1420,330,900);
 gr.addColorStop(0,'rgba(255,190,90,0.85)');gr.addColorStop(1,'rgba(255,190,90,0)');
 g.fillStyle=gr;g.fillRect(0,0,W,H);g.restore();
 figbar(lt,'CASE FILE \u00b7 UJJAIN','FIG. 09 \u00b7 YOUR TURN',true);
 const mp=ss(0.4,1.2,lt);
 if(mp>0){g.save();g.strokeStyle='rgba(255,177,78,0.9)';g.lineWidth=4;g.shadowColor='#ffb14e';g.shadowBlur=12;
  g.beginPath();g.moveTo(560,0);g.lineTo(560,H*mp);g.stroke();g.restore();}
 const lp=ss(1.3,1.8,lt);
 if(lp>0&&logo.complete){g.save();const sc=1.6-0.6*ov(lp);g.globalAlpha=lp;
  g.translate(560,430);g.scale(sc,sc);
  g.save();g.beginPath();g.arc(0,0,260,0,6.29);g.clip();
  g.drawImage(logo,-260,-260,520,520);g.restore();
  g.strokeStyle='#ffb14e';g.lineWidth=6;g.beginPath();g.arc(0,0,264,0,6.29);g.stroke();
  g.restore();}
 T(560,772,'CHRONIC OF HISTORIC','Anton',56,'#f3eee2','center',ss(2.2,2.7,lt),3);
 const qp=ss(4.6,5.1,lt);
 if(qp>0){g.save();g.globalAlpha=qp;
  g.fillStyle='rgba(8,8,14,0.6)';rrect(1010,300,800,150,18);g.fill();
  g.font='44px InterB';g.fillStyle='#f3eee2';g.textAlign='center';g.textBaseline='middle';
  g.fillText('SHUNYA REKHA WAPAS',1410,355);
  g.fillText('UJJAIN AANI CHAHIYE?',1410,410);g.restore();}
 const q1=ss(6.3,6.65,lt),q2=ss(6.9,7.25,lt);
 [[q1,'1 \u00b7 HAAN',1220,'#ffb14e','#1a1206'],[q2,'2 \u00b7 NAHIN',1610,'#f3eee2','#1a2030']].forEach(cfg=>{
  const [qq,txt,x,bg2,fg]=cfg;if(qq<=0)return;
  g.save();const sc=1.5-0.5*ov(qq);g.globalAlpha=qq;g.translate(x,540);g.scale(sc,sc);
  g.fillStyle=bg2;rrect(-170,-46,340,92,46);g.fill();
  g.fillStyle=fg;g.font='44px InterB';g.textAlign='center';g.textBaseline='middle';
  g.fillText(txt,0,3);g.restore();});
 const sp=ss(9.4,9.8,lt);
 if(sp>0){g.save();const sc=1.4-0.4*ov(sp);g.globalAlpha=sp;g.translate(1410,680);g.scale(sc,sc);
  g.rotate(Math.sin(lt*13)*(lt<11?0.05:0));
  g.fillStyle='#d6361f';rrect(-210,-48,420,96,48);g.fill();
  g.fillStyle='#fff';g.font='46px InterB';g.textAlign='center';g.textBaseline='middle';
  g.fillText('SUBSCRIBE',8,3);
  g.beginPath();g.moveTo(-168,-15);g.lineTo(-142,-15);g.lineTo(-155,13);g.closePath();g.fill();
  g.restore();}
 stamp(lt,12.5,1410,850,'CASE ABHI BHI KHULA HAI','#e8503a',40,-0.07);
 const fo=ss(TOTAL-B[8]-1.3,TOTAL-B[8]-0.1,lt);
 if(fo>0){g.save();g.globalAlpha=fo;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
const FIGS=[fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9];
function captions(t,bi){
 let cur=null;
 for(const c of CAPS)if(t>=c.start&&t<c.end){cur=c;break;}
 if(!cur)return;
 const dark=(bi===4||bi===6);
 const base=dark?'#1a2030':'#ffffff', hi2=dark?'#c9601e':'#ffb14e';
 const n=cur.words.length,prog=(t-cur.start)/(cur.end-cur.start);
 g.save();g.font='40px InterS';g.textBaseline='middle';
 const meas=cur.words.map(w=>g.measureText(w+' ').width);
 let tw=0;for(const m of meas)tw+=m;
 let x=W/2-tw/2;const y=1006;
 if(!dark){g.shadowColor='rgba(0,0,0,0.65)';g.shadowBlur=10;}
 cur.words.forEach((w,i)=>{
  const on=prog*n>=i;const clean=w.replace(/[^A-Z0-9]/g,'');
  g.fillStyle=HI.includes(clean)?hi2:base;
  g.globalAlpha=on?1:0.3;g.textAlign='left';g.fillText(w,x,y);x+=meas[i];});
 g.restore();}
function flash(lt){const a=1-ss(0,0.14,lt);if(a>0){g.save();g.globalAlpha=a*0.45;g.fillStyle='#fff8ea';g.fillRect(0,0,W,H);g.restore();}}
function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 let bi=0;for(let i=0;i<B.length;i++)if(t>=B[i])bi=i;
 const lt=t-B[bi];
 FIGS[bi](t,lt);
 if(bi>0)flash(lt);
 captions(t,bi);
 g.save();g.fillStyle='rgba(255,255,255,0.2)';g.fillRect(0,H-4,W,4);
 g.fillStyle='#ffb14e';g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
 g.save();g.globalAlpha=0.42;
 g.drawImage(noiseCv,-(Math.floor(t*13)%19),-(Math.floor(t*7)%23),W+40,H+40);g.restore();
 g.drawImage(vig,0,0);
 const fi=ss(0,0.5,t);
 if(fi<1){g.save();g.globalAlpha=1-fi;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}}
window.renderAt=function(t){draw(t);return cv.toDataURL('image/jpeg',0.84);};
window.renderBatch=function(ts){return ts.map(t=>{draw(t);return cv.toDataURL('image/jpeg',0.84);});};
document.fonts.ready.then(()=>{try{
 ['Anton','InterB','InterS','Mono','Yatra','Deva'].forEach(f=>{g.font='30px '+f;g.fillText('\u0909 Ag',-100,-100);});
 const wait=()=>{if(nimg>=wantimg){try{draw(1);draw(45);draw(95);draw(135);draw(175);window.__ready=true;}catch(e){window.__err=''+(e.stack||e);}}else setTimeout(wait,60);};
 wait();}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff)
    html = html.replace("__TOT__", str(TOTAL)).replace("BEATSJ", json.dumps(BEATS)).replace("DURJ", json.dumps(DUR))
    html = html.replace("CAPSJ", json.dumps(caps)).replace("HIJ", json.dumps(sorted(HI)))
    html = html.replace("INDIAJ", json.dumps(india)).replace("WORLDJ", json.dumps(world))
    html = html.replace("NIGHT64", b64(U10 + "/bg_night_wide.jpg"))
    html = html.replace("DAWN64", b64(U10 + "/bg_dawn_wide.jpg"))
    html = html.replace("ASTR64", b64(U10 + "/card_astronomer.jpg"))
    html = html.replace("CONF64", b64(U10 + "/card_conference.jpg"))
    html = html.replace("LOGO64", b64(LOGO))
    hp = os.path.join(ROOT, "page.html")
    open(hp, "w").write(html)
    return hp, caps


def ts_srt(x):
    hh = int(x // 3600); mm = int(x % 3600 // 60); s = x % 60
    return ("%02d:%02d:%06.3f" % (hh, mm, s)).replace(".", ",")
def write_srt(caps, path):
    L = []
    for i, c in enumerate(caps):
        L.append("%d\n%s --> %s\n%s\n" % (i + 1, ts_srt(c["start"]), ts_srt(min(c["end"], TOTAL)),
                                          " ".join(c["words"])))
    open(path, "w").write("\n".join(L))


def run(mode):
    os.makedirs(ROOT, exist_ok=True)
    hp, caps = build_html()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True,
                                    args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 200, "height": 200})
        page.goto("file://" + hp)
        try:
            page.wait_for_function("window.__ready === true || window.__err", timeout=180000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            chk = os.environ.get("CHK_TIMES")
            TSL = ([float(x) for x in chk.split(",")] if chk
                   else [BEATS[i] + DUR[i] * 0.72 for i in range(9)])
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
    out = os.path.join(ROOT, "final.mp4")
    subprocess.run([FF, "-nostdin", "-y", "-framerate", str(FPS),
                    "-i", os.path.join(ROOT, "frames", "%05d.jpg"),
                    "-i", os.path.join(ROOT, "master.wav"),
                    "-c:v", "libx264", "-preset", "veryfast", "-threads", "2", "-crf", "26",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", out], check=True, capture_output=True)
    write_srt(caps, os.path.join(ROOT, "final.srt"))
    print("SUCCESS: %s %.2f MB" % (out, os.path.getsize(out) / 1e6))


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
