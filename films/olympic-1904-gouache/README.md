# 1904 Olympic marathon — 10-second gouache motion test

[Download the 10-second MP4](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-gouache-test-v1.mp4)

A separate project in the same repository. Portrait 1080×1920, 30 fps, three shots and two hard cuts. This is a condensed visual test from the supplied unfinished Persian marathon script, not the full script compressed into ten seconds.

| Time | Direction | Persian copy |
|---|---|---|
| 0–3 s | Elevated stadium view; gentle pullback; small painted running figures | کمدی‌ترین مسابقهٔ تاریخ المپیک! |
| 3–6 s | Closer lateral view of running figures; dusty track; starter sound | آمریکا، ۱۹۰۴؛ ۱۸ نفر نتونستن مسابقه رو تموم کنن! |
| 6–10 s | Félix introduced in a terracotta long-sleeved shirt and long trousers; slow push; distant runners | فلیکس کارواخال؛ دوندهٔ کوبایی، با همین لباس‌ها! |

The final clothing line previews a later beat from the script. There is **no narration**, because none was supplied for this test. Persian text, outdoor air, dirt footsteps and one brief starting crack; **no background music**. Do not treat the timing as voiceover alignment.

Opaque painted assets, coal/slate darks, golden light, olive fields and a terracotta hero take direction from Lemo-Opuscar's **Welsh Valley Gouache** reference, Opuscar98 entry 14. The warmer stadium environment adapts that landscape language to the 1904 race. This is a painterly illustration rather than an archival reconstruction or an exact likeness of Félix.

Motion is assembled in Canvas: four sprite columns provide staggered painted running poses; background camera transforms, airborne dust and subtle character motion continue between the cuts. The four generated columns contain similar alternate poses, so this is a deliberately limited run cycle, not fluid full character animation. The background and character paint texture moves with the artwork; no frame-random repainting is used.

Assets `stadium.png`, `felix.png` and `runners.png` were generated for this test with the image-generation tool. `Arabic.ttf` reuses the existing project font and its license under the repository's `licenses/`. Shared rendering utilities are from Lemo-Opuscar (MIT; repository credits retained).

Rebuild from the repository root after the existing setup:

```bash
bash films/olympic-1904-gouache/build.sh
```

No new runtime dependencies or API credentials are needed to rebuild the included assets. Intermediate WAVs, frames and render segments live in ignored folders.
