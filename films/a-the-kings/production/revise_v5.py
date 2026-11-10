import json,xml.etree.ElementTree as E
from pathlib import Path
p=Path(__file__).parent;a=json.loads((p/'art-v4.json').read_text());r=E.fromstring('<svg>'+a[18]+'</svg>')
g=next(g for g in r.iter('g') if g.get('class')=='comment-keyword');txt=g.find('text');txt.set('x','403');txt.set('text-anchor','start');E.SubElement(g,'line',{'class':'typing-caret','x1':'403','x2':'403','y1':'845','y2':'985','stroke':'#943f36','stroke-width':'5'})
a[18]=''.join(E.tostring(e,encoding='unicode') for e in r);(p/'art-v5.json').write_text(json.dumps(a));shots=json.loads((p/'scenes.json').read_text());c=json.loads((p/'captions.json').read_text());title=json.loads((p/'titles.json').read_text());meta=json.loads((p/'meta-v4.json').read_text());(p/'data.js').write_text('const ART='+json.dumps(a)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(c,ensure_ascii=False)+';const TITLES='+json.dumps(title,ensure_ascii=False)+';const META='+json.dumps(meta)+';')
