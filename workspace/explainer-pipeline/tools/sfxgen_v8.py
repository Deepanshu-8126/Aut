import json
B=json.load(open('/var/tmp/v8build/beats.json'))
beats=B['beats']; TOTAL=B['TOTAL']
SFX='/home/user/explainer-pipeline/assets/sfx/'
def ssAt(b,k):
    import math
    i=int(k); f=k-i
    ss=b['ss']; se=b['se']
    s0=ss[min(i,len(ss)-1)]
    if f<=0: return s0
    e0=se[min(i,len(se)-1)]
    return s0+f*(e0-s0)
EV=[]  # (t, file, vol, note)
def add(t,f,v,n): EV.append((round(t,2),f,v,n))
WH=['mk1489_air_woosh','mk1492_whoosh_fast','mk1143_whoosh_deep_impact','mk1486_tunnel_woosh']
wi=0
for bi,b in enumerate(beats):
    p=b['p']; tr=b['tr']; t0=b['t0']
    # beat-start whoosh
    if tr=='typo' and p.get('style')=='mega':
        add(max(40.2,t0-0.04),'mk788_big_impact',0.5,'mega lead')
    else:
        add(t0,WH[wi%4],0.42,'cut'); wi+=1
    for c in p.get('chips',[]): add(ssAt(b,c[0])+0.15,'mk2380_paper_quick',0.5,'chip')
    if tr=='typo':
        for L in p.get('lines',[]):
            f='mk788_big_impact' if p.get('style')=='mega' else ('mk677_glass_hit' if p.get('style')!='ledger' else 'mk677_glass_hit')
            add(ssAt(b,L[0]),f,0.5 if p.get('style')=='mega' else 0.4,'line')
        if p.get('riser'): add(b['t1']-3.0,'mk790_trailer_riser',0.4,'riser')
    if tr=='numpop':
        for it in p.get('items',[]): add(ssAt(b,it[0]),'mk788_big_impact',0.5,'numpop')
    if tr=='doc':
        for L in p.get('lines',[]): add(ssAt(b,L[0])+0.1,'mk1125_typewriter_soft',0.45,'docline')
        if p.get('stamp'): add(ssAt(b,p['stamp'][1])+0.35,'mk788_big_impact',0.5,'stamp')
        add(t0+0.05,'mk1530_paper_slide',0.5,'paper in')
    if tr=='quote': add(t0+0.3,'mk685_suspense_bass',0.42,'quote bass')
    if tr=='verdict':
        add(t0+0.25,'mk788_big_impact',0.5,'letter slam')
        for c in p.get('con',[]): add(ssAt(b,c[0]),'mk677_glass_hit',0.42,'con')
    if tr=='map':
        add(t0+0.4,'mk1486_tunnel_woosh',0.35,'map draw')
        for k in (0,2,4):
            if k<len(b['ss']): add(b['ss'][k]+0.3,'mk2380_paper_quick',0.4,'map chip')
    if tr=='fullclip': add(t0+0.1,'mk1104_page_turn',0.35,'reel')
    if tr=='winclip': add(t0+0.1,'mk1430_camera_shutter',0.4,'reel win')
    if tr=='storm':
        add(t0,'mk2390_rain_thunder',0.5,'thunder'); add(t0+4,'mk2393_light_rain_loop',0.45,'rain')
    if tr=='dark' and p.get('drop'): pass
    if tr=='finale':
        add(ssAt(b,1)+0.2,'mk1125_typewriter_soft',0.5,'type')
        add(b['ss'][-1]+0.1,'mk788_big_impact',0.6,'OPEN stamp')
        add(b['ss'][-1]+0.6,'mk1368_typewriter_bell',0.45,'bell')
    g=p.get('g')
    if g=='ticket': add(t0+0.1,'mk1530_paper_slide',0.5,''); add(ssAt(b,0.35),'mk1993_coin_single',0.5,'$20'); add(ssAt(b,1),'mk788_big_impact',0.45,'FL305')
    if g=='typename': add(ssAt(b,0.2),'mk1125_typewriter_soft',0.5,'typing'); add(ssAt(b,1),'mk2380_paper_quick',0.45,'')
    if g=='seatmap': add(ssAt(b,0.3),'mk2380_paper_quick',0.45,''); add(ssAt(b,1),'mk677_glass_hit',0.4,'')
    if g=='briefcase':
        for k in (1,2,3): add(ssAt(b,k),'mk677_glass_hit',0.45,'item')
    if g=='cash': add(t0+0.4,'mk1936_coins',0.5,''); add(ssAt(b,1),'mk2846_money_drop',0.55,'')
    if g=='microfilm':
        for i in range(6): add(t0+0.4+i*0.55,'mk1430_camera_shutter',0.4,'shutter')
        add(ssAt(b,2),'mk788_big_impact',0.45,'remember')
    if g=='checklist':
        for k in range(6): add(ssAt(b,k)+0.1,'mk1125_typewriter_soft',0.4,'chk')
    if g=='warnlight': add(t0+0.2,'mk1059_tick_tock',0.4,''); add(ssAt(b,1),'mk685_suspense_bass',0.45,'warn')
    if g=='bump': add(ssAt(b,2.3),'mk788_big_impact',0.6,'BUMP')
    if g=='radar': add(t0+0.3,'mk1059_tick_tock',0.4,''); add(ssAt(b,3),'mk788_big_impact',0.45,'nothing')
    if g=='evidence':
        for d in (0.3,1.5,2.7): add(t0+d,'mk677_glass_hit',0.45,'tag')
    if g=='headlines':
        for k in range(4): add(ssAt(b,min(k,len(b['ss'])-1)),'mk1530_paper_slide',0.5,'paper')
    if g=='mccoydive': add(t0+0.3,'mk1486_tunnel_woosh',0.45,''); add(ssAt(b,1),'mk788_big_impact',0.45,'')
    if g=='doors': add(ssAt(b,1),'mk1143_whoosh_deep_impact',0.5,''); add(ssAt(b,2),'mk1143_whoosh_deep_impact',0.5,'')
    if g=='match':
        for k in (2,3,4): add(ssAt(b,k),'mk788_big_impact',0.5,'MATCH')
    if g=='ticker': add(t0+0.3,'mk685_suspense_bass',0.45,''); add(ssAt(b,5),'mk788_big_impact',0.55,'ZERO')
    if g=='tie': add(t0+0.2,'mk1489_air_woosh',0.4,'')
    if g=='microscope': add(ssAt(b,2.4),'mk685_suspense_bass',0.45,'titanium')
    if g=='profile':
        for k in (1,2,3,4,5): add(ssAt(b,k),'mk2380_paper_quick',0.42,'trait')
    if g=='closed': add(ssAt(b,1.3),'mk788_big_impact',0.6,'CLOSED')
# extra atmosphere
add(241.4,'mk1590_airplane_rumble',0.5,'climb rumble')
add(70.97,'mk1590_airplane_rumble',0.4,'takeoff')
add(262.2,'mk2393_light_rain_loop',0.4,'stairs rain')
add(287.0,'mk2390_rain_thunder',0.35,'storm out')
for hb in (796.0,804.0,812.0): add(hb,'mk494_slow_heartbeat',0.5,'heart')
add(818.0,'mk492_mystery_heartbeat',0.45,'heart end')
EV.sort()
json.dump(EV,open('/var/tmp/v8build/sfx.json','w'))
md=['# SOUND MAP TABLE — DBC v8 (video time s)','| t | file | vol | note |','|---|------|-----|------|']
for t,f,v,n in EV: md.append(f'| {t} | {f} | {v} | {n} |')
open('/home/user/explainer-pipeline/assets/dbclong/v8/SOUND_MAP_V8.md','w').write('\n'.join(md))
print('SFX events (s1-s8):',len(EV),' + 26 s0 events =',len(EV)+26)
