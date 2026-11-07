import subprocess,json,re
from pathlib import Path
P=Path('/home/user/outputs/fcy-fingers');S=Path('/home/user/explainer-pipeline/assets/sfx');F='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg';D=25.6
cues=[('mk788',.56,.32,.0,.04,'hook'),('mk1492',0,.25,1.35,.035,'finger close-up'),('mk677',0,.20,5.80,.04,'nerve signal'),('mk1489',.12,.3,8.95,.035,'vessel narrows'),('mk1492',0,.25,12.20,.035,'folds form'),('mk677',0,.20,14.35,.03,'grip study'),('mk677',0,.20,16.70,.015,'grip contact'),('mk1489',.12,.3,19.00,.03,'return to character')]
(P/'SOUND_MAP.json').write_text(json.dumps([dict(file=a,trim=b,duration=c,time=d,gain=e,event=f) for a,b,c,d,e,f in cues],indent=2))
subprocess.run([F,'-v','error','-y','-i',str(P/'assets/music_464.mp3'),'-af',f'atrim=start=12:duration={D},asetpts=PTS-STARTPTS,volume=0.07,aresample=48000,afade=t=in:st=0:d=0.4,afade=t=out:st=24.8:d=0.8','-c:a','pcm_s24le',str(P/'bed.wav')],check=True)
cmd=[F,'-v','error','-y','-i',str(P/'voice_paced.wav'),'-i',str(P/'bed.wav')];fc=[f'[0:a]aresample=48000,adelay=120:all=1,apad,atrim=duration={D},volume=.9[vo]','[1:a]aresample=48000[music]'];ins='[vo][music]'
for i,(name,tr,du,t,v,_) in enumerate(cues):
 cmd+=['-i',str(S/(name+'.mp3'))];fc.append(f'[{i+2}:a]aresample=48000,atrim=start={tr}:duration={du},asetpts=PTS-STARTPTS,volume={v},afade=t=out:st={max(0,du-.06)}:d=0.06,adelay={round(t*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
fc.append(f'{ins}amix=inputs={len(cues)+2}:duration=first:normalize=0[out]');cmd+=['-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s24le',str(P/'mix.wav')];subprocess.run(cmd,check=True)
r=subprocess.run([F,'-hide_banner','-i',str(P/'mix.wav'),'-af','loudnorm=I=-16:TP=-1.8:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);a=json.loads(re.search(r'\{\s*"input_i".*?\}',r.stderr,re.S).group());print(a,flush=True)
flt=f"loudnorm=I=-16:TP=-1.8:LRA=11:measured_I={a['input_i']}:measured_TP={a['input_tp']}:measured_LRA={a['input_lra']}:measured_thresh={a['input_thresh']}:offset={a['target_offset']}:linear=false,aresample=48000,volume=-0.4dB"
subprocess.run([F,'-v','error','-y','-i',str(P/'mix.wav'),'-af',flt,'-c:a','pcm_s24le',str(P/'audio_master.wav')],check=True);print('Audio built')
