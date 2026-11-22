# اصالت فرش | Comic History Cartoon
A 93-second vertical teaching Reel using the supplied script and uncut narrator recording. Version 2 renders thirty edge-to-edge vertical scenes with occasional full-bleed slides. The opener unrolls an articulated rug prop, lands a tag and cuts to a yarn detail. In the teaching section the same rug stays in view as the origin label flips. Replacement puppet heads and timed body poses give the vendor and weaver contrasting reactions. The timeline and Persian SRT live alongside the film source. The camera and foley play at 24 fps and the articulated paper puppets use stepped 12 fps poses. The caption is a cream card with dark Persian lettering, 288 pixels from the lower edge at 1080 × 1920.

Source style and technique: [Lemo Opuscar Comic History Cartoon](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/comic-history/STYLE.md). The paper puppet sheets and carpet illustrations were generated for this film. Rug designs are illustrative. Iran geometry is generalized modern [Natural Earth 1:110m](https://www.naturalearthdata.com/about/terms-of-use/) public-domain geography. The travel panel depicts an unspecified overseas workshop. Noto Sans Arabic is reused with its OFL from the previous project. Paper and fabric foley use [Wyzowl SFX Kit](https://github.com/wyzowl/sfx-kit), CC0. Versions 1–4 use effects only.

The original script and MP3 are retained. Persian captions translate the short English terms while the terms themselves appear on panel cards. Caption anchors use speech pauses, script and local bilingual transcription as evidence. They are phrase-level estimates.

Rebuild from the repo root with the installed Opuscar Python environment and browser:
```sh
P=films/carpet-comic-history
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/timing.py"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/key.py"
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node "$P/tools/preflight.mjs"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/mix.py"
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs "$P" --fps 24 --workers 3 --size 1080x1920 --out "$P/out/picture-v4.mp4"
bash "$P/tools/export-v5.sh"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/verify.py"
```

The original framed cut is retained as `video/carpet-comic-history-v1.mp4`. The revised cut is `video/carpet-comic-history-v2.mp4`. See `review/v2-frames.jpg` for selected revision frames.

Version 3 retains the magnified knot only in the hook (approximately 4.8–6.8s). A weaving shuttle passes through the warp and pulls the red weft at 10.8s, with a different composition for the overseas workshop at 54.32s. A beater comb compacts three rows at 23.6s. The pattern chart unfolds at 74.62s, and the tools reappear together at 83.37s. Four new keyed heads depict focus, delight, sheepishness and thoughtfulness. The new sprites are derived from an original generated sheet matched to the existing cast. The narration and caption timeline match v2. See `review/v3-frames.jpg` for the revised compositions.

Version 4 adds a close view of the bazaar trade ledger around 15.7s and a parcel landing beside the Tabriz design around 52.7s. The vendor crosses the market with a brisk walk, and the weaver walks more cautiously while carrying the parcel. Both walks animate separate thigh and shin pivots and use individually timed footfalls. Each character uses four faces across the film, including their neutral expression. The new prop sprites come from an original generated sheet. See `review/v4-frames.jpg`.

Version 5 uses the v4 picture stream and adds four SFX Kit cues. A coin drops on the ledger at 16.11s, a ding introduces Origin at 42.31s, a soft whoosh leads into the page transition at 47.89s and a soft impact follows the parcel landing at 53.37s. The original score is synthesized by `tools/score.py` using hammered and plucked string timbres inspired by santur and bağlama and a gentle hand-drum pulse. Its level and speech-band energy drop under the narrator. The music contains no samples from commercial recordings. The score and final mix render to `out/`. For an audio-only rebuild, run the mixer, `export-v5.sh` and verifier against the tracked v4 MP4. The export copies the video stream directly.
