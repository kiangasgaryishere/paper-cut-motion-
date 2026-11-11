import fs from 'fs';import {openDemo,closeServer} from '../../core/render/page.mjs';
const base='films/olympic-1904-gouache';const{page,browser}=await openDemo(base,{w:1080,h:1920});
const result=await page.evaluate(()=>{
 // Independently traced corridor of dirt in the painted stadium, in painting coordinates.
 const corridor=[[380,1130],[330,1290],[540,1390],[660,1180],[900,1010],[1080,970],[1080,850],[740,940],[500,1060]];
 function inside(x,y){let c=false;for(let i=0,j=corridor.length-1;i<corridor.length;j=i++){const a=corridor[i],b=corridor[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c;}return c}
 const errors=[];let feet=0,minForward=1,minSizeDrop=100;const ts=Array.from({length:301},(_,i)=>i/30);
 for(const time of ts){const t=Math.min(9.999999,time);window.render(t);const cam=window.cameraFor(t);if(540+cam.dx-540*cam.s>0||540+cam.dx+540*cam.s<1080||960+cam.dy-960*cam.s>0||960+cam.dy+960*cam.s<1920)errors.push({type:'background_edge',t});
 const states=window.runnerStates(t);for(const r of states){if(r.u<=1&&!inside(r.x,r.y))errors.push({type:'foot_outside_painted_road',t,id:r.id,x:r.x,y:r.y});feet++;
 if(t<9.9){const next=window.runnerStates(t+.05).find(n=>n.id===r.id),road=window.roadAt(r.u),vx=next.x-r.x,vy=next.y-r.y,dot=(vx*road.dx+vy*road.dy)/(Math.hypot(vx,vy)*Math.hypot(road.dx,road.dy));minForward=Math.min(minForward,dot);minSizeDrop=Math.min(minSizeDrop,r.h-next.h);if(dot<.98||vy>=0||next.h>=r.h)errors.push({type:'motion_not_forward_with_depth',t,id:r.id,dot});}}
 const title=document.querySelector('#title').getBoundingClientRect(),cap=document.querySelector('#caption').getBoundingClientRect();if(title.bottom>560||cap.top<1350)errors.push({type:'text_layout',t});}
 const captions=window.CUES.map(c=>{const frame=Math.ceil(c.t0*30-.00001);window.render(frame/30);return{start:c.t0,first_frame:frame,visible:document.querySelector('#caption').style.opacity==='1',text:document.querySelector('#caption').textContent};});if(captions.some(c=>!c.visible||/[A-Za-z]/.test(c.text)))errors.push({type:'caption_frame_or_language'});
 return{samples:ts.length,feet_checked:feet,road_corridor:corridor,min_forward_alignment:minForward,min_size_drop_per_50ms:minSizeDrop,caption_start_frames:captions,errors};
});fs.writeFileSync(base+'/motion-layout-QC-v2.json',JSON.stringify(result,null,2));console.log(JSON.stringify({samples:result.samples,feet_checked:result.feet_checked,min_forward_alignment:result.min_forward_alignment,errors:result.errors}));await browser.close();closeServer();if(result.errors.length)process.exitCode=1;
