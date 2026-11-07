# STICKMAN TEST — 100% code skeleton animation (walk/run/jump-flip/land/victory)
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
FB=ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/Inter-Black.ttf',56*2)
FO=ImageFont.truetype('/home/user/explainer-pipeline/assets/fonts/Teko.ttf',110*2)
W,H=1080,1920; SS=2; FPS=30; DUR=10.0; N=int(DUR*FPS)
GY=1430  # ground
INK=(26,26,30); PAPER=(250,247,240); ORG=(226,96,40)
# ---- motion profile: x(t) precompute (continuous) ----
def vel(t):
    if t<0.4: return 0
    if t<3.2: return 390
    if t<5.5: return 390+470*min(1,(t-3.2)/0.8)
    if t<6.45: return 860                 # airborne
    if t<7.0: return max(0,860*(1-(t-6.45)/0.55))
    return 0
X=[120.0]
for i in range(1,N+1): X.append(X[-1]+vel(i/FPS)/FPS)
TJ,TA=5.5,0.95                            # jump launch, airtime
OBX=X[int((TJ+TA*0.5)*FPS)]               # obstacle mid-air pe
def smooth(a): return a*a*(3-2*a)
def pose(t):
    # returns dict: lean, legs[(th,kn)x2], arms[(sh,el)x2], bob, squash, flip, armup
    p={'lean':0,'legs':[(0,0),(0,0)],'arms':[(10,15),(-10,15)],'bob':2*math.sin(t*2.2),'squash':1.0,'flip':0,'ddust':0}
    walk=run=air=land=vict=0.0
    if 0.4<=t<3.2: walk=min(1,(t-0.4)/0.25)
    if 3.2<=t<TJ: run=min(1,(t-3.2)/0.4); walk=1-run
    if TJ<=t<TJ+TA: air=1.0
    if TJ+TA<=t<7.6: land=1.0
    if t>=7.6: vict=min(1,(t-7.6)/0.4); land=1-vict
    x=X[int(t*FPS)]
    if walk>0 or run>0:
        stride=250+110*run; ph=2*math.pi*x/stride
        A=28+20*run; K=35+30*run
        thL=A*math.sin(ph); thR=A*math.sin(ph+math.pi)
        knL=K*max(0,math.sin(ph+2.2)); knR=K*max(0,math.sin(ph+math.pi+2.2))
        aA=25+20*run
        p['legs']=[(thL,knL),(thR,knR)]
        p['arms']=[(aA*math.sin(ph+math.pi),25+15*run),(aA*math.sin(ph),25+15*run)]
        p['lean']=4*walk+14*run
        p['bob']=abs(math.sin(ph))*(6+8*run)
    if air>0:
        tau=(t-TJ)/TA
        p['flip']=360*smooth(tau)
        p['legs']=[(70,100),(55,95)]; p['arms']=[(140,30),(120,40)]; p['lean']=0; p['bob']=0
    if land>0:
        lt=min(1,(t-TJ-TA)/0.18)
        sq=1-0.30*math.sin(min(1,(t-TJ-TA)/0.35)*math.pi)
        p['squash']=sq; p['legs']=[(25,70*(1-lt*0.6)),(18,60*(1-lt*0.6))]
        p['arms']=[(60*(1-lt),20),(50*(1-lt),25)]; p['lean']=10*(1-lt); p['ddust']=1-lt
    if vict>0:
        wv=math.sin(t*7)
        p['legs']=[(4,6),(-4,6)]; p['arms']=[(168+8*wv,10),(165-8*wv,12)]
        p['bob']=3*math.sin(t*3); p['lean']=0
    return p
def jump_dy(t):
    if TJ<=t<TJ+TA:
        tau=t-TJ; vy=2*320/ (TA/2)
        g=2*vy/TA
        return -(vy*tau-0.5*g*tau*tau)*2/ (TA*vy) *320*2/2  # normalized parabola
    return 0
def dy_air(t):
    if TJ<=t<TJ+TA:
        tau=(t-TJ)/TA
        return -560*4*tau*(1-tau)
    return 0
