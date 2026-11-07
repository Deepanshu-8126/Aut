import json
M = json.load(open('/var/tmp/v8build/sentmap.json'))
order = ['s1','s2','s3','s4','s5','s6','s7a','s7b','s8']
S0_END = 40.10; VO_LEAD = 0.6
starts = {}; vo = {}
cur = S0_END
for s in order:
    starts[s] = round(cur,2); vo[s] = round(cur+VO_LEAD,2)
    last = M[s]['sents'][-1]['end']
    tail = 4.6 if s=='s8' else 0.7
    cur = round(vo[s] + last + tail, 2)
TOTAL = cur

SPEC = {
's1': [
 (1,'fullclip',{'label':'PORTLAND INTERNATIONAL AIRPORT','right':'NOV 24 1971 - 2:45 PM','reel':'TERMINAL - 1948 - REPRESENTATION'}),
 (2,'fullclip',{'label':'THE NORTHWEST ORIENT COUNTER','right':'DARK SUIT - CLIP-ON TIE','reel':'TICKET DESK - 1948 - REPRESENTATION'}),
 (4,'gadget',{'g':'ticket'}),
 (7,'gadget',{'g':'typename'}),
 (9,'gadget',{'g':'seatmap'}),
 (11,'winclip',{'label':'CABIN SERVICE - BOURBON & SODA','reel':'ARCHIVE 1958 - REPRESENTATION'}),
 (12,'fullclip',{'label':'FLIGHT 305 - WHEELS UP 2:50 PM','right':'PDX > SEA','reel':'ARCHIVE FILM - REPRESENTATION'}),
 (15,'numpop',{'items':[[0,'36','PASSENGERS'],[1,'6','CREW'],[2,'30 MIN','HOP TO SEATTLE']]}),
 (17,'fullimg',{'img':'note','chips':[[0,'A FOLDED NOTE',''],[1,'FLORENCE SCHAFFNER','FLIGHT ATTENDANT - 23']]}),
 (20,'doc',{'style':'memo','head':'WHAT SHE THOUGHT','lines':[[0,'Just a phone number.'],[1,'It happens all the time.'],[2,'Into the purse. Unread.']]}),
 (22,'quote',{'lines':['MISS, YOU\u2019D BETTER','LOOK AT THAT NOTE.'],'attrib':'- THE MAN IN SEAT 18-E'}),
 (23,'typo',{'style':'mega','lines':[[0,'I HAVE A BOMB.']],'drop':True}),
 (27,'doc',{'style':'felt','head':'THE NOTE - FELT PEN','lines':[[1,'I HAVE A BOMB'],[1.4,'IN MY BRIEFCASE.'],[2,'I WANT YOU'],[3,'TO SIT BY ME.']]}),
 (29,'dark',{'sub':'SHE SITS. SHE ASKS TO SEE IT.'}),
 (33,'gadget',{'g':'briefcase'}),
 (35,'typo',{'style':'big','lines':[[0,'HE CLOSES IT.'],[1,'AND STARTS DICTATING.']],'riser':True}),
],
's2': [
 (0,'dark',{'sub':'THE DEMANDS - SPECIFIC.'}),
 (4,'numpop',{'items':[[0,'$200,000','CASH - BY 5:00 PM - IN A KNAPSACK'],[2,'4','PARACHUTES - TWO FRONT, TWO BACK']]}),
 (6,'quote',{'lines':['NO FUNNY STUFF,','OR I\u2019LL DO THE JOB.'],'attrib':'+ ONE FUEL TRUCK, STANDING BY','red':True}),
 (8,'fullclip',{'label':'SEATTLE - FLIGHT 305 INBOUND','right':'FIRST STRANGE TURN','reel':'SEATTLE 1962 - REPRESENTATION'}),
 (12,'quote',{'lines':['WE\u2019LL SHOW FULL COMPLIANCE.','PAY HIM. WHATEVER HE WANTS.'],'attrib':'- DONALD NYROP - PRESIDENT, NORTHWEST ORIENT'}),
 (13,'typo',{'style':'big','lines':[[0,'$200,000 IS CHEAPER'],[0.35,'THAN A DESTROYED 727.']]}),
 (16,'gadget',{'g':'cash'}),
 (20,'gadget',{'g':'microfilm'}),
 (25,'map',{'mode':'sea'}),
 (26,'fullclip',{'label':'TOUCHDOWN - 5:39 PM','right':'SEATTLE-TACOMA','reel':'ARCHIVE FILM - REPRESENTATION'}),
 (27,'fullclip',{'label':'CASH + 4 CHUTES - UP THE REAR STAIRS','right':'$200,000 ABOARD','reel':'ARCHIVE FILM - REPRESENTATION'}),
 (29,'fullclip',{'label':'ALL 36 PASSENGERS WALK FREE','right':'MOST NEVER KNEW','reel':'ARCHIVE FILM - REPRESENTATION'}),
 (31,'typo',{'style':'big','lines':[[0,'NOW IT IS JUST COOPER'],[1,'AND THE CREW.']],'riser':True}),
],
's3': [
 (1,'doc',{'style':'memo','head':'FLIGHT INSTRUCTIONS - PRECISE','lines':[[1,'\u201cTHIS MAN KNOWS AIRCRAFT.\u201d']]}),
 (7,'gadget',{'g':'checklist'}),
 (10,'quote',{'lines':['FINE.','REFUEL IN RENO.'],'attrib':'- COOPER, WHEN TOLD MEXICO WAS IMPOSSIBLE'}),
 (12,'fullclip',{'label':'CLIMB-OUT 7:36 PM - INTO THE STORM','right':'DEST: RENO','reel':'ARCHIVE FILM - REPRESENTATION'}),
 (14,'fullimg',{'img':'seat','dark':True,'chips':[[1,'TYING SOMETHING','AROUND HIS WAIST'],[1.5,'THE MONEY BAG','']]}),
 (17,'gadget',{'g':'warnlight'}),
 (18,'fullimg',{'img':'stairs','dark':True,'wind':True,'chips':[[0,'AFT STAIRS - OPEN','10,000 FT']]}),
 (21,'numpop',{'items':[[0,'200+ MPH','WIND PAST THE STAIRS'],[1,'FREEZING','RAIN'],[2,'TOTAL','DARKNESS BELOW']]}),
 (24,'gadget',{'g':'bump'}),
 (26,'storm',{}),
 (30,'gadget',{'g':'radar'}),
 (32,'typo',{'style':'mega','lines':[[1,'EMPTY.']]}),
 (33,'gadget',{'g':'evidence'}),
 (34,'typo',{'style':'big','lines':[[0,'DAN COOPER'],[0.4,'WAS GONE.']],'fade':True}),
],
's4': [
 (3,'typo',{'style':'big','lines':[[1,'D.B. COOPER'],[1.3,'IS NOT HIS NAME.'],[3,'THE TICKET SAID: DAN.']]}),
 (6,'typo',{'style':'big','lines':[[0,'SO WHERE DID \u201cD.B.\u201d COME FROM?'],[1,'A MISTAKE.'],[2,'MADE ON DEADLINE.']]}),
 (9,'doc',{'style':'tele','head':'POLICE BLOTTER - NIGHT ONE','lines':[[0,'LOCAL MAN CHECKED: RECORD ON FILE'],[1,'NAME: D.B. COOPER'],[2,'STATUS: CLEARED IMMEDIATELY']],'stamp':['CLEARED',2]}),
 (10,'doc',{'style':'tele','head':'WIRE DESK - JAMES LONG, ON DEADLINE','lines':[[0.3,'REPORTER RACES THE CLOCK...'],[0.6,'WRONG NAME GOES OUT ON THE WIRE'],[0.9,'>> D.B. COOPER <<']]}),
 (14,'gadget',{'g':'headlines'}),
 (17,'doc',{'style':'file','head':'FBI CASE FILE','lines':[[0,'SUBJECT NAME: UNKNOWN'],[1,'CODENAME: NORJAK'],[2,'(NORTHWEST HIJACKING)']]}),
 (19,'typo',{'style':'big','lines':[[0,'THE WRONG NAME'],[0.4,'BECAME A LEGEND.']]}),
 (23,'typo',{'style':'ledger','lines':[[1,'THE NAME - AN ERROR.'],[2,'THE SKETCH - A GUESS.'],[3,'THE IDENTITY - A BLANK.']]}),
 (24,'doc',{'style':'file','head':'THE ONLY HARD EVIDENCE','lines':[[0.3,'10,000 SERIAL NUMBERS'],[0.7,'SITTING IN A FILE.'],[0.95,'WAITING.']]}),
],
's5': [
 (4,'map',{'mode':'zone'}),
 (6,'fullimg',{'img':'search2','chips':[[0,'18 DAYS','AGENTS + SOLDIERS'],[1,'400 TROOPS','SENT BACK IN SPRING']]}),
 (7,'winclip',{'label':'ON FOOT - HELICOPTERS - A SUBMARINE','reel':'PACIFIC NORTHWEST 1953 - REPRESENTATION'}),
 (12,'typo',{'style':'ledger','lines':[[1,'NO PARACHUTE.'],[2,'NO BODY.'],[3,'NO MONEY.'],[4,'NOT ONE SHRED.']]}),
 (14,'typo',{'style':'big','lines':[[0,'COULD ANYONE SURVIVE THAT?'],[1,'RUN THE NUMBERS.']]}),
 (21,'numpop',{'items':[[0,'10,000 FT','NIGHT JUMP'],[2,'-7 C','BEFORE WIND CHILL'],[4,'BLIND','CLOUD LAYER AT 5,000 FT'],[5,'SEWN SHUT','HIS RESERVE WAS A DUMMY'],[6,'100 FT','TREES + FROZEN LAKES']]}),
 (22,'typo',{'style':'big','lines':[[0,'EXPERTS: SURVIVAL'],[0.35,'CLOSE TO IMPOSSIBLE.']]}),
 (24,'typo',{'style':'big','lines':[[0,'BUT WITHIN MONTHS -'],[1,'FIVE COPYCATS JUMPED.']]}),
 (26,'gadget',{'g':'mccoydive'}),
 (29,'typo',{'style':'big','lines':[[0,'IMPOSSIBLE? NO.'],[2,'JUST VERY, VERY UNLIKELY.']]}),
 (32,'gadget',{'g':'doors'}),
 (34,'typo',{'style':'big','lines':[[0,'NINE YEARS. NOTHING.'],[1,'THEN A SIX-YEAR-OLD'],[1.45,'WENT CAMPING.']],'riser':True}),
],
's6': [
 (1,'fullimg',{'img':'tenabar_scene','chips':[[0,'FEBRUARY 10, 1980',''],[1,'TENA BAR','COLUMBIA RIVER']]}),
 (3,'fullimg',{'img':'tenabar','chips':[[0,'BRIAN INGRAM','CLEARING A CAMPFIRE SPOT'],[1,'3 INCHES DOWN','HIS HAND HITS PAPER']]}),
 (8,'fullimg',{'img':'bills','chips':[[1,'ROTTED','FUSED TOGETHER'],[3,'RUBBER BANDS','STILL WRAPPED'],[4,'$5,800','IN TWENTIES']]}),
 (13,'gadget',{'g':'match'}),
 (15,'typo',{'style':'big','lines':[[0,'$5,800 - COOPER\u2019S RANSOM.'],[1,'THE FIRST PHYSICAL TRACE.']]}),
 (20,'map',{'mode':'river'}),
 (25,'typo',{'style':'ledger','lines':[[1,'LOST IT?'],[2,'BURIED IT?'],[3,'SOMEONE ELSE?'],[4,'NOBODY KNOWS.']]}),
 (28,'doc',{'style':'file','head':'AUCTION - 2008','lines':[[0,'15 RUINED BILLS'],[1,'SOLD: $37,000'],[2,'TRIPLE FACE VALUE, FOR MONEY THAT FAILED']]}),
 (29,'dark',{'sub':'THE PART THAT KEEPS INVESTIGATORS AWAKE -'}),
 (35,'gadget',{'g':'ticker'}),
 (37,'typo',{'style':'mega','lines':[[0,'THE MONEY DID NOT DISAPPEAR.'],[1,'IT STOPPED EXISTING.']],'fade':True}),
],
's7a': [
 (2,'gadget',{'g':'tie'}),
 (4,'doc',{'style':'file','head':'DNA - 2001','lines':[[0,'PARTIAL PROFILE PULLED FROM TIE'],[1,'RESULT: NO MATCH']],'stamp':['NO MATCH',1]}),
 (7,'gadget',{'g':'microscope'}),
 (11,'typo',{'style':'big','lines':[[0,'1971: ALMOST NOBODY'],[0.35,'HANDLED TITANIUM.'],[1,'AEROSPACE.'],[2,'CHEMICAL PLANTS.'],[3,'BOEING CONTRACTORS.']]}),
 (17,'gadget',{'g':'profile'}),
 (19,'typo',{'style':'big','lines':[[0,'THE SUSPECTS.'],[1,'800+ SERIOUS FILES.']]}),
 (27,'doc',{'style':'suspect','head':'SUSPECT 01 - RICHARD McCOY','lines':[[2,'THE COPYCAT - SAME METHOD, $500,000'],[4,'VIETNAM VETERAN'],[5,'HELICOPTER PILOT'],[6,'SKYDIVER'],[7,'ARRESTED IN TWO DAYS']]}),
 (30,'doc',{'style':'file','head':'McCOY - ENDGAME','lines':[[0,'NEVER ADMITTED HE WAS COOPER'],[1,'ESCAPED PRISON WITH A FAKE GUN'],[1.5,'KILLED IN FBI SHOOTOUT'],[2,'AGENTS BELIEVED HE WAS THE ANSWER']]}),
 (34,'doc',{'style':'suspect','head':'FBI VERDICT - McCOY','lines':[[0,'ALIBI: LAS VEGAS, THAT DAY'],[1,'CREW: \u201cTHE FACE IS WRONG\u201d'],[2,'TOO YOUNG']],'stamp':['NOT HIM',2]}),
],
's7b': [
 (5,'doc',{'style':'suspect','head':'SUSPECT 02 - ROBERT RACKSTRAW','lines':[[1,'ARMY VETERAN'],[2,'PILOT'],[3,'EXPLOSIVES TRAINING'],[4,'FACE MATCHED THE SKETCH']]}),
 (7,'doc',{'style':'file','head':'THE COLBERT TEAM','lines':[[0,'40 RETIRED INVESTIGATORS'],[0.5,'YEARS BUILDING THE CASE'],[1,'CLAIM: HIDDEN CONFESSIONS IN HIS LETTERS']]}),
 (11,'doc',{'style':'file','head':'RACKSTRAW - THE RECORD','lines':[[0,'FBI LOOKED AT HIM IN THE 70s'],[0.6,'AND DROPPED HIM'],[1,'DENIED EVERYTHING UNTIL 2019'],[2,'\u201cMY LIFE WAS RUINED BY A THEORY.\u201d']]}),
 (13,'quote',{'lines':['I\u2019M DAN COOPER.'],'attrib':'- DUANE WEBER, ALLEGED DEATHBED WHISPER - DNA: NO MATCH','red':True}),
 (15,'doc',{'style':'suspect','head':'ALSO IN THE FILE','lines':[[0,'KENNETH CHRISTIANSEN - NW EMPLOYEE, PARATROOPER'],[0.6,'(HIS OWN BROTHER SUSPECTED HIM)'],[1,'SHERIDAN PETERSON - BOEING, SMOKEJUMPER']]}),
 (17,'typo',{'style':'big','lines':[[0,'EVERY SUSPECT FITS HALFWAY.'],[1,'NOT ONE FITS WHOLE.']]}),
 (20,'gadget',{'g':'closed'}),
 (23,'doc',{'style':'file','head':'THE VAULT - WASHINGTON','lines':[[0,'ALL EVIDENCE: SEALED'],[1,'FILE OPEN EXACTLY ONE INCH'],[2,'FOR ONE THING ONLY: THE MONEY.']]}),
],
's8': [
 (2,'typo',{'style':'big','lines':[[0,'NOVEMBER 24, 1971.'],[1,'YOU NOW KNOW WHAT THE FBI KNOWS.'],[2,'THREE POSSIBILITIES.']]}),
 (8,'verdict',{'k':'A','title':'COOPER DIED IN THE JUMP','pro':'EXPLAINS THE SILENCE + MISSING MONEY','con':[[4,'WHERE IS THE PARACHUTE?'],[5,'WHERE ARE THE BONES?'],[6,'400 TROOPS FOUND NOTHING']]}),
 (13,'verdict',{'k':'B','title':'COOPER GOT AWAY WITH IT','pro':'EXPLAINS THE EMPTY FOREST','con':[[3,'WHY WAS THE MONEY BURIED UPSTREAM?'],[4,'WHY NEVER SPEND A SINGLE BILL?']]}),
 (18,'verdict',{'k':'C','title':'SOMEONE WE ALREADY MET','pro':'McCOY - RACKSTRAW - 800 FILES','con':[[4,'THE PROOF DIED WITH HIM.']]}),
 (20,'typo',{'style':'big','lines':[[0,'PICK ONE.'],[1,'WHICHEVER YOU CHOOSE, YOU MUST'],[1.4,'IGNORE ONE PIECE OF EVIDENCE.']]}),
 (21,'typo',{'style':'big','lines':[[0,'THAT IS WHY THIS CASE'],[0.4,'CANNOT CLOSE.']]}),
 (26,'typo',{'style':'ledger','lines':[[0,'ONE MAN.'],[1,'ONE NIGHT.'],[2,'ONE JUMP INTO A STORM.'],[3,'FIFTY-FIVE YEARS.']]}),
 (27,'dark',{'sub':'THE ONLY CERTAINTY: NOTHING IS CERTAIN.','drop':True}),
 (29,'finale',{}),
],
}

