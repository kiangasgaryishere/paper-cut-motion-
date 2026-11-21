// Original Family Album Polaroids composition. Time is the supplied uncut narration.
const canvas=document.querySelector('canvas'),g=canvas.getContext('2d'),caption=document.querySelector('#caption');
await Promise.all([document.fonts.load('700 70px Hand'),document.fonts.load('400 52px Hand'),document.fonts.load('43px Fa')]);
const captions=await fetch('captions.json').then(r=>r.json());
const files={hosts:'hosts.png',a:'events-a.png',b:'events-b.png',retire:'retirement.png'};
const images={};await Promise.all(Object.entries(files).map(async([k,v])=>{const im=new Image();im.src='assets/'+v;await im.decode();images[k]=im;}));
const C={paper:'#eee5d2',border:'#faf4e8',ink:'#29383b',blue:'#507b94',coral:'#b86d68',pink:'#d596a5',teal:'#7ba8a5'};
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)),mix=(a,b,u)=>a+(b-a)*u,ss=u=>{u=clamp(u);return u*u*(3-2*u)},ease=(t,a,b)=>ss((t-a)/(b-a));
function rand(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const grain=new OffscreenCanvas(300,300),ng=grain.getContext('2d'),rng=rand(71),pix=ng.createImageData(300,300);
for(let i=0;i<pix.data.length;i+=4){const n=Math.round(70+rng()*100);pix.data.set([n,n-5,n-10,10+rng()*13],i);}ng.putImageData(pix,0,0);
const grainPat=g.createPattern(grain,'repeat');
// Spritesheet quadrants are cropped only by the video compositor; original generated files stay intact.
const S={hosts:['hosts'],retire:['retire'],alien:['a',0],bird:['a',1],cup:['a',2],pope:['a',3],united:['b',0],nassr:['b',1],tehran:['b',2],award:['b',3]};
const textures={};for(const [id,[k,q]]of Object.entries(S)){const im=images[k],sx=q===undefined?0:(q%2)*im.width/2,sy=q===undefined?0:Math.floor(q/2)*im.height/2,sw=q===undefined?im.width:im.width/2,sh=q===undefined?im.height:im.height/2;
 const c=new OffscreenCanvas(Math.round(sw),Math.round(sh));c.getContext('2d').drawImage(im,sx,sy,sw,sh,0,0,c.width,c.height);textures[id]=c;}
function path(points,width=4,color=C.ink){g.strokeStyle=color;g.lineWidth=width;g.lineCap='round';g.lineJoin='round';g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.stroke();}
function hand(s,x,y,h=62,color=C.ink,align='center',bold=false){g.save();g.fillStyle=color;g.font=`${bold?700:400} ${h}px Hand`;g.textAlign=align;g.textBaseline='alphabetic';g.fillText(s,x,y);g.restore();}
function fit(im,x,y,w,h,fx=.5,fy=.5,dx=0){const k=Math.max(w/im.width,h/im.height),sw=w/k,sh=h/k,sx=clamp(fx*im.width-sw/2,0,im.width-sw),sy=clamp(fy*im.height-sh/2,0,im.height-sh);g.drawImage(im,sx,sy,sw,sh,x+dx,y,w,h);}
function scene(id,x,y,w,h,t,{alive=0,fx=.5,fy=.5}={}){const im=textures[id];g.save();g.beginPath();g.rect(x,y,w,h);g.clip();g.filter=`saturate(${.90+alive*.37}) contrast(${.97+alive*.07}) brightness(1.015)`;
 if(alive>.05&&['alien'].includes(id)){
  // Horizontal panning-shutter smear on the environment; the focal subjects remain sharper.
  for(let i=-2;i<=2;i++){g.globalAlpha=i===-2?1:1/(i+3);fit(im,x-18,y,w+36,h,fx,fy,i*alive*5+Math.sin(t*.6)*alive*3);}g.globalAlpha=1;
  g.save();g.beginPath();if(id==='alien')g.ellipse(x+w*.50,y+h*.24,w*.40,h*.18,0,0,Math.PI*2);else g.roundRect(x+w*.12,y+h*.18,w*.76,h*.69,90);g.clip();fit(im,x,y,w,h,fx,fy);g.restore();
 }else fit(im,x,y,w,h,fx,fy);
 g.filter='none';g.fillStyle='rgba(47,58,58,.035)';g.fillRect(x,y,w,h);g.restore();}
function shadow(w,h){g.shadowColor='rgba(36,30,28,.22)';g.shadowBlur=18;g.shadowOffsetX=7;g.shadowOffsetY=12;g.fillStyle=C.border;g.fillRect(-w/2,-h/2,w,h);g.shadowColor='transparent';g.shadowBlur=0;g.shadowOffsetX=g.shadowOffsetY=0;}
function photo(id,x,y,w=860,h=1010,rot=0,t=0,opt={}){g.save();g.translate(x,y);g.rotate(rot);const p=opt.pad??28,bottom=opt.bottom??150;shadow(w,h);const ix=-w/2+p,iy=-h/2+p,iw=w-2*p,ih=h-p-bottom;scene(id,ix,iy,iw,ih,t,opt);
 g.strokeStyle='rgba(47,58,58,.10)';g.lineWidth=1;g.strokeRect(-w/2+.5,-h/2+.5,w-1,h-1);
 if(opt.label){const ls=Array.isArray(opt.label)?opt.label:[opt.label];ls.forEach((s,i)=>hand(s,0,h/2-bottom+65+i*62,opt.font??60,C.ink,'center',opt.bold??false));}
 if(opt.ribbon){g.fillStyle='#313938';g.beginPath();g.moveTo(w/2-170,-h/2);g.lineTo(w/2-100,-h/2);g.lineTo(w/2,-h/2+100);g.lineTo(w/2,-h/2+170);g.closePath();g.fill();}
 g.restore();}
function stamp(s,x,y,h=75,a=1,rot=-.08,color=C.coral){g.save();g.globalAlpha=a;g.translate(x,y);g.rotate(rot);g.font=`700 ${h}px Hand`;const w=g.measureText(s).width+55;g.strokeStyle=color;g.lineWidth=5;g.strokeRect(-w/2,-h*.95,w,h*1.35);hand(s,0,0,h,color,'center',true);g.restore();}
function drawAlbum(t){g.setTransform(1,0,0,1,0,0);const desk=g.createLinearGradient(0,0,1080,1920);desk.addColorStop(0,'#654339');desk.addColorStop(1,'#3e2b28');g.fillStyle=desk;g.fillRect(0,0,1080,1920);
 for(let i=0;i<30;i++){const x=i*43+Math.sin(i*8)*17;path([[x,0],[x+Math.sin(i)*25,900],[x+10,1920]],i%4===0?3:1,'#9d6f4724');}
 g.save();g.shadowColor='#181b1970';g.shadowBlur=36;g.shadowOffsetY=20;g.fillStyle='#697b78';g.beginPath();g.roundRect(22,92,1036,1658,22);g.fill();g.shadowColor='transparent';
 const pg=g.createLinearGradient(48,0,1032,0);pg.addColorStop(0,'#e7dcc7');pg.addColorStop(.46,'#f1e8d8');pg.addColorStop(.495,'#c9bda8');pg.addColorStop(.505,'#f6eddd');pg.addColorStop(.56,'#f1e8d6');pg.addColorStop(1,'#e7ddc8');g.fillStyle=pg;g.fillRect(44,113,992,1606);
 for(let i=0;i<5;i++){path([[41-i*3,125+i*5],[40-i*3,1723+i*3],[1030+i*3,1723+i*3]],1,'#c8bda9');}
 g.fillStyle=grainPat;g.fillRect(44,113,992,1606);const shine=g.createLinearGradient(80,0,1030,1920);shine.addColorStop(0,'#ffffff00');shine.addColorStop(.42,'#ffffff02');shine.addColorStop(.50,'#ffffff22');shine.addColorStop(.55,'#ffffff00');g.fillStyle=shine;g.fillRect(45,116,990,1602);g.restore();
}
function zoom(z,fx=540,fy=800,screenY=900){g.translate(540,screenY);g.scale(z,z);g.translate(-fx,-fy);}
function hero(t){let z=1,fcx=540,fcy=760,sy=900;
 if(t<5.27){z=mix(.90,2.95,ease(t,.55,4.6));fcx=mix(540,665,ease(t,1.8,4.6));fcy=mix(760,680,ease(t,1.8,4.6));}
 else if(t<8.39){z=2.95;fcx=665;fcy=680;}
 else{z=mix(2.95,.72,ease(t,8.39,9.4));fcx=mix(665,540,ease(t,8.39,9.4));fcy=mix(680,790,ease(t,8.39,9.4));}
 g.save();zoom(z,fcx,fcy,sy);photo('hosts',540,780,880,1030,-.025,t,{label:'BEFORE GTA VI',font:69,bold:true,ribbon:true,alive:ease(t,2.8,4.5)});
 if(t<4.1)hand('R.I.P. MEME',540,210,72,C.ink,'center',true);
 if(t>9.4){const q=ease(t,9.4,10.1);photo('alien',135,1370+120*(1-q),310,340,-.13,t,{label:'ALIENS',font:30,bottom:65,pad:12});photo('bird',490,1410+140*(1-q),310,340,.07,t,{label:'TWITTER / X',font:28,bottom:65,pad:12});photo('cup',850,1345+180*(1-q),310,340,.12,t,{label:'WORLD CUP',font:27,bottom:65,pad:12});if(t>11.3)stamp('ONE MORE...',800,1150,42,ease(t,11.3,11.7),.11);}
 g.restore();}
function single(id,t,start,label,opt={}){const a=ease(t,start-.35,start+.28),age=t-start;const z=1+Math.sin(clamp(age/6)*Math.PI)*.025;g.save();zoom(z,540,800,800);photo(id,540+mix(500,0,a),800,880,1040,mix(.14,opt.rot??-.025,a),t,{label,font:opt.font??66,bold:opt.bold??false,alive:opt.alive??0,fx:opt.fx??.5,fy:opt.fy??.5});g.restore();}
function aliens(t){const k=ease(t,14.16,16.15)*(1-ease(t,17.2,18.5));g.save();zoom(1+k*1.85,540,mix(800,670,k),mix(800,960,k));photo('alien',540,800,890,1030,-.016*(1-k),t,{label:'ALIENS',font:78,alive:k});g.restore();if(t>18)stamp('BEFORE GTA VI',540,1390,57,ease(t,18,18.5),.025);}
function social(t){const enter=ease(t,20.05,20.65),focus=ease(t,23.8,24.6);photo('bird',mix(1080,540,enter),790,870,1040,-.025,t,{label:'TWITTER',font:72,fx:mix(.18,.60,focus)});
 const q=ease(t,21.95,22.35);if(q>0){g.save();g.translate(600,1285+Math.sin(q*Math.PI)*-35);g.rotate(.045);g.fillStyle=C.border;g.fillRect(-220,-76,440,125);hand('X',0,5,103,C.ink,'center',true);path([[-165,-31],[-48,-31]],6,C.coral);g.restore();}
 if(t>24.25)hand('new identity. same wait.',540,1420,43,C.blue);}
function worldCup(t){single('cup',t,26.81,['MESSI','WORLD CUP'],{font:61});if(t>29.7){g.save();g.globalAlpha=Math.sin(Math.PI*clamp((t-29.7)/1.5))*.5;path([[500,390],[500,470]],3,'#fff9d8');path([[460,430],[540,430]],3,'#fff9d8');g.restore();}if(t>31)stamp('BEFORE GTA VI',540,1415,55,ease(t,31,31.45),-.025);}
function travel(t){const ids=['united','nassr','tehran'],names=['MANCHESTER UNITED','AL NASSR','TEHRAN'],starts=[33.05,35.61,36.91];
 const overview=ease(t,38.6,39.5);if(overview<1){let i=t<35.61?0:t<36.91?1:2;const e=ease(t,starts[i]-.18,starts[i]+.28);g.save();zoom(mix(1,.64,overview),540,800,800);photo(ids[i],540+mix(480,0,e),800,880,1040,-.025,t,{label:names[i],font:i===0?50:74});g.restore();}
 if(overview>0){g.save();g.globalAlpha=overview;const cfg=[[300,530,-.09],[745,800,.075],[330,1085,-.035]];for(let i=0;i<3;i++)photo(ids[i],...cfg[i].slice(0,2),455,540,cfg[i][2],t,{label:names[i],font:i===0?25:35,pad:16,bottom:90});g.restore();}
 if(t>=42.05){const q=ease(t,42.05,42.5);stamp('ALL BEFORE',650,1110,80,q,.04);stamp('GTA VI',650,1250,105,q,.04,C.blue);}}
function conclave(t){single('pope',t,44.77,['A NEW POPE','BEFORE GTA VI'],{font:60});if(t>47.7){const u=ease(t,47.7,48.1);photo('hosts',860+130*(1-u),340,270,270,.10,t,{bottom:40,pad:11,fx:.63,fy:.25});}}
function tease(t){g.save();zoom(mix(1.15,1.55,ease(t,49.6,51.6)),540,780,800);photo('hosts',540,790,880,1020,.02,t,{label:'WAIT. WHAT?',font:78,fx:.58});g.restore();}
function award(t){const r=ease(t,51.95,52.55);photo('award',540+450*(1-r),690,890,940,-.025,t,{label:'GTA VI: NOMINATED',font:55});
 // A ballpoint game label belongs to the photographed keepsake, not an official award logo.
 g.save();g.rotate(-.025);hand('VI',700,675,88,'#f6e5ea','center',true);g.restore();
 if(t>=55.25){let u=ease(t,55.25,55.7);photo('award',790,1280+150*(1-u),310,320,.07,t,{label:'BEFORE GTA VI',font:24,pad:12,bottom:65});hand('VI',835,1265,42,'#f8e9ef','center',true);}
 if(t>58){const u=ease(t,58,58.6);g.save();g.globalAlpha=u;path([[250,1300],[250,1415],[800,1415],[800,1315]],5,C.blue);path([[780,1330],[800,1305],[819,1335]],5,C.blue);g.restore();}
 if(t>59.8)stamp('BEFORE ITSELF?',530,1415,64,ease(t,59.8,60.3),-.025);}
function ending(t){let k=ease(t,62.15,65.0)*(1-ease(t,67.55,68.8)),z=1+k*.70;g.save();zoom(z,540,800,mix(800,960,k));photo('retire',540,800,900,1320,-.018*(1-k),t,{label:t<67.5?'THE WAIT IS OVER.':'R.I.P. — BEFORE GTA VI',font:48,bottom:120,alive:k,fy:.45});
 if(t>65.1&&t<67.8)stamp('RETIRED.',540,348,50,ease(t,65.1,65.5),-.06,C.blue);
g.restore();}
const SHOTS=[{id:'hook',start:0,end:14.0,visual:'memorial photo and hosts reaction',camera:'push into photograph then album pullback'},{id:'aliens',start:14,end:20.15,visual:'UFO photo with directional background smear',camera:'match push then return'},{id:'twitter',start:20.15,end:26.6,visual:'blue bird and X physical identity gag',camera:'comparison and focus'},{id:'messi',start:26.6,end:32.85,visual:'trophy and Argentina jersey',camera:'slow push'},{id:'ronaldo',start:32.85,end:44.55,visual:'three suitcase/journey photos',camera:'arrivals then three-card reveal'},{id:'pope',start:44.55,end:49.6,visual:'white cap/conclave keepsake',camera:'photo reveal and host insert'},{id:'tease',start:49.6,end:52.0,visual:'hosts reaction',camera:'anticipation push'},{id:'award',start:52,end:62.0,visual:'recursive awards/game photograph',camera:'nested inset then explaining pullback'},{id:'ending',start:62,end:71,visual:'hosts retirement portrait with enormous watch',camera:'photo comes alive then final album pullback'}];
const EV=[
 [0.05,'photo',.42,.52],[2.85,'stamp',.18,.58],[5.0,'air',.45,.14],[8.15,'page',.72,.42],[9.6,'photo',.36,.35],[10.65,'photo',.34,.3],[11.5,'tap',.12,.28],
 [13.92,'page',.52,.4],[14.20,'ufo',.65,.28],[16.2,'air',.45,.17],[18,'stamp',.17,.36],
 [20.0,'page',.56,.44],[22.05,'stamp',.18,.5],[24.2,'tap',.1,.3],
 [26.55,'photo',.38,.4],[27.15,'applause',1.25,.35],[30.4,'shutter',.2,.22],[31.05,'stamp',.15,.28],
 [32.85,'slide',.45,.43],[35.43,'slide',.36,.35],[36.75,'slide',.36,.38],[38.65,'page',.65,.34],[42.13,'stamp',.22,.57],
 [44.35,'page',.6,.43],[44.82,'bell',.9,.28],[47.8,'photo',.32,.3],[49.45,'slide',.32,.3],
 [51.80,'page',.62,.42],[52.35,'shutter',.2,.3],[54.15,'applause',.8,.25],[55.4,'photo',.25,.4],[56,'shutter',.18,.22],[59.85,'stamp',.2,.43],
 [61.8,'page',.65,.44],[62.25,'coast',2.6,.2],[65.15,'stamp',.2,.38],[67.65,'air',.5,.15],[68.2,'photo',.4,.3]
].map(([t,type,dur,gain])=>({t,type,dur,gain}));
const MILESTONES=[.14,2.85,5.27,8.4,10.7,13.2,14.16,16.2,18,20.4,22.05,24.2,26.81,29.7,31,33.05,35.61,36.91,39.2,42.2,44.77,47.8,49.81,52.27,55.38,58.2,60.1,62.2,65.15,68.2,70];
window.DUR=71;window.EV=EV;window.SHOTS=SHOTS;window.CAPTIONS=captions;window.MILESTONES=MILESTONES;
window.render=t=>{drawAlbum(t);if(t<14)hero(t);else if(t<20.15)aliens(t);else if(t<26.6)social(t);else if(t<32.85)worldCup(t);else if(t<44.55)travel(t);else if(t<49.6)conclave(t);else if(t<52)tease(t);else if(t<62)award(t);else ending(t);
 g.setTransform(1,0,0,1,0,0);const v=g.createRadialGradient(540,860,650,540,960,1150);v.addColorStop(0,'#26333200');v.addColorStop(1,'#26333214');g.fillStyle=v;g.fillRect(0,0,1080,1920);
 caption.textContent=captions.find(c=>t>=c.start&&t<c.end)?.text||'';};window.render(0);window.READY=true;
