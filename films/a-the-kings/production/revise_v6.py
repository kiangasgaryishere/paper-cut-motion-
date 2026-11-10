import json,xml.etree.ElementTree as E
from pathlib import Path
p=Path(__file__).parent;a=json.loads((p/'art-v5.json').read_text())
r=E.fromstring('<svg>'+a[0]+'</svg>')
for g in r.iter('g'):
 cls=g.get('class','')
 if cls=='hook-card-a':g.find('rect').set('fill','#FFFAF0')
 if cls=='hook-card-the':
  g.find('rect').set('fill','#8E343B');g.find('text').set('fill','#FFF7E9')
a[0]=''.join(E.tostring(e,encoding='unicode') for e in r)
r=E.fromstring('<svg>'+a[18]+'</svg>')
for g in r.iter('g'):
 if g.get('class')=='comment-bubble':g.find('path').set('fill','#8E343B')
 if g.get('class')=='comment-keyword':
  g.find('text').set('fill','#FFF7E9');g.find('line').set('stroke','#E2BF77')
a[18]=''.join(E.tostring(e,encoding='unicode') for e in r)
shots=json.loads((p/'scenes.json').read_text());c=json.loads((p/'captions.json').read_text());titles=json.loads((p/'titles.json').read_text());meta=json.loads((p/'meta-v4.json').read_text())
(p/'art-v6.json').write_text(json.dumps(a));(p/'data.js').write_text('const ART='+json.dumps(a)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(c,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';const META='+json.dumps(meta)+';')
