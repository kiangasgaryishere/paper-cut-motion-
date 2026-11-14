import{W,H,Ink,line,circle,makePaper,paperCanvas,composeOn,reseed,setBoil,setGlyphs}from '../connected-speech-marker/lib/pen.js';
import{clamp,lerp,eio}from '../connected-speech-marker/lib/core-utils.js';import{buildPage}from './film-art.js';
const canvas=document.getElementById('paper'),g=canvas.getContext('2d'),stage=document.getElementById('stage'),caption=document.getElementById('caption'),ink=new Ink(),Q=new URLSearchParams(location.search);
const start=Number(Q.get('start')||0),end=Number(Q.get('end')||87),LIFT=15;let DATA,PAGES=[];const out=g.createImageData(W,H),temp=document.createElement('canvas');temp.width=W;temp.height=H;const tx=temp.getContext('2d',{willReadFrequently:true});
const ca=document.createElement('canvas'),cb=document.createElement('canvas');for(const c of[ca,cb]){c.width=W;c.height=H;}const ia=g.createImageData(W,H),ib=g.createImageData(W,H);
const PUSH={};
const CACHE=new Map();const COUNTS={shrek1:121,shrek2:224,mummy:56};
async function getFrame(asset,idx){idx=Math.min(COUNTS[asset]-1,Math.max(0,idx));const key=asset+'/'+idx;if(CACHE.has(key)){const im=CACHE.get(key);CACHE.delete(key);CACHE.set(key,im);return im;}const im=await new Promise((ok,no)=>{const q=new Image();q.onload=()=>ok(q);q.onerror=no;q.src=`out/${asset}/${String(idx+1).padStart(3,'0')}.jpg`;});CACHE.set(key,im);while(CACHE.size>12)CACHE.delete(CACHE.keys().next().value);return im;}
let textBounds=[];const length=it=>it.T?it.T.L:it.len;
function compile(shot,boil){reseed(200+shot.page*100);setBoil(boil);const actions=[];
 const E=(a,b,items,kind)=>{items=[items].flat(4);actions.push({a:shot.start_frame/24+a,b:shot.start_frame/24+b,items,kind});};
 const S=(a,b,items)=>E(a,b,items,'line');
 const T=(str,x,y,size,a,b,color='black',align='left',weight=700)=>{const t=ink.layout(str,x,y,{size,color,align,font:'Kalam',weight,seed:170+str.length*5+x,jit:.65});E(a,b,{T:t},'write');if(!boil){const left=align==='center'?x-t.w/2:align==='right'?x-t.w:x;textBounds.push({page:shot.page,text:str,left,right:left+t.w,top:y-size*1.15,bottom:y+size*.32,start:shot.start_frame/24+a,end:shot.end_frame/24,color});}};
 S(shot.page===1?2.8:.01,shot.page===1?2.94:.11,circle(936,210,43,{w:6}));T(String(shot.page),936,231,49,shot.page===1?2.95:.12,shot.page===1?3.08:.24,'black','center');
 if(PUSH[shot.page-1]){const[x,y]=PUSH[shot.page-1].incoming;S(-.25,-.1,circle(x,y,28,{w:6,seed:7777,jitter:.25}));}
 buildPage({...shot,real:Q.has('real'),replay:Q.has('replay')},{S,T});
 if(PUSH[shot.page]){const[x,y]=PUSH[shot.page].out;const at=2.1;S(at,at+.12,circle(x,y,28,{w:6,seed:7777,jitter:.25}));}
 return actions;}
