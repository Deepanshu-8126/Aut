import numpy as np, subprocess, os
SR=48000; DUR=25.0; N=int(SR*DUR)
FF="/var/tmp/ffstatic/ffmpeg"
SFX="/home/user/explainer-pipeline/assets/sfx/"
MUS="/home/user/explainer-pipeline/assets/music/677.mp3"
def load(f,trim=None):
    cmd=[FF,"-nostdin","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f32le","-"]
    raw=subprocess.run(cmd,capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.float32).copy()
    if trim: a=a[:int(trim*SR)]
    return a
def fade(a,fi=0.01,fo=0.05):
    a=a.copy(); ni=int(fi*SR); no=int(fo*SR)
    if ni>0 and len(a)>ni: a[:ni]*=np.linspace(0,1,ni)
    if no>0 and len(a)>no: a[-no:]*=np.linspace(1,0,no)
    return a
mix=np.zeros(N,dtype=np.float32)
def put(a,t,vol):
    i0=int(t*SR); seg=a*vol
    i1=min(N,i0+len(seg))
    if i1>i0: mix[i0:i1]+=seg[:i1-i0]
# ---- SOUND MAP (Hollywood stack, library-first) ----
braam=fade(load(SFX+"mk1287.mp3",2.6),0.005,0.4)
deep =fade(load(SFX+"mk1143.mp3",2.0),0.005,0.3)
big  =fade(load(SFX+"mk788.mp3",3.0),0.005,0.5)
wfast=fade(load(SFX+"mk1492.mp3",1.0))
wair =fade(load(SFX+"mk1489.mp3",1.2))
tun  =fade(load(SFX+"mk1486.mp3",2.2),0.01,0.6)
thud =fade(load(SFX+"mk2636.mp3",0.8))
riser=fade(load(SFX+"mk790.mp3"),0.02,0.03)   # 2.61s
heart=fade(load(SFX+"mk494.mp3",1.6),0.05,0.3) # one beat cycle ~1.6s
susp =fade(load(SFX+"mk685.mp3",2.4),0.02,0.6)
hitP =fade(load(SFX+"mk2155.mp3",1.2),0.002,0.3)   # strong punch impact
hardP=fade(load(SFX+"mk2143.mp3",0.9),0.002,0.2)   # hard quick punch
plant=fade(load(SFX+"mk2151.mp3",0.5),0.002,0.1)   # soft pad plant
elec =fade(load(SFX+"mk2599.mp3",2.2),0.01,0.7)    # electric shockwave (charge)
roar =fade(load(SFX+"mk1972.mp3",2.3),0.01,0.6)    # GIANT MONSTER ROAR
whist=fade(load(SFX+"mk2048.mp3",1.0),0.005,0.2)   # air whistle (launch)
metal=fade(load(SFX+"mk2980.mp3",1.6),0.002,0.4)   # factory metal hit (rack crash)
can  =fade(load(SFX+"mk389.mp3",1.3),0.01,0.3)     # falling can rattle
boing=fade(load(SFX+"mk2894.mp3",1.1),0.002,0.2)   # cartoon boing (pad bonk)
pop  =fade(load(SFX+"mk2364.mp3",0.35),0.002,0.08) # hard pop click (captions)
fallw=fade(load(SFX+"mk395.mp3",0.55),0.01,0.12)   # falling whistle (pad drop)
scream=fade(load(SFX+"mk391.mp3",0.95),0.02,0.25)  # batman flight scream
splat=fade(load(SFX+"mk2889.mp3",0.7),0.002,0.15)  # cartoon splat (flop)
slap =fade(load(SFX+"mk2167.mp3",0.5),0.001,0.1)   # slap crack (thappad layer)
stepsrc=load(SFX+"mk543.mp3")
senv=np.abs(stepsrc); k=int(0.01*SR)
senv=np.convolve(senv,np.ones(k)/k,mode="same")
pk=[];i=int(0.1*SR)
while i<len(senv)-int(0.3*SR) and len(pk)<6:
    j=i+int(np.argmax(senv[i:i+int(0.8*SR)]))
    pk.append(j); i=j+int(0.35*SR)
