from pathlib import Path
import subprocess,re,json,sys
import imageio_ffmpeg
P=Path('/home/user/outputs/c09-roman-dodecahedron');S=Path('/home/user/explainer-pipeline/assets/sfx');ff=imageio_ffmpeg.get_ffmpeg_exe();dur=31.8
# Full-graph mix. Start trims for 788, 1143, 1104, 1489 and 494 measured by silence detect at -35dB.
cues=[('mk788',.566,.70,.03,.18,'poster entrance'),('mk1530',0,.42,2.70,.15,'evidence card'),('mk1143',.194,.72,5.90,.14,'unanswered question'),('mk1104',.06,.38,8.00,.16,'Europe map'),('mk677',0,.24,8.65,.09,'count'),('mk1489',.122,.42,12.80,.10,'first theory'),('mk1489',.122,.42,15.40,.10,'second theory'),('mk1489',.122,.42,16.90,.10,'third theory'),('mk1143',.194,.60,18.78,.13,'not proven'),('mk1104',.06,.38,20.72,.15,'England map'),('mk1530',0,.42,24.50,.13,'context card'),('mk494',.443,2.30,28.00,.085,'final question')]
(P/'SOUND_MAP.json').write_text(json.dumps([dict(file=n,trim=tr,duration=d,time=t,gain=g,event=e) for n,tr,d,t,g,e in cues],indent=2))
cmd=[ff,'-v','error','-y','-i',str(P/'voice_original.wav'),'-i',str(P/'assets/mixkit_871.mp3')]
for n,*_ in cues:cmd+=['-i',str(S/(n+'.mp3'))]
f=[f'[0:a]aresample=48000,adelay=220:all=1,apad,atrim=duration={dur},volume=0.90[voice]',f'[1:a]aresample=48000,atrim=start=6:duration=20,asetpts=PTS-STARTPTS,asplit=2[m1][m2]','[m1][m2]acrossfade=d=2:c1=tri:c2=tri,atrim=duration=31.8,volume=0.12,afade=t=in:st=0:d=0.5,afade=t=out:st=30.3:d=1.5[music]'];ins='[voice][music]'
for i,(n,tr,d,t,g,e) in enumerate(cues):
 f.append(f'[{i+2}:a]aresample=48000,atrim=start={tr}:duration={d},asetpts=PTS-STARTPTS,volume={g},afade=t=out:st={max(0,d-.12)}:d=0.12,adelay={round(t*1000)}:all=1[s{i}]');ins+=f'[s{i}]'
f.append(f'{ins}amix=inputs={len(cues)+2}:duration=first:normalize=0[out]');wav=P/'mix_pre.wav';cmd+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(wav)];subprocess.run(cmd,check=True)
r=subprocess.run([ff,'-hide_banner','-i',str(wav),'-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True);print('\n'.join(z for z in r.stderr.splitlines() if 'mean_volume:' in z or 'max_volume:' in z));m=re.search(r'max_volume: (-?[\d.]+) dB',r.stderr);peak=float(m.group(1));db=min(0,-1.0-peak);print('peak correction dB',db,flush=True)
video=P/'picture_c09.mp4';out=P/'CHRONIC_ROMAN_DODECAHEDRON_REVIEW.mp4';cmd=[ff,'-v','error','-y','-i',str(video),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-af',f'volume={db}dB','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(dur),str(out)];subprocess.run(cmd,check=True);subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],check=True);print('FINAL DECODE OK',out,flush=True)
