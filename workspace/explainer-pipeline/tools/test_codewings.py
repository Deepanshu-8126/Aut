import os, math, importlib.util, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
spec=importlib.util.spec_from_file_location("rl","/home/user/explainer-pipeline/tools/render_reel50.py")
rl=importlib.util.module_from_spec(spec); spec.loader.exec_module(rl)
m=rl.m; W,H=1080,1920; FPS=30; DUR=8.0; N=int(DUR*FPS)
ART=Image.open("/home/user/explainer-pipeline/assets/shunya38/s1_vivid.jpg").convert("RGB")
w0,h0=ART.size
SRC=np.asarray(ART,np.float32)
# ---- FLAP-WARP field (precompute once) ----
Xg,Yg=np.meshgrid(np.arange(w0,dtype=np.float32),np.arange(h0,dtype=np.float32))
DX=np.zeros((h0,w0),np.float32); DY=np.zeros((h0,w0),np.float32); PH=np.zeros((h0,w0),np.float32)
def smoothwin(u,lo,hi,edge):
    a=np.clip((u-lo)/edge,0,1); b=np.clip((hi-u)/edge,0,1)
    return (a*a*(3-2*a))*(b*b*(3-2*b))
def add_wing(px0,px1,py0,py1,rootx,rooty,tipx,tipy,ddx,ddy,A,ph0):
    global DX,DY,PH
    x0,x1,y0,y1=px0*w0,px1*w0,py0*h0,py1*h0
    rx,ry,tx,ty=rootx*w0,rooty*h0,tipx*w0,tipy*h0
    ax,ay=tx-rx,ty-ry; L=math.hypot(ax,ay); ax,ay=ax/L,ay/L
    s=np.clip(((Xg-rx)*ax+(Yg-ry)*ay)/L,0,1)**1.7
    win=smoothwin(Xg,x0,x1,(x1-x0)*0.14)*smoothwin(Yg,y0,y1,(y1-y0)*0.14)
    amp=A*s*win
    nn=math.hypot(ddx,ddy); ddx,ddy=ddx/nn,ddy/nn
    DX+=amp*ddx; DY+=amp*ddy
    PH=np.where(amp>0.05, 2.4*np.clip(((Xg-rx)*ax+(Yg-ry)*ay)/L,0,1)+ph0, PH)
# === TRAINED from LTX optical flow (2026-10-22): flap 0.27Hz, sweep 2x, clouds alive ===
# left bada wing (root 0.46,0.43 -> tip 0.08,0.92)
add_wing(0.00,0.50,0.26,0.97, 0.46,0.43, 0.08,0.92, 0.18,0.98, 9.0, 0.0)
# right upar wing (root 0.57,0.34 -> tip 0.97,0.06)
add_wing(0.50,1.00,0.02,0.37, 0.57,0.34, 0.97,0.06, -0.10,0.99, 7.0, 0.9)
# Vishnu ji ka dupatta
add_wing(0.10,0.42,0.20,0.44, 0.38,0.26, 0.14,0.36, 0.08,0.99, 3.5, 1.7)
# PAAS ke badal (neeche) — LTX 1.55px/fr churn; horizontal drift-lehar
add_wing(0.00,1.00,0.72,1.00, 0.10,0.98, 0.95,0.86, 0.97,0.24, 20.0, 3.0)
# door ke badal (upar) — parallax: bas saans (LTX 0.05 = approx still)
add_wing(0.55,1.00,0.38,0.62, 0.98,0.50, 0.60,0.44, 0.90,0.40, 1.2, 4.5)
AMP=np.sqrt(DX*DX+DY*DY); WMASK=(AMP/max(1e-6,float(AMP.max()))).astype(np.float32)
TIP=np.clip((WMASK-0.45)/0.55,0,1).astype(np.float32)   # sirf tip zone
XI=Xg.astype(np.int32); YI=Yg.astype(np.int32)
def warp_art(t):
    th=2*math.pi*0.85*t-PH
    osc=(np.sin(th)+0.28*np.sin(2*th+0.6)).astype(np.float32)      # downstroke tez, upstroke dheemi
    osc=osc+(0.16*TIP*np.sin(2*math.pi*2.6*t-2.0*PH)).astype(np.float32)  # tip feather flutter
    sx=np.clip(Xg-DX*osc,0,w0-2); sy=np.clip(Yg-DY*osc,0,h0-2)
    x0=sx.astype(np.int32); y0=sy.astype(np.int32)
    fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
    out=(SRC[y0,x0]*(1-fx)*(1-fy)+SRC[y0,x0+1]*fx*(1-fy)+SRC[y0+1,x0]*(1-fx)*fy+SRC[y0+1,x0+1]*fx*fy)
    # flap ke saath pankh pe roshni ka pulse (3D shading feel)
    lite=(1.0+0.05*WMASK*math.sin(2*math.pi*0.85*t-1.0))[...,None]
    out=np.clip(out*lite,0,255)
    return Image.fromarray(out.astype(np.uint8))
