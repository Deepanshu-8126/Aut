#!/usr/bin/env python3
# ANIMATION PROOF — element-layer animation (spin + flames + ray flicker + crescendo)
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W,H,FPS=1080,1920,30; DUR=10.0; N=int(DUR*FPS)
A="/home/user/explainer-pipeline/assets/anim_test"
OUT="/var/tmp/anim/frames"; os.makedirs(OUT,exist_ok=True)
TIRO=ImageFont.truetype("/var/tmp/fonts/tiro.ttf",54)
MONO=ImageFont.truetype("/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf",22)
PAPER=(233,226,208)

bg=Image.open(f"{A}/bg_plate.jpg").convert("RGB")
s=max(W/bg.width,H/bg.height); bg=bg.resize((int(bg.width*s)+1,int(bg.height*s)+1),Image.LANCZOS)
BG=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).convert("RGBA")

wh=Image.open(f"{A}/wheel_faceon.jpg").convert("RGB")
wh=ImageEnhance.Brightness(wh).enhance(1.12)
wh=ImageEnhance.Color(wh).enhance(0.88)
L=np.asarray(wh.convert("L"))
mk=Image.fromarray(((L>16)*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(2))
WHEEL=wh.convert("RGBA"); WHEEL.putalpha(mk)

# procedural flame ring (polar streaks), 1024px
def flame_ring(seed, r0, r1, col):
    S=1024; yy,xx=np.mgrid[0:S,0:S]
    cx=cy=S/2
    r=np.sqrt((xx-cx)**2+(yy-cy)**2)/(S/2)
    th=np.arctan2(yy-cy,xx-cx)
    rng=np.random.default_rng(seed)
    ph=rng.random(5)*6.28; k=[7,13,19,29,37]
    streak=np.zeros_like(th)
    for p,kk in zip(ph,k): streak+=np.sin(th*kk+p)
    streak=(streak/5*0.5+0.5)**2.2
    band=np.clip(1-np.abs((r-(r0+r1)/2)/((r1-r0)/2)),0,1)**1.5
    a=(streak*band*210).astype(np.uint8)
    im=np.zeros((S,S,4),np.uint8)
    im[...,0]=col[0]; im[...,1]=col[1]; im[...,2]=col[2]; im[...,3]=a
    return Image.fromarray(im).filter(ImageFilter.GaussianBlur(3))
F1=flame_ring(3,0.78,1.00,(255,170,60))
F2=flame_ring(9,0.70,0.94,(255,120,40))

CX,CY=int(0.50*W),int(0.21*H); SPAN=int(0.62*W); SQ=0.50; TILT=-16
def xform(img,ang,scale=1.0):
    r=img.rotate(ang,resample=Image.BILINEAR)
    w2=int(SPAN*scale); r=r.resize((w2,int(w2*SQ)),Image.BILINEAR)
    return r.rotate(TILT,expand=True,resample=Image.BILINEAR)

rng=np.random.default_rng(7)
smoke=Image.fromarray((rng.random((240,135))*255).astype(np.uint8)).resize((2160,3840),Image.BILINEAR).filter(ImageFilter.GaussianBlur(60)).convert("L")
PART=[(random.random(),random.random(),0.3+random.random()*0.9,random.random()*6.28) for _ in range(46)]
yy,xx=np.mgrid[0:H,0:W]
vd=np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.60))**2)
VIG=Image.merge("RGBA",[Image.new("L",(W,H),0)]*3+[Image.fromarray((np.clip(vd-0.55,0,1)*0.9*255).astype(np.uint8))])

