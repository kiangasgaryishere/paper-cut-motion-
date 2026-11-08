import fs from 'fs';import {openDemo,closeServer} from '../../../core/render/page.mjs';
const base='films/a-the-kings/production';const dir=base+'/out/caption-patches';fs.mkdirSync(dir,{recursive:true});
const {page,browser}=await openDemo(base,{w:1080,h:1920});
const cues=await page.evaluate(()=>CUES);const patches=[];const errors=[];
for(let i=0;i<cues.length;i++){
 const c=cues[i],n=Math.floor((c.speech_onset-.02)*30),t=n/30;
 await page.evaluate(t=>window.render(t),t);
 const actual=await page.locator('#fa').innerText();if(actual!==c.text)errors.push({i,n,actual,expected:c.text});
 if(Math.ceil(c.t0*30-1e-9)>n){let file=`${dir}/frame-${n}.jpg`;await page.screenshot({path:file,type:'jpeg',quality:95});patches.push({n,file,t});}
}
fs.writeFileSync(base+'/caption-frame-QC.json',JSON.stringify({cue_frames_checked:cues.length,errors,rounding_cases:patches.map(x=>x.n)},null,2));fs.writeFileSync(dir+'/manifest.json',JSON.stringify(patches,null,2));console.log({checked:cues.length,patches:patches.length,errors});await browser.close();closeServer();if(errors.length)process.exitCode=1;
