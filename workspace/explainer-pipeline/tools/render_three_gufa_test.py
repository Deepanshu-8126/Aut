#!/usr/bin/env python3
# THREE.JS 3D TEST — "GUFA DIORAMA" (skill 10-3d-scene-spec, ZEUS-style spec)
# 1 WHAT: ek Patal-gufa chamber. Center: stone pedestal + amber dome shila.
#   Back wall: hamari AI engraving framed plate (image->3D diorama trick). Bas.
# 2 MOVES: camera dolly-in + slow orbit (never cuts); droplet falls every 1.8s
#   onto dome -> ripple ring + light pulse; 300 dust motes drift; torch flickers.
# 3 LOOK: bg/fog #050308, warm amber pedestal light + cool cyan rim, matte rock,
#   dense fog, grain+vignette in 2D composite.
# 6 BANNED: lens flare, hard shadows, text inside 3D, realistic textures.
# 7 BUDGET: (1) chamber+fog (2) camera path (3) pedestal glow (4) stalactites
#   (5) droplet+ripple (6) dust+shaft. Ship 1-3 minimum.
# 8 PROOF: --preview checkpoints before render; frame-verify final mp4.
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/three3d"
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
TOTAL = 15.5

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
def drip(a=0.2):
    t = np.arange(_n(0.3)) / SR
    return a * np.sin(2 * np.pi * (2200 - 1400 * t) * t) * np.exp(-t * 26)
def bell(f, a, d=2.2):
    t = np.arange(_n(d)) / SR
    return a * (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2.76*t)) * np.exp(-t * 2.1)

def build_audio():
    n = _n(TOTAL); sfx = np.zeros(n); vo = np.zeros(n)
    def put(dst, x, at):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); dst[i:i + L] += x[:L]
    put(sfx, whoosh(0.8, 0.3), 0.1)
    tt = 1.1
    while tt < TOTAL - 1:
        put(sfx, drip(0.18), tt + 0.9); tt += 1.8
    put(sfx, bell(587, 0.14), TOTAL - 2.6)
    wv = os.path.join(ROOT, "tvo3d.wav")
    if not os.path.exists(wv):
        subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(PR, "tvo3d.mp3"),
                        "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
    wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
    wf.close()
    i0 = _n(0.5); L = min(len(dat), n - i0)
    vo[i0:i0 + L] += dat[:L] * 1.3
    t = np.arange(n) / SR
    mus = 0.04 * (np.sin(2 * np.pi * 73.42 * t) + np.sin(2 * np.pi * 73.73 * t + 0.8)) \
        + 0.006 * np.sin(2 * np.pi * 220 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.09 * t))
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    mus *= (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.9 + mus
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
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const gl=document.createElement('canvas');gl.width=GW;gl.height=GH;
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
// ---------- THREE scene ----------
const renderer=new THREE.WebGLRenderer({canvas:gl,antialias:false});
renderer.setSize(GW,GH,false);
renderer.outputEncoding=THREE.sRGBEncoding;
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x050308);
scene.fog=new THREE.FogExp2(0x050308,0.052);
const cam=new THREE.PerspectiveCamera(42,GW/GH,0.1,100);
// cave walls: displaced cylinder
{const geo=new THREE.CylinderGeometry(11,11,14,56,20,true);
 const pos=geo.attributes.position,r=rng(21);
 const bump=[];for(let i=0;i<pos.count;i++)bump.push(r());
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i);
  const d=1-0.14*bump[i]-0.06*Math.sin(y*1.7+x*0.8)*Math.cos(z*0.9);
  pos.setX(i,x*d);pos.setZ(i,z*d);}
 geo.computeVertexNormals();
 const mat=new THREE.MeshStandardMaterial({color:0x4a3a30,roughness:0.95,metalness:0.02,side:THREE.BackSide});
 const m=new THREE.Mesh(geo,mat);m.position.y=5;scene.add(m);}
// floor
{const geo=new THREE.CircleGeometry(11.5,48);
 const pos=geo.attributes.position,r=rng(33);
 for(let i=0;i<pos.count;i++){const d=Math.hypot(pos.getX(i),pos.getY(i));
  if(d>1.8)pos.setZ(i,0.22*r()-0.11);}
 geo.computeVertexNormals();
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:0x3c3028,roughness:0.95}));
 m.rotation.x=-Math.PI/2;scene.add(m);}
