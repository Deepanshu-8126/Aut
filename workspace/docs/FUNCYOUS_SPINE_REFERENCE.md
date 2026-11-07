# Funcyous spine / height Short — saved style reference

User's reference: https://youtube.com/shorts/V52x3gWCIic — “you wake up 2 cm taller every morning - here's why”. It is a reference for motion, storytelling and delivery; do not assume the user wants the same topic repeated.

## Evidence recovered on 2026-10-31
- YouTube page confirmed title, but web fetch did not provide playable video; exact live-video contents not independently compared.
- Private Kaggle `ukboy7u787/roop-v2-spine-test`: downloaded `ROOP_SPINE_TEST.mp4` to `/home/user/spine_reference/ROOP_SPINE_TEST.mp4`. SHA-256 `857356fb6e274dfc87e7319c2287fe7aac15ce56233f4895261212fde6c08bf2`; 25.73 sec, 30 fps, 1080×1920. Its exact equivalence to the live V3.4 upload has not been verified. Kaggle retains the file if local copy does not persist.
- Inspected 20 visual samples in `/home/user/spine_reference/reference_sheet.jpg` and read the project sources. This is not a full human visual watch or audio listen.
- Sources: `/home/user/outputs/roop-v2-test/test.html`, `render3.py`, `mix3.py`, `img/`, `ROOP_SPINE_TEST_V3.srt`, and `THUMB_SPINE.jpg`. These are project artifacts, not proven to be the precise final live-version recipe.

## What the recovered version shows
- Starts with a sleeping character and a strong short caption, then wakes/stretch pose changes; returns to the sleep scene for the loop.
- X-ray visualization in the sleeping body, a close disc comparison with water particles and a size marker, then standing character changing posture with downward arrows; astronaut contextual scene.
- Full-frame illustrated character scenes and recognizable silhouette, not a succession of text cards. Text is concise, high contrast and keyed to the spoken sequence; colored keywords provide emphasis. Match story to images.

## Technique evidenced in saved source
- The HTML canvas composites **separate image variants** with controlled alpha blends to suggest waking/stretching, disc shape change, posture, breathing and blinking. It also uses timed captions, particle flow, arrows, gentle movement, flash, vignette and a loop. This is not evidence of a fully rigged character or genuine 3D simulation.
- `render3.py` samples canvas time at a 1.08 multiplier and renders 772 frames; raw timeline values in `test.html` are not automatically the final video timestamps.
- `mix3.py` describes a voice track and explicitly timed SFX/bed. The exact voice in the uploaded Short remains unverified. Funcyous's current documented voice lock is `am_adam`, not a claim that this was the exact live voice.
- Avoid identity-changing, ghostly or anatomically inconsistent blends. Story-driven character motion and a visible mechanism are the reference; decorative zoom, glow and particles alone do not substitute. Read applicable current Funcyous/channel/sound/testing rules before a new build.
- The reference's quantitative and astronaut statements should not be copied as verified facts without fresh sourcing; no general claim that astronauts have no gravity.

## Testing and limits
- Machine motion/retention scores are proxies, not proof the result is engaging or viral. Check final captions, voice, music, effects and visual meaning through human eye/ear review where available. No claim of model retraining or a complete preserved exact V3.4 recipe.
