import json, re
V8='/home/user/explainer-pipeline/assets/dbclong/v8/'
src=open(V8+'test38.html').read()
# strip old dispatcher tail
cut=src.index('window.seek=function')
head=src[:cut]
# extend image boot
head=head.replace(
 "const names={counter:'../scene_counter.jpg',plane:'../img_727.jpg',wanted:'../img_wanted.jpg',search:'../img_search_era.jpg',jump:'../scene_jump.jpg'};",
 "const names={counter:'../scene_counter.jpg',plane:'../img_727.jpg',wanted:'../img_wanted.jpg',search:'../img_search_era.jpg',jump:'../scene_jump.jpg',note:'../scene_note.jpg',seat:'../scene_seat.jpg',stairs:'../scene_stairs.jpg',tenabar_scene:'../scene_tenabar.jpg',tenabar:'../img_tenabar.jpg',bills:'../img_bills_found.jpg',search2:'../scene_search.jpg'};")
head=head.replace(
 "['Cinzel','../../fonts/Cinzel-Black.ttf']",
 "['Cinzel','../../fonts/Cinzel-Black.ttf'],['PFI','../../fonts/PlayfairDisplay-Italic.ttf']")

BEATS=json.load(open('/var/tmp/v8build/beats.json'))
CAPS=json.load(open('/var/tmp/v8build/caps.json'))

