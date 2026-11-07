from faster_whisper import WhisperModel
import soundfile as sf
import numpy as np,json
p='/home/user/outputs/fcy-chimera/adam/'
a,s=sf.read(p+'voice_raw.wav',dtype='float32')
# resample 24k to 16k
from scipy.signal import resample_poly
a=resample_poly(a,2,3)
m=WhisperModel('small',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
segs,info=m.transcribe(a,language='en',word_timestamps=True,beam_size=3,vad_filter=False)
words=[{'word':w.word.strip(),'start':round(w.start,3),'end':round(w.end,3)} for seg in segs for w in seg.words]
print(json.dumps(words,indent=2));open(p+'words.json','w').write(json.dumps(words,indent=2))