L1,L2,A1,A2,TOR,HR=190,190,146,146,260,62
def draw_man(d,x,y,P,sc=1.0):
    lean=math.radians(P['lean']); flip=math.radians(P['flip'])
    def rot(px,py,cx,cy,a):
        s,c=math.sin(a),math.cos(a); dx,dy=px-cx,py-cy
        return cx+dx*c-dy*s, cy+dx*s+dy*c
    hip=(x,y)
    sq=P['squash']
    pts={}
    neck=(x+TOR*math.sin(lean)*sq*0 + TOR*math.sin(lean), y-TOR*sq*math.cos(lean))
    headc=(neck[0]+ (HR+14)*math.sin(lean), neck[1]-(HR+14)*math.cos(lean))
    segs=[]
    segs.append((hip,neck,21))
    for i,(th,kn) in enumerate(P['legs']):
        a1=math.radians(th); a2=math.radians(th-kn) if False else math.radians(th+ (kn if th<0 else kn))
        a1=math.radians(th); 
        kx=hip[0]+L1*math.sin(a1); ky=hip[1]+L1*math.cos(a1)*sq
        a2=math.radians(th - kn)
        ax=kx+L2*math.sin(a2); ay=ky+L2*math.cos(a2)*sq
        segs.append((hip,(kx,ky),19)); segs.append(((kx,ky),(ax,ay),19))
    sh=neck
    for i,(sa,el) in enumerate(P['arms']):
        b1=math.radians(180-sa) if False else math.radians(sa)
        ex=sh[0]+A1*math.sin(b1)*(1 if i==0 else -1); ey=sh[1]+A1*math.cos(b1)
        b2=math.radians(sa+el)
        hx=ex+A2*math.sin(b2)*(1 if i==0 else -1); hy=ey+A2*math.cos(b2)
        segs.append((sh,(ex,ey),17)); segs.append(((ex,ey),(hx,hy),17))
    # flip rotation around hip
    out=[]
    for (p1,p2,w) in segs:
        q1=rot(p1[0],p1[1],x,y-190,flip); q2=rot(p2[0],p2[1],x,y-190,flip)
        out.append((q1,q2,w))
    hc=rot(headc[0],headc[1],x,y-190,flip)
    for (q1,q2,w) in out:
        d.line([q1,q2],fill=INK,width=int(w*SS*sc),joint="curve")
        for q in (q1,q2):
            r=w*SS*sc*0.5; d.ellipse((q[0]-r,q[1]-r,q[0]+r,q[1]+r),fill=INK)
    r=HR*SS/2*2*sc*0.5
    d.ellipse((hc[0]-HR*sc*SS/1,hc[1]-HR*sc*SS/1,hc[0]+HR*sc*SS,hc[1]+HR*sc*SS),outline=INK,width=int(16*SS*sc))
def frame(i):
    t=i/FPS
    im=Image.new("RGB",(W*SS,H*SS),PAPER)
    d=ImageDraw.Draw(im)
    camx=max(0,X[i]-W*0.40)
    # dot grid
    gx0=int(camx//80)*80
    for gx in range(gx0,int(camx)+W+80,80):
        for gy in range(80,H,80):
            d.ellipse(((gx-camx)*SS-3,gy*SS-3,(gx-camx)*SS+3,gy*SS+3),fill=(214,208,196))
    # ground
    d.line([(0,GY*SS+40),(W*SS,GY*SS+40)],fill=INK,width=8*SS)
    # obstacle
    ox=(OBX-camx)
    d.rounded_rectangle((ox*SS-110*SS,(GY-380)*SS,ox*SS+110*SS,GY*SS+40),24,outline=INK,width=9*SS,fill=(240,233,220))
    d.text((ox*SS-38*SS,(GY-300)*SS),"42",font=FO,fill=INK)
    P=pose(t)
    y=GY-0.92*(L1+L2)+P['bob']+dy_air(t)
    draw_man(d,(X[i]-camx),y,P)
    # dust on land/skid
    if P.get('ddust',0)>0:
        rng=np.random.default_rng(777)
        for k in range(14):
            a=rng.uniform(0,3.14); rr=rng.uniform(10,90)*P['ddust']
            px=(X[i]-camx-50-rr*math.cos(a)*0.8); py=GY-8-rr*math.sin(a)*0.45
            rad=(3+5*P['ddust'])
            d.ellipse(((px-rad)*SS,(py-rad)*SS,(px+rad)*SS,(py+rad)*SS),fill=(190,182,168))
    # confetti on victory
    if t>=7.8:
        rng=np.random.default_rng(99)
        for k in range(26):
            px=rng.uniform(0.1,0.9)*W; spd=rng.uniform(140,260); ph0=rng.uniform(0,6)
            py=(t-7.8)*spd+rng.uniform(-300,0)
            if 0<py<H:
                col=ORG if k%2 else (240,180,40)
                d.ellipse(((px-7)*SS,(py-7)*SS,(px+7)*SS,(py+7)*SS),fill=col)
    # top title
    d.text((60*SS,90*SS),"STICKMAN • 100% CODE",font=FB,fill=INK)
    out=im.resize((W,H),Image.LANCZOS)
    if t<0.2: out=ImageEnhance.Brightness(out).enhance(0.6+2*t)
    if t>DUR-0.5: out=ImageEnhance.Brightness(out).enhance(max(0.2,(DUR-t)/0.5+0.4))
    return out
if __name__=="__main__":
    for i in range(N):
        p=f"/var/tmp/stick/{i:05d}.jpg"
        if os.path.exists(p): continue
        frame(i).save(p,quality=88)
        if i%60==0: print("fr",i,flush=True)
    print("DONE",N)
