import fs from'fs';import path from'path';import{fileURLToPath}from'url';import{openDemo,closeServer}from'../../../core/render/page.mjs';
const dir=fileURLToPath(new URL('../',import.meta.url));const{page,browser}=await openDemo(dir,{w:1080,h:1920});const frames=[];
for(const t of[6.75,6.95,7.15,11.75,11.792,11.95,12.2,26.15,26.2084,26.45,41.95,42,42.2,54.25]){await page.evaluate(t=>render(t),t);await page.screenshot({path:path.join(dir,`out/transition-${t}.jpg`),type:'jpeg',quality:85});frames.push(await page.evaluate(()=>FILM_STATE));}
fs.writeFileSync(path.join(dir,'analysis/production-transitions.json'),JSON.stringify(frames,null,2));await browser.close();closeServer();
