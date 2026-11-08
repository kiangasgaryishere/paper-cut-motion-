import {openDemo,closeServer} from '../../../core/render/page.mjs';
const {page,browser}=await openDemo('films/a-the-kings/production',{w:1080,h:1920});
const result=await page.evaluate(()=>{const errors=[];for(const c of CUES){window.render((c.t0+c.t1)/2);const r=document.querySelector('#caption').getBoundingClientRect();const f=document.querySelector('#fa');if(r.bottom>1750||r.top<1250||f.scrollWidth>f.clientWidth+2)errors.push({at:c.t0,top:r.top,bottom:r.bottom,overflow:f.scrollWidth-f.clientWidth});}return {cues:CUES.length,errors}});
console.log(JSON.stringify(result));await browser.close();closeServer();if(result.errors.length)process.exitCode=1;
