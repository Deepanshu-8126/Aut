from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess, math, imageio_ffmpeg, numpy as np
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01');O=P/'working_full_chapter'; ff=imageio_ffmpeg.get_ffmpeg_exe(); W,H=1920,1080
A=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi';G=P/'assets/nanda_search_images'; F='/home/user/explainer-pipeline/assets/fonts/'
h1=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',72); h2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',48); h3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',34); sm=ImageFont.truetype(F+'Inter-Medium.ttf',24)

def easing(x):
 x=min(1,max(0,x));return x*x*(3-2*x)
def alphacol(rgb,a):return tuple(rgb)+(int(max(0,min(255,a))),)
def write_clip(name,count,make):
 out=O/name
 cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(count):proc.stdin.write(make(i/24).convert('RGB').tobytes())
  proc.stdin.close();rc=proc.wait()
 except BaseException:
  proc.kill();raise
 if rc:raise RuntimeError(name+' encode failed '+str(rc))
 print('ANIMATED',name,count,'frames',flush=True);return out

# Natural Earth land/borders, geographic pin 30.37608N 79.97012E; signals are NOT an actual telemetry path.
map_base=Image.open(O/'real_geography_map.png').convert('RGB');px=(79.97012-58)/44*W;py=(43-30.37608)/39*H

