import fs from 'fs';import path from 'path';import {openDemo,closeServer} from '../../../core/render/page.mjs';
const dir=path.resolve('films/rahnama-five-whiteboard');fs.mkdirSync(dir+'/out',{recursive:true});
const {browser,page}=await openDemo(dir,{w:1080,h:1920,warnings:true});
const report=await page.evaluate(()=>{const bad=[],overflow=[],captions=window.CAPTIONS;for(let t=0;t<window.DUR;t+=1/24){const q=captions.find(x=>t>=x.start&&t<x.end);if(q&&/[A-Za-z]/.test(q.text))bad.push(t);}return {duration:window.DUR,frames:window.DUR*24,events:window.EV,camera:window.CAMERA,caption_count:captions.length,non_persian_caption_times:bad};});
fs.writeFileSync(dir+'/out/events.json',JSON.stringify(report,null,2));
// Real DOM caption layout in Chromium, plus deterministic seek on a representative final frame.
const layouts=await page.evaluate(()=>{const e=document.querySelector('#caption');return window.CAPTIONS.map(c=>{e.textContent=c.text;return {text:e.textContent,x:e.offsetLeft,y:e.offsetTop,w:e.offsetWidth,h:e.offsetHeight,scroll:e.scrollHeight,client:e.clientHeight};});});
if(layouts.some(x=>x.y<1400||x.y+x.h>1652||x.scroll>x.client+2))throw Error('caption bounds');
await page.evaluate(()=>window.render(74.5));const a=await page.screenshot();await page.evaluate(()=>window.render(4.9));await page.evaluate(()=>window.render(74.5));const b=await page.screenshot();if(!a.equals(b))throw Error('nondeterministic seek');
fs.writeFileSync(dir+'/out/preflight.json',JSON.stringify({caption_layouts:layouts,deterministic_seek:true,event_count:report.events.length,invalid_events:report.events.filter(x=>!Number.isFinite(x.t)||x.dur<0),no_latin_captions:!report.non_persian_caption_times.length},null,2));
console.log('preflight',report.frames,'frames;',report.events.length,'events;',layouts.length,'captions');await browser.close();closeServer();
