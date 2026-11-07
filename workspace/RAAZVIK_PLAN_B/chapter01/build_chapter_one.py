from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, subprocess, imageio_ffmpeg, math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01'); R=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi'; Q=P/'assets/nanda_search_images'; O=P/'working_full_chapter'; O.mkdir(exist_ok=True)
F='/home/user/explainer-pipeline/assets/fonts/'; ff=imageio_ffmpeg.get_ffmpeg_exe(); W,H=1920,1080
H1=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',70); H2=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',48); H3=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',36); EN=ImageFont.truetype(F+'Inter-Bold.ttf',42); SM=ImageFont.truetype(F+'Inter-Medium.ttf',23); BIG=ImageFont.truetype(F+'Inter-Black.ttf',122)

def boxfit(path,size):return ImageOps.fit(Image.open(path).convert('RGB'),size,Image.Resampling.LANCZOS)
def map_image():
 im=Image.new('RGB',(W,H),'#101c23');d=ImageDraw.Draw(im)
 lon0,lon1,lat0,lat1=58,102,4,43
 def xy(lon,lat):return ((lon-lon0)/(lon1-lon0)*W,(lat1-lat)/(lat1-lat0)*H)
 for x in range(60,101,10):
  a,b=xy(x,lat0),xy(x,lat1);d.line((*a,*b),fill='#253640',width=2)
 for y in range(10,41,10):
  a,b=xy(lon0,y),xy(lon1,y);d.line((*a,*b),fill='#253640',width=2)
 geo=json.load(open('/home/user/explainer-pipeline/assets/world_110m.geojson'))
 for f in geo['features']:
  g=f['geometry']; typ=g['type']; coords=g['coordinates']; polygons=[coords] if typ=='Polygon' else coords if typ=='MultiPolygon' else []
  for poly in polygons:
   ring=poly[0]; pts=[xy(lon,lat) for lon,lat,*_ in ring]
   if pts:d.polygon(pts,fill='#718179',outline='#a2b0a5',width=2)
 borders=json.load(open('/home/user/explainer-pipeline/assets/world_borders_110m.geojson'))
 for f in borders['features']:
  g=f['geometry']; coords=g['coordinates']; lines=[coords] if g['type']=='LineString' else coords if g['type']=='MultiLineString' else []
  for line in lines:
   pts=[xy(lon,lat) for lon,lat,*_ in line];
   if len(pts)>1:d.line(pts,fill='#cad0bc',width=2)
 px,py=xy(79.97012,30.37608);d.ellipse((px-14,py-14,px+14,py+14),fill='#f4cf81');d.ellipse((px-27,py-27,px+27,py+27),outline='#f4cf81',width=3)
 d.text((px+35,py-62),'नंदा देवी',font=H3,fill='#fff9ed',stroke_width=3,stroke_fill='#101c23');d.text((220,785),'भारत',font=H2,fill='white',stroke_width=3,stroke_fill='#101c23');d.text((1290,190),'चीन',font=H2,fill='white',stroke_width=3,stroke_fill='#101c23')
 d.text((65,1010),'MAP: NATURAL EARTH  ·  APPROXIMATE LOCATION  ·  NOT A ROUTE',font=SM,fill='#e0e4dc');p=O/'real_geography_map.png';im.save(p);return p
