from pathlib import Path
p=Path('films/a-the-kings')
crown='<path d="M-100 0 L-125 -95 L-52 -53 L0 -125 L52 -53 L125 -95 L100 0Z" fill="#bf873d" stroke="#5b4c32" stroke-width="5"/><rect x="-100" y="0" width="200" height="25" rx="7" fill="#c69954"/>'
def king(x,y,color):
 return f'<g transform="translate({x} {y})" filter="url(#s)"><path d="M-130 200L-105 -55Q0 -145 105 -55L130 200Z" fill="{color}" stroke="#eae3d3" stroke-width="14"/><circle cy="-140" r="63" fill="#c9b99b"/><path d="M-62 -160Q0 -245 62 -160L55 -199Q0 -239 -55 -199Z" fill="#403e35"/><path d="M-35 -120Q0 -87 35 -120L24 -78L-24 -78Z" fill="#6e6252"/></g>'
def text(x,y,t,size=65,color='#242923'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-family="Georgia" font-size="{size}">{t}</text>'
def card(x,y,t,color='#f6f0e4'):
 return f'<g filter="url(#s)"><rect x="{x-160}" y="{y-85}" width="320" height="125" fill="{color}"/>{text(x,y,t,62)}</g>'
def crownat(x,y,scale=1):return f'<g transform="translate({x} {y}) scale({scale})" filter="url(#s)">{crown}</g>'
scenes=[]
scenes.append((1,'THE QUESTION',card(310,470,'A')+card(770,470,'THE')+crownat(540,940,1.7)+text(540,1210,'One crown. Which article?',48)))
scenes.append((3,'THE VACANCY',text(540,410,'1066',180)+ '<g filter="url(#s)"><path d="M310 1120V650Q540 420 770 650V1120Z" fill="#82715a"/><path d="M360 1060V690Q540 500 720 690V1060Z" fill="#4e5146"/><rect x="300" y="1030" width="480" height="75" fill="#ae9874"/></g>'+crownat(540,1030,.8)+text(540,1280,'An empty throne',60)))
scenes.append((5,'THREE CLAIMANTS',crownat(540,520)+king(240,930,'#5b6652')+king(540,1100,'#68767d')+king(840,930,'#943f36')+text(240,1220,'HAROLD',30)+text(540,1390,'HARALD',30)+text(840,1220,'WILLIAM',30)))
scenes.append((8,'TWO FRONTS','<path d="M480 490L640 540L590 690L700 820L630 990L730 1140L580 1240L340 1200L430 1020L390 860L480 700Z" fill="#969985" stroke="#f6f0e4" stroke-width="20" filter="url(#s)"/><path d="M790 450Q680 550 550 730M800 1260Q650 1260 620 1140" stroke="#943f36" fill="none" stroke-width="12" stroke-dasharray="14 12"/>'+card(780,400,'NORTH')+card(760,1340,'SOUTH')))
scenes.append((11,'THE REVEAL',king(540,980,'#943f36')+crownat(540,760,.65)+card(540,490,'THE KING')+text(540,1320,'of England',70)))
scenes.append((12,'THE COMPARISON','<path d="M540 450V1310" stroke="#a59b84" stroke-width="2"/>'+card(270,570,'A KING')+card(810,570,'THE KING')+king(270,1000,'#a7a18e')+text(270,900,'?',115)+king(810,1000,'#943f36')+crownat(810,780,.55)+text(270,1340,'one, unspecified',36)+text(810,1340,'identifiable',36)))
scenes.append((13,'THE WORD ROOT',text(540,510,'A',240)+ '<path d="M540 570V790" stroke="#bf873d" stroke-width="7"/>'+card(540,940,'ĀN')+text(540,1160,'ONE',90)+ '<circle cx="540" cy="1260" r="22" fill="#bf873d"/>'))
scenes.append((15,'SHARED REFERENCE',king(220,1040,'#5b6652')+king(860,1040,'#68767d')+crownat(540,780,.8)+'<path d="M260 850L475 740M820 850L605 740" stroke="#bf873d" fill="none" stroke-width="5" stroke-dasharray="10 12"/>'+text(540,480,'THE',180)+text(540,1350,'We both know which one.',45)))
scenes.append((18,'THE INVITATION',crownat(540,620,.8)+ '<g filter="url(#s)"><path d="M210 830H870V1100H420L300 1190V1100H210Z" fill="#f6f0e4"/></g>'+text(540,1020,'THE',155)+text(540,1330,'Comment to practise',52)))
base='''<defs><filter id="s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="8" dy="14" stdDeviation="9" flood-color="#342c20" flood-opacity=".23"/></filter><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".45" numOctaves="3" seed="4"/><feColorMatrix type="saturate" values="0"/></filter></defs><rect width="1080" height="1920" fill="#eae3d3"/><rect width="1080" height="1920" filter="url(#paper)" opacity=".055"/><rect x="65" y="65" width="950" height="1790" fill="none" stroke="#a59b84"/>'''
panels=[]
for n,title,body in scenes:
 panels.append('<svg viewBox="0 0 1080 1920" width="100%" height="100%">'+base+text(540,170,f'{n:02d} / {title}',33)+body+'<rect x="110" y="1480" width="860" height="185" rx="8" fill="#242923" opacity=".07"/>'+text(540,1550,'PERSIAN CAPTION AREA',30)+text(540,1610,'English translation',28)+text(540,1770,'COMPOSITION STUDY · NOT FINAL ART',25)+'</svg>')
(p/'index.html').write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%;overflow:hidden}#frame{height:100%;width:100%}</style><div id="frame"></div><script>const frames='+__import__('json').dumps(panels)+';window.DUR=9;window.render=t=>document.getElementById("frame").innerHTML=frames[Math.min(8,Math.floor(t))];window.render(0);window.READY=true;</script>')
