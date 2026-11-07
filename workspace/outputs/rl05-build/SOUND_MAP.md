# rl05 SOUND MAP — Hulk vs Godzilla (25.0s, NO VO, @ROop_Loop)
Times = engine code times (no VO → no silencedetect pass; impacts IMP1=10.5, IMP2=17.9 from rl05.html).
Braam mk1287 ALLOWED on @ROop_Loop (banned Chronic only). Bed = own sub-drone (677 BANNED here).

## BED (full 25s)
- sub-drone: sine 52Hz + brown noise lowpass 110, vol 0.16
- swells (vol→0.30): 2.6–4.0 (shadow creep), 16.0–17.6 (doom shadow)
- duck→0.05: 6.9–7.4 ("oh." comedy beat)
- HARD SILENCE (all layers, silence-weapon): 10.20–10.50, 17.60–17.90

## EVENTS
| t | sfx | treat | vol |
|---|-----|-------|-----|
| 0.00 | mk1287 braam | trim 2.2s | 0.75 |
| 1.45/1.80/2.15 | mk543 step slice (-ss0.30,0.28s) | — | 0.30 |
| 3.20 | mk1143 distant thud | pitch 0.75 | 0.35 |
| 4.10 | mk790 riser -ss0.92 | end ON 5.6 | 0.45 |
| 5.65 | mk1972 ROAR | pitch 0.84 (Godzilla) trim 2.2s | 0.85 |
| 7.05 | mk2364 tiny pop ("oh.") | — | 0.35 |
| 8.45 | mk1972 ROAR | normal pitch (Hulk) trim 1.5s | 0.55 |
| 8.80 | mk790 riser | end ON 10.0 | 0.40 |
| 10.10 | mk2143 whoosh (windup) | — | 0.45 |
| 10.20–10.50 | SILENCE WEAPON | | |
| 10.50 | IMPACT STACK mk788+mk2155+mk2143+mk1143+mk1287+mk2167 | 0.9/0.9/0.65/0.75/0.65/0.5 | |
| 10.56 | mk2894 boing (comedy BONK tail) | — | 0.50 |
| 11.25 | mk391 fall scream | trim 1.1s | 0.45 |
| 11.75 | mk2889 fast splat (flop) | — | 0.60 |
| 11.98 | mk2894 boing (bounce settle) | pitch 1.2 | 0.30 |
| 13.07 | mk677 pop (PLAN B star) | — | 0.45 |
| 13.12 | mk2364 pop (burger) | — | 0.55 |
| 14.25 | mk2143 whoosh | pitch 0.7 (giant lean) | 0.40 |
| 14.75/15.05 | mk2143 lowpass 900 (sniffs) | trim 0.35s | 0.20 |
| 16.30 | mk790 riser -ss0.92 | end ON 17.9 (doom) | 0.45 |
| 17.60–17.90 | SILENCE WEAPON | | |
| 17.90 | STOMP STACK mk788+mk2155+mk1143+mk1287 pitch 0.9 | 1.0/0.9/0.85/0.8 | |
| 17.90 | mk2889 SPLAT (burger squash) | — | 0.80 |
| 19.00 | mk1972 anguish | pitch 1.12 trim 1.6s | 0.50 |
| 21.40/22.05/22.70 | mk543 heavy step | pitch 0.6, fading 0.40→0.25 | |
| 23.50 | mk2143 whoosh (panel cut-in) | — | 0.45 |
| 23.85 | mk677 pop (ROUND 2?!) | — | 0.45 |
| 23.80 | mk790 riser -ss0.92 | runs to 25.0 → loops INTO 0.00 braam (seam mask) | 0.40 |

## MASTER
amix normalize=0 → highpass f=30 → acompressor 2:1 → alimiter 0.891 level=false → peak ≤ -1dB (volumedetect on FINAL mp4).
