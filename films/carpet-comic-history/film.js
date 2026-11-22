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
const extras = Object.fromEntries(await Promise.all(
  ['weaver-question','weaver-smile','rug-cut','merchant-shock','merchant-doubt','wool','weaver-focus','weaver-delight','merchant-sheepish','merchant-thinking',
   'pattern-chart','weaving-shuttle','beater-comb'].map(async id => [id,await load(id+'.png')])));
const pictures = {rug:0,market:1,loom:2,swatch:3};
function artCrop(id,x,y,w,h,zoom=1,fx=.5,fy=.5){
  const i=pictures[id], sw=art.width/2, sh=art.height/2;
  const k=Math.max(w/sw,h/sh)*zoom, cw=w/k, ch=h/k;
  ctx.drawImage(art,(i%2)*sw+(sw-cw)*fx,Math.floor(i/2)*sh+(sh-ch)*fy,cw,ch,x,y,w,h);
}
function backdrop(id,t,{zoom=1,fx=.5,fy=.5,dim=.14}={}){
  artCrop(id,0,0,1080,1920,zoom+.055*ease(t/4),fx,fy);
  const g=ctx.createLinearGradient(0,0,0,1920);
  g.addColorStop(0,'#31211a19');g.addColorStop(.52,'#31211a00');g.addColorStop(1,'#30231b76');
  ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
  ctx.fillStyle='rgba(47,31,19,'+dim+')';ctx.fillRect(0,0,1080,1920);
}
function circle(x,y,r,c){
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=c;ctx.fill();
}
const ramp=(t,a,b)=>ease((t-a)/(b-a));
const beat=(t,a,b,c,d)=>ramp(t,a,b)*(1-ramp(t,c,d));
function actor(id,x,y,size,t,face,action={}){
  const p=actors[id], head=extras[action.head]||p.head;
  const q=Math.floor(t*12)/12;
  const land=beat(q,.1,.28,.28,.55), jump=beat(q,0,.2,.2,.42);
  ctx.save();
  ctx.translate(x+(action.entry||0)*(1-ramp(q,0,.5)),y-29*jump);
  ctx.scale(size*face*(1+.07*land),size*(1-.08*land));
  ctx.rotate(action.lean||0);
  ctx.shadowColor='#271b176a';ctx.shadowOffsetX=8;ctx.shadowOffsetY=13;ctx.shadowBlur=9;
  ctx.drawImage(p.legs,-72,126,144,220);
  ctx.drawImage(p.torso,-119,-32,238,188);
  ctx.save();ctx.translate(64,0);ctx.rotate(action.arm??.1);
  ctx.drawImage(p.arm,-26,-21,213,155);
  ctx.shadowColor='transparent';circle(0,0,9,gold);
  ctx.restore();
  ctx.save();ctx.translate(0,-49);ctx.rotate(action.tilt||0);
  ctx.drawImage(head,-111,-211,222,236);
  ctx.restore();ctx.restore();
}
function prop(id,x,y,w,h,angle=0,lift=0){
  ctx.save();ctx.translate(x,y-lift);ctx.rotate(angle);
  ctx.shadowColor='#30221966';ctx.shadowBlur=9+lift*.23;
  ctx.shadowOffsetY=7+lift*.4;ctx.shadowOffsetX=5+lift*.25;
  ctx.drawImage(extras[id],-w/2,-h/2,w,h);ctx.restore();
}
function card(text,x,y,w,h,t,{fill='#fff0cb',color=ink,latin=false,size=55}={}){
  if(t<0)return;
  const u=ramp(t,0,.34);
  const bounce=t>.34?Math.sin((t-.34)*29)*Math.exp(-(t-.34)*12)*11:0;
  ctx.save();ctx.translate(x+(1-u)*165,y-(1-u)*122+bounce);ctx.rotate(-.035-(1-u)*.13);
  paper(-w/2,-h/2,w,h,fill);
  label(text,0,0,size,color,latin);
  ctx.restore();
}
function burst(x,y,t,accent=cream){
  if(t<0||t>.37)return;
  ctx.save();ctx.globalAlpha=1-t/.37;
  for(let i=0;i<9;i++){
    const a=i*Math.PI*2/9, r=38+t*120;
    line([[x+Math.cos(a)*r,y+Math.sin(a)*r],[x+Math.cos(a)*(r+32),y+Math.sin(a)*(r+32)]],accent,6);
  }
  ctx.restore();
}
function flip(t,at,x,y,front,back,width=580){
  const q=ramp(t,at,at+.34);
  ctx.save();ctx.translate(x,y);ctx.rotate(-.055);
  ctx.scale(Math.max(.015,Math.abs(Math.cos(q*Math.PI))),1);
  paper(-width/2,-70,width,140,q<.5?'#f5dfb3':'#d6e0df');
  label(q<.5?front:back,0,0,width<500?43:52);
  ctx.restore();
  burst(x+260,y-45,t-at-.29);
}
function atlas(t,route=false){
  rect(0,0,1080,1920,'#a9c2bb',null);
  ctx.fillStyle=fiber;ctx.fillRect(0,0,1080,1920);
  const project=([lon,lat])=>[65+(lon-43)*44,502+(40-lat)*52];
  ctx.setLineDash([6,10]);
  for(let i=0;i<16;i++)line([[i*79,0],[i*79,1920]],'#596e6562',2);
  for(let i=0;i<23;i++)line([[0,i*91],[1080,i*91]],'#596e6562',2);
  ctx.setLineDash([]);
  const polys=geometry.type==='Polygon'?[geometry.coordinates]:geometry.coordinates;
  for(const polygon of polys){
    ctx.beginPath();polygon[0].map(project).forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();
    for(let j=5;j>=1;j--){ctx.lineWidth=j*17;ctx.strokeStyle=j%2?'#9bb5ac':'#afc8bf';ctx.stroke();}
    ctx.fillStyle='#d6b477';ctx.fill();ctx.strokeStyle='#584932';ctx.lineWidth=5;ctx.stroke();
  }
  label('ایران',560,944,65,'#5e513c');
  for(const [i,[ll,name]] of [[[46.29,38.08],'تبریز'],[[51.44,33.98],'کاشان']].entries()){
    const [x,y]=project(ll), u=ramp(t,i*.68,i*.68+.36);
    if(u<=0)continue;
    const lift=88*(1-u);
    line([[x,y-lift],[x+12,y-32-lift]],ink,5);circle(x+12,y-36-lift,12,red);
    label(name,x+70,y-51-lift,41);
    burst(x,y,t-i*.68-.36,red);
  }
  if(route){
    const u=ramp(t,.25,1.5), x=lerp(350,880,u), y=lerp(795,1110,u)-180*Math.sin(Math.PI*u);
    ctx.setLineDash([14,11]);line([[350,795],[x,y]],red,7);ctx.setLineDash([]);
    prop('rug-cut',x,y,184,235,-.15+u*.32,25*Math.sin(Math.PI*u));
    card('کارگاهی در کشوری دیگر',704,1270,586,116,t-1.4,{size:38});
  }
}
function unroll(t){
  backdrop('market',t,{dim:.25});
  const u=ramp(t,.05,1.25);
  ctx.save();ctx.beginPath();ctx.rect(143,220,794,1100*u);ctx.clip();
  prop('rug-cut',540,774,798,1110,-.05);ctx.restore();
  if(u<1&&u>.01){
    ctx.save();ctx.translate(540,220+1100*u);
    ctx.fillStyle='#764334';ctx.shadowColor='#221b185f';ctx.shadowBlur=19;
    ctx.beginPath();ctx.roundRect(-380,-30,760,65,31);ctx.fill();
    for(let i=0;i<8;i++)line([[-358+i*101,-17],[-363+i*101,10]],'#ead5a366',4);
    ctx.restore();
  }
  const hit=beat(t,1.18,1.39,1.5,1.95);
  actor(1,805,1060,1.13,t,-1,{entry:235,arm:-.2+hit*.89,lean:-hit*.1,head:t>2?'merchant-sheepish':undefined});
  card('فرش ایرانی؟',390,1100,557,154,t-1.36,{size:74});
  burst(532,1000,t-1.70);
}
function knot(t){
  const pull=beat(t,.42,.92,1.12,1.52);
  backdrop('loom',t,{zoom:1.50,fx:.88,fy:.41,dim:.15});
  const end=lerp(800,959,pull);
  ctx.strokeStyle='#8d3c31';ctx.lineWidth=17;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(570,774);ctx.bezierCurveTo(645,842,698+pull*48,719-pull*45,end,852-pull*100);ctx.stroke();
  prop('wool',end,875-pull*100,200,182,-pull*.6,0);
  burst(577,774,t-.9);
}
function debate(t,kind){
  backdrop(kind==='weaver'?'swatch':'market',t,{fx:kind==='weaver'?.17:.53,dim:.25});
  const a=beat(t,.30,.66,.95,1.16), b=beat(t,1.02,1.35,1.85,2.17);
  if(kind!=='weaver')actor(1,815,1020,1.41,t,-1,{entry:255,arm:.16+a*.67,lean:-a*.13,tilt:.06*b,head:b>.21?'merchant-shock':t>2.18?'merchant-thinking':'merchant-doubt'});
  actor(0,kind==='weaver'?320:250,1025,1.40,t,1,{entry:-220,arm:-.31+b*.85,tilt:-.12*b,lean:.135*b,head:t<1.15?(kind==='weaver'?'weaver-focus':'weaver-question'):'weaver-delight'});
  if(kind!=='weaver')flip(t,1.23,535,1169,'ایرانی؟','کجا بافته شد؟');
  else prop('wool',600+ramp(t,.53,1.58)*147,1054,184,160,ramp(t,.53,1.58)*.58,Math.sin(ramp(t,.53,1.58)*Math.PI)*86);
}
// Three distinct material actions: passing a shuttle, beating the yarn, and folding open a chart.
function workSurface(a,b){
  const gradient=ctx.createLinearGradient(0,100,1080,1680);
  gradient.addColorStop(0,a);gradient.addColorStop(1,b);
  ctx.fillStyle=gradient;ctx.fillRect(0,0,1080,1920);
  ctx.fillStyle=fiber;ctx.fillRect(0,0,1080,1920);
}
function warp(top,bottom,count,x0,x1){
  for(let i=0;i<count;i++){
    const x=lerp(x0,x1,i/(count-1));
    line([[x,top],[x+(i%3)-1,bottom]], i%3===0?'#c5a87d':'#e0cda4',5);
    line([[x+2,top],[x+2,bottom]],'#fff0c653',2);
  }
}
function shuttleScene(t,overseas=false){
  workSurface(overseas?'#627c76':'#385063',overseas?'#324b47':'#1f3040');
  const count=overseas?19:26;
  const top=overseas?540:235, bottom=overseas?1248:1400;
  warp(top,bottom,count,42,1038);
  const passTimes=overseas?[.24,.94]:[.28,1.23,2.18];
  for(const [i,start] of passTimes.entries()){
    const u=ramp(t,start,start+.66), y=790+i*107;
    const from=i%2?1000:80,to=i%2?80:1000,x=lerp(from,to,u);
    if(!u)continue;
    line([[from,y],[x,y]],'#452525',15);
    line([[from,y-3],[x,y-3]],'#cf7563',8);
    if(t<start+.82)prop('weaving-shuttle',x,y,332,98,i%2?Math.PI:-.08,30+58*Math.sin(u*Math.PI));
    for(let j=i%2;j<count;j+=2){
      const px=lerp(42,1038,j/(count-1));
      line([[px,y-28],[px,y+28]],'#ecdbb4',6);
    }
    burst(to,y,t-start-.66,'#e6c690');
  }
  if(overseas){
    prop('pattern-chart',212,355,260,350,-.105,0);
    actor(0,788,540,1.05,t,-1,{entry:180,arm:.23,head:'weaver-focus'});
  }
}
function combScene(t){
  workSurface('#c49f68','#806347');
  ctx.save();ctx.translate(540,820);ctx.rotate(-.20);ctx.translate(-540,-820);
  warp(220,1250,19,125,955);
  for(let i=0;i<3;i++){
    const tap=.38+i*.69;
    const pull=ramp(t,tap,tap+.27);
    const y=1060-i*98+pull*55;
    line([[122,y],[950,y]],i%2?'#37536d':'#9a3d36',38);
    line([[122,y-8],[950,y-8]],i%2?'#63839b':'#c87860',7);
    burst(510,y-35,t-tap-.20,'#f9e1aa');
  }
  const step=Math.min(2,Math.max(0,Math.floor((t-.17)/.69)));
  const tap=.38+step*.69, strike=beat(t,tap-.17,tap+.20,tap+.26,tap+.56);
  prop('beater-comb',530,691-step*80+strike*170,350,474,.08-strike*.09,92*(1-strike));
  ctx.restore();
}
function chartScene(t,tools=false){
  workSurface(tools?'#cbb17e':'#6d3b43',tools?'#957344':'#412831');
  const u=ramp(t,.25,1.21);
  const w=tools?465:685,h=tools?676:918;
  const cx=tools?407:540,cy=tools?775:793;
  ctx.save();ctx.translate(cx,cy);ctx.rotate(lerp(-.14,-.045,u));
  for(const side of [-1,1]){
    ctx.save();
    const opened=ramp(u,side<0?0:.13,side<0?.68:1);
    ctx.scale(.055+.945*opened,1);
    ctx.beginPath();ctx.rect(side<0?-w/2:0,-h/2,w/2,h);ctx.clip();
    prop('pattern-chart',0,0,w,h,0,0);
    rect(side<0?-w/2:0,-h/2,w/2,h,'rgba(66,48,36,'+(.33*(1-opened))+')',null);
    ctx.restore();
  }
  line([[0,-h/2],[0,h/2]],'#53423049',3);
  ctx.restore();
  if(tools){
    const settle=ramp(t,1.1,1.65);
    prop('weaving-shuttle',821,515+(1-settle)*95,285,85,.29,45*(1-settle));
    prop('beater-comb',800,958,245,340,.20,0);
  }
  burst(cx,cy-h/2,t-1.20,'#f4d9a7');
}
function compare(t){
  backdrop('swatch',t,{dim:.45});
  prop('rug-cut',540,607,616,831,-.035,0);
  card('Origin',298,1095,370,133,t,{fill:'#dbe5e5',latin:true,size:67});
  card('Design',778,1095,370,133,t-.42,{fill:'#f2d3b3',latin:true,size:67});
  if(t>1.10) flip(t,3.16,298,1263,'محل بافت','محل بافتِ دیگر',370);
  card('همان طرح',778,1263,360,109,t-2.5,{fill:'#f2d3b3',size:44});
  if(t>4.62)line([[665,1345],[883,1341]],gold,9);
}
const shots=timeline.shots;
function scene(index,t){
  const {kind,title}=shots[index];
  if(index===0){unroll(t);return;}
  if(index===1){
    if(t>1.14){knot(t-1.14);return;}
    backdrop('rug',t,{zoom:1.13,dim:.20});
    actor(0,205,1020,1.25,t,1,{arm:.10+.58*beat(t,.23,.46,.62,1.02),entry:-130,head:'weaver-question'});
    flip(t,.53,611,1040,'نقش ایرانی','محل بافت؟');
    return;
  }
  if(kind==='map'||kind==='route'){atlas(t,kind==='route');return;}
  if(kind==='compare'){compare(t);return;}
  if(kind==='debate'||kind==='weaver'){debate(t,kind);return;}
  if(kind==='loom'){
    if(index===3||index===16)shuttleScene(t,index===16);
    else if(index===7)combScene(t);
    else chartScene(t,true);
    return;
  }
  if(kind==='cta'){
    backdrop('swatch',t,{dim:.33});
    prop('rug-cut',540,750,703,920,-.09,0);
    card('هنر',540,1100,690,278,t-.1,{size:142,fill:'#efe2ba',color:blue});
    burst(835,1010,t-.45);
    return;
  }
  if(kind==='choice'){
    backdrop('rug',t,{dim:.32});
    const cards=['محل بافت','دستِ بافنده','تاریخِ طرح'];
    cards.forEach((word,i)=>card(word,540,545+i*227,624,140,t-.28-i*.79,
      {size:59,fill:['#e7d4a5','#d9e4e6','#efd2b3'][i]}));
    return;
  }
  if(kind==='market'){
    backdrop('market',t,{fx:.22+.54*ramp(t,0,2.4),zoom:1.02,dim:.16});
    if(index===8){prop('rug-cut',280,870,385,533,-.19,15);prop('rug-cut',765,880,385,533,.12,70*(1-ramp(t,.33,1.1)));}
    else actor(1,740,1050,1.26,t,-1,{entry:290,arm:.1+.6*beat(t,.43,.77,1.28,1.67)});
    return;
  }
  if(kind==='swatch'){
    if(index===24){chartScene(t);return;}
    backdrop('swatch',t,{fx:.19+.61*ramp(t,0,2.4),dim:.10});
    if(index===9||index===20){
      prop('rug-cut',260,800,455,655,-.19,0);
      const u=ramp(t,.33,1.26);
      prop('rug-cut',lerp(278,790,u),830,455,655,.12,92*Math.sin(Math.PI*u));
      burst(935,690,t-1.26);
    }else prop('wool',755,1150,230,225,t*.72,19);
    return;
  }
  backdrop(kind==='origin'?'market':kind==='study'?'swatch':'rug',t,
    {zoom:index%2?1.11:1.02,fx:index%2?.22:.72,dim:.18});
  if(kind==='tag'||kind==='origin'){
    actor(1,235,1010,1.21,t,1,{entry:-190,arm:.03+beat(t,.43,.75,.92,1.25)*.7,head:kind==='origin'?'merchant-thinking':'merchant-sheepish'});
    flip(t,.72,619,1156,kind==='tag'?'طرح ایرانی':'محل تولید',kind==='tag'?'محل بافت؟':'مهارت بافنده؟');
  }else if(kind==='badge'||kind==='study'){
    card(title,540,1100,815,168,t-.22,{size:58,latin:/^[A-Za-z]/.test(title)});
    burst(891,1015,t-.55);
  }else{
    prop('rug-cut',545,780,595,810,-.10+.08*ramp(t,0,1.5),32*Math.sin(Math.PI*ramp(t,0,1.2)));
  }
}
function render(t){
  ctx.setTransform(1,0,0,1,0,0);
  const n=Math.max(0,shots.findLastIndex(s=>t>=s.start));
  const age=t-shots[n].start;
  if(n>0&&n%4===2&&age<.24){
    const x=1080*ramp(age,0,.24);
    ctx.save();ctx.translate(-x,0);scene(n-1,shots[n].start-shots[n-1].start+age);ctx.restore();
    ctx.save();ctx.translate(1080-x,0);scene(n,age);ctx.restore();
  }else{
    const hit=n===0?age-1.7:n===13?age-3.5:-1;
    const jitter=hit>=0&&hit<.21?Math.sin(hit*84)*(1-hit/.21)*8:0;
    if(jitter){ctx.save();ctx.translate(540+jitter,960);ctx.scale(1.023,1.023);ctx.translate(-540,-960);}
    scene(n,age);
    if(jitter)ctx.restore();
  }
  const cue=timeline.captions.find(c=>c.start<=t&&c.end>t);
  caption.textContent=cue?.text||'';
}
window.DUR=timeline.duration;
window.render=render;
window.TIMELINE=timeline;
render(0);
window.READY=true;
