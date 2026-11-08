import json,copy,xml.etree.ElementTree as E
from pathlib import Path
p=Path(__file__).parent;a=json.loads((p/'art-v2.json').read_text())
D='<defs><filter id="s" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="7" dy="12" stdDeviation="8" flood-opacity=".23"/></filter></defs>'
def svg(e):return E.tostring(e,encoding='unicode')
def text(x,y,t,size=60,color='#242923'):return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Latin" font-size="{size}" fill="{color}">{t}</text>'
def fa(x,y,w,t,size=44):return f'<foreignObject x="{x}" y="{y}" width="{w}" height="100"><div xmlns="http://www.w3.org/1999/xhtml" dir="rtl" style="font:{size}px Arabic;color:#242923;text-align:center">{t}</div></foreignObject>'
def card(x,y,w,h,t,size=60):return f'<g filter="url(#s)"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="6" fill="#faf3e4"/>'+text(x,y+size*.35,t,size)+'</g>'
def crown(x,y,scale=.7):return f'<g transform="translate({x} {y}) scale({scale})" filter="url(#s)"><path d="M-100 0L-125 -95L-52 -53L0 -125L52 -53L125 -95L100 0Z" fill="#bf873d" stroke="#5b4c32" stroke-width="5"/><rect x="-100" width="200" height="25" rx="7" fill="#c69954"/></g>'
def actor(index,transform):
 root=E.fromstring('<svg>'+a[index]+'</svg>')
 g=next(e for e in root if e.tag=='g' and e.get('transform')=='translate(540 980)') if index==5 else next(e for e in root if e.tag=='g' and e.get('transform')=='translate(540 1120)')
 g=copy.deepcopy(g);g.set('transform',transform)
 return g
# Keep England's contextual flag only in the introduction and the king-of-England reveal.
for i,s in enumerate(a):
 root=E.fromstring('<svg>'+s+'</svg>')
 for e in list(root):
  if e.get('data-context-flag')=='true':
   if i not in [1,10]:root.remove(e)
   else:e.set('data-country','england')
 a[i]=''.join(svg(e) for e in root)
# A Norwegian flag on the ship's mast, not a floating England badge.
mapshape='<path d="M480 490L640 540L590 690L700 820L630 990L730 1140L580 1240L340 1200L430 1020L390 860L480 700Z" fill="#969985" stroke="#f6f0e4" stroke-width="20" filter="url(#s)"/>'
a[6]=D+mapshape+'''<path d="M780 950Q700 950 550 820" fill="none" stroke="#68767d" stroke-width="10" stroke-dasharray="14 10"/>
<g class="norwegian-ship" transform="translate(760 860)" filter="url(#s)"><path d="M-140 0H140L85 65H-85Z" fill="#685842"/><path d="M-80 10H80" stroke="#a28a61" stroke-width="9"/><path d="M0 -245V0" stroke="#685842" stroke-width="10"/><path d="M12 -175V-25H140Z" fill="#eee4cf" stroke="#685842" stroke-width="5"/>
<g data-country="norway" transform="translate(0 -245)"><rect width="145" height="95" fill="#a7353c"/><path d="M45 0V95M0 47H145" stroke="#faf7ef" stroke-width="24"/><path d="M45 0V95M0 47H145" stroke="#273e60" stroke-width="12"/></g></g>'''
# A real victory tableau: Harold upright; a defeated opponent, broken shield, lowered weapon.
harold_g=actor(5,'translate(330 1000)')
for e in list(harold_g):
 if e.tag=='path' and e.get('d','').startswith('M90 108'):harold_g.remove(e)
harold=svg(harold_g)
norway=svg(actor(4,'translate(740 1060)'))
a[7]=D+'''<path d="M150 1220Q540 1170 940 1220L940 1300H150Z" fill="#c9b99b"/><g opacity=".3"><path d="M210 680H850M250 710V1050M800 710V1050" fill="none" stroke="#8e8268" stroke-width="22"/></g>'''+harold+crown(330,780,.65)+'<g class="norway-defeated">'+norway+'</g>'+'''<g class="broken-shield" filter="url(#s)"><path d="M685 1180L735 1100L758 1195L718 1280Z" fill="#68767d"/><path d="M770 1115L830 1160L800 1280L770 1220Z" fill="#68767d"/><path d="M680 1290L850 1280" stroke="#504938" stroke-width="8"/></g><path d="M453 1161L475 870M450 920L496 925" stroke="#b9b8ac" stroke-width="10"/>'''
# Death remains visible: same green Harold, closed/crossed eyes, fallen body, dropped crown and sword.
body=actor(5,'translate(540 980)')
for e in list(body):
 if e.tag=='circle' and e.get('r')=='3':
  x=float(e.get('cx'));y=float(e.get('cy'));body.remove(e)
  E.SubElement(body,'path',{'d':f'M{x-6} {y-6}L{x+6} {y+6}M{x+6} {y-6}L{x-6} {y+6}','stroke':'#242923','stroke-width':'4'})
 if e.tag=='path' and e.get('d','').startswith('M90 108'):body.remove(e)
