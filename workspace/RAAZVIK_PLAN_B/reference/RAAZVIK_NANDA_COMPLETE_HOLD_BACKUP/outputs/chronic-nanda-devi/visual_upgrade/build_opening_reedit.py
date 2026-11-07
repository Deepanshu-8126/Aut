import pathlib, subprocess, imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
P=pathlib.Path('/home/user/outputs/chronic-nanda-devi');D=P/'visual_upgrade/opening_reedit';D.mkdir(exist_ok=True)
f=imageio_ffmpeg.get_ffmpeg_exe();font='/home/user/explainer-pipeline/assets/fonts/NotoSansDevanagari-Bold.ttf'; hindi=ImageFont.truetype(font,53); small=ImageFont.truetype(font,20)
# Provisional editorial cuts: ASR timings require human ear check. Attribution tracked separately.
shots=[
(0,3.6,'img','assets/nanda_devi_real.jpg',0,'1965','नंदा देवी की आधुनिक तस्वीर'),
(3.6,6.2,'vid','visual_upgrade/assets/climber_pexels_12050237.mp4',0,'एक सीक्रेट मिशन','चित्रात्मक दृश्य • आधुनिक पर्वतारोही'),
(6.2,9.6,'img','climbers_reconstruction.png',0,'भारतीय और अमेरिकी टीम','AI पुनर्निर्माण • वास्तविक अभियान नहीं'),
(9.6,13.8,'img','cold_war_chapter/assets/nepal_porters_1997_john_pavelka.jpg',0,'सामान पहुँचाने वाले लोग','चित्रात्मक तस्वीर • नेपाल, 1997'),
(13.8,17.9,'img','assets/nanda_devi_real.jpg',0,'एक मशीन, पहाड़ की ओर','नंदा देवी की आधुनिक तस्वीर'),
(17.9,24.4,'img','opening_chapter_edit/region_context.png',0,'चीन से जुड़े सिग्नल','संदर्भ नक्शा • सटीक रास्ता नहीं दिखाया गया'),
(24.4,29.9,'img','sync_fix/real_aec.png',0,'बिजली का स्रोत','ऐतिहासिक RTG उदाहरण • अलग मॉडल'),
(29.9,33.4,'img','sync_fix/doe_cutaway.png',0,'प्लूटोनियम','RTG का उदाहरण • अलग मॉडल'),
(33.4,36.6,'vid','cold_war_chapter/assets/storm_weather_representative.mp4',0,'मौसम बदला','चित्रात्मक दृश्य • वास्तविक 1965 तूफ़ान नहीं'),
(36.6,39.8,'vid','cold_war_chapter/assets/storm_nepal_representative.mp4',0,'बर्फ़ और तेज़ हवा','चित्रात्मक दृश्य • वास्तविक 1965 तूफ़ान नहीं'),
(39.8,44.2,'img','cache_reconstruction.png',0,'टीम को लौटना पड़ा','AI पुनर्निर्माण • कल्पित दृश्य, वास्तविक जगह नहीं'),
(44.2,48.5,'img','assets/nanda_devi_real.jpg',0,'लौटकर लेने की योजना','नंदा देवी की आधुनिक तस्वीर'),
(48.5,52.2,'vid','visual_upgrade/assets/climber_pexels_12050237.mp4',6,'मशीन वहाँ नहीं मिली','चित्रात्मक दृश्य • वास्तविक खोज नहीं'),
(52.2,54.7,'img','opening_chapter_edit/region_context.png',0,'खोज जारी रही','संदर्भ नक्शा • सटीक रास्ता नहीं दिखाया गया'),
(54.7,60.6,'img','assets/nanda_devi_real.jpg',0,'कुछ हिस्से मिलने का दावा','1993 की पहचान अभियान से जुड़े लोगों का अनुमान'),
(60.6,65.1,'img','sync_fix/doe_cutaway.png',0,'कैप्सूल मिलने का पक्का सबूत नहीं','RTG का उदाहरण • अलग मॉडल')]
# This chapter is an internal render, not a historically complete final or full-film export.
parts=[]
for i,(a,b,kind,path,offset,title,credit) in enumerate(shots):
 out=D/f'part_{i:02d}.mp4';parts.append(out);overlay=D/f'overlay_{i:02d}.png'
 im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im);d.text((70,85),title,font=hindi,fill='white',stroke_width=3,stroke_fill='black');d.text((70,1020),credit,font=small,fill='#eee9df',stroke_width=2,stroke_fill='black');im.save(overlay)
 source=P/path
 inp=(['-ss',str(offset),'-i',str(source)] if kind=='vid' else ['-loop','1','-framerate','24','-i',str(source)])
 n=round(b*24)-round(a*24);vf='[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=24[base];[base][1:v]overlay=0:0,format=yuv420p[v]'
 cmd=[f,'-v','error','-y']+inp+['-i',str(overlay),'-filter_complex',vf,'-map','[v]','-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','21','-r','24',str(out)]
 subprocess.run(cmd,check=True);print('built',i,round(a,1),round(b,1),flush=True)
(D/'concat.txt').write_text(''.join("file '"+str(x)+"'\n" for x in parts));silent=D/'opening_picture.mp4';subprocess.run([f,'-v','error','-y','-f','concat','-safe','0','-i',str(D/'concat.txt'),'-c','copy',str(silent)],check=True)
out=D/'RAAZVIK_OPENING_REEDIT_INTERNAL.mp4';subprocess.run([f,'-v','error','-y','-i',str(silent),'-i','/home/user/nanda-voice.mp3','-map','0:v','-map','1:a','-t','65.1','-c:v','copy','-c:a','aac','-b:a','192k',str(out)],check=True)
print('DONE',out,flush=True)