def map_frame(t):
 # gentle camera motion on the geographic plate, so the map is not a static title card.
 z=1.0+0.035*easing(t/6.5); cw=int(W/z);ch=int(H/z);cx=int(W/2+(px-W/2)*0.25);cy=int(H/2+(py-H/2)*0.25); x=max(0,min(W-cw,cx-cw//2));y=max(0,min(H-ch,cy-ch//2)); im=map_base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA');d=ImageDraw.Draw(im,'RGBA');mx=(px-x)*W/cw;my=(py-y)*H/ch
 # Radar pulse explains receiving signals, not a reconstruction of actual source or line of sight.
 for phase in (0,0.7,1.4):
  age=(t+phase)%2.1;r=22+age*105;alpha=int(190*(1-age/2.1));d.ellipse((mx-r,my-r,mx+r,my+r),outline=(239,193,104,alpha),width=4)
 d.ellipse((mx-9,my-9,mx+9,my+9),fill=(255,223,157,255))
 title='मशीन पहाड़ पर' if t<3.05 else 'चीन के मिसाइल सिग्नल'
 alpha=255*easing(min((t%3.05)/0.35,1));d.text((100,125),title,font=h1,fill=(255,250,238,int(alpha)),stroke_width=4,stroke_fill=(8,18,23,int(alpha)))
 d.text((100,230),'निगरानी की योजना' if t<3.05 else 'सिग्नल सुनने की कोशिश',font=h2,fill=(241,204,133,int(alpha)),stroke_width=3,stroke_fill=(8,18,23,int(alpha)))
 d.text((75,965),'SIGNAL PULSE IS CONCEPTUAL  ·  NOT AN ACTUAL ROUTE OR COVERAGE',font=sm,fill=(245,246,235,255),stroke_width=3,stroke_fill=(0,0,0,200))
 return im

# The site, device shape and rope setup are all symbolic; do not invent an actual cache location.
img=Image.open(A/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg').convert('RGB');bg=ImageOps.fit(img,(W,H),Image.Resampling.LANCZOS).convert('RGBA');dark=Image.new('RGBA',(W,H),(10,22,27,175));bg=Image.alpha_composite(bg,dark)
def cache_frame(t):
 im=bg.copy();d=ImageDraw.Draw(im,'RGBA');p=easing(t/.85)
 d.text((100,116),'मशीन बाँधकर छोड़ी',font=h1,fill=(255,255,246,255),stroke_width=3,stroke_fill='#0b161a')
 # symbol appears as a flat diagram; no claim of real equipment geometry.
 d.rounded_rectangle((1170,415,1510,680),radius=16,fill=(37,57,62,int(235*p)),outline=(239,210,152,int(255*p)),width=6)
 d.line((1220,495,1460,495),fill=(239,210,152,int(225*p)),width=5);d.text((1220,530),'उपकरण',font=h2,fill=(255,255,240,int(255*p)))
 # abstract anchor outside the device; rope draws out progressively to demonstrate the action.
 d.line((680,695,820,430),fill=(217,229,222,255),width=12);d.polygon([(795,433),(838,408),(847,455)],fill=(238,219,176,255))
 points=[(824,454),(920,455),(1020,540),(1135,545),(1170,505)]
 progress=easing((t-.45)/1.45)*(len(points)-1)
 for i in range(len(points)-1):
  q=max(0,min(1,progress-i));a,b=points[i],points[i+1];d.line((a[0],a[1],a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q),fill=(249,204,116,255),width=9)
 d.text((90,1008),'CONCEPTUAL DIAGRAM  ·  EXACT SITE AND CONFIGURATION UNKNOWN',font=sm,fill=(247,248,238,255),stroke_width=2,stroke_fill=(0,0,0,180))
 return im

def clue_frame(t):
 im=Image.new('RGBA',(W,H),(17,32,39,255));d=ImageDraw.Draw(im,'RGBA');d.text((95,115),'बाद में कुछ हिस्सों का दावा',font=h1,fill=(255,255,250,255))
 for x in range(0,W,90):d.line((x,240,x,H),fill=(93,125,123,28),width=1)
 a=easing((t-.2)/1.0); d.rounded_rectangle((205,320,940,755),radius=24,outline=(219,226,213,int(255*a)),width=5,fill=(35,57,60,int(210*a)))
 d.rectangle((390,420,750,660),outline=(235,197,126,int(255*a)),width=8);d.line((390,485,750,485),fill=(235,197,126,int(255*a)),width=5)
 d.text((1050,395),'खाली बाहरी हिस्से?',font=h2,fill=(245,246,236,int(255*easing((t-1)/.8))))
 d.text((1050,495),'पहचान: रिपोर्ट के अनुसार',font=h3,fill=(231,200,136,int(255*easing((t-2)/.8))))
 d.text((80,1008),'CONCEPTUAL GRAPHIC  ·  NOT A PHOTO OF RECOVERED MATERIAL',font=sm,fill=(239,241,233,255))
 return im

mapclip=write_clip('dynamic_map_17_8_24_3.mp4',156,map_frame)
cacheclip=write_clip('dynamic_cache_42_45.mp4',72,cache_frame)
clueclip=write_clip('dynamic_clue_54_5_60_6.mp4',146,clue_frame)
# Use different real Nanda Devi views for later returns, no replacement of one mountain with another.
ranikhet=G/'site-commons-wikimedia-org-nanda-devi-fi-4.jpg';gorson=G/'site-commons-wikimedia-org-nanda-devi-pe-4.jpg'
def replacement_img(path,out,n,title):
 ov=Image.new('RGBA',(W,H));d=ImageDraw.Draw(ov);d.line((95,115,230,115),fill='#ebc887',width=5);d.text((95,160),title,font=h1,fill='white',stroke_width=3,stroke_fill='#0e181c');d.text((70,1020),'NANDA DEVI  ·  MODERN PHOTOGRAPH',font=sm,fill='white',stroke_width=3,stroke_fill='#0e181c');ovpath=O/(out+'.png');ov.save(ovpath)
 cmd=[ff,'-v','error','-y','-loop','1','-framerate','24','-i',str(path),'-loop','1','-framerate','24','-i',str(ovpath),'-filter_complex',"[0:v]scale=2200:1238:force_original_aspect_ratio=increase,crop=2200:1238,zoompan=z='min(zoom+0.00013,1.035)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=24[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",'-map','[v]','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','21','-r','24',str(O/out)]
 subprocess.run(cmd,check=True);return O/out
p16=replacement_img(ranikhet,'part16_fresh.mp4',89,'1966: उपकरण गायब');p21=replacement_img(gorson,'part21_fresh.mp4',106,'मशीन यहाँ पहुँची कैसे?')
parts=[]
for i in range(23):
 if i==6:parts.append(mapclip)
 elif i==7:continue
 elif i==14:parts.append(cacheclip)
 elif i==16:parts.append(p16)
 elif i==18:parts.append(clueclip)
 elif i==19:continue
 elif i==21:parts.append(p21)
 else:parts.append(O/f'part_{i:02d}.mp4')
(O/'concat_dynamic.txt').write_text(''.join("file '"+str(x)+"'\n" for x in parts));pic=O/'picture_dynamic.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat_dynamic.txt'),'-c','copy',str(pic)],check=True)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';out=P/'RAAZVIK_CHAPTER01_ANIMATED_REVIEW_NOT_FINAL.mp4';subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',voice,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
print('DONE',out,flush=True)
