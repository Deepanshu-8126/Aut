#!/usr/bin/env python3
# MODE 3D SHOWCASE TEST — "REAL FEEL" (spec per skills/10 + MODE_3D_LOCKED.md)
# 1 WHAT: 4 feature scenes, one continuous cam each:
#   A 0-7.5  snowy Himalayan valley fly-through (fbm terrain, vertex-color snow, 500 snow pts)
#   B 7.5-13.5 dusk lake (CPU wave verts + Phong specular, 2 torch fires + flicker lights, rain)
#   C 13.5-23.5 UNDERWATER dive (caustic planes, 300 bubbles, light shafts, sunken AI-engraving plate)
#   D 23.5-27.5 starfield end card "MODE 3D LOCKED"
# 2 MOVES: eased dolly per scene + handheld micro-shake; particles always alive.
# 3 LOOK: per-scene fog+grade; fake bloom pass in 2D; grain+vignette; band locked style.
# 6 BANNED: shadows, EffectComposer, cuts inside a scene, >600 pts/scene.
# 7 BUDGET: (1)terrain (2)water+fire (3)underwater+plate (4)stars. Ship 1-3 minimum.
# 8 PROOF: --preview 7 checkpoints; frame-verify final mp4.
import os, sys, io, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/three3dv2"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
PT = os.path.join(ASSETS, "patal")
PR = os.path.join(ASSETS, "props")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
FPS = 30
W, H = 1920, 1080
GW, GH = 1280, 720
TOTAL = 27.5

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
def bell(f, a, d=2.4):
    t = np.arange(_n(d)) / SR
    return a * (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2.76*t)) * np.exp(-t * 1.9)

def gate(n, t0, t1, f=0.7):
    t = np.arange(n) / SR
    up = np.clip((t - t0) / f, 0, 1); dn = np.clip((t1 - t) / f, 0, 1)
    return np.minimum(up, dn)

