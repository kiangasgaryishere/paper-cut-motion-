const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d', {willReadFrequently:true});
const caption = document.querySelector('#caption');
const ink = '#30251d', cream = '#f3e7cc', gold = '#d7ab5e', red = '#9c433d', blue = '#305875';
const timeline = await fetch('timeline.json').then(r => r.json());
const geometry = await fetch('assets/iran.json').then(r => r.json());
await document.fonts.load('47px Fa');
const load = async file => {const im = new Image();im.src = 'assets/'+file;await im.decode();return im;};
const art = await load('scenes.png');
const actors = await Promise.all([0,1].map(async i => Object.fromEntries(await Promise.all(
  ['head','arm','torso','legs'].map(async part => [part,await load(i+'-'+part+'.png')])))));
const tile = new OffscreenCanvas(184,184);
const texture = tile.getContext('2d');
let seed=5507;
const random = () => ((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
for(let i=0;i<6200;i++){
  texture.fillStyle=random()<.55?'#6f493a16':'#fff7e23b';
  texture.fillRect(random()*184,random()*184,.5+random()*2,.45+random()*1.25);
}
const fiber=ctx.createPattern(tile,'repeat');
const clamp=(x)=>Math.max(0,Math.min(1,x));
const ease=x=>{const v=clamp(x);return v*v*(3-2*v);};
const lerp=(a,b,t)=>a+(b-a)*t;
const rect=(x,y,w,h,fill,stroke=ink,lw=4)=>{
  ctx.fillStyle=fill;ctx.fillRect(x,y,w,h);
  if(stroke){ctx.lineWidth=lw;ctx.strokeStyle=stroke;ctx.strokeRect(x,y,w,h);}
};
function label(text,x,y,size=48,color=ink,latin=false){
  ctx.font=latin?'bold '+size+'px Georgia':size+'px Fa';
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.direction=latin?'ltr':'rtl';
  ctx.fillStyle=color;ctx.fillText(text,x,y,920);
}
function line(points,color=ink,w=4){
  ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));
  ctx.strokeStyle=color;ctx.lineWidth=w;ctx.stroke();
}
function paper(x,y,w,h,color=cream){
  ctx.fillStyle='#3e2f2638';ctx.fillRect(x+9,y+13,w,h);
  rect(x,y,w,h,color);
  ctx.fillStyle=fiber;ctx.fillRect(x,y,w,h);
}
function printImage(which,x,y,w,h,zoom=1){
  const ids={rug:0,market:1,loom:2,swatch:3};
  const q=ids[which], sw=art.width/2, sh=art.height/2;
  const scale=Math.max(w/sw,h/sh)*zoom;
  const cw=w/scale,ch=h/scale;
  paper(x-13,y-13,w+26,h+26,'#f9eed7');
  ctx.drawImage(art,(q%2)*sw+(sw-cw)/2,Math.floor(q/2)*sh+(sh-ch)/2,cw,ch,x,y,w,h);
  ctx.strokeStyle=ink;ctx.lineWidth=3;ctx.strokeRect(x,y,w,h);
}
function actor(id,x,y,s,t,face=1){
  const parts=actors[id], beat=Math.floor(t*12)/12;
  ctx.save();ctx.translate(x,y+Math.sin(beat*4+id)*8*s);ctx.scale(s*face,s);
  ctx.shadowColor='#30251d55';ctx.shadowOffsetX=6;ctx.shadowOffsetY=9;ctx.shadowBlur=6;
  ctx.drawImage(parts.legs,-72,126,144,220);
  ctx.drawImage(parts.torso,-119,-32,238,188);
  ctx.save();ctx.translate(64,0);ctx.rotate(-.13+.38*Math.sin(beat*3.9+id));
  ctx.drawImage(parts.arm,-26,-21,213,155);
  ctx.shadowColor='transparent';circle(0,0,9,gold);
  ctx.restore();
  ctx.save();ctx.translate(0,-48);ctx.rotate(.04*Math.sin(beat*4+id));
  ctx.drawImage(parts.head,-112,-211,224,238);ctx.restore();ctx.restore();
}
function circle(x,y,r,c){
  ctx.fillStyle=c;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();
}
function tag(text,x,y,w,h,t,{fill='#fff0cb',color=ink,latin=false,size=55}={}){
  if(t<0)return;
  const u=ease(t/.37);
  const rebound=t>.37?Math.sin((t-.37)*29)*Math.exp(-(t-.37)*14)*9:0;
  ctx.save();ctx.translate(x+(1-u)*320,y-(1-u)*92+rebound);ctx.rotate(-.035-(1-u)*.12);
  paper(-w/2,-h/2,w,h,fill);
  ctx.setLineDash([9,7]);ctx.strokeStyle='#886d5080';ctx.lineWidth=2;
  ctx.strokeRect(-w/2+12,-h/2+12,w-24,h-24);ctx.setLineDash([]);
  label(text,0,0,size,color,latin);ctx.restore();
}
function map(t,route=false){
  paper(111,538,858,650,'#dfd4ae');
  const project=([lon,lat])=>[185+(lon-43)*31.8,615+(40-lat)*33.5];
  for(let i=0;i<11;i++){
    ctx.setLineDash([4,8]);line([[123+i*82,553],[123+i*82,1174]],'#82795a65',2);ctx.setLineDash([]);
  }
  const polygons=geometry.type==='Polygon'?[geometry.coordinates]:geometry.coordinates;
  for(const polygon of polygons){
    const points=polygon[0].map(project);
    ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();
    ctx.fillStyle='#aeaa7c';ctx.fill();ctx.strokeStyle='#696045';ctx.lineWidth=4;ctx.stroke();
  }
  for(const [i,city] of [[[46.29,38.08],'تبریز'],[[51.44,33.98],'کاشان']].entries()){
    const [x,y]=project(city[0]);const v=ease((t-i*.6)/.4);
    if(v>0){circle(x,y,10*v,red);label(city[1],x+60,y-23,35);}
  }
  line([[165,1098],[290,1098]],ink,3);line([[165,1089],[165,1107]],ink,3);line([[290,1089],[290,1107]],ink,3);
  label('۳۵۰ کیلومتر',226,1132,22);
  const north=903;line([[north,1040],[north,1115]],ink,3);line([[north-23,1078],[north+23,1078]],ink,3);
  line([[north-10,1056],[north,1040],[north+10,1056]],ink,3);
  if(route){
    const u=ease(t/1.1);ctx.setLineDash([13,10]);line([[390,779],[532,753],[lerp(532,838,u),lerp(753,938,u)]],red,5);ctx.setLineDash([]);
    tag('کارگاهی در کشوری دیگر',708,1025,415,94,t-.45,{size:29});
  }
}
const shots=timeline.shots;
function header(title,n){
  rect(64,156,952,160,'#eee0bf');
  rect(88,178,88,100,blue);
  label(String(n+1).padStart(2,'0'),132,226,42,cream,true);
  label(title,583,234,46,ink,/^[A-Za-z]/.test(title));
}
function panel(shot,n,t){
  const {kind,title}=shot;
  rect(43,104,994,1638,'#f0e3c7',ink,9);
  ctx.fillStyle=fiber;ctx.fillRect(48,110,984,1626);
  if(title && kind!=='cta')header(title,n);
  const drift = 1+ease(t/3.4)*.047;
  if(['rug','market','loom','swatch'].includes(kind)){
    printImage(kind,100,412,880,791,drift);
    if(kind==='rug'&&n===0) tag('نقش آشنا؛ منشأ نامعلوم',543,1252,713,111,t-1.25,{size:40});
    if(kind==='swatch')tag('نقش · رنگ · بافت',540,1260,620,108,t-.9,{size:43});
  }else if(kind==='map'||kind==='route'){
    map(t,kind==='route');
  }else if(kind==='compare'){
    header('دو ویژگی متفاوت',n);
    printImage('rug',114,454,852,570,1.04);
    tag('Origin',328,1070,382,123,t,{fill:'#cedce1',latin:true,size:65});
    tag('Design',753,1070,382,123,t-.65,{fill:'#f0d6be',latin:true,size:65});
    tag('منشأ تولید',328,1226,382,106,t-1.3,{fill:'#cedce1',size:42});
    tag('طرح فرش',753,1226,382,106,t-3.8,{fill:'#f0d6be',size:42});
    const active=t>4.65?753:t>3.15?328:0;
    if(active)line([[active-125,1308],[active+125,1305]],red,6);
  }else if(kind==='debate'||kind==='weaver'){
    printImage(kind==='weaver'?'loom':'rug',139,425,802,610,1.07);
    actor(0,kind==='weaver'?320:265,1010,1.03,t);
    if(kind==='debate')actor(1,806,1025,.98,t,-1);
    if(kind==='weaver')tag('مهارتِ بافت',728,1183,365,114,t-.7,{size:41,fill:'#cedce1'});
    if(n===17)tag('؟',540,1160,172,130,t-.5,{size:86,fill:'#f4d8ad'});
  }else if(kind==='choice'){
    printImage('swatch',115,434,850,569,1.03);
    ['جای بافت','مهارت','تاریخ طرح'].forEach((s,i)=>tag(s,224+i*314,1112,287,122,t-i*.62,{size:37,fill:i===1?'#c9dce1':'#f1d9b6'}));
  }else if(kind==='cta'){
    printImage('swatch',116,360,847,600,1.06);
    tag('هنر',540,1094,657,270,t,{size:138,fill:'#d8e3e4',color:blue});
    label('کلمهٔ کامنت',540,1293,40);
  }else{
    const which=kind==='origin'?'loom':kind==='study'?'swatch':'rug';
    printImage(which,130,401,820,676,drift);
    if(kind==='tag')actor(1,242,956,.86,t);
    const word=kind==='tag'?'برچسبِ فرش':kind==='origin'?'منشأ تولید':kind==='study'?'داستان + تمرین': title;
    tag(word,kind==='tag'?662:540,1205,kind==='tag'?560:750,158,t-.32,{fill:'#e9d6ab',latin:/^[A-Za-z]/.test(word),size:52});
  }
}
function position(n){
  const row=Math.floor(n/4),col=n%4;
  return [(row%2?3-col:col)*1090,row*1930];
}
function render(t){
  ctx.setTransform(1,0,0,1,0,0);
  rect(0,0,1080,1920,'#806851',null);
  ctx.fillStyle=fiber;ctx.fillRect(0,0,1080,1920);
  let n=shots.findLastIndex(s=>t>=s.start);
  n=Math.max(n,0);
  const age=t-shots[n].start, travel=n?ease(age/.44):1;
  const next=position(n),prev=position(Math.max(n-1,0));
  const scale=lerp(.94,1,travel);
  const x=lerp(prev[0],next[0],travel),y=lerp(prev[1],next[1],travel);
  ctx.save();ctx.translate(540,920);ctx.scale(scale,scale);ctx.translate(-540-x,-920-y);
  function show(i,local){
    const [px,py]=position(i);
    ctx.save();ctx.translate(px,py);rect(0,65,1080,1710,cream,null);panel(shots[i],i,local);ctx.restore();
  }
  if(travel<1)show(n-1,shots[n].start-shots[n-1].start);
  show(n,age);
  ctx.restore();
  const cue=timeline.captions.find(c=>c.start<=t&&c.end>t);
  caption.textContent=cue?.text||'';
}
window.DUR=timeline.duration;
window.render=render;
window.TIMELINE=timeline;
render(0);
window.READY=true;
