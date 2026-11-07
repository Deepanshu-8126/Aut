#!/usr/bin/env python3
"""
MODE 1E TEST — tabletop3d (drawn-by-code, MIT) — "Stonehenge on a desk"
Raymarched GLSL miniature: 3 stone blocks hop in stop-motion onto a cutting mat
and assemble a trilithon; sticky note reads STONEHENGE?. 10s | 1080x1920 | 24fps.
Run: --preview | --render   (speed test: --speed)
"""
import os, sys, json, base64, subprocess, time, wave, io
import numpy as np
import imageio_ffmpeg
from PIL import Image

W, H = 1080, 1920
FPS = 24
DUR = 10.0
ROOT = "/var/tmp/tt3d"
os.makedirs(ROOT, exist_ok=True)
AST = "/home/user/explainer-pipeline/assets"
DBC = os.path.join(AST, "dbc")
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FF = imageio_ffmpeg.get_ffmpeg_exe()
CHROME = "/opt/playwright/browsers/chromium-1248/chrome-linux64/chrome"
SR = 48000


def b64f(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()


HTML = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Hand';src:url(data:font/ttf;base64,__F_HAND__);}
@font-face{font-family:'Mono';src:url(data:font/ttf;base64,__F_MONO__);}
body{margin:0;background:#111;}
</style><script>__CORE__</script><script>__TT3D__</script></head><body>
<canvas id="out" width="1080" height="1920"></canvas>
<script>
const W=1080,H=1920;
const out=document.getElementById('out'), ctx=out.getContext('2d');
function cl(v){return Math.max(0,Math.min(1,v));}
function ss(a,b,t){const x=cl((t-a)/(b-a));return x*x*(3-2*x);}
function lerp(a,b,u){return a+(b-a)*u;}

const GLSL=`
// a megalith block: rounded box with chipped edges
float megalith(vec3 p, vec3 h){
  float d=sdRoundBox(p,h,0.09);
  d+=0.015*noise(p*5.0)-0.0075;        // hewn surface
  return d;
}
vec2 map(vec3 p){
  // desk wood
  vec2 r=vec2(p.y+0.0,1.0);
  // cutting mat
  float mat=sdBox(p-vec3(0.0,0.05,0.0),vec3(9.0,0.05,7.5));
  r=opU(r,vec2(mat,2.0));
  // the far wall
  r=opU(r,vec2(22.0+p.z,7.0));
  // a mug behind, out of focus
  vec3 mp=p-vec3(11.0,0.0,-13.0);
  float cup=sdCylinder(mp-vec3(0.0,4.75,0.0),4.75,4.1)-0.1;
  cup=max(cup,-sdCylinder(mp-vec3(0.0,5.6,0.0),4.4,3.7));
  cup=min(cup,sdTorus((mp-vec3(-4.5,5.0,0.0)).xzy,vec2(1.9,0.42)));
  r=opU(r,vec2(cup,10.0));
  // a pencil lying at the right
  vec3 pp=p-vec3(5.2,0.14,3.4); pp.xz=rot(-0.5)*pp.xz;
  float pen=sdCappedCylinder(pp,vec3(-2.6,0.0,0.0),vec3(2.2,0.0,0.0),0.14);
  pen=min(pen,sdRoundCone(pp,vec3(2.2,0.0,0.0),vec3(2.85,0.0,0.0),0.14,0.02));
  r=opU(r,vec2(pen,11.0));
  // upright A: position PF(0..2), yaw PF(3)
  vec3 a=p-vec3(PF(0),PF(1),PF(2)); a.xz=rot(PF(3))*a.xz;
  r=opU(r,vec2(megalith(a,vec3(0.55,1.45,0.38)),20.0));
  // upright B: PF(4..7)
  vec3 b=p-vec3(PF(4),PF(5),PF(6)); b.xz=rot(PF(7))*b.xz;
  r=opU(r,vec2(megalith(b,vec3(0.52,1.42,0.40)),20.0));
  // lintel: PF(8..11), extra pitch PF(12)
  vec3 c=p-vec3(PF(8),PF(9),PF(10)); c.xz=rot(PF(11))*c.xz; c.xy=rot(PF(12))*c.xy;
  r=opU(r,vec2(megalith(c,vec3(1.55,0.38,0.45)),21.0));
  // sticky note in front (texture uTex0)
  vec3 np=p-vec3(-1.0,0.11,5.3);
  np.xz=rot(0.14)*np.xz;
  np.y-=0.09*pow(max(0.0,-np.z-0.6),2.0);
  r=opU(r,vec2(sdBox(np,vec3(1.75,0.015,1.75))*0.8,6.0));
  return r;
}
vec3 albedo(float m, vec3 p, vec3 n){
  if(m==1.0){float w=woodGrain(p);return mix(vec3(0.60,0.41,0.25),vec3(0.40,0.25,0.14),w);}
  if(m==2.0){
    vec2 g=abs(fract(p.xz+0.5)-0.5), g5=abs(fract(p.xz/5.0+0.5)-0.5)*5.0;
    float line=max(smoothstep(0.03,0.0,min(g.x,g.y))*0.55,smoothstep(0.05,0.0,min(g5.x,g5.y)));
    return mix(vec3(0.15,0.33,0.27)*(0.94+0.12*noise(p*6.0)),vec3(0.76,0.84,0.78),line*0.8);
  }
  if(m==20.0||m==21.0){ // weathered sarsen grey, lichen tint
    float sp=fbm(p*2.6);
    vec3 base=mix(vec3(0.56,0.55,0.52),vec3(0.36,0.36,0.35),sp);
    return mix(base,vec3(0.45,0.52,0.38),smoothstep(0.62,0.85,fbm(p*1.3+7.0))*0.5);
  }
  if(m==10.0)return vec3(0.24,0.38,0.60);
  if(m==11.0){ // pencil: yellow body
    return vec3(0.85,0.62,0.12);
  }
  if(m==7.0)return vec3(0.8,0.74,0.66);
  if(m==6.0){
    vec3 np=p-vec3(-1.0,0.11,5.3); np.xz=rot(0.14)*np.xz;
    vec2 uv=np.xz/3.5+0.5;
    return texture(uTex0,uv).rgb*(0.96+0.08*fibres(p));
  }
  return vec3(0.55,0.5,0.46)*(0.9+0.1*noise(p*0.8));
}
vec4 material(float m){
  if(m==20.0||m==21.0)return vec4(0.82,0.0,0.12,0.004); // rough stone
  if(m==10.0)return vec4(0.14,0.0,0.0,0.0);             // glazed ceramic
  if(m==11.0)return vec4(0.35,0.0,0.0,0.0);             // painted wood
  if(m==6.0)return vec4(0.85,0.0,0.3,0.004);            // paper
  if(m==2.0)return vec4(0.7,0.0,0.1,0.0);
  return vec4(0.6,0.0,0.1,0.006);
}
float relief(float m, vec3 p){
  if(m==20.0||m==21.0)return fbm(p*3.0)*0.8;
  return m==6.0?fibres(p):m==1.0?woodGrain(p):0.0;
}
`;

const env={px:[W,H]};
let R=null, note=null;
function setupGL(){
  note=document.createElement('canvas');
  note.width=note.height=512;
  const x=note.getContext('2d');
  x.fillStyle='#f4d65a';x.fillRect(0,0,512,512);
  x.save();x.translate(256,256);x.rotate(-0.04);
  x.fillStyle='#2b2a6e';x.font='82px Hand';x.textAlign='center';
  x.fillText('stonehenge',0,-25);x.fillText('...but why?',0,80);
  x.restore();
  R=Tabletop3D.renderer(env,{scene:GLSL,scale:__SCALE__,params:16,band:160});
  return 'ok';
}

// ---- stop-motion choreography (drawings on twos, d = floor(t*12)) ----
// hop helper: from a to b between tq0..tq1 with height h
function hop(tq,t0,t1,a,b,h){
  const u=cl((tq-t0)/(t1-t0));
  return [lerp(a[0],b[0],u), lerp(a[1],b[1],u)+4*h*u*(1-u), lerp(a[2],b[2],u), u];
}
function pose(t){
  const d=Math.floor(t*8+1e-6), tq=d/8;
  // upright A: hops in from the left in 3 hops, 0.8s..3.0s
  const A0=[-9.5,1.5,0.6],A1=[-6.3,1.5,0.3],A2=[-3.6,1.5,0.1],A3=[-1.65,1.5,0.0];
  let A=A0,ay=0.12;
  if(tq<0.8)A=A0;
  else if(tq<1.5)A=hop(tq,0.8,1.5,A0,A1,1.1);
  else if(tq<2.2)A=hop(tq,1.5,2.2,A1,A2,1.1);
  else if(tq<3.0)A=hop(tq,2.2,3.0,A2,A3,1.3);
  else {A=A3;ay=0.12;}
  // settle wobble just after landing
  let aroll=0; if(tq>=3.0&&tq<3.4)aroll=0.06*Math.cos((tq-3.0)*34.0);
  // upright B: from the right, 2.6s..4.8s
  const B0=[9.5,1.5,0.5],B1=[5.8,1.5,0.2],B2=[1.65,1.5,0.0];
  let Bp=B0,by=-0.1;
  if(tq<2.6)Bp=B0;
  else if(tq<3.6)Bp=hop(tq,2.6,3.6,B0,B1,1.2);
  else if(tq<4.6)Bp=hop(tq,3.6,4.6,B1,B2,1.4);
  else Bp=B2;
  let broll=0; if(tq>=4.6&&tq<5.0)broll=-0.06*Math.cos((tq-4.6)*34.0);
  // lintel: lies in front, tilts (anticipation), flies up in an arc 5.6s..7.2s, lands flat
  const L0=[0.0,0.42,3.0],L1=[0.0,3.35,0.0];
  let L=L0,lpitch=0,lyaw=0.0;
  if(tq<5.2){L=L0;lyaw=0.3;}
  else if(tq<5.6){L=L0;lyaw=0.3;lpitch=(tq-5.2)*0.45;}
  else if(tq<7.2){const h2=hop(tq,5.6,7.2,L0,L1,2.1);L=h2;lpitch=0.18*(1-h2[3]);lyaw=0.3*(1-h2[3]);}
  else L=L1;
  let lroll=0; if(tq>=7.2&&tq<7.7)lroll=0.05*Math.cos((tq-7.2)*30.0);
  const nA=Tabletop3D.nudge(d,'A',0.006), nB=Tabletop3D.nudge(d,'B',0.006), nL=Tabletop3D.nudge(d,'L',0.006);
  return {d:d,p:[
    A[0]+nA[0],A[1],A[2]+nA[2], ay+aroll,
    Bp[0]+nB[0],Bp[1],Bp[2]+nB[2], by+broll,
    L[0]+nL[0],L[1],L[2]+nL[2], lyaw, lpitch+lroll]};
}
function drawTag(){
  ctx.save();
  ctx.font='700 26px Mono';ctx.textAlign='left';ctx.textBaseline='alphabetic';
  ctx.fillStyle='rgba(255,255,255,0.78)';
  ctx.fillText('MODE 1E TEST \u00b7 TABLETOP3D',64,120);
  ctx.strokeStyle='rgba(255,255,255,0.45)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(64,134);ctx.lineTo(64+386,134);ctx.stroke();
  ctx.restore();
}
function emblem(){
  const img=IMGS.logo; if(!img)return;
  const s=92,x=W-s-56,y=64;
  ctx.save();ctx.globalAlpha=0.92;
  ctx.beginPath();ctx.arc(x+s/2,y+s/2,s/2,0,Math.PI*2);ctx.clip();
  ctx.drawImage(img,x,y,s,s);ctx.restore();
  ctx.strokeStyle='rgba(212,168,67,0.8)';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.arc(x+s/2,y+s/2,s/2+1,0,Math.PI*2);ctx.stroke();
}
window.renderAt=function(t){
  const q=pose(t);
  // slow push-in; camera cut closer for the final seconds
  const push=ss(0,10,t);
  const cam=t<7.6?[ -1.4, lerp(8.6,7.6,push), lerp(19.5,17.5,push)]
                 :[ 1.5, 4.8, 13.6];
  const tgt=t<7.6?[0.0,1.6,0.6]:[0.05,1.8,0.1];
  R.render(ctx,q.d,{
    p:q.p, cam:cam, target:tgt, fov:0.5,
    focus:t<7.6?lerp(19.5,17.5,push):13.6, aperture:0.4,
    keyDir:[-0.55,0.8,0.45], key:2.3, soft:6,
    lampPos:[9,9,-2], lamp:1.15, lampReach:13,
    exposure:Tabletop3D.flicker(q.d), textures:[note],
  });
  Tabletop3D.post(ctx,env,q.d);
  drawTag();emblem();
  return out.toDataURL('image/jpeg',0.92);
};
window.renderBatch=function(ts){return ts.map(t=>window.renderAt(t));};
const IMGS={};
const im=new Image();
window.onerror=(m)=>{window.__err=String(m);};
im.onload=()=>{IMGS.logo=im;
  document.fonts.ready.then(()=>{
    try{setupGL();window.renderAt(0.01);window.__ready=true;}
    catch(e){window.__err=String(e);}
  });};
im.src='data:image/png;base64,__LOGO__';
</script></body></html>
"""


def build_html(scale):
    html = (HTML
            .replace("__CORE__", open(os.path.join(DBC, "core.js")).read())
            .replace("__TT3D__", open(os.path.join(DBC, "tabletop3d.js")).read())
            .replace("__F_HAND__", b64f(os.path.join(DBC, "PatrickHand-Regular.ttf")))
            .replace("__F_MONO__", b64f(os.path.join(AST, "fonts/JetBrainsMono-Bold.ttf")))
            .replace("__LOGO__", b64f(LOGO))
            .replace("__SCALE__", str(scale)))
    hp = os.path.join(ROOT, "index.html")
    with open(hp, "w") as f:
        f.write(html)
    return hp


def build_audio():
    N = int(DUR * SR)
    mix = np.zeros(N, dtype=np.float32)
    t = np.arange(N) / SR
    # room tone + lamp hum
    mix += (np.sin(2 * np.pi * 50 * t) * 0.012 + np.sin(2 * np.pi * 120 * t) * 0.006).astype(np.float32)
    rng = np.random.default_rng(7)
    nz = rng.standard_normal(N).astype(np.float32)
    k = int(SR * 0.012)
    nz = np.convolve(nz, np.ones(k) / k, mode="same")
    mix += nz * 0.015

    def seg(s, d):
        i0 = int(s * SR); i1 = min(N, i0 + int(d * SR)); return i0, i1, np.arange(i1 - i0) / SR

    def thud(t0, a=0.3, f=70):
        i0, i1, lt = seg(t0, 0.3)
        mix[i0:i1] += ((np.sin(2 * np.pi * f * lt) + 0.4 * rng.standard_normal(len(lt))) *
                       np.exp(-lt * 16) * a).astype(np.float32)

    def tick(t0, a=0.1):
        i0, i1, lt = seg(t0, 0.05)
        mix[i0:i1] += (rng.standard_normal(len(lt)) * np.exp(-lt * 90) * a).astype(np.float32)

    # hops land (A: 1.5,2.2,3.0 · B: 3.6,4.6 · lintel: 7.2)
    for s, a, f in [(1.5 / 1, 0.22, 85), (2.2, 0.22, 82), (3.0, 0.3, 75),
                    (3.6, 0.24, 85), (4.6, 0.3, 72), (7.2, 0.42, 58)]:
        thud(s, a, f)
    for s in np.arange(0.4, 9.6, 1 / 12 * 4):  # faint stop-motion camera ticks
        tick(s, 0.03)
    # small end chime
    i0, i1, lt = seg(8.6, 1.0)
    mix[i0:i1] += (np.sin(2 * np.pi * 988 * lt) * np.exp(-lt * 4) * 0.05).astype(np.float32)
    mix = np.tanh(mix * 1.1) * 0.9
    st = np.stack([mix, mix], axis=1)
    wf = wave.open(os.path.join(ROOT, "master.wav"), "wb")
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((st * 32767).astype(np.int16).tobytes())
    wf.close()


def run(mode):
    scale = 0.26
    hp = build_html(scale)
    from playwright.sync_api import sync_playwright
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/playwright/browsers"
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True, args=[
            "--use-gl=angle", "--use-angle=swiftshader", "--no-sandbox",
            "--disable-dev-shm-usage", "--js-flags=--max-old-space-size=2048"])
        page = browser.new_page(viewport={"width": 200, "height": 120})
        page.goto("file://" + hp)
        try:
            page.wait_for_function("window.__ready===true||window.__err", timeout=240000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return

        if mode == "--speed":
            t0 = time.time()
            page.evaluate("window.renderAt(1.9)")
            t1 = time.time()
            page.evaluate("window.renderAt(2.1)")   # new drawing
            t2 = time.time()
            page.evaluate("window.renderAt(2.13)")  # memoised (same drawing)
            t3 = time.time()
            print("first %.2fs | new drawing %.2fs | memo %.3fs" % (t1 - t0, t2 - t1, t3 - t2))
            browser.close(); return

        if mode == "--preview":
            ims = []
            chk = os.environ.get("CHK_TIMES")
            TSL = ([float(x) for x in chk.split(",")] if chk
                   else [1.0, 2.8, 4.4, 6.6, 7.9, 9.5])
            for st in TSL:
                d = page.evaluate("window.renderAt(%f)" % st)
                ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))))
            tw, th = 360, 640
            cols = min(3, len(ims)); rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw, rows * th), "black")
            for i, im in enumerate(ims):
                sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
            sheet.save(os.path.join(ROOT, "preview_sheet.jpg"), quality=88)
            browser.close()
            print("preview ->", os.path.join(ROOT, "preview_sheet.jpg"))
            return

        FR = os.path.join(ROOT, "frames")
        os.makedirs(FR, exist_ok=True)
        DFPS = 8
        n = int(round(DUR * DFPS))
        t0 = time.time()
        BATCH = 6
        i = 0
        while i < n:
            j = min(n, i + BATCH)
            todo = [k for k in range(i, j) if not os.path.exists(os.path.join(FR, "f_%05d.jpg" % k))]
            if todo:
                ts = [(k + 0.02) / DFPS for k in todo]
                data = page.evaluate("window.renderBatch(%s)" % json.dumps(ts))
                for k, d in zip(todo, data):
                    with open(os.path.join(FR, "f_%05d.jpg" % k), "wb") as f:
                        f.write(base64.b64decode(d.split(",", 1)[1]))
            i = j
            if (i // BATCH) % 8 == 0:
                el = time.time() - t0
                print("frame %d/%d (%.1f fps)" % (i, n, i / max(el, 1)), flush=True)
        browser.close()

    print("RENDER WALL TIME: %.1fs" % (time.time() - t0))
    build_audio()
    out = os.path.join(ROOT, "final.mp4")
    subprocess.run([FF, "-nostdin", "-y", "-framerate", "8",
                    "-i", os.path.join(FR, "f_%05d.jpg"), "-r", str(FPS),
                    "-i", os.path.join(ROOT, "master.wav"),
                    "-c:v", "libx264", "-preset", "veryfast", "-threads", "2",
                    "-crf", "21", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    print("SUCCESS:", out, "%.2f MB" % (os.path.getsize(out) / 1e6))


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--preview")