def build_audio():
    n = _n(TOTAL); beds = np.zeros(n); sfx = np.zeros(n); vo = np.zeros(n)
    t = np.arange(n) / SR
    def put(dst, x, at):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); dst[i:i + L] += x[:L]
    # A wind
    beds += box(noise(TOTAL, 3), 220) * 6.0 * 0.55 * gate(n, -0.5, 8.0)
    # B rain hiss + lap + fire crackle
    x2 = noise(TOTAL, 11)
    beds += (x2 - box(x2, 5)) * 0.30 * gate(n, 7.6, 13.9, 0.5)
    beds += box(noise(TOTAL, 13), 500) * 8.0 * 0.35 * (0.6 + 0.4*np.sin(2*np.pi*0.33*t)) * gate(n, 7.4, 13.9)
    rs = np.random.RandomState(42)
    for _ in range(90):
        tt = 7.9 + rs.rand() * 5.4
        d = 0.02 + rs.rand() * 0.03
        pop = noise(d, rs.randint(1, 9999)) * np.exp(-np.arange(_n(d)) / (_n(d) * 0.3)) * (0.5 + rs.rand())
        put(sfx, pop * 0.16, tt)
    # C underwater rumble + blips
    beds += (0.085 * np.sin(2*np.pi*52*t) + box(noise(TOTAL, 17), 900) * 7 * 0.28) * gate(n, 13.4, 24.2)
    for k in range(11):
        tt = 14.2 + rs.rand() * 8.6
        put(sfx, envad(tone(0.16, 260 + rs.rand()*200, 700 + rs.rand()*400, 0.05), 0.03, 0.1), tt)
    # transitions + bell
    put(sfx, whoosh(0.8, 0.26, 6), 7.2)
    put(sfx, whoosh(0.9, 0.26, 8), 13.1)
    put(sfx, whoosh(1.0, 0.24, 9), 23.1)
    put(sfx, bell(523, 0.13), 24.0)
    # drone
    beds += 0.026 * (np.sin(2*np.pi*65*t) + np.sin(2*np.pi*65.33*t + 0.7))
    # VO
    wv = os.path.join(ROOT, "tvo.wav")
    if not os.path.exists(wv):
        subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(PR, "tvo3dv2.mp3"),
                        "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
    wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
    wf.close()
    i0 = _n(0.6); L = min(len(dat), n - i0)
    vo[i0:i0 + L] += dat[:L] * 1.35
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    beds *= (1.0 - 0.5 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.9 + beds
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok")

def b64(p): return base64.b64encode(open(p, "rb").read()).decode()

def build_html():
    three = open("/var/tmp/three/three.min.js").read()
    ff = """
@font-face{font-family:'Mono';src:url('file://%s/JetBrainsMono-Bold.ttf');}
@font-face{font-family:'Deva';src:url('file:///var/tmp/ujjain/TiroDeva.ttf');}
""" % FONTS
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body>
<script>THREELIB</script>
<script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,GW=1280,GH=720,TOTAL=__TOT__;
const S1E=7.5,S2E=13.5,S3E=23.5;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const gl=document.createElement('canvas');gl.width=GW;gl.height=GH;
const bl=document.createElement('canvas');bl.width=320;bl.height=180;const blg=bl.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
function vnoise(x,y){const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;
 function hsh(a,b){let n=(a*374761393+b*668265263)|0;n=Math.imul(n^(n>>>13),1274126177);return(((n^(n>>>16))>>>0)%1000)/1000;}
 const sx=xf*xf*(3-2*xf),sy=yf*yf*(3-2*yf);
 const a=hsh(xi,yi),b2=hsh(xi+1,yi),c=hsh(xi,yi+1),d=hsh(xi+1,yi+1);
 return a+(b2-a)*sx+(c-a)*sy+(a-b2-c+d)*sx*sy;}
function fbm(x,y){let v=0,amp=1,f=1,s=0;for(let o=0;o<4;o++){v+=amp*vnoise(x*f,y*f);s+=amp;amp*=0.5;f*=2.07;}return v/s;}
const renderer=new THREE.WebGLRenderer({canvas:gl,antialias:false});
renderer.setSize(GW,GH,false);renderer.outputEncoding=THREE.sRGBEncoding;
const cam=new THREE.PerspectiveCamera(44,GW/GH,0.1,400);
// ============ SCENE A: snowy valley ============
const scA=new THREE.Scene();
scA.background=new THREE.Color(0xa9c3dd);scA.fog=new THREE.FogExp2(0xb6c9de,0.0058);
{const geo=new THREE.PlaneGeometry(260,260,150,150);
 const pos=geo.attributes.position,NV=pos.count;
 for(let i=0;i<NV;i++){const x=pos.getX(i),y=pos.getY(i);
  let h=Math.pow(fbm(x*0.016+3.7,y*0.016+8.2),2.1)*46;
  h+=fbm(x*0.085+11,y*0.085+4)*3.2-1.3;
  h+=(fbm(x*0.14+7,y*0.14+2)-0.5)*4.5;
  h*=1-0.85*Math.exp(-(x*x)/(2*14*14));
  pos.setZ(i,Math.max(h,0));}
 geo.computeVertexNormals();
 const nr=geo.attributes.normal;const col=new Float32Array(NV*3);
 for(let i=0;i<NV;i++){const h=pos.getZ(i);
  const sl=nr.getZ(i);let s=clamp(ss(7,12,h)*ss(0.55,0.8,sl)+0.3*ss(0.93,0.99,sl)*ss(2,5,h),0,1);
  const spk=fbm(pos.getX(i)*0.2,pos.getY(i)*0.2);
  const r0=0.14+0.08*spk,g0=0.13+0.07*spk,b0=0.12+0.07*spk;
  col[i*3]=r0+(0.92-r0)*s;col[i*3+1]=g0+(0.95-g0)*s;col[i*3+2]=b0+(0.99-b0)*s;}
 geo.setAttribute('color',new THREE.BufferAttribute(col,3));
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({vertexColors:true,roughness:0.93,metalness:0}));
 m.rotation.x=-Math.PI/2;scA.add(m);}
scA.add(new THREE.HemisphereLight(0xcfe0ff,0x4a443e,0.55));
{const sun=new THREE.DirectionalLight(0xffd9a8,1.45);sun.position.set(60,42,-20);scA.add(sun);}
let SNOW,SNOWD=[];
{const r=rng(91),N=500,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){p[i*3]=(r()-0.5)*48;p[i*3+1]=r()*26;p[i*3+2]=95-r()*125;
  SNOWD.push([r()*6.28,1.4+r()*1.6,p[i*3],p[i*3+1]]);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 SNOW=new THREE.Points(geo,new THREE.PointsMaterial({color:0xffffff,size:0.14,transparent:true,opacity:0.85,sizeAttenuation:true}));
 scA.add(SNOW);}