mp=map_image()
# Construct honest technical comparison graphic, not a photoreal 1965 device.
def diagram(kind):
 im=Image.new('RGB',(W,H),'#13242b');d=ImageDraw.Draw(im)
 for x in range(0,W,90):d.line((x,0,x,H),fill='#23373d',width=1)
 for y in range(0,H,90):d.line((0,y,W,y),fill='#23373d',width=1)
 if kind=='heat':
  steps=[(150,'प्लूटोनियम','गर्मी'),(710,'RTG','बिजली'),(1270,'उपकरण','सिग्नल')]
  for x,a,b in steps:
   d.rounded_rectangle((x,330,x+450,690),radius=24,fill='#243b40',outline='#91a59e',width=3);d.text((x+38,390),a,font=(EN if a=='RTG' else H2),fill='#f4f3eb');d.text((x+38,515),b,font=H2,fill='#e8c281')
  for x in (630,1190): d.line((x,510,x+60,510),fill='#e8c281',width=7);d.polygon([(x+60,495),(x+80,510),(x+60,525)],fill='#e8c281')
  d.text((80,90),'बिजली कहाँ से आती थी?',font=H1,fill='white')
 elif kind=='cache':
  d.text((90,110),'लौटने की योजना थी',font=H1,fill='white');d.line((250,690,720,480,1120,690),fill='#b2c1bb',width=8);d.rectangle((640,545,780,640),outline='#ecc783',width=6);d.text((860,505),'सामान यहीं सुरक्षित किया गया',font=H2,fill='white');d.text((860,575),'सटीक जगह अज्ञात',font=H3,fill='#b8c5bd')
 elif kind=='clue':
  d.text((90,130),'बाद में कुछ हिस्सों का दावा',font=H1,fill='white');d.rounded_rectangle((170,340,790,700),radius=15,outline='#c4d1c9',width=5);d.text((260,475),'बाहरी हिस्से?',font=H2,fill='#e4c080');d.line((915,310,915,730),fill='#d2d9cf',width=3);d.rounded_rectangle((1040,340,1690,700),radius=15,outline='#c4d1c9',width=5);d.text((1140,455),'फ्यूल कैप्सूल',font=H2,fill='white');d.text((1140,535),'मिलने की पुष्टि नहीं',font=H3,fill='#e4c080')
 d.text((75,1008),'EXPLANATORY GRAPHIC  ·  NOT THE ACTUAL DEVICE OR SITE',font=SM,fill='#d1dad4');p=O/(kind+'.png');im.save(p);return p
heat=diagram('heat');cache=diagram('cache');clue=diagram('clue')
# Transparent typography overlays; text never asserts that modern stock is the expedition.
def overlay(title='',label='',subtitle=''):
 key=str(abs(hash((title,label,subtitle))));p=O/('overlay_'+key+'.png')
 if p.exists():return p
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 if title:
  d.line((95,115,230,115),fill='#ebc887',width=5);d.text((95,160),title,font=H1,fill='white',stroke_width=3,stroke_fill='#0e181c')
 if subtitle:d.text((98,260),subtitle,font=H3,fill='#eacb8c',stroke_width=2,stroke_fill='#0e181c')
 if label:d.text((70,1020),label,font=SM,fill='white',stroke_width=3,stroke_fill='#0e181c')
 im.save(p);return p
