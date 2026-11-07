#!/usr/bin/env python3
"""Chapter 1 review: clean rebuild of affected shots, short Hindi source IDs, SFX. Not a final QC pass."""
from pathlib import Path
import subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01'); O=P/'heading_sound_work';O.mkdir(exist_ok=True)
A=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi'; B=P/'assets/nanda_search_images';ff=imageio_ffmpeg.get_ffmpeg_exe();src=P/'RAAZVIK_CHAPTER01_VISUAL_EXPLAINER_REVIEW.mp4';F='/home/user/explainer-pipeline/assets/fonts/';W,H=1920,1080
h1=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',66);h2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',45);h3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',32)

def text(d,xy,s,font,fill='#f6f3ed',stroke=0): d.text(xy,s,font=font,fill=fill,stroke_width=stroke,stroke_fill='#081318')
def bg(path,brightness=.7):return ImageEnhance.Brightness(ImageOps.fit(Image.open(path).convert('RGB'),(W,H),Image.Resampling.LANCZOS)).enhance(brightness).convert('RGBA')
def write(im,name):im.convert('RGB').save(O/name,quality=95)
# The 1997 Nepal photograph is explicitly illustrative, never labelled as the expedition's people.
im=bg(P/'assets/nasa_blue_marble_himalaya.jpg',.22);port=Image.open(A/'cold_war_chapter/assets/nepal_porters_1997_john_pavelka.jpg').convert('RGB');port.thumbnail((1030,725),Image.Resampling.LANCZOS);im.alpha_composite(port.convert('RGBA'),(100,(H-port.height)//2));d=ImageDraw.Draw(im);text(d,(1210,355),'शेरपा और',h1);text(d,(1210,450),'पोर्टर्स',h1,fill='#efcb92');d.line((1214,560,1440,560),fill='#dfb274',width=5);write(im,'support.jpg')
write(bg(B/'site-commons-wikimedia-org-nanda-devi-pe-4.jpg',.82),'peak.jpg')
write(bg(B/'site-commons-wikimedia-org-nanda-devi-fi-4.jpg',.72),'closing.jpg')
write(bg(P/'assets/nasa_rtgs_msl_2011.jpg',.83),'nasa_rtg.jpg')
# Authentic US State Department website transcription, presented as such, not a scan/newspaper.
im=bg(P/'assets/nasa_blue_marble_himalaya.jpg',.18);d=ImageDraw.Draw(im);text(d,(95,105),'1978 का अमेरिकी',h1);text(d,(95,195),'सरकारी रिकॉर्ड',h1,fill='#ebc58e');text(d,(100,305),'वेबसाइट पर लिखा हुआ टेक्स्ट',h3);doc=Image.open(A/'visual_upgrade/FRUS_1978_official_page_capture.png').convert('RGB').crop((0,0,1232,535));doc.thumbnail((1250,545),Image.Resampling.LANCZOS);im.alpha_composite(doc.convert('RGBA'),(405,422));write(im,'evidence.jpg')
# Clear source/context captions, not microscopic English. They remain on-screen only for relevant shots.
labels=[(0,3.208,'सांकेतिक दृश्य • पंचाचूली'),(3.208,6,'आधुनिक सैटेलाइट तस्वीर'),(6,9,'कोहली की तस्वीर • 2015'),(9,14,'सांकेतिक तस्वीर • नेपाल, 1997'),(14,18,'नंदा देवी • आधुनिक तस्वीर'),(18,24,'आधुनिक सैटेलाइट तस्वीर'),(24,27,'NASA का RTG • अलग मॉडल, 2011'),(27,33,'RTG का चित्र • अलग मॉडल'),(33,39,'सांकेतिक दृश्य • 1965 की फुटेज नहीं'),(39,42,'सांकेतिक दृश्य • असली टीम नहीं'),(42,48,'आधुनिक तस्वीर • अमेरिकन अल्पाइन क्लब का विवरण'),(54.25,60.583,'2026 की रिपोर्ट • प्रतिभागी का दावा'),(64.583,74,'नंदा देवी • आधुनिक तस्वीर')]
for i,(_,_,s) in enumerate(labels):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im); box=d.textbbox((0,0),s,font=h3,stroke_width=2);tw=box[2]-box[0];d.rounded_rectangle((55,1003,90+tw,1060),radius=8,fill=(8,20,25,195));text(d,(73,1007),s,h3,stroke=1);im.save(O/f'label{i}.png')

def run(c):subprocess.run([str(x) for x in c],check=True)
def old(a,b,name):
 # Remove the previous tiny English bottom strip by a clean reframing of the whole image, not blur.
 run([ff,'-v','error','-y','-ss',str(a/24),'-i',src,'-vf','fps=24,crop=1920:1000:0:0,scale=1920:1080','-frames:v',str(b-a),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',O/(name+'.mp4')])
def still(name,n):
 run([ff,'-v','error','-y','-loop','1','-framerate','24','-i',O/(name+'.jpg'),'-vf',"zoompan=z='min(zoom+0.00010,1.025)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24",'-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',O/(name+'.mp4')])
def map2():
 base=Image.open(P/'assets/nasa_blue_marble_himalaya.jpg').convert('RGB');px=(79.97012-70)/25*W;py=(38.0625-30.37608)/14.0625*H
 enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-frames:v','144','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(O/'map2.mp4')],stdin=subprocess.PIPE)
 for i in range(144):
  t=i/24;z=1+.04*min(t/6,1);cw=int(W/z);ch=int(H/z);x=max(0,min(W-cw,int(W/2-cw/2+(px-W/2)*.12)));y=max(0,min(H-ch,int(H/2-ch/2+(py-H/2)*.12)))
  im=base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA');im=Image.alpha_composite(im,Image.new('RGBA',(W,H),(8,15,19,65)));d=ImageDraw.Draw(im);mx=(px-x)*W/cw;my=(py-y)*H/ch;d.ellipse((mx-11,my-11,mx+11,my+11),fill='#ffca80');d.ellipse((mx-32,my-32,mx+32,my+32),outline='#ffca80',width=4);text(d,(mx+45,my-67),'नंदा देवी',h3,stroke=2)
  text(d,(80,110),'प्लान क्या था?' if t<3 else 'चीन के मिसाइल सिग्नल',h1,stroke=2)
  if t>=3:
   text(d,(83,215),'सुनने की कोशिश',h2,fill='#eecb98',stroke=2)
   for k in range(2):
    a=(t-3+k*.65)%1.7;r=44+a*85;d.arc((mx-r,my-r,mx+r,my+r),-60,80,fill='#eab26b',width=4)
  enc.stdin.write(im.convert('RGB').tobytes())
 enc.stdin.close();assert enc.wait()==0
def weather(src,n,name):
 run([ff,'-v','error','-y','-i',src,'-vf','fps=24,tpad=stop_mode=clone:stop_duration=1,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',O/(name+'.mp4')])
if True:
 old(0,216,'old0');still('support',120);still('peak',96);map2();still('nasa_rtg',72);old(648,792,'old27');weather(P/'pexels_weather_11686252.mp4',72,'storm1');weather(P/'pexels_weather_11279478.mp4',72,'storm2');old(936,1152,'old39');still('evidence',150);old(1302,1550,'old54');still('closing',226)
 
names=['old0','support','peak','map2','nasa_rtg','old27','storm1','storm2','old39','evidence','old54','closing'];(O/'concat.txt').write_text(''.join("file '"+str(O/(x+'.mp4'))+"'\n" for x in names));run([ff,'-v','error','-y','-f','concat','-safe','0','-i',O/'concat.txt','-c','copy',O/'picture_unlabelled.mp4'])
# One libass subtitle stream avoids the memory cost of twelve simultaneous 1080p overlays.
def ts(t):
 c=round(t*100);h=c//360000;m=(c//6000)%60;sec=(c//100)%60;return f'{h}:{m:02d}:{sec:02d}.{c%100:02d}'
ass='[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Label,Noto Sans Devanagari,42,&H00F5F3ED,&H00FFFFFF,&H00131908,&HAA101A08,-1,0,0,0,100,100,0,0,3,4,0,1,70,70,36,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
for a,b,s in labels: ass+=f'Dialogue: 0,{ts(a)},{ts(b)},Label,,0,0,0,,{s}\n'
(O/'captions.ass').write_text(ass)
if True:
 run([ff,'-v','error','-y','-i',O/'picture_unlabelled.mp4','-vf',f"ass={O/'captions.ass'}:fontsdir={F}",'-frames:v','1776','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',O/'picture.mp4'])
print('PICTURE COMPLETE',flush=True)
# Original master VO at unity; selected one-shots are quiet. Avoid gain normalization and double layers.
voice=Path('/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3');S=Path('/home/user/explainer-pipeline/assets/sfx')
cues=[('mk1489',.12,1.45,3.208,.10),('mk1430',.10,.40,9,.10),('mk1489',.12,1.45,18,.09),('mk1157',.32,8,33,.085),('mk1530',0,.5,48,.09),('mk1104',0,.38,54.25,.08)]
cmd=[ff,'-v','error','-y','-i',O/'picture.mp4','-i',voice]
for name,_,_,_,_ in cues:cmd+=['-i',S/(name+'.mp3')]
filters=['[1:a]atrim=0:74,asetpts=PTS-STARTPTS,aresample=48000[vo]'];ins='[vo]'
for j,(name,trim,dur,at,gain) in enumerate(cues):
 fade=f',afade=t=in:st=0:d=1,afade=t=out:st={dur-1}:d=1' if name=='mk1157' else ',afade=t=out:st='+str(max(0,dur-.15))+':d=0.15'
 filters.append(f'[{j+2}:a]atrim=start={trim}:duration={dur},asetpts=PTS-STARTPTS,aresample=48000,volume={gain}{fade},adelay={int(at*1000)}:all=1[s{j}]');ins+=f'[s{j}]'
filters.append(f'{ins}amix=inputs={len(cues)+1}:duration=first:normalize=0,alimiter=limit=0.96:level=0[mix]')
out=P/'RAAZVIK_CHAPTER01_REAL_PHOTO_SOUND_REVIEW.mp4';cmd+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[mix]','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out];run(cmd);print('DONE',out,flush=True)
