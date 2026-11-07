import subprocess
SFX='/home/user/explainer-pipeline/assets/sfx/'
D='21.55'
# (file, at, ss, dur, vol)
EV=[
('mk1287', 0.0,   0.0, 2.2, 0.42),                      # braam hook
('mk2364', 2.343, 0.0, 0.5, 0.28),                      # cut: lab
('mk2143', 3.2,   0.0, 0.6, 0.22),('mk2143', 4.6, 0.0, 0.6, 0.24),  # ticks lab
('mk790',  5.55,  0.92, 1.15, 0.34),                    # riser into XY
('mk1143', 6.60,  0.0, 0.9, 0.55),                      # IMPACT XY reveal
('mk677',  6.95,  0.03, 0.5, 0.30),                     # stamp 46,XY
('mk2364', 9.339, 0.0, 0.5, 0.28),                      # cut: body
('mk677', 10.597, 0.03, 0.5, 0.20),('mk677', 11.943, 0.03, 0.5, 0.20), # caption ticks
('mk2364',13.606, 0.0, 0.5, 0.28),                      # cut: XX
('mk1143',14.98,  0.0, 0.9, 0.38),('mk677', 15.10, 0.03, 0.5, 0.26),  # stamp 46,XX
('mk2364',16.385, 0.0, 0.5, 0.26),                      # cut: retest
('mk677', 17.852, 0.03, 0.5, 0.26),                     # "not wrong"
('mk790', 18.95,  0.92, 1.15, 0.30),                    # riser into womb
('mk2364',19.736, 0.0, 0.5, 0.28),                      # cut: womb
('mk494', 19.9,   0.0, 1.85, 0.30),('mk494', 21.85, 0.0, 1.85, 0.30),('mk494', 23.8, 0.0, 1.85, 0.26), # heartbeat womb
('mk1143',23.95,  0.0, 0.9, 0.55),                      # IMPACT never left
('mk2364',25.924, 0.0, 0.5, 0.28),                      # cut: body today
('mk2364',29.262, 0.0, 0.5, 0.28),                      # cut: payoff
('mk1143',29.30,  0.0, 0.9, 0.40),                      # ONE BODY
('mk677', 30.62,  0.03, 0.5, 0.30),                     # TWO DNA
('mk2364',31.95,  0.0, 0.5, 0.20),                      # loop whoosh-back
]
EV=[(f,float(__import__('numpy').interp(t,[0, 2.343, 6.592, 9.339, 10.597, 13.606, 14.98, 16.385, 17.852, 19.736, 23.851, 25.924, 29.262, 30.573, 31.6, 32.85],[0, 1.8, 4.64, 6.68, 7.34, 7.88, 8.22, 9.68, 10.8, 12.24, 14.88, 16.42, 19.18, 19.86, 20.68, 21.55])),ss,du,vol) for f,t,ss,du,vol in EV]
ins=['-i','/home/user/outputs/fcy-chimera/adam/voice_processed.wav',
 '-f','lavfi','-t',D,'-i','sine=frequency=52:sample_rate=48000',
 '-f','lavfi','-t',D,'-i','anoisesrc=color=brown:sample_rate=48000:seed=11']
fc=["[0:a]volume=1.0[vo]",
 "[1:a]volume=0.4[sn];[2:a]lowpass=f=100,volume=0.3[bn];[sn][bn]amix=inputs=2:normalize=0,"
 "volume=0.11,afade=t=in:d=0.5,afade=t=out:st=20.75:d=0.8[bed]"]
labels=['[vo]','[bed]']
for n,(f,t,ss,du,vol) in enumerate(EV):
    ins+=['-ss',str(ss),'-t',str(du),'-i',SFX+f+'.mp3']
    fc.append(f"[{3+n}:a]aresample=48000,volume={vol},adelay={int(t*1000)}|{int(t*1000)}[e{n}]")
    labels.append(f"[e{n}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0,"
 "highpass=f=30,acompressor=ratio=2:threshold=-18dB:attack=5:release=120:makeup=2,"
 f"alimiter=limit=0.87:level=false,atrim=0:{D}[out]")
cmd=['ffmpeg','-nostdin','-y']+ins+['-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s16le','/var/tmp/fcyc_adam_audio.wav']
subprocess.run(cmd,check=True,capture_output=True)
print('AUDIO OK')