// ============ SCENE B: dusk lake ============
const scB=new THREE.Scene();
scB.background=new THREE.Color(0x171026);scB.fog=new THREE.FogExp2(0x171026,0.035);
let WATER,WBASE;
{const geo=new THREE.PlaneGeometry(90,90,62,62);
 WBASE=geo.attributes.position.array.slice();
 WATER=new THREE.Mesh(geo,new THREE.MeshPhongMaterial({color:0x0d2638,specular:0x9db8ff,shininess:140}));
 WATER.rotation.x=-Math.PI/2;scB.add(WATER);}
{const r=rng(17);for(let i=0;i<4;i++){
 const hill=new THREE.Mesh(new THREE.ConeGeometry(9+r()*7,4+r()*4,7),
  new THREE.MeshStandardMaterial({color:0x100b18,roughness:1}));
 hill.position.set(-16+i*11+r()*4,1.6,-24-r()*8);hill.scale.y=0.8;scB.add(hill);}}
const TORCH=[];const FIRES=[];
function mkTorch(sc,x,z,seed){
 const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.1,2.5,8),
  new THREE.MeshStandardMaterial({color:0x241a12,roughness:0.9}));
 pole.position.set(x,1.25,z);sc.add(pole);
 const L=new THREE.PointLight(0xff8830,1.6,18,2);L.position.set(x,2.75,z);sc.add(L);TORCH.push(L);
 const r=rng(seed);
 for(const[cnt,colr,sz]of[[60,0xff7a20,0.20],[16,0xffc070,0.09]]){
  const p=new Float32Array(cnt*3),dat=[];
  for(let i=0;i<cnt;i++){dat.push([r(),r()*6.28,0.7+r()*0.6]);p[i*3]=x;p[i*3+1]=2.5;p[i*3+2]=z;}
  const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
  const pts=new THREE.Points(geo,new THREE.PointsMaterial({color:colr,size:sz,transparent:true,opacity:0.85,
   blending:THREE.AdditiveBlending,depthWrite:false}));
  sc.add(pts);FIRES.push({pts,dat,x,z,top:2.45});}}
mkTorch(scB,-2.2,-6,111);mkTorch(scB,2.6,-8,222);
scB.add(new THREE.AmbientLight(0x241a2e,1.0));
{const moon=new THREE.DirectionalLight(0x8ca8e0,0.35);moon.position.set(-20,18,-10);scB.add(moon);}
let RAIN,RAIND=[];
{const r=rng(55),N=420,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){p[i*3]=(r()-0.5)*28;p[i*3+1]=r()*12;p[i*3+2]=14-r()*30;
  RAIND.push([p[i*3],p[i*3+1],14+r()*4]);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 RAIN=new THREE.Points(geo,new THREE.PointsMaterial({color:0xaac4e8,size:0.055,transparent:true,opacity:0.5,sizeAttenuation:true}));
 scB.add(RAIN);}
// ============ SCENE C: underwater ============
const scC=new THREE.Scene();
scC.background=new THREE.Color(0x07323a);scC.fog=new THREE.FogExp2(0x07323a,0.046);
const sandCv=document.createElement('canvas');sandCv.width=sandCv.height=256;
{const sc2=sandCv.getContext('2d');sc2.fillStyle='#7a6a4e';sc2.fillRect(0,0,256,256);
 const r=rng(31);for(let i=0;i<2600;i++){const v=40+r()*70;
 sc2.fillStyle='rgba('+(90+v|0)+','+(78+v*0.9|0)+','+(55+v*0.7|0)+',0.5)';
 sc2.fillRect(r()*256,r()*256,1.6,1.6);}}
{const tx=new THREE.CanvasTexture(sandCv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(6,6);
 const geo=new THREE.PlaneGeometry(70,70,56,56);
 const pos=geo.attributes.position,r=rng(63);
 for(let i=0;i<pos.count;i++){const x=pos.getX(i),y=pos.getY(i);
  pos.setZ(i,fbm(x*0.12+1,y*0.12+5)*1.1-0.3);}
 geo.computeVertexNormals();
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({map:tx,roughness:0.95}));
 m.rotation.x=-Math.PI/2;scC.add(m);}
{const pmat=new THREE.MeshStandardMaterial({color:0x6a6a5c,roughness:0.9});
 const p1=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.68,4.4,10),pmat);
 p1.position.set(-2.8,2.1,-4.6);p1.rotation.z=0.12;scC.add(p1);
 const p2=new THREE.Mesh(new THREE.CylinderGeometry(0.5,0.58,3.8,10),pmat);
 p2.position.set(2.9,0.62,-1.4);p2.rotation.z=Math.PI/2*0.94;p2.rotation.y=0.5;scC.add(p2);
 const r=rng(44);for(let i=0;i<6;i++){
  const st=new THREE.Mesh(new THREE.SphereGeometry(0.3+r()*0.5,8,6),pmat);
  st.position.set((r()-0.5)*10,0.15+r()*0.2,(r()-0.5)*8-1);st.scale.y=0.55;scC.add(st);}}
