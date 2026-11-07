import os, math, importlib.util, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
spec=importlib.util.spec_from_file_location("r38","/home/user/explainer-pipeline/tools/render_shunya38.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
W,H=1080,1920; FPS=30
A="/home/user/explainer-pipeline/assets/reel50"
OUT="/var/tmp/reel50/frames"
DUR=51.0; N=int(DUR*FPS); XF=0.5
YEL=m.YEL; WHT=m.WHT
# scenes: (name, start, end, vo_start, vo_dur, kind)
SC=[("s1",0.00,5.10,0.50,3.70,"ltx"),
    ("s2",5.10,12.00,5.50,5.78,"ltx_or_code"),
    ("s3",12.00,18.70,12.40,5.62,"code"),
    ("s4",18.70,25.80,19.10,5.98,"code"),
    ("s5",25.80,32.40,26.20,5.57,"ltx_or_code"),
    ("s6",32.40,37.60,32.80,4.06,"ltx_or_code"),
    ("s7",37.60,44.50,38.00,5.74,"code"),
    ("s8",44.50,51.00,45.00,3.05,"code")]
IMG={"s2":f"{A}/n2_murti_v.jpg","s3":f"{A}/n3_granth_v.jpg","s4":f"{A}/n4_wheelbg_v.jpg",
     "s5":f"{A}/n5_rishi_v.jpg","s6":f"{A}/n6_storm_v.jpg","s7":f"{A}/n7_galaxy_v.jpg","s8":f"{A}/n8_cta_v.jpg"}
IMGS={k:Image.open(v).convert("RGB") for k,v in IMG.items()}
LTXD={}
for nm in ("s1","s2","s5","s6"):
    d=f"/var/tmp/ltxfr_{nm}" if nm!="s1" else "/var/tmp/ltxfr"
    if os.path.isdir(d) and len(os.listdir(d))>30: LTXD[nm]=(d,len(os.listdir(d)))
# word-pop spec: per scene lines [(word,tier,color)]
def wp_times(lines, vs, vd):
    tot=sum(len(w) for ln in lines for (w,_,_) in ln); acc=vs; ts=[]
    for ln in lines:
        for (w,_,_) in ln:
            ts.append(acc); acc+=vd*len(w)/tot
    return ts
WPS={}
_spec={
"s1":[[("हर",0,WHT),("मूर्ति",0,WHT),("में",0,WHT)],[("एक",1,YEL),("चीज़",1,YEL)],[("कभी",2,YEL),("नहीं",2,YEL),("बदलती",2,WHT)]],
"s2":[[("विष्णु",0,WHT),("जी",0,WHT),("की",0,WHT),("उँगली",0,WHT),("पर",0,WHT),("ये",0,WHT),("चक्र...",0,WHT)],
      [("हज़ारों",1,YEL),("साल",1,YEL)],[("से",2,WHT),("घूम",2,YEL),("रहा",2,WHT),("है...",2,WHT),("क्यों?",2,YEL)]],
"s3":[[("पुराण",0,WHT),("कहते",0,WHT),("हैं",0,WHT),("—",0,WHT),("इसका",0,WHT),("नाम",0,WHT)],
      [("सुदर्शन",1,YEL)],[("मतलब",2,WHT),("—",2,WHT),("सही",2,YEL),("देखना।",2,YEL)]],
"s4":[[("तीर",0,WHT),("फेंको",0,WHT),("तो",0,WHT),("गया...",0,WHT)],[("पर",1,YEL),("ये",1,YEL),("चक्र",1,YEL)],
      [("काम",0,WHT),("पूरा",0,WHT),("करके",0,WHT)],[("वापस",2,YEL),("लौट",2,YEL),("आता",2,WHT),("है।",2,WHT)]],
"s5":[[("ऋषियों",0,WHT),("ने",0,WHT),("कहा",0,WHT),("—",0,WHT)],[("ये",1,YEL),("पहिया",1,YEL)],
      [("बाहर",2,WHT),("नहीं...",2,WHT),("भीतर",2,YEL),("घूमता",2,YEL),("है।",2,WHT)]],
"s6":[[("आपका",0,WHT),("मन",0,WHT),("भी",0,WHT)],[("दिन-रात",1,YEL)],
      [("ऐसे",0,WHT),("ही",0,WHT),("घूमता",0,WHT),("है...",0,WHT)],[("बिना",2,YEL),("रुके।",2,YEL)]],
"s7":[[("सधा",0,WHT),("हुआ",0,WHT),("मन",0,WHT)],[("वही",1,YEL),("चक्र",1,YEL)],
      [("है",0,WHT),("—",0,WHT),("जो",0,WHT),("हर",0,WHT),("उलझन",0,WHT),("को",0,WHT)],[("काट",2,YEL),("देता",2,WHT),("है।",2,WHT)]],
"s8":[[("ऐसे",0,WHT),("ही",0,WHT),("रहस्यों",0,WHT),("के",0,WHT),("लिए...",0,WHT)],[("जुड़े",1,YEL),("रहिए।",1,WHT)]]}
for (nm,a,b,vs,vd,_k) in SC:
    WPS[nm]=(_spec[nm],wp_times(_spec[nm],vs,vd))
GL2={"s2":(0.40,0.12,150),"s3":(0.52,0.35,160),"s4":(0.53,0.30,220),"s5":(0.48,0.56,170),
     "s6":(0.43,0.36,150),"s7":(0.60,0.22,170),"s8":(0.50,0.15,200)}
GLS={k:m.glow_sprite(r) for k,(x,y,r) in GL2.items()}
import random as _rnd
def _rays():
    r=Image.new("RGBA",(W,H),(0,0,0,0)); dr=ImageDraw.Draw(r)
    rd=_rnd.Random(7)
    for k in range(4):
        x0=int(W*(0.12+0.24*k)); wdt=rd.randint(90,160)
        dr.polygon([(x0,-60),(x0+wdt,-60),(x0+wdt-430,H+60),(x0-430,H+60)],fill=(255,230,170,58))
    return r.filter(ImageFilter.GaussianBlur(42))
RAYS=_rays()
GL8=m.glow_sprite(85)
_rg=_rnd.Random(11)
FIRE=[(_rg.uniform(0.30,0.78),_rg.uniform(0.42,0.82),_rg.uniform(0.5,1.3),_rg.uniform(0,6.28)) for _ in range(16)]
EMB=[(_rg.uniform(0.56,0.74),_rg.uniform(0.70,0.92),_rg.uniform(0.5,1.2),_rg.uniform(0,6.28)) for _ in range(12)]
ZR={"s2":(1.08,1.03),"s3":(1.06,1.17),"s4":(1.045,1.105),"s5":(1.16,1.06),"s6":(1.05,1.12),"s7":(1.04,1.11),"s8":(1.04,1.06)}
def _blit_rays(fr,t,amp):
    a=amp*(0.55+0.45*math.sin(t*0.45))
    if a<=0.03: return
    rr=RAYS.copy(); rr.putalpha(rr.getchannel("A").point(lambda v:int(v*a)))
    fr.alpha_composite(rr,(int(26*math.sin(t*0.22)),0))
def rotpatch(fr,cx,cy,rr,ang,hole=0):
    bx=(cx-rr,cy-rr,cx+rr,cy+rr)
    disc=fr.crop(bx).rotate(-ang,resample=Image.BILINEAR)
    mm=Image.new("L",(2*rr,2*rr),0); md=ImageDraw.Draw(mm)
    md.ellipse((8,8,2*rr-8,2*rr-8),fill=255)
    if hole>0: md.ellipse((rr-hole,rr-hole,rr+hole,rr+hole),fill=0)
    fr.paste(disc,bx,mm.filter(ImageFilter.GaussianBlur(16 if hole>0 else 14)))
_SW={}
def swirl(fr,cx,cy,CR,t,Adeg,T):
    if CR not in _SW:
        g=np.arange(-CR,CR).astype(np.float32)
        X,Y=np.meshgrid(g,g)
        R=np.sqrt(X*X+Y*Y)/CR
        _SW[CR]=(R*CR,np.clip(1-R*R,0,1)**2,np.arctan2(Y,X))
    RAD,F,TH=_SW[CR]
    box=(cx-CR,cy-CR,cx+CR,cy+CR)
    win=np.asarray(fr.crop(box).convert("RGB"),np.float32)
    A=math.radians(Adeg)
    p1=(t/T)%1.0; w1=1-abs(2*p1-1)
    out=None
    for pp,wgt in ((p1,w1),(((p1+0.5)%1.0),1-w1)):
        an=TH-((pp-0.5)*A)*F
        sx=np.clip(RAD*np.cos(an)+CR,0,2*CR-2); sy=np.clip(RAD*np.sin(an)+CR,0,2*CR-2)
        x0=sx.astype(np.int32); y0=sy.astype(np.int32)
        fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
        wi=(win[y0,x0]*(1-fx)*(1-fy)+win[y0,x0+1]*fx*(1-fy)+win[y0+1,x0]*(1-fx)*fy+win[y0+1,x0+1]*fx*fy)
        out=wi*wgt if out is None else out+wi*wgt
    patch=Image.fromarray(np.clip(out,0,255).astype(np.uint8))
    mm=Image.new("L",(2*CR,2*CR),0); ImageDraw.Draw(mm).ellipse((4,4,2*CR-4,2*CR-4),fill=255)
    fr.paste(patch,box,mm.filter(ImageFilter.GaussianBlur(6)))
def xw(img,ang,scale):
    r=img.rotate(ang,resample=Image.BILINEAR)
    w2=int(0.50*W*scale); r=r.resize((w2,int(w2*0.55)),Image.BILINEAR)
    return r.rotate(-14,expand=True,resample=Image.BILINEAR)
def scene_frame(s,t):
    nm,a,b,vs,vd,kind=s
    tl=t-a; sd=b-a; pr=max(0,min(1,tl/sd))
    if nm in LTXD:
        d,n=LTXD[nm]
        idx=min(int(tl*30),n-1)
        fr=Image.open(f"{d}/{idx+1:05d}.jpg").convert("RGBA")
    else:
        pe=pr*pr*(3-2*pr)
        z0,z1=ZR.get(nm,(1.08,1.03)); z=z0+(z1-z0)*pe
        art=IMGS[nm]; w0,h0=art.size
        S=max(W/w0,H/h0)*z
        phh=sum(map(ord,nm))
        dr_=0.0 if nm=="s4" else 1.0
        dxf=dr_*7.0*math.sin(t*0.6+phh); dyf=dr_*5.0*math.sin(t*0.83+phh*1.7)
        if nm=="s7": dyf-=55.0*pe
        left=(w0-W/S)/2.0+dxf/S; top=(h0-H/S)/2.0+dyf/S
        left=min(max(0.0,left),w0-W/S); top=min(max(0.0,top),h0-H/S)
        fr=art.transform((W,H),Image.AFFINE,(1.0/S,0,left,0,1.0/S,top),resample=Image.BILINEAR).convert("RGBA")
        if nm=="s2":
            for (fx,fy,fr_,ax,fq,ph2) in [(0.25,0.35,0.12,5,0.07,0.5),(0.70,0.55,0.12,4,0.06,2.5)]:
                m._tpatch(fr,t,fx,fy,fr_,ax,fq,ph2)
            rotpatch(fr,int(0.40*W),int(0.12*H),int(0.085*W),(t*60)%360)
        if nm=="s3":
            for (fx,fy,fr_,ax,fq,ph2) in [(0.70,0.50,0.10,4,0.08,1.0)]:
                m._tpatch(fr,t,fx,fy,fr_,ax,fq,ph2)
            _blit_rays(fr,t,0.75)
            ed=ImageDraw.Draw(fr)
            for (ex,ey,es,eph) in EMB:
                yy=(ey-((t*0.055*es)%0.32))
                aa=int(170*(0.3+0.7*math.sin(t*2.6+eph)**2)*min(1,(ey-yy)*18+0.25))
                xx=(ex+0.014*math.sin(t*1.7+eph))
                ed.ellipse((xx*W-2,yy*H-2,xx*W+2,yy*H+2),fill=(255,190,110,aa))
            fk=1.0+0.035*math.sin(t*9.1)+0.022*math.sin(t*23.7)
            fr=ImageEnhance.Brightness(fr).enhance(max(0.96,min(1.06,fk)))
        if nm=="s4":
            zc=1.075; u4=(0.53+(zc-1)/2)/zc; v4=(0.30+(zc-1)/2)/zc
            cx4=int(round((u4*w0-left)*S)); cy4=int(round((v4*h0-top)*S)); sf=z/zc
            for F,sp,ba in ((m.F1,-95,0.85),(m.F2,70,0.7)):
                fl=xw(F,(t*sp)%360,1.16*sf)
                aa=fl.getchannel("A").point(lambda v:int(min(255,v*ba*m.flick(t,5.1,8.3,sp))))
                fl.putalpha(aa); fr.alpha_composite(fl,(cx4-fl.width//2,cy4-fl.height//2))
            rr_=xw(m.WHEEL,(t*34)%360,1.09*sf)
            gl2=rr_.filter(ImageFilter.GaussianBlur(22))
            gl2.putalpha(gl2.getchannel("A").point(lambda v:int(v*0.8)))
            fr.alpha_composite(gl2,(cx4-gl2.width//2,cy4-gl2.height//2))
            fr.alpha_composite(rr_,(cx4-rr_.width//2,cy4-rr_.height//2))
        if nm=="s5":
            _blit_rays(fr,t,1.0)
            fd=ImageDraw.Draw(fr)
            for (fx2,fy2,fs2,fp2) in FIRE:
                aa=int(190*(0.15+0.85*max(0,math.sin(t*1.1*fs2+fp2))**3))
                xx=fx2+0.016*math.sin(t*0.9+fp2); yy=fy2+0.012*math.sin(t*0.7+fp2*2)
                fd.ellipse((xx*W-2.5,yy*H-2.5,xx*W+2.5,yy*H+2.5),fill=(255,232,150,aa))
        if nm=="s6":
            swirl(fr,int(round((0.490*w0-left)*S)),int(round((0.458*h0-top)*S)),int(0.12*W),t,85,2.6)
            fl=1.0+0.55*max(0,math.sin(t*7.3)*math.sin(t*3.1)-0.58)
            if fl>1.01: fr=ImageEnhance.Brightness(fr).enhance(min(1.30,fl))
        if nm=="s7":
            swirl(fr,int(round((0.635*w0-left)*S)),int(round((0.315*h0-top)*S)),int(0.13*W),t,60,3.8)
        if nm=="s8":
            cx8,cy8,R8=int(0.50*W),int(0.15*H),int(0.165*W)
            ga=t*0.9
            for gk,gph in ((1.0,0.0),(0.55,math.pi)):
                gx8=cx8+int(R8*math.cos(ga+gph)); gy8=cy8+int(R8*0.95*math.sin(ga+gph))
                gg=GL8.copy(); gg.putalpha(gg.getchannel("A").point(lambda v:int(v*gk*(0.55+0.3*math.sin(t*2.1+gph)))))
                fr.alpha_composite(gg,(gx8-GL8.width//2,gy8-GL8.height//2))
    if nm in GL2:
        gx,gy,gr=GL2[nm]; gi=GLS[nm].copy()
        pu=0.60+0.40*math.sin(t*2*math.pi*0.4+1.1)
        if nm=="s8": pu*=(1.0+0.5*pr)
        gi.putalpha(gi.getchannel("A").point(lambda v:int(v*pu)))
        fr.alpha_composite(gi,(int(gx*W)-gi.width//2,int(gy*H)-gi.height//2))
    return fr
def frame(i):
    t=i/FPS
    cur=None; prev=None; mix=0
    for si,s in enumerate(SC):
        if s[1]<=t<s[2]: cur=s
        if si>0 and SC[si][1]<=t<SC[si][1]+XF: prev=SC[si-1]; mix=1-(t-SC[si][1])/XF
    if cur is None: cur=SC[-1]
    fr=scene_frame(cur,min(t,cur[2]-0.001))
    if prev is not None and mix>0:
        if prev[0]=="s2" and "s2" not in LTXD:
            pv=Image.open("/var/tmp/reel50/frames/00359.jpg").convert("RGBA")
        else:
            pv=scene_frame(prev,min(t,prev[2]-0.001))
        fr=Image.blend(fr,pv,mix)
    sx=int((t*14)%1080); sy=int((t*5)%1920)
    sl=m.smoke.crop((sx,sy,sx+W,sy+H))
    fr.alpha_composite(Image.merge("RGBA",[Image.new("L",(W,H),200),Image.new("L",(W,H),170),Image.new("L",(W,H),120),sl.point(lambda v:int(v*0.05))]))
    pd=ImageDraw.Draw(fr)
    for (p0,p1,spd,ph) in m.PART:
        py=(p1-t*spd*0.045)%1.0; pxx=(p0+0.012*math.sin(t*1.3+ph))%1.0
        a2=int(110*(0.4+0.6*math.sin(t*2+ph)**2)); r2=2 if spd<0.8 else 3
        pd.ellipse((pxx*W-r2,py*H-r2,pxx*W+r2,py*H+r2),fill=(255,214,140,a2))
    # title on s1
    if 0.3<=t<4.9:
        a=min(1,(t-0.3)/0.35,(4.9-t)/0.5)
        ti=Image.new("RGBA",(W,420),(0,0,0,0)); td=ImageDraw.Draw(ti)
        tw=td.textlength("घूमता चक्र",font=m.TITLE)
        hal=Image.new("RGBA",(W,420),(0,0,0,0)); hdw=ImageDraw.Draw(hal)
        hdw.text(((W-tw)/2,60),"घूमता चक्र",font=m.TITLE,fill=(0,0,0,255))
        hal=hal.filter(ImageFilter.GaussianBlur(14))
        ti.alpha_composite(hal); ti.alpha_composite(hal)
        td=ImageDraw.Draw(ti)
        td.text(((W-tw)/2,60),"घूमता चक्र",font=m.TITLE,fill=m.GOLD+(255,))
        sub="विष्णु जी की उँगली का रहस्य"
        sw=td.textlength(sub,font=m.SUBT)
        td.text(((W-sw)/2,250),sub,font=m.SUBT,fill=m.PAPER+(235,))
        sc=1.045-0.045*min(1,(t-0.3)/0.9)
        ti2=ti.resize((int(W*sc),int(420*sc)),Image.BILINEAR)
        alc=ti2.getchannel("A").point(lambda v:int(v*a)); ti2.putalpha(alc)
        fr.alpha_composite(ti2,(int((W-ti2.width)/2),int(H*0.205)))
    # word-pop captions
    for (nm,a,b,vs,vd,_k) in SC:
        if a<=t<b and t>=vs-0.05:
            lines,times=WPS[nm]
            m.draw_wordpop(fr,t,lines,times,y0=int(H*0.775) if nm=="s8" else None); break
    # CTA extras
    if t>=45.2:
        e=min(1,(t-45.2)/0.7); ee=1-(1-e)**3
        ycard=int(H*0.30-(1-ee)*500)
        fr.alpha_composite(m.SHAD,(int(W/2-m.SHAD.width/2),ycard+14))
        fr.alpha_composite(m.CARD,(int(W/2-m.CARD.width/2),ycard))
        ps=1+0.03*math.sin(t*3.2)
        pw,ph_=int(360*ps),int(96*ps)
        pill=Image.new("RGBA",(pw,ph_),(0,0,0,0)); pld=ImageDraw.Draw(pill)
        pld.rounded_rectangle((0,0,pw-1,ph_-1),ph_//2,fill=(226,56,38,255))
        stw=pld.textlength("SUBSCRIBE",font=m.SUBF)
        pld.text(((pw-stw)/2,ph_/2-30),"SUBSCRIBE",font=m.SUBF,fill=(255,255,255,255))
        fr.alpha_composite(pill,(int(W/2-pw/2),int(H*0.575-ph_/2)))
    d=ImageDraw.Draw(fr)
    d.text((W-150,H-64),"AI ART",font=m.MONO,fill=(255,255,255,118))
    d.text((40,H-64),"CHRONIC OF HISTORIC",font=m.MONO,fill=(255,255,255,60))
    fr.alpha_composite(m.VIGRGBA)
    g=np.asarray(fr.convert("RGB"),np.int16)
    g=np.clip(g+np.random.default_rng(i).integers(-3,4,(H,W,1),np.int16),0,255).astype(np.uint8)
    out=Image.fromarray(g)
    if t>DUR-0.8: out=ImageEnhance.Brightness(out).enhance(max(0,(DUR-t)/0.8))
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    return out
VO_TXT={"s1":"हर मूर्ति में एक चीज़ कभी नहीं बदलती।","s2":"विष्णु जी की उँगली पर ये चक्र... हज़ारों साल से घूम रहा है। क्यों?",
"s3":"पुराण कहते हैं — इसका नाम सुदर्शन है। मतलब — सही देखना।","s4":"तीर फेंको तो गया... पर ये चक्र, काम पूरा करके वापस लौट आता है।",
"s5":"ऋषियों ने कहा — ये पहिया बाहर नहीं... भीतर घूमता है।","s6":"आपका मन भी दिन-रात ऐसे ही घूमता है... बिना रुके।",
"s7":"सधा हुआ मन वही चक्र है — जो हर उलझन को काट देता है।","s8":"ऐसे ही रहस्यों के लिए... जुड़े रहिए।"}
def write_srt(path):
    def ts(t):
        hh=int(t//3600); mm=int(t%3600//60); ss=int(t%60); ms=int((t%1)*1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"
    with open(path,"w") as f:
        for i,(nm,a,b,vs,vd,_k) in enumerate(SC,1):
            f.write(f"{i}\n{ts(vs)} --> {ts(vs+vd)}\n{VO_TXT[nm]}\n\n")
if __name__=="__main__":
    write_srt("/var/tmp/reel50/final.srt")
    print("LTX scenes:",list(LTXD.keys()),flush=True)
    done=0
    for i in range(N):
        p=f"{OUT}/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=87)
        done+=1
        if done%300==0: print("fr",i,flush=True)
    print("FRAMES DONE",N)
