import fs from 'fs';import crypto from 'crypto';import{openDemo,closeServer}from '../../core/render/page.mjs';
const base='films/olympic-1904-gouache';const{page,browser}=await openDemo(base,{w:1080,h:1920});
const q=await page.evaluate(()=>{const errors=[],cuts=[];let last='';
 for(let f=2100;f<2930;f++){const t=f/30;window.render(t);const s=window.HICKS_V3_STATE,c=document.querySelector('#caption'),h=document.querySelector('#title'),hr=h.getBoundingClientRect();
 if(s.kind!==last){cuts.push({frame:f,time:t,source_time:s.source_time,kind:s.kind});last=s.kind;}
 if(hr.bottom>490||h.scrollWidth>h.clientWidth+1)errors.push({frame:f,type:'heading_overflow'});
 if(c.style.opacity==='1'&&/[A-Za-z]/.test(c.textContent))errors.push({frame:f,type:'English_caption'});
 if(c.getBoundingClientRect().top<1350)errors.push({frame:f,type:'caption_outside_safe_region'});
 }
 const cues=window.EDITED_CUES.filter(c=>c.t0>=70).map(c=>{const f=Math.ceil(c.t0*30-.00001);window.render(f/30);const el=document.querySelector('#caption');if(el.style.opacity!=='1'||el.textContent!==c.text)errors.push({type:'caption_start',frame:f,expected:c.text,actual:el.textContent});return{time:c.t0,frame:f,text:c.text};});
 window.render(91.7);const transition={source:window.HICKS_V3_STATE.source_time,title:document.querySelector('#title').textContent,caption:document.querySelector('#caption').textContent};if(!transition.caption.includes('دقت کردی')||!transition.title.includes('دقت کردی'))errors.push({type:'repeated_sentence_not_removed'});
 const removed=window.EDITED_CUES.filter(c=>c.text==='و بالاخره قهرمان شد!');if(removed.length)errors.push({type:'removed_caption_still_present'});
 const vocab=FINISH.vocab.map((v,i)=>{window.render(v.start-window.HICKS_V3_EDIT.removed+.1);if(window.HICKS_V3_STATE.active_vocab!==i)errors.push({type:'vocab_desync',i});return{term:v.en,edited_time:v.start-window.HICKS_V3_EDIT.removed};});
 window.render(window.HICKS_V3_EDIT.duration-.2);const keyword=window.HICKS_V3_STATE.keyword;if(keyword!=='PHRASAL')errors.push({type:'final_CTA_missing'});
 return{patch_frames_checked:830,new_shots:cuts.filter(c=>c.kind!=='retained'),cuts,edited_captions:cues,transition,removed_caption_count:removed.length,vocab,final_keyword:keyword,duration:window.HICKS_V3_EDIT.duration,errors};});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');q.motion_checks=[];
for(const [a,b]of [[75.2,76.2],[82.5,83.5],[85.5,86.5]]){await page.evaluate(t=>window.render(t),a);const x=hash(await page.screenshot());await page.evaluate(t=>window.render(t),b);const y=hash(await page.screenshot());q.motion_checks.push({time_a:a,time_b:b,picture_changes:x!==y});if(x===y)q.errors.push({type:'static_shot',a,b});}
await page.evaluate(()=>window.render(83));const a=hash(await page.screenshot());await page.evaluate(()=>window.render(122));await page.evaluate(()=>window.render(83));q.seek_determinism=a===hash(await page.screenshot());if(!q.seek_determinism)q.errors.push({type:'seek_determinism'});
for(const t of [75.4,78.5,83,86.5,90.6,91.7,121.8]){await page.evaluate(t=>window.render(t),t);await page.screenshot({path:base+`/out/hicks-v3-${t}.jpg`});}
fs.writeFileSync(base+'/layout-QC-hicks-v3.json',JSON.stringify(q,null,2));console.log(JSON.stringify({frames:q.patch_frames_checked,new_shots:q.new_shots,caption_starts:q.edited_captions.length,transition:q.transition,keyword:q.final_keyword,motion_checks:q.motion_checks,seek:q.seek_determinism,error_count:q.errors.length,errors:q.errors.slice(0,5)}));await browser.close();closeServer();if(q.errors.length)process.exitCode=1;