const texLoader=new THREE.TextureLoader();let texOk=0;
texLoader.load('data:image/jpeg;base64,GAN64',(tx)=>{
 tx.encoding=THREE.sRGBEncoding;
 const fr=new THREE.Mesh(new THREE.PlaneGeometry(3.5,2.45),
  new THREE.MeshStandardMaterial({color:0xcfc3a8,roughness:0.9}));
 fr.position.set(0,1.32,-2.66);fr.rotation.x=-0.1;fr.rotation.y=0.16;scC.add(fr);
 const pl=new THREE.Mesh(new THREE.PlaneGeometry(3.2,2.14),
  new THREE.MeshStandardMaterial({map:tx,roughness:0.82}));
 pl.position.set(0,1.32,-2.6);pl.rotation.x=-0.1;pl.rotation.y=0.16;scC.add(pl);
 texOk=1;});
const cauCv=document.createElement('canvas');cauCv.width=cauCv.height=256;
{const cc=cauCv.getContext('2d');cc.fillStyle='#000';cc.fillRect(0,0,256,256);
 const r=rng(77);cc.strokeStyle='rgba(255,255,255,0.55)';cc.lineWidth=2.2;
 for(let i=0;i<46;i++){cc.beginPath();
  cc.ellipse(r()*256,r()*256,8+r()*26,6+r()*20,r()*3.14,0,6.29);cc.stroke();}
 cc.filter='blur(3px)';cc.drawImage(cauCv,0,0);}
const CAUS=[];
for(const[yy,op]of[[0.14,0.20],[0.24,0.14]]){
 const tx=new THREE.CanvasTexture(cauCv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(3.2,3.2);
 const m=new THREE.Mesh(new THREE.PlaneGeometry(60,60),
  new THREE.MeshBasicMaterial({map:tx,transparent:true,opacity:op,color:0x9fe8e0,
   blending:THREE.AdditiveBlending,depthWrite:false}));
 m.rotation.x=-Math.PI/2;m.position.y=yy;scC.add(m);CAUS.push(tx);}
const SHAFTS=[];
{const r=rng(88);for(let i=0;i<3;i++){
 const sh=new THREE.Mesh(new THREE.ConeGeometry(1.6+r()*1.4,14,18,1,true),
  new THREE.MeshBasicMaterial({color:0x8fd8d0,transparent:true,opacity:0.05,
   blending:THREE.AdditiveBlending,side:THREE.DoubleSide,depthWrite:false}));
 sh.position.set(-5+i*5+r()*2,7.5,-3-r()*4);sh.rotation.z=0.12-i*0.1;scC.add(sh);SHAFTS.push(sh);}}
let BUB,BUBD=[];
{const r=rng(99),N=300,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){p[i*3]=(r()-0.5)*20;p[i*3+1]=r()*9;p[i*3+2]=10-r()*18;
  BUBD.push([p[i*3],r()*9,0.35+r()*0.8,r()*6.28]);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 BUB=new THREE.Points(geo,new THREE.PointsMaterial({color:0xcfeef2,size:0.07,transparent:true,opacity:0.55,sizeAttenuation:true}));
 scC.add(BUB);}
{const sun2=new THREE.DirectionalLight(0xaee2f0,0.95);sun2.position.set(6,20,4);scC.add(sun2);}
scC.add(new THREE.AmbientLight(0x0e3a42,1.1));
const plLight=new THREE.PointLight(0xd8c89a,0.8,9,2);plLight.position.set(1.5,2.6,0.6);scC.add(plLight);
// ============ SCENE D: stars ============
const scD=new THREE.Scene();scD.background=new THREE.Color(0x02030a);
{const r=rng(13),N=900,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){const a=r()*6.28,b=Math.acos(2*r()-1),rad=40+r()*15;
  p[i*3]=rad*Math.sin(b)*Math.cos(a);p[i*3+1]=rad*Math.cos(b)*0.7+8;p[i*3+2]=rad*Math.sin(b)*Math.sin(a);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 scD.add(new THREE.Points(geo,new THREE.PointsMaterial({color:0xcfe0ff,size:0.22,transparent:true,opacity:0.9,sizeAttenuation:true})));}
scD.add(new THREE.AmbientLight(0x404060,1));
// ============ 2D layers ============
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.42,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(3,2,5,0.62)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=13;}nc.putImageData(id,0,0);}
function mkGrade(top,bot){const c=document.createElement('canvas');c.width=64;c.height=64;
 const x=c.getContext('2d');const gr=x.createLinearGradient(0,0,0,64);
 gr.addColorStop(0,top);gr.addColorStop(1,bot);x.fillStyle=gr;x.fillRect(0,0,64,64);return c;}
