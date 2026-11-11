/* Absolute recording time; parts are only render windows on the same timeline. */
(()=>{
 const baseRender=window.render,harbor=new Image(),table=new Image();harbor.src='assets/harbor-part02.png';table.src='assets/empty-purse-part02.png';
 let baseReady=window.READY===true,extraReady=false;Object.defineProperty(window,'READY',{configurable:true,get:()=>baseReady&&extraReady,set:v=>{baseReady=v;}});
 const params=new URLSearchParams(location.search),start=Number(params.get('start')||0),end=Number(params.get('end')||20);window.DUR=end-start;window.TOTAL_DURATION=20;
 const shots={intro:312/30,harbor:411/30,loss:479/30,english:548/30};
 const captions=[
 {t0:312/30,t1:13.3,text:'اول، فلیکس کارواخال؛\nدوندهٔ کوبایی!',speech_onset:10.451333,speech_end:13.060125},
 {t0:411/30,t1:479/30,text:'برای سفر به آمریکا\nپول جمع کرده بود.',speech_onset:13.752375,speech_end:15.929958},
 {t0:479/30,t1:17.966667,text:'ولی همه‌ش رو\nتوی قمار باخت!',speech_onset:16.0115,speech_end:17.712583},
 {t0:548/30,t1:20,text:'پولش تموم شد!',speech_onset:18.29425,speech_end:19.601417}
 ];
 window.CUES=[...window.CUES,...captions];window.PART02_CUES=captions;window.PART02_SHOTS=shots;
 function imageWorld(img,s,dx=0,dy=0){g.save();g.translate(540+dx,960+dy);g.scale(s,s);g.drawImage(img,-540,-960,1080,1920);g.restore();}
 function portrait(t,x,bottom,h){const w=h*hero.width/hero.height;g.save();g.translate(x+Math.sin(t*.7)*2,bottom);g.rotate(Math.sin(t*1.8)*.003);g.drawImage(hero,-w/2,-h+Math.sin(t*2)*2,w,h);g.restore();}
 // Ragged opaque pigment strokes stay fixed to each coin's surface as it moves.
 function coin(x,y,r,angle,seed){g.save();g.translate(x,y);g.rotate(angle);g.fillStyle='#1d1b1e45';g.beginPath();g.ellipse(3,7,r*.96,r*.35,0,0,7);g.fill();g.fillStyle='#D3A03D';g.beginPath();for(let k=0;k<=28;k++){const a=k/28*Math.PI*2,rr=r*(.95+.06*rnd(seed+k));const px=Math.cos(a)*rr,py=Math.sin(a)*rr*.73;k?g.lineTo(px,py):g.moveTo(px,py);}g.closePath();g.fill();g.strokeStyle='#F1C565';g.lineWidth=3;g.beginPath();g.ellipse(-2,-2,r*.80,r*.53,-.1,.1,3.9);g.stroke();for(let k=0;k<9;k++){g.strokeStyle=k%2?'#1d1b1e33':'#F6CF2F77';g.lineWidth=2+rnd(seed+90+k)*2;const xx=(rnd(seed+40+k)-.5)*r*1.3,yy=(rnd(seed+60+k)-.5)*r*.8;g.beginPath();g.moveTo(xx,yy);g.lineTo(xx+r*.30,yy-r*.09);g.stroke();}g.restore();}
 function paint(t){const age=t-shots.intro;title.style.direction='rtl';title.style.fontFamily='Fa';title.style.color='#1D1B1E';title.style.webkitTextStroke='1.5px #F1C565';kicker.style.color='#1D1B1E';rule.style.top='405px';
 if(t<shots.intro){paintWorld(t,cameraFor(t));title.textContent='دوی ماراتون';title.style.fontSize='90px';kicker.textContent='المپیک ۱۹۰۴';}
 else if(t<shots.harbor){paintWorld(t,{s:1.22+age*.006,dx:-40,dy:-15});g.fillStyle='#1d1b1e33';g.beginPath();g.ellipse(535,1460,170,20,0,0,7);g.fill();portrait(t,540,1460,950+ease(age/3.3)*22);title.textContent='فلیکس کارواخال';title.style.fontSize='86px';kicker.textContent='از کوبا تا المپیک';}
 else if(t<shots.loss){const a=t-shots.harbor;imageWorld(harbor,1.07+a*.006,-a*4);portrait(t,350,1440,810);for(let k=0;k<3;k++){const q=ease((a-.25-k*.40)/.25);if(q>0)coin(655+k*51,1340-10*(k%2)-(1-q)*25,23*q,-.12+k*.14,100+k*17);}title.textContent='پولِ سفر';title.style.fontSize='88px';kicker.textContent='راهیِ آمریکا';}
 else{const a=t-shots.loss,focus=ease((t-shots.english)/1.7);imageWorld(table,1.045+a*.004+focus*.025,-focus*14,-focus*8);for(let k=0;k<3;k++){const q=ease((t-(16.15+k*.60))/.65);if(q<1)coin(425+k*105+q*830,1320+q*q*130,27,Math.sin(t*4+k)*.12+q*7,210+k*13);}title.style.color='#FFF5D8';title.style.webkitTextStroke='0px';kicker.style.color='#F1C565';if(t<shots.english){title.textContent='همه‌ش رو باخت!';title.style.fontSize='84px';kicker.textContent='پولِ سفر، پایِ قمار';}else{title.style.direction='ltr';title.style.fontFamily='Arial, sans-serif';title.textContent='He ran out\nof money!';title.style.fontSize='80px';kicker.textContent='پولش تمام شد';rule.style.top='470px';}}
 const c=captions.find(c=>t>=c.t0-.000001&&t<c.t1-.000001);cap.style.opacity=c?1:0;if(c)cap.textContent=c.text;
 }
 window.renderAbsolute=absolute=>{const t=Math.max(0,Math.min(19.999999,absolute));if(t<10){title.style.fontFamily='Fa';title.style.direction='rtl';title.style.webkitTextStroke='1.5px #F1C565';baseRender(t);return;}stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;g.clearRect(0,0,1080,1920);paint(t);};
 window.render=local=>window.renderAbsolute(local+start);
 Promise.all([harbor.decode(),table.decode(),hero.decode(),document.fonts.load('700 50px Fa')]).then(()=>{extraReady=true;window.render(0);});
})();
