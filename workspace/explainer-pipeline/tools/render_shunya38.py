#!/usr/bin/env python3
# VIDEO 38 "घूमता चक्र" — MODE SHUNYA full (~104.5s) — original script/scenes
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W,H,FPS = 1080,1920,30
DUR = 104.5; N = int(DUR*FPS)
A38="/home/user/explainer-pipeline/assets/shunya38"
AT ="/home/user/explainer-pipeline/assets/shunya_test"
OUT="/var/tmp/sh38/frames"; os.makedirs(OUT,exist_ok=True)
TIRO   = ImageFont.truetype("/var/tmp/fonts/tiro.ttf", 54)
TIRO_S = ImageFont.truetype("/var/tmp/fonts/tiro.ttf", 42)
TITLE  = ImageFont.truetype("/home/user/explainer-pipeline/assets/fonts/NotoSansDevanagari-Black.ttf", 128)
SUBT   = ImageFont.truetype("/var/tmp/fonts/tiro.ttf", 46)
MONO   = ImageFont.truetype("/home/user/explainer-pipeline/assets/fonts/JetBrainsMono-Bold.ttf", 22)
SUBF   = ImageFont.truetype("/home/user/explainer-pipeline/assets/fonts/Inter-Black.ttf", 44)
PAPER=(233,226,208); GOLD=(232,178,74)

SHOTS=[ # img_path, t0,t1, z0,z1,px,dy, glow(cx,cy,r)
 (f"{A38}/s1_vivid.jpg", 0.00,  5.50, 1.00,1.030,-8,12,(0.40,0.135,150)),
 (f"{A38}/n2_murti.jpg",        5.50, 10.95, 1.025,1.00,  6,12,(0.63,0.09,120)),
 (f"{A38}/n3_granth.jpg",      10.95, 18.20, 1.00,1.030, -7,12,(0.40,0.52,150)),
 (f"/home/user/explainer-pipeline/assets/anim_test/bg_plate.jpg",  18.20, 25.41, 1.00,1.00,  0, 0,(0.52,0.205,260)),
 (f"{A38}/n5_arc.jpg",         25.41, 32.00, 1.00,1.030, -8,12,(0.55,0.38,160)),
 (f"{A38}/n6_return.jpg",      32.00, 38.31, 1.025,1.00,  6,12,(0.52,0.41,140)),
 (f"{A38}/n7_rishi.jpg",       38.31, 45.30, 1.00,1.030, -6,12,(0.50,0.57,130)),
 (f"{AT}/s3_mind_head.jpg",    45.30, 52.21, 1.00,1.00,   0, 0,(0.62,0.285,190)),
 (f"{A38}/n9_storm.jpg",       52.21, 58.80, 1.00,1.030,  7,12,(0.60,0.45,150)),
 (f"{A38}/n10_lake.jpg",       58.80, 65.27, 1.025,1.00, -6,12,(0.46,0.22,150)),
 (f"{AT}/s4_mirror.jpg",       65.27, 73.50, 1.00,1.030, -6,12,(0.46,0.25,150)),
 (f"{A38}/n12_river.jpg",      73.50, 82.05, 1.025,1.00,  6,12,(0.55,0.52,110)),
 (f"{A38}/n13_finger.jpg",     82.05, 93.19, 1.00,1.040,  6,12,(0.52,0.26,170)),
 (f"{A38}/n14_cta.jpg",        93.19,104.50, 1.00,1.025, -5,12,(0.50,0.10,200)),
]
XF=0.8

