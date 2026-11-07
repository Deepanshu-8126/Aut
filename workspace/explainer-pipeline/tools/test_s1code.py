# REEL-42 OPENING (s1) — 100% CODE (flap-warp v5) — faithful: title+wordpop+fades
import os, math, importlib.util, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
spec=importlib.util.spec_from_file_location("tw","/home/user/explainer-pipeline/tools/test_codewings.py")
tw=importlib.util.module_from_spec(spec); spec.loader.exec_module(tw)   # wings v5 engine
rl=tw.rl; m=tw.m
W,H=1080,1920; FPS=30; DUR=5.1; N=int(DUR*FPS)
def frame(i):
    t=i/FPS
    fr=tw.frame(i).convert("RGBA")   # wings+clouds+halo+rays+particles+grain (v5)
    # title (reel-42 locked block)
    if 0.3<=t<4.9:
        a=min(1,(t-0.3)/0.35,(4.9-t)/0.5)
        ti=Image.new("RGBA",(W,420),(0,0,0,0)); td=ImageDraw.Draw(ti)
        tww=td.textlength("घूमता चक्र",font=m.TITLE)
        hal=Image.new("RGBA",(W,420),(0,0,0,0)); hdw=ImageDraw.Draw(hal)
        hdw.text(((W-tww)/2,60),"घूमता चक्र",font=m.TITLE,fill=(0,0,0,255))
        hal=hal.filter(ImageFilter.GaussianBlur(14))
        ti.alpha_composite(hal); ti.alpha_composite(hal)
        td=ImageDraw.Draw(ti)
        td.text(((W-tww)/2,60),"घूमता चक्र",font=m.TITLE,fill=m.GOLD+(255,))
        sub="विष्णु जी की उँगली का रहस्य"
        sw=td.textlength(sub,font=m.SUBT)
        td.text(((W-sw)/2,250),sub,font=m.SUBT,fill=m.PAPER+(235,))
        sc=1.045-0.045*min(1,(t-0.3)/0.9)
        ti2=ti.resize((int(W*sc),int(420*sc)),Image.BILINEAR)
        alc=ti2.getchannel("A").point(lambda v:int(v*a)); ti2.putalpha(alc)
        fr.alpha_composite(ti2,(int((W-ti2.width)/2),int(H*0.205)))
    # word-pop (s1 locked spec)
    if t>=0.45:
        lines,times=rl.WPS["s1"]
        m.draw_wordpop(fr,t,lines,times)
    out=fr.convert("RGB")
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(t/0.2)
    return out
if __name__=="__main__":
    for i in range(N):
        p=f"/var/tmp/s1c/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=87)
    print("DONE",N)
