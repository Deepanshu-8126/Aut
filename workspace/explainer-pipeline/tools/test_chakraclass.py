# CHAKRA-CLASS DESIGN TEST — 100% code, zero AI frames, 10s
import os, math, importlib.util, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
spec=importlib.util.spec_from_file_location("rl","/home/user/explainer-pipeline/tools/render_reel50.py")
rl=importlib.util.module_from_spec(spec); spec.loader.exec_module(rl)
m=rl.m; W,H=1080,1920; FPS=30; DUR=10.0; N=int(DUR*FPS)
ART=Image.open("/home/user/explainer-pipeline/assets/reel50/n7_galaxy_v.jpg").convert("RGB")
w0,h0=ART.size
U7,V7=0.635,0.315             # galaxy core (locked)
GLC=m.glow_sprite(60); GLB=m.glow_sprite(190)
def frame(i):
    t=i/FPS; pr=t/DUR; pe=pr*pr*(3-2*pr)
    z=1.04+0.10*pe; S=max(W/w0,H/h0)*z
    dxf=6.0*math.sin(t*0.5); dyf=4.0*math.sin(t*0.75+2.0)-40.0*pe
    left=(w0-W/S)/2+dxf/S; top=(h0-H/S)/2+dyf/S
    left=min(max(0.0,left),w0-W/S); top=min(max(0.0,top),h0-H/S)
    fr=ART.transform((W,H),Image.AFFINE,(1.0/S,0,left,0,1.0/S,top),resample=Image.BILINEAR).convert("RGBA")
    cx=int(round((U7*w0-left)*S)); cy=int(round((V7*h0-top)*S))
    # 1) galaxy differential swirl (locked 60/3.8)
    rl.swirl(fr,cx,cy,int(0.13*W),t,60,3.8)
    # 2) core glow pulse
    gg=GLB.copy(); gg.putalpha(gg.getchannel("A").point(lambda v:int(v*(0.5+0.35*math.sin(t*2*math.pi*0.33+1.0)))))
    fr.alpha_composite(gg,(cx-GLB.width//2,cy-GLB.height//2))
    # 3) ORBIT: 3 comets elliptical paths + fading trails (pure parametric = perfect smooth)
    d=ImageDraw.Draw(fr)
    for (rA,rB,sp,ph,tilt) in [(0.21,0.085,0.55,0.0,-0.30),(0.16,0.065,-0.72,2.1,-0.30),(0.26,0.105,0.40,4.2,-0.30)]:
        for k in range(16,-1,-1):
            tk=t-k*0.042
            a=sp*tk*2*math.pi*0.32+ph
            ex=rA*W*math.cos(a); ey=rB*W*math.sin(a)
            px=cx+ex*math.cos(tilt)-ey*math.sin(tilt); py=cy+ex*math.sin(tilt)+ey*math.cos(tilt)
            behind=math.sin(a)<0
            al=int((60 if behind else 255)*(1-k/17)**1.6)
            rr=(3.0 if behind else 5.2)*(1-k/20)
            if k==0 and not behind:
                gs=GLC.copy(); gs.putalpha(gs.getchannel("A").point(lambda v:int(v*1.0)))
                fr.alpha_composite(gs,(int(px)-GLC.width//2,int(py)-GLC.height//2))
            d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=(255,226,160,al))
            if k<3 and not behind:
                d.ellipse((px-rr*0.45,py-rr*0.45,px+rr*0.45,py+rr*0.45),fill=(255,255,240,al))
    # 4) rays + global life stack
    rr2=rl.RAYS.copy(); rr2.putalpha(rr2.getchannel("A").point(lambda v:int(v*0.5*(0.55+0.45*math.sin(t*0.45)))))
    fr.alpha_composite(rr2,(int(24*math.sin(t*0.2)),0))
    sx2=int((t*14)%1080); sy2=int((t*5)%1920)
    sl=m.smoke.crop((sx2,sy2,sx2+W,sy2+H))
    fr.alpha_composite(Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120),sl.point(lambda v:int(v*0.05))]))
    for (p0,p1,spd,ph2) in m.PART:
        py2=(p1-t*spd*0.045)%1.0; pxx=(p0+0.012*math.sin(t*1.3+ph2))%1.0
        a2=int(110*(0.4+0.6*math.sin(t*2+ph2)**2)); r2=2 if spd<0.8 else 3
        d.ellipse((pxx*W-r2,py2*H-r2,pxx*W+r2,py2*H+r2),fill=(255,214,140,a2))
    d.text((40,H-64),"CHAKRA-CLASS 100% CODE",font=m.MONO,fill=(255,255,255,70))
    d.text((W-150,H-64),"AI ART",font=m.MONO,fill=(255,255,255,118))
    fr.alpha_composite(m.VIGRGBA)
    g=np.asarray(fr.convert("RGB"),np.int16)
    g=np.clip(g+np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16),0,255).astype(np.uint8)
    out=Image.fromarray(g)
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    if t>DUR-0.6: out=ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.6))
    return out
if __name__=="__main__":
    for i in range(N):
        p=f"/var/tmp/cc/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=87)
        if i%60==0: print("fr",i,flush=True)
    print("DONE",N)
