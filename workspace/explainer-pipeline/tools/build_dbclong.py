#!/usr/bin/env python3
"""DBC LONG pipeline: TL from VO durations -> per-section render -> concat -> mux -> srt.
Usage: python3 build_dbclong.py [render|audio|all] [sections e.g. 1,2,3]"""
import json,subprocess,sys,os,glob,math
AST='/home/user/explainer-pipeline/assets/dbclong'
FF=glob.glob('/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-*')[0]
SFX='/home/user/explainer-pipeline/assets/sfx'
TMP='/var/tmp/lf'; os.makedirs(TMP,exist_ok=True)
def dur(f):
    r=subprocess.run([FF,'-i',f],capture_output=True,text=True).stderr
    for l in r.split('\n'):
        if 'Duration' in l:
            h,m,s=l.split('Duration:')[1].split(',')[0].strip().split(':')
            return int(h)*3600+int(m)*60+float(s)
    return 0
# ---- timeline ----
VOD=[dur(f'{AST}/vo{i}.mp3') for i in range(1,7)]
PAD=[8.5,2.0,2.5,2.0,2.0,11.0]  # sec1 title hold, sec6 outro
VOS=0.6  # vo starts after section start
TL={'s':[]}; t=0.0
for i in range(6):
    d=VOD[i]+VOS+PAD[i]
    TL['s'].append({'t0':round(t,2),'dur':round(d,2),'vo':round(t+VOS,2),'vod':round(VOD[i],2)})
    t+=d
TOTAL=t
import re as _re
_md=open(f'{AST}/SCRIPT.md').read()
_caps=[]
for _i in range(6):
    _m=_re.search(rf'### vo{_i+1}[^\n]*\n(.*?)(?=\n###|\n---|\Z)',_md,_re.S)
    _txt=_m.group(1).strip().replace('\n',' ')
    _sents=_re.split(r'(?<=[.!?]) +',_txt)
    _tot=sum(len(x) for x in _sents);_t=TL['s'][_i]['vo']
    for _sn in _sents:
        _d=TL['s'][_i]['vod']*len(_sn)/_tot
        _caps.append({'a':round(_t,2),'b':round(_t+_d,2),'txt':_sn})
        _t+=_d
TL['caps']=_caps
def _snt(i,j):
    cs=[c for c in _caps if c['a']>=TL['s'][i]['t0']-0.01 and c['a']<TL['s'][i]['t0']+TL['s'][i]['dur']]
    return cs[min(j,len(cs)-1)]['a']
TL['vs']=[
 {'a':round(_snt(1,1),2),'b':round(_snt(1,1)+6.0,2),'l':'CABIN · 1958 PROMO FILM — REPRESENTATION','src':'v1'},
 {'a':round(_snt(1,13)+0.5,2),'b':round(_snt(1,13)+5.0,2),'l':'707 FILM · 1958 — REPRESENTATION','src':'v5'},
 {'a':round(_snt(2,0)+1.2,2),'b':round(_snt(2,0)+6.7,2),'l':'JET AGE PROMO FILM — REPRESENTATION','src':'v2'},
 {'a':round(_snt(3,2)+1.0,2),'b':round(_snt(3,2)+6.0,2),'l':'TIMBER COUNTRY · 1953 — REPRESENTATION','src':'v3'},
 {'a':round(_snt(4,2),2),'b':round(_snt(4,2)+5.5,2),'l':'COLUMBIA RIVER FILM — REPRESENTATION','src':'v4'}]
json.dump(TL,open(f'{AST}/tl.json','w'),indent=1)
print('TOTAL',round(TOTAL,1),'s'); [print(i+1,s) for i,s in enumerate(TL['s'])]
mode=sys.argv[1] if len(sys.argv)>1 else 'all'
secs=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else [1,2,3,4,5,6]
# ---- render ----
if mode in ('render','all'):
    from playwright.sync_api import sync_playwright
    import time
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={'width':960,'height':540},device_scale_factor=2)
        pg.goto(f'file://{AST}/dbclong.html')
        pg.wait_for_function('window.READY===true',timeout=60000)
        pg.evaluate('setTL('+json.dumps(TL)+')')
        for si in secs:
            s=TL['s'][si-1]; t0=time.time()
            f0=math.floor(s['t0']*30); f1=math.floor((s['t0']+s['dur'])*30)
            for fr in range(f0,f1):
                pg.evaluate(f'renderAt({(fr+0.5)/30})')
                pg.screenshot(path=f'{TMP}/f{fr-f0:06d}.jpg',type='jpeg',quality=88)
            subprocess.run([FF,'-nostdin','-framerate','30','-i',f'{TMP}/f%06d.jpg',
                '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
                '-y',f'{TMP}/sec{si}.mp4'],capture_output=True)
            for fjpg in glob.glob(f'{TMP}/f*.jpg'): os.remove(fjpg)
            print(f'sec{si} rendered+encoded {int(time.time()-t0)}s frames={f1-f0}')
        b.close()
