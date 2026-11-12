# Sources and attribution

| Material | Source / license / use |
|---|---|
| Script and original mommy.mp3 | Supplied by the user for this film; script.md and assets/narration.mp3 remain unedited. Existing English dialogue is part of the supplied audio. No demo voice is extracted or reused. |
| Marker style documentation | Lemo-Opuscar by Lemomo (LemoLab), https://github.com/lemomo-ai/lemo-opuscar/tree/3a7132b996be0241c1ea0ab180d519f06e6f10b6/styles/marker-paper ; current docs are CC BY-NC 4.0 with additional permission for making commercial/client films and project delivery. Source docs/poster are studied locally; links and independent project analysis are retained here. |
| Marker pen / ink-density / paper renderer | `styles/marker-paper/demo/pen.js`, source commit above; MIT, see licenses/Lemo-Opuscar-MIT.txt. Adapted dimensions from landscape to portrait and import to local core-utils.js. |
| Glyph skeleton tool | `styles/marker-paper/demo/tools/skeleton.py`, same source commit; MIT. Upstream algorithm retained; local wrapper selects Kalam fonts/characters for this film. |
| Core math utilities | Lemo-Opuscar core/lib.js from existing local library commit 143f387ad774525dc9abc0ff05fb5f4bfbaa5f02; MIT. Local copy avoids assuming this project's core/lib.js exists. |
| English typography | Kalam Bold / Regular, https://github.com/google/fonts/tree/main/ofl/kalam ; SIL Open Font License, licenses/Kalam-OFL.txt. |
| Persian typography | Noto Sans Arabic, reused from this repository's existing self-hosted font; Noto license retained in licenses/Persian-Noto-font-license.txt. Persian script glyph coverage checked; no missing Persian glyphs in supplied script. |
| Sound references | Marker native mix.py (MIT) for felt/paper algorithms; SFX Kit by Wyzowl, https://github.com/wyzowl/sfx-kit (CC0) for available fallback marker/paper assets. No new final sound assets/mix rendered at this review stage. |

Reference poster belongs to the upstream demo, CC BY 4.0, not an original frame of this film. It stays local for analysis. All review/styleframe PNGs here are original project compositions rendered with the marker engine. The user's film has no upstream demo sign-off or watermark.