function transform(s,t){let z=1,cx=W/2,cy=H/2;const age=t-s.a,d=s.b-s.a;
 if(PUSH[s.page-1]&&age<.55){const q=eio(clamp(age/.55));const[x,y]=PUSH[s.page-1].incoming;z=Math.exp(lerp(Math.log(7),0,q));cx=lerp(x,540,q);cy=lerp(y,960,q);}
 else if(PUSH[s.page]&&t>s.b-.5){const q=eio(clamp((t-s.b+.5)/.5)),[x,y]=PUSH[s.page].out;z=Math.exp(lerp(0,Math.log(7),q));cx=lerp(540,x,q);cy=lerp(960,y,q);}
 else if([4,7,8,12,13].includes(s.page)){const q=eio(clamp(age/Math.max(1,d-.8)));z=1+.025*q;cx=540+(s.page===4?12:-5)*q;cy=960;}
 const hw=W/2/z,hh=H/2/z;cx=clamp(cx,hw,W-hw);cy=clamp(cy,hh,H-hh);return[z,0,0,z,540-z*cx,960-z*cy];}
function draw(s,t,image){const tq=Math.floor(t*12+1e-6)/12,boil=Math.floor(t*12+1e-6)%3,M=transform(s,t);ink.clear();ink.setCamera(M);
 for(const e of s.build[boil]){const p=clamp((tq-e.a)/(e.b-e.a));if(p<=0)continue;let left=p>=1?Infinity:p*(e.items.reduce((a,it)=>a+length(it),0)+LIFT*(e.items.length-1));
  for(const it of e.items){if(left<=0)break;if(it.T){const T=it.T,boxX=T.x+Math.min(0,...T.gl.map(c=>c.ox)),boxW=T.w;const x0=M[0]*boxX+M[4],x1=x0+M[0]*boxW,yy=M[3]*T.y+M[5];if(x0>=30&&x1<=W-30&&yy-M[3]*T.size>=20&&yy+M[3]*T.size*.3<=H-100)ink.write(T,left);}else ink.stroke(it,left);left-=length(it)+LIFT;}}
 tx.setTransform(1,0,0,1,0,0);tx.fillStyle='#FAF9F5';tx.fillRect(0,0,W,H);tx.setTransform(...M);tx.imageSmoothingQuality='high';tx.drawImage(s.paper,0,0);tx.setTransform(1,0,0,1,0,0);composeOn(tx.getImageData(0,0,W,H).data,ink,image);return M;}
function peel(t,A,B){const a=B.a,b=a+.55,u=eio(clamp((t-a)/(b-a)));draw(A,A.b-.001,ia);draw(B,t,ib);ca.getContext('2d').putImageData(ia,0,0);cb.getContext('2d').putImageData(ib,0,0);
 const n=[-W/Math.hypot(W,H),-H/Math.hypot(W,H)],tv=[-n[1],n[0]],travel=lerp(-20,Math.hypot(W,H)+260,u),F=[W+n[0]*travel,H+n[1]*travel],P=(p,v,k)=>[p[0]+v[0]*k,p[1]+v[1]*k];
 const half=sign=>{const a=P(F,tv,-4000),b=P(F,tv,4000);g.beginPath();g.moveTo(...a);g.lineTo(...b);g.lineTo(...P(b,n,sign*4000));g.lineTo(...P(a,n,sign*4000));g.closePath();};g.drawImage(cb,0,0);g.save();half(-1);g.clip();const shade=g.createLinearGradient(...F,...P(F,n,-42));shade.addColorStop(0,'rgba(70,63,51,.14)');shade.addColorStop(1,'rgba(70,63,51,0)');g.fillStyle=shade;g.fillRect(0,0,W,H);g.restore();g.save();half(1);g.clip();g.drawImage(ca,0,0);g.restore();
 const corners=[[0,0],[W,0],[W,H],[0,H]],poly=[];for(let i=0;i<4;i++){const p=corners[i],q=corners[(i+1)%4],dp=(p[0]-F[0])*n[0]+(p[1]-F[1])*n[1],dq=(q[0]-F[0])*n[0]+(q[1]-F[1])*n[1];if(dp<0)poly.push(p);if((dp<0)!==(dq<0)){const r=dp/(dp-dq);poly.push([lerp(p[0],q[0],r),lerp(p[1],q[1],r)]);}}
 if(poly.length>2){const flap=poly.map(p=>P(p,n,-2*((p[0]-F[0])*n[0]+(p[1]-F[1])*n[1])*.86));g.save();g.beginPath();flap.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.closePath();const fill=g.createLinearGradient(...F,...P(F,n,520));fill.addColorStop(0,'#E2E0D9');fill.addColorStop(.35,'#EFEDE8');fill.addColorStop(1,'#F7F6F2');g.fillStyle=fill;g.fill();g.strokeStyle='rgba(150,142,128,.25)';g.lineWidth=1;g.stroke();g.restore();}}
