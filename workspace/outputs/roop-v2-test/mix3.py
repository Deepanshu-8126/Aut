import subprocess
SFX='/home/user/explainer-pipeline/assets/sfx/'
EV=[
('mk1287', 0.0, 0.0, 2.0, 0.4, 1.0),
('mk2143', 0.991, 0.0, 0.5, 0.28, 1.0),('mk2143', 4.342, 0.0, 0.6, 0.3, 1.0),('mk2364', 13.426, 0.0, 0.5, 0.25, 1.0),('mk1492', 9.722, 0.05, 1.1, 0.25, 1.0),('mk2143', 9.464, 0.0, 0.6, 0.3, 1.0),
('mk2143', 12.235, 0.0, 0.6, 0.3, 1.0),('mk2143', 17.022, 0.0, 0.6, 0.3, 1.0),('mk2143', 21.5, 0.0, 0.6, 0.3, 1.0),
('mk790', 8.352, 0.92, 1.2, 0.28, 1.0),('mk790', 17.926, 0.92, 1.2, 0.28, 1.0),
('mk2364', 0.991, 0.0, 0.5, 0.28, 1.0),('mk2364', 5.296, 0.0, 0.5, 0.28, 1.0),('mk2364', 12.917, 0.0, 0.5, 0.28, 1.0),
('mk2364', 15.565, 0.0, 0.5, 0.3, 1.0),('mk2364', 19.037, 0.0, 0.5, 0.3, 1.0),('mk2364', 9.464, 0.0, 0.5, 0.3, 1.0),
('mk1143', 10.2, 0.0, 0.9, 0.30, 1.0),('mk1143', 14.15, 0.0, 0.9, 0.26, 1.0),('mk494', 17.05, 0.0, 1.85, 0.34, 1.0),
('mk677', 22.028, 0.03, 0.5, 0.28, 1.0),('mk677', 22.972, 0.03, 0.5, 0.28, 1.0),
('mk677', 23.815, 0.03, 0.5, 0.28, 1.0),('mk677', 24.713, 0.03, 0.5, 0.3, 1.0),
]
ins=['-i','vo.wav',
 '-f','lavfi','-t','25.74','-i','sine=frequency=52:sample_rate=48000',
 '-f','lavfi','-t','25.74','-i','anoisesrc=color=brown:sample_rate=48000:seed=5']
fc=["[0:a]atempo=1.08,volume=1.0[vo]",
 "[1:a]volume=0.4[sn];[2:a]lowpass=f=100,volume=0.3[bn];[sn][bn]amix=inputs=2:normalize=0,volume=0.11[bed]"]
labels=['[vo]','[bed]']
for n,(f,t,ss,du,vol,pit) in enumerate(EV):
    ins+=['-ss',str(ss),'-t',str(du),'-i',SFX+f+'.mp3']
    fc.append(f"[{3+n}:a]aresample=48000,volume={vol},adelay={int(t*1000)}|{int(t*1000)}[e{n}]")
    labels.append(f"[e{n}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0,"
 "highpass=f=30,acompressor=ratio=2:threshold=-18dB:attack=5:release=120:makeup=2,"
 "alimiter=limit=0.87:level=false,atrim=0:25.74[out]")
cmd=['ffmpeg','-nostdin','-y']+ins+['-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s16le','/var/tmp/rt_audio3.wav']
subprocess.run(cmd,check=True,capture_output=True)
print('AUDIO OK')
