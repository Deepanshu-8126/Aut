from pathlib import Path
import subprocess,json,re
P=Path('/home/user/outputs/c09-roman-dodecahedron');F='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg';S=Path('/home/user/explainer-pipeline/assets/sfx');D=16.8
old=json.loads((P/'SOUND_MAP_V4.json').read_text()); indexes=[0,2,4,3,6,7,8,10,11,13]; times=[0,3.75,5.0,6.9,8.9,9.75,10.62,11.48,12.85,14.76];cues=[]
for i,t in zip(indexes,times):
 c=old[i].copy();c['time']=t;c['gain']=min(c['gain'],.04 if c['file'] in ('mk1143','mk494') else .09);c['event']=['hook','detail','Europe map','unknown','measuring theory','knitting theory','ritual theory','England map','museum example, not the find','final question'][len(cues)];cues.append(c)
(P/'SOUND_MAP_V6.json').write_text(json.dumps(cues,indent=2))
cmd=[F,'-v','error','-y','-i',str(P/'assets/mixkit_871.mp3'),'-af',f'atrim=start=6:duration={D},asetpts=PTS-STARTPTS,aresample=48000,volume=0.12,afade=t=in:st=0:d=0.4,afade=t=out:st=15.8:d=1', '-c:a','pcm_s24le',str(P/'music_bed_v6.wav')];subprocess.run(cmd,check=True)
cmd=[F,'-v','error','-y','-i',str(P/'voice_v6_short.wav'),'-i',str(P/'music_bed_v6.wav')]
for c in cues:cmd+=['-i',str(S/(c['file']+'.mp3'))]
f=[f'[0:a]aresample=48000,adelay=120:all=1,apad,atrim=duration={D},volume=0.90[voice]','[1:a]aresample=48000,asetpts=PTS-STARTPTS[music]'];ins='[voice][music]'
for i,c in enumerate(cues):
 tr,d,t,g=(c[x] for x in ['trim','duration','time','gain']);f.append(f'[{i+2}:a]aresample=48000,atrim=start={tr}:duration={d},asetpts=PTS-STARTPTS,volume={g},afade=t=out:st={max(0,d-.12)}:d=0.12,adelay={round(t*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+2}:duration=first:normalize=0[out]');cmd+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(P/'mix_v6_pre.wav')];subprocess.run(cmd,check=True)
r=subprocess.run([F,'-hide_banner','-i',str(P/'mix_v6_pre.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);a=json.loads(re.search(r'\{\s*"input_i".*?\}',r.stderr,re.S).group());print('Loudness input',a,flush=True)
flt=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={a['input_i']}:measured_TP={a['input_tp']}:measured_LRA={a['input_lra']}:measured_thresh={a['input_thresh']}:offset={a['target_offset']}:linear=false,aresample=48000"
subprocess.run([F,'-v','error','-y','-i',str(P/'mix_v6_pre.wav'),'-af',flt,'-c:a','pcm_s24le',str(P/'mastered_v6.wav')],check=True);print('V6 master audio ready',flush=True)