# segment windows (VO start,end) + clause lists
SEGS=[
 (0.50,10.15, ["हर मूर्ति में एक चीज़ कभी नहीं बदलती...","विष्णु जी की उँगली पर घूमता चक्र।","हज़ारों साल से घूम रहा है... कभी रुका नहीं।","क्यों?"]),
 (10.95,24.61,["पुराण कहते हैं — इसका नाम सुदर्शन है।","दो शब्द...","सु — यानी शुभ। दर्शन — यानी देखना।","सोचिए... संसार के सबसे बड़े अस्त्र का नाम...","\"सही देखना\" है।"]),
 (25.41,37.51,["और एक बात इसे हर अस्त्र से अलग करती है।","तीर फेंका... तो गया।","पर ये चक्र... काम पूरा करके वापस लौट आता है।","जिसने छोड़ा... उसी के पास।"]),
 (38.31,51.41,["ऋषियों ने इसमें एक गहरा इशारा देखा।","ये पहिया बाहर नहीं... भीतर घूमता है।","आपका मन — दिन-रात चलता हुआ... बिना रुके...","बिल्कुल इसी चक्र की तरह।"]),
 (52.21,64.47,["अब फ़र्क़ सिर्फ़ इतना है।","बेक़ाबू मन... वही चक्र है जो अपने ही घर में तूफ़ान मचाता है।","और सधा हुआ मन... वही चक्र —","जो हर उलझन को काट देता है।"]),
 (65.27,81.25,["तो साधते कैसे हैं?","पुरानी विधि एक ही है — देखना।","आँख बंद कीजिए... और अपनी ही सोच को ऐसे देखिए,","जैसे किनारे पर बैठकर नदी को।","जो सोच देखी जाती है... वो धीमी पड़ जाती है।"]),
 (82.05,92.39,["इसीलिए सुदर्शन सिर्फ़ हथियार नहीं... एक कला है।","शुभ देखने की कला।","और ये चक्र... आपकी उँगली पर भी घूम रहा है।"]),
 (93.19,101.76,["अगर ये बात भीतर तक पहुँची...","तो कमेंट में लिखिए — \"शुभ दर्शन\"।","और ऐसे ही रहस्यों के लिए... जुड़े रहिए।"]),
]
CAPS=[]
for (s0,s1,cls) in SEGS:
    tot=sum(len(c) for c in cls); acc=s0
    for c in cls:
        d=(s1-s0)*len(c)/tot
        CAPS.append((acc,acc+d,c)); acc+=d

FDIR="/home/user/explainer-pipeline/assets/fonts"
TEKO_B=ImageFont.truetype(f"{FDIR}/Teko.ttf",128); TEKO_B.set_variation_by_name("Bold")
TEKO_M=ImageFont.truetype(f"{FDIR}/Teko.ttf",100); TEKO_M.set_variation_by_name("Bold")
TIRO_W=ImageFont.truetype(f"{FDIR}/TiroDevanagariHindi-Regular.ttf",46)
YEL=(255,221,0); WHT=(246,243,235)
def _mkwp():
    out=[]
    spec=[(0,[[("हर",0,WHT),("मूर्ति",0,WHT),("में",0,WHT)],
              [("एक",1,YEL),("चीज़",1,YEL)],
              [("कभी",2,YEL),("नहीं",2,YEL),("बदलती...",2,WHT)]]),
          (1,[[("विष्णु",0,WHT),("जी",0,WHT),("की",0,WHT),("उँगली",0,WHT),("पर",0,WHT)],
              [("घूमता",1,YEL),("चक्र",1,WHT)]])]
    for ci,lines in spec:
        a0,b0,_=CAPS[ci]
        tot=sum(len(w) for ln in lines for (w,f,c) in ln)
        acc=a0; times=[]
        for ln in lines:
            for (w,f,c) in ln:
                times.append(acc); acc+=(b0-a0)*len(w)/tot
        out.append((a0,b0,lines,times))
    return out
WP=_mkwp()
def draw_wordpop(fr,t,lines,times,y0=None):
    dd=ImageDraw.Draw(fr)
    FM={0:TIRO_W,1:TEKO_B,2:TEKO_M}; SW={0:3,1:7,2:5}; LH={0:80,1:160,2:126}
    y=int(H*0.555) if y0 is None else int(y0); k=0
    for ln in lines:
        vis=[]
        for (w,f,c) in ln:
            if t>=times[k]: vis.append((w,f,c))
            k+=1
        if vis:
            fnt=FM[vis[0][1]]; sww=SW[vis[0][1]]; gap=18 if vis[0][1]==0 else 28
            ww=[dd.textlength(w,font=fnt) for (w,_,_) in vis]
            totw=sum(ww)+gap*(len(vis)-1)
            x=(W-totw)/2
            for (wd,tg,col),wl in zip(vis,ww):
                if tg>0: dd.text((x+5,y+6),wd,font=fnt,fill=(0,0,0,160),stroke_width=sww,stroke_fill=(0,0,0,160))
                dd.text((x,y),wd,font=fnt,fill=col+(255,),stroke_width=sww,stroke_fill=(12,10,5,255))
                x+=wl+gap
        y+=LH[ln[0][1]]