JS = r'''
// ================= V8 FULL ENGINE =================
const BEATS=__BEATS__;
const CAPS=__CAPS__;
function ssAt(b,k){const i=Math.floor(k),f=k-i;const s0=b.ss[Math.min(i,b.ss.length-1)]??b.t0;if(f<=0)return s0;const e0=b.se[Math.min(i,b.se.length-1)]??(s0+1);return s0+f*(e0-s0)}
function drawCap(t){for(const c of CAPS){if(t>=c.t0&&t<c.t1){cap(c.txt);return}}}
function redline(y){X.fillStyle='rgba(198,40,40,0.8)';X.fillRect(0,y,1920,2)}
function paperBox(x,y,w,h,col){X.save();X.shadowColor='rgba(0,0,0,0.75)';X.shadowBlur=50;X.fillStyle=col||'#e9e4d8';X.fillRect(x,y,w,h);X.restore();halftoneDots(x,y,w,h)}
function stampR(txt,x,y,t0,t,big){if(t<t0)return;const sl=slamT(t0,t,0.3);X.save();X.translate(x,y);X.rotate(-0.12);X.scale(sl.s,sl.s);X.globalAlpha=sl.a*0.92;
  X.font=(big?110:64)+'px Bebas';const w=X.measureText(txt).width;X.strokeStyle='#c62828';X.lineWidth=big?8:5;X.strokeRect(-w/2-26,big?-74:-46,w+52,big?118:76);
  X.fillStyle='#c62828';X.textAlign='center';X.fillText(txt,0,big?16:10);X.restore();flash(sl.fl*0.5)}
function typeOn(txt,x,y,font,fill,t0,t,cps){if(t<t0)return 0;const n=Math.floor((t-t0)*(cps||26));X.save();X.font=font;X.fillStyle=fill;X.textAlign='left';
  X.fillText(txt.slice(0,n)+(n<txt.length&&Math.floor(t*3)%2?'_':''),x,y);X.restore();return n>=txt.length?1:0.5}
function archImg(im,lt,p){const z=(p&&p.z||1.04)+lt*0.011,s=Math.max(1920/im.width,1080/im.height)*z;
  X.save();X.translate(960+Math.sin(lt*0.3)*6,540);X.filter='grayscale(1) contrast(1.18) brightness('+((p&&p.dark)?0.55:0.8)+')';
  X.drawImage(im,-im.width*s/2,-im.height*s/2,im.width*s,im.height*s);X.filter='none';X.restore();
  X.fillStyle='rgba(8,10,14,0.25)';X.fillRect(0,0,1920,1080)}
const CHIPPOS=[[110,140],[1250,150],[110,800],[1250,790]];
// ---------- renderers ----------
function rFullimg(t,b){const p=b.p,lt=t-b.t0;archImg(IMGS[p.img],lt,p);
  if(p.wind){const r=seededRand(77);X.save();X.strokeStyle='rgba(200,215,235,0.28)';X.lineWidth=2;
    for(let i=0;i<70;i++){const x=(r()*2300+lt*1700)%2200-140,y=(r()*1200+lt*900)%1200-60;X.beginPath();X.moveTo(x,y);X.lineTo(x-70,y+34);X.stroke()}X.restore()}
  (p.chips||[]).forEach((c,i)=>{const tc=ssAt(b,c[0])+0.15;const pos=CHIPPOS[i%4];chip(pos[0],pos[1],0,0,c[1],c[2],tc,t)})}
function rFullclip(t,b){const p=b.p;X.fillStyle='#000';X.fillRect(0,0,1920,1080);
  X.fillStyle='#0a0b0d';X.fillRect(0,0,1920,100);X.fillRect(0,940,1920,140);redline(98);redline(940);
  const bl=Math.floor(t*2.2)%2===0;X.fillStyle=bl?'#c62828':'#5a1414';X.beginPath();X.arc(44,50,10,0,7);X.fill();
  X.save();X.font='600 26px JBM';X.fillStyle='#cfd2d8';X.textAlign='left';X.fillText('ARCHIVE FILM    '+p.label,76,60);
  X.textAlign='right';X.fillStyle='#c62828';X.fillText(p.right||'',1880,60);
  X.font='600 22px JBM';X.fillStyle='#6d727c';X.textAlign='left';X.fillText(p.reel||'',76,972);X.restore()}
function rWinclip(t,b){const p=b.p;bgDark();
  X.strokeStyle='rgba(220,224,230,0.85)';X.lineWidth=3;X.strokeRect(336,146,1248,668);
  X.strokeStyle='#c62828';X.lineWidth=5;for(const [cx,cy,dx,dy] of [[336,146,1,1],[1584,146,-1,1],[336,814,1,-1],[1584,814,-1,-1]]){
    X.beginPath();X.moveTo(cx,cy+dy*40);X.lineTo(cx,cy);X.lineTo(cx+dx*40,cy);X.stroke()}
  const bl=Math.floor(t*2.2)%2===0;X.fillStyle=bl?'#c62828':'#5a1414';X.beginPath();X.arc(360,120,9,0,7);X.fill();
  X.save();X.font='600 26px JBM';X.fillStyle='#cfd2d8';X.textAlign='left';X.fillText(p.label,390,129);
  X.font='600 22px JBM';X.fillStyle='#6d727c';X.fillText(p.reel||'',340,856);X.restore()}
function rTypo(t,b){const p=b.p;bgDark();
  X.save();const g=X.createRadialGradient(960,540,100,960,540,900);g.addColorStop(0,'rgba(198,40,40,0.10)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,1920,1080);X.restore();
  const n=p.lines.length;
  if(p.style==='mega'){const [k,txt]=p.lines[0];const tc=ssAt(b,k);const sl=slamT(tc,t,0.34);
    X.save();X.translate(960,540);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;X.font='170px Anton';X.fillStyle='#f2efe9';X.textAlign='center';
    X.shadowColor='rgba(198,40,40,0.8)';X.shadowBlur=40;X.fillText(txt,0,55);X.restore();flash(sl.fl);
    if(t>tc&&t<tc+0.3){const r=seededRand(Math.floor(t*60));X.save();X.translate((r()-0.5)*14,(r()-0.5)*14);X.restore()}}
  else if(p.style==='ledger'){p.lines.forEach((L,i)=>{const tc=ssAt(b,L[0]);if(t<tc)return;const sl=slamT(tc,t,0.3);
    X.save();X.globalAlpha=sl.a;X.translate(430,330+i*140);X.scale(sl.s,sl.s);
    X.fillStyle='#c62828';X.fillRect(-60,-34,14,46);X.font='64px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText(L[1],0,12);X.restore();flash(sl.fl*0.4)})}
  else{const y0=540-(n-1)*65;p.lines.forEach((L,i)=>{const tc=ssAt(b,L[0]);if(t<tc)return;const sl=slamT(tc,t,0.32);
    X.save();X.globalAlpha=sl.a;X.translate(960,y0+i*130);X.scale(sl.s,sl.s);X.font='92px Cinzel';
    X.fillStyle=/[$0-9]/.test(L[1])?'#e8d9b0':'#f2efe9';X.textAlign='center';X.fillText(L[1],0,32);X.restore();flash(sl.fl*0.5)});
    const last=p.lines[n-1];if(t>ssAt(b,last[0])+0.5){const pp=clamp((t-ssAt(b,last[0])-0.5)/0.4,0,1);X.fillStyle='#c62828';X.fillRect(960-pp*330,y0+n*130-40+66,pp*660,8)}}
  if(p.fade){const ft=b.t1-0.8;if(t>ft){X.fillStyle='rgba(0,0,0,'+clamp((t-ft)/0.8,0,1)*0.9+')';X.fillRect(0,0,1920,1080)}}}
function rNumpop(t,b){const p=b.p;bgDark();
  X.save();const g=X.createRadialGradient(960,500,60,960,500,800);g.addColorStop(0,'rgba(198,40,40,0.14)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,1920,1080);X.restore();
  let act=-1;for(let i=0;i<p.items.length;i++){if(t>=ssAt(b,p.items[i][0]))act=i}
  if(act<0)return;const it=p.items[act],tc=ssAt(b,it[0]);const sl=slamT(tc,t,0.36);
  X.save();X.translate(960,490);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;
  X.font='250px Anton';X.fillStyle='#f2efe9';X.textAlign='center';X.shadowColor='rgba(198,40,40,0.65)';X.shadowBlur=50;X.fillText(it[1],0,80);X.restore();
  const a2=clamp((t-tc-0.18)/0.25,0,1);X.save();X.globalAlpha=a2;X.font='600 38px JBM';X.fillStyle='#c62828';X.textAlign='center';X.fillText(it[2]||'',960,700);X.restore();flash(sl.fl)}
function rQuote(t,b){const p=b.p;bgDark();const lt=t-b.t0;
  X.save();X.globalAlpha=0.12;X.font='420px Cinzel';X.fillStyle='#c62828';X.fillText('\u201C',120,420);X.restore();
  X.strokeStyle='rgba(198,40,40,0.5)';X.lineWidth=2;X.strokeRect(150,200,1620,660);X.strokeRect(162,212,1596,636);
  const n=p.lines.length,y0=520-(n-1)*60;
  p.lines.forEach((ln,i)=>{const tc=b.t0+0.3+i*((b.se[0]-b.t0)>3?1.1:0.7);const a=clamp((t-tc)/0.5,0,1);
    X.save();X.globalAlpha=a;X.font='76px PFI';X.fillStyle=p.red?'#e05a5a':'#f2efe9';X.textAlign='center';
    X.shadowColor='rgba(255,255,255,0.35)';X.shadowBlur=26;X.fillText(ln,960,y0+i*120);X.restore()});
  const aa=clamp((lt-1.4)/0.5,0,1);X.save();X.globalAlpha=aa;X.font='600 28px JBM';X.fillStyle='#9aa0aa';X.textAlign='center';X.fillText(p.attrib||'',960,820);X.restore()}
function rDoc(t,b){const p=b.p;bgDark();const st=p.style;
  const col=st==='file'||st==='suspect'?'#d8c9a3':(st==='tele'?'#f2efe6':'#e9e4d8');
  X.save();X.translate(960,540);X.rotate(-0.012);
  const w=st==='suspect'?1280:1150,h=700;paperBox(-w/2,-h/2,w,h,col);
  if(st==='file'||st==='suspect'){X.fillStyle='#c9b88d';X.fillRect(-w/2,-h/2-34,340,36);X.font='600 24px JBM';X.fillStyle='#4a3f28';X.textAlign='left';X.fillText('CASE FILE - NORJAK',-w/2+18,-h/2-9)}
  if(st==='tele'){X.fillStyle='#777';for(let i=0;i<16;i++){X.beginPath();X.arc(-w/2+30,-h/2+40+i*40,5,0,7);X.fill()}}
  X.font='44px Bebas';X.fillStyle='#1c1a16';X.textAlign='left';X.fillText(p.head,-w/2+70,-h/2+86);
  X.fillStyle='#c62828';X.fillRect(-w/2+70,-h/2+104,w-180,4);
  let py=-h/2+190;
  const fnt=st==='felt'?'62px PFI':(st==='tele'?'600 40px JBM':'600 42px JBM');
  const lh=st==='felt'?96:86;
  p.lines.forEach((L)=>{const tc=ssAt(b,L[0])+0.1;typeOn(L[1],-w/2+70,py,fnt,st==='felt'?'#2a2420':'#24211b',tc,t,st==='felt'?20:30);py+=lh});
  if(st==='suspect'){X.strokeStyle='#4a3f28';X.lineWidth=3;X.strokeRect(w/2-330,-h/2+140,250,310);
    X.fillStyle='rgba(40,36,28,0.85)';X.fillRect(w/2-327,-h/2+143,244,304);
    X.save();X.fillStyle='#6a6052';X.beginPath();X.arc(w/2-205,-h/2+260,56,0,7);X.fill();X.beginPath();X.ellipse(w/2-205,-h/2+400,92,74,0,Math.PI,0);X.fill();X.restore();
    X.font='600 20px JBM';X.fillStyle='#4a3f28';X.textAlign='center';X.fillText('NO VERIFIED PHOTO',w/2-205,-h/2+486);X.textAlign='left'}
  X.restore();
  if(p.stamp){const tc=ssAt(b,p.stamp[1])+0.35;stampR(p.stamp[0],1380,780,tc,t,false)}}
function rDark(t,b){const p=b.p;X.fillStyle='#050607';X.fillRect(0,0,1920,1080);
  const pu=0.5+0.5*Math.sin(t*2.4);X.save();const g=X.createRadialGradient(960,540,50,960,540,700);
  g.addColorStop(0,'rgba(198,40,40,'+(0.05+pu*0.05)+')');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,1920,1080);X.restore();
  const a=clamp((t-b.t0-0.4)/0.6,0,1);X.save();X.globalAlpha=a;X.font='600 40px JBM';X.fillStyle='#cfd2d8';X.textAlign='center';X.fillText(p.sub||'',960,540);X.restore()}
function rStorm(t,b){const lt=t-b.t0;
  const im=IMGS.jump,s=Math.max(1920/im.width,1080/im.height)*(1.3+lt*0.015);
  X.save();X.translate(960-lt*14,500);X.filter='grayscale(0.9) brightness(0.62) contrast(1.25)';
  X.drawImage(im,-im.width*s/2,-im.height*s/2,im.width*s,im.height*s);X.filter='none';X.restore();
  const r=seededRand(99);X.save();X.strokeStyle='rgba(190,205,230,0.33)';X.lineWidth=2;
  for(let i=0;i<150;i++){const x=(r()*2300+lt*1600)%2200-140,y=(r()*1300+lt*2600)%1300-110;X.beginPath();X.moveTo(x,y);X.lineTo(x-36,y+70);X.stroke()}X.restore();
  const lc=(t*0.8)%1;if(lc<0.07)flash(0.14);
  chip(110,140,0,0,'8:13 PM','THE BUMP',b.t0+0.2,t);chip(1250,150,0,0,'STEPPED OFF','INTO THE NIGHT',ssAt(b,1),t)}
function rVerdict(t,b){const p=b.p;bgDark();
  X.save();X.globalAlpha=0.10;X.font='760px Cinzel';X.fillStyle='#c62828';X.textAlign='center';X.fillText(p.k,960,800);X.restore();
  const sl=slamT(b.t0+0.25,t,0.4);X.save();X.globalAlpha=sl.a;X.translate(300,470);X.scale(sl.s,sl.s);
  X.font='300px Cinzel';X.fillStyle='#c62828';X.textAlign='center';X.fillText(p.k,0,100);X.strokeStyle='rgba(242,239,233,0.8)';X.lineWidth=4;X.strokeRect(-160,-160,320,330);X.restore();flash(sl.fl*0.6);
  const a1=clamp((t-b.t0-0.5)/0.4,0,1);X.save();X.globalAlpha=a1;X.font='78px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText(p.title,560,360);
  X.font='600 30px JBM';X.fillStyle='#7fa07f';X.fillText('EXPLAINS: '+p.pro,560,440);X.restore();
  (p.con||[]).forEach((c,i)=>{const tc=ssAt(b,c[0]);if(t<tc)return;const sl2=slamT(tc,t,0.3);
    X.save();X.globalAlpha=sl2.a;X.translate(560,530+i*92);X.scale(sl2.s,sl2.s);
    X.font='54px Bebas';X.fillStyle='#c62828';X.fillText('\u2715  ',0,20);X.fillStyle='#e8e4dc';X.fillText(c[1],60,20);X.restore()})}
function rFinale(t,b){bgDark();const lt=t-b.t0;
  X.save();const g=X.createRadialGradient(560,520,80,560,520,760);g.addColorStop(0,'rgba(198,40,40,0.22)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,1920,1080);X.restore();
  const a=clamp(lt/0.6,0,1);X.save();X.globalAlpha=a;X.translate(560,560);
  const w=640,h=w*IMGS.wanted.height/IMGS.wanted.width;
  X.save();X.shadowColor='#c62828';X.shadowBlur=60;X.filter='grayscale(1) brightness(0.6) contrast(1.5)';X.drawImage(IMGS.wanted,-w/2,-h/2,w,h);X.restore();
  X.globalCompositeOperation='multiply';X.fillStyle='rgba(120,20,20,0.32)';X.fillRect(-w/2,-h/2,w,h);X.restore();
  X.save();X.font='140px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText('D.B. COOPER',960,420);
  X.font='600 32px JBM';X.fillStyle='#9aa0aa';X.fillText('ONE MAN. ONE NIGHT. ONE JUMP.',964,490);X.restore();
  typeOn('THE CASE REMAINS, OFFICIALLY AND FOREVER...',964,580,'600 34px JBM','#cfd2d8',ssAt(b,1,0)+0.2,t,24);
  const oc=ssAt(b,b.ss.length-1)+0.1;stampR('OPEN.',1280,780,oc,t,true);
  if(t>oc+0.6){const bl2=Math.floor(t*1.6)%2===0;X.save();X.font='600 30px JBM';X.fillStyle=bl2?'#c62828':'#7a1d1d';X.textAlign='left';X.fillText('NORJAK - UNSOLVED - 55 YEARS',964,870);X.restore()}}
'''

