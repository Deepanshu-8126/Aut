# 🔊 SFX LIBRARY + SOUND DESIGN LAW — LOCKED (2026-10-24)
**User order: "top creators library se SFX lete hain, ek-ek cheez deeply detailed — kab kya aayega. Hum bhi."**
Files: `/home/user/explainer-pipeline/assets/sfx/` (20 Mixkit pro SFX, free license, 9.7 MB, PERMANENT — kabhi delete nahi)
Rule: **LIBRARY-FIRST.** Synth SFX (code-generated thud/whoosh) = sirf fallback jab library mein exact sound na ho.

---

## 📦 THE PACK (event → file)
| Event | File | Notes |
|---|---|---|
| Hook slam / braam | `mk788_big_impact.mp3` | trim first hit ~1.2s |
| Riser INTO stamp | `mk790_trailer_riser.mp3` | end riser exactly ON stamp frame |
| Stamp hit | `mk1143_whoosh_deep_impact.mp3` | layer under slam |
| Scene cut (normal) | `mk1492_whoosh_fast.mp3` | at cut −0.15s |
| Scene cut (big/act change) | `mk1486_tunnel_woosh.mp3` | hook→map, jump→polaroid |
| Small element move/pop | `mk1489_air_woosh.mp3` | pins, chips entering |
| Chip/data pop | `mk677_glass_hit.mp3` | first 0.4s, vol 0.5 |
| Polaroid/card slide | `mk1530_paper_slide.mp3` | card entrances |
| Map/doc turn | `mk1104_page_turn.mp3` | map card arrival |
| Sketch/paper drop | `mk2380_paper_quick.mp3` | evidence reveals |
| Polaroid reveal | `mk1430_camera_shutter.mp3` | photo "develop" moment |
| Typewriter text | `~~mk1125~~ (DEAD 404 Oct 28 — replacement dhoondhna)_typewriter_soft.mp3` | per-char beats (loop clicks) |
| Typewriter line done | `mk1368_typewriter_bell.mp3` | header complete ding |
| Tension clock | `mk1059_tick_tock.mp3` | countdown/decision beats, vol 0.3 |
| ABC heartbeat | `mk494_slow_heartbeat.mp3` | verdict section bed, vol 0.5 |
| Mystery transition | `mk492_mystery_heartbeat.mp3` | into final question |
| Reveal sub-hit | `mk685_suspense_bass.mp3` | big fact lands (use first hit) |
| Storm ambience | `mk2390_rain_thunder.mp3` | night/storm scenes, vol 0.25 |
| Soft rain bed | `mk2393_light_rain_loop.mp3` | hook ambience, vol 0.2 |
| Airplane flyby | `mk1590_airplane_rumble.mp3` | plane scenes, fade in/out, vol 0.35 |

## ⏱️ "KAB KYA BAJEGA" — TIMING LAW (Chronic Dossier reference map)
Har video banate waqt pehle SOUND MAP TABLE banao (scene × second × SFX), fir assemble:
1. **0.0s HOOK:** ambience bed start (rain/wind/location-true) + 0.5-0.7s pe BIG IMPACT on title slam
2. **Har scene cut:** whoosh (fast ya tunnel by weight) at cut −0.15s
3. **Har stamp:** riser 1.0-1.1s pehle start → stamp frame pe impact. Riser ka END stamp pe hi lage — ye non-negotiable
4. **Har card/photo entry:** paper slide ya page turn; photo reveal pe camera shutter
5. **Har chip/callout pop:** air woosh ya glass hit (vol 0.4-0.5, subtle)
6. **Typewriter headers:** soft clicks per char + bell on complete
7. **Action scene:** location-true ambience layer (plane=rumble, storm=thunder, sea=waves) vol 0.25-0.35 under music
8. **Verdict/ABC section:** slow heartbeat bed + hot-cycle pe tick-tock optional
9. **Ending loop:** mystery transition into final line
10. **MIX LAW:** VO king (full) > SFX hits 0.8-0.9 > ambience 0.2-0.35 > music bed 0.26. NO DOUBLE MUSIC. Target mean ≈ −19 dB, peak ≤ −1 dB
11. **DENSITY LAW:** koi bhi 3s window silent-flat nahi — kuch na kuch move/sound ho. Par 2 se zyada SFX ek saath kabhi nahi (mud ho jata hai)