def write_srt(path):
    def ts(t):
        hh=int(t//3600); mm=int(t%3600//60); ss=int(t%60); ms=int((t%1)*1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"
    with open(path,"w") as f:
        for i,(a,b,c) in enumerate(CAPS,1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")

IMGS={p:Image.open(p).convert("RGB") for (p,*_) in [ (s[0],) for s in SHOTS ]}
def cover(im,scale):
    s=max(W/im.width,H/im.height)*scale
    return im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)

def glow_sprite(r):
    d=r*2; y,x=np.mgrid[0:d,0:d]
    a=np.clip(1-np.sqrt((x-r)**2+(y-r)**2)/r,0,1)**2.2
    sp=np.zeros((d,d,4),np.uint8); sp[...,0]=255; sp[...,1]=196; sp[...,2]=96
    sp[...,3]=(a*90).astype(np.uint8)
    return Image.fromarray(sp)
GL={s[0]:glow_sprite(s[7][2]) for s in SHOTS}

# ===== v2 FX ENGINE =====
AN="/home/user/explainer-pipeline/assets/anim_test"
_wh=Image.open(f"{AN}/wheel_faceon.jpg").convert("RGB")
_wh=ImageEnhance.Brightness(_wh).enhance(1.12); _wh=ImageEnhance.Color(_wh).enhance(0.88)
_L=np.asarray(_wh.convert("L"))
_mk=Image.fromarray(((_L>16)*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(2))
WHEEL=_wh.convert("RGBA"); WHEEL.putalpha(_mk)
def _flame(seed,r0,r1,col):
    S=1024; yy2,xx2=np.mgrid[0:S,0:S]; c=S/2
    r=np.sqrt((xx2-c)**2+(yy2-c)**2)/(S/2); th=np.arctan2(yy2-c,xx2-c)
    rg=np.random.default_rng(seed); ph=rg.random(5)*6.28
    st=np.zeros_like(th)
    for pph,kk in zip(ph,[7,13,19,29,37]): st+=np.sin(th*kk+pph)
    st=(st/5*0.5+0.5)**2.2
    band=np.clip(1-np.abs((r-(r0+r1)/2)/((r1-r0)/2)),0,1)**1.5
    im=np.zeros((S,S,4),np.uint8); im[...,0]=col[0]; im[...,1]=col[1]; im[...,2]=col[2]
    im[...,3]=(st*band*210).astype(np.uint8)
    return Image.fromarray(im).filter(ImageFilter.GaussianBlur(3))
F1=_flame(3,0.78,1.00,(255,170,60)); F2=_flame(9,0.70,0.94,(255,120,40))
WCX,WCY=int(0.50*W),int(0.21*H); WSPAN=int(0.62*W); WSQ=0.50; WTILT=-16
def xformW(img,ang,scale=1.0):
    r=img.rotate(ang,resample=Image.BILINEAR)
    w2=int(WSPAN*scale); r=r.resize((w2,int(w2*WSQ)),Image.BILINEAR)
    return r.rotate(WTILT,expand=True,resample=Image.BILINEAR)
def flick(t,a,b,c): return 0.72+0.28*(0.5*math.sin(t*a+c)+0.3*math.sin(t*b+c*2)+0.2*math.sin(t*a*1.7+c*3))
ROTP={f"{A38}/n13_finger.jpg":(0.52,0.26,0.17,12.0,None),
      f"{A38}/n9_storm.jpg":(0.60,0.45,0.11,None,(4.0,0.15)),
      f"{A38}/n14_cta.jpg":(0.50,0.105,0.22,7.0,None)}
# ---- v3: s1 wing-flap + chakra vortex ----
def _wingmask(w,h,pvx,pvy,r0,excl,efr=38.0):
    yy,xx=np.mgrid[0:h,0:w]
    d=np.sqrt((xx-pvx)**2+(yy-pvy)**2)
    a=np.clip((d-r0)/130.0,0,1)
    ef=np.minimum.reduce([xx/38.0,yy/38.0,(w-1-xx)/efr,(h-1-yy)/38.0])
    a*=np.clip(ef,0,1)
    for (ex,ey,er) in excl:
        dh=np.sqrt((xx-ex)**2+(yy-ey)**2)
        a*=np.clip((dh-er)/60.0,0,1)
    return Image.fromarray((a*235).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
WINGS=[]
for (fx0,fy0,fx1,fy1),(fpx,fpy),sgn,phz,excl in [
    ((0.00,0.26,0.50,0.74),(0.47,0.53),-1.0,0.0,[(0.52,0.47,0.09)]),
    ((0.55,0.00,1.00,0.40),(0.655,0.385),1.0,0.45,[(0.80,0.44,0.10)])]:
    bx0,by0,bx1,by1=int(fx0*W),int(fy0*H),int(fx1*W),int(fy1*H)
    pvx,pvy=int(fpx*W)-bx0,int(fpy*H)-by0
    exl=[(int(a0*W)-bx0,int(b0*H)-by0,int(c0*W)) for (a0,b0,c0) in excl]
    WINGS.append((((bx0,by0,bx1,by1)),(pvx,pvy),sgn,phz,_wingmask(bx1-bx0,by1-by0,pvx,pvy,55,exl,130.0 if fx1>0.99 else 38.0)))
WINGS2=[]
for (fx0,fy0,fx1,fy1),(fpx,fpy),sgn,phz,excl,efr in [
    ((0.00,0.30,0.40,0.72),(0.26,0.48),-1.0,0.0,[],38.0),
    ((0.62,0.00,1.00,0.34),(0.80,0.22),1.0,0.45,[],130.0),
    ((0.20,0.52,0.80,1.00),(0.58,0.56),-0.5,0.8,[(0.52,0.58,0.07)],38.0)]:
    bx0,by0,bx1,by1=int(fx0*W),int(fy0*H),int(fx1*W),int(fy1*H)
    pvx,pvy=int(fpx*W)-bx0,int(fpy*H)-by0
    exl=[(int(a0*W)-bx0,int(b0*H)-by0,int(c0*W)) for (a0,b0,c0) in excl]
    WINGS2.append((((bx0,by0,bx1,by1)),(pvx,pvy),sgn,phz,_wingmask(bx1-bx0,by1-by0,pvx,pvy,40,exl,efr)))
VORT=_flame(17,0.26,0.95,(255,195,95)).resize((250,250),Image.BILINEAR)
VORT2=_flame(23,0.18,0.98,(255,180,70)).resize((720,720),Image.BILINEAR)
# ===== end FX =====


rng=np.random.default_rng(7)
smoke=Image.fromarray((rng.random((240,135))*255).astype(np.uint8)).resize((2160,3840),Image.BILINEAR).filter(ImageFilter.GaussianBlur(60)).convert("L")
PART=[(random.random(),random.random(),0.3+random.random()*0.9,random.random()*6.28) for _ in range(46)]
yy,xx=np.mgrid[0:H,0:W]
vd=np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.60))**2)
VIGIM=Image.fromarray((np.clip(vd-0.55,0,1)*0.9*255).astype(np.uint8))
VIGRGBA=Image.merge("RGBA",[Image.new("L",(W,H),0)]*3+[VIGIM])

