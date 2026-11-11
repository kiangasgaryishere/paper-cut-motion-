/* Three new Hicks compositions. One frame/sample-exact removal after the English line. */
(()=>{
 const params=new URLSearchParams(location.search);if(['original','v2'].includes(params.get('edit')))return;
 const previous=window.renderAbsolute,art={},paths={close:'hicks-close-v3.png',pov:'hicks-pov-v3.png',assisted:'hicks-assisted-v3.png'};
 for(const[k,v]of Object.entries(paths)){art[k]=new Image();art[k].src='assets/'+v;}
 const ready=Object.getOwnPropertyDescriptor(window,'READY');let loaded=false;
 Object.defineProperty(window,'READY',{configurable:true,get:()=>ready.get()&&loaded,set:v=>ready.set(v)});
 const edit={start:2749/30,end:2819/30,removed:70/30,duration:3710/30};
 const shots=[{start:2242/30,end:81,kind:'close'},{start:81,end:2554/30,kind:'pov'},{start:2554/30,end:edit.start,kind:'assisted'}];
 window.HICKS_V3_EDIT=edit;window.HICKS_V3_SHOTS=shots;window.TOTAL_DURATION=edit.duration;
 window.DUR=Number(params.get('end')||edit.duration)-Number(params.get('start')||0);
 window.EDITED_CUES=window.CUES.filter(c=>!(c.t0>=edit.start-.00001&&c.t0<edit.end-.00001)).map(c=>({...c,t0:c.t0>=edit.end-.00001?c.t0-edit.removed:c.t0,t1:c.t1>edit.end?c.t1-edit.removed:Math.min(c.t1,edit.start),speech_onset:c.speech_onset>=edit.end?c.speech_onset-edit.removed:c.speech_onset}));
 function picture(img,s,dx,dy,rot=0){g.save();g.translate(540+dx,960+dy);g.rotate(rot);g.scale(s,s);g.drawImage(img,-540,-960,1080,1920);g.restore();}
 function dust(age,seed=0){g.save();for(let i=0;i<12;i++){const p=(age*.19+rnd(i+seed))%1;g.globalAlpha=Math.sin(p*Math.PI)*.12;g.fillStyle=i%2?'#F1C565':'#FFF1CB';g.beginPath();g.ellipse(150+rnd(i+27+seed)*780+p*25,1430-p*100,2+p*7,1+p*2,-.2,0,7);g.fill();}g.restore();}
 function close(age){const s=1.015+age*.0035,dx=-6+age*2.3,dy=Math.sin(age*2.2)*1.7;picture(art.close,s,dx,dy);dust(age,70);return{camera_scale:s,camera_x:dx,breathing_y:dy};}
 function pov(age){const s=1.025+age*.007,dx=Math.sin(age*1.4)*4,dy=Math.sin(age*2)*2;picture(art.pov,s,dx,dy,Math.sin(age*1.1)*.0025);
 // Small, slow heat shimmer is confined to landscape, below the reserved title area.
 g.save();g.translate(540+dx,960+dy);g.rotate(Math.sin(age*1.1)*.0025);g.scale(s,s);g.translate(-540,-960);
 for(let y=570;y<1340;y+=8){const envelope=Math.sin((y-570)/(1340-570)*Math.PI),shift=Math.sin(y*.025-age*2.4)*2.5*envelope;g.drawImage(art.pov,0,y/1920*art.pov.height,art.pov.width,8/1920*art.pov.height,shift,y,1080,8);}
 g.restore();return{camera_scale:s,shimmer_phase:age*2.4,nearby_finish_visible:true};}
 function ribbon(age){g.save();g.strokeStyle='#A94737';g.lineWidth=10;g.lineCap='round';g.beginPath();g.moveTo(1020,1110);g.bezierCurveTo(1000+Math.sin(age*2.1)*5,1150,985+Math.sin(age*2.1+.8)*9,1180,975+Math.sin(age*2.1+1.5)*11,1215);g.stroke();g.strokeStyle='#FFF1CB';g.lineWidth=4;g.stroke();g.restore();}
 function assisted(age){const s=1.012+age*.002,dx=10-age*3.0,dy=Math.sin(age*2.6)*1.2;picture(art.assisted,s,dx,dy);ribbon(age);dust(age,200);return{camera_scale:s,track_x:dx,ribbon_phase:age*2.1};}
 window.renderAbsolute=edited=>{const t=Math.max(0,Math.min(edit.duration-.000001,edited)),source=t>=edit.start-.000001?t+edit.removed:t,shot=shots.find(s=>source>=s.start-.000001&&source<s.end-.000001);
 if(!shot){previous(source);window.HICKS_V3_STATE={edited_time:t,source_time:source,kind:'retained',keyword:window.FINISH_STATE?.keyword||'',active_vocab:window.FINISH_STATE?.active_vocab??-1};return;}
 stage.style.transform=`scale(${innerWidth/1080},${innerHeight/1920})`;g.clearRect(0,0,1080,1920);
 const s=FINISH.scenes.find(s=>source>=s.start-.000001&&source<s.end-.000001);
 title.style.top='190px';title.style.left='90px';title.style.fontFamily=s.english?'Arial, sans-serif':'Fa';title.style.direction=s.english?'ltr':'rtl';title.style.fontSize=s.size+'px';title.style.lineHeight='1.35';title.style.color='#1D1B1E';title.style.webkitTextStroke=s.english?'0px':'1.5px #F1C565';title.textContent=s.title;kicker.style.color='#1D1B1E';kicker.textContent=s.kicker;rule.style.top=s.title.includes('\n')?'445px':'405px';
 let size=s.size;while((title.getBoundingClientRect().bottom>470||title.scrollWidth>title.clientWidth+1)&&size>48){size-=2;title.style.fontSize=size+'px';}
 const age=source-shot.start,motion=shot.kind==='close'?close(age):shot.kind==='pov'?pov(age):assisted(age);
 const c=FINISH.captions.find(c=>source>=c.t0-.000001&&source<c.t1-.000001);cap.style.opacity=c?1:0;if(c)cap.textContent=c.text;
 window.HICKS_V3_STATE={edited_time:t,source_time:source,kind:shot.kind,...motion};
 };
 Promise.all(Object.values(art).map(i=>i.decode())).then(()=>{loaded=true;window.render(0);});
})();