a[9]=D+'''<path d="M150 1210Q540 1160 940 1210L940 1310H150Z" fill="#c9b99b"/><path d="M460 1160Q550 1130 665 1170Q620 1220 485 1200Z" fill="#943f36" opacity=".45"/>'''+ '<g class="harold-fallen">'+svg(body)+'</g>'+crown(820,1220,.7)+'''<g transform="rotate(84 300 1230)"><path d="M300 1300V1100M270 1255H330" stroke="#adaea7" stroke-width="12"/><path d="M300 1300V1345" stroke="#615139" stroke-width="16"/></g>'''
# Old English first; the AN > A derivation appears only when the narration reaches it.
a[13]=D+'''<g filter="url(#s)"><path d="M160 570Q340 520 540 580Q740 520 920 570V1220Q740 1170 540 1230Q340 1170 160 1220Z" fill="#d2bd93"/><path d="M180 550Q360 510 540 560V1190Q340 1140 180 1190Z" fill="#f4e8cb"/><path d="M540 560Q730 510 900 550V1190Q740 1140 540 1190Z" fill="#e9dbb8"/><path d="M540 560V1220" stroke="#b49c74" stroke-width="6"/></g>'''+text(540,650,'OLD ENGLISH',64)+'''<g opacity=".25" stroke="#887450" stroke-width="5"><path d="M225 735H460M225 770H450M610 735H845M610 770H825M225 1085H450M610 1085H825"/></g>'''+text(350,930,'ān',110)+fa(245,970,210,'«یک»',40)+'''<g class="an-to-a"><path d="M460 890H635M610 865L635 890L610 915" fill="none" stroke="#bf873d" stroke-width="10"/>'''+text(745,935,'A',125)+fa(635,990,220,'حرف تعریف',36)+'</g>'
# A family diagram, not the misleading claim that modern THAT directly turned into THE.
a[14]=D+'''<g class="family-tree" transform="translate(54 120) scale(.9)">'''+card(540,510,730,120,'OLD ENGLISH',57)+fa(200,592,680,'خانوادهٔ واژه‌های اشاره',40)+card(285,750,190,110,'sē',70)+card(540,750,190,110,'sēo',64)+card(795,750,190,110,'þæt',66)+'''<path d="M190 675H890M190 675V690M890 675V690" fill="none" stroke="#8f826b" stroke-width="5"/><path d="M285 810V885M795 810V1010" fill="none" stroke="#bf873d" stroke-width="7"/>'''+card(285,940,190,90,'þē',58)+'''<path d="M285 985V1040" stroke="#bf873d" stroke-width="7"/>'''+card(285,1100,250,120,'THE',76)+card(795,1100,250,120,'THAT',72)+'''</g><g class="deictic-example">'''+crown(540,1240,.48)+'''<path d="M350 1260L430 1205L465 1210L430 1250L475 1245L490 1270L420 1310H360Z" fill="#c9b38d" stroke="#f4ead5" stroke-width="7"/></g>'''
shots=json.loads((p/'scenes.json').read_text());cues=json.loads((p/'captions.json').read_text());titles=json.loads((p/'titles.json').read_text())
titles.update({'6':'حملهٔ پادشاه نروژ','7':'پیروزی هارولد بر نروژ','9':'هارولد کشته می‌شود','13':'ریشه در انگلیسی قدیم','14':'THE؛ از خانوادهٔ اشاره'})
for i,description in {6:'کشتی با پرچم نروژ روی دکل در کنار نقشه؛ بدون پرچم انگلیس.',7:'هارولد ایستاده، حریف نروژی شکست‌خورده و سپر شکسته.',9:'بدن افتاده هارولد با لباس سبز، چشم بسته، تاج و شمشیر روی زمین.',13:'کتاب انگلیسی قدیم؛ ān به معنی یک و اتصال به A در زمان گفتار.',14:'خانواده اشاره sē / sēo / þæt؛ مسیر þē به THE و شاخه THAT؛ مثال اشاره به تاج.'}.items():shots[i]['visual']=description
(p/'scenes.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2));(p/'titles.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2));(p/'art-v3.json').write_text(json.dumps(a))
(p/'data.js').write_text('const ART='+json.dumps(a)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(cues,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';')
assert sum('data-country="england"' in x for x in a)==2
assert 'data-country="norway"' in a[6] and 'data-country="england"' not in a[6]
print('England: scenes 2,11 only. Norway flag: ship in scene 7. Rebuilt victory, death, Old English and THE family.')
