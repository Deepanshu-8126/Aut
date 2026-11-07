from pathlib import Path
import subprocess,imageio_ffmpeg
P=Path('/home/user/outputs/fcy-ears');S=Path('/home/user/explainer-pipeline/assets/sfx');ff=imageio_ffmpeg.get_ffmpeg_exe();D=35.4
cues=[('mk788',0.0,.10,.14),('mk1489',6.85,.07,.25),('mk1489',10.6,.045,.24),('mk1492',16.2,.05,.22),('mk677',22.7,.025,.16),('mk1489',28.9,.035,.22),('mk677',32.9,.045,.22)]
cmd=[ff,'-v','error','-y','-i',str(P/'voice_final.wav'),'-stream_loop','-1','-ss','12','-i','/home/user/outputs/fcy-fingers/assets/music_464.mp3'];filters=[f'[0:a]aresample=48000,adelay=120:all=1,apad,atrim=duration={D},volume=0.95[v]',f'[1:a]atrim=duration={D},asetpts=PTS-STARTPTS,aresample=48000,volume=0.06,afade=t=in:st=0:d=0.4,afade=t=out:st=34.4:d=1[m]'];mix='[v][m]'
for i,(n,t,vol,dur) in enumerate(cues):
 cmd+=['-i',str(S/(n+'.mp3'))];filters.append(f'[{i+2}:a]aresample=48000,atrim=duration={dur},asetpts=PTS-STARTPTS,volume={vol},afade=t=out:st={max(0,dur-.05)}:d=0.05,adelay={int(t*1000)}:all=1[s{i}]');mix+=f'[s{i}]'
filters.append(f'{mix}amix=inputs={len(cues)+2}:duration=first:normalize=0,alimiter=limit=0.85:level=0,volume=0.94[out]');cmd+=['-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s24le',str(P/'audio_mix.wav')];subprocess.run(cmd,check=True)
r=subprocess.run([ff,'-hide_banner','-i',str(P/'audio_mix.wav'),'-filter_complex','ebur128=peak=true','-f','null','-'],capture_output=True,text=True);print(r.stderr[-500:]);(P/'audio_measure.log').write_text(r.stderr)
