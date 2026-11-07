from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import subprocess, math, imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01');T=P/'v2_edit';T.mkdir(exist_ok=True);F='/home/user/explainer-pipeline/assets/fonts/';ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1920,1080
hi=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',70); h2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',44);hs=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',33); en=ImageFont.truetype(F+'Inter-Bold.ttf',39);tiny=ImageFont.truetype(F+'Inter-Medium.ttf',23);big=ImageFont.truetype(F+'Inter-Black.ttf',112)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';old=P/'RAAZVIK_CHAPTER01_REAL_TERRAIN_REVIEW_NOT_FINAL.mp4';stock=P/'RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/visual_upgrade/assets/panchachuli_pexels_36907717.mp4';doe=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/sync_fix/doe_cutaway.png'

def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def rawclip(name,frames,framefn):
 out=T/name;cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)];pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(frames):pr.stdin.write(framefn(i/24).convert('RGB').tobytes())
 pr.stdin.close();rc=pr.wait();assert rc==0,(name,rc)
 print('built',name,frames,flush=True);return out
# Opening: real moving, modern footage from Panchachuli, not footage of 1965 or of Nanda Devi.
ov=Image.new('RGBA',(W,H));d=ImageDraw.Draw(ov);d.line((95,125,240,125),fill='#e7c482',width=5);d.text((95,170),'1965',font=big,fill='white',stroke_width=3,stroke_fill='#111a20');d.text((95,315),'भारत के हिमालय में',font=hi,fill='white',stroke_width=3,stroke_fill='#111a20');d.text((65,1010),'ILLUSTRATIVE MODERN FOOTAGE  ·  PANCHACHULI, UTTARAKHAND',font=tiny,fill='white',stroke_width=3,stroke_fill='#111a20');ov.save(T/'open_overlay.png')
intro=T/'01_open_video.mp4';subprocess.run([ff,'-v','error','-y','-i',str(stock),'-loop','1','-framerate','24','-i',str(T/'open_overlay.png'),'-filter_complex','[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,setsar=1[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]','-map','[v]','-frames:v','77','-an','-c:v','libx264','-preset','veryfast','-crf','20','-r','24',str(intro)],check=True);print('built real opening',flush=True)
# Real NASA Blue Marble WMS EPSG:4326 lat 12..37.875, lon 60..106.
base=Image.open(P/'assets/nasa_india_wide.jpg').convert('RGBA');px=(79.97012-60)/46*W;py=(37.875-30.37608)/25.875*H

def map_frame(t):
 z=1+0.10*smooth(t/2.8);cw=int(W/z);ch=int(H/z);cx=W/2+(px-W/2)*.55;cy=H/2+(py-H/2)*.55;x=max(0,min(W-cw,int(cx-cw/2)));y=max(0,min(H-ch,int(cy-ch/2))); im=base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.BICUBIC);d=ImageDraw.Draw(im,'RGBA');mx=(px-x)*W/cw;my=(py-y)*H/ch
 alpha=int(255*smooth((t-.3)/.5));
 for phase in [0,.8]:
  age=(t+phase)%1.6;r=18+age*75; d.ellipse((mx-r,my-r,mx+r,my+r),outline=(250,205,132,int(190*(1-age/1.6))),width=4)
 d.ellipse((mx-12,my-12,mx+12,my+12),fill=(255,222,155,alpha));d.text((mx+32,my-56),'नंदा देवी',font=hs,fill=(255,255,245,alpha),stroke_width=3,stroke_fill=(3,10,16,alpha));d.text((90,100),'एक सीक्रेट मिशन',font=hi,fill='white',stroke_width=4,stroke_fill='#10191d');d.text((95,205),'उत्तराखंड',font=h2,fill='#e9c583',stroke_width=3,stroke_fill='#10191d');d.text((60,1014),'NASA BLUE MARBLE / GIBS  ·  MODERN TERRAIN  ·  APPROXIMATE LOCATION',font=tiny,fill='white',stroke_width=3,stroke_fill='#10191d');return im
mapclip=rawclip('02_animated_geography.mp4',67,map_frame)
# Keep the published DOE cutaway recognizable. Animate callout and conceptual heat/electricity, not physical movement of components.
diagram=Image.open(doe).convert('RGBA');diagram.thumbnail((995,825),Image.Resampling.LANCZOS);back=Image.new('RGBA',(W,H),(12,24,31,255));back.alpha_composite(diagram,(865,145))

def rtg_frame(t):
 im=back.copy();d=ImageDraw.Draw(im,'RGBA');d.line((105,125,240,125),fill=(229,191,118,255),width=5);d.text((105,175),'बिजली का सोर्स',font=hi,fill=(248,248,238,255));d.text((105,275),'RTG',font=en,fill=(229,191,118,255));p=smooth((t-.4)/1.0);d.rounded_rectangle((105,390,650,518),radius=14,outline=(211,219,207,int(255*p)),width=4);d.text((145,420),'गर्मी से बिजली',font=h2,fill=(255,255,245,int(255*p)))
 if t>=2.6:
  q=smooth((t-2.6)/.6);d.text((108,600),'प्लूटोनियम',font=hi,fill=(255,209,132,int(255*q)));d.text((110,690),'रेडियोएक्टिव मटेरियल',font=hs,fill=(245,247,238,int(255*q)))
 # Pulses are graphic callouts, not actual measurements or proof of precise assembly.
 cx,cy=1370,532
 for phase in [0,.7,1.4]:
  age=(t+phase)%2.2;r=36+age*78;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(239,190,111,int(155*(1-age/2.2))),width=4)
 d.text((70,1010),'DOE RTG CUTAWAY  ·  DIFFERENT MODEL  ·  GRAPHIC IS EXPLANATORY',font=tiny,fill='white',stroke_width=2,stroke_fill='#0c161c');return im
rtgclip=rawclip('04_animated_rtg.mp4',149,rtg_frame)
# Frame-exact retained passages avoid audio changes. Total 1776 frames = 74.00 seconds.
def extract(name,start,end):
 out=T/name;subprocess.run([ff,'-v','error','-y','-i',str(old),'-vf',f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','24',str(out)],check=True);print('retained',name,flush=True);return out
middle=extract('03_existing_6_to_27.mp4',144,648);end=extract('05_existing_33_to_74.mp4',797,1776)
parts=[intro,mapclip,middle,rtgclip,end];(T/'concat.txt').write_text(''.join("file '"+str(x)+"'\n" for x in parts));pic=T/'picture.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(T/'concat.txt'),'-c','copy',str(pic)],check=True)
out=P/'RAAZVIK_CHAPTER01_MOVING_OPENING_RTG_REVIEW.mp4';subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',voice,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True);print('DONE',out,flush=True)
