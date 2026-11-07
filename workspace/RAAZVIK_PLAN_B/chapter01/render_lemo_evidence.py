#!/usr/bin/env python3
"""LEMO-inspired evidence beat, not a finished chapter; no fake historic footage."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess,imageio_ffmpeg,math
P=Path('/home/user/RAAZVIK_PLAN_B/chapter01');O=P/'lemo_work';O.mkdir(exist_ok=True);W,H=1920,1080;ff=imageio_ffmpeg.get_ffmpeg_exe()
F='/home/user/explainer-pipeline/assets/fonts/';head=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',52);small=ImageFont.truetype(F+'Inter-Medium.ttf',22); hsmall=ImageFont.truetype(F+'NotoSansDevanagari-Bold.ttf',32)
mapfile=P/'assets/nasa_blue_marble_himalaya.jpg';record=P/'assets/RAAZVIK_NANDA_COMPLETE_HOLD_BACKUP/outputs/chronic-nanda-devi/visual_upgrade/FRUS_1978_official_page_capture.png'
if not mapfile.exists() or not record.exists():raise SystemExit('verified source asset missing')
background=Image.open(mapfile).convert('RGBA');bg_dark=Image.new('RGBA',(W,H),(4,13,20,170));background=Image.alpha_composite(background,bg_dark)
# This is a screenshot of the official transcription, NOT an archival scan.
raw=Image.open(record).convert('RGBA');card=raw.crop((0,0,1232,530));card.thumbnail((1180,530),Image.Resampling.LANCZOS)

def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def frame(t):
 im=background.copy();d=ImageDraw.Draw(im,'RGBA');d.text((85,110),'अगले साल टीम लौटी',font=head,fill=(244,246,240,255),stroke_width=2,stroke_fill=(0,0,0,140));d.text((88,210),'मशीन नहीं मिली',font=head,fill=(255,207,134,255),stroke_width=2,stroke_fill=(0,0,0,140));
 # Source panel enters from the same content coordinate over the terrain; the webpage remains recognizable as a web transcription.
 u=ease((t-.3)/.85);x=int(680+(1-u)*120);y=340
 panel=card.copy();width=int(510*ease((t-2.0)/.8));
 # Blend translucent highlight over actual source text; never redraw the original words.
 if width>0:
  mark=Image.new('RGBA',panel.size);ImageDraw.Draw(mark).rectangle((548,300,548+width,335),fill=(246,196,82,85));panel=Image.alpha_composite(panel,mark)
 im.alpha_composite(panel,(x,y));d=ImageDraw.Draw(im,'RGBA');d.text((x,y-70),'US STATE DEPARTMENT  ·  14 APRIL 1978',font=small,fill=(255,255,248,int(255*u)));d.text((x,y+panel.height+25),'OFFICIAL WEBSITE TRANSCRIPTION  ·  NOT THE ORIGINAL PAPER',font=small,fill=(247,246,233,int(255*u)))
 return im.convert('RGB')
output=O/'evidence_1966_internal.mp4';cmd=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-frames:v','150','-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',str(output)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(150):proc.stdin.write(frame(i/24).tobytes())
proc.stdin.close();assert proc.wait()==0;print('INTERNAL EVIDENCE BEAT',output)
