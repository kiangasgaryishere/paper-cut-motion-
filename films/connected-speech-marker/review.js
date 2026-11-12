// Preproduction-only frames, using the selected upstream marker/density renderer.
import{W,H,Ink,line,curve,circle,arc,arrow,rect,makePaper,paperCanvas,composeOn,reseed,setBoil,setGlyphs}from './lib/pen.js';
const cv=document.getElementById('paper'),g=cv.getContext('2d'),stage=document.getElementById('stage'),caption=document.getElementById('caption'),ink=new Ink();
let paper;window.REVIEW_TEXTS=[];const image=g.createImageData(W,H);
const captions=['فهمیدی چی گفت؟','مثلاً «دید یو» توی گفتار سریع\nممکنه شبیه «دیدجا» شنیده بشه!','کلمهٔ «لیسن» رو کامنت کن\nتا برات بفرستیم!'];
function stroke(s){ink.add(s)}
function text(s,x,y,size=60,color='black',align='left',weight=700){const T=ink.layout(s,x,y,{size,color,align,font:'Kalam',weight,seed:170+s.length*5+x,jit:.65});ink.write(T);const left=align==='center'?x-T.w/2:align==='right'?x-T.w:x;window.REVIEW_TEXTS.push({text:s,left,right:left+T.w,baseline:y,size});return T;}
function page(n){stroke(circle(936,210,43,{w:6}));text(String(n),936,231,49,'black','center');}
function ear(x,y,s=1){stroke(curve([[x+38*s,y+110*s],[x+12*s,y+88*s],[x+6*s,y+45*s],[x+21*s,y+5*s],[x+64*s,y-13*s],[x+105*s,y+15*s],[x+112*s,y+59*s],[x+91*s,y+100*s],[x+65*s,y+133*s],[x+59*s,y+157*s],[x+39*s,y+165*s],[x+21*s,y+149*s]],{w:7}));stroke(curve([[x+40*s,y+89*s],[x+70*s,y+78*s],[x+75*s,y+40*s],[x+53*s,y+23*s],[x+32*s,y+48*s],[x+40*s,y+64*s]],{w:6}));}
function figure(x,y,hat=false){stroke(circle(x,y,42,{w:7}));stroke(curve([[x,y+45],[x-4,y+125],[x+10,y+195]],{w:8}));stroke(curve([[x-4,y+88],[x-77,y+138],[x-100,y+115]],{w:7}));stroke(curve([[x+1,y+89],[x+67,y+108],[x+83,y+78]],{w:7}));stroke(line(x+10,y+195,x-45,y+294,{w:8}));stroke(line(x+10,y+195,x+65,y+292,{w:8}));
 if(hat){stroke(line(x-69,y-28,x+65,y-28,{w:8}));stroke(curve([[x-45,y-28],[x-35,y-71],[x+30,y-69],[x+42,y-28]],{w:7}));}else{stroke(curve([[x-43,y-4],[x-52,y-34],[x-15,y-55],[x+27,y-49],[x+46,y-12]],{w:7}));}
 stroke(line(x-15,y-3,x-10,y-3,{w:6}));stroke(line(x+13,y-3,x+18,y-3,{w:6}));stroke(curve([[x-10,y+19],[x+1,y+25],[x+16,y+16]],{w:5}));}
function hook(){page(1);text('What did',105,275,102);text('you hear?',105,402,102);stroke(line(112,442,630,442,{w:7}));
 stroke(rect(110,600,860,710,{w:7}));stroke(curve([[145,1190],[245,1020],[335,1188]],{w:6}));stroke(curve([[763,1190],[842,1040],[928,1190]],{w:6}));stroke(line(150,1204,930,1204,{w:6}));
 figure(350,870,true);figure(720,880,false);
 stroke(curve([[584,740],[598,669],[720,642],[842,661],[874,725],[840,774],[758,787],[680,781],[641,812],[650,775],[598,767],[584,740]],{w:6}));
 text('First, just listen.',540,1420,54,'black','center',400);
 text('?',735,747,104,'red','center');}
function connected(){page(5);text('How does it',100,262,91);text('sound?',100,379,102);stroke(line(110,422,738,422,{w:7}));
 text('Did',270,687,116);text('you',510,687,116);text('written',540,767,42,'black','center',400);
 stroke(line(275,714,410,714,{w:6,color:'blue'}));stroke(line(520,714,665,714,{w:6,color:'blue'}));
 stroke(curve([[280,842],[312,811],[344,861],[376,813],[408,849],[440,817],[472,859],[504,806],[536,853],[568,813],[600,855],[632,817],[664,849],[696,809]],{w:6}));
 stroke(arrow(530,907,530,1024,{w:7,head:23}));ear(790,1060,.75);
 text('Didja',514,1183,137,'black','center');text('heard',540,1326,47,'black','center',400);
 stroke(arc(520,1142,194,-.12,Math.PI*2+.12,{ry:85,w:6,color:'red'}));}
function pageIcon(x,y){stroke(rect(x,y,160,206,{w:6}));for(let i=0;i<3;i++)stroke(line(x+30,y+60+i*40,x+128,y+60+i*40,{w:6}));}
function cta(){page(10);text('Ready to',104,275,100);text('practise?',104,399,100);stroke(line(112,443,650,443,{w:7}));
 stroke(arrow(540,590,540,733,{w:7,head:24}));
 stroke(curve([[173,855],[895,855],[895,1127],[390,1127],[336,1180],[337,1127],[173,1127],[173,855]],{w:7}));text('LISTEN',540,1045,120,'black','center');
 stroke(line(327,1080,750,1080,{w:7,color:'red'}));}
window.reviewInkCoverage=()=>{const q={};for(const [key,cv]of Object.entries(ink.L)){const a=cv.getContext('2d').getImageData(0,0,W,H).data;let n=0;for(let i=3;i<a.length;i+=4)n+=a[i];q[key]=n;}const total=Object.values(q).reduce((a,b)=>a+b,0);return Object.fromEntries(Object.entries(q).map(([k,v])=>[k,Math.round(v/total*10000)/100]));};
window.DUR=0;window.REVIEW_ONLY=true; // Deliberately block accidental full-video export of this gallery.
window.render=t=>{const id=Math.min(2,Math.max(0,Math.floor(t)));stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;window.REVIEW_TEXTS=[];reseed(200+id*100);setBoil(0);ink.clear();ink.setCamera([1,0,0,1,0,0]);[hook,connected,cta][id]();g.putImageData(composeOn(paper,ink,image),0,0);caption.textContent=captions[id];window.REVIEW_FRAME=id;};
Promise.all([document.fonts.load('700 100px Kalam'),document.fonts.load('400 50px Kalam'),document.fonts.load('500 47px Fa'),fetch('glyphs.json').then(r=>r.json())]).then(([, , ,glyphs])=>{setGlyphs(glyphs);const pc=paperCanvas(makePaper(44));paper=pc.getContext('2d').getImageData(0,0,W,H).data;window.render(0);window.READY=true;});