beats=[]; caps=[]
for s in order:
    sents=M[s]['sents']; v=vo[s]; prev=-1; t0=starts[s]
    for (last,tr,p) in SPEC[s]:
        idxs=list(range(prev+1,last+1))
        se=[round(v+sents[i]['end'],2) for i in idxs]
        ss=[]
        for i in idxs:
            st = v+sents[i-1]['end']+0.12 if i>0 else v+0.05
            ss.append(round(max(st, t0),2))
        t1 = round(se[-1]+ (0.28 if tr not in ('typo','dark') else 0.22),2)
        if (last==len(sents)-1): t1 = starts[order[order.index(s)+1]] if s!='s8' else TOTAL
        beats.append({'sec':s,'tr':tr,'p':p,'t0':round(t0,2),'t1':round(t1,2),'ss':ss,'se':se,
                      'txt':[sents[i]['t'] for i in idxs]})
        for k,i in enumerate(idxs):
            caps.append({'t0':ss[k],'t1':min(se[k]+0.9, t1),'txt':sents[i]['t']})
        prev=last; t0=t1
json.dump({'TOTAL':TOTAL,'starts':starts,'vo':vo,'beats':beats},open('/var/tmp/v8build/beats.json','w'))
json.dump(caps,open('/var/tmp/v8build/caps.json','w'))
print('TOTAL',TOTAL,'beats:',len(beats),'caps:',len(caps))
ev=len(beats)
for b in beats:
    p=b['p']
    ev += len(p.get('chips',[]))+len(p.get('items',[]))+len(p.get('lines',[]))+len(p.get('con',[]))
print('visual events (ex-s0):',ev,'per min:',round(ev/((TOTAL-40.1)/60),1))
bad=[(b['sec'],b['tr'],round(b['t1']-b['t0'],2)) for b in beats if b['t1']-b['t0']<1.0 or b['t1']-b['t0']>13]
print('suspect durations:',bad)
