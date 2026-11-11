import fs from 'fs';import crypto from 'crypto';import{openDemo,closeServer}from '../../core/render/page.mjs';
const base='films/olympic-1904-gouache';const{page,browser}=await openDemo(base,{w:1080,h:1920});
const q=await page.evaluate(()=>{const errors=[],cuts=[];let last='';
 for(let f=0;f<600;f++){const t=f/30;window.render(t);const s=window.OPENING_V2_STATE,c=document.querySelector('#caption'),h=document.querySelector('#title'),hr=h.getBoundingClientRect();if(s.kind!==last){cuts.push({frame:f,time:t,kind:s.kind});last=s.kind;}
 if(hr.bottom>555||h.scrollWidth>h.clientWidth+1)errors.push({frame:f,type:'heading_overflow'});
 if(c.style.opacity==='1'&&/[A-Za-z]/.test(c.textContent))errors.push({frame:f,type:'English_caption'});
 if(s.kind==='olympic_gate'&&s.runners.some(r=>!Number.isFinite(r.x+r.y+r.h)||r.u<0||r.u>1))errors.push({frame:f,type:'runner_geometry'});
 if(s.kind==='nonfinishers'&&s.foreground_bottom>c.getBoundingClientRect().top-12)errors.push({frame:f,type:'foreground_caption_overlap'});
 }
 window.render(8.6);const count=window.OPENING_V2_STATE;if(count.number!==18||count.marks!==18)errors.push({type:'incorrect_nonfinisher_count'});
 window.render(4.2);const a=window.OPENING_V2_STATE.runners;window.render(5.2);const b=window.OPENING_V2_STATE.runners;
 const travel=a.map(r=>{const z=b.find(x=>x.id===r.id);return{id:r.id,delta_u:z.u-r.u,delta_y:z.y-r.y,height_change:z.h-r.h};});if(travel.some(r=>r.delta_u<=0||r.delta_y>=0||r.height_change>=0))errors.push({type:'runners_not_travelling_into_depth'});
 window.render(3.5);const j1={shot:window.OPENING_V2_STATE.kind,caption:document.querySelector('#caption').textContent};window.render(7.2);const j2={shot:window.OPENING_V2_STATE.kind,caption:document.querySelector('#caption').textContent};
 if(j1.shot!=='hook_j_cut'||!j1.caption.includes('۱۹۰۴')||j2.shot!=='olympic_gate'||!j2.caption.includes('۱۸'))errors.push({type:'narrative_J_cut'});
 return{frames_checked:600,cuts,number:count.number,tally_marks:count.marks,runner_travel:travel,narrative_J_cuts:[j1,j2],errors};});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');await page.evaluate(()=>window.render(6.4));const a=hash(await page.screenshot());await page.evaluate(()=>window.render(124));await page.evaluate(()=>window.render(6.4));q.seek_determinism=a===hash(await page.screenshot());if(!q.seek_determinism)q.errors.push({type:'seek_determinism'});
for(const t of [1,4.4,6.4,8.6,10.2,10.5]){await page.evaluate(t=>window.render(t),t);await page.screenshot({path:base+`/out/revision-${t}.jpg`});}
fs.writeFileSync(base+'/layout-QC-opening-v2.json',JSON.stringify(q,null,2));console.log(JSON.stringify(q));await browser.close();closeServer();if(q.errors.length)process.exitCode=1;
