from pathlib import Path
import subprocess,json,re
P=Path('/home/user/outputs/c09-roman-dodecahedron');F='/usr/local/lib/python3.13/site-packages/static_ffmpeg/bin/linux/ffmpeg';S=Path('/home/user/explainer-pipeline/assets/sfx');D=31.8
cues=json.loads((P/'SOUND_MAP_V3.json').read_text())
for c in cues:
 if c['file']=='mk1143':c['gain']=0.065
# Prepare one continuous intro-loop bed first; this avoids the observed missing bed from 21–28 seconds in V3.
cmd=[F,'-v','error','-y','-i',str(P/'assets/mixkit_871.mp3'),'-i',str(P/'assets/mixkit_871.mp3'),'-filter_complex',f'[0:a]atrim=start=6:duration=20,asetpts=PTS-STARTPTS[a];[1:a]atrim=start=6:duration=20,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=2:c1=tri:c2=tri,atrim=duration={D},aresample=48000,volume=0.12,afade=t=in:st=0:d=0.5,afade=t=out:st=30.3:d=1.5[out]','-map','[out]','-c:a','pcm_s24le',str(P/'music_bed_v4.wav')];subprocess.run(cmd,check=True)
cmd=[F,'-v','error','-y','-i',str(P/'voice_original.wav'),'-i',str(P/'music_bed_v4.wav')]
for c in cues:cmd+=['-i',str(S/(c['file']+'.mp3'))]
f=[f'[0:a]aresample=48000,adelay=220:all=1,apad,atrim=duration={D},volume=0.90[voice]','[1:a]aresample=48000,asetpts=PTS-STARTPTS[music]'];ins='[voice][music]'
for i,c in enumerate(cues):
 tr,d,t,g=(c[x] for x in ['trim','duration','time','gain']);f.append(f'[{i+2}:a]aresample=48000,atrim=start={tr}:duration={d},asetpts=PTS-STARTPTS,volume={g},afade=t=out:st={max(0,d-.12)}:d=0.12,adelay={round(t*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+2}:duration=first:normalize=0[out]');cmd+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(P/'mix_v4_pre.wav')];subprocess.run(cmd,check=True);(P/'SOUND_MAP_V4.json').write_text(json.dumps(cues,indent=2))
r=subprocess.run([F,'-hide_banner','-i',str(P/'mix_v4_pre.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=re.search(r'\{\s*"input_i".*?\}',r.stderr,re.S);a=json.loads(m.group());print('Input loudness:',a,flush=True)
flt=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={a['input_i']}:measured_TP={a['input_tp']}:measured_LRA={a['input_lra']}:measured_thresh={a['input_thresh']}:offset={a['target_offset']}:linear=false,aresample=48000"
subprocess.run([F,'-v','error','-y','-i',str(P/'mix_v4_pre.wav'),'-af',flt,'-c:a','pcm_s24le',str(P/'mastered_v4.wav')],check=True);print('V4 master audio ready',flush=True)
