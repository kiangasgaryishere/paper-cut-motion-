import fs from 'node:fs';
import {openDemo,closeServer} from '../../../core/render/page.mjs';
const dir='films/carpet-comic-history';
const {browser,page}=await openDemo(dir,{w:1080,h:1920,warnings:true});
try {
  const result=await page.evaluate(()=>{
    const {captions,shots}=window.TIMELINE;
    const el=document.querySelector('#caption');
    return {captions:captions.length,shots:shots.length,boxes:captions.map(c=>{
      el.textContent=c.text;
      const b=el.getBoundingClientRect();
      return {top:b.top,bottom:b.bottom,x:b.left,right:b.right,overflow:el.scrollWidth>el.clientWidth};
    })};
  });
  if(result.boxes.some(b=>b.top<1380||b.bottom>1640||b.x<90||b.right>970||b.overflow))throw Error(JSON.stringify(result.boxes));
  await page.evaluate(()=>window.render(46.9));
  const check=await page.screenshot({path:dir+'/out/v3-terms.jpg',type:'jpeg',quality:90});
  await page.evaluate(()=>window.render(0));
  await page.evaluate(()=>window.render(46.9));
  if(!check.equals(await page.screenshot({type:'jpeg',quality:90})))throw Error('Non-deterministic frame');
  for(const [t,name] of [[1.9,'hook'],[90.3,'ending']]){
    await page.evaluate(time=>window.render(time),t);
    await page.screenshot({path:dir+'/out/v3-'+name+'.jpg',type:'jpeg',quality:90});
  }
  const observedFaces=await page.evaluate(()=>{
    for(const t of [2.7,4.0,14.65,15.3,51.05,52.35,57.9,59.8,62.68])window.render(t);
    return window.USED_FACES().map(faces=>faces.sort());
  });
  const expectedFaces=[
    ['neutral','weaver-delight','weaver-focus','weaver-question'],
    ['merchant-sheepish','merchant-shock','merchant-thinking','neutral']
  ];
  if(JSON.stringify(observedFaces)!==JSON.stringify(expectedFaces))throw Error('Expected four rendered faces per character: '+JSON.stringify(observedFaces));
  result.observedFaces=observedFaces;
  fs.writeFileSync(dir+'/out/preflight.json',JSON.stringify(result,null,2));
  console.log('Checked subtitle layout, deterministic render and representative shots',result.captions,result.shots);
} finally {await browser.close();closeServer();}
