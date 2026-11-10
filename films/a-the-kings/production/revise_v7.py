import json,re,xml.etree.ElementTree as E
from pathlib import Path
p=Path(__file__).parent;a=json.loads((p/'art-v6.json').read_text())
colors={'#242923':'#14233F','#5b6652':'#3F754F','#68767d':'#3C729C','#943f36':'#B73945','#bf873d':'#D89B2A','#c69954':'#E7AE40','#8e343b':'#B62546','#969985':'#70A796','#685842':'#79532F','#694d48':'#67384F','#fffaf0':'#FFFDF4','#fff7e9':'#FFF9F2','#f4e8cb':'#FFF0C7','#e9dbb8':'#F7D797'}
for i,s in enumerate(a):
 for old,new in colors.items():s=re.sub(re.escape(old),new,s,flags=re.I)
 a[i]=s
# Colored teaching nodes and consistent comparison accents.
r=E.fromstring('<svg>'+a[14]+'</svg>')
for g in r.iter('g'):
 t=g.find('text');box=g.find('rect')
 if t is not None and box is not None and t.text in ['THE','THAT']:
  box.set('fill','#B62546' if t.text=='THE' else '#007E98');t.set('fill','#FFF9F2')
a[14]=''.join(E.tostring(e,encoding='unicode') for e in r)
a[11]+='<path class="learning-mark" d="M180 1310Q540 1340 900 1310" fill="none" stroke="#007E98" stroke-width="13" stroke-linecap="round"/>'
a[12]+='<path class="learning-mark" d="M350 1275Q540 1305 730 1275" fill="none" stroke="#B62546" stroke-width="13" stroke-linecap="round"/>'
a[15]+='<path class="learning-mark" d="M430 770C430 650 650 650 650 770C650 875 430 875 430 770" fill="none" stroke="#F3C454" stroke-width="9" stroke-linecap="round"/>'
a[17]+='<path class="learning-mark" d="M270 1150L770 1150" fill="none" stroke="#007E98" stroke-width="10" stroke-linecap="round"/>'
shots=json.loads((p/'scenes.json').read_text());c=json.loads((p/'captions.json').read_text());titles=json.loads((p/'titles.json').read_text());meta=json.loads((p/'meta-v4.json').read_text());(p/'art-v7.json').write_text(json.dumps(a));(p/'data.js').write_text('const ART='+json.dumps(a)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(c,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';const META='+json.dumps(meta)+';')
