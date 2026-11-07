#!/usr/bin/env python3
# SHUNYA-STYLE 10s TEST — awoken_yodha formula clone (micro-motion on AI stills)
# 1080x1920 @30fps, ~16.5s. Pure PIL+numpy. Frames -> /var/tmp/shunya/frames
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W,H,FPS = 1080,1920,30
DUR = 16.5; N = int(DUR*FPS)
A = "/home/user/explainer-pipeline/assets/shunya_test"
OUT = "/var/tmp/shunya/frames"; os.makedirs(OUT, exist_ok=True)
TIRO = ImageFont.truetype("/var/tmp/fonts/tiro.ttf", 56)
TIRO_S = ImageFont.truetype("/var/tmp/fonts/tiro.ttf", 42)
MONO = ImageFont.truetype("/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf", 22)
PAPER=(233,226,208); GOLD=(232,178,74)

# ---------- scenes: (img, t0, t1, zoom0, zoom1, panx, glow(cx,cy,r), spin) ----------
SC = [
 dict(img="s1_vishnu_garuda.jpg", t0=0.0,  t1=4.1,  z0=1.00, z1=1.035, px=-8, glow=(0.34,0.295,150), spin=None),
 dict(img="s2_chakra_hand.jpg",   t0=4.1,  t1=8.3,  z0=1.025, z1=1.00, px=7,  glow=(0.52,0.205,260), spin=None),
 dict(img="s3_mind_head.jpg",     t0=8.3,  t1=12.3, z0=1.00, z1=1.00, px=0, dy=0,  glow=(0.62,0.285,190), spin=None),
 dict(img="s4_mirror.jpg",        t0=12.3, t1=16.5, z0=1.00, z1=1.035, px=-6, glow=(0.46,0.25,150), spin=None),
]
XF = 0.8  # crossfade

CAPS = [
 (0.4,2.3,"विष्णु जी के हाथ में..."),
 (2.3,4.1,"ये चक्र देखा है?"),
 (4.1,5.2,"सुदर्शन।"),
 (5.2,8.1,"सु — शुभ  ·  दर्शन — देखना"),
 (8.3,10.1,"ये सिर्फ़ हथियार नहीं..."),
 (10.1,12.1,"ये आपका मन है।"),
 (12.3,13.9,"जो घूमता रहता है..."),
 (13.9,16.1,"जब तक आप उसे चलाना नहीं सीखते।"),
]

# ---------- preload + cover-scale ----------
def cover(im, scale=1.0):
    s = max(W/im.width, H/im.height)*scale
    return im.resize((int(im.width*s)+1, int(im.height*s)+1), Image.LANCZOS)
IMGS = {s['img']: Image.open(f"{A}/{s['img']}").convert("RGB") for s in SC}

# glow sprite (radial gold)
def glow_sprite(r):
    d = r*2
    y,x = np.mgrid[0:d,0:d]
    dist = np.sqrt((x-r)**2+(y-r)**2)/r
    a = np.clip(1-dist,0,1)**2.2
    sp = np.zeros((d,d,4),np.uint8)
    sp[...,0]=255; sp[...,1]=196; sp[...,2]=96
    sp[...,3]=(a*90).astype(np.uint8)
    return Image.fromarray(sp)
GLOWS = {s['img']: glow_sprite(s['glow'][2]) for s in SC}

# smoke layer: big blurred noise, tiled drift
rng = np.random.default_rng(7)
sm = rng.random((240,135))*255
smoke = Image.fromarray(sm.astype(np.uint8)).resize((2160,3840),Image.BILINEAR).filter(ImageFilter.GaussianBlur(60)).convert("L")

# particles
PART = [(random.random(), random.random(), 0.3+random.random()*0.9, random.random()*6.28) for _ in range(46)]

# vignette (static)
yy,xx = np.mgrid[0:H,0:W]
vd = np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.60))**2)
VIG = (np.clip(vd-0.55,0,1)*0.9*255).astype(np.uint8)
VIGIM = Image.fromarray(np.zeros((H,W),np.uint8)).convert("L"); VIGIM.putdata(VIG.flatten())
VIGRGBA = Image.merge("RGBA",[Image.new("L",(W,H),0)]*3+[VIGIM])

