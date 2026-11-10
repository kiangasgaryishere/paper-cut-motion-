import json,copy,xml.etree.ElementTree as E,math
from pathlib import Path
p=Path(__file__).parent;a=json.loads((p/'art-v3.json').read_text())
D='<defs><filter id="s" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="7" dy="12" stdDeviation="8" flood-opacity=".23"/></filter></defs>'
def text(x,y,t,size=90):return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Latin" font-size="{size}" font-weight="700" fill="#242923">{t}</text>'
def crown(x,y,s=.6):return f'<g transform="translate({x} {y}) scale({s})" filter="url(#s)"><path d="M-100 0L-125 -95L-52 -53L0 -125L52 -53L125 -95L100 0Z" fill="#bf873d" stroke="#5b4c32" stroke-width="5"/><rect x="-100" width="200" height="25" rx="7" fill="#c69954"/></g>'
root=E.fromstring('<svg>'+a[5]+'</svg>');actor=copy.deepcopy(next(g for g in root if g.tag=='g' and g.get('transform')=='translate(540 980)'));actor.set('transform','translate(540 860)')
for e in list(actor):
 if e.tag=='path' and e.get('d','').startswith('M-20 -106'):e.set('d','M-20 -106Q0 -94 20 -106')
 if e.get('fill')=='#5b6652':e.set('fill','#515c65')
 if e.tag=='path' and e.get('d','').startswith('M90 108'):actor.remove(e)
a[0]=D+'''<g filter="url(#s)"><path d="M300 1180V600Q300 430 540 410Q780 430 780 600V1180Z" fill="#a58b61"/><path d="M350 1125V620Q350 480 540 465Q730 480 730 620V1125Z" fill="#694d48"/><path d="M335 590Q540 420 745 590" fill="none" stroke="#c6aa73" stroke-width="12"/><rect x="280" y="1110" width="520" height="100" rx="15" fill="#b3986d"/><path d="M320 1210L300 1320H360L390 1210M690 1210L720 1320H780L760 1210" fill="#89734f"/><rect x="265" y="910" width="80" height="220" fill="#a58b61"/><rect x="735" y="910" width="80" height="220" fill="#a58b61"/></g>
<g class="seated-legs"><path d="M430 1040Q480 1020 530 1080L505 1250H430Z" fill="#515c65"/><path d="M550 1080Q600 1020 650 1040V1250H575Z" fill="#515c65"/><path d="M430 1230H505V1280H390Q380 1250 430 1230M575 1230H650Q700 1250 690 1280H575Z" fill="#413b31"/></g>'''+E.tostring(actor,encoding='unicode')+crown(540,630)+'''<g class="hook-card-a" filter="url(#s)"><rect x="190" y="855" width="245" height="235" rx="5" fill="#faf3e4" stroke="#c6b99d" stroke-width="3"/>'''+text(312,1010,'A',128)+'''</g><g class="hook-card-the" filter="url(#s)"><rect x="645" y="855" width="245" height="235" rx="5" fill="#faf3e4" stroke="#c6b99d" stroke-width="3"/>'''+text(767,1003,'THE',95)+'''</g><g class="hook-hands"><ellipse cx="430" cy="1010" rx="23" ry="32" fill="#cbb38e"/><ellipse cx="650" cy="1010" rx="23" ry="32" fill="#cbb38e"/></g>'''
# Geographic outline from Natural Earth (public domain); store only the England feature.
geo=p/'england-natural-earth.geojson'
if not geo.exists():
 j=json.load(open('/tmp/natural-earth-subunits.geojson'));f=next(f for f in j['features'] if f['properties'].get('SU_A3')=='ENG');geo.write_text(json.dumps({'type':'Feature','properties':{'name':'England','source':'Natural Earth 1:10m admin_0_map_subunits','license':'Public domain'},'geometry':f['geometry']},separators=(',',':')))
f=json.loads(geo.read_text());polys=f['geometry']['coordinates'];rings=[r for poly in polys for r in poly];pts=[v for r in rings for v in r];cos=math.cos(math.radians(53));xy=[(x*cos,-y) for x,y in pts];xmin=min(x for x,y in xy);xmax=max(x for x,y in xy);ymin=min(y for x,y in xy);ymax=max(y for x,y in xy);scale=min(650/(xmax-xmin),820/(ymax-ymin));cx=(xmin+xmax)/2;cy=(ymin+ymax)/2
paths=[]
for ring in rings:
 ps=[(540+(x*cos-cx)*scale,890+(-y-cy)*scale) for x,y in ring];kept=[]
 for q in ps:
  if not kept or math.dist(q,kept[-1])>1.2:kept.append(q)
 if len(kept)>2:paths.append('M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in kept)+'Z')
outline=' '.join(paths)
def england_map(i):
 return f'''<g data-map-country="england" filter="url(#s)"><defs><clipPath id="england-map-{i}"><path d="{outline}" fill-rule="evenodd"/></clipPath></defs><g clip-path="url(#england-map-{i})"><rect x="100" y="400" width="880" height="1000" fill="#fcf8ee"/><path d="M540 400V1400M100 900H980" stroke="#a7353c" stroke-width="95"/></g><path d="{outline}" fill="none" stroke="#c7bcaa" stroke-width="3" fill-rule="evenodd"/></g>'''
a[1]=D+england_map(1)
# On the needs-a-king scene, keep the country and vacancy side by side.
r=E.fromstring('<svg>'+a[3]+'</svg>');portrait=''.join(E.tostring(e,encoding='unicode') for e in r if e.tag=='g')
a[3]=D+'<g transform="translate(-75 40) scale(.78)">'+england_map(3)+'</g><g transform="translate(330 180) scale(.8)">'+portrait+'</g>'
# Keep the invasion map geographically consistent, neutral under the Norway narration.
r=E.fromstring('<svg>'+a[6]+'</svg>')
for e in r:
 if e.tag=='path' and e.get('fill')=='#969985':e.set('d',outline)
a[6]=''.join(E.tostring(e,encoding='unicode') for e in r)
# Remove the two former floating flags: only the two flag-shaped maps remain.
for i,s in enumerate(a):
 r=E.fromstring('<svg>'+s+'</svg>')
 for e in list(r):
  if e.get('data-context-flag')=='true':r.remove(e)
 a[i]=''.join(E.tostring(e,encoding='unicode') for e in r)
(p/'art-v4.json').write_text(json.dumps(a))
print('Opening: seated king holding A and THE; two actual England outlines filled by St George cross; standalone England flags removed.')
