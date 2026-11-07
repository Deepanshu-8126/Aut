import os,subprocess,json,shutil,hashlib
from pathlib import Path
P=Path('/home/user/RAAZVIK_PLAN_B/continuation/kaggle_parts_v3');O=Path('/home/user/RAAZVIK_PLAN_B/continuation/workprint_v3'); O.mkdir(exist_ok=True); import imageio_ffmpeg; ff=imageio_ffmpeg.get_ffmpeg_exe()
assert ff, 'ffmpeg unavailable'
files=[P/f'part_{i:02}.mp4' for i in range(1,12)]; dur=[74,41.625,21.25,32.75,30.5,40,36.75,47.75,109,217,196.625]; assert all(p.exists() for p in files)
L=O/'concat.txt';L.write_text('ffconcat version 1.0\n'+''.join("file '%s'\nduration %.6f\n"%(p,d) for p,d in zip(files,dur)))
def run(a): print('RUN',a[:8],flush=True);subprocess.run(a,check=True)
video=O/'picture_only.mp4';run([ff,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(L),'-map','0:v:0','-c:v','copy','-an',str(video)])
args=[ff,'-hide_banner','-loglevel','error','-y','-i',str(video)]
for p in files:args+=['-i',str(p)]
f=[]
for i,d in enumerate(dur,1):
 n=round(d*48000);f.append(f'[{i}:a:0]aresample=48000,apad,atrim=end_sample={n},asetpts=PTS-STARTPTS[a{i}]')
f.append(''.join(f'[a{i}]' for i in range(1,12))+'concat=n=11:v=0:a=1[a]')
full=O/'RAAZVIK_FULL_HD_WORKPRINT_NOT_FINAL.mp4';args+=['-filter_complex',';'.join(f),'-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t','847.25','-movflags','+faststart',str(full)];run(args)
mobile=O/'RAAZVIK_FULL_MOBILE_WORKPRINT_NOT_FINAL.mp4';run([ff,'-hide_banner','-loglevel','error','-y','-i',str(full),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','28','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mobile)])
for p in [full,mobile]:
 run([ff,'-hide_banner','-loglevel','error','-i',str(p),'-f','null','-']);h=hashlib.sha256(p.read_bytes()).hexdigest();print('QC',p.name,p.stat().st_size,h,flush=True)
(O/'WORKPRINT_WARNING.txt').write_text('INTERNAL REVIEW V3 ONLY — not approved or release-ready. The Week article date has conflicting machine transcriptions of voice and needs human ear verification. Authentic 1978 newspaper clipping is rights-blocked. AI and modern stock are illustrative. Later visual sync and source/rights verification remain pending.\n')
video.unlink();print('COMPLETE',flush=True)
