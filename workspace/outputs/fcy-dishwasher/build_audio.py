from pathlib import Path
import subprocess,json,re
P=Path('/home/user/outputs/fcy-dishwasher');S=Path('/home/user/explainer-pipeline/assets/sfx');F='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg';D=32.0
cues=[('mk788',.566,.45,0,.075,'hook clean impact'),('mk1492',0,.25,4.96,.05,'schematic change'),('mk677',0,.2,7.12,.05,'heat'),('mk1489',.122,.35,9.54,.065,'pump cut'),('mk677',0,.2,11.68,.04,'arm feed'),('mk1489',.122,.35,13.18,.06,'jet close-up'),('mk677',0,.22,15.99,.05,'spin reaction'),('mk1492',0,.25,17.82,.05,'spray'),('mk1489',.122,.35,19.94,.05,'filter'),('mk677',0,.2,21.70,.05,'filter'),('mk1492',0,.25,24.40,.05,'drain'),('mk677',0,.2,27.24,.05,'fresh rinse'),('mk1489',.122,.35,29.48,.05,'loop')]
cues += [('mk1492',0,.20,6.15,.025,'water detail insert'),('mk1492',0,.20,3.70,.035,'plate close-up'),('mk1489',.122,.25,7.25,.035,'water detail'),('mk1492',0,.20,11.50,.035,'spray-arm insert'),('mk1489',.122,.25,14.40,.018,'jet detail'),('mk1492',0,.20,22.52,.035,'recirculation') ]
(P/'SOUND_MAP_V3.json').write_text(json.dumps([dict(file=a,trim=b,duration=c,time=d,gain=e,event=f) for a,b,c,d,e,f in cues],indent=2))
subprocess.run([F,'-v','error','-y','-i',str(P/'assets/music_464.mp3'),'-af',f'atrim=start=12:duration={D},asetpts=PTS-STARTPTS,volume=0.075,aresample=48000,afade=t=in:st=0:d=0.4,afade=t=out:st=31.2:d=0.8','-c:a','pcm_s24le',str(P/'bed_v3.wav')],check=True)
cmd=[F,'-v','error','-y','-i',str(P/'voice_master.wav'),'-i',str(P/'bed_v3.wav')]
for a,*_ in cues:cmd+=['-i',str(S/(a+'.mp3'))]
f=[f'[0:a]aresample=48000,adelay=120:all=1,apad,atrim=duration={D},volume=.9[voice]','[1:a]aresample=48000[music]'];inputs='[voice][music]'
for i,(a,tr,d,t,g,_) in enumerate(cues):
 f.append(f'[{i+2}:a]aresample=48000,atrim=start={tr}:duration={d},asetpts=PTS-STARTPTS,volume={g},afade=t=out:st={max(0,d-.06)}:d=0.06,adelay={round(t*1000)}:all=1[s{i}]');inputs+=f'[s{i}]'
f.append(f'{inputs}amix=inputs={len(cues)+2}:duration=first:normalize=0[out]');cmd+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(P/'mix_pre_v3.wav')];subprocess.run(cmd,check=True)
r=subprocess.run([F,'-hide_banner','-i',str(P/'mix_pre_v3.wav'),'-af','loudnorm=I=-16:TP=-1.8:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);a=json.loads(re.search(r'\{\s*"input_i".*?\}',r.stderr,re.S).group());print(a,flush=True)
flt=f"loudnorm=I=-16:TP=-1.8:LRA=11:measured_I={a['input_i']}:measured_TP={a['input_tp']}:measured_LRA={a['input_lra']}:measured_thresh={a['input_thresh']}:offset={a['target_offset']}:linear=false,aresample=48000,volume=-0.4dB"
subprocess.run([F,'-v','error','-y','-i',str(P/'mix_pre_v3.wav'),'-af',flt,'-c:a','pcm_s24le',str(P/'master_audio_v3.wav')],check=True);print('audio complete')
