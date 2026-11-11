/* Third review window, absolute narration interval [20,30). */
(()=>{
 const previous=window.renderAbsolute,before=new Image(),after=new Image();before.src='assets/tailoring-before-part03.png';after.src='assets/tailoring-after-part03.png';
 const priorReady=Object.getOwnPropertyDescriptor(window,'READY');let assetsReady=false;Object.defineProperty(window,'READY',{configurable:true,get:()=>priorReady.get()&&assetsReady,set:v=>priorReady.set(v)});
 const params=new URLSearchParams(location.search);window.TOTAL_DURATION=30;window.DUR=Number(params.get('end')||30)-Number(params.get('start')||0);
 const cuts={clothes:611/30,english:725/30,tailoring:785/30,left:28.85,right:29.05};
 const cues=[{t0:611/30,t1:23.833333,text:'روز مسابقه با شلوار بلند\nو پیراهن آستین‌بلند اومد!',speech_onset:20.415458,speech_end:23.532208},{t0:725/30,t1:25.8,text:'این‌طوری اومد!',speech_onset:24.21175,speech_end:25.311208},{t0:785/30,t1:30,text:'یکی از دونده‌ها قیچی برداشت\nو پاچه‌های شلوارش رو کوتاه کرد!',speech_onset:26.210958,speech_end:29.7225}];
 window.PART03_CUES=cues;window.PART03_CUTS=cuts;window.CUES=[...window.CUES,...cues];
 function picture(img,s=1,dx=0,dy=0){g.save();g.translate(540+dx,960+dy);g.scale(s,s);g.drawImage(img,-540,-960,1080,1920);g.restore();}
 function outfit(t){const age=t-cuts.clothes,cam={s:1.22,dx:-30-age*2,dy:-10};g.save();g.translate(540+cam.dx,960+cam.dy);g.scale(cam.s,cam.s);g.translate(-540,-960);g.drawImage(bg,0,0,1080,1920);const runners=runnerStates(t-10).filter(r=>r.h>25&&r.u<1.04);runners.forEach(r=>roadDust(r,t));runners.forEach(r=>paintedRunner(r,t));g.restore();const h=945+ease(age/5.8)*10,w=h*hero.width/hero.height;g.fillStyle='#1d1b1e33';g.beginPath();g.ellipse(538,1460,155,18,0,0,7);g.fill();g.save();g.translate(540+Math.sin(age*.6)*2,1460);g.rotate(Math.sin(age*1.7)*.003);g.drawImage(hero,-w/2,-h+Math.sin(age*2)*2,w,h);g.restore();}
 function offcut(t,start,x,seed){if(t<start)return;const age=t-start,p=clamp(age/.65),y=1240+350*p*p;g.save();g.translate(x+35*Math.sin(p*2+seed),y);g.rotate((p*.8-.2)*(seed%2?1:-1));g.scale(1,1-.5*p);g.beginPath();g.moveTo(-28,-65);g.lineTo(27,-62);g.lineTo(35,64);g.lineTo(-31,72);g.closePath();g.clip();g.drawImage(before,before.width*.54,before.height*.66,before.width*.10,before.height*.11,-35,-72,70,150);g.restore();}
 function tailoring(t){const age=t-cuts.tailoring,s=1+age*.002,dx=-age*.7;picture(before,s,dx);const progress=ease((t-cuts.left)/.18);if(progress>0){g.save();g.globalAlpha=progress;picture(after,s,dx);g.restore();}offcut(t,cuts.left,585,21);offcut(t,cuts.right,850,42);}
 window.renderAbsolute=absolute=>{const t=Math.max(0,Math.min(29.999999,absolute));if(t<20){previous(t);return;}if(t<cuts.clothes){previous(19.999999);return;}stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;g.clearRect(0,0,1080,1920);title.style.fontFamily='Fa';title.style.direction='rtl';title.style.color='#1D1B1E';title.style.webkitTextStroke='1.5px #F1C565';kicker.style.color='#1D1B1E';rule.style.top='405px';
 if(t<cuts.tailoring){outfit(t);if(t<cuts.english){title.textContent='با همین لباس‌ها!';title.style.fontSize='86px';kicker.textContent='روز مسابقه';}else{title.style.fontFamily='Arial, sans-serif';title.style.direction='ltr';title.textContent='He showed up\nlike this!';title.style.fontSize='76px';kicker.textContent='این‌طوری اومد!';rule.style.top='455px';}}
 else{tailoring(t);title.textContent=t<29.4?'قیچی به دادش رسید!':'شلوار، شلوارک شد!';title.style.fontSize='76px';kicker.textContent='یک کمکِ غیرمنتظره';}
 const c=cues.find(c=>t>=c.t0-.000001&&t<c.t1-.000001);cap.style.opacity=c?1:0;if(c)cap.textContent=c.text;
 };
 Promise.all([before.decode(),after.decode(),hero.decode(),document.fonts.load('700 50px Fa')]).then(()=>{assetsReady=true;window.render(0);});
})();