CAPS=[(0.4,4.9,"ये चक्र कभी रुकता नहीं..."),(5.1,9.6,"ना बाहर — ना भीतर।")]
_cc={}
def cap(txt):
    if txt in _cc: return _cc[txt]
    tmp=Image.new("RGBA",(W,170),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    tw=d.textlength(txt,font=TIRO)
    halo=Image.new("RGBA",(W,170),(0,0,0,0)); hd=ImageDraw.Draw(halo)
    hd.text(((W-tw)/2,34),txt,font=TIRO,fill=(0,0,0,255))
    halo=halo.filter(ImageFilter.GaussianBlur(9))
    tmp.alpha_composite(halo); tmp.alpha_composite(halo)
    d=ImageDraw.Draw(tmp); d.text(((W-tw)/2,34),txt,font=TIRO,fill=PAPER+(255,))
    sh=tmp.transform((W,170),Image.AFFINE,(1,-0.10,15,0,1,0),resample=Image.BILINEAR)
    _cc[txt]=sh; return sh

def flick(t,a,b,c): return 0.72+0.28*(0.5*math.sin(t*a+c)+0.3*math.sin(t*b+c*2)+0.2*math.sin(t*a*1.7+c*3))

for i in range(N):
    p=f"{OUT}/{i:05d}.jpg"
    if os.path.exists(p): continue
    t=i/FPS
    cres=1.0+0.65*max(0,(t-7.0)/3.0)          # last-3s crescendo
    fr=BG.copy()
    # flames (counter-rotating, flickering) behind wheel
    for F,sp,base_a in ((F1,-95,0.85),(F2,70,0.7)):
        fl=xform(F,(t*sp)%360,1.18)
        aa=fl.getchannel("A").point(lambda v:int(min(255,v*base_a*flick(t,5.1,8.3,sp)*cres)))
        fl.putalpha(aa)
        fr.alpha_composite(fl,(CX-fl.width//2,CY-fl.height//2))
    # wheel spin
    r=xform(WHEEL,(t*34)%360,1.0)
    glow=r.filter(ImageFilter.GaussianBlur(22))
    ga=glow.getchannel("A").point(lambda v:int(min(255,v*0.8*cres)))
    glow.putalpha(ga)
    fr.alpha_composite(glow,(CX-glow.width//2,CY-glow.height//2))
    fr.alpha_composite(r,(CX-r.width//2,CY-r.height//2))
    # flickering rays (static geometry, opacity jitter)
    ray=Image.new("RGBA",(W,H),(0,0,0,0)); rd=ImageDraw.Draw(ray)
    for k,(dx0,dx1) in enumerate([(-260,-90),(-40,40),(100,270)]):
        a=int(26*flick(t,7.3+k,11.1,k*2.3)*cres)
        rd.polygon([(CX+dx0*0.25,CY),(CX+dx1*0.25,CY),(CX+dx1,0),(CX+dx0,0)],fill=(255,208,120,a))
    fr.alpha_composite(ray.filter(ImageFilter.GaussianBlur(18)))
    # smoke + particles
    sx=int((t*14)%1080); sy=int((t*5)%1920)
    sl=smoke.crop((sx,sy,sx+W,sy+H))
    fr.alpha_composite(Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120),sl.point(lambda v:int(v*0.06))]))
    pd=ImageDraw.Draw(fr)
    for (p0,p1,spd,ph) in PART:
        py=(p1-t*spd*0.045)%1.0; pxx=(p0+0.012*math.sin(t*1.3+ph))%1.0
        a2=int(110*(0.4+0.6*math.sin(t*2+ph)**2)); r2=2 if spd<0.8 else 3
        pd.ellipse((pxx*W-r2,py*H-r2,pxx*W+r2,py*H+r2),fill=(255,214,140,a2))
    # captions INSTANT swap
    for (c0,c1,txt) in CAPS:
        if c0<=t<c1: fr.alpha_composite(cap(txt),(0,int(H*0.665))); break
    d=ImageDraw.Draw(fr)
    d.text((W-150,H-64),"AI ART",font=MONO,fill=(255,255,255,118))
    d.text((40,H-64),"CHRONIC OF HISTORIC",font=MONO,fill=(255,255,255,60))
    fr.alpha_composite(VIG)
    g=np.asarray(fr.convert("RGB"),np.int16)
    g=np.clip(g+np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16),0,255).astype(np.uint8)
    out=Image.fromarray(g)
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    if t>DUR-0.5: out=ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.5))
    out.save(p,quality=87)
    if i%60==0: print("fr",i,flush=True)
print("DONE",N)