## FUNCYOUS pe bhi same library use hogi (events: mechanism click, part pop, cutaway whoosh, etc.)
Download more: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3` | catalog scrape: curl -A "Mozilla/5.0" mixkit.co/free-sound-effects/<category>/

## 🔄 2026-10-25 UPDATE — HORROR ADDITIONS (SANNATA lane) + pack re-pull
(Sandbox reset ne purana pack uda diya tha — core re-downloaded. Current files in assets/sfx/:)
| Event | File |
|---|---|
| Horror ambience bed (82s, loop) | mk2482.mp3 |
| Graveyard wind layer | mk1157.mp3 |
| Horror deep drum heartbeat | mk559.mp3 |
| Horror impact (scream/lantern hits) | mk773.mp3 |
| Terror transition (scream layer) | mk2484.mp3 |
| Terror sweep of darkness (act change) | mk2630.mp3 |
| Horror swish (scene cuts) | mk1495.mp3 |
| Scary wooden door opening | mk190.mp3 |
| Knocking on thick wooden door | mk197.mp3 (P1/P3 "andar se awaaz" ke liye) |
| Man running in forest (chase) | mk1236.mp3 |
| Core re-pulled | mk788, mk790, mk1143, mk1489, mk685 |
SANNATA P2 SOUND MAP = reference template for horror shorts (see SANNATA_P2_METADATA.md / chat log 2026-10-25).

## ADDED 2026-10-25 (bomb-test v3 — cinematic bed upgrade)
| file | dur | use |
|---|---|---|
| mk2745.mp3 | 88.4s | ⭐ DARK DRONE bed (bass-heavy) — long-form chapter bed, lowpass 2400 + vol 0.42 |
| mk2741.mp3 | 70.6s | dark drone alt bed |
| mk1287.mp3 | 4.9s | ⭐ DEEP BRAAM — reveals/impacts; asetrate*0.78 + bass g=5 = stamp sub-layer |
| mk2636.mp3 | 1.0s | tight thud — callout ticks (trim 0.6s) |
RECIPE (locked v3): jet rumble = anoisesrc brown lowpass130 v0.5 + drone bed + braam @reveal + thud ticks @mentions + stamp = mk1495 + mk1287-pitched-down; master: highpass28 → acompressor 2.2:1 makeup4 → alimiter → peak ≤ -1dB.

## 2026-10-26 ADDED (downloaded, assets/sfx/)
| mk1372.mp3 | typewriter continuous typing 24.4s | chapter-card typing slices |
| mk1386.mp3 | typewriter typing B 26.4s | long record-card typing |
| mk1368.mp3 | typewriter bell 1.8s | header complete ding |
| ~~mk1125~~ (DEAD 404 Oct 28 — replacement dhoondhna).mp3 | single keypress 0.26s | lone key hit |

## 🔴 SYNTH SFX LAW (2026-10-26, learned the hard way)
1. ffmpeg bandpass/bandreject/equalizer `w=` DEFAULT IS Q-FACTOR, not Hz. ALWAYS write `width_type=h:w=<Hz>`.
2. Never mix inline lavfi synth chains blind. Pre-render to WAV with 2-pass auto-gain (target max -13dB), verify with volumedetect, THEN add as file input + adelay.
3. Band-isolation measurements also need width_type=h, warna numbers meaningless.
- Pen-sketch recipe: pink noise seed → bandpass f=2500-2900 width_type=h w=3400-3800 → tremolo f=10-13 d=0.85 → fades → 2-pass gain. Files: pen0/1/2.wav + whir.wav (vol .35).

---

# 🎪 TOON + MEME PACK (2026-10-26) — `assets/sfx/toon/`
**Kyun:** User verdict — generic Mixkit whoosh se NYT wala maza nahi aata. Ye pack = storytime-comedy vocabulary (NYT/Almost Real lane ke liye).

## FILES (21, sab ffprobe-verified)
| File | Dur | Beat kab use kare |
|---|---|---|
| meme_vine_boom.mp3 | 1.3s | 💥 PUNCHLINE LANDA / shock reveal / zoom-punch ke saath (NYT ka bread-butter) |
| meme_record_scratch.mp3 | 0.7s | ⏸️ "ruk ruk ruk" moment, freeze-frame, galat baat suni |
| meme_dun_dun_dun.mp3 | 5.1s | 😱 dramatic reveal (trim 1.5-2s), genre-flip horror beat |
| meme_bruh.mp3 | 0.9s | 😑 deadpan reaction, kisi ki bakwas pe |
| meme_slide_whistle_fail.mp3 | 3.8s | 📉 fail/nakami (trim), girne se pehle |
| meme_crickets_awkward.mp3 | 4.2s | 🦗 awkward silence, joke flop, koi jawab nahi |
| meme_sad_violin.mp3 | 4.6s | 😢 fake-sad moment, mock sympathy |
| meme_anime_wow.mp3 | 4.2s | ✨ sarcastic "wow" reveal (trim 1-1.5s) |
| desi_dhol.mp3 | 6.5s | 🥁 desi entry/celebration/band baaja beat (trim) |
| mk2894_boing_hit.mp3 | 1.3s | 🤸 bounce, takkar, cartoon hit |
| mk2151_soft_punch.mp3 | 0.5s | 👊 halka punch/thappad/nudge |
| mk2889_fast_splat.mp3 | 1.1s | 💩 splat, girna, kuch girana |
| mk391_falling_scream.mp3 | 3.9s | 🪂 lamba cartoon fall (trim) |
| mk395_falling_whistle.mp3 | 2.7s | 🎵 classic fall-whistle (Avantika-fall type beats) |
| mk746_dazzle_hit_birds.mp3 | 1.9s | 🐦 sar pe lagi + chakkar (dizzy birds) |
| mk473_fail_piano.mp3 | 2.4s | 🎹 comic fail sting |
| mk744_trombone_disappoint.mp3 | 2.7s | 📯 wah-wah-waah disappointment |
| mk2876_fail_low_tone.mp3 | 1.6s | ❌ chhota fail blip |
| mk2888_game_slide.mp3 | 1.1s | 🎮 quick slide/transition comedy |
| mk616_toy_whistle_spin.mp3 | 1.3s | 🌀 spin/scheme-sochna moment |
| mk2882_cartoon_laugh.mp3 | 2.1s | 😂 character giggle insert |

## 🎯 NYT-STYLE SOUND RULES (decode se)
1. **STING-PER-PUNCHLINE:** har joke land hone pe EK sound (vine boom / fail piano / bruh). Khali punchline = मरी हुई punchline.
2. **SOUND = JOKE bhi ho sakta hai** (NYT ka "ढंग ढंग ढंग" theme-song gag) — kabhi kabhi sound ko hi 2x repeat karke callback banao.
3. **SILENCE WEAPON:** punchline se pehle 0.3-0.5s pura silence → sting. Crickets = silence ka joke version.
4. **GENRE-FLIP AUDIO:** comedy→horror flip pe music band + dun_dun_dun + low drone (mk1287 braam old pack se).
5. **NO DOUBLE AUDIO LAYERS law** abhi bhi LAGU — ek beat pe ek sting, stack nahi.
6. Volume: stings 0.35-0.5, VO ke neeche nahi — VO gap MEIN rakhlo (sync-point cuts).

## ⚠️ LICENSE HONESTY
- **mk*.mp3 = Mixkit License** — free, commercial OK ✅
- **meme_*/desi_dhol = myinstants (user-uploaded meme sounds)** — license UNCLEAR. Ye sounds YouTube comedy mein industry-wide use hote hain aur SFX pe Content ID strike ka risk practically zero hai, par formally "cleared" nahi hain. Jahan possible ho Mixkit twin use karo (boing/fail/trombone ke Mixkit versions is pack mein hain). Vine boom jaise iconic memes ka koi Mixkit twin nahi — risk/reward user ka final call.

---

# 🎵 STORYTIME MUSIC BEDS (2026-10-26) — `assets/music/storytime/`
**YE WO ASLI SOUND HAI jo NYT-type videos me bajta hai** — Kevin MacLeod (incompetech.com), storytime-animation industry ka standard. 10 tracks, sab verified.

## BED → MOOD MAP
| Track | Dur | Kab bajao |
|---|---|---|
| km_monkeys_spinning_monkeys | 2:05 | 🐒 THE iconic storytime bed — default comedy narration |
| km_fluffing_a_duck | 1:07 | 🦆 cute/silly beats, bachpan memories |
| km_carefree | 3:25 | 😌 relaxed happy storytelling, flashback |
| km_sneaky_snitch | 2:16 | 🕵️ scheme/shaitani/chori — plan banate waqt |
| km_investigations | 1:33 | 🔍 sneaky lite, "kuch gadbad hai" |
| km_scheming_weasel_fast | 1:29 | 🏃 chase/panic/bhagam-bhag |
| km_run_amok | 1:47 | 🤪 chaos comedy, sab bigad gaya |
| km_show_must_be_go | 3:36 | 🎪 intro/outro/CTA block |
| km_darkest_child_horror | 3:58 | 👻 GENRE FLIP horror (A16/F2 ending) |
| km_night_of_chaos_horror | 3:30 | 😱 horror chase after flip |

## ⚖️ LICENSE (IMPORTANT)
**CC-BY 4.0/3.0 — FREE for YouTube monetized use, PAR ATTRIBUTION MANDATORY.**
Har video description me paste karo (jo tracks use hue):
```
Music: "<Track Name>" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0
https://creativecommons.org/licenses/by/4.0/
```
Ye line UPLOAD KIT template me bhi daalni hai jab ye beds use hon. Content ID safe (KM tracks whitelisted/dispute-proof with attribution).

## EXTRA FOLEY ADDED (`assets/sfx/toon/`)
| File | Use |
|---|---|
| toon_run_takeoff.mp3 (2.6s) | 🏃💨 bhaagne ka take-off zip (NYT chase staple) |
| meme_slap.mp3 (1.6s) | 👋 thappad/hit |
| ding_correct.mp3 (3.0s, trim) | ✅ sahi jawab/idea ding |
| buzzer_wrong.mp3 (1.1s) | ❌ galat jawab buzzer |
| toon_pop.mp3 (0.5s) | 💭 appear/disappear pop |

## 🎚️ MUSIC USAGE RULES (NYT pattern)
1. Bed ALWAYS low (vol 0.10-0.16), VO king.
2. **Bed SWITCH = scene mood switch** — ek video me 3-5 bed changes (narration→scheme→chase→horror). Ye unka secret pacing hathiyar hai.
3. Punchline pe bed DUCK ya CUT (0.3-0.5s silence) → sting → bed wapas.
4. Genre flip pe: comedy bed HARD CUT → 1s silence → horror bed fade-in.
5. Funcyous beds (#595/#464) aur Dadi bed (Mixkit #5) ki jagah ab Dadi/NYT lane ke liye YE pack default hai — Mixkit #5 backup.

## 🔒 FUNCYOUS MECHANISM SOUND MAP — LOCKED (2026-10-27, video 67 tap-to-pay)
User order: "background music best sfx viral". Ye ab HAR Funcyous short ka audio skeleton hai:
| Beat | Sound | Vol |
|---|---|---|
| Hook card slam (0.04s) | mk788 big impact (1.1s trim) | 0.48 |
| Bed act-1 | #595 @0.26 (EDIT ENERGY), duck 0.45 under VO | 0.26 |
| X-ray section cut | mk1486 tunnel woosh (act change) | 0.42 |
| Coil/mechanism complete | mk677 glass hit | 0.45 |
| Chip/part pulse | mk1489 air woosh | 0.35 |
| Normal section cuts | mk1492 whoosh fast, cut −0.15s | 0.36-0.40 |
| INTO payoff drop | mk790 riser, END exactly ON drop + bed hard dip 0.45s pehle (silence weapon) | 0.42 |
| PAYOFF hit | mk685 suspense bass + synth 55Hz sub boom | 0.52+0.42 |
| Bed act-2 (payoff se) | #464 @0.28 SLAM-in (0.06s) | 0.28 |
| Diegetic beat (payment beep/click) | synth terminal double-beep 1760Hz ×2 (library fallback law) | 0.34 |
| Subscribe tap press | mk677 soft | 0.30 |
| Loopback | mk1489 | 0.34 |
| Thumb-tail slam | mk788 (0.9s trim) | 0.42 |
Micro-fades 0.02s har SFX pe. Peak −1.2dB. VO king. NO DOUBLE LAYERS.
SFX re-pull (mixkit direct): assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3 — 788/790/1492/1486/677/685/1489.

## 2026-10-28 ADDED — ACTION PACK (rl04 "proper action match" order, @ROop_Loop)
| Event | File | Notes |
|---|---|---|
| Strong punch impact | mk2155.mp3 | pad slam layer + punch lead |
| Hard quick punch | mk2143.mp3 | impact stack crisp layer |
| Soft quick punch | mk2151.mp3 | pad plant / small props |
| GIANT MONSTER ROAR | mk1972.mp3 | Hulk roar (trim 2.3s) ⭐ |
| Electric shockwave | mk2599.mp3 | energy charge ignition (trim 2.2s) |
| Air whistle punch | mk2048.mp3 | dash/launch |
| Factory metal hard hit | mk2980.mp3 | body→rack crash |
| Falling empty can | mk389.mp3 | post-crash rattle (vol 0.22) |
| Boing hit | mk2894.mp3 | cartoon bonk |
| Hard pop click | mk2364.mp3 | caption pops |
| Footsteps tunnel loop | mk543.mp3 | onset-sliced single steps |
| Training punching bag | mk2113.mp3 | gym ambience (unused rl04, banked) |
ROop_Loop IMPACT STACK recipe: mk788 + mk2155 + mk2143 + mk1143 + mk1287 (0.9/0.9/0.65/0.75/0.65) after silence-weapon duck.

---
## 🌍 SOURCE ATLAS (Oct 28 training) — kahan se kya uthana hai
_Priority order: pehle apni downloaded library, phir Mixkit, phir neeche ke._

| # | Site | License/Attribution | Limit | Kab use karein |
|---|---|---|---|---|
| 1 | **Mixkit** (locked primary) | Free license, NO attribution, no signup | unlimited | Sab kuch pehle yahan — URL recipe: `assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3` (UA Mozilla/5.0) |
| 2 | **Pixabay SFX** pixabay.com/sound-effects | Pixabay License, NO attribution, no signup | unlimited | Mixkit mein na mile toh — 200k+ files, MP3 direct |
| 3 | **YouTube Audio Library** (Studio → Audio) | YT license, copyright-100%-safe | unlimited | Monetization-critical beds; Studio ke andar hi hai |
| 4 | **Freesound** freesound.org | CC0 filter lagao (CC-BY = credit zaroori) | account | Ajeeb/specific sounds (creature, machinery) — SIRF CC0 filter |
| 5 | **BBC Sound Archive** sound-effects.bbcrewind.co.uk | personal/research free; commercial = permission | — | Chronic archival authenticity (33k historic) — RESEARCH refs only, commercial careful |
| 6 | **SONNISS GDC bundles** | royalty-free, no attribution | bulk GB packs | Ek baar download, permanent pro pack (cinematic) |
| 7 | **ZapSplat** | free = ATTRIBUTION required | 10/day | Avoid — credit jhanjhat, sirf emergency |
| 8 | **Uppbeat** | free = ATTRIBUTION required | — | Avoid same reason |
| ⛔ | ElevenLabs SFX free | NON-commercial only | — | BANNED hamari videos ke liye |

**LAW:** attribution-wale source se liya toh description mein credit line MANDATORY (KM jaise). No-attribution sources (Mixkit/Pixabay/YT-AL/SONNISS/CC0) = clean, inhi ko prefer karo.

---
## 💎 PRO LIBRARIES — jo top creators ACTUALLY use karte hain (Oct 28 research)
| Library | Kaun use karta | Price | Note |
|---|---|---|---|
| **Epidemic Sound** | #1 — most YouTubers ka default (vlogs/MrBeast-style) | $13-49/mo | 40k tracks + 90k SFX; cancel = rights GONE (rental trap) |
| **Artlist** | filmmakers/cinematic channels | ~$199/yr | downloaded tracks FOREVER yours (lifetime license) |
| **Musicbed** | ad agencies, premium docs | $99-499/yr | sabse cinematic, overkill |
| **Soundstripe** | budget creators | mid | Epidemic ka alternative |

### 🧠 HAMARA FREE BRIDGE (quality gap kaise paatna hai — LAW)
1. **SONNISS GDC bundles = asli jugaad** — multi-GB PRO-recorded packs, royalty-free FOREVER, no attribution, free. Ye wahi studio-grade quality hai jo paid libraries bechti hain. (Ek baar download → permanent library, Kaggle dataset pe backup.)
2. **YT Audio Library** = Epidemic jitna hi monetization-safe, free (search kharab hai — mood/instrument filter use karo).
3. **Quality ka 70% TECHNIQUE hai, source nahi:** layering (riser+impact+whoosh stack), dB discipline, EQ (highpass 28, compressor, limiter), contact-frame sync — ye sab hamare paas already locked hai. Pro library wala bhi bina technique ke flat lagta hai.
4. **Agar kabhi revenue aaye** → pehla paid investment = Epidemic personal $13/mo (sab channels ka sound instantly upgrade). Tab tak: Mixkit+Pixabay+SONNISS+technique.


---
## ✅ LIBRARY REBUILT + VIRAL-CORE SETUP (Oct 28)
Over-cap snapshot ne assets/sfx uda diya tha — doc ke ids se FULL REBUILD: 49 files, 11MB (beds 96k compressed), `explainer-pipeline/assets/sfx/`. mk1125 ab 404 = DEAD.

### 🎯 VIRAL SHORTS CORE PALETTE (har channel ki pipeline mein yahi stack):
| Reveal-stack role | File | Use |
|---|---|---|
| RISER (build 2-3s) | mk790 | end EXACTLY on reveal frame |
| IMPACT (moment of truth) | mk788 (+mk1143 layer) | reveal/result/punch frame |
| WHOOSH (har cut) | mk1492 fast / mk1489 air | cut −0.15s, −18to−22dB |
| TEXT POP | mk677 / mk2364 | har text/chip pop, vol 0.4-0.5 |
| TICK (tension) | mk1059 / mk2636 | countdown/decision, vol 0.3 |
| SUB-HIT (fact lands) | mk685 / mk1287 braam | big reveal sub-layer |
| DRONE BED | mk2745 (96k) | lowpass 2400, vol 0.42 |
| GLITCH/CHAOS | montage cuts | (Mixkit glitch id TBD — Pixabay fallback) |
+ ACTION PACK (ROop_Loop): 1972 roar, 2155/2143/2151 punch, 2167 slap, 2599 elec, 2980 metal, 2894 boing, 2889 splat, 391 scream, 543 steps, 2113 bag, 395 fallw, 389 can, 2048 whistle, 2364 pop
+ Dadi toon pack: 2390/2393/1590/2482/1157/559/773/2484/2630/190/197/1236 + beds 494/492/1530/1104/1430/1368/2741/1486/1495/2380
