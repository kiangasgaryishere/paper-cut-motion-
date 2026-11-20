from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1]
brief={'project':'rahnama-five-whiteboard','audience':'adult language learners considering classes','purpose':'explain five personalized Rahnama learning features; CTA comment برنامه','script_required':True,'script':'script.md','narration':'assets/narration.mp3','style':'Lemo Opuscar Whiteboard','style_url':'https://lemomo-ai.github.io/lemo-opuscar/styles/whiteboard/','mode':'complete production','involvement':'prior independent-production authorization persists','format':{'width':1080,'height':1920,'fps':24,'duration':76,'fps_reason':'native selected style / prior project cadence; explicit 24fps adaptation of skill 30fps default'},'music':False,'repository':'kiangasgaryishere/paper-cut-motion-','branch':'main','auto_commit_push':True,'font_fallback':'Noto Sans Arabic; authorized Morabba binary unavailable','official_logo_supplied':False}
(P/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n')
e=json.loads((P/'out/events.json').read_text())
(P/'timeline.json').write_text(json.dumps({'duration':76,'fps':24,'source_voice_duration':3604000/48000,'edits':[],'tail_hold':44000/48000,'caption_lead_seconds':.03,'captions_file':'captions.json','camera':e['camera'],'sound_events':e['events'],'implementation':'film.js is authoritative drawing geometry/deadlines; re-export using tools/check-film.mjs'},ensure_ascii=False,indent=2)+'\n')
(P/'REFERENCES.md').write_text('''# References and scope

Primary: https://lemomo-ai.github.io/lemo-opuscar/styles/whiteboard/ ; official source https://github.com/lemomo-ai/lemo-opuscar/tree/143f387ad774525dc9abc0ff05fb5f4bfbaa5f02/styles/whiteboard . Gallery retrieval was proxy-blocked; official raw STYLE.md matched local documentation byte-for-byte in setup/whiteboard-readiness. Adopted principles: one glossy board, real single-line strokes, floating pens without hands, camera riding routes, material-matched foley, eventual whole-board reveal. No demo characters, story, narration, music or sample branding reused.

Secondary: user-made Opuscar Short Video Director skill in this repository; grow-rahnama skill for brand constraints, adult learner focus, blue/coral palette, no invented logo/evidence. Explicit Whiteboard choice overrides general brand cut-paper/oil template. Supplied script supersedes older internal descriptions of services; film adds no performance guarantees, pricing or measured student results.

SFX Kit https://github.com/wyzowl/sfx-kit remains installed as a fallback reference. This film needs native felt/gloss, wipe and pin sounds; deterministic native Opuscar synthesis was selected instead of unrelated library sounds.
''')
(P/'DECISIONS.md').write_text('''# Decisions

- Full film is authorized by current request and prior production preference; no new style/material questions required.
- Complete user MP3 is time authority. Source script remains byte-identical. No sentence deletion, time stretch, replacement narration or music.
- Five stations on one board, rather than repeated title cards or generic teacher imagery. Motion is continuous and local; camera travels only between distinct ideas.
- Source phrase pauses guide captions. 30ms lead is intentional; 24fps makes display granularity 41.667ms. No word-level forced-alignment or perceptual listening claim.
- Persian caption translation of spoken “Learning Roadmap” is نقشهٔ راه یادگیری; the original English stays on the board. No Latin words inside subtitle box.
- Black writing; blue/coral diagrams and emphasis. One primary new element at a time. Existing words hold for reading.
- Morabba cannot be fetched via available skill binary access and is absent locally. Reuse actual joined Noto Sans Arabic and identify it honestly. No redistribution of proprietary font binaries.
- “رهنما” is an ordinary school-name mention, never an invented official logo. Conceptual figures are not real staff/student photographs or proof of outcomes.
- 24fps explicitly chosen for native Whiteboard motion and existing project cadence; portrait dimensions and caption-safe placement retained.
- No cover, Instagram caption or worksheet generated because user requested the video only.
- Preserve unrelated untracked cancelled Olympic v4 files and previous film versions; stage only this new project and its final MP4.
- Use CPU-backed Canvas2D for this 2D-only film to avoid software-GPU bottlenecks. Native geometry/material retained; cached surfaces are reused only while camera, ink, eraser and pen poses are completely static.
- Clamp subtitle tail padding against the next phrase onset, preventing adjacent-phrase overlap.
- Raise foreground writing after objective stem checks; locally limit effect transients instead of reducing the whole effects stem. Speech ducking remains active.
''')
(P/'CREDITS.md').write_text('''# Credits / rights

- User-supplied script.md and new class.mp3: retained as source materials under the user's production authorization. Narration file is assets/narration.mp3.
- Lemo Opuscar by Lemomo / LemoLab. Native Whiteboard stroke/board/pen/prop engine shared from setup/whiteboard-readiness/engine; upstream https://github.com/lemomo-ai/lemo-opuscar at143f387ad774525dc9abc0ff05fb5f4bfbaa5f02, MIT code; license at setup/whiteboard-readiness/licenses/Opuscar-MIT.txt. Portrait viewport adaptation already prepared in shared engine. New composition/story/camera/geometry in film.js.
- Native Whiteboard foley functions in tools/native-foley.py adapted from upstream styles/whiteboard/demo/mix.py, same upstream MIT. New event timing/voice processing in tools/mix.py. No demo score or demo narration.
- EMS Tech single-line font shared from setup/whiteboard-readiness/fonts/EMSTech.json, original font metadata/OFL retained in that file.
- Noto Sans Arabic shared from films/connected-speech-marker/fonts/Persian.ttf; license at films/connected-speech-marker/licenses/Persian-Noto-font-license.txt. Persian centerline glyph paths use user-project typography preparation, based on the upstream MIT skeleton algorithm. Small dot components preserved explicitly for legibility.
- General official style text remains at its source; only links and this project's original interpretation are committed. No copied reference poster.
- Rahnama name/colour guidance is user brand material. No official logo binary was supplied or recreated. No proprietary Morabba font copied.
''')
(P/'README.md').write_text('''# Rahnama five features — Whiteboard

Original 76s portrait Reel from supplied Persian script and narration. Output: ../../video/rahnama-five-whiteboard-v1.mp4. Production notes: TREATMENT.md, STORYBOARD.md, ART_DIRECTION.md, SOUND_PLAN.md. No music. Complete narration retained. Whiteboard source/style and font credits in CREDITS.md. Captions use actual Noto Sans Arabic fallback because Morabba binary was unavailable.

Rebuild from repository root (Node/Chromium/FFmpeg and Opuscar Python dependencies described in setup/):

```bash
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/prepare.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/rahnama-five-whiteboard/tools/check-film.mjs
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/mix.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs films/rahnama-five-whiteboard --fps 24 --workers 3 --size 1080x1920 --out films/rahnama-five-whiteboard/out/picture.mp4
ffmpeg -y -i films/rahnama-five-whiteboard/out/picture.mp4 -i films/rahnama-five-whiteboard/out/mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t 76 video/rahnama-five-whiteboard-v1.mp4
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/document.py
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/verify.py
```

Out/stills/WAV intermediate files are ignored; source MP3, timing, code and final MP4 are retained. Rebuild paths reflect this managed environment; use an equivalent Python with numpy, scipy, Pillow/RAQM and soundfile elsewhere. No external paid model/API required to render.
''')
print('Project memory updated')