# ---- concat + audio ----
if mode in ('audio','all'):
    open(f'{TMP}/cat.txt','w').write('\n'.join(f"file '{TMP}/sec{i}.mp4'" for i in range(1,7)))
    subprocess.run([FF,'-nostdin','-f','concat','-safe','0','-i',f'{TMP}/cat.txt','-c','copy','-y',f'{TMP}/video.mp4'],capture_output=True)
    S=[x['t0'] for x in TL['s']]; V=[x['vo'] for x in TL['s']]; D=[x['dur'] for x in TL['s']]
    def ms(x): return int(x*1000)
    # SFX events (sync with engine fractions)
    ev=[]
    ad=lambda f,t,v,tr=None: ev.append((f,ms(t),v,tr))
    caps=TL['caps']
    def snt(i,j):
        cs=[c for c in caps if c['a']>=TL['s'][i]['t0']-0.01 and c['a']<TL['s'][i]['t0']+TL['s'][i]['dur']]
        return cs[min(j,len(cs)-1)]['a']
    # --- SEC1 cold open
    ad('mk1125_typewriter_soft',0.5,0.5)
    ad('mk788_big_impact',2.0,0.7)                  # folder slam
    ad('mk1530_paper_slide',5.2,0.7)                # ticket
    ad('mk1430_camera_shutter',snt(0,5),0.65)       # name circle
    ad('mk2380_paper_quick',snt(0,6),0.6)           # note
    ad('mk685_suspense_bass',snt(0,10),0.9)         # A BOMB
    ad('mk1489_air_woosh',snt(0,11),0.65)           # jump scene
    ad('mk788_big_impact',snt(0,12),0.8)            # GONE
    ad('mk790_trailer_riser',0.86*D[0]+S[0],0.6)    # title
    # chapter risers + hits
    for ch in range(1,6):
        ad('mk1492_whoosh_fast',S[ch]-0.3,0.6)
        ad('mk677_glass_hit',S[ch]+0.25,0.6)
    # --- SEC2
    ad('mk1125_typewriter_soft',snt(1,4)+0.3,0.45)  # demands typing
    ad('mk1489_air_woosh',snt(1,8),0.6)             # circling
    ad('mk1590_airplane_rumble',snt(1,13),0.24,8)   # landing
    ad('mk1430_camera_shutter',snt(1,17)+0.3,0.7)
    ad('mk1430_camera_shutter',snt(1,17)+0.9,0.7)
    ad('mk1430_camera_shutter',snt(1,17)+1.5,0.7)
    # --- SEC3
    ad('mk1590_airplane_rumble',S[2],0.26,12)
    ad('mk1059_tick_tock',snt(2,3),0.35,6)          # AFT STAIRS light
    ad('mk685_suspense_bass',snt(2,4),0.7)          # stairs open
    ad('mk788_big_impact',snt(2,7),0.85)            # "NO." slam
    ad('mk1059_tick_tock',snt(2,8),0.3,8)           # 13 min silence
    ad('mk788_big_impact',snt(2,9),0.95)            # 8:13 bump EXACT
    ad('mk1486_tunnel_woosh',snt(2,13),0.6)         # jump scene
    ad('mk1104_page_turn',snt(2,15),0.6)            # reno
    # --- SEC4
    ad('mk1143_whoosh_deep_impact',snt(3,1),0.7)    # NORJAK stamp
    ad('mk2390_rain_thunder',snt(3,2),0.3,6)        # search rain
    ad('mk677_glass_hit',snt(3,4),0.65)             # 400 counter
    ad('mk1104_page_turn',snt(3,9),0.6)             # evidence
    ad('mk1104_page_turn',snt(3,12),0.55)
    ad('mk1430_camera_shutter',snt(3,15),0.7)       # sketches
    # --- SEC5
    ad('mk2380_paper_quick',snt(4,4),0.65)          # hands hit paper
    ad('mk685_suspense_bass',snt(4,8),0.85)         # Cooper's money
    ad('mk677_glass_hit',snt(4,15),0.7)             # $194,200
    # --- SEC6
    ad('mk1530_paper_slide',snt(5,2),0.6)
    ad('mk1530_paper_slide',snt(5,4),0.6)
    ad('mk1530_paper_slide',snt(5,6),0.6)
    ad('mk1143_whoosh_deep_impact',snt(5,10),0.8)   # CLOSED stamp
    ad('mk790_trailer_riser',snt(5,12),0.55)        # verdict
    ad('mk788_big_impact',snt(5,22),0.8)            # OPEN.
    ad('mk492_mystery_heartbeat',TOTAL-12,0.5,11)
    ins=['-i',f'{TMP}/video.mp4','-i','/var/tmp/bedchap.wav']
    for i in range(1,7): ins+=['-i',f'{AST}/vo{i}.mp3']
    for e in ev: ins+=['-i',f'{SFX}/{e[0]}.mp3']
    fc=[]
    bump=S[2]+0.60*D[2]
    fc.append(f"[1:a]atrim=0:{TOTAL:.2f},volume=0.18,volume=enable='between(t,{bump:.1f},{bump+2.5:.1f})':volume=0.4,afade=t=out:st={TOTAL-6:.1f}:d=6[bed]")
    mixin=['[bed]']
    for i in range(6):
        fc.append(f"[{2+i}:a]adelay={ms(V[i])}|{ms(V[i])},volume=1.0[vo{i}]"); mixin.append(f'[vo{i}]')
    for j,e in enumerate(ev):
        tr=f"atrim=0:{e[3]}," if e[3] else ""
        fc.append(f"[{8+j}:a]{tr}adelay={e[1]}|{e[1]},volume={e[2]}[sx{j}]"); mixin.append(f'[sx{j}]')
    fc.append(''.join(mixin)+f"amix=inputs={len(mixin)}:normalize=0,aresample=44100,aformat=channel_layouts=stereo,alimiter=limit=0.95[a]")
    cmd=[FF,'-nostdin']+ins+['-filter_complex',';'.join(fc),'-map','0:v','-map','[a]',
        '-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{TOTAL:.2f}','-y','/home/user/outputs/dbcooper-complete-file.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True)
    print('mux exit',r.returncode, r.stderr[-400:] if r.returncode else 'OK')
    # loudness check
    r=subprocess.run([FF,'-nostdin','-i','/home/user/outputs/dbcooper-complete-file.mp4','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    print('\n'.join(l for l in r.stderr.split('\n') if 'volume' in l))
print('done')
