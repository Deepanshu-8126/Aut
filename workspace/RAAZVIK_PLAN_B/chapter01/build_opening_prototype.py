from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess, imageio_ffmpeg, math
D=Path('/home/user/RAAZVIK_PLAN_B/chapter01'); A=D/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi'; B=D/'assets/nanda_search_images'; W,H=1920,1080
F='/home/user/explainer-pipeline/assets/fonts/'
hi=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',76); his=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',45); inter=ImageFont.truetype(F+'Inter-Bold.ttf',38); tiny=ImageFont.truetype(F+'Inter-Medium.ttf',24); large=ImageFont.truetype(F+'Inter-Black.ttf',112)

def photo(path):return ImageOps.fit(Image.open(path).convert('RGB'),(W,H),Image.Resampling.LANCZOS,centering=(.5,.48)).convert('RGBA')
def grad(img,side='left',alpha=215):
 layer=Image.new('RGBA',(W,H)); pix=layer.load()
 for x in range(W):
  strength=max(0,1-x/(W*.78)) if side=='left' else max(0,(x-W*.35)/(W*.65))
  for y in range(H):pix[x,y]=(7,14,20,int(alpha*strength))
 return Image.alpha_composite(img,layer)
def caption(d,txt,y=1018):d.text((90,y),txt,font=tiny,fill=(242,241,231,235),stroke_width=2,stroke_fill=(0,0,0,150))
def save(img,n):p=D/f'frame_{n}.png';img.convert('RGB').save(p);return p
out=[]
im=grad(photo(A/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg'));d=ImageDraw.Draw(im);d.line((90,164,225,164),fill='#d3ac67',width=5);d.text((90,205),'1965',font=large,fill='#f8f4e9');d.text((94,340),'भारत के हिमालय में',font=hi,fill='white');caption(d,'NANDA DEVI  ·  MODERN PHOTOGRAPH');out.append(save(im,0))
im=grad(photo(B/'site-commons-wikimedia-org-nanda-devi-pe-4.jpg'));d=ImageDraw.Draw(im);d.line((90,190,220,190),fill='#d3ac67',width=5);d.text((90,235),'एक सीक्रेट',font=hi,fill='#f8f4e9');d.text((90,330),'मिशन',font=hi,fill='#f8f4e9');caption(d,'NANDA DEVI  ·  MODERN PHOTOGRAPH');out.append(save(im,1))
im=Image.new('RGBA',(W,H),(19,29,35,255)); bg=ImageOps.fit(Image.open(A/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg').convert('RGB'),(W,H));bg=bg.convert('RGBA');overlay=Image.new('RGBA',(W,H),(9,17,22,200));im=Image.alpha_composite(bg,overlay); portrait=Image.open(A/'cold_war_chapter/assets/kohli_2015.jpg').convert('RGBA');portrait=ImageOps.fit(portrait,(510,675),Image.Resampling.LANCZOS);im.alpha_composite(portrait,(190,190));d=ImageDraw.Draw(im);d.line((790,235,925,235),fill='#d3ac67',width=5);d.text((790,288),'भारतीय और अमेरिकी',font=his,fill='white');d.text((790,365),'climbers',font=inter,fill='#d3ac67');d.text((790,495),'एम. एस. कोहली',font=his,fill='white');d.text((790,560),'2015 PHOTOGRAPH',font=tiny,fill='#bfc5c2');caption(d,'PMO / PIB  ·  M. S. KOHLI, PHOTOGRAPHED IN 2015');out.append(save(im,2))
im=grad(photo(A/'cold_war_chapter/assets/nepal_porters_1997_john_pavelka.jpg'),side='right',alpha=170);d=ImageDraw.Draw(im);d.text((1030,285),'शेरपा और',font=his,fill='white',stroke_width=2,stroke_fill='black');d.text((1030,355),'स्थानीय सहयोगी',font=his,fill='white',stroke_width=2,stroke_fill='black');caption(d,'ILLUSTRATIVE PHOTO  ·  NEPAL, 1997  ·  NOT THE 1965 TEAM');out.append(save(im,3))
ff=imageio_ffmpeg.get_ffmpeg_exe();parts=[]
for i,(path,frames) in enumerate(zip(out,[77,67,72,120])):
 target=D/f'test_part_{i}.mp4';parts.append(target)
 vf="zoompan=z='min(zoom+0.00012,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24,format=yuv420p"
 cmd=[ff,'-v','error','-y','-loop','1','-framerate','24','-i',str(path),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-r','24',str(target)]
 subprocess.run(cmd,check=True); print('SHOT',i,'done',flush=True)
(D/'parts.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts))
silent=D/'prototype_picture.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(D/'parts.txt'),'-c','copy',str(silent)],check=True)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';final=D/'CHAPTER01_STYLE_TEST_NOT_FINAL.mp4'
subprocess.run([ff,'-v','error','-y','-i',str(silent),'-i',voice,'-map','0:v:0','-map','1:a:0','-t','14','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)],check=True)
print('DONE',final,flush=True)