# italic caption renderer (shear)
_cap_cache = {}
def cap_img(txt, f):
    key=(txt,f.size)
    if key in _cap_cache: return _cap_cache[key]
    tmp = Image.new("RGBA",(W,160),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    tw = d.textlength(txt,font=f)
    # dark halo for readability on busy art
    halo = Image.new("RGBA",(W,160),(0,0,0,0)); hd=ImageDraw.Draw(halo)
    hd.text(((W-tw)/2,30), txt, font=f, fill=(0,0,0,255))
    halo = halo.filter(ImageFilter.GaussianBlur(9))
    tmp.alpha_composite(halo); tmp.alpha_composite(halo)
    d=ImageDraw.Draw(tmp); d.text(((W-tw)/2,30), txt, font=f, fill=PAPER+(255,))
    sh = tmp.transform((W,160), Image.AFFINE, (1,-0.10,14,0,1,0), resample=Image.BILINEAR)
    sh = sh.filter(ImageFilter.GaussianBlur(0.4))
    _cap_cache[key]=sh; return sh

def scene_frame(s, t):
    lt = t - s['t0']; sd = s['t1']-s['t0']; p = max(0,min(1,lt/sd))
    z = s['z0'] + (s['z1']-s['z0'])*p
    im = cover(IMGS[s['img']], z)
    ox = int((im.width-W)/2 + s['px']*math.sin(p*math.pi*0.9))
    oy = int((im.height-H)/2 - s.get('dy',12)*p)
    fr = im.crop((ox,oy,ox+W,oy+H)).convert("RGBA")
    # chakra spin (face-on): rotate circular crop
    if s['spin']:
        cx,cy,rr = s['spin']; cx=int(cx*W); cy=int(cy*H); r=int(rr*W)
        box=(cx-r,cy-r,cx+r,cy+r)
        disc = fr.crop(box).rotate(-(t*34)%360, resample=Image.BILINEAR)
        m = Image.new("L",(2*r,2*r),0); ImageDraw.Draw(m).ellipse((6,6,2*r-6,2*r-6),fill=255)
        m = m.filter(ImageFilter.GaussianBlur(7))
        fr.paste(disc, box, m)
    # glow pulse
    gx,gy,gr = s['glow']; g = GLOWS[s['img']]
    pulse = 0.60+0.40*math.sin(t*2*math.pi*0.4 + 1.1)
    gi = g.copy(); al = gi.getchannel("A").point(lambda v: int(v*pulse))
    gi.putalpha(al)
    fr.alpha_composite(gi,(int(gx*W)-g.width//2,int(gy*H)-g.height//2))
    # light rays (rotating wedges, additive-ish)
    ray = Image.new("RGBA",(W,H),(0,0,0,0)); rd=ImageDraw.Draw(ray)
    for k in range(2):
        ang = math.radians((t*2.5 + k*37) % 60 - 30)
        x0 = W*0.5 + math.tan(ang)*H
        rd.polygon([(W*0.5-70,-50),(W*0.5+70,-50),(x0+180,H),(x0-180,H)],fill=(255,208,120,10))
    fr.alpha_composite(ray.filter(ImageFilter.GaussianBlur(24)))
    # smoke drift (edges)
    sx = int((t*14) % 1080); sy = int((t*5) % 1920)
    sl = smoke.crop((sx,sy,sx+W,sy+H))
    smrgba = Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120), sl.point(lambda v:int(v*0.06))])
    fr.alpha_composite(smrgba)
    # particles
    pd = ImageDraw.Draw(fr)
    for (p0,p1,spd,ph) in PART:
        py = (p1 - t*spd*0.045) % 1.0
        pxx = (p0 + 0.012*math.sin(t*1.3+ph)) % 1.0
        al2 = int(110*(0.4+0.6*math.sin(t*2+ph)**2))
        r2 = 2 if spd<0.8 else 3
        pd.ellipse((pxx*W-r2,py*H-r2,pxx*W+r2,py*H+r2), fill=(255,214,140,al2))
    return fr

def frame(i):
    t = i/FPS
    # active scene(s) + crossfade
    cur = None; prev=None; mix=0
    for si,s in enumerate(SC):
        if s['t0'] <= t < s['t1']: cur=s; 
        if si>0 and SC[si]['t0']<=t<SC[si]['t0']+XF: prev=SC[si-1]; mix=1-(t-SC[si]['t0'])/XF
    if cur is None: cur=SC[-1]
    fr = scene_frame(cur, min(t,cur['t1']-0.001))
    if prev is not None and mix>0:
        fp = scene_frame(prev, min(t,prev['t1']-0.001))
        fr = Image.blend(fr, fp, mix)
    # caption
    for (c0,c1,txt) in CAPS:
        if c0<=t<c1:
            a = min(1,(t-c0)/0.25, (c1-t)/0.3)
            f = TIRO if len(txt)<22 else TIRO_S
            ci = cap_img(txt,f)
            al = ci.getchannel("A").point(lambda v:int(v*max(0,a)))
            c2 = ci.copy(); c2.putalpha(al)
            # soft shadow behind text
            fr.alpha_composite(c2,(0,int(H*0.630)))
            break
    # AI ART tag + mark
    d = ImageDraw.Draw(fr)
    d.text((W-150, H-64), "AI ART", font=MONO, fill=(255,255,255,118))
    d.text((40, H-64), "CHRONIC OF HISTORIC", font=MONO, fill=(255,255,255,60))
    fr.alpha_composite(VIGRGBA)
    # grain
    g = np.asarray(fr.convert("RGB"), np.int16)
    noise = np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16)
    g = np.clip(g+noise,0,255).astype(np.uint8)
    out = Image.fromarray(g)
    # ending fade
    if t>DUR-0.6: out = ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.6))
    if t<0.2: out = ImageEnhance.Brightness(out).enhance(t/0.2)
    return out

if __name__=="__main__":
    import sys
    done=0
    for i in range(N):
        p=f"{OUT}/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p, quality=87)
        done+=1
        if done%100==0: print("fr",i,flush=True)
    print("FRAMES DONE",N)