const GRADES=[mkGrade('#ffd9a0','#8098c0'),mkGrade('#6a3a80','#ff8850'),
 mkGrade('#1a7a70','#083a46'),mkGrade('#283860','#060a18')];
const sunCv=document.createElement('canvas');sunCv.width=sunCv.height=600;
{const x=sunCv.getContext('2d');const gr=x.createRadialGradient(300,300,10,300,300,300);
 gr.addColorStop(0,'rgba(255,236,190,0.95)');gr.addColorStop(0.25,'rgba(255,210,140,0.45)');
 gr.addColorStop(1,'rgba(255,190,110,0)');x.fillStyle=gr;x.fillRect(0,0,600,600);}
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
const CHIPS=['TERRAIN \u00b7 SNOW \u00b7 FLY-THROUGH','WATER \u00b7 FIRE \u00b7 RAIN \u00b7 DUSK',
 'UNDERWATER \u00b7 CAUSTICS \u00b7 BUBBLES \u00b7 2.5D PLATE','STARFIELD \u00b7 MODE LOCKED'];
const DLBL=['\u092c\u0930\u094d\u092b\u093c\u0940\u0932\u0947 \u092a\u0939\u093e\u0921\u093c \u2014 \u0909\u0921\u093c\u0924\u093e \u0915\u0948\u092e\u0930\u093e',
 '\u0936\u093e\u092e \u0915\u0940 \u091d\u0940\u0932 \u2014 \u092e\u0936\u093e\u0932\u0947\u0902 \u0914\u0930 \u092c\u093e\u0930\u093f\u0936',
 '\u092a\u093e\u0928\u0940 \u0915\u0947 \u0905\u0902\u0926\u0930 \u2014 \u0921\u0942\u092c\u093e \u0939\u0941\u0906 \u0907\u0924\u093f\u0939\u093e\u0938',
 '\u092e\u094b\u0921 \u0925\u094d\u0930\u0940-\u0921\u0940 \u2014 \u0932\u0949\u0915\u094d\u0921'];
function waveZ(x,y,t){return 0.14*Math.sin(x*0.5+t*1.2)+0.10*Math.sin(y*0.7+t*0.9+x*0.3)
 +0.05*Math.sin((x+y)*1.3+t*2.2);}
