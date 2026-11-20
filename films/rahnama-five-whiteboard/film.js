import * as W from '../../setup/whiteboard-readiness/engine/wb.js';
await W.loadFont('tech','../../setup/whiteboard-readiness/fonts/EMSTech.json');
await document.fonts.load('500 43px Fa');
const [fa,captions]=await Promise.all(['assets/persian-strokes.json','captions.json'].map(x=>fetch(x).then(r=>r.json())));
const tl=new W.Timeline(),K=new W.Pen('coal','#10171B',{park:[-500,-800],len:300}),B=new W.Pen('blue','#124CB5',{park:[-750,-800],len:300}),R=new W.Pen('coral','#F15B45',{park:[-1000,-800],len:300});
const ink={color:K.color,w:7},bl={color:B.color,w:9},re={color:R.color,w:9};
const groups=[],jobs=[];
function draw(p,sh,a,b,tag='diagram'){jobs.push({a,run:()=>tl.draw(p,sh,a,{by:b,tag})});}
function label(s,x,y,h,a,b){const q=W.text(s,x,y,{h,w:h*.10,color:K.color,align:'center'});groups.push(q);draw(K,q,a,b,s);return q;}
function persian(key,x,y,width,a,b){let z=fa[key],sc=width/z.w;const q=z.paths.map(p=>W.poly(p.flatMap(([px,py])=>[x-width/2+px*sc,y+py*sc]),{...ink,w:8,jitter:.17,kind:'text'}));groups.push(q);draw(K,q,a,b,key);}
function frame(x,y,w,h,o=bl){return W.roundRect(x,y,w,h,18,o);}
function check(x,y,s=1){return W.poly([[x-22*s,y],[x-4*s,y+20*s],[x+34*s,y-27*s]],re);}
function person(x,y,s=1){return [W.circle(x,y-45*s,30*s,ink),W.curve([[x-58*s,y+75*s],[x-48*s,y+10*s],[x,y],[x+48*s,y+10*s],[x+58*s,y+75*s]],ink)];}
function calendar(x,y,w=240){return [frame(x,y,w,175),W.line(x,y+45,x+w,y+45,bl),W.line(x+45,y-15,x+45,y+15,re),W.line(x+w-45,y-15,x+w-45,y+15,re)];}
function bubble(x,y,w=260,h=130){return [frame(x,y,w,h),W.poly([[x+55,y+h],[x+30,y+h+38],[x+100,y+h]],bl)];}
const cx=[1100,2800,4500,6100,6100,4450,2800],cy=[1200,1200,1200,1200,3200,3200,3200];
function num(n,a,b){draw(R,W.circle(cx[n],cy[n]-540,57,re),a,b);label(String(n),cx[n],cy[n]-515,65,a,b+.05);}
// Hook: complete thought in the first five seconds; open loop around checkpoint five.
persian('hook',1100,590,780,-.8,1.25);
draw(B,[W.poly([[795,1080],[795,925],[1098,950],[1098,1120],[795,1080]],bl),W.poly([[1100,950],[1405,925],[1405,1080],[1100,1120]],bl)],-.2,1.8);
draw(R,W.line(795,1150,1405,890,re),1.9,2.45);
for(let n=1;n<=5;n++){const x=770+(n-1)*165;draw(B,W.circle(x,1420,44,bl),2.55+(n-1)*.28,2.8+(n-1)*.28);label(String(n),x,1441,53,2.55+(n-1)*.28,2.8+(n-1)*.28);}
draw(R,W.circle(1430,1420,68,re),4.58,5.12);draw(R,W.line(1430,1310,1430,1265,re),5.18,5.4);
// 1 — exact needs become a term/week roadmap.
num(1,6.15,6.65);label('JUST A LEVEL?',2800,830,62,6.8,7.9);
draw(B,frame(2560,980,480,180),8.4,9);label('A2',2800,1104,106,9.1,9.7);
draw(R,W.poly([[3080,1030],[3120,1030],[3120,1090],[3090,1100],[3090,1130]],re),10.0,10.5);
jobs.push({a:11.8,run:()=>tl.erase(W.zigzag(2400,870,850,430,5),11.8,.6,{width:210,strength:.94})});
label('YOUR NEEDS',2800,1040,57,12.42,13.3);
draw(B,W.arrow(2510,1160,3090,1160,bl),13.35,14.3);
label('LEARNING',2800,1265,64,14.5,15.15);label('ROADMAP',2800,1355,64,15.2,15.95);
draw(B,[calendar(2470,1410,260),calendar(2860,1410,260)],16.32,17.5);label('TERM',2600,1538,46,17.55,18);label('WEEK',2990,1538,46,18.05,18.5);draw(R,[check(2650,1485,.8),check(3040,1485,.8)],18.55,19.1);
// 2 — content selection has a physical selection magnet, not more title cards.
num(2,19.55,20);label('SAME FOR ALL?',4500,830,64,20.4,21.7);
draw(B,[frame(4190,980,180,140),frame(4410,980,180,140),frame(4630,980,180,140)],21.8,22.8);
draw(R,W.line(4180,1145,4820,960,re),22.9,23.45);
label('YOUR WEEK',4500,1235,62,23.5,24.6);
draw(B,[frame(4120,1310,210,180),W.poly([[4195,1350],[4195,1450],[4260,1400],[4195,1350]],bl)],25.55,26.1);
draw(B,[W.roundRect(4440,1310,80,115,35,bl),W.curve([[4408,1390],[4408,1470],[4552,1470],[4552,1390]],bl),W.line(4480,1460,4480,1505,bl)],26.15,26.8);
draw(B,[frame(4680,1320,180,160),W.line(4725,1400,4785,1400,bl),W.line(4755,1370,4755,1430,bl),W.circle(4822,1380,8,re),W.circle(4822,1425,8,re)],26.85,27.7);
draw(R,[check(4240,1560,.8),check(4500,1560,.8),check(4760,1560,.8)],28,28.9);
draw(B,[W.arrow(4170,1640,4780,1640,bl)],29.2,30.2);
// 3 — four different uses, occupying separate corners of one diagram.
num(3,31.6,32.1);label('USE IT.',6100,830,96,32.55,33.65);
draw(B,[frame(5710,980,280,200),W.line(5710,1080,5990,1080,bl),W.line(5850,980,5850,1180,bl)],34.85,35.8);
draw(R,[W.circle(5780,1030,20,re),W.circle(5920,1130,20,re)],35.95,36.6);
draw(B,[bubble(6190,990,280,130),bubble(6260,1170,200,100)],37.7,38.8);draw(R,check(6390,1050,.9),38.85,39.45);
draw(B,[person(5790,1420,.75),person(5940,1420,.75)],39.88,40.85);
draw(R,[W.line(5745,1360,5835,1360,re),W.line(5895,1360,5985,1360,re)],40.9,41.1);
draw(B,[frame(6190,1390,240,180),W.poly([[6230,1530],[6275,1480],[6325,1510],[6390,1430]],bl)],41.15,42.1);draw(R,check(6410,1410,.8),42.15,42.75);
// 4 — support crosses the classroom boundary, then connects teachers.
num(4,43.27,43.8);label('BEYOND CLASS',6100,2830,66,44.15,45.6);
draw(B,[frame(5720,2970,260,230),W.rect(5900,3090,80,110,bl),W.line(5680,3200,6005,3200,bl)],45.8,46.7);
draw(B,W.arrow(5950,3140,6330,3140,bl),46.8,47.65);
draw(B,bubble(6230,2960,240,125),47.98,48.65);label('?',6350,3050,80,48.7,48.98);
draw(R,check(6360,3160),49.1,50.15);
draw(B,[person(5800,3490,.75),person(6100,3490,.75),person(6400,3490,.75),W.line(5840,3580,6360,3580,bl)],51.1,52.6);
draw(R,[check(5800,3600,.65),check(6100,3600,.65),check(6400,3600,.65)],52.7,53.65);
// 5 — the promised payoff: records → educational review → next-week adaptation.
num(5,54.35,54.9);label('THE FEEDBACK LOOP',4450,2830,57,55.35,56.8);
draw(B,[frame(4050,2980,270,380),W.roundRect(4120,2950,130,60,15,bl)],57.4,58.2);
draw(B,[W.line(4100,3080,4270,3080,bl),W.line(4100,3180,4270,3180,bl),W.line(4100,3280,4270,3280,bl)],58.25,59.2);
draw(R,[check(4130,3080,.55),W.circle(4160,3180,24,re),check(4250,3280,.55)],59.25,60.4);
draw(B,[W.arrow(4370,3190,4510,3190,bl),person(4650,3100,.8),person(4810,3150,.8),W.curve([[4550,3330],[4770,3380],[4870,3280]],bl)],60.9,62.6);
draw(R,W.circle(4740,3220,145,re),62.65,63.5);
draw(B,[calendar(4310,3450,330),W.arrow(4760,3390,4680,3520,bl)],63.8,64.8);label('NEXT WEEK',4475,3578,30,64.85,65.6);draw(R,check(4670,3580),65.65,66.35);
// Route between the five concepts is drawn just ahead of the travelling camera.
draw(B,W.arrow(1610,1150,2290,1150,bl),5.55,6.15);
draw(B,W.arrow(3320,1150,3980,1150,bl),19.1,19.55);
draw(B,W.arrow(5020,1150,5580,1150,bl),31.1,31.6);
draw(B,W.arrow(6490,1660,6490,2470,bl),42.8,43.3);
draw(B,W.arrow(5560,3170,5000,3170,bl),53.8,54.35);
draw(R,W.curve([[3980,3390],[3630,3370],[3560,2220],[3150,1700]],re),66.4,67.4);
// Final callback and comment instruction; not an invented official logo.
persian('brand',2800,2610,500,67.4,68.7);
label('YOUR PLAN',2800,2940,91,70.1,71.35);
draw(B,[W.roundRect(2360,3050,880,400,35,bl),W.poly([[2530,3450],[2480,3530],[2640,3450]],bl)],71.4,72.6);
persian('cta',2800,3160,545,72.65,73.65);draw(R,W.line(2520,3390,3080,3390,re),73.7,74.15);
for(const t of[0,6.15,19.55,31.6,43.27,54.35,72.6])tl.cue(t,'cap');
tl.cue(28,'magnet',{x:4500,y:1560});tl.cue(65.65,'magnet',{x:4670,y:3580});for(const j of jobs.sort((a,b)=>a.a-b.a))j.run();tl.end();
const cam=new W.Camera([[0,1100,1200,1],[5.65,1100,1200,1],[6.55,2800,1200,1],[19.15,2800,1200,1],[20,4500,1200,1],[31.15,4500,1200,1],[32,6100,1200,1],[42.85,6100,1200,1],[43.7,6100,3200,1],[53.85,6100,3200,1],[54.7,4450,3200,1],[66.4,4450,3200,1],[67.5,3900,2250,.125],[69.35,3900,2250,.125],[70.2,2800,3200,1],[75.1,2800,3200,1],[76,2800,3200,1.025]]);
// Whole labels disappear together during a travel; never leave misleading half-words at the edge.
for(const q of groups){const b=[Math.min(...q.map(s=>s.box[0])),Math.min(...q.map(s=>s.box[1])),Math.max(...q.map(s=>s.box[2])),Math.max(...q.map(s=>s.box[3]))];for(const s of q)s.hide=t=>{const c=cam.at(t);if(c.z<.3)return false;const a=W.toScreen(c,b[0],b[1]),d=W.toScreen(c,b[2],b[3]);return a[0]<50||d[0]>1030||a[1]<100||d[1]>1410;};}
const board=new W.Board(tl,{W:8000,H:4500,ghosts:[W.line(390,1800,7200,1790,{color:'#9aa0a8',alpha:.025,w:7})]});
board.objs.push({draw:(g,t,c)=>{for(const p of[K,B,R])W.drawMarker(g,p,W.penPose(p,t,cam),c,t);for(const e of tl.erasers)if(t>=e.t0&&t<=e.t1+.2)W.drawEraser(g,e,t,c);if(t>28)W.drawPinMagnet(g,4500,1560,c,{color:R.color,size:85});if(t>65.65)W.drawPinMagnet(g,4670,3580,c,{color:R.color,size:85});}});
const canvas=document.querySelector('canvas'),g=canvas.getContext('2d'),caption=document.querySelector('#caption');
const blur=new OffscreenCanvas(1080,1920),bg=blur.getContext('2d');
window.DUR=76;window.EV=tl.ev;window.CAMERA=cam.k;window.CAPTIONS=captions;
window.render=t=>{const c=cam.at(t),d=cam.at(t+1/24),travel=Math.hypot((d.x-c.x)*c.z,(d.y-c.y)*c.z)+Math.abs(d.z-c.z)*1500;
 if(travel>14){g.clearRect(0,0,1080,1920);for(let i=0;i<3;i++){board.render(bg,t+i/(24*3),cam);g.globalAlpha=1/(i+1);g.drawImage(blur,0,0);}g.globalAlpha=1;}else board.render(g,t,cam);
 const q=captions.find(c=>t>=c.start&&t<c.end);caption.textContent=q?.text||'';
};window.render(0);window.READY=true;