JS2 = r'''
// ---------- maps ----------
function mapBase(t,zoom,cx,cy){buildLand();
  X.save();X.translate(960,540);X.scale(zoom,zoom);X.translate(-cx,-cy);
  const og=X.createLinearGradient(0,0,0,1080);og.addColorStop(0,'#0a1420');og.addColorStop(1,'#060d16');X.fillStyle=og;X.fillRect(-400,-400,2800,1900);
  X.save();const lg=X.createLinearGradient(600,0,1920,1080);lg.addColorStop(0,'#17211c');lg.addColorStop(1,'#0e1511');X.fillStyle=lg;
  X.beginPath();X.moveTo(LAND[0][0][0],LAND[0][0][1]);for(const p of LAND[0])X.lineTo(p[0],p[1]);
  X.lineTo(2400,1500);X.lineTo(2400,-300);X.closePath();X.fill();X.restore();
  X.strokeStyle='rgba(120,160,130,0.3)';X.lineWidth=1.5;
  for(const [rx,ry,len,rr] of LAND.ridges){X.beginPath();X.moveTo(rx-len/2,ry);X.lineTo(rx-len*0.15,ry-len*0.3);X.lineTo(rx+len*0.1,ry-len*0.12);X.lineTo(rx+len/2,ry);X.stroke()}
  X.fillStyle='rgba(40,70,50,0.5)';const fr=seededRand(12);for(let i=0;i<260;i++){X.fillRect(640+fr()*1300,fr()*1080,3,3)}
  X.strokeStyle='rgba(90,160,190,0.75)';X.lineWidth=5;X.beginPath();X.moveTo(LAND.river[0][0],LAND.river[0][1]);for(const p of LAND.river)X.lineTo(p[0],p[1]);X.stroke()}
function mapMark(x,y,nm,on,t){if(!on)return;X.save();X.fillStyle='#c62828';X.beginPath();X.arc(x,y,9,0,7);X.fill();
  X.strokeStyle='rgba(198,40,40,0.55)';X.lineWidth=3;const rr=10+((t*40)%26);X.beginPath();X.arc(x,y,rr,0,7);X.stroke();
  X.font='600 26px JBM';X.fillStyle='#e8e4dc';X.textAlign='left';X.fillText(nm,x+20,y-14);X.restore()}
function rMap(t,b){const p=b.p,lt=t-b.t0;
  if(p.mode==='sea'){mapBase(t,1.7,965,420);
    const S=[965,355];mapMark(S[0],S[1],'SEATTLE',true,t);
    const ang=lt*1.5,rx=150,ry=95;const px=S[0]+Math.cos(ang)*rx,py=S[1]+Math.sin(ang)*ry;
    X.save();X.setLineDash([8,8]);X.strokeStyle='rgba(220,90,90,0.75)';X.lineWidth=3;X.beginPath();X.ellipse(S[0],S[1],rx,ry,0,0,7);X.stroke();X.setLineDash([]);
    X.translate(px,py);X.rotate(Math.atan2(Math.cos(ang)*ry,-Math.sin(ang)*rx)+Math.PI);
    X.fillStyle='#f2efe9';X.beginPath();X.moveTo(16,0);X.lineTo(-10,8);X.lineTo(-5,0);X.lineTo(-10,-8);X.closePath();X.fill();X.restore();
    X.restore();
    chip(110,140,0,0,'2 HOURS','CIRCLING - CASH COUNTED',ssAt(b,0,0.3),t);
    chip(1250,150,0,0,'2ND BOURBON','HE PAYS FOR IT',ssAt(b,2),t);
    chip(1250,790,0,0,'TRIES TO TIP','THE CREW',ssAt(b,4),t)}
  else if(p.mode==='zone'){mapBase(t,2.1,870,610);
    const A=[880,640],L=[930,600];
    X.save();X.setLineDash([10,7]);X.strokeStyle='#c62828';X.lineWidth=3;X.strokeRect(800,545,230,160);X.setLineDash([]);X.restore();
    mapMark(A[0],A[1],'ARIEL, WA',t>ssAt(b,2),t);mapMark(L[0],L[1],'LAKE MERWIN',t>ssAt(b,3),t);
    const sy=545+((lt*60)%160);X.save();X.strokeStyle='rgba(220,90,90,0.5)';X.lineWidth=2;X.beginPath();X.moveTo(800,sy);X.lineTo(1030,sy);X.stroke();X.restore();
    X.restore();
    chip(110,140,0,0,'JUMP ZONE','FLIGHT DATA + WIND + TIMING',ssAt(b,1),t);
    chip(110,800,0,0,'DENSE PINE','FOREST',ssAt(b,4),t)}
  else{mapBase(t,2.0,900,760);
    const TB=[880,800];
    X.save();X.setLineDash([12,9]);X.strokeStyle='rgba(220,220,230,0.7)';X.lineWidth=3;X.beginPath();X.moveTo(700,980);X.lineTo(1010,560);X.stroke();X.setLineDash([]);X.restore();
    mapMark(TB[0],TB[1],'TENA BAR',t>b.t0+0.6,t);
    if(t>ssAt(b,2)){const sl=slamT(ssAt(b,2),t,0.3);X.save();X.globalAlpha=sl.a;
      X.strokeStyle='#c62828';X.lineWidth=6;X.beginPath();X.moveTo(960,900);X.lineTo(TB[0]+14,TB[1]+14);X.stroke();
      X.fillStyle='#c62828';X.beginPath();X.moveTo(TB[0]+10,TB[1]+10);X.lineTo(TB[0]+40,TB[1]+18);X.lineTo(TB[0]+24,TB[1]+40);X.closePath();X.fill();X.restore()}
    X.restore();
    chip(110,140,0,0,'THE WRONG RIVER','MILES UPSTREAM OF THE FLIGHT PATH',ssAt(b,1),t);
    chip(1250,150,0,0,'FLOATS DOWN','NEVER UP',ssAt(b,3),t)}}
// ---------- gadgets ----------
const GADGETS={
ticket(t,b){bgDark();const sl=slamT(b.t0+0.1,t,0.36);X.save();X.translate(960,500);X.rotate(-0.02);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;
  paperBox(-520,-220,1040,440,'#e9e4d8');X.font='52px Bebas';X.fillStyle='#1c1a16';X.textAlign='left';X.fillText('NORTHWEST ORIENT AIRLINES',-470,-140);
  X.fillStyle='#c62828';X.fillRect(-470,-120,940,3);
  X.font='600 38px JBM';X.fillStyle='#24211b';X.fillText('PORTLAND  >  SEATTLE',-470,-40);
  X.fillText('ONE WAY - COACH',-470,30);X.font='600 30px JBM';X.fillStyle='#6d6456';X.fillText('NOV 24 1971 - GATE 52',-470,100);
  X.restore();flash(sl.fl*0.6);
  if(t>ssAt(b,0,0.35)){const s2=slamT(ssAt(b,0,0.35),t,0.3);X.save();X.translate(1420,330);X.scale(s2.s,s2.s);X.globalAlpha=s2.a;X.rotate(0.06);
    X.font='96px Anton';X.fillStyle='#c62828';X.textAlign='center';X.fillText('$20',0,0);X.font='600 26px JBM';X.fillText('CASH. NO CARD.',0,46);X.restore()}
  if(t>ssAt(b,1)){const s3=slamT(ssAt(b,1),t,0.3);X.save();X.translate(960,500);X.rotate(-0.02);X.scale(s3.s,s3.s);X.globalAlpha=s3.a*0.95;
    X.font='110px Anton';X.fillStyle='#c62828';X.textAlign='center';X.fillText('FLIGHT 305',0,190);X.restore();flash(s3.fl*0.5)}},
typename(t,b){bgDark();
  typeOn('PASSENGER NAME:',560,330,'600 34px JBM','#9aa0aa',b.t0+0.1,t,30);
  const tc=ssAt(b,0,0.2);const full='DAN  COOPER';const n=Math.floor(clamp((t-tc)/0.9,0,1)*full.length);
  X.save();X.font='170px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText(full.slice(0,n)+(n<full.length&&Math.floor(t*3)%2?'_':''),560,540);X.restore();
  chip(110,140,0,0,'NO ID REQUIRED','IT WAS 1971',ssAt(b,1),t);
  if(t>ssAt(b,2)){X.save();X.font='600 30px JBM';X.fillStyle='#c62828';X.textAlign='left';X.fillText('>> NAME NEVER VERIFIED',560,640);X.restore()}},
seatmap(t,b){bgDark();const lt=t-b.t0;
  X.save();X.translate(960,540);X.scale(1.0+lt*0.03,1.0+lt*0.03);X.translate(-40+lt*30,0);
  X.strokeStyle='rgba(220,224,230,0.8)';X.lineWidth=4;
  X.beginPath();X.moveTo(-820,-150);X.quadraticCurveTo(-880,0,-820,150);X.lineTo(640,150);X.quadraticCurveTo(840,90,880,0);X.quadraticCurveTo(840,-90,640,-150);X.closePath();X.stroke();
  const r=seededRand(3);for(let c=0;c<30;c++){for(let s=0;s<6;s++){const x=-760+c*46,y=-110+s*37+(s>2?38:0);
    X.fillStyle='rgba(120,128,140,0.5)';X.fillRect(x,y,26,22)}}
  const ex=-760+29*46,ey=-110+4*37+38;
  const pu=0.5+0.5*Math.sin(t*5);X.fillStyle='rgba(198,40,40,'+(0.6+pu*0.4)+')';X.fillRect(ex-4,ey-4,34,30);
  X.strokeStyle='#c62828';X.lineWidth=3;X.strokeRect(ex-14,ey-14,54,50);X.restore();
  chip(110,140,0,0,'SEAT 18-E','THE VERY LAST ROW',ssAt(b,0,0.3),t);
  if(t>ssAt(b,1)){X.save();X.font='600 30px JBM';X.fillStyle='#c62828';X.textAlign='center';X.fillText('NOBODY BEHIND HIM. NOBODY WATCHING.',960,900);X.restore()}},
briefcase(t,b){bgDark();
  X.save();X.translate(760,560);X.strokeStyle='#cfd2d8';X.lineWidth=5;X.strokeRect(-300,-110,600,260);
  const op=clamp((t-b.t0-0.3)/0.8,0,1)*0.5;X.save();X.translate(-300,-110);X.rotate(-op);X.strokeRect(0,-26,600,26);X.restore();
  const r=seededRand(8);X.strokeStyle='#9aa0aa';X.lineWidth=3;
  X.beginPath();X.moveTo(-220,40);for(let i=0;i<8;i++){X.lineTo(-220+i*60,40+Math.sin(i*2.2)*26)}X.stroke();
  for(let i=0;i<3;i++){X.fillStyle='#8a2222';X.fillRect(-180+i*110,-60,70,150)}X.restore();
  const items=[[1,'RED CYLINDERS'],[2,'WIRES'],[3,'A LARGE BATTERY']];
  items.forEach((it,i)=>{const tc=ssAt(b,it[0]);if(t<tc)return;const sl=slamT(tc,t,0.3);
    X.save();X.globalAlpha=sl.a;X.translate(1430,330+i*150);X.scale(sl.s,sl.s);
    X.font='56px Bebas';X.fillStyle='#f2efe9';X.textAlign='center';X.fillText(it[1],0,10);
    X.strokeStyle='#c62828';X.lineWidth=4;const w=X.measureText(it[1]).width;X.strokeRect(-w/2-20,-36,w+40,66);X.restore();flash(sl.fl*0.4)});
  if(t>ssAt(b,0,0.5)){X.save();X.font='600 28px JBM';X.fillStyle='#9aa0aa';X.textAlign='left';X.fillText('OPENED - JUST ENOUGH.',480,900);X.restore()}},
cash(t,b){bgDark();const lt=t-b.t0;
  const r=seededRand(21);X.save();X.translate(960,600);
  const n=Math.min(26,Math.floor(lt*9));for(let i=0;i<n;i++){const row=Math.floor(i/9),cx=-390+(i%9)*95,cy=60-row*70;
    X.save();X.translate(cx,cy);X.rotate((r()-0.5)*0.14);X.fillStyle='#b5bd9e';X.fillRect(-42,-20,84,40);X.strokeStyle='#5d6450';X.strokeRect(-42,-20,84,40);
    X.fillStyle='#434b38';X.beginPath();X.arc(0,0,11,0,7);X.fill();X.restore()}X.restore();
  const cnt=Math.floor(clamp((t-ssAt(b,1))/1.6,0,1)*10000);
  if(t>ssAt(b,1)){X.save();X.font='150px Anton';X.fillStyle='#f2efe9';X.textAlign='center';X.shadowColor='rgba(198,40,40,0.6)';X.shadowBlur=36;
    X.fillText(cnt.toLocaleString('en-US'),960,330);X.font='600 34px JBM';X.fillStyle='#c62828';X.fillText('TWENTY-DOLLAR BILLS',960,400);X.restore()}
  chip(110,140,0,0,'SEATTLE BANK','PULLED IN HOURS',ssAt(b,0,0.4),t)},
microfilm(t,b){bgDark();const lt=t-b.t0;
  X.save();X.translate(880,560);X.fillStyle='#b5bd9e';X.fillRect(-240,-110,480,220);X.strokeStyle='#5d6450';X.lineWidth=3;X.strokeRect(-240,-110,480,220);
  X.fillStyle='#434b38';X.beginPath();X.arc(0,0,56,0,7);X.fill();
  X.font='600 24px JBM';X.fillStyle='#2e3326';X.textAlign='left';X.fillText('L21490617A',-228,-80);X.restore();
  X.save();X.strokeStyle='#9aa0aa';X.lineWidth=6;X.beginPath();X.moveTo(880,250);X.lineTo(880,330);X.stroke();
  X.fillStyle='#24262c';X.fillRect(780,180,200,80);X.fillStyle='#0c0d10';X.fillRect(850,230,60,36);X.restore();
  const fl2=(t*2.8)%1;if(fl2<0.09&&t<ssAt(b,1))flash(0.35);
  const cnt=Math.floor(clamp((t-b.t0)/( ssAt(b,1)-b.t0),0,1)*10000);
  X.save();X.font='110px Anton';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText(cnt.toLocaleString('en-US'),1240,480);
  X.font='600 30px JBM';X.fillStyle='#9aa0aa';X.fillText('SERIALS PHOTOGRAPHED',1240,540);X.restore();
  chip(110,140,0,0,'MICROFILM','EVERY SINGLE BILL',b.t0+0.3,t);
  if(t>ssAt(b,2)){const sl=slamT(ssAt(b,2),t,0.3);X.save();X.globalAlpha=sl.a;X.translate(1430,760);X.scale(sl.s,sl.s);
    X.font='64px Bebas';X.fillStyle='#c62828';X.textAlign='center';X.fillText('REMEMBER THIS DETAIL',0,0);X.restore();flash(sl.fl*0.4)}},
checklist(t,b){bgDark();X.save();X.translate(960,540);X.rotate(-0.01);paperBox(-560,-330,1120,660,'#e9e4d8');
  X.font='44px Bebas';X.fillStyle='#1c1a16';X.textAlign='left';X.fillText('COOPER\u2019S ORDERS - FLIGHT 305 TO RENO',-500,-250);
  X.fillStyle='#c62828';X.fillRect(-500,-232,1020,4);
  const items=[[0,'COURSE: MEXICO CITY'],[1,'ALTITUDE: 10,000 FT'],[2,'FLAPS: 15 DEGREES'],[3,'LANDING GEAR: DOWN'],[4,'SPEED: AS SLOW AS IT FLIES'],[5,'AFT STAIRS: LOWERED']];
  items.forEach((it,i)=>{const tc=ssAt(b,it[0]);if(t<tc)return;const a=clamp((t-tc)/0.25,0,1);
    X.save();X.globalAlpha=a;X.strokeStyle='#c62828';X.lineWidth=4;X.strokeRect(-500,-190+i*88,40,40);
    if(t>tc+0.2){X.beginPath();X.moveTo(-492,-168+i*88);X.lineTo(-480,-156+i*88);X.lineTo(-466,-184+i*88);X.stroke()}
    X.font='600 40px JBM';X.fillStyle='#24211b';X.fillText(it[1],-430,-158+i*88);X.restore()});
  X.restore()},
warnlight(t,b){X.fillStyle='#07080c';X.fillRect(0,0,1920,1080);
  X.save();X.translate(960,520);X.fillStyle='#14161c';X.fillRect(-620,-260,1240,520);X.strokeStyle='#2a2e38';X.lineWidth=3;X.strokeRect(-620,-260,1240,520);
  const cells=[['FUEL','#3a3e48'],['HYD','#3a3e48'],['AFT STAIRS','X'],['CABIN ALT','#3a3e48'],['APU','#3a3e48'],['DOORS','#3a3e48']];
  cells.forEach((c,i)=>{const cx=-470+(i%3)*320,cy=-120+Math.floor(i/3)*220;
    let col=c[1];if(c[1]==='X'){const on=t>ssAt(b,1)&&Math.floor(t*3.5)%2===0;col=on?'#d84040':'#5a1414'}
    X.fillStyle=col;X.fillRect(cx-130,cy-60,260,120);X.strokeStyle='#0a0b0d';X.lineWidth=2;X.strokeRect(cx-130,cy-60,260,120);
    X.font='600 30px JBM';X.fillStyle=c[1]==='X'?'#fff':'#788';X.textAlign='center';X.fillText(c[0],cx,cy+10)});X.restore();
  chip(110,140,0,0,'8:00 PM','WARNING LIGHT',ssAt(b,0),t);
  if(t>ssAt(b,2)){X.save();X.font='600 34px JBM';X.fillStyle='#c62828';X.textAlign='center';X.fillText('THE AFT STAIRS ARE OPEN.',960,930);X.restore()}},
bump(t,b){X.fillStyle='#030405';X.fillRect(0,0,1920,1080);
  const tb=ssAt(b,2,0.3);const j=(t>tb&&t<tb+0.4)?(0.4-(t-tb))*40:0;const r=seededRand(Math.floor(t*60));
  X.save();X.translate((r()-0.5)*j,(r()-0.5)*j);
  X.font='190px Anton';X.fillStyle='#f2efe9';X.textAlign='center';X.shadowColor='rgba(198,40,40,0.7)';X.shadowBlur=46;X.fillText('8:13 PM',960,500);
  if(t>tb){const sl=slamT(tb,t,0.3);X.globalAlpha=sl.a;X.font='84px Bebas';X.fillStyle='#c62828';X.fillText('A SUDDEN BUMP.',960,660);flash(sl.fl)}
  X.restore();if(t>tb&&t<tb+0.1)flash(0.3)},
radar(t,b){X.fillStyle='#04070a';X.fillRect(0,0,1920,1080);const lt=t-b.t0;
  X.save();X.translate(960,540);
  for(const rr of [120,240,360,440]){X.strokeStyle='rgba(60,180,120,0.25)';X.lineWidth=2;X.beginPath();X.arc(0,0,rr,0,7);X.stroke()}
  X.strokeStyle='rgba(60,180,120,0.2)';X.beginPath();X.moveTo(-460,0);X.lineTo(460,0);X.moveTo(0,-460);X.lineTo(0,460);X.stroke();
  const ang=lt*1.8;const g=X.createConicGradient?X.createConicGradient(ang,0,0):null;
  X.save();X.rotate(ang);const gr=X.createLinearGradient(0,0,440,0);gr.addColorStop(0,'rgba(80,220,140,0.5)');gr.addColorStop(1,'rgba(80,220,140,0)');
  X.fillStyle=gr;X.beginPath();X.moveTo(0,0);X.arc(0,0,440,-0.5,0.02);X.closePath();X.fill();X.restore();
  X.font='600 26px JBM';X.fillStyle='rgba(120,220,160,0.8)';X.textAlign='center';X.fillText('NO CONTACT',0,-480);X.restore();
  chip(110,140,0,0,'2 X F-106','SHADOWING FLT 305',b.t0+0.2,t);
  chip(1250,150,0,0,'NO CHUTE SEEN','NO MAN SEEN',ssAt(b,1),t);
  if(t>ssAt(b,3)){const sl=slamT(ssAt(b,3),t,0.3);X.save();X.globalAlpha=sl.a;X.translate(960,900);X.scale(sl.s,sl.s);
    X.font='70px Bebas';X.fillStyle='#c62828';X.textAlign='center';X.fillText('RADAR: NOTHING.',0,0);X.restore();flash(sl.fl*0.5)}},
evidence(t,b){bgDark();
  const items=[['THE CLIP-ON TIE','LEFT ON 18-E',0.3],['8 CIGARETTE BUTTS','ASHTRAY',1.5],['66 FINGERPRINTS','MATCHED NO ONE',2.7]];
  items.forEach((it,i)=>{const tc=b.t0+it[2];if(t<tc)return;const sl=slamT(tc,t,0.32);
    X.save();X.globalAlpha=sl.a;X.translate(430+i*530,540);X.scale(sl.s,sl.s);X.rotate(-0.02+i*0.02);
    paperBox(-210,-260,420,520,'#d8c9a3');
    X.fillStyle='#4a3f28';X.font='600 24px JBM';X.textAlign='center';X.fillText('EVIDENCE '+(i+1),0,-200);
    X.fillStyle='#c62828';X.fillRect(-160,-180,320,3);
    X.font='46px Bebas';X.fillStyle='#1c1a16';X.fillText(it[0],0,0);
    X.font='600 24px JBM';X.fillStyle='#6d6456';X.fillText(it[1],0,60);
    X.strokeStyle='#4a3f28';X.lineWidth=2;X.beginPath();X.arc(0,-130,26,0,7);X.stroke();X.restore();flash(sl.fl*0.4)})},
headlines(t,b){bgDark();
  const hs=[['MORNING WIRE','HIJACKER "D.B. COOPER" VANISHES'],['THE DAILY REGISTER','D.B. COOPER JUMPS WITH $200,000'],['EVENING NETWORK NEWS','MANHUNT FOR D.B. COOPER'],['NATIONAL PRESS','D.B. COOPER: FOLK LEGEND?']];
  hs.forEach((h,i)=>{const tc=ssAt(b,Math.min(i,b.ss.length-1));if(t<tc)return;const sl=slamT(tc,t,0.3);
    X.save();X.translate(560+i*270,400+i*120);X.rotate(-0.06+i*0.04);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;
    paperBox(-380,-240,760,480,'#efeadc');
    X.font='34px Bebas';X.fillStyle='#55504a';X.textAlign='center';X.fillText(h[0],0,-170);
    X.fillStyle='#1c1a16';X.fillRect(-330,-150,660,3);
    X.font='56px Bebas';X.fillText(h[1],0,-60);
    X.fillStyle='#8a8578';for(let r2=0;r2<5;r2++){X.fillRect(-330,0+r2*34,660,12)}X.restore();flash(sl.fl*0.3)})},
mccoydive(t,b){bgDark();
  X.save();X.font='64px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText('COOPER',260,320);X.fillText('McCOY',260,560);X.restore();
  const p1=clamp((t-b.t0-0.3)/1.2,0,1),p2=clamp((t-ssAt(b,0,0.3))/1.2,0,1);
  X.fillStyle='#8a8f98';X.fillRect(260,350,p1*620,46);
  X.fillStyle='#c62828';X.fillRect(260,590,p2*1240,46);
  X.save();X.font='600 32px JBM';X.fillStyle='#9aa0aa';X.textAlign='left';if(p1>0.9)X.fillText('~290 KM/H',910,384);
  if(p2>0.9){X.fillStyle='#c62828';X.fillText('~500 KM/H - NEARLY 2X',1530,624)}X.restore();
  if(t>ssAt(b,1)){const sl=slamT(ssAt(b,1),t,0.3);X.save();X.globalAlpha=sl.a;X.translate(960,840);X.scale(sl.s,sl.s);
    X.font='60px Bebas';X.fillStyle='#f2efe9';X.textAlign='center';X.fillText('LANDED. WALKED AWAY. WENT HOME.',0,0);X.restore()}},
doors(t,b){bgDark();
  const ds=[[1,'DOOR ONE','DIED IN THE WOODS.','THE FOREST KEPT HIM.'],[2,'DOOR TWO','WALKED OUT.','VANISHED INTO AMERICA.']];
  ds.forEach((d,i)=>{const tc=ssAt(b,d[0]);if(t<tc)return;const sl=slamT(tc,t,0.34);
    X.save();X.translate(560+i*800,540);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;
    X.fillStyle='#101216';X.fillRect(-260,-360,520,720);X.strokeStyle=i?'#c62828':'#8a8f98';X.lineWidth=5;X.strokeRect(-260,-360,520,720);
    X.fillStyle=i?'#c62828':'#8a8f98';X.beginPath();X.arc(190,0,14,0,7);X.fill();
    X.font='40px Bebas';X.fillStyle='#9aa0aa';X.textAlign='center';X.fillText(d[1],0,-280);
    X.font='54px Bebas';X.fillStyle='#f2efe9';X.fillText(d[2],0,-40);
    X.font='600 26px JBM';X.fillStyle=i?'#e05a5a':'#9aa0aa';X.fillText(d[3],0,40);X.restore();flash(sl.fl*0.4)});
  if(t>b.t0+(b.t1-b.t0)*0.75){X.save();X.font='600 34px JBM';X.fillStyle='#c62828';X.textAlign='center';X.fillText('NINE YEARS: NEITHER DOOR OPENED.',960,980);X.restore()}},
match(t,b){bgDark();X.save();X.translate(960,520);X.rotate(-0.01);paperBox(-560,-300,1120,600,'#f2efe6');
  X.font='40px Bebas';X.fillStyle='#1c1a16';X.textAlign='left';X.fillText('FBI SERIAL REGISTRY - NORJAK RANSOM',-500,-220);
  X.fillStyle='#c62828';X.fillRect(-500,-202,1020,4);
  const rows=['L21490617A','L14547196B','L22916423A','L31372747B','L04961277A'];
  rows.forEach((rr,i)=>{X.font='600 38px JBM';X.fillStyle='#24211b';X.fillText(rr,-500,-130+i*88)});X.restore();
  for(let i=0;i<3;i++){const tc=ssAt(b,2+i);stampR('MATCH',700+i*260,430+i*120,tc,t,false)}
  chip(110,140,0,0,'TENA BAR BILLS','$5,800 - RUBBER BANDS',b.t0+0.3,t)},
ticker(t,b){bgDark();const lt=t-b.t0;
  const r=seededRand(Math.floor(t*5));X.save();X.globalAlpha=0.35;X.font='600 26px JBM';X.fillStyle='#4a7a5a';X.textAlign='left';
  for(let i=0;i<12;i++){const sr=seededRand(i*7+Math.floor(lt*3));let s2='';for(let j2=0;j2<3;j2++)s2+='L'+Math.floor(sr()*89999999+10000000)+'A  ';
    X.fillText(s2,80,120+i*80)}X.restore();
  X.save();X.font='200px Anton';X.fillStyle='#f2efe9';X.textAlign='center';X.shadowColor='rgba(198,40,40,0.7)';X.shadowBlur=50;
  X.fillText('$194,200',960,460);X.font='600 36px JBM';X.fillStyle='#c62828';X.fillText('STILL OUT THERE. ZERO SERIALS EVER SCANNED.',960,540);X.restore();
  chip(110,800,0,0,'NOT A BANK','NOT ONE BILL',ssAt(b,1),t);
  chip(1250,790,0,0,'NOT A CASINO','NOT A STORE',ssAt(b,2),t);
  if(t>ssAt(b,5)){const sl=slamT(ssAt(b,5),t,0.34);X.save();X.globalAlpha=sl.a;X.translate(960,760);X.scale(sl.s,sl.s);
    X.font='150px Anton';X.fillStyle='#c62828';X.textAlign='center';X.fillText('ZERO HITS',0,0);X.restore();flash(sl.fl)}},
tie(t,b){bgDark();
  X.save();const g=X.createRadialGradient(960,500,40,960,500,520);g.addColorStop(0,'rgba(230,235,245,0.14)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,1920,1080);X.restore();
  X.save();X.translate(960,480);const sl=slamT(b.t0+0.2,t,0.4);X.scale(sl.s,sl.s);X.globalAlpha=sl.a;
  X.fillStyle='#14161c';X.beginPath();X.moveTo(0,-230);X.lineTo(70,-160);X.lineTo(34,-150);X.lineTo(80,180);X.lineTo(0,260);X.lineTo(-80,180);X.lineTo(-34,-150);X.lineTo(-70,-160);X.closePath();X.fill();
  X.strokeStyle='#3a3e48';X.lineWidth=3;X.stroke();
  X.strokeStyle='rgba(200,210,225,0.5)';X.lineWidth=2;X.beginPath();X.moveTo(-54,-162);X.lineTo(54,-162);X.stroke();X.restore();
  chip(110,140,0,0,'EXHIBIT - THE TIE','BLACK - CLIP-ON - JCPENNEY',b.t0+0.4,t);
  chip(1250,150,0,0,'LEFT ON SEAT 18-E','HIS ONE MISTAKE?',ssAt(b,2),t)},
microscope(t,b){X.fillStyle='#05060a';X.fillRect(0,0,1920,1080);const lt=t-b.t0;
  X.save();X.beginPath();X.arc(960,540,400,0,7);X.clip();
  X.fillStyle='#0c1118';X.fillRect(560,140,800,800);
  const r=seededRand(55);for(let i=0;i<40;i++){const x=560+r()*800,y=140+r()*800,s2=2+r()*5;
    X.fillStyle='rgba(140,160,190,0.5)';X.fillRect(x+Math.sin(lt*0.7+i)*8,y+Math.cos(lt*0.5+i)*8,s2,s2)}
  if(t>ssAt(b,2,0.2)){const r2=seededRand(9);for(let i=0;i<12;i++){const x=660+r2()*600,y=240+r2()*600;
    const pu=0.5+0.5*Math.sin(t*3+i);X.save();X.shadowColor='#e8eaf2';X.shadowBlur=24*pu;X.fillStyle='rgba(235,240,250,'+(0.7+0.3*pu)+')';
    X.fillRect(x+Math.sin(lt*0.6+i)*10,y,4+(i%3)*3,4+(i%2)*4);X.restore()}}
  X.restore();
  X.strokeStyle='rgba(200,210,230,0.5)';X.lineWidth=3;X.beginPath();X.arc(960,540,400,0,7);X.stroke();
  X.strokeStyle='rgba(200,210,230,0.25)';X.beginPath();X.moveTo(960,140);X.lineTo(960,940);X.moveTo(560,540);X.lineTo(1360,540);X.stroke();
  X.save();X.font='600 28px JBM';X.fillStyle='#9aa0aa';X.textAlign='left';X.fillText('ELECTRON MICROSCOPE - CITIZEN SLEUTHS',110,120);X.restore();
  if(t>ssAt(b,2,0.4)){const sl=slamT(ssAt(b,2,0.4),t,0.32);X.save();X.globalAlpha=sl.a;X.translate(960,980);X.scale(sl.s,sl.s);
    X.font='64px Bebas';X.fillStyle='#c62828';X.textAlign='center';X.fillText('PURE, UNALLOYED TITANIUM',0,0);X.restore();flash(sl.fl*0.5)}},
profile(t,b){bgDark();const lt=t-b.t0;
  const bl=Math.max(0,10-lt*3.2);
  X.save();X.translate(560,540);const w=560,h=w*IMGS.wanted.height/IMGS.wanted.width;
  X.filter='grayscale(1) contrast(1.3) brightness(0.75) blur('+bl.toFixed(1)+'px)';
  X.drawImage(IMGS.wanted,-w/2,-h/2,w,h);X.filter='none';
  X.strokeStyle='rgba(198,40,40,0.6)';X.lineWidth=3;X.strokeRect(-w/2,-h/2,w,h);X.restore();
  const traits=[[1,'NOT A RANDOM CRIMINAL'],[2,'INSIDE THE AIRCRAFT WORLD'],[3,'AN ENGINEER.'],[4,'A MANAGER.'],[5,'KNEW EXACTLY WHAT A 727 COULD DO']];
  traits.forEach((tr,i)=>{const tc=ssAt(b,tr[0]);if(t<tc)return;const a=clamp((t-tc)/0.3,0,1);
    X.save();X.globalAlpha=a;X.fillStyle='#c62828';X.fillRect(920,300+i*110-26,12,40);
    X.font='46px Bebas';X.fillStyle='#f2efe9';X.textAlign='left';X.fillText(tr[1],960,300+i*110);X.restore()});
  chip(110,110,0,0,'PROFILE','SHARPENING',b.t0+0.3,t)},
closed(t,b){bgDark();
  X.save();X.translate(960,520);X.rotate(-0.012);paperBox(-560,-320,1120,640,'#d8c9a3');
  X.fillStyle='#c9b88d';X.fillRect(-560,-354,340,36);X.font='600 24px JBM';X.fillStyle='#4a3f28';X.textAlign='left';X.fillText('CASE FILE - NORJAK',-542,-329);
  X.font='44px Bebas';X.fillStyle='#1c1a16';X.fillText('FEDERAL BUREAU OF INVESTIGATION',-500,-240);
  X.fillStyle='#c62828';X.fillRect(-500,-222,1020,4);
  X.font='600 38px JBM';X.fillStyle='#24211b';X.fillText('DATE: JULY 8, 2016',-500,-140);
  X.fillText('CASE AGE: 45 YEARS',-500,-60);X.fillText('STATUS:',-500,20);X.restore();
  const tc=ssAt(b,1,0.3);stampR('CLOSED',1060,560,tc,t,true);
  if(t>ssAt(b,2)){X.save();X.font='600 32px JBM';X.fillStyle='#c62828';X.textAlign='center';X.fillText('NORJAK WAS OVER.',960,960);X.restore()}}
};
function rGadget(t,b){GADGETS[b.p.g](t,b)}
const R={fullimg:rFullimg,fullclip:rFullclip,winclip:rWinclip,typo:rTypo,numpop:rNumpop,quote:rQuote,doc:rDoc,dark:rDark,storm:rStorm,verdict:rVerdict,finale:rFinale,map:rMap,gadget:rGadget};
window.seek=function(t){X.clearRect(0,0,1920,1080);
  if(t<40.1){
    if(t<4.88)b1(t);else if(t<7.99)b2(t);else if(t<11.79)b3(t);else if(t<15.01)b4(t);else if(t<18.35)b5(t);
    else if(t<22.18)b6(t);else if(t<29.30)b7(t);else if(t<31.23)b8(t);else if(t<36.36)b9(t);else b10(t);
    scan();grain(t);vignette();
    for(const e of [4.88,7.99,11.79,15.01,18.35,22.18,29.30,31.23,36.36]){if(t>e&&t<e+0.07)flash(0.22)}
    return}
  let bt=BEATS.beats[BEATS.beats.length-1];
  for(const b of BEATS.beats){if(t>=b.t0&&t<b.t1){bt=b;break}}
  R[bt.tr](t,bt);
  scan();grain(t);vignette();
  if(t>bt.t0&&t<bt.t0+0.07)flash(0.2);
  if(bt.tr!=='fullclip')drawCap(t);else drawCap(t);
};
</script></body></html>
'''
JS = JS.replace('__BEATS__', json.dumps(BEATS)).replace('__CAPS__', json.dumps(CAPS))
open(V8+'engine_v8.html','w').write(head + JS + JS2.replace('</script></body></html>','') if False else head + (JS.split('// ---------- maps ----------')[0] if False else JS[:0]) )
# simpler: JS2 contains dispatcher & closing tags; JS contains data+renderers. Concatenate properly:
full = head + JS.replace('</script></body></html>','') if '</script>' in JS else head+JS
# JS doesn't contain closing; JS2 does. Rebuild cleanly:
full = head + JS + JS2
# remove accidental closing inside JS (none) - write
open(V8+'engine_v8.html','w').write(full)
print('engine written', len(full), 'bytes')
