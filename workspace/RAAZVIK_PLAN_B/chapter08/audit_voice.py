from faster_whisper import WhisperModel
import numpy as np,wave,json
p='/home/user/RAAZVIK_PLAN_B/chapter08/'
with wave.open(p+'voice_chunk.wav','rb') as w: a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,num_workers=1)
s,info=m.transcribe(a,language='hi',beam_size=5,word_timestamps=True,vad_filter=False)
r=[]
for z in s:
 v={'start':z.start,'end':z.end,'text':z.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in z.words]};r.append(v);print(v['start'],v['end'],v['text'],flush=True)
open(p+'voice_audit_machine.json','w').write(json.dumps(r,ensure_ascii=False,indent=2))