// stalactites + stalagmites
{const r=rng(55);
 for(let i=0;i<16;i++){
  const a=r()*6.28,rad=3.2+r()*6,hh=1.2+r()*2.6;
  const cone=new THREE.Mesh(new THREE.ConeGeometry(0.28+r()*0.5,hh,7),
   new THREE.MeshStandardMaterial({color:0x56453a,roughness:0.9}));
  cone.position.set(Math.cos(a)*rad,11.6-hh/2,Math.sin(a)*rad);
  cone.rotation.x=Math.PI;cone.rotation.z=(r()-0.5)*0.15;scene.add(cone);
  if(r()>0.45){const h2=0.5+r()*1.3;
   const up=new THREE.Mesh(new THREE.ConeGeometry(0.3+r()*0.4,h2,7),
    new THREE.MeshStandardMaterial({color:0x4e3f34,roughness:0.95}));
   up.position.set(Math.cos(a)*rad*(0.8+r()*0.3),h2/2,Math.sin(a)*rad*(0.8+r()*0.3));
   scene.add(up);}}}
// pedestal + dome shila
{const ped=new THREE.Mesh(new THREE.CylinderGeometry(1.5,1.9,1.1,24),
  new THREE.MeshStandardMaterial({color:0x5a4a3c,roughness:0.85}));
 ped.position.y=0.55;scene.add(ped);
 const dome=new THREE.Mesh(new THREE.SphereGeometry(0.95,24,18,0,6.29,0,1.62),
  new THREE.MeshStandardMaterial({color:0x8a5a28,roughness:0.5,metalness:0.15,
   emissive:0x331c06,emissiveIntensity:1}));
 dome.position.y=1.1;dome.scale.y=1.25;scene.add(dome);
 window.DOME=dome;}
// engraving plate on back wall (image -> 3D diorama)
const texLoader=new THREE.TextureLoader();let texOk=0;
texLoader.load('data:image/jpeg;base64,GAN64',(tx)=>{
 tx.encoding=THREE.sRGBEncoding;
 const fr=new THREE.Mesh(new THREE.PlaneGeometry(4.6,3.1),
  new THREE.MeshStandardMaterial({color:0xeadfc8,roughness:0.9}));
 fr.position.set(-4.4,3.4,-7.6);fr.rotation.y=0.42;scene.add(fr);
 const pl=new THREE.Mesh(new THREE.PlaneGeometry(4.3,2.8),
  new THREE.MeshStandardMaterial({map:tx,roughness:0.85}));
 pl.position.set(-4.38,3.4,-7.55);pl.rotation.y=0.42;scene.add(pl);
 texOk=1;});
// droplet + ripple
const drop=new THREE.Mesh(new THREE.SphereGeometry(0.09,10,8),
 new THREE.MeshStandardMaterial({color:0x9adfff,emissive:0x3a7a99,roughness:0.2}));
scene.add(drop);
const ripple=new THREE.Mesh(new THREE.TorusGeometry(0.5,0.03,8,36),
 new THREE.MeshBasicMaterial({color:0x7ad0ff,transparent:true,opacity:0}));
ripple.rotation.x=-Math.PI/2;ripple.position.y=2.12;scene.add(ripple);
// light shaft cone (additive)
const shaft=new THREE.Mesh(new THREE.ConeGeometry(2.6,10.5,24,1,true),
 new THREE.MeshBasicMaterial({color:0x8fb8d8,transparent:true,opacity:0.07,
  blending:THREE.AdditiveBlending,side:THREE.DoubleSide,depthWrite:false}));
shaft.position.set(0,6.4,0);scene.add(shaft);
// dust points
{const r=rng(77),N=320,pos=new Float32Array(N*3);window.DUSTP=[];
 for(let i=0;i<N;i++){const a=r()*6.28,rad=r()*8,y=0.3+r()*9;
  pos[i*3]=Math.cos(a)*rad;pos[i*3+1]=y;pos[i*3+2]=Math.sin(a)*rad;
  DUSTP.push([r()*6.28,0.08+r()*0.2]);}
 const geo=new THREE.BufferGeometry();
 geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
 const m=new THREE.Points(geo,new THREE.PointsMaterial({color:0xd8c9a8,size:0.045,
  transparent:true,opacity:0.65,sizeAttenuation:true}));
 scene.add(m);window.DUST=m;}