# Time anchors are estimates only; continuous audio remains uncut.
N=R/'visual_upgrade/assets/nanda_devi_michael_scalet.jpg'; G=Q/'site-commons-wikimedia-org-nanda-devi-pe-4.jpg';V=R/'visual_upgrade/assets';PORT=R/'cold_war_chapter/assets/nepal_porters_1997_john_pavelka.jpg'; K=R/'cold_war_chapter/assets/kohli_2015.jpg'; DOE=R/'sync_fix/doe_cutaway.png'; STAMP=R/'cold_war_chapter/assets/everest_stamp.jpg'
# start,end,kind,path,offset,title,caption,subtitle
shots=[
 (0,3.2,'img',N,0,'1965','NANDA DEVI  ·  MODERN PHOTOGRAPH',''),
 (3.2,6.0,'img',mp,0,'एक सीक्रेट मिशन','',''),
 (6,9,'img',K,0,'भारतीय और अमेरिकी टीम','M. S. KOHLI  ·  PHOTOGRAPHED IN 2015','मिशन लीडर: एम. एस. कोहली'),
 (9,11.4,'img',PORT,0,'शेरपा और स्थानीय लोग','ILLUSTRATIVE: NEPAL PORTERS, 1997  ·  NOT THE 1965 TEAM',''),
 (11.4,14,'video',V/'trekking_pexels_2894895.mp4',1,'','ILLUSTRATIVE MODERN HIKING FOOTAGE',''),
 (14,17.8,'img',G,0,'नंदा देवी','NANDA DEVI  ·  MODERN PHOTOGRAPH',''),
 (17.8,21,'img',mp,0,'सिग्नल सुनने का प्लान','',''),
 (21,24.3,'img',mp,0,'चीन से जुड़े सिग्नल','','सटीक सिग्नल रूट नहीं दिखाया गया'),
 (24.3,27,'img',heat,0,'','',''),
 (27,30,'img',DOE,0,'ऊर्जा का स्रोत','DOE RTG CUTAWAY  ·  EXAMPLE OF A DIFFERENT MODEL',''),
 (30,33.2,'img',heat,0,'','',''),
 (33.2,36.5,'video',V/'machhapuchchhre_pexels_14372030.mp4',0,'मौसम बदल गया','ILLUSTRATIVE WEATHER  ·  NOT 1965 FOOTAGE',''),
 (36.5,39.5,'video',V/'climber_pexels_12050237.mp4',2,'','ILLUSTRATIVE CLIMBING  ·  NOT THE 1965 TEAM',''),
 (39.5,42.0,'video',V/'kedarkantha_pexels_19983625.mp4',1,'टीम को लौटना पड़ा','ILLUSTRATIVE MODERN FOOTAGE',''),
 (42,45,'img',cache,0,'','',''),
 (45,48.2,'img',G,0,'वापस आने की योजना','NANDA DEVI  ·  MODERN PHOTOGRAPH',''),
 (48.2,51.9,'img',N,0,'1966: उपकरण गायब','NANDA DEVI  ·  MODERN PHOTOGRAPH',''),
 (51.9,54.5,'img',mp,0,'खोज जारी रही','','जगह और रास्ता अनिश्चित'),
 (54.5,57.5,'img',clue,0,'','',''),
 (57.5,60.6,'img',clue,0,'','',''),
 (60.6,64.6,'img',DOE,0,'कैप्सूल मिलने की पुष्टि नहीं','DOE RTG CUTAWAY  ·  EXAMPLE OF A DIFFERENT MODEL',''),
 (64.6,69,'img',N,0,'मशीन यहाँ पहुँची कैसे?','NANDA DEVI  ·  MODERN PHOTOGRAPH',''),
 (69,74,'video',V/'panchachuli_pexels_36907717.mp4',0,'पूरी कहानी','ILLUSTRATIVE HIMALAYAN FOOTAGE  ·  PANCHACHULI','')]
parts=[]
for i,(a,b,kind,path,offset,title,label,subtitle) in enumerate(shots):
 out=O/f'part_{i:02d}.mp4';n=round(b*24)-round(a*24);parts.append(out);ov=overlay(title,label,subtitle)
 if not Path(path).exists():raise FileNotFoundError(path)
 if kind=='video':
  inputs=['-ss',str(offset),'-i',str(path),'-loop','1','-framerate','24','-i',str(ov)]; filters='[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=24[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]'
 else:
  # Low-resolution archival photos are contained with a blurred backdrop instead of stretched as native HD.
  if path in [K,DOE,STAMP]:
   inputs=['-loop','1','-framerate','24','-i',str(path),'-loop','1','-framerate','24','-i',str(ov)]
   filters='[0:v]split=2[one][two];[one]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:5,eq=brightness=-0.3[bg];[two]scale=1450:900:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[mid];[mid][1:v]overlay=0:0:shortest=1,format=yuv420p[v]'
  else:
   inputs=['-loop','1','-framerate','24','-i',str(path),'-loop','1','-framerate','24','-i',str(ov)]
   filters="[0:v]scale=2200:1238:force_original_aspect_ratio=increase,crop=2200:1238,zoompan=z='min(zoom+0.00013,1.035)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=24[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]"
 cmd=[ff,'-v','error','-y']+inputs+['-filter_complex',filters,'-map','[v]','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','21','-r','24',str(out)]
 subprocess.run(cmd,check=True); print('SHOT',i,round(a,1),'–',round(b,1),'frames',n,flush=True)
(O/'concat.txt').write_text(''.join("file '"+str(x)+"'\n" for x in parts));pic=O/'picture_only.mp4';subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy',str(pic)],check=True)
voice='/home/user/RAAZVIK_PLAN_B/reference/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/nanda-voice.mp3';out=P/'RAAZVIK_CHAPTER01_PICTURE_REVIEW_NOT_FINAL.mp4'
subprocess.run([ff,'-v','error','-y','-i',str(pic),'-i',voice,'-map','0:v','-map','1:a','-t','74','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
print('DONE',out,flush=True)
