from pathlib import Path
p=Path('/home/user/outputs/fcy-chimera')
new=[0,1.80,4.64,6.68,7.34,7.88,8.22,9.68,10.8,12.24,14.88,16.42,19.18,19.86,20.68,21.55]
old=[0,2.343,6.592,9.339,10.597,13.606,14.98,16.385,17.852,19.736,23.851,25.924,29.262,30.573,31.6,32.85]
s=(p/'test_v3_working.html').read_text()
s=s.replace("cap([['her body runs on ','#fff'],['her brother\\'s','#ff8c5a'],[' blood','#fff']],25,845,L(26.0));", "cap([['her blood cells carry ','#fff'],['her brother\\'s DNA','#ff8c5a']],25,845,L(26.0));")
s=s.replace("cap([['his blood ','#ff8c5a'],['flowed into her veins','#fff']],25,845,L(20.6));", "cap([['his blood ','#ff8c5a'],['flowed into her veins','#fff']],25,845,L(21.6));")
# Suppress outdated 'every other cell' caption before female reveal; keep skin/mouth timed.
s=s.replace("else cap([['OTHER','#4ff0c0'],[' tested cells...','#fff']],32,845,L(11.943));", "else cap([['her ','#fff'],['MOUTH','#4ff0c0'],['...','#fff']],32,845,1);")
anchor='window.renderAt=function(t){\n const T=t;'
warp=f'''window.renderAt=function(t){{
 const nt={new};const ot={old};
 let j=0;while(j<nt.length-2 && t>=nt[j+1])j++;
 t=ot[j]+(ot[j+1]-ot[j])*Math.max(0,Math.min(1,(t-nt[j])/(nt[j+1]-nt[j])));
 const T=t;'''
assert anchor in s;s=s.replace(anchor,warp)
(p/'test_adam.html').write_text(s)
r=(p/'render.py').read_text().replace("OUT='/var/tmp/fcyc'","OUT='/var/tmp/fcyc_adam'").replace('N=986; FPS=30; DUR=32.85','N=647; FPS=30; DUR=21.55').replace('chimera/test.html','chimera/test_adam.html')
(p/'adam/render_adam.py').write_text(r)
# Map legacy effect times to measured new speech; keep their durations rather than changing pitch.
import numpy as np
mix=(p/'mix.py').read_text().replace("D='32.85'","D='21.55'").replace("ins=['-i','vo.wav',", "ins=['-i','/home/user/outputs/fcy-chimera/adam/voice_processed.wav',")
mix=mix.replace("ins=['-i'", f"EV=[(f,float(__import__('numpy').interp(t,{old},{new})),ss,du,vol) for f,t,ss,du,vol in EV]\nins=['-i'",1)
mix=mix.replace('st=32.05:d=0.8','st=20.75:d=0.8').replace('/var/tmp/fcyc_audio.wav','/var/tmp/fcyc_adam_audio.wav')
(p/'adam/mix_adam.py').write_text(mix)
print('created',len(s), 'caption adjusted', 'her blood cells carry' in s)