function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 let si,tl,sc;
 if(t<S1E){si=0;tl=t;sc=scA;}
 else if(t<S2E){si=1;tl=t-S1E;sc=scB;}
 else if(t<S3E){si=2;tl=t-S2E;sc=scC;}
 else{si=3;tl=t-S3E;sc=scD;}
 const shx=0.05*Math.sin(t*7.3)+0.03*Math.sin(t*13.7),shy=0.04*Math.sin(t*9.1+2);
 if(si===0){
  const u=ss(0,7.4,tl);
  const cx=2.2*Math.sin(tl*0.35),cy=11.5-5.3*u,cz=78-88*u;
  cam.position.set(cx+shx,cy+shy,cz);
  cam.lookAt(cx*0.4,6.5,cz-42);
  const pos=SNOW.geometry.attributes.position;
  for(let i=0;i<SNOWD.length;i++){const d=SNOWD[i];
   pos.array[i*3+1]=((d[3]-d[1]*t)%26+26)%26;
   pos.array[i*3]=d[2]+1.3*Math.sin(t*0.7+d[0]);}
  pos.needsUpdate=true;
 }else if(si===1){
  const u=ss(0,5.9,tl);
  cam.position.set(-1.6+3.0*u+shx,2.5-0.75*u+shy,15.5-8.8*u);
  cam.lookAt(0.3,1.15,-6.6);
  const p=WATER.geometry.attributes.position;
  for(let i=0;i<p.count;i++){const x=WBASE[i*3],y=WBASE[i*3+1];
   p.array[i*3+2]=waveZ(x,y,t);}
  p.needsUpdate=true;WATER.geometry.computeVertexNormals();
  for(let i=0;i<TORCH.length;i++)TORCH[i].intensity=1.6+0.45*Math.sin(t*11+i*2)
   +0.28*Math.sin(t*29.9+i*5)+0.16*Math.sin(t*47+i*9);
  for(const F of FIRES){const p2=F.pts.geometry.attributes.position;
   for(let i=0;i<F.dat.length;i++){const d=F.dat[i];
    const ph=(d[0]+t*d[2])%1;const rad=(1-ph*0.7)*0.26*(0.75+0.25*Math.sin(t*13+i));
    p2.array[i*3]=F.x+Math.cos(d[1]+t*2)*rad;
    p2.array[i*3+1]=F.top+ph*0.72+0.06*Math.sin(t*9+i);
    p2.array[i*3+2]=F.z+Math.sin(d[1]+t*2)*rad;}
   p2.needsUpdate=true;}
  const rp=RAIN.geometry.attributes.position;
  for(let i=0;i<RAIND.length;i++){const d=RAIND[i];
   rp.array[i*3+1]=((d[1]-d[2]*t)%12+12)%12;
   rp.array[i*3]=d[0]+0.4*Math.sin(t*0.9+i);}
  rp.needsUpdate=true;
 }else if(si===2){
  const u=ss(0,9.5,tl);
  cam.position.set(0.5+0.8*u+shx*1.4,9.4-7.6*u+shy*1.4,12.6-10.5*u);
  cam.lookAt(0,1.32,-2.6);
  CAUS[0].offset.set(t*0.025,t*0.018);CAUS[1].offset.set(-t*0.021,t*0.028);
  for(let i=0;i<SHAFTS.length;i++){SHAFTS[i].rotation.y=t*0.12+i;
   SHAFTS[i].material.opacity=0.045+0.02*Math.sin(t*0.8+i*2);}
  plLight.intensity=0.8+0.15*Math.sin(t*5.1)+0.1*Math.sin(t*11.7);
  const bp=BUB.geometry.attributes.position;
  for(let i=0;i<BUBD.length;i++){const d=BUBD[i];
   bp.array[i*3+1]=((d[1]+d[2]*t)%9+9)%9+0.2;
   bp.array[i*3]=d[0]+0.35*Math.sin(t*1.8+d[3]);}
  bp.needsUpdate=true;
 }else{
  cam.position.set(0,2,0.1);
  cam.lookAt(Math.sin(tl*0.07+2.2)*10,6+tl*0.4,-12);
 }
 renderer.render(sc,cam);
 // ---- composite ----
 g.fillStyle='#000';g.fillRect(0,0,W,H);
 g.drawImage(gl,0,0,W,H);
 blg.drawImage(gl,0,0,320,180);
 g.save();g.globalCompositeOperation='lighter';
 g.globalAlpha=[0.06,0.16,0.19,0.12][si];g.drawImage(bl,0,0,W,H);g.restore();
 if(si===0){g.save();g.globalCompositeOperation='lighter';g.globalAlpha=0.32;
  g.drawImage(sunCv,W*0.74-210,H*0.16-210,420,420);g.restore();}
 g.save();g.globalCompositeOperation='overlay';g.globalAlpha=0.16;
 g.drawImage(GRADES[si],0,0,W,H);g.restore();
 // band
 g.fillStyle='rgba(7,5,10,0.92)';g.fillRect(0,H-96,W,96);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-96,W,3);
 T(60,H-46,'MODE 3D \u00b7 REAL-FEEL TEST','Mono',30,'#ff8c3b','left',1,2);
 T(W/2+80,H-46,DLBL[si],'Deva',32,'#eef2f8','center');
 T(W-60,H-46,'CODE SE \u00b7 NO AI VIDEO','Mono',21,'rgba(238,242,248,0.55)','right',1,2);
 T(60,66,CHIPS[si],'Mono',23,'rgba(238,242,248,0.62)','left',0.95,3);
 if(si===3){
  const a=ss(S3E+0.5,S3E+1.1,t);
  T(W/2,H*0.40,'MODE 3D','Mono',128,'rgba(238,242,248,'+a+')','center',1,10);
  T(W/2,H*0.53,'\u0905\u0938\u0932\u0940 \u0915\u0948\u092e\u0930\u093e \u2014 \u0905\u0938\u0932\u0940 \u090f\u0939\u0938\u093e\u0938 \u2014 \u0932\u0949\u0915\u094d\u0921','Deva',38,'rgba(232,178,74,'+a+')','center');
  T(W/2,H*0.62,'TERRAIN \u00b7 WATER \u00b7 FIRE \u00b7 RAIN \u00b7 UNDERWATER \u00b7 CAUSTICS \u00b7 STARS','Mono',22,'rgba(238,242,248,'+(a*0.6)+')','center',1,3);}
 g.save();g.globalAlpha=0.4;
 g.drawImage(noiseCv,-(Math.floor(t*13)%19),-(Math.floor(t*7)%23),W+40,H+40);g.restore();
 g.drawImage(vig,0,0);
 g.save();g.fillStyle='rgba(255,255,255,0.2)';g.fillRect(0,H-4,W,4);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
 let dark=1-ss(0,0.55,t);
 for(const b of[S1E,S2E,S3E])dark=Math.max(dark,1-ss(0,0.3,Math.abs(t-b)));
 dark=Math.max(dark,ss(TOTAL-0.9,TOTAL-0.1,t));
 if(dark>0){g.save();g.globalAlpha=dark;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
window.renderAt=function(t){draw(t);return cv.toDataURL('image/jpeg',0.85);};
window.renderBatch=function(ts){const out=[];for(const t of ts){draw(t);out.push(cv.toDataURL('image/jpeg',0.85));}return out;};
document.fonts.ready.then(()=>{
 const wait=()=>{if(texOk){try{draw(2);draw(10);draw(18);draw(25);window.__ready=true;}catch(e){window.__err=''+(e.stack||e);}}
  else setTimeout(wait,60);};
 wait();});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff).replace("THREELIB", three)
    html = html.replace("__TOT__", str(TOTAL))
    html = html.replace("GAN64", b64(PT + "/card_adiganesh.jpg"))
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
            page.wait_for_function("window.__ready === true || window.__err", timeout=150000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            TSL = [float(x) for x in os.environ.get("CHK_TIMES", "2.5,6,9.5,12.8,16.5,22,26.5").split(",")]
            ims = []
            for st in TSL:
                d = page.evaluate("window.renderAt(%f)" % st)
                ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))))
            tw, th = 640, 360
            cols = 2; rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw, rows * th), "black")
            for i, im in enumerate(ims):
                sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
            sheet.save(os.path.join(ROOT, "preview_sheet.jpg"), quality=86)
            browser.close(); print("preview ->", os.path.join(ROOT, "preview_sheet.jpg")); return
        FR = os.path.join(ROOT, "frames"); os.makedirs(FR, exist_ok=True)
        n = int(round(TOTAL * FPS)); t0 = time.time(); i = 0
        while i < n:
            batch = [k for k in range(i, min(i + 6, n))
                     if not os.path.exists(os.path.join(FR, "%05d.jpg" % k))]
            if batch:
                urls = page.evaluate("ts => window.renderBatch(ts)", [k / FPS for k in batch])
                for k, d in zip(batch, urls):
                    open(os.path.join(FR, "%05d.jpg" % k), "wb").write(base64.b64decode(d.split(",", 1)[1]))
            i += 6
            if (i // 6) % 20 == 0:
                print("frame %d/%d (%.1f fps)" % (i, n, i / max(0.01, time.time() - t0)), flush=True)
        browser.close()
    build_audio()
    print("FRAMES+AUDIO DONE n=%d" % n)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
