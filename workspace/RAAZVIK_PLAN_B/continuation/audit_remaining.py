from faster_whisper import WhisperModel
from pathlib import Path
import numpy as np,subprocess,imageio_ffmpeg,json
P=Path('/home/user/RAAZVIK_PLAN_B/continuation'); voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';ff=imageio_ffmpeg.get_ffmpeg_exe();model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,num_workers=1);start=324.625
while start<847.2:
 dur=min(60,847.224-start); data=subprocess.run([ff,'-v','error','-ss',str(start),'-i',voice,'-t',str(dur),'-ar','16000','-ac','1','-f','s16le','-'],capture_output=True,check=True).stdout;a=np.frombuffer(data,dtype=np.int16).astype(np.float32)/32768
 seg,_=model.transcribe(a,language='hi',beam_size=5,word_timestamps=True,vad_filter=False);r=[]
 for z in seg:
  v={'start':start+z.start,'end':start+z.end,'text':z.text,'words':[{'start':start+w.start,'end':start+w.end,'word':w.word} for w in z.words]};r.append(v);print(round(v['start'],2),round(v['end'],2),v['text'],flush=True)
 (P/f'audit_{int(start):04}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));start+=dur