// lights
scene.add(new THREE.AmbientLight(0x202030,0.7));
const warm=new THREE.PointLight(0xffa04a,1.5,16,2);warm.position.set(0,2.6,0);scene.add(warm);
const warm2=new THREE.PointLight(0xff8838,0.7,10,2);warm2.position.set(3.2,1.4,2.6);scene.add(warm2);
const rim=new THREE.DirectionalLight(0x3a6a9a,0.5);rim.position.set(-6,8,-4);scene.add(rim);
const down=new THREE.SpotLight(0x9ec8e8,0.9,20,0.42,0.5,1.5);
down.position.set(0,11.5,0);down.target.position.set(0,0,0);scene.add(down);scene.add(down.target);
// ---------- 2D composite ----------
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.4,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(3,2,5,0.6)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=13;}nc.putImageData(id,0,0);}
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 // camera path: dolly-in + slow orbit, never cuts
 const u=ss(0,TOTAL*0.92,t);
 const ang=-0.42+0.75*u, rad=15.5-8.2*u, cy=3.4-0.7*u+0.06*Math.sin(t*0.8);
 cam.position.set(Math.sin(ang)*rad,cy,Math.cos(ang)*rad);
 cam.lookAt(0,2.1,0);
 // droplet loop
 const ph=((t+0.7)%1.8)/1.8;
 const dy=6.2-(6.2-2.15)*Math.min(1,ph/0.52)*Math.pow(Math.min(1,ph/0.52),1);
 drop.position.set(0,ph<0.52?6.2-(6.2-2.15)*Math.pow(ph/0.52,2):2.15,0);
 drop.visible=ph<0.56;
 const rp=clamp((ph-0.52)/0.45,0,1);
 ripple.scale.setScalar(0.4+rp*2.2);
 ripple.material.opacity=rp>0?0.5*(1-rp):0;
 warm.intensity=1.5+0.25*Math.sin(t*13)+0.12*Math.sin(t*31)+(rp>0?0.6*(1-rp):0);
 shaft.rotation.y=t*0.1;shaft.material.opacity=0.06+0.02*Math.sin(t*0.7);
 // dust drift
 const pos=DUST.geometry.attributes.position;
 for(let i=0;i<DUSTP.length;i++){
  pos.array[i*3]+=Math.sin(t*0.5+DUSTP[i][0])*0.0012;
  pos.array[i*3+1]+=DUSTP[i][1]*0.004*Math.sin(t*0.3+i);
  pos.array[i*3+2]+=Math.cos(t*0.4+DUSTP[i][0])*0.0012;}
 pos.needsUpdate=true;
 renderer.render(scene,cam);
 // composite
 g.fillStyle='#000';g.fillRect(0,0,W,H);
 g.drawImage(gl,0,0,W,H);
 // band
 g.fillStyle='rgba(7,5,10,0.92)';g.fillRect(0,H-96,W,96);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-96,W,3);
 T(60,H-46,'THREE.JS 3D TEST \u00b7 GUFA DIORAMA','Mono',32,'#ff8c3b','left',1,2);
 T(840,H-46,'\u0905\u0938\u0932\u0940 \u0925\u094d\u0930\u0940-\u0921\u0940 \u0915\u0948\u092e\u0930\u093e \u2014 \u0915\u094b\u0921 \u0938\u0947','Deva',32,'#eef2f8','left');
 T(W-60,H-46,'REAL-TIME CODE \u00b7 NO AI VIDEO','Mono',22,'rgba(238,242,248,0.55)','right',1,2);
 T(60,70,'SPEC \u2192 BUILD \u2192 PROOF','Mono',24,'rgba(238,242,248,0.5)','left',ss(0.5,1.2,t),3);
 // grain + vignette + progress
 g.save();g.globalAlpha=0.4;
 g.drawImage(noiseCv,-(Math.floor(t*13)%19),-(Math.floor(t*7)%23),W+40,H+40);g.restore();
 g.drawImage(vig,0,0);
 g.save();g.fillStyle='rgba(255,255,255,0.2)';g.fillRect(0,H-4,W,4);
 g.fillStyle='#ff8c3b';g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
 const fi=ss(0,0.5,t);
 if(fi<1){g.save();g.globalAlpha=1-fi;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
 const out=ss(TOTAL-1.0,TOTAL-0.1,t);
 if(out>0){g.save();g.globalAlpha=out;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
window.renderAt=function(t){draw(t);return cv.toDataURL('image/jpeg',0.85);};
window.renderBatch=function(ts){const out=[];for(const t of ts){draw(t);out.push(cv.toDataURL('image/jpeg',0.85));}return out;};
document.fonts.ready.then(()=>{
 const wait=()=>{if(texOk){try{draw(1);draw(8);window.__ready=true;}catch(e){window.__err=''+(e.stack||e);}}
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
            page.wait_for_function("window.__ready === true || window.__err", timeout=120000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            TSL = [float(x) for x in os.environ.get("CHK_TIMES", "1.5,4,7,10,13,15").split(",")]
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
