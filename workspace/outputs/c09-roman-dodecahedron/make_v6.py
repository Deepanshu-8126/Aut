from pathlib import Path
p=Path('/home/user/outputs/c09-roman-dodecahedron');s=(p/'refine_v5.py').read_text();s=s[:s.index('def frame(t):')];s=s.replace('fps=30;dur=31.8','fps=30;dur=16.8').replace("'whisper_word_draft.json'","'whisper_v6.json'").replace("words=json.loads((P/'whisper_v6.json').read_text()); groups=[]", "words=json.loads((P/'whisper_v6.json').read_text()); words[6]['word']=' 12-SIDED'; words[6]['end']=words[7]['end']; del words[7]; groups=[]").replace('+0.22','+0.12').replace('+.22','+.12')
s+=r'''
def hook(t):
 im=overlay_black(cover_zoom(imgs['lyon'],t,1.06+0.06*min(t,2)/2,.48,.52),85);d=ImageDraw.Draw(im)
 title(d,'ROMAN',100,52);title(d,'DODECAHEDRON',160,46);title(d,'WHAT WAS IT FOR?',245,37,GOLD)
 source_chip(d,['LYON MUSEUM EXAMPLE  /  CC0'],710)
 return im

def frame(t):
 if t<2.15 or t>=16.35: im=hook(t if t<2.15 else 0)
 elif t<3.75:
  im=overlay_black(cover_zoom(imgs['lyon'],t,1.18+0.10*(t-2.15),.48,.53),40);d=ImageDraw.Draw(im);title(d,'12 SIDES',125,52);source_chip(d,['LYON MUSEUM EXAMPLE / CC0'],710)
 elif t<5.0:
  im=overlay_black(cover_zoom(imgs['lyon'],t,1.38,.47,.55),55);d=ImageDraw.Draw(im);title(d,'HOLES & KNOBS',125,43);source_chip(d,['LYON MUSEUM EXAMPLE / CC0'],710)
 elif t<6.9:
  im=bg(t);im.paste(maps['europe'],(0,110));d=ImageDraw.Draw(im);title(d,'OVER 100 FOUND',130,43);source_chip(d,['EXAMPLES ACROSS EUROPE'],710)
 elif t<8.9:
  im=overlay_black(cover_zoom(imgs['vienne'],t,1.07+0.08*(t-6.9),.5,.5),100);d=ImageDraw.Draw(im);title(d,'PURPOSE',160,45);title(d,'STILL A MYSTERY',218,42,GOLD);source_chip(d,['VIENNE MUSEUM EXAMPLE / CC0'],710)
 elif t<9.75:
  im=overlay_black(cover_zoom(imgs['tongeren'],t,1.14,.47,.5),100);d=ImageDraw.Draw(im);title(d,'A MEASURING TOOL?',160,42);source_chip(d,['THEORY / NOT ESTABLISHED','TONGEREN MUSEUM EXAMPLE'],700)
 elif t<10.62:
  im=overlay_black(cover_zoom(imgs['knitting'],t,1.06,.5,.5),85);d=ImageDraw.Draw(im);title(d,'FOR KNITTING?',130,44);source_chip(d,['AI ILLUSTRATION / THEORY ONLY'],710)
 elif t<11.48:
  im=overlay_black(cover_zoom(imgs['bronze'],t,1.12,.5,.5),100);d=ImageDraw.Draw(im);title(d,'A RITUAL OBJECT?',170,42);source_chip(d,['THEORY / NOT ESTABLISHED','HUNT MUSEUM EXAMPLE / CC0'],700)
 elif t<12.85:
  im=bg(t);im.paste(maps['england'],(0,110));d=ImageDraw.Draw(im);title(d,'ENGLAND / 2023',125,44);source_chip(d,['NORTON DISNEY VILLAGE / APPROX.'],710)
 elif t<14.76:
  im=overlay_black(cover_zoom(imgs['bronze'],t,1.07+.06*(t-12.85),.5,.5),90);d=ImageDraw.Draw(im);title(d,'FOUND INTACT',135,46);source_chip(d,['MUSEUM EXAMPLE','NOT THE 2023 FIND'],700)
 else:
  im=overlay_black(cover_zoom(imgs['vienne'],t,1.12+.05*(t-14.76),.5,.5),135);d=ImageDraw.Draw(im);title(d,'WHAT DO YOU THINK?',190,39);title(d,'WHAT WAS IT FOR?',245,42,GOLD);source_chip(d,['VIENNE MUSEUM EXAMPLE / CC0'],710)
 applycaps(im,t)
 return im.convert('RGB')

checks=[0,.5,1.2,2.4,3.8,5.1,6,7.2,8.3,9.1,9.9,10.8,11.7,13.1,14.9,16.5];sheet=Image.new('RGB',(270*4,500*4),'#101818');sd=ImageDraw.Draw(sheet)
for i,t in enumerate(checks):
 q=frame(t);q.thumbnail((270,480));x=i%4*270;y=i//4*500;sheet.paste(q,(x,y));sd.text((x+5,y+481),str(t),fill='white')
sheet.save(P/'c09_v6_contact.jpg',quality=90)
frame(0).save(P/'v6_hook.png')
if os.environ.get('PROBE')=='1': print('V6 probe ready');raise SystemExit
out=P/'picture_refined_v6.mp4';cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','3',str(out)];enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(round(dur*fps)):
 enc.stdin.write(frame(i/fps).tobytes())
 if i%150==0:print('frame',i,flush=True)
enc.stdin.close();assert enc.wait()==0
print('V6 PICTURE COMPLETE',flush=True)
'''
(p/'refine_v6.py').write_text(s)