function soundEvents(){const ev=[];for(const s of PAGES){for(const e of s.build[0]){const total=e.items.reduce((a,it)=>a+length(it),0)+LIFT*(e.items.length-1);let offset=0;for(const it of e.items){const len=length(it),at=e.a+(e.b-e.a)*offset/total,d=(e.b-e.a)*len/total;const x=it.T?it.T.x:it.start[0];if(at>=s.a&&d>0)ev.push({type:it.T?'write':'line',t:at,d,v:len/Math.max(d,.01),x,col:it.T?it.T.color:it.color,page:s.page});offset+=len+LIFT;}}if(s.page>1){const prev=PAGES[s.page-2];ev.push({type:PUSH[prev.page]?'push':'peel',t:PUSH[prev.page]?s.a-.5:s.a,d:PUSH[prev.page]?1.05:.55,page:s.page});}}
 return ev;}


function center(asset,t){if(asset!=='mummy')return(asset==='shrek1'?(t<.75||t>=3.5):(t<.75||t>=3&&t<5||t>=8))?1010:820;if(t<.75)return lerp(1740,1680,clamp(t/.75));if(t<1.1)return lerp(1220,1080,clamp((t-.75)/.35));if(t<1.9)return 1070;return lerp(1070,1230,clamp((t-1.9)/.44));}
async function drawMovie(t,s){window.MOVIE_STATE=null;const seg=DATA.segments.find(e=>['movie','hold','reverse'].includes(e.kind)&&t>=e.start_frame/24&&t<e.end_frame/24);let e=seg;let frame,local,post=false;
const english=document.querySelector('#english'),hook=document.querySelector('#hooktitle');english.style.display='none';hook.style.display=t>=3.4&&t<8.35?'block':'none';hook.textContent=t<6.2?'چی گفت؟':'دوباره گوش کن';
if(seg){if(e.kind==='reverse'){let q=clamp((t-e.start_frame/24)/((e.end_frame-e.start_frame)/24));frame=Math.round(lerp(e.from_source_frame,e.to_source_frame,q));local=frame/24;}else if(e.kind==='hold'){frame=e.source_frame;local=frame/24;}else{local=t-e.start_frame/24+(e.source_start_frame||0)/24;frame=Math.floor(local*24+1e-5);}}
else if(s.page===1){e={asset:'shrek1',id:'opening-held',layout:'panel',end_frame:61};frame=120;local=5;post=true;}
else if(s.page===2){e={asset:'shrek1',id:'first-line-held',layout:'panel',end_frame:258};frame=92;local=92/24;post=true;}
else if(s.page===6){e={asset:'mummy',id:'mummy-held',layout:'panel',end_frame:795};frame=55;local=55/24;post=true;}
else if(s.page===9){e={asset:'mummy',id:'mummy-replay-held',layout:'panel',end_frame:1278};frame=55;local=55/24;post=true;}
else if(s.page===10){e={asset:'shrek2',id:'return-poster',layout:'panel',end_frame:1278};frame=0;local=0;post=true;}
if(!e)return;let x=60,y=e.asset==='mummy'&&s.page===6?546:596,w=960,h=e.asset==='mummy'?408:540,u=1;
if(seg){x=0;y=0;w=1080;h=1920;u=0;}
else{const end=e.end_frame/24+(e.id==='opening-held'?.25:0);if(t>=end&&t<end+.58){u=eio(clamp((t-end)/.58));x=lerp(0,x,u);y=lerp(0,y,u);w=lerp(1080,w,u);h=lerp(1920,h,u);}if(s.page===1&&t>8.35){u=1-eio(clamp((t-8.35)/(211/24-8.35)));x=lerp(0,60,u);y=lerp(0,596,u);w=lerp(1080,960,u);h=lerp(1920,540,u);}}
const im=await getFrame(e.asset,frame),sw=Math.min(im.naturalWidth,im.naturalHeight*w/h),sx=clamp(center(e.asset,local)-sw/2,0,im.naturalWidth-sw);g.save();g.imageSmoothingQuality='high';g.drawImage(im,sx,0,sw,im.naturalHeight,x,y,w,h);g.restore();
if(seg?.kind==='movie'&&seg.subtitles){let tt=t-seg.start_frame/24;const c=DATA.english_captions.find(c=>c.asset===seg.asset&&tt>=c.start&&tt<c.end);if(c){english.textContent=c.text;english.style.display='block';}}
window.MOVIE_STATE={asset:e.asset,id:e.id||e.kind,kind:e.kind||'poster',frame,rect:[x,y,w,h],subtitles:english.style.display==='block'};}
window.render=async local=>{const t=clamp(local+start,0,86.999999),s=PAGES.find(s=>t>=s.a&&t<s.b)||PAGES[PAGES.length-1];stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;if(s.page>1&&!PUSH[s.page-1]&&![2,6,9,10,11].includes(s.page)&&t<s.a+.55)peel(t,PAGES[s.page-2],s);else{draw(s,t,out);g.putImageData(out,0,0);}
 const c=DATA.captions.find(c=>t>=c.start_frame/24-1e-6&&t<c.end_frame/24-1e-6);caption.style.opacity=c?'1':'0';caption.style.fontSize=c&&c.text.length>75?'43px':'47px';if(c){caption.replaceChildren();for(const [i,part]of c.text.split('LISTEN').entries()){if(i){const span=document.createElement('bdi');span.dir='ltr';span.textContent='LISTEN';caption.appendChild(span);}caption.appendChild(document.createTextNode(part));}}
 await drawMovie(t,s);
 window.FILM_STATE={time:t,page:s.page,heading:s.heading,caption:c?.text||'',keyword:s.page===15&&t>=85?'LISTEN':'',camera:transform(s,t),transition:s.page>1&&t<s.a+.55?(PUSH[s.page-1]?'push-through':'peel'):'none'};};
