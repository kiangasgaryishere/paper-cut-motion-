# اصالت فرش | Comic History Cartoon
A 93-second vertical teaching Reel using the supplied script and uncut narrator recording. Version 2 renders thirty edge-to-edge vertical scenes with occasional full-bleed slides. The opener unrolls an articulated rug prop, lands a tag and cuts to a yarn detail. In the teaching section the same rug stays in view as the origin label flips. Replacement puppet heads and timed body poses give the vendor and weaver contrasting reactions. The timeline and Persian SRT live alongside the film source. The camera and foley play at 24 fps and the articulated paper puppets use stepped 12 fps poses. The caption is a cream card with dark Persian lettering, 288 pixels from the lower edge at 1080 × 1920.

Source style and technique: [Lemo Opuscar Comic History Cartoon](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/comic-history/STYLE.md). The paper puppet sheets and carpet illustrations were generated for this film. Rug designs are illustrative. Iran geometry is generalized modern [Natural Earth 1:110m](https://www.naturalearthdata.com/about/terms-of-use/) public-domain geography. The travel panel depicts an unspecified overseas workshop. Noto Sans Arabic is reused with its OFL from the previous project. Paper and fabric foley use [Wyzowl SFX Kit](https://github.com/wyzowl/sfx-kit), CC0. No music.

The original script and MP3 are retained. Persian captions translate the short English terms while the terms themselves appear on panel cards. Caption anchors use speech pauses, script and local bilingual transcription as evidence. They are phrase-level estimates.

Rebuild from the repo root with the installed Opuscar Python environment and browser:
```sh
P=films/carpet-comic-history
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/timing.py"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/key.py"
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node "$P/tools/preflight.mjs"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/mix.py"
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs "$P" --fps 24 --workers 3 --size 1080x1920 --out "$P/out/picture-v2.mp4"
bash "$P/tools/export.sh"
/workspace/lemo-opuscar/.venv/bin/python "$P/tools/verify.py"
```

The original framed cut is retained as `video/carpet-comic-history-v1.mp4`. The revised cut is `video/carpet-comic-history-v2.mp4`. See `review/v2-frames.jpg` for selected revision frames.
