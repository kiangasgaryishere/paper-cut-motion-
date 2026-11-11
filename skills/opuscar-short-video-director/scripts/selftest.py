#!/usr/bin/env python3
"""Synthetic helper/skill checks only; no network, installations or production media."""
import copy,json,re,shutil,subprocess,tempfile,unittest,wave
from pathlib import Path
from init_project import initialize
from validate_plan import validate

ROOT=Path(__file__).resolve().parents[1]
class SkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name)
        script=self.base/'supplied.md';script.write_text('متن آمادهٔ کاربر برای بررسی ابزارها.\n',encoding='utf-8');self.project=initialize(self.base/'film',script)
    def ready(self):
        b=json.loads((self.project/'brief.json').read_text());t=json.loads((self.project/'timeline.json').read_text())
        for i in [1,2]:(self.project/f'frame-{i}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><rect width="1080" height="1920" fill="#eee"/></svg>')
        b['goal']='Synthetic validation fixture, not a production approval.';b['style'].update(identifier='test-fixture',source='https://lemomo-ai.github.io/lemo-opuscar/',invariants_recorded=True,style_frames=['frame-1.svg','frame-2.svg'])
        b['production'].update(mode_confirmed=True,participation_confirmed=True);b['audio']['narration'].update(required=False,status='not-required');b['text']['captions']['language']='fa';b['plan'].update(art_direction='ready',storyboard='ready',sound_plan='ready',review_status='approved',decision_reference='Synthetic self-test only')
        t['duration_frames']=360;t['shots']=[dict(id=f's{i}',start_frame=i*120,end_frame=(i+1)*120,visual='test composition',action='test action',camera='locked',transition_out='cut',sound_direction='silence') for i in range(3)]
        return b,t
    def save(self,b,t):
        (self.project/'brief.json').write_text(json.dumps(b));(self.project/'timeline.json').write_text(json.dumps(t));return validate(self.project)
    def test_init_requires_script_and_preserves_it(self):
        self.assertIn('متن آماده', (self.project/'script.md').read_text())
        with self.assertRaises(ValueError):initialize(self.project,self.base/'supplied.md')
        with self.assertRaises(ValueError):initialize(self.base/'other',self.base/'missing.md')
    def test_draft_is_not_ready(self):self.assertFalse(validate(self.project)['ready'])
    def test_valid_plan_and_independent_mode(self):
        b,t=self.ready();self.assertTrue(self.save(b,t)['ready']);b['production']['participation']='independent';self.assertFalse(self.save(b,t)['ready']);b['plan']['review_status']='delegated';self.assertTrue(self.save(b,t)['ready'])
    def test_gaps_and_missing_visual_events(self):
        b,t=self.ready();t['shots'][1]['start_frame']=121;self.assertFalse(self.save(b,t)['ready'])
        t['shots']=[dict(t['shots'][0],end_frame=360)];self.assertFalse(self.save(b,t)['ready']);t['milestones']=[dict(frame=f,event='subtle teaching emphasis') for f in [90,180,270]];self.assertTrue(self.save(b,t)['ready'])
    def test_caption_language_and_bounds(self):
        b,t=self.ready();t['captions']=[dict(start_frame=0,end_frame=30,text='THE')];self.assertFalse(self.save(b,t)['ready']);t['captions'][0]['text']='نمونه';self.assertTrue(self.save(b,t)['ready']);t['captions'][0]['end_frame']=400;self.assertFalse(self.save(b,t)['ready'])
    def test_sound_sync_and_negative_trim(self):
        b,t=self.ready();s=dict(id='e1',moment_frame=15,sync_at=.01,start_seconds=.49,duration_seconds=.2,source='procedural',method='test impulse',purpose='test contact',under_voiceover_db=-2);t['sound_events']=[s];self.assertTrue(self.save(b,t)['ready']);s['start_seconds']=.5;self.assertFalse(self.save(b,t)['ready']);s.update(moment_frame=0,start_seconds=0,trim_start_seconds=.01);self.assertTrue(self.save(b,t)['ready'])
    def test_source_map_cut_requires_authorization(self):
        b,t=self.ready();count=14*48000
        with wave.open(str(self.project/'voice.wav'),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(48000);wav.writeframes(bytes(count*2))
        b['audio']['narration'].update(required=True,status='provided',path='voice.wav',decoded_samples=count)
        t['source_map']=[dict(kind='source',output_start_sample=0,output_end_sample=288000,source_start_sample=0,source_end_sample=288000),dict(kind='source',output_start_sample=288000,output_end_sample=576000,source_start_sample=384000,source_end_sample=672000)]
        self.assertFalse(self.save(b,t)['ready']);t['approved_audio_edits']=[dict(source_start_sample=288000,source_end_sample=384000,approval='Synthetic test approval',reason='test cut')];self.assertTrue(self.save(b,t)['ready']);t['source_map'][1]['output_start_sample']+=1;self.assertFalse(self.save(b,t)['ready'])
    def test_local_links_frontmatter_and_shell(self):
        text=(ROOT/'SKILL.md').read_text();self.assertTrue(text.startswith('---\nname: opuscar-short-video-director\n'));self.assertIn('\ndescription: ',text)
        for file in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',file.read_text()):
                if '://' in target or target.startswith(('#','mailto:')):continue
                target=target.split('#')[0]
                self.assertTrue((file.parent/target).exists(),f'{file}: broken link {target}')
        if shutil.which('bash'):subprocess.run(['bash','-n',str(ROOT/'scripts/setup.sh')],check=True)
    def test_malformed_json_is_reported(self):
        (self.project/'timeline.json').write_text('{bad');self.assertFalse(validate(self.project)['ready'])

if __name__=='__main__':unittest.main(verbosity=2)