def frame(i):
    t=i/FPS
    art=warp_art(t)
    pr=t/DUR; pe=pr*pr*(3-2*pr)
    z=1.05+0.06*pe; S=max(W/w0,H/h0)*z
    dxf=6.0*math.sin(t*0.55); dyf=4.0*math.sin(t*0.8+2.0)+3.5*math.sin(2*math.pi*0.85*t+math.pi)
    left=(w0-W/S)/2+dxf/S; top=(h0-H/S)/2+dyf/S
    left=min(max(0.0,left),w0-W/S); top=min(max(0.0,top),h0-H/S)
    fr=art.transform((W,H),Image.AFFINE,(1.0/S,0,left,0,1.0/S,top),resample=Image.BILINEAR).convert("RGBA")
    # badal turbulence (LTX-jaisa local churn)
    for (fx3,fy3,fr3,ax3,fq3,ph3) in [(0.20,0.84,0.12,6,0.09,0.3),(0.55,0.90,0.13,6,0.08,2.1),(0.85,0.80,0.11,5,0.09,4.0)]:
        m._tpatch(fr,t,fx3,fy3,fr3,ax3,fq3,ph3)
    # halo chakra swirl (Vishnu ki ungli ke upar)
    rl.swirl(fr,int(round((0.375*w0-left)*S)),int(round((0.115*h0-top)*S)),int(0.075*W),t,70,2.2)
    # rays from top-right sun
    rr2=rl.RAYS.transpose(Image.FLIP_LEFT_RIGHT).copy()
    a=0.6*(0.55+0.45*math.sin(t*0.45))
    rr2.putalpha(rr2.getchannel("A").point(lambda v:int(v*a)))
    fr.alpha_composite(rr2,(int(20*math.sin(t*0.22)),0))
    # global smoke+particles+vignette (locked layers)
    sx2=int((t*14)%1080); sy2=int((t*5)%1920)
    sl=m.smoke.crop((sx2,sy2,sx2+W,sy2+H))
    fr.alpha_composite(Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120),sl.point(lambda v:int(v*0.05))]))
    pd=ImageDraw.Draw(fr)
    for (p0,p1,spd,ph2) in m.PART:
        py=(p1-t*spd*0.045)%1.0; pxx=(p0+0.012*math.sin(t*1.3+ph2))%1.0
        a2=int(110*(0.4+0.6*math.sin(t*2+ph2)**2)); r2=2 if spd<0.8 else 3
        pd.ellipse((pxx*W-r2,py*H-r2,pxx*W+r2,py*H+r2),fill=(255,214,140,a2))
    pd.text((40,H-64),"CODE-WINGS TEST",font=m.MONO,fill=(255,255,255,70))
    pd.text((W-150,H-64),"AI ART",font=m.MONO,fill=(255,255,255,118))
    fr.alpha_composite(m.VIGRGBA)
    g=np.asarray(fr.convert("RGB"),np.int16)
    g=np.clip(g+np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16),0,255).astype(np.uint8)
    out=Image.fromarray(g)
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    if t>DUR-0.6: out=ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.6))
    return out
if __name__=="__main__":
    for i in range(N):
        p=f"/var/tmp/wings/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=87)
        if i%60==0: print("fr",i,flush=True)
    print("DONE",N)
