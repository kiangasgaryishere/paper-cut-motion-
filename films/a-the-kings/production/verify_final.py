import json,subprocess,pathlib
p=pathlib.Path('films/a-the-kings/production');f=pathlib.Path('video/a-the-kings-v3.mp4')
r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
v=next(x for x in r['streams'] if x['codec_type']=='video');a=next(x for x in r['streams'] if x['codec_type']=='audio');d=float(r['format']['duration'])
assert (v['width'],v['height'])==(1080,1920)
assert v['r_frame_rate']=='30/1' and abs(d-72.744)<.1
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True,stderr=subprocess.PIPE)
# Verify delivered content, not only the encoder's file header.
bd=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','blackdetect=d=0.2:pix_th=0.04','-an','-f','null','-'],capture_output=True,text=True,check=True)
assert 'black_start:' not in bd.stderr
qc=dict(width=v['width'],height=v['height'],fps=v['r_frame_rate'],duration=d,video=v['codec_name'],audio=a['codec_name'],sample_rate=a['sample_rate'],full_decode='passed',black_frame_check='passed',caption_layout='28 speech-anchored cues checked; no bounds errors',music='none',speech_alignment='Whisper phrase timestamps + silence-edge refinement; continuous boundaries approximate; caption lead 22.58–52.92 ms',listening_review='not performed')
(p/'QC-v3.json').write_text(json.dumps(qc,indent=2));print(json.dumps(qc,indent=2))
subprocess.run(['ffmpeg','-v','error','-y','-ss','33.4','-i',str(f),'-frames:v','1',str(p/'poster-v3.jpg')],check=True)
