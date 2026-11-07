#!/usr/bin/env python3
# dbclong engine v3: beat-sync shot system + chapters + scenes + maps
p='/home/user/explainer-pipeline/assets/dbclong/dbclong.html'
s=open(p).read()
def rep(a,b,tag):
    global s
    assert a in s, 'MISS '+tag
    s=s.replace(a,b,1)

# 1) scene images into srcs
rep("planeCut:'../dbc02/plane_cut.png',",
    "planeCut:'../dbc02/plane_cut.png',scCounter:'scene_counter.jpg',scSeat:'scene_seat.jpg',scNote:'scene_note.jpg',scTarmac:'scene_tarmac.jpg',scStairs:'scene_stairs.jpg',scJump:'scene_jump.jpg',scSearch:'scene_search.jpg',scTena:'scene_tenabar.jpg',",'srcs')

# 2) setTL computes per-section sentence times
rep("let TL=null;window.setTL=j=>{TL=j;};",
    "let TL=null,SN=null;window.setTL=j=>{TL=j;SN=TL.s.map((sc,i)=>(TL.caps||[]).filter(c=>c.a>=sc.t0-0.01&&c.a<sc.t0+sc.dur));};\n"
    "function SNr(i,j){if(!SN||!SN[i]||!SN[i].length)return 0;const c=SN[i][Math.min(j,SN[i].length-1)];return c.a-TL.s[i].t0;}",'setTL')

# 3) v3 helpers before SECTION 1 comment
HELP=r'''
// ========== V3 SHOT SYSTEM ==========
function runShots(i,u,D,shots){
  const st=shots.map(sh=>sh.s<0?0:SNr(i,sh.s));
  let k=shots.length-1;while(k>0&&u<st[k])k--;
  const a=st[k],b=(k<shots.length-1?st[k+1]:D);
  const q=Math.max(0,Math.min(1,(u-a)/Math.max(0.001,b-a)));
  shots[k].d(q,u-a);
  if(u-a<0.28&&k>0){X.fillStyle='rgba(6,7,9,'+(0.7*(1-(u-a)/0.28))+')';X.fillRect(0,0,W,H);}
}
function SCN(im,q,label,sub){
  X.save();const z=1.05+0.09*ss(q);
  X.translate(W/2,H/2);X.scale(z,z);X.translate(-W/2,-H/2);
  X.filter='contrast(1.06) saturate(0.8) brightness(0.9)';
  if(im)cover(im,0,0,W,H);X.filter='none';X.restore();
  const g=X.createLinearGradient(0,0,0,300);g.addColorStop(0,'rgba(5,6,8,0.8)');g.addColorStop(1,'rgba(5,6,8,0)');
  X.fillStyle=g;X.fillRect(0,0,W,300);
  if(label){X.fillStyle=RED;X.fillRect(90,86,8,60);
    X.font='900 42px InterB';X.fillStyle=TXT;X.fillText(label,120,118);
    if(sub){X.font='700 25px JBM';X.fillStyle=SEC;X.fillText(sub,120,160);}}
}
function CHAP(n,t1,t2,u){if(u>2.4)return;const fo=u>1.9?Math.max(0,1-(u-1.9)/0.5):1;
  X.globalAlpha=fo;X.fillStyle='#07080A';X.fillRect(0,0,W,H);
  X.strokeStyle=HAIR;X.lineWidth=2;X.beginPath();X.moveTo(W/2-320,H/2-96);X.lineTo(W/2+320,H/2-96);X.stroke();
  X.textAlign='center';X.fillStyle=RED;X.font='700 36px JBM';
  X.fillText('CHAPTER 0'+n,W/2,H/2-130);
  const sc2=u<0.35?1.25-0.25*EB(u/0.35):1;
  X.save();X.translate(W/2,H/2+10);X.scale(sc2,sc2);
  X.fillStyle=TXT;X.font='900 124px InterB';X.fillText(t1,0,30);X.restore();
  if(t2){X.font='700 28px JBM';X.fillStyle=SEC;X.fillText(t2,W/2,H/2+120);}
  X.textAlign='left';X.globalAlpha=1;}
function mapBase(tag){X.fillStyle='#0E1013';X.fillRect(0,0,W,H);
  X.strokeStyle='rgba(46,50,56,0.45)';X.lineWidth=1;
  for(let gx=48;gx<W;gx+=96){X.beginPath();X.moveTo(gx,0);X.lineTo(gx,H);X.stroke();}
  for(let gy=24;gy<H;gy+=96){X.beginPath();X.moveTo(0,gy);X.lineTo(W,gy);X.stroke();}
  X.strokeStyle='rgba(139,144,151,0.3)';X.lineWidth=3;X.beginPath();X.moveTo(430,0);
  for(let yy=0;yy<=H;yy+=40)X.lineTo(430+Math.sin(yy*0.013)*70+R(yy)*18,yy);X.stroke();
  X.font='700 22px JBM';X.fillStyle='rgba(139,144,151,0.6)';
  X.fillText(tag||'PACIFIC NORTHWEST · OPERATIONAL CHART — SCHEMATIC',90,66);}
function cityDot(x,y,name,side){X.fillStyle=TXT;X.beginPath();X.arc(x,y,9,0,7);X.fill();
  X.strokeStyle='rgba(236,234,228,0.4)';X.lineWidth=2;X.beginPath();X.arc(x,y,19,0,7);X.stroke();
  X.font='900 32px InterB';X.fillStyle=TXT;
  X.fillText(name,side<0?x-X.measureText(name).width-30:x+30,y+11);}
function planeTri(x,y,ang){X.save();X.translate(x,y);X.rotate(ang);
  X.fillStyle=RED;X.beginPath();X.moveTo(18,0);X.lineTo(-12,-11);X.lineTo(-6,0);X.lineTo(-12,11);X.closePath();X.fill();X.restore();}
const SEAp=[930,250],PDXp=[780,840];
function routeLine(ax,ay,bx,by,q,col){X.strokeStyle=col||RED;X.lineWidth=5;X.setLineDash([16,12]);
  X.beginPath();X.moveTo(ax,ay);X.lineTo(ax+(bx-ax)*q,ay+(by-ay)*q);X.stroke();X.setLineDash([]);
  return [ax+(bx-ax)*q,ay+(by-ay)*q,Math.atan2(by-ay,bx-ax)];}
function bigCount(val,label,y,p,pre){if(p<=0)return;const v=Math.floor(val*Math.min(1,E(p)));
  X.textAlign='center';X.font='900 170px InterB';X.fillStyle=TXT;
  X.fillText((pre||'')+v.toLocaleString('en-US'),W/2,y);
  X.font='700 32px JBM';X.fillStyle=SEC;X.fillText(label,W/2,y+64);X.textAlign='left';}
function silCard(x,y,name,sub,p,col){if(p<=0)return;paperCard(x,y,420,560,0.01*(R(x)-0.5),p);
  if(p>0.5){X.fillStyle='#2a2username620';X.fillStyle='#262219';
    X.beginPath();X.arc(x+210,y+170,85,0,7);X.fill();
    X.beginPath();X.ellipse(x+210,y+330,130,85,0,Math.PI,0);X.fill();
    X.fillStyle=INK;X.font='900 34px InterB';X.textAlign='center';
    X.fillText(name,x+210,y+440);
    X.font='700 22px JBM';X.fillStyle='#55504a';X.fillText(sub,x+210,y+478);
    X.textAlign='left';
    }}
'''
rep("// ---------- SECTION 1: cold open dossier desk ----------",HELP+"\n// ---------- SECTION 1: cold open dossier desk ----------",'helpers')

