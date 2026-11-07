from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,math,imageio_ffmpeg
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01');O=P/'working_full_chapter';W,H=1920,1080;F='/home/user/explainer-pipeline/assets/fonts/'; ff=imageio_ffmpeg.get_ffmpeg_exe()
H1=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',72);H2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',42); H3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',33); SM=ImageFont.truetype(F+'Inter-Medium.ttf',21)
# Actual georeferenced NASA Blue Marble imagery, exact EPSG:4326 bounds of WMS request.
base=Image.open(P/'assets/nasa_blue_marble_himalaya.jpg').convert('RGBA'); latmin,latmax,lonmin,lonmax=24,38.0625,70,95
def xy(lon,lat):return (W*(lon-lonmin)/(lonmax-lonmin),H*(latmax-lat)/(latmax-latmin))
d=ImageDraw.Draw(base,'RGBA');borders=json.load(open('/home/user/explainer-pipeline/assets/world_borders_110m.geojson'))
for feat in borders['features']:
 g=feat['geometry'];lines=[g['coordinates']] if g['type']=='LineString' else g['coordinates'] if g['type']=='MultiLineString' else []
 for l in lines:
  pts=[xy(lon,lat) for lon,lat,*_ in l]
  if len(pts)>1:d.line(pts,fill=(244,243,222,115),width=3)
# Political labels are general regional context only; borders shown by Natural Earth are approximate.
d.text(xy(76,27),'भारत',font=H2,fill=(255,255,245,230),stroke_width=4,stroke_fill=(7,16,19,220));d.text(xy(88.5,34.2),'चीन',font=H2,fill=(255,255,245,230),stroke_width=4,stroke_fill=(7,16,19,220))
px,py=xy(79.97012,30.37608)
def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
clip=O/'dynamic_nasa_terrain_map.mp4'
cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(clip)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(156):
 t=i/24;z=1+0.06*ease(t/6.5);cw=int(W/z);ch=int(H/z);cx=W/2+(px-W/2)*.2;cy=H/2+(py-H/2)*.2;x=max(0,min(W-cw,int(cx-cw/2)));y=max(0,min(H-ch,int(cy-ch/2)));im=base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.BICUBIC);draw=ImageDraw.Draw(im,'RGBA');mx=(px-x)*W/cw;my=(py-y)*H/ch
 for phase in (0,.7,1.4):
  age=(t+phase)%2.1;r=20+age*95;a=int(195*(1-age/2.1));draw.ellipse((mx-r,my-r,mx+r,my+r),outline=(245,202,111,a),width=5)
 draw.ellipse((mx-12,my-12,mx+12,my+12),fill=(255,225,160,255));draw.text((mx+26,my-54),'नंदा देवी',font=H3,fill='white',stroke_width=4,stroke_fill='#0b171c')
 title='मशीन पहाड़ पर' if t<3.05 else 'चीन के मिसाइल सिग्नल';sub='निगरानी की योजना' if t<3.05 else 'सिग्नल सुनने की कोशिश';draw.text((85,90),title,font=H1,fill='white',stroke_width=4,stroke_fill='#0b171c');draw.text((88,190),sub,font=H2,fill='#ffe0a3',stroke_width=3,stroke_fill='#0b171c')
 draw.text((55,1000),'NASA BLUE MARBLE / GIBS  ·  MODERN SATELLITE MOSAIC  ·  PULSE IS CONCEPTUAL',font=SM,fill='white',stroke_width=3,stroke_fill='#0b171c')
 proc.stdin.write(im.convert('RGB').tobytes())
proc.stdin.close();rc=proc.wait();assert rc==0
parts=[]
for i in range(23):
 if i==6:parts.append(clip)
 elif i in (7,19):continue
 elif i==14:parts.append(O/'dynamic_cache_42_45.mp4')
 elif i==16:parts.append(O/'part16_fresh.mp4')
 elif i==18:parts.append(O/'dynamic_clue_54_5_60_6.mp4')
 elif i==21:parts.append(O/'part21_fresh.mp4')
 else:parts.append(O/f'part_{i:02d}.mp4')
(O/'concat_nasa.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts));pic=O/'picture_nasa.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat_nasa.txt'),'-c','copy',str(pic)],check=True)
v='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';out=P/'RAAZVIK_CHAPTER01_REAL_TERRAIN_REVIEW_NOT_FINAL.mp4';subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',v,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True);print('DONE',out)
