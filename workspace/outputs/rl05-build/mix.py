import subprocess, shlex
SFX='/home/user/explainer-pipeline/assets/sfx/'
# (file, start_t, ss, dur, vol, pitch, extra_filter)
EV=[
('mk1287',0.00,0.00,2.2,0.75,1.0,''),
('mk543',1.45,0.30,0.28,0.30,1.0,''),('mk543',1.80,0.30,0.28,0.30,1.0,''),('mk543',2.15,0.30,0.28,0.30,1.0,''),
('mk1143',3.20,0.19,1.2,0.35,0.75,''),
('mk790',4.10,0.92,1.5,0.45,1.0,''),
('mk1972',5.65,0.00,2.2,0.85,0.84,''),
('mk2364',7.05,0.00,0.5,0.35,1.0,''),
('mk1972',8.45,0.00,1.5,0.55,1.0,''),
('mk790',8.80,0.92,1.2,0.40,1.0,''),
('mk2143',10.10,0.00,0.6,0.45,1.0,''),
# IMPACT 1 stack @10.5
('mk788',10.50,0.55,1.1,0.90,1.0,''),('mk2155',10.50,0.00,0.9,0.90,1.0,''),('mk2143',10.50,0.00,0.6,0.65,1.0,''),
('mk1143',10.50,0.19,0.9,0.75,1.0,''),('mk1287',10.50,0.00,1.6,0.65,1.0,''),('mk2167',10.50,0.00,1.0,0.50,1.0,''),
('mk2894',10.56,0.00,1.0,0.50,1.0,''),
('mk391',11.25,0.00,1.1,0.45,1.0,''),
('mk2889',11.75,0.00,1.0,0.60,1.0,''),
('mk2894',11.98,0.00,0.8,0.30,1.2,''),
('mk677',13.07,0.03,0.6,0.45,1.0,''),
('mk2364',13.12,0.00,0.5,0.55,1.0,''),
('mk2143',14.25,0.00,0.8,0.40,0.7,''),
('mk2143',14.75,0.00,0.35,0.20,1.0,'lowpass=f=900,'),('mk2143',15.05,0.00,0.35,0.20,1.0,'lowpass=f=900,'),
('mk790',16.30,0.92,1.6,0.45,1.0,''),
# IMPACT 2 stomp stack @17.9
('mk788',17.90,0.55,1.2,1.00,0.9,''),('mk2155',17.90,0.00,1.0,0.90,0.9,''),
('mk1143',17.90,0.19,1.0,0.85,0.9,''),('mk1287',17.90,0.00,1.8,0.80,0.9,''),
('mk2889',17.90,0.00,1.0,0.80,1.0,''),
('mk1972',19.00,0.00,1.6,0.50,1.12,''),
('mk543',21.40,0.30,0.5,0.40,0.6,''),('mk543',22.05,0.30,0.5,0.33,0.6,''),('mk543',22.70,0.30,0.5,0.25,0.6,''),
('mk2143',23.50,0.00,0.6,0.45,1.0,''),
('mk677',23.85,0.03,0.6,0.45,1.0,''),
('mk790',23.80,0.92,1.2,0.40,1.0,''),
]
ins=['-f','lavfi','-t','25.0','-i','sine=frequency=52:sample_rate=48000',
     '-f','lavfi','-t','25.0','-i','anoisesrc=color=brown:sample_rate=48000:seed=7']
fc=[]
# bed: sine + brown, swells + duck + hard silences
fc.append("[0:a]volume=0.5[sn];[1:a]lowpass=f=110,volume=0.35[bn];[sn][bn]amix=inputs=2:normalize=0,"
 "volume=0.16,"
 "volume=1.9:enable='between(t,2.6,4.0)',volume=1.9:enable='between(t,16.0,17.6)',"
 "volume=0.3:enable='between(t,6.9,7.4)'[bed]")
labels=['[bed]']
for n,(f,t,ss,du,vol,pit,extra) in enumerate(EV):
    idx=len(ins)//2  # not reliable; use explicit counter below
for n,(f,t,ss,du,vol,pit,extra) in enumerate(EV):
    ins+= ['-ss',str(ss),'-t',str(du),'-i',SFX+f+'.mp3']
    i=2+n
    pf=f"asetrate=44100*{pit},aresample=48000," if pit!=1.0 else "aresample=48000,"
    fc.append(f"[{i}:a]{pf}{extra}volume={vol},adelay={int(t*1000)}|{int(t*1000)}[e{n}]")
    labels.append(f"[e{n}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0,"
 "volume=0:enable='between(t,10.20,10.50)',volume=0:enable='between(t,17.60,17.90)',"
 "highpass=f=30,acompressor=ratio=2:threshold=-18dB:attack=5:release=120:makeup=2,"
 "alimiter=limit=0.87:level=false,atrim=0:25.0[out]")
cmd=['ffmpeg','-nostdin','-y']+ins+['-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s16le','/var/tmp/rl05_audio.wav']
print(' '.join(shlex.quote(c) for c in cmd)[:300],'...')
subprocess.run(cmd,check=True,capture_output=True)
print('AUDIO OK')