# 4) sec1 inserts: note scene + jump scene
rep("  // plane photo",
"""  const sn6=SNr(0,6);
  if(u>sn6&&u<F(0.47)){photoCard(IMGS.scNote,70,500,660,430,-0.025,E((u-sn6)/0.6),'20:05 — THE NOTE · RECONSTRUCTION',null);}
  // plane photo""",'sec1-note')
rep("  // GONE",
"""  const sj=SNr(0,11);
  if(u>sj&&u<F(0.70)){SCN(IMGS.scJump,Math.min(1,(u-sj)/9),'10,000 FEET · FREEZING STORM','SOMEWHERE OVER SOUTHWEST WASHINGTON');
    redChip('$200,000 TIED TO HIS BODY',120,H-200,E((u-sj-2.2)/0.5));}
  // GONE""",'sec1-jump')

# 5) replace sec2..sec6 wholesale
i0=s.index('// ---------- SECTION 2')
i1=s.index('const SECF=[')
NEW=r'''// ========== SECTION 2: THE HIJACK ==========
function sec2(u,D){
  const t0=TL.s[1].t0,S=j=>SNr(1,j);
  runShots(1,u,D,[
   {s:-1,d:(q,lu)=>{ // map route PDX->SEA
     mapBase();cityDot(SEAp[0],SEAp[1],'SEATTLE',1);cityDot(PDXp[0],PDXp[1],'PORTLAND',1);
     const tip=routeLine(PDXp[0],PDXp[1],SEAp[0],SEAp[1],Math.min(1,lu/6));
     planeTri(tip[0],tip[1],tip[2]);
     clockChip('FLIGHT 305 · 30 MINUTE HOP',90,H-220,E(lu/0.6));
     redChip('36 PASSENGERS · ZERO SUSPICION',90,H-150,E((u-S(1))/0.5));}},
   {s:3,d:(q,lu)=>{ // briefcase
     SCN(IMGS.scSeat,q,'SEAT 18-E','HE OPENS THE BRIEFCASE — JUST ENOUGH');
     redChip('WIRES · BATTERY · RED CYLINDERS',120,206,E((lu-1.2)/0.5));}},
   {s:4,d:(q,lu)=>{ // demands doc
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     paperCard(W/2-520,140,1040,760,-0.008,E(lu/0.6));
     if(lu>0.5){X.fillStyle=INK;X.font='900 54px InterB';X.fillText('THE DEMANDS',W/2-430,280);
       X.strokeStyle='#b3261a';X.lineWidth=3;X.beginPath();X.moveTo(W/2-430,305);X.lineTo(W/2+70,305);X.stroke();
       typeTxt('1.  $200,000 — NEGOTIABLE AMERICAN CURRENCY',W/2-430,400,t0+S(5),34,'700 34px JBM','#3a3326');
       typeTxt('2.  FOUR PARACHUTES — TWO FRONT, TWO BACK',W/2-430,490,t0+S(6),34,'700 34px JBM','#3a3326');
       typeTxt('3.  FUEL TRUCK — WAITING IN SEATTLE',W/2-430,580,t0+S(7),34,'700 34px JBM','#3a3326');
       stamp('PRECISE',W/2+320,250,-0.12,E((lu-0.9)/0.4),'rgba(179,38,26,0.85)',{w:300,h:84,f:40});}}},
   {s:8,d:(q,lu)=>{ // circling
     mapBase();cityDot(SEAp[0],SEAp[1],'SEATTLE',1);
     X.font='700 26px JBM';X.fillStyle=SEC;X.fillText('PUGET SOUND',SEAp[0]-420,SEAp[1]+160);
     X.strokeStyle='rgba(255,74,46,0.5)';X.lineWidth=4;X.setLineDash([14,10]);
     X.beginPath();X.ellipse(SEAp[0]-120,SEAp[1]+120,300,160,0.2,0,Math.min(6.28,lu*1.1));X.stroke();X.setLineDash([]);
     const a=lu*1.1,px=SEAp[0]-120+300*Math.cos(a+0.2),py=SEAp[1]+120+160*Math.sin(a+0.2);
     planeTri(px,py,a+Math.PI/2);
     clockChip('TWO HOURS OF LOOPS',90,H-220,E(lu/0.5));
     redChip('BELOW: FBI ASSEMBLES $200,000',90,H-150,E((lu-2)/0.5));}},
   {s:10,d:(q,lu)=>{ // bourbon
     SCN(IMGS.scSeat,q,'CALM. POLITE. UNHURRIED.',null);
     clockChip('BOURBON AND SODA — HE PAID',120,190,E((lu-0.4)/0.4));
     redChip('HE EVEN OFFERED A TIP',120,260,E((u-S(12))/0.4));}},
   {s:13,d:(q,lu)=>{ // landing
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.p727f,W/2-620,160,1240,640,0.012,E(lu/0.6),'NORTHWEST ORIENT · BOEING 727','17:39 · SEA-TAC RUNWAY');
     stamp('MECHANICAL DELAY',W/2+300,760,-0.08,E((u-S(14))/0.4),'rgba(179,38,26,0.8)',{w:560,h:90,f:40});}},
   {s:15,d:(q,lu)=>{ // exchange
     SCN(IMGS.scTarmac,q,'THE EXCHANGE','PASSENGERS OUT · MONEY AND PARACHUTES IN');
     redChip('10,000 TWENTY-DOLLAR BILLS',120,206,E((lu-1.5)/0.5));}},
   {s:16,d:(q,lu)=>{ // serials
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.money,W/2-760,220,700,470,-0.02,E(lu/0.5),'THE RANSOM · FBI PHOTOGRAPH',null);
     X.fillStyle=PAN;X.fillRect(W/2+40,220,700,470);X.strokeStyle=HAIR;X.strokeRect(W/2+40,220,700,470);
     if(lu>0.5){typeTxt('EVERY BILL → ONE CAMERA',W/2+90,310,t0+S(17),30,'900 40px InterB',TXT);
       bigCountR(10000,'SERIAL NUMBERS PHOTOGRAPHED',W/2+390,470,E((u-S(18))/2.5));
       redChip('ONE BILL SURFACES = THEY KNOW',W/2+90,610,E((u-S(19))/0.5));}}},
  ]);
  CHAP(1,'THE HIJACK','FLIGHT 305 · NOVEMBER 24, 1971',u);
  grainPass(0.045);vig(0.42);}
function bigCountR(val,label,x,y,p){if(p<=0)return;const v=Math.floor(val*Math.min(1,E(p)));
  X.textAlign='center';X.font='900 120px InterB';X.fillStyle=TXT;X.fillText(v.toLocaleString('en-US'),x,y);
  X.font='700 26px JBM';X.fillStyle=SEC;X.fillText(label,x,y+52);X.textAlign='left';}
// ========== SECTION 3: THE JUMP ==========
function sec3(u,D){
  const t0=TL.s[2].t0,S=j=>SNr(2,j);
  runShots(2,u,D,[
   {s:-1,d:(q,lu)=>{ // night departure
     mapBase('AIRBORNE · 19:36 — “DESTINATION: MEXICO CITY”');
     cityDot(SEAp[0],SEAp[1],'SEATTLE',1);
     const tip=routeLine(SEAp[0],SEAp[1],1060,1040,Math.min(1,lu/8),'rgba(255,74,46,0.9)');
     planeTri(tip[0],tip[1],tip[2]);
     X.font='700 26px JBM';X.fillStyle=SEC;X.fillText('VICTOR-23 AIRWAY',SEAp[0]+90,620);
     clockChip('ALT 10,000 FT · FLAPS 15 · GEAR DOWN',90,H-220,E((lu-1)/0.5));
     redChip('CABIN UNPRESSURIZED · ONE PASSENGER AFT',90,H-150,E((u-S(2))/0.5));}},
   {s:3,d:(q,lu)=>{ // warning light
     X.fillStyle='#070809';X.fillRect(0,0,W,H);
     X.fillStyle=PAN;X.fillRect(W/2-560,H/2-240,1120,480);X.strokeStyle=HAIR;X.strokeRect(W/2-560,H/2-240,1120,480);
     const on=Math.floor(T*3)%2===0;
     X.fillStyle=on?RED:'#3a1410';X.beginPath();X.arc(W/2-330,H/2-40,70,0,7);X.fill();
     if(on){X.shadowColor=RED;X.shadowBlur=60;X.beginPath();X.arc(W/2-330,H/2-40,70,0,7);X.fill();X.shadowColor='transparent';}
     X.font='900 56px InterB';X.fillStyle=TXT;X.fillText('AFT STAIRS',W/2-170,H/2-60);
     X.font='700 30px JBM';X.fillStyle=SEC;X.fillText('20:00 — A LIGHT THE CREW HAD',W/2-170,H/2+10);
     X.fillText('NEVER SEEN IN FLIGHT',W/2-170,H/2+54);
     redChip('THE REAR STAIRWAY IS OPEN',W/2-330,H/2+140,E((u-S(4))/0.5));}},
   {s:5,d:(q,lu)=>{ // intercom
     SCN(IMGS.scStairs,q,null,null);
     X.fillStyle='rgba(6,7,9,0.55)';X.fillRect(0,0,W,H);
     paperCard(W/2-540,H/2-200,1080,220,-0.006,E(lu/0.4));
     if(lu>0.3)typeTxt('COCKPIT:  “IS THERE ANYTHING WE CAN DO FOR YOU?”',W/2-480,H/2-80,t0+S(5)+0.3,36,'700 34px JBM','#3a3326');
     if(u>S(6)){const bp=u<S(6)+0.3?2.0-1.0*EB((u-S(6))/0.3):1;
       X.save();X.translate(W/2,H/2+170);X.scale(bp,bp);
       X.font='900 180px InterB';X.fillStyle=TXT;X.textAlign='center';X.fillText('“NO.”',0,60);
       X.textAlign='left';X.restore();}}},
   {s:8,d:(q,lu)=>{ // 13 min silence
     X.fillStyle='#050608';X.fillRect(0,0,W,H);
     const mm=Math.min(13,Math.floor(lu/((SNr(2,9)-SNr(2,8))||4)*13));
     X.textAlign='center';X.font='900 230px InterB';X.fillStyle=TXT;
     X.fillText('20:'+String(mm).padStart(2,'0'),W/2,H/2+40);
     X.font='700 34px JBM';X.fillStyle=SEC;X.fillText('THIRTEEN MINUTES OF SILENCE',W/2,H/2+140);
     X.textAlign='left';
     X.strokeStyle='rgba(139,144,151,0.5)';X.lineWidth=3;X.beginPath();
     for(let xx=0;xx<W;xx+=8){X.lineTo(xx,H-200+(R(xx)*2-1)*2);}X.stroke();}},
   {s:9,d:(q,lu)=>{ // pressure bump
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     X.fillStyle=PAN;X.fillRect(160,200,W-320,560);X.strokeStyle=HAIR;X.strokeRect(160,200,W-320,560);
     X.font='700 26px JBM';X.fillStyle=SEC;X.fillText('CABIN PRESSURE TRACE — 20:13:00',200,260);
     X.strokeStyle=TXT;X.lineWidth=4;X.beginPath();
     const sp=Math.min(1,lu/2.5);
     for(let xx=0;xx<=(W-400)*sp;xx+=6){const px=200+xx;
       let py=520+Math.sin(xx*0.02)*6;
       const bx=(W-400)*0.55;
       if(xx>bx&&xx<bx+90)py+=Math.sin((xx-bx)/90*Math.PI)*170;
       X.lineTo(px,py);}X.stroke();
     if(sp>0.56){X.fillStyle=RED;X.font='900 44px InterB';X.fillText('20:13',200+(W-400)*0.55-40,420);}
     clockChip('NOSE DIPPED',200,800,E((u-S(10))/0.4));
     clockChip('TAIL ROSE',480,800,E((u-S(11))/0.4));
     redChip('AIRCRAFT SUDDENLY ~200 LBS LIGHTER',720,800,E((u-S(12))/0.5));}},
   {s:13,d:(q,lu)=>{ // the jump
     SCN(IMGS.scJump,q,'INTO THE STORM','FREEZING RAIN · TOTAL DARKNESS');
     redChip('TWO F-106 FIGHTERS SHADOWING — SAW NOTHING',120,206,E((u-S(14))/0.5));}},
   {s:15,d:(q,lu)=>{ // reno empty
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.p727,W/2-620,150,1240,620,-0.01,E(lu/0.5),'RENO, NEVADA · 22:15','FEDERAL AGENTS STORM THE AIRCRAFT');
     stamp('CABIN EMPTY',W/2-280,420,-0.1,E((lu-1.2)/0.4),'rgba(179,38,26,0.85)',{w:460,h:96,f:46});
     clockChip('THE MONEY — GONE',W/2-600,830,E((u-S(16))/0.4));
     clockChip('TWO PARACHUTES — GONE',W/2-240,830,E((u-S(17))/0.4));
     redChip('DAN COOPER — GONE',W/2+260,830,E((u-S(18))/0.4));}},
  ]);
  CHAP(2,'THE JUMP','20:13 PM · SOMEWHERE OVER WASHINGTON',u);
  grainPass(0.05);vig(0.45);}
// ========== SECTION 4: THE MANHUNT ==========
function sec4(u,D){
  const t0=TL.s[3].t0,S=j=>SNr(3,j);
  runShots(3,u,D,[
   {s:-1,d:(q,lu)=>{
     desk();
     X.save();X.translate(W/2,H/2);X.rotate(-0.01);X.translate(-W/2,-H/2);
     X.fillStyle=MANILA;X.fillRect(W/2-560,H/2-320,1120,640);X.restore();
     stamp('NORJAK',W/2,H/2-80,-0.06,E((u-S(1))/0.4),'rgba(179,38,26,0.9)',{w:620,h:150,f:86});
     typeTxt('NORTHWEST HIJACKING — FBI CASE 164-81',W/2-430,H/2+120,t0+S(1)+1.0,34,'700 32px JBM','#5c5138');
     clockChip('THE LARGEST MANHUNT IN FBI HISTORY',W/2-430,H/2+180,E(lu/0.6));}},
   {s:2,d:(q,lu)=>{
     SCN(IMGS.scSearch,q,'THE DROP ZONE · LEWIS RIVER','ELBOW TO ELBOW · RAIN AND MUD');
     clockChip('18 DAYS · HUNDREDS OF SOLDIERS',120,196,E((lu-1.5)/0.5));
     stamp('NOTHING',W-430,H-320,-0.1,E((u-S(3))/0.4),'rgba(179,38,26,0.9)',{w:380,h:96,f:52});}},
   {s:4,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     bigCount(400,'TROOPS · SPRING 1972 · 40 MORE DAYS',H/2-60,E(lu/2));
     stamp('NOT A BOOT',W/2-480,H/2+180,-0.07,E((u-S(6))/0.35),'rgba(179,38,26,0.85)',{w:400,h:86,f:42});
     stamp('NOT A CHUTE',W/2,H/2+210,0.05,E((u-S(7))/0.35),'rgba(179,38,26,0.85)',{w:430,h:86,f:42});
     stamp('NOT ONE BILL',W/2+480,H/2+170,-0.04,E((u-S(8))/0.35),'rgba(179,38,26,0.85)',{w:450,h:86,f:42});}},
   {s:9,d:(q,lu)=>{ // evidence light table
     X.fillStyle='#F7F9FB';X.fillRect(0,0,W,H);
     X.fillStyle='#0c0d0f';X.font='900 46px InterB';X.fillText('WHAT HE LEFT BEHIND',120,140);
     X.fillStyle='#FF5A1F';X.fillRect(120,160,220,6);
     // tie card
    if(lu>0.3){X.save();X.translate(300,560);X.rotate(-0.03);
     X.fillStyle='#fff';X.shadowColor='rgba(0,0,0,0.18)';X.shadowBlur=24;X.fillRect(-170,-260,340,520);X.shadowColor='transparent';
     X.fillStyle='#17181b';X.beginPath();X.moveTo(0,-180);X.lineTo(44,-120);X.lineTo(26,140);X.lineTo(0,190);X.lineTo(-26,140);X.lineTo(-44,-120);X.closePath();X.fill();
     X.fillStyle='#101114';X.beginPath();X.moveTo(0,-180);X.lineTo(30,-150);X.lineTo(0,-120);X.lineTo(-30,-150);X.closePath();X.fill();
     X.fillStyle='#55504a';X.font='700 22px JBM';X.textAlign='center';X.fillText('CLIP-ON TIE · J.C. PENNEY',0,230);X.textAlign='left';X.restore();}
     // butts card
    if(u>S(12)){X.save();X.translate(830,560);X.rotate(0.02);
     X.fillStyle='#fff';X.shadowColor='rgba(0,0,0,0.18)';X.shadowBlur=24;X.fillRect(-200,-200,400,400);X.shadowColor='transparent';
     for(let i=0;i<8;i++){X.save();X.translate(-120+(i%4)*80,-60+Math.floor(i/4)*90);X.rotate((R(i)-0.5)*0.6);
       X.fillStyle='#d8d2c4';X.fillRect(-36,-9,72,18);X.fillStyle='#b98a52';X.fillRect(16,-9,20,18);X.restore();}
     X.fillStyle='#55504a';X.font='700 22px JBM';X.textAlign='center';X.fillText('8 CIGARETTE BUTTS',0,150);
     X.fillStyle='#b3261a';X.font='700 24px JBM';X.fillText('— LATER LOST BY THE BUREAU —',0,185);X.textAlign='left';X.restore();}
     // prints card
    if(u>S(13)){X.save();X.translate(1360,560);X.rotate(-0.015);
     X.fillStyle='#fff';X.shadowColor='rgba(0,0,0,0.18)';X.shadowBlur=24;X.fillRect(-200,-200,400,400);X.shadowColor='transparent';
     X.strokeStyle='#2a2b2e';X.lineWidth=3;
     for(let r=14;r<110;r+=14){X.beginPath();X.arc(0,-20,r,0.3+R(r)*0.6,5.6-R(r*3)*0.5);X.stroke();}
     X.fillStyle='#55504a';X.font='700 22px JBM';X.textAlign='center';X.fillText('66 PRINTS · NO MATCH',0,150);X.textAlign='left';X.restore();}
     if(u>S(14)){X.fillStyle='#FF5A1F';X.font='700 28px JBM';X.fillText('2001: PARTIAL DNA FROM THE TIE',120,930);}}},
   {s:15,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.wanted,W/2-700,130,640,700,-0.02,E(lu/0.5),'FBI COMPOSITE · 1971',null);
     photoCard(IMGS.sketch,W/2+60,130,640,700,0.02,E((lu-0.4)/0.5),'“CALM · FORGETTABLE · MID-FORTIES”',null);}},
   {s:16,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     bigCount(800,'SUSPECTS PROCESSED — FIRST FIVE YEARS',H/2-40,E(lu/2.2),'');
     stamp('ALL CLEARED',W/2,H/2+190,-0.05,E((u-S(17))/0.4),'rgba(179,38,26,0.9)',{w:480,h:100,f:50});
     if(u>S(18)){X.textAlign='center';X.font='700 32px JBM';X.fillStyle=SEC;
       X.fillText('OUT OF AN AIRPLANE. OUT OF EXISTENCE.',W/2,H-200);X.textAlign='left';}}},
  ]);
  CHAP(3,'THE MANHUNT','NORJAK · 1971–1976',u);
  grainPass(0.045);vig(0.42);}
// ========== SECTION 5: THE MONEY ==========
function sec5(u,D){
  const t0=TL.s[4].t0,S=j=>SNr(4,j);
  runShots(4,u,D,[
   {s:-1,d:(q,lu)=>{
     X.fillStyle='#050608';X.fillRect(0,0,W,H);
     typeTxt('FEBRUARY 10, 1980',W/2,H/2-40,t0+0.7,20,'900 110px InterB',TXT,'center');
     if(u>S(1)){X.textAlign='center';X.font='700 36px JBM';X.fillStyle=RED;
       X.fillText('NINE YEARS LATER',W/2,H/2+60);X.textAlign='left';}}},
   {s:2,d:(q,lu)=>{
     mapBase('COLUMBIA RIVER · WEST OF VANCOUVER, WA');
     X.strokeStyle='rgba(120,160,190,0.55)';X.lineWidth=14;X.beginPath();X.moveTo(300,820);
     for(let xx=300;xx<1700;xx+=40)X.lineTo(xx,820+Math.sin(xx*0.004)*60);X.stroke();
     X.font='700 26px JBM';X.fillStyle='rgba(120,160,190,0.8)';X.fillText('COLUMBIA RIVER',1350,760);
     X.fillStyle=RED;X.beginPath();X.arc(700,800,12,0,7);X.fill();
     X.font='900 34px InterB';X.fillStyle=TXT;X.fillText('TENA BAR',620,740);}},
   {s:3,d:(q,lu)=>{
     SCN(IMGS.scTena,q,'A FAMILY PICNIC','BRIAN INGRAM · AGE 8 · DIGGING A FIRE PIT');
     redChip('THREE INCHES DOWN — PAPER',120,206,E((u-S(4))/0.5));}},
   {s:5,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.dig,W/2-740,170,700,540,-0.02,E(lu/0.5),'THE BUNDLES · FBI EVIDENCE PHOTO','RUBBER BANDS STILL HOLDING');
     photoCard(IMGS.tena,W/2+60,170,700,540,0.02,E((lu-0.5)/0.5),'TENA BAR · COLUMBIA RIVER',null);
     redChip('$5,800 · THREE BUNDLES',W/2-740,790,E((u-S(6))/0.4));}},
   {s:7,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.bill,W/2-620,200,1240,520,0.008,E(lu/0.5),'SERIAL CHECK — 72 HOURS',null);
     stamp('COOPER RANSOM',W/2,420,-0.08,E((u-S(8))/0.4),'rgba(179,38,26,0.9)',{w:640,h:120,f:58});
     redChip('FIRST TRACE OF HIM IN NINE YEARS',W/2-620,800,E((u-S(9))/0.4));}},
   {s:10,d:(q,lu)=>{
     mapBase('THE PROBLEM — IT MAKES NO SENSE');
     X.strokeStyle='rgba(120,160,190,0.55)';X.lineWidth=14;X.beginPath();X.moveTo(300,820);
     for(let xx=300;xx<1700;xx+=40)X.lineTo(xx,820+Math.sin(xx*0.004)*60);X.stroke();
     X.fillStyle=RED;X.beginPath();X.arc(700,800,12,0,7);X.fill();
     X.font='900 30px InterB';X.fillStyle=TXT;X.fillText('TENA BAR',620,745);
     X.strokeStyle=RED;X.lineWidth=5;
     X.beginPath();X.moveTo(1180,330);X.lineTo(1215,370);X.moveTo(1215,330);X.lineTo(1180,370);X.stroke();
     X.font='900 30px InterB';X.fillText('DROP ZONE · LEWIS RIVER',1240,360);
     X.strokeStyle='rgba(255,74,46,0.8)';X.setLineDash([12,10]);X.beginPath();X.moveTo(1180,360);X.lineTo(720,790);X.stroke();X.setLineDash([]);
     redChip('20 MILES · WRONG RIVER',860,560,E((lu-1)/0.5));
     clockChip('UPSTREAM OF WHERE CURRENT COULD CARRY IT',120,H-200,E((u-S(11))/0.5));
     if(u>S(12)){X.font='700 28px JBM';X.fillStyle=SEC;X.fillText('GEOLOGISTS ARE STILL ARGUING',120,H-240);}}},
   {s:13,d:(q,lu)=>{
     X.fillStyle='#050608';X.fillRect(0,0,W,H);
     X.textAlign='center';X.font='900 96px InterB';X.fillStyle=TXT;
     X.fillText('THE MONEY DIDN’T ANSWER',W/2,H/2-60);
     if(u>S(14)){X.fillStyle=RED;X.fillText('IT MADE IT WORSE.',W/2,H/2+80);}
     X.textAlign='left';}},
   {s:15,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     bigCount(194200,'STILL OUT THERE — EVERY SERIAL KNOWN',H/2-40,E(lu/2.5),'$');
     stamp('NOT SPENT',W/2-480,H/2+190,-0.06,E((u-S(16))/0.35),'rgba(179,38,26,0.85)',{w:380,h:86,f:42});
     stamp('NOT FOUND',W/2,H/2+220,0.04,E((u-S(17))/0.35),'rgba(179,38,26,0.85)',{w:390,h:86,f:42});
     stamp('NOT ONCE',W/2+470,H/2+180,-0.05,E((u-S(18))/0.35),'rgba(179,38,26,0.85)',{w:360,h:86,f:42});}},
  ]);
  CHAP(4,'THE MONEY','TENA BAR · FEBRUARY 1980',u);
  grainPass(0.045);vig(0.42);}
// ========== SECTION 6: THE SUSPECTS / VERDICT ==========
function sec6(u,D){
  const t0=TL.s[5].t0,S=j=>SNr(5,j);
  runShots(5,u,D,[
   {s:-1,d:(q,lu)=>{
     desk();
     X.textAlign='center';
     typeTxt('SO WHO WAS HE?',W/2,H/2-20,t0+0.7,18,'900 130px InterB',TXT,'center');
     if(u>S(1)){X.font='700 32px JBM';X.fillStyle=SEC;X.fillText('THE SUSPECT LIST READS LIKE A NOVEL',W/2,H/2+80);}
     X.textAlign='left';}},
   {s:2,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     X.fillStyle=TXT;X.font='900 44px InterB';X.fillText('SUSPECT 01',120,150);X.fillStyle=RED;X.fillRect(120,170,160,6);
     silCard(W/2-660,240,'RICHARD McCOY','COPYCAT · CAUGHT',E(lu/0.5));
     if(lu>0.8){clockChip('IDENTICAL HIJACK — 5 MONTHS LATER',W/2-140,330,E((lu-0.8)/0.4));}
     stamp('AGE 29 — RULED OUT',W/2+240,620,-0.07,E((u-S(3))/0.4),'rgba(179,38,26,0.85)',{w:600,h:96,f:44});}},
   {s:4,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     X.fillStyle=TXT;X.font='900 44px InterB';X.fillText('SUSPECT 02',120,150);X.fillStyle=RED;X.fillRect(120,170,160,6);
     silCard(W/2-660,240,'DUANE WEBER','DEATHBED CONFESSION',E(lu/0.5));
     if(lu>0.8){paperCard(W/2-120,300,780,220,0.015,E((lu-0.8)/0.4));
       X.fillStyle='#3a3326';X.font='700 40px JBM';X.fillText('“I AM DAN COOPER.”',W/2-40,430);}
     stamp('DNA: NO MATCH',W/2+240,640,-0.06,E((u-S(5))/0.4),'rgba(179,38,26,0.85)',{w:500,h:96,f:46});}},
   {s:6,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     X.fillStyle=TXT;X.font='900 44px InterB';X.fillText('SUSPECT 03',120,150);X.fillStyle=RED;X.fillRect(120,170,160,6);
     silCard(W/2-660,240,'KENNETH CHRISTIANSEN','NWA EMPLOYEE · PARATROOPER',E(lu/0.5));
     if(lu>0.8){clockChip('HIS OWN BROTHER WAS CONVINCED',W/2-140,330,E((lu-0.8)/0.4));}
     stamp('NEVER CHARGED',W/2+240,620,-0.05,E((u-S(7))/0.4),'rgba(139,144,151,0.9)',{w:520,h:96,f:46});}},
   {s:8,d:(q,lu)=>{
     X.fillStyle='#050608';X.fillRect(0,0,W,H);
     X.textAlign='center';X.font='900 84px InterB';X.fillStyle=TXT;
     X.fillText('THE EVIDENCE NEVER',W/2,H/2-50);X.fillText('QUITE CLOSED.',W/2,H/2+60);X.textAlign='left';}},
   {s:9,d:(q,lu)=>{
     desk();
     X.save();X.translate(W/2,H/2);X.rotate(-0.012);X.translate(-W/2,-H/2);
     X.fillStyle=MANILA;X.fillRect(W/2-560,H/2-300,1120,600);X.restore();
     typeTxt('JULY 2016 — AFTER 45 YEARS',W/2-440,H/2-160,t0+S(9)+0.5,28,'700 36px JBM','#5c5138');
     stamp('CLOSED — UNSOLVED',W/2,H/2+10,-0.07,E((u-S(10))/0.4),'rgba(179,38,26,0.92)',{w:900,h:150,f:64});
     clockChip('THE EVIDENCE STILL SITS IN A VAULT',W/2-440,H/2+160,E((u-S(11))/0.5));}},
   {s:12,d:(q,lu)=>{
     X.fillStyle=GND;X.fillRect(0,0,W,H);
     photoCard(IMGS.face,W-760,140,600,760,0.015,E(lu/0.5),'THE ONLY FACE WE HAVE',null);
     X.font='900 56px InterB';X.fillStyle=TXT;X.fillText('TWO POSSIBILITIES.',130,230);
     if(u>S(13)){X.font='700 30px JBM';X.fillStyle=SEC;
       X.fillText('1. THE FOREST KEPT HIM —',130,330);X.fillText('   THE MONEY IS STILL OUT THERE.',130,375);}
     if(u>S(14)){X.font='700 30px JBM';X.fillStyle=SEC;
       X.fillText('2. AN OLD MAN DIED QUIETLY,',130,455);X.fillText('   CARRYING THE ANSWER.',130,500);}
     clockChip('A — HE NEVER SURVIVED THAT NIGHT',130,600,E((u-S(15))/0.4));
     clockChip('B — HE LANDED, AND WALKED AWAY',130,680,E((u-S(16))/0.4));
     clockChip('C — THE FBI MET HIM, AND MISSED',130,760,E((u-S(17))/0.4));}},
   {s:18,d:(q,lu)=>{
     X.fillStyle='#07080A';X.fillRect(0,0,W,H);
     if(IMGS.qm){X.globalAlpha=0.85;const qw=300,qh=qw*1388/536;
       X.drawImage(IMGS.qm,544,74,536,1388,W-480,H/2-390,qw,qh);X.globalAlpha=1;}
     X.font='900 120px InterB';X.fillStyle=TXT;X.fillText('CHRONIC',130,H/2-60);
     X.font='700 34px JBM';X.fillStyle=SEC;X.fillText('NEW CASE FILES EVERY WEEK',130,H/2+10);
     redChip('DROP YOUR VERDICT — A, B OR C',130,H/2+70,E((lu-0.5)/0.5));
     if(u>S(20)){X.font='700 30px JBM';X.fillStyle=SEC;
       X.fillText('THE BEST THEORY DECIDES THE NEXT FILE.',130,H/2+200);}
     stamp('STILL UNSOLVED',W/2+180,H-220,-0.06,E((u-S(21))/0.4),'rgba(179,38,26,0.92)',{w:620,h:120,f:56});
     if(u>S(22)){const bp=u<S(22)+0.3?1.9-0.9*EB((u-S(22))/0.3):1;
       X.save();X.translate(W/2-320,H-180);X.scale(bp,bp);
       X.font='900 96px InterB';X.fillStyle=RED;X.fillText('OPEN.',0,0);X.restore();}}},
  ]);
  CHAP(5,'THE SUSPECTS','800 NAMES · ONE ANSWER',u);
  grainPass(0.05);vig(0.45);}
'''
s=s[:i0]+NEW+s[i1:]
open(p,'w').write(s)
print('V3 ENGINE WRITTEN, lines:',s.count('\n'))