# papercut logo card
LOGO=Image.open("/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png").convert("RGBA")
LOGO.thumbnail((520,520))
CARD=Image.new("RGBA",(600,600),(0,0,0,0))
cd=ImageDraw.Draw(CARD)
cd.rounded_rectangle((8,8,592,592),18,fill=(238,233,220,255))
CARD.alpha_composite(LOGO,((600-LOGO.width)//2,(600-LOGO.height)//2))
CARD=CARD.rotate(-3,expand=True,resample=Image.BICUBIC)
SHAD=Image.new("RGBA",CARD.size,(0,0,0,0))
sd=ImageDraw.Draw(SHAD); sd.rounded_rectangle((16,20,CARD.width-4,CARD.height-2),22,fill=(0,0,0,130))
SHAD=SHAD.filter(ImageFilter.GaussianBlur(16))

_cc={}
def cap_img(txt,f):
    k=(txt,f.size)
    if k in _cc: return _cc[k]
    tmp=Image.new("RGBA",(W,170),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    tw=d.textlength(txt,font=f)
    halo=Image.new("RGBA",(W,170),(0,0,0,0)); hd=ImageDraw.Draw(halo)
    hd.text(((W-tw)/2,34),txt,font=f,fill=(0,0,0,255))
    halo=halo.filter(ImageFilter.GaussianBlur(9))
    tmp.alpha_composite(halo); tmp.alpha_composite(halo)
    d=ImageDraw.Draw(tmp); d.text(((W-tw)/2,34),txt,font=f,fill=PAPER+(255,))
    sh=tmp.transform((W,170),Image.AFFINE,(1,-0.10,15,0,1,0),resample=Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.4))
    _cc[k]=sh; return sh

def _mpad(big,l,t,r,b):
    if l==0 and t==0 and r==0 and b==0: return big
    arr=np.asarray(big)
    arr=np.pad(arr,((t,b),(l,r),(0,0)),mode='edge')
    return Image.fromarray(arr)
def qt(t,r=12.0): return math.floor(t*r)/r
def flapw(tq,f,ph):
    x=2*math.pi*((tq*f)+ph)
    return math.sin(x-0.55*math.sin(x))
def warp_wing(imRGBA,box,pv,msk,t,sgn,phz,amax):
    PAD=150
    x0,y0,x1,y1=box
    dx0,dy0,dx1,dy1=x0-PAD,y0-PAD,x1+PAD,y1+PAD
    ex0,ey0=max(0,dx0),max(0,dy0); ex1,ey1=min(imRGBA.width,dx1),min(imRGBA.height,dy1)
    big=np.asarray(_mpad(imRGBA.crop((ex0,ey0,ex1,ey1)),ex0-dx0,ey0-dy0,dx1-ex1,dy1-ey1),dtype=np.float32)
    hh,ww=big.shape[:2]
    pvx,pvy=pv[0]+PAD,pv[1]+PAD
    yy,xx=np.mgrid[0:hh,0:ww].astype(np.float32)
    rx=xx-pvx; ry=yy-pvy
    r=np.sqrt(rx*rx+ry*ry)+1e-3
    rmax=0.9*max(hh,ww)
    rn=np.clip(r/rmax,0,1)
    A=math.radians(amax)*flapw(t,0.75,phz*0.159)*sgn
    th=A*(0.22+0.78*rn**1.35)+math.radians(1.2)*np.sin(r/95.0-2*math.pi*1.1*t+phz)*rn
    cs=np.cos(th); sn=np.sin(th)
    sx=np.clip(pvx+rx*cs+ry*sn,0,ww-1); sy=np.clip(pvy-rx*sn+ry*cs,0,hh-1)
    xi=sx.astype(np.int32); yi=sy.astype(np.int32)
    xj=np.minimum(xi+1,ww-1); yj=np.minimum(yi+1,hh-1)
    fx=(sx-xi)[...,None]; fy=(sy-yi)[...,None]
    out=big[yi,xi]*(1-fx)*(1-fy)+big[yi,xj]*fx*(1-fy)+big[yj,xi]*(1-fx)*fy+big[yj,xj]*fx*fy
    pt=Image.fromarray(out.astype(np.uint8)).crop((x0-dx0,y0-dy0,x1-dx0,y1-dy0))
    imRGBA.paste(pt,box,msk)
def _tpatch(fr,t,fx,fy,fr_,ax,fq,ph2):
    rc=int(fr_*W); cx=int(fx*W); cy=int(fy*H)
    dx=int(ax*math.sin(2*math.pi*fq*t+ph2)+ax*0.9); dyy=int(ax*0.5*math.sin(2*math.pi*fq*0.8*t+ph2+1.0))
    bx2=(cx-rc,cy-rc,cx+rc,cy+rc)
    pt2=fr.crop(bx2)
    mm2=Image.new("L",(2*rc,2*rc),0); ImageDraw.Draw(mm2).ellipse((10,10,2*rc-10,2*rc-10),fill=200)
    fr.paste(pt2,(bx2[0]+dx,bx2[1]+dyy),mm2.filter(ImageFilter.GaussianBlur(18)))
def shot_frame(s,t):
    p,t0,t1,z0,z1,px,dy,g=s
    sd=t1-t0; pr=max(0,min(1,(t-t0)/sd))
    z=z0+(z1-z0)*pr
    if "n7_rishi" in p and pr>0.9: z+=0.06*((pr-0.9)/0.1)**2
    if "n2_murti" in p: z=max(1.002,z*(1.0+0.005*math.sin(2*math.pi*0.22*t)))
    s1g=None
    if "s1_vivid" in p:
        im=cover(IMGS[p],1.0).convert("RGBA")
        for (wbx,(pvx,pvy),sgn,phz,msk),amax in zip(WINGS,(11.0,9.0)):
            warp_wing(im,wbx,(pvx,pvy),msk,t,sgn,phz,amax)
        wbx,(pvx,pvy),sgn,phz,msk=WINGS2[2]
        warp_wing(im,wbx,(pvx,pvy),msk,t,-1.0,0.8,6.0)
        for (fx,fy,fr_,ax,fq,ph2) in [(0.30,0.34,0.07,3,0.5,1.0),(0.48,0.40,0.07,3,0.4,2.2)]:
            _tpatch(im,t,fx,fy,fr_,ax,fq,ph2)
        for (fx,fy,fr_,ax,fq,ph2) in [(0.14,0.10,0.11,9,0.08,0.0),(0.52,0.06,0.09,7,0.07,2.0),(0.88,0.72,0.10,9,0.085,4.0),(0.08,0.84,0.10,7,0.08,1.0)]:
            _tpatch(im,t,fx,fy,fr_,ax,fq,ph2)
        vo_=VORT.rotate((t*220)%360,resample=Image.BILINEAR)
        va=vo_.getchannel("A").point(lambda v:int(min(255,v*1.1*flick(t,6.1,9.7,1.3))))
        vo_.putalpha(va); im.alpha_composite(vo_,(int(0.40*im.width)-125,int(0.135*im.height)-125))
        zz=1.26-(1.26-1.05)*(1-(1-pr)**1.7)
        sw,sh=int(im.width*zz),int(im.height*zz)
        im=im.resize((sw,sh),Image.BILINEAR)
        pre=1-(1-pr)**2.2
        ox=(sw-W)//2+int(50*(1-pre))+int(5*math.sin(t*2*math.pi*0.5))
        oy=(sh-H)//2+int(170*(1-pre))+int(8*math.sin(t*2*math.pi*0.85+1.6))
        ox=max(0,min(sw-W,ox)); oy=max(0,min(sh-H,oy))
        fr=im.crop((ox,oy,ox+W,oy+H))
        s1g=((int(0.40*sw)-ox)/W,(int(0.135*sh)-oy)/H)
    else:
        im=cover(IMGS[p],z)
        ox=int((im.width-W)/2 + px*math.sin(pr*math.pi*0.9))
        oy=int((im.height-H)/2 - dy*pr)
        ox=max(0,min(im.width-W,ox)); oy=max(0,min(im.height-H,oy))
        fr=im.crop((ox,oy,ox+W,oy+H)).convert("RGBA")
    if "n2_murti" in p:
        for (fx,fy,fr_,ax,fq,ph2) in [(0.80,0.30,0.15,6,0.07,0.5),(0.45,0.16,0.12,5,0.06,2.5),(0.78,0.62,0.13,5,0.055,4.5)]:
            _tpatch(fr,t,fx,fy,fr_,ax,fq,ph2)
        vo_=VORT2.rotate((-t*150)%360,resample=Image.BILINEAR)
        va=vo_.getchannel("A").point(lambda v:int(min(255,v*1.4*flick(t,5.3,8.9,2.1))))
        vo_.putalpha(va); fr.alpha_composite(vo_,(int(0.63*W)-360,int(0.09*H)-360))
    if "bg_plate" in p:
        for F,sp,ba in ((F1,-95,0.85),(F2,70,0.7)):
            fl=xformW(F,(t*sp)%360,1.18)
            aa=fl.getchannel("A").point(lambda v:int(min(255,v*ba*flick(t,5.1,8.3,sp))))
            fl.putalpha(aa); fr.alpha_composite(fl,(WCX-fl.width//2,WCY-fl.height//2))
        rr_=xformW(WHEEL,(t*34)%360,1.0)
        gl2=rr_.filter(ImageFilter.GaussianBlur(22))
        gl2.putalpha(gl2.getchannel("A").point(lambda v:int(v*0.8)))
        fr.alpha_composite(gl2,(WCX-gl2.width//2,WCY-gl2.height//2))
        fr.alpha_composite(rr_,(WCX-rr_.width//2,WCY-rr_.height//2))
    if p in ROTP:
        rcx,rcy,rrr,spd,osc=ROTP[p]; rcx=int(rcx*W); rcy=int(rcy*H); rrp=int(rrr*W)
        angr=(t*spd)%360 if spd else osc[0]*math.sin(t*osc[1]*2*math.pi)
        bx=(rcx-rrp,rcy-rrp,rcx+rrp,rcy+rrp)
        disc=fr.crop(bx).rotate(-angr,resample=Image.BILINEAR)
        mm=Image.new("L",(2*rrp,2*rrp),0); ImageDraw.Draw(mm).ellipse((8,8,2*rrp-8,2*rrp-8),fill=255)
        fr.paste(disc,bx,mm.filter(ImageFilter.GaussianBlur(14)))
    gx,gy,gr=g
    if s1g is not None: gx,gy=s1g
    gi=GL[p].copy()
    pулse=0.60+0.40*math.sin(t*2*math.pi*0.4+1.1)
    if "mind_head" in p: pулse*= (0.55+0.45*pr)
    if "n14_cta" in p: pулse*= (1.0+0.5*pr)
    al=gi.getchannel("A").point(lambda v:int(v*pулse)); gi.putalpha(al)
    fr.alpha_composite(gi,(int(gx*W)-gi.width//2,int(gy*H)-gi.height//2))
    ray=Image.new("RGBA",(W,H),(0,0,0,0)); rd=ImageDraw.Draw(ray)
    for k in range(2):
        ang=math.radians(-14+28*k)
        x0=W*0.5+math.tan(ang)*H
        ra=int(12*flick(t,7.3+k,11.1,k*2.3))
        rd.polygon([(W*0.5-70,-50),(W*0.5+70,-50),(x0+180,H),(x0-180,H)],fill=(255,208,120,ra))
    fr.alpha_composite(ray.filter(ImageFilter.GaussianBlur(24)))
    sx=int((t*14)%1080); sy=int((t*5)%1920)
    sl=smoke.crop((sx,sy,sx+W,sy+H))
    fr.alpha_composite(Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120),sl.point(lambda v:int(v*0.06))]))
    pd=ImageDraw.Draw(fr)
    for (p0,p1,spd,ph) in PART:
        py=(p1-t*spd*0.045)%1.0; pxx=(p0+0.012*math.sin(t*1.3+ph))%1.0
        a2=int(110*(0.4+0.6*math.sin(t*2+ph)**2)); r2=2 if spd<0.8 else 3
        pd.ellipse((pxx*W-r2,py*H-r2,pxx*W+r2,py*H+r2),fill=(255,214,140,a2))
    return fr

def frame(i):
    t=i/FPS
    cur=None; prev=None; mix=0
    for si,s in enumerate(SHOTS):
        if s[1]<=t<s[2]: cur=s
        if si>0 and SHOTS[si][1]<=t<SHOTS[si][1]+XF: prev=SHOTS[si-1]; mix=1-(t-SHOTS[si][1])/XF
    if cur is None: cur=SHOTS[-1]
    fr=shot_frame(cur,min(t,cur[2]-0.001))
    if prev is not None and mix>0:
        fr=Image.blend(fr,shot_frame(prev,min(t,prev[2]-0.001)),mix)
    # hook title
    if 0.3<=t<5.3:
        a=min(1,(t-0.3)/0.35,(5.3-t)/0.5)
        ti=Image.new("RGBA",(W,420),(0,0,0,0)); td=ImageDraw.Draw(ti)
        tw=td.textlength("घूमता चक्र",font=TITLE)
        hal=Image.new("RGBA",(W,420),(0,0,0,0)); hdw=ImageDraw.Draw(hal)
        hdw.text(((W-tw)/2,60),"घूमता चक्र",font=TITLE,fill=(0,0,0,255))
        hal=hal.filter(ImageFilter.GaussianBlur(14))
        ti.alpha_composite(hal); ti.alpha_composite(hal)
        td=ImageDraw.Draw(ti)
        td.text(((W-tw)/2,60),"घूमता चक्र",font=TITLE,fill=GOLD+(255,))
        sub="विष्णु जी की उँगली का रहस्य"
        sw=td.textlength(sub,font=SUBT)
        td.text(((W-sw)/2,250),sub,font=SUBT,fill=PAPER+(235,))
        sc=1.045-0.045*min(1,(t-0.3)/0.9)
        ti2=ti.resize((int(W*sc),int(420*sc)),Image.BILINEAR)
        alc=ti2.getchannel("A").point(lambda v:int(v*a)); ti2.putalpha(alc)
        fr.alpha_composite(ti2,(int((W-ti2.width)/2),int(H*0.205)))
    # captions
    inwp=None
    for (wa,wb,wl_,wt_) in WP:
        if wa<=t<wb: inwp=(wl_,wt_); break
    if inwp is not None:
        draw_wordpop(fr,t,inwp[0],inwp[1])
    for (c0,c1,txt) in CAPS:
        if inwp is not None: break
        if c0<=t<c1:
            a=1.0
            f=TIRO if len(txt)<24 else TIRO_S
            ci=cap_img(txt,f); c2=ci.copy()
            alx=c2.getchannel("A").point(lambda v:int(v*max(0,a))); c2.putalpha(alx)
            fr.alpha_composite(c2,(0,int(H*0.665)))
            break
    # CTA extras
    if t>=93.19:
        e=min(1,(t-93.19)/0.7); ee=1-(1-e)**3
        ycard=int(H*0.30 - (1-ee)*500)
        fr.alpha_composite(SHAD,(int(W/2-SHAD.width/2),ycard+14))
        fr.alpha_composite(CARD,(int(W/2-CARD.width/2),ycard))
        # subscribe pill pulse
        ps=1+0.03*math.sin(t*3.2)
        pw,ph_=int(360*ps),int(96*ps)
        pill=Image.new("RGBA",(pw,ph_),(0,0,0,0)); pld=ImageDraw.Draw(pill)
        pld.rounded_rectangle((0,0,pw-1,ph_-1),ph_//2,fill=(226,56,38,255))
        stw=pld.textlength("SUBSCRIBE",font=SUBF)
        pld.text(((pw-stw)/2,ph_/2-30),"SUBSCRIBE",font=SUBF,fill=(255,255,255,255))
        fr.alpha_composite(pill,(int(W/2-pw/2),int(H*0.575-ph_/2)))
    d=ImageDraw.Draw(fr)
    d.text((W-150,H-64),"AI ART",font=MONO,fill=(255,255,255,118))
    d.text((40,H-64),"CHRONIC OF HISTORIC",font=MONO,fill=(255,255,255,60))
    fr.alpha_composite(VIGRGBA)
    g=np.asarray(fr.convert("RGB"),np.int16)
    g=np.clip(g+np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16),0,255).astype(np.uint8)
    out=Image.fromarray(g)
    if t>DUR-0.8: out=ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.8))
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    return out

if __name__=="__main__":
    write_srt("/var/tmp/sh38/final.srt")
    done=0
    for i in range(N):
        p=f"{OUT}/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=87)
        done+=1
        if done%300==0: print("fr",i,flush=True)
    print("FRAMES DONE",N)
