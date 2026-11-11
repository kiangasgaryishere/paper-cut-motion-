#!/usr/bin/env python3
"""Validate preproduction JSON. Does not certify media, licensing or artistic quality."""
import argparse,json,math,re,sys
from fractions import Fraction
from pathlib import Path

def integer(x):return isinstance(x,int) and not isinstance(x,bool)
def number(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def validate(project):
    project=Path(project).expanduser().resolve();errors=[];warnings=[]
    def need(ok,message):
        if not ok:errors.append(message)
    def exists(path):return bool(isinstance(path,str) and path and (project/Path(path).expanduser()).is_file())
    try:
        brief=json.loads((project/'brief.json').read_text(encoding='utf-8'));t=json.loads((project/'timeline.json').read_text(encoding='utf-8'))
        need(isinstance(brief,dict) and isinstance(t,dict),'Brief and timeline must be objects.')
        if errors:return {'ready':False,'errors':errors,'warnings':warnings}
        need(brief.get('schema_version')==t.get('schema_version')==1,'Unsupported schema version.')
        script=brief.get('script',{});need(script.get('status')=='supplied' and exists(script.get('path')),'An existing supplied script is required.')
        if exists(script.get('path')):need(bool((project/script['path']).read_text(encoding='utf-8-sig').strip()),'Supplied script is empty.')
        need(bool(brief.get('goal')),'Resolve the video goal.')
        prod=brief.get('production',{});need(prod.get('mode') in ['full','ten-second'] and prod.get('mode_confirmed') is True,'Confirm full or ten-second production mode.')
        participation=prod.get('participation');need(participation in ['close-review','key-checkpoints','independent'] and prod.get('participation_confirmed') is True,'Confirm participation level.')
        plan=brief.get('plan',{})
        for section in ['art_direction','storyboard','sound_plan']:need(plan.get(section)=='ready',f'Complete {section} before production.')
        need(plan.get('review_status')==('delegated' if participation=='independent' else 'approved'),'Required plan review/delegation is unresolved.')
        need(bool(plan.get('decision_reference')),'Record the actual review/delegation decision.')
        style=brief.get('style',{});need(bool(style.get('identifier') and style.get('source')) and style.get('invariants_recorded') is True,'Record the actual Opuscar style source and invariants.')
        frames=style.get('style_frames',[]);need(isinstance(frames,list) and len(frames)>=2 and all(exists(f) for f in frames),'At least two actual style-frame files are required.')
        fps=t.get('fps');sr=t.get('sample_rate');duration=t.get('duration_frames')
        need(integer(fps) and 1<=fps<=120,'fps must be an integer from 1 to 120.')
        need(integer(sr) and sr>=8000,'sample_rate must be a positive supported integer.')
        need(integer(duration) and duration>0,'duration_frames must be a positive integer.')
        if not (integer(fps) and fps>0 and integer(sr) and sr>0 and integer(duration) and duration>0):return {'ready':False,'errors':errors,'warnings':warnings}
        need(brief.get('delivery',{}).get('fps')==fps,'Brief/timeline frame rates differ.')
        need(brief.get('audio',{}).get('sample_rate')==sr,'Brief/timeline sample rates differ.')
        text=brief.get('text',{}).get('captions',{});language=text.get('language');need(bool(language),'Resolve caption language, or explicitly choose none.')
        lead=text.get('lead_ms',0)
        if not number(lead) or not 0<=lead<=50:warnings.append('Unusual caption lead; audition explicitly rather than applying a blanket offset.')
        shots=t.get('shots',[]);need(isinstance(shots,list) and bool(shots),'Add timed shots.')
        end=0;ids=set();events={0,duration}
        for shot in shots:
            sid=shot.get('id');a=shot.get('start_frame');b=shot.get('end_frame')
            need(bool(sid) and sid not in ids,'Shot IDs must be present and unique.');ids.add(sid)
            if not (integer(a) and integer(b) and 0<=a<b<=duration):errors.append(f'Invalid shot range: {sid}');continue
            need(a==end,f'Shot gap/overlap before {sid}.');end=b;events.add(a)
            for key in ['visual','action','camera','transition_out','sound_direction']:need(bool(shot.get(key)),f'Missing {key} for {sid}.')
        need(end==duration,'Shots do not cover the complete output.')
        for event in t.get('milestones',[]):
            frame=event.get('frame');need(integer(frame) and 0<=frame<duration and bool(event.get('event')),'Invalid visual milestone.')
            if integer(frame) and 0<=frame<duration:events.add(frame)
        sequence=sorted(events)
        for a,b in zip(sequence,sequence[1:]):need(b-a<=4*fps,f'No meaningful visual event between frames {a} and {b} (over 4 seconds).')
        for group in ['captions','teaching_highlights']:
            last=0
            for cue in t.get(group,[]):
                a=cue.get('start_frame');b=cue.get('end_frame')
                valid=integer(a) and integer(b) and 0<=a<b<=duration
                need(valid,f'Invalid {group} interval.')
                if not valid:continue
                if group=='captions':
                    need(a>=last,'Overlapping/out-of-order captions.');last=b;need(bool(cue.get('text')),'Empty caption.')
                    if language=='none':errors.append('Caption cues exist while caption language is none.')
                    if language=='fa' and text.get('allow_target_language') is False:need(not re.search('[A-Za-z]',cue.get('text','')),'Latin teaching text in Persian-only bottom captions.')
                else:need(bool(cue.get('target') and cue.get('description')),'Teaching highlight needs a target and description.')
        sound_ids=set()
        for sound in t.get('sound_events',[]):
            sid=sound.get('id');need(bool(sid) and sid not in sound_ids,'Sound IDs must be present and unique.');sound_ids.add(sid)
            frame=sound.get('moment_frame');sync=sound.get('sync_at');start=sound.get('start_seconds');length=sound.get('duration_seconds')
            valid=integer(frame) and 0<=frame<duration and number(sync) and sync>=0 and number(start) and start>=0 and number(length) and length>0
            need(valid,f'Invalid sound timing: {sid}')
            if valid:
                theoretical=frame/fps-sync;trim=sound.get('trim_start_seconds',0)
                need(number(trim) and abs(trim-max(0,-theoretical))<=1/sr,f'Incorrect negative-start trim for {sid}.')
                need(abs(start-max(0,theoretical))<=1/sr,f'Sound does not meet its sync point: {sid}')
                need(start+length<=duration/fps+1/sr,f'Sound extends past output; trim/fade it: {sid}')
            need(bool(sound.get('purpose')) and number(sound.get('under_voiceover_db')),f'Missing purpose/local speech policy for {sid}.')
            if sound.get('source')=='procedural':need(bool(sound.get('method')),f'Describe procedural method for {sid}.')
            else:need(bool(sound.get('source') and sound.get('license')) and exists(sound.get('asset')),f'Select an existing sound asset and record source/license: {sid}')
        narration=brief.get('audio',{}).get('narration',{})
        if narration.get('required') is False:need(narration.get('status')=='not-required','Explicitly resolve no-narration policy.')
        else:
            count=narration.get('decoded_samples');need(narration.get('status')=='provided' and exists(narration.get('path')) and integer(count) and count>0,'Lock actual narration file and decoded sample count.')
            mapping=t.get('source_map',[]);need(bool(mapping),'Add the narration source/output map.')
            output_end=0;source_end=0
            approved=t.get('approved_audio_edits',[])
            def authorized(a,b):return any(e.get('source_start_sample')==a and e.get('source_end_sample')==b and e.get('approval') and e.get('reason') for e in approved)
            for segment in mapping:
                a=segment.get('output_start_sample');b=segment.get('output_end_sample')
                if not (integer(a) and integer(b) and 0<=a<b):errors.append('Invalid source-map output interval.');continue
                need(a==output_end,'Gap/overlap in output source map.');output_end=b
                if segment.get('kind')=='silence':need(bool(segment.get('reason')),'Explain intentional silence.');continue
                need(segment.get('kind')=='source','Unknown source-map kind.')
                sa=segment.get('source_start_sample');sb=segment.get('source_end_sample')
                if not (integer(sa) and integer(sb) and integer(count) and 0<=sa<sb<=count):errors.append('Invalid narration source interval.');continue
                need(b-a==sb-sa,'Narration speed changed in source map.')
                need(sa>=source_end,'Repeated/backward narrator samples require an explicit alternate edit plan.')
                if sa>source_end:need(authorized(source_end,sa),'Unapproved narration deletion in source map.')
                source_end=sb
            need(output_end==round(Fraction(duration*sr,fps)),'Narration map does not cover the output audio.')
            if integer(count) and source_end<count:need(authorized(source_end,count),'Unapproved unused narrator tail.')
    except (OSError,UnicodeError,json.JSONDecodeError,TypeError,AttributeError,KeyError,ValueError) as exc:errors.append('Malformed/incomplete project: '+str(exc))
    return {'ready':not errors,'errors':errors,'warnings':warnings,'scope':'Preproduction logic only; inspect actual media, content, assets and artistic quality separately.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');a=p.parse_args();report=validate(a.project);print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['ready'] else 2
if __name__=='__main__':sys.exit(main())