if(Q.has('real')){Object.assign(caption.style,{background:'#1B1C20',color:'#FFFFFF',clipPath:'none',border:'0',borderRadius:'16px',padding:'18px 25px 24px'});}
Promise.all([document.fonts.load('700 100px Kalam'),document.fonts.load('400 50px Kalam'),document.fonts.load('500 47px Fa'),fetch('../connected-speech-marker/glyphs.json').then(r=>r.json()),fetch('timeline.json').then(r=>r.json())]).then(async([, , ,glyphs,data])=>{setGlyphs(glyphs);DATA=data;PAGES=DATA.shots.map(s=>({...s,a:s.start_frame/24,b:s.end_frame/24,build:[0,1,2].map(boil=>compile(s,boil))}));const paper=paperCanvas(makePaper(44));for(const s of PAGES)s.paper=paper;window.DUR=end-start;window.TOTAL_DURATION=87;window.EV=soundEvents();window.FILM_TEXTS=textBounds;window.PAGES=PAGES.map(({page,a,b})=>({page,a,b}));await window.render(0);window.READY=true;});

window.inkStats=()=>{const counts={};for(const[k,c]of Object.entries(ink.L)){const d=c.getContext("2d").getImageData(0,0,W,H).data;let n=0;for(let i=3;i<d.length;i+=64)if(d[i]>10)n++;counts[k]=n;}const total=Object.values(counts).reduce((a,b)=>a+b,0)||1;return{counts,blue_red_share:(counts.blue+counts.red)/total};};
