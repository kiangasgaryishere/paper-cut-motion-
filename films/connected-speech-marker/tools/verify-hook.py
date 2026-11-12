from pathlib import Path
import subprocess,json,hashlib
from PIL import Image
P=Path(__file__).resolve().parents[1];R=P.parents[1];V=R/'video/connected-speech-real-footage-v2.mp4';OLD=R/'video/connected-speech-real-footage-v1.mp4'
def run(a):return subprocess.run(a,capture_output=True,check=True)
m=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(s for s in m['streams'] if s['codec_type']=='video');assert(v['width'],v['height'],v['nb_frames'],v['r_frame_rate'])==(1080,1920,'1449','24/1');assert float(m['format']['duration'])==60.375
assert not run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']).stderr
# Packet-identical AAC verifies there was no audio retiming/re-encode or mixing change.
def digest_audio(p):return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-']).stdout).hexdigest()
a,b=digest_audio(V),digest_audio(OLD);assert a==b
im=Image.open(P/'real-footage/opening-hook.png');assert im.mode=='RGBA' and im.getpixel((0,0))[3]==0
for t,label in [(0,'first-frame'),(.8,'intro'),(2.7,'first-screening'),(6.8,'captioned-replay')]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1',str(P/f'real-footage/v2-{label}.jpg')],check=True)
q={'version':'real-footage-v2','file':str(V.relative_to(R)),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'duration':60.375,'frame_count':1449,'width':1080,'height':1920,'fps':24,'hook_text':'این صحنه رو ببین','hook_interval_frames':[0,45],'hook_font_size':92,'full_decode':'passed','audio_packet_equality_with_v1':True,'aac_payload_sha256':a,'audio_checks':'Inherited from verified v1: unchanged AAC packets.','listening_review':'not performed; audio unchanged'}
(P/'real-footage/QC-v2.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q,ensure_ascii=False,indent=2))
