// Technical readiness check only. Not a treatment, storyboard or production film.
import * as W from './engine/wb.js';
await Promise.all([W.loadFont('tech','fonts/EMSTech.json'),document.fonts.load('44px AD'),document.fonts.load('47px Fa')]);
const tl=new W.Timeline(),blue=new W.Pen('blue',W.INK.blue,{park:[-100,1100]}),red=new W.Pen('red',W.INK.red,{park:[1180,1100]});
tl.draw(blue,W.text('READY',600,720,{h:110,color:W.INK.blue}),.1,{by:1.1});
tl.draw(blue,W.arrow(650,1000,1370,1000,{w:9,color:W.INK.blue}),1.15,{by:1.85});
tl.draw(red,W.circle(1450,1000,70,{w:9,color:W.INK.red}),1.9,{by:2.5});
tl.end();const cam=new W.Camera([[0,1000,1100,1],[3,1100,1150,.95]]),board=new W.Board(tl,{ghosts:[W.line(600,1320,1420,1310,{color:'#9aa0a8',alpha:.06,w:7})]});
board.objs.push({draw:(g,t,c)=>{for(const p of[blue,red])W.drawMarker(g,p,W.penPose(p,t,cam),c,t);}});
const g=document.querySelector('canvas').getContext('2d');window.DUR=3;window.EV=tl.ev;window.render=t=>board.render(g,t,cam);window.render(0);window.READY=true;