stepcuts=[fade(stepsrc[max(0,j-int(0.02*SR)):j+int(0.20*SR)],0.004,0.08) for j in pk[:4]]
RD=len(riser)/SR
# S1 pad slam = frame0 identity (loop law: same at 24.45)
put(braam,0.00,0.95); put(deep,0.04,0.65); put(hitP,0.00,0.55)
put(wfast,1.20,0.45)
for si,st in enumerate([1.35,1.80,2.25,2.70]): put(stepcuts[si%len(stepcuts)],st,0.5)  # steps ON foot-contact frames
# S1 slam aftermath thud (hook shake needs sound — SFX-on-contact law)
slam0=load(SFX+"mk2113.mp3")[:int(0.9*SR)]
slam0=fade(slam0,0.002,0.45); put(slam0,0.02,0.5)
put(plant,2.92,0.65)                                        # pad plant
put(wair,3.30,0.40)
put(wfast,5.00,0.5)
put(susp,5.05,0.45); put(elec,5.15,0.42)                    # charge menace + electric ignition
put(riser,6.80-RD,0.55)                                     # riser ends ON roar
put(roar,6.78,0.85); put(big,6.80,0.55); put(braam,6.84,0.38)  # REAL ROAR + impact bed
put(pop,6.95,0.42)                                          # caption pop
put(wfast,8.05,0.42)
for hb in [8.15,9.0]: put(heart,hb,0.55)                    # hide beat
for kt in [8.35,8.62,8.9]: put(plant,kt,0.12)               # knee-knock ticks
put(riser,10.80-RD,0.62); put(whist,10.60,0.5)              # riser + launch air-whistle
put(big,10.80,0.9); put(hitP,10.80,0.9); put(slap,10.80,0.5); put(hardP,10.81,0.65); put(deep,10.82,0.75); put(braam,10.84,0.65)  # IMPACT STACK
put(tun,10.95,0.5); put(scream,10.86,0.34); put(metal,11.76,0.55); put(splat,11.76,0.38); put(can,12.06,0.22)  # flight scream + RACK CRASH + splat + rattle
put(pop,11.90,0.42)                                         # 3001. pop
put(wair,12.55,0.3)                                         # pad re-entry
put(fallw,12.48,0.40); put(boing,13.00,0.6); put(thud,13.00,0.3); put(thud,13.28,0.22); put(thud,13.50,0.14)  # BOING bonk+bounces
put(wair,13.80,0.35)
put(wair,14.62,0.22)                                        # smug crossfade
put(deep,15.62,0.55)                                        # banner stamp ON pop-in frame
for st2 in [15.72,16.22,16.68]: put(thud,st2,0.14)          # struggle efforts
put(splat,16.97,0.5); put(wair,16.95,0.32)                  # FLOP to flag-sit
put(wair,18.55,0.28)
put(susp,18.90,0.22)                                        # flag pop
put(wfast,17.95,0.40)
put(braam,20.20,0.5)                                        # punch-in sting
put(pop,21.02,0.4)                                          # ROUND THREE? pop
put(pop,22.00,0.36)
put(braam,22.60,0.6)                                        # eye push braam
put(riser,24.45-RD,0.6)                                     # riser into loop slam
put(braam,24.45,0.95); put(deep,24.49,0.65); put(hitP,24.45,0.55)  # loop slam = frame0 sound
# ---- MUSIC BED: ROop_Loop dark drone (rl03 DNA — NO other channel's music) ----
tt=np.arange(N,dtype=np.float32)/SR
rng=np.random.default_rng(7)
wn=rng.standard_normal(N).astype(np.float32)
br=np.cumsum(wn); br-=np.linspace(br[0],br[-1],N); br/=(np.max(np.abs(br))+1e-9)
y=br.copy()
for _ in range(2):
    out=np.empty_like(y); acc=0.0; k=2*np.pi*110/SR
    kk=k/(k+1)
    out[0]=y[0]*kk
    for i in range(1,N): out[i]=out[i-1]+kk*(y[i]-out[i-1])
    y=out
drone_noise=y/(np.max(np.abs(y))+1e-9)
sub=np.sin(2*np.pi*52*tt)*(0.55+0.45*np.sin(2*np.pi*0.45*tt+1.2))
pad=(np.sin(2*np.pi*98*tt)+0.7*np.sin(2*np.pi*147.3*tt)+0.5*np.sin(2*np.pi*196.5*tt))/2.2
padlfo=0.5+0.5*np.sin(2*np.pi*0.18*tt)
bed=(0.5*drone_noise+0.42*sub+0.20*pad*padlfo).astype(np.float32)
bed/= (np.max(np.abs(bed))+1e-9)
env=np.full(N,0.17,dtype=np.float32)
def duck(t0,t1,v,r=0.15):
    i0,i1=int(t0*SR),int(t1*SR); nr=int(r*SR)
    env[i0:i1]=v
    if i0-nr>0: env[i0-nr:i0]=np.linspace(env[i0-nr-1],v,nr)
    if i1+nr<N: env[i1:i1+nr]=np.linspace(v,0.17,nr)
duck(0.0,1.2,0.12)
duck(2.9,5.0,0.27)        # confidence beat swell
duck(5.0,6.8,0.24)        # charge swell
duck(6.8,8.05,0.08)
duck(9.3,10.45,0.22)      # windup swell
duck(10.45,10.80,0.012,0.25)  # SILENCE WEAPON
duck(10.80,11.6,0.10)
duck(20.0,22.6,0.14)
duck(22.6,24.40,0.20)     # end swell
bed[-int(0.25*SR):]*=np.linspace(1,0,int(0.25*SR))
mix+=bed*env
# ---- MASTER ----
mix.tofile("/var/tmp/rl4f/premix.f32")
subprocess.run([FF,"-nostdin","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","/var/tmp/rl4f/premix.f32",
 "-af","highpass=f=28,acompressor=ratio=2.2:threshold=-18dB:attack=6:release=120:makeup=4dB,alimiter=limit=0.87:level=false",
 "-ar","48000","/var/tmp/rl4f/flm_rl04.wav"],capture_output=True)
raw=subprocess.run([FF,"-nostdin","-v","error","-i","/var/tmp/rl4f/flm_rl04.wav","-f","f32le","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.float32)
rms=20*np.log10(np.sqrt(np.mean(a**2))+1e-9); pk=20*np.log10(np.max(np.abs(a))+1e-9)
print("dur",len(a)/SR,"mean dB",round(rms,1),"peak dB",round(pk,1))
# RMS curve architecture check (Gate 6): dip->spike + no 3s hole < -35dB
w=int(0.25*SR)
curve=[20*np.log10(np.sqrt(np.mean(a[i:i+w]**2))+1e-9) for i in range(0,len(a)-w,w)]
import json
holes=[round(i*0.25,2) for i,c in enumerate(curve) if c<-35]
print("min win dB",round(min(curve),1),"@",curve.index(min(curve))*0.25,"| spike after dip:",round(max(curve[44:48]),1))
print("sub-35 windows:",holes)
