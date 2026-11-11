/* Two new painted shots and a narration J-cut; absolute recording time stays fixed. */
(()=>{
 if(new URLSearchParams(location.search).get('edit')==='original')return;
 const previous=window.renderAbsolute,gate=new Image(),tired=new Image(),road=new Image();
 gate.src='assets/olympic-gate-v2.png';tired.src='assets/exhausted-runners-v2.png';road.src='assets/valley-road.png';
 const ready=Object.getOwnPropertyDescriptor(window,'READY');let loaded=false;
 Object.defineProperty(window,'READY',{configurable:true,get:()=>ready.get()&&loaded,set:v=>ready.set(v)});
 const cuts={olympics:3.6,nonfinishers:7.3,felix:10.4};window.OPENING_V2_CUTS=cuts;
 function type(str,x,y,size,color='#1D1B1E',fa=true){g.save();g.font='900 '+size+'px '+(fa?'Fa':'Arial');g.fillStyle=color;g.textAlign='center';g.direction=fa?'rtl':'ltr';g.fillText(str,x,y);g.restore();}
 function world(img,s,dx,dy,draw){g.save();g.translate(540+dx,960+dy);g.scale(s,s);g.drawImage(img,-540,-960,1080,1920);g.translate(-540,-960);draw?.();g.restore();}
 // All moving runners and the background share this camera. Travel is into depth.
 function states(t){return Array.from({length:9},(_,i)=>{const u=.08+i*.062+(t-cuts.olympics)*.075,v=1-u;
 const pts=[[428,1540],[300,1370],[430,1190],[842,1050]],x=v**3*pts[0][0]+3*v*v*u*pts[1][0]+3*v*u*u*pts[2][0]+u**3*pts[3][0],y=v**3*pts[0][1]+3*v*v*u*pts[1][1]+3*v*u*u*pts[2][1]+u**3*pts[3][1];
 return{id:i,u,x:x+[-1,1,0][i%3]*18*(1-u),y,h:205-150*u,phase:i*.71};}).sort((a,b)=>a.y-b.y);}
 function flag(t){const x=134,y=610,w=168,h=94;g.save();
 for(let j=0;j<32;j++){const xx=j*w/32,off=Math.sin(t*4.8-j*.18)*(xx/w)*13;
 for(let k=0;k<13;k++){g.fillStyle=k%2?'#FFF1CB':'#AB4044';g.fillRect(x+xx,y+off+k*h/13,w/32+1,h/13+1);}
 if(j<13){g.fillStyle='#48505E';g.fillRect(x+xx,y+off,w/32+1,h*7/13);for(let k=0;k<5;k++){g.fillStyle='#FFF1CB';g.fillRect(x+xx+1,y+off+5+k*9,2,2);}}}g.restore();}
 function gateShot(t){const age=t-cuts.olympics,rs=states(t),s=1.08+.026*ease(age/1.2)+age*.004;
 world(gate,s,22-age*13,8,()=>{flag(t);rs.forEach(r=>roadDust(r,t));rs.forEach(r=>paintedRunner(r,t));});
 title.textContent='آمریکا • ۱۹۰۴';title.style.fontSize='96px';kicker.textContent='المپیک سنت‌لوئیس';rule.style.top='405px';
 // A second animated accent follows the spoken marathon cue, without another cut.
 if(t>=5.866667){g.save();g.globalAlpha=ease((t-5.866667)/.22);type('دوی ماراتون',540,505,49,'#48505E');g.restore();}
 return{kind:'olympic_gate',runners:rs,camera:{s,dx:22-age*13,dy:8},flag:true};}
 function failureShot(t){const age=t-cuts.nonfinishers,p=ease(age/.5),s=1.12+age*.011;
 world(road,s,-25+age*7,25,()=>{const r=roadAt(.75+age*.018);paintedRunner({x:r.x,y:r.y,h:100,phase:.7},t);});
 // Foreground breathes gently while the landscape tracks separately.
 g.save();g.translate(540,1455+Math.sin(age*3.3)*2);g.scale(.97+p*.03,1+Math.sin(age*3.3)*.002);const w=900,h=w*tired.height/tired.width;g.drawImage(tired,-w/2,-h,w,h);g.restore();
 title.textContent='۱۸ نفر نرسیدن!';title.style.fontSize='88px';kicker.textContent='این ماراتون، معمولی نبود';rule.style.top='405px';
 // Exactly 18 rough pigment tally marks: graphic emphasis, not 18 fake portraits.
 g.save();g.translate(540,650);g.scale(.88+.12*p,.88+.12*p);g.fillStyle='#1D1B1E';g.beginPath();g.ellipse(0,0,160,123,0,0,7);g.fill();type('۱۸',0,75,179,'#F1C565');g.restore();
 let marks=0;for(let i=0;i<18;i++){const a=clamp((age-.22-i*.022)/.12);if(a<=0)continue;marks++;const x=247+(i%9)*73,y=790+Math.floor(i/9)*36;g.save();g.strokeStyle='#A94738';g.lineWidth=8;g.lineCap='round';g.beginPath();g.moveTo(x,y);g.lineTo(x+17*a,y-20*a);g.stroke();g.restore();}
 return{kind:'nonfinishers',number:18,marks,foreground_bottom:1455+Math.sin(age*3.3)*2};}
 window.renderAbsolute=t=>{
 if(t<101/30||t>=cuts.felix){previous(t);window.OPENING_V2_STATE={kind:'original',time:t};return;}
 // Subtitle starts at 3.3667 s, voice at 3.416708 s, incoming picture at 3.6 s.
 if(t<cuts.olympics){previous(100/30);const c=CUES.find(c=>t>=c.t0&&t<c.t1);cap.style.opacity=c?1:0;if(c)cap.textContent=c.text;window.OPENING_V2_STATE={kind:'hook_j_cut',time:t};return;}
 stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;g.clearRect(0,0,1080,1920);
 title.style.top='190px';title.style.left='90px';title.style.fontFamily='Fa';title.style.direction='rtl';title.style.lineHeight='1.52';title.style.color='#1D1B1E';title.style.webkitTextStroke='1.5px #F1C565';kicker.style.color='#1D1B1E';
 window.OPENING_V2_STATE={time:t,...(t<cuts.nonfinishers?gateShot(t):failureShot(t))};
 const c=CUES.find(c=>t>=c.t0-.000001&&t<c.t1-.000001);cap.style.opacity=c?1:0;if(c)cap.textContent=c.text;
 };
 Promise.all([gate.decode(),tired.decode(),road.decode(),document.fonts.load('900 179px Fa')]).then(()=>{loaded=true;window.render(0);});
})();
