# 🔒 MODE SHUNYA v2 — PERMANENT LOCK (2026-10-22)
**User approved after 10+ tests. Ye document hi kanoon hai. Ek-ek cheez yahan likhi hai — kaise ghumta hai, kya code, kya params. Isse hatke kuch kiya = galti.**

- **Category:** HISTORY niche → sub-category "SHUNYA" (mythology/philosophy vivid reels, 45–60s, 1080x1920 @ 30fps)
- **Reference master:** `outputs/42-sudarshan-reel-50s.mp4` + `.srt` (51.00s)
- **Locked renderer:** `explainer-pipeline/tools/render_reel50.py` (base engine import: `render_shunya38.py`)
- **Channel:** CHRONIC OF HISTORIC (logo uploads mein) · tag neeche-left `CHRONIC OF HISTORIC` (alpha 60) + neeche-right `AI ART` (alpha 118), font MONO

---

## 1) ART (stills)
- Vivid comic / graphic-novel style, **poore reel mein EK hi style**, 768x1376 (9:16), JPG q92
- Har scene ka apna bespoke art — template copy-paste BANNED
- **Approved reel ke andar art kabhi REPLACE nahi** — sirf motion/edit se refine (user ka order: "isi mein edit kar")
- Naya art sirf naye topic ke naye reel pe

## 2) TIMELINE MATH (42 ka locked pattern)
1. VO lines pehle banao (voice-06, **Devanagari-only text**), har ek ki duration measure karo
2. Scene dur = vo_dur + ~0.9–1.3s saans; vo_start = scene_start + 0.4–0.5s
3. Crossfade **XF=0.5s** har cut pe; fade-in 0.2s / fade-out 0.8s; total 45–60s
4. 42 ka table (start,end,vo_start,vo_dur): s1 0–5.10/0.50+3.70 · s2 5.10–12.00/5.50+5.78 · s3 12.00–18.70/12.40+5.62 · s4 18.70–25.80/19.10+5.98 · s5 25.80–32.40/26.20+5.57 · s6 32.40–37.60/32.80+4.06 · s7 37.60–44.50/38.00+5.74 · s8 44.50–51.00/45.00+3.05

## 3) MOTION — 4-ENGINE HYBRID (sabse important section)
**A=LTX (soft, first choice) · B=sprite-bind (rigid) · C=swirl (vortex) · D=flap-warp (soft ka CODE fallback)**
**Rule: cheez ki PRAKRITI dekho, phir engine chuno.**

### Engine A — LTX img2vid (soft/living: pankh, kapda, dhuaan, paani, aag)
- HF Space `Lightricks/ltx-video-distilled`, gradio_client, endpoint `/image_to_video`
- Params: `input_image_filepath=handle_file(art)`, `height_ui/width_ui=1152x640`, `mode="image-to-video"`, `duration_ui=5–7`, `ui_guidance_scale=1`, `improve_texture_flag=True`
- Quota sach: anon ~2 min GPU/day (IP-based, reset 24h) · free account ~3.5–5 min · Kaggle 30h/wk = asli unlimited
- Clip ko frames mein extract karo (scale/crop/unsharp locked recipe), renderer frame-dir se uthata hai
- **LTX clips /var/tmp mein marte hain reset pe** — final mp4 hi unki motion ka permanent ghar hai. Re-render chahiye toh final mp4 se segment frames wapas nikalo (42 mein aise hi s1+s2 bache the)

### Engine B — Rigid sprite rotation (chakra, wheel, koi bhi GOL thos cheez)
- Object ka **alag sprite** banao (wheel_faceon.jpg jaisa), use ghumao — background ka patch kabhi mat ghumao
- **Elliptical-disc rule: PEHLE rotate, PHIR squash** — `xw()`:
```python
def xw(img,ang,scale):
    r=img.rotate(ang,resample=Image.BILINEAR)          # sub-pixel smooth
    w2=int(0.50*W*scale); r=r.resize((w2,int(w2*0.55)),Image.BILINEAR)  # squash 0.55
    return r.rotate(-14,expand=True,resample=Image.BILINEAR)            # tilt -14°
```
- 42 params: wheel 34°/s scale 1.09 · flame rings F1 −95°/s alpha 0.85, F2 +70°/s alpha 0.7, scale 1.16, flicker `m.flick(t,5.1,8.3,sp)` · glow = sprite ka GaussianBlur(22) alpha 0.8 peeche
- Flame sprite recipe (locked): polar k=[7,13,19,29,37] ^2.2×band^1.5 α210 blur3

### Engine B ka MATH-BIND (ghost ka permanent ilaaj)
Sprite ko background ke painted object pe LOCK karna zaroori hai warna zoom pe painted disc jhaankta hai (42 mein yahi bug tha):
1. Jis z (`zc`) pe position calibrate ki thi, usse **art-fraction** nikalo: `u=(fx+(zc-1)/2)/zc`, `v=(fy+(zc-1)/2)/zc` (fx,fy = frame-fraction e.g. 0.53, 0.30)
2. Har frame pe sprite center: `cx=round((u*w0-left)*S)`, `cy=round((v*h0-top)*S)` aur sprite scale ko `sf=z/zc` se multiply
3. Is scene pe **drift=0** rakho (42: s4)
→ Ab zoom karo ya pan, sprite painted object se chipka rahega. Ghost **mathematically impossible**.

### Engine C — Differential swirl (galaxy, bhanwar, toofan — koi bhi NON-SYMMETRIC ghoomne wali cheez)
**Rigid rotpatch yahan BANNED** (test-proof: galaxy 186° ghoomi → planet neeche, kala gaddha, circle seam — user ne pakda). Sahi physics: **center tez, kinara zero** — real galaxy jaisi differential rotation, seam ban hi nahi sakta:
```python
def swirl(fr,cx,cy,CR,t,Adeg,T):
    # cache: R(radius), F=falloff (1-r^2)^2 (kinare pe 0), TH=angle grid
    g=np.arange(-CR,CR); X,Y=np.meshgrid(g,g); R=np.sqrt(X*X+Y*Y)/CR
    F=np.clip(1-R*R,0,1)**2; TH=np.arctan2(Y,X); RAD=R*CR
    win=np.asarray(fr.crop((cx-CR,cy-CR,cx+CR,cy+CR)).convert("RGB"),np.float32)
    A=math.radians(Adeg)
    p1=(t/T)%1.0; w1=1-abs(2*p1-1)        # FLOW-MAP: 2 layers, weights sum=1
    for pp,wgt in ((p1,w1),(((p1+0.5)%1.0),1-w1)):
        an=TH-((pp-0.5)*A)*F               # bounded warp ±A/2, par motion endless
        # bilinear sample: sx=RAD*cos(an)+CR, sy=RAD*sin(an)+CR → 4-tap lerp
    # paste with soft ellipse mask blur 6
```
- **Kyun flow-map:** ek layer ka warp badhta jata hai, jab wo reset hota hai uska weight 0 hota hai → koi pop nahi, motion hamesha aage. Apparent speed = A/T.
- **Locked params:** storm/bhanwar `A=85° T=2.6s` (≈33°/s churn) · galaxy `A=60° T=3.8s` (≈16°/s)
- **Center art mein grid-overlay se pinpoint karo** (42: storm-eye 0.490,0.458 · galaxy-core 0.635,0.315), phir har frame map: `cx=round((u*w0-left)*S)` — camera ke saath track
- CR itna rakho ki nazuk cheez (ungli, chehra) falloff ke bahar rahe (42: storm 0.12W, galaxy 0.13W)

### Engine D — FLAP-WARP (CODE fallback jab LTX available nahi — LOCKED 2026-10-22, proof: outputs/43-garuda-codewings-test.mp4)
**Rule: soft/living cheez (pankh/kapda/dupatta) pe PEHLE LTX try karo. Quota khatam / offline → Engine D. Quality ~80-90%, par unlimited + free + repeatable.**
Code: `tools/test_codewings.py` (isko copy karo). Formula:
1. **Art-space displacement field (precompute once):** har wing/kapde ke liye `add_wing(patch, root, tip, dir, A, phase)`:
   - `s = clip(((P-root)·axis)/L, 0,1)^1.7` → root pe 0, tip pe max
   - edge window: smoothstep borders 14% patch ka → **kinaro pe ZERO = seam impossible**
   - traveling wave: `PH = 2.4*s + phase0` (lehar root→tip chalti hai)
2. **Real wingbeat (ye hi "real vibe" deta hai):**
   - asymmetric stroke: `osc = sin(θ) + 0.28*sin(2θ+0.6)`, θ=2π·0.85t−PH (downstroke tez, upstroke dheemi — pure sine BANNED, robotic lagta hai)
   - tip feather flutter: `+0.16*TIP*sin(2π·2.6t−2PH)` jahan TIP = clip((WMASK−0.45)/0.55)
   - **body bob (sabse zaroori):** camera dyf mein `+3.5*sin(2π·0.85t+π)` — flap ka lift-reaction
   - wing light pulse: `out *= 1+0.05*WMASK*sin(2π·0.85t−1.0)` — 3D shading illusion
3. **TRAINED PARAMS (LTX optical-flow se seekhe, 2026-10-22 — "LTX teacher method"):**
   - **Flap freq 0.27Hz** (har ~3.7s majestic flap — 0.85Hz phadphadahat BANNED; bada parinda SOAR karta hai)
   - bada wing A=26px · chhota wing A=18px (phase+0.9) · dupatta A=6px (phase+1.7) · tip-flutter 1.9Hz ×0.12
   - **Badal zinda rakho:** paas ke badal warp A=20px horizontal-lehar + 3× `m._tpatch` turbulence (fr~0.12, ax 5-6, fq 0.08-0.09) · door ke badal A=1.2px (parallax!)
   - body bob 5px @ 0.27Hz antiphase
   - **LTX-TEACHER METHOD (reusable training recipe):** final video se LTX segment nikalo → `cv2.calcOpticalFlowFarneback` (incremental loop, kabhi stack mat karo = OOM) → measure: dominant freq (zone flow FFT), zone amplitude map, vert:horiz ratio → wahi numbers Engine D mein daalo. Har naye LTX clip se seekh ke MOTION BANK banta jayega.
   - **Honest ceiling:** flow-metric LTX se 1:1 match NAHI hoga (LTX har feather ki texture alag regenerate karta hai; coherent warp wahan tak nahi jaata — zyada amplitude = rubber). Target: wing-tip flow ~0.3-0.5 @540w, visual sweep saaf dikhe, art intact.
4. **NO-TOUCH zones:** chehra/aankh/body patch ke BAHAR rakho (grid-overlay se regions pinpoint karo, jaise swirl centers)
5. Bilinear remap (sub-pixel) + warp ART-space mein karo, phir affine camera upar

## 4) CAMERA — SUB-PIXEL AFFINE ONLY (smoothness ka raaz)
**Integer crop BANNED** (test-proof: 1px steps = micro-judder; chakra bilinear tha isliye makkhan tha — user ne difference pakda):
```python
pe=pr*pr*(3-2*pr)                          # smoothstep ease — har zoom pe
z=z0+(z1-z0)*pe; S=max(W/w0,H/h0)*z        # sab FLOAT
dxf=7.0*math.sin(t*0.6+phh); dyf=5.0*math.sin(t*0.83+phh*1.7)   # organic drift (sprite-bind scene pe 0)
left=(w0-W/S)/2+dxf/S; top=(h0-H/S)/2+dyf/S   # float, clamp [0, w0-W/S]
fr=art.transform((W,H),Image.AFFINE,(1/S,0,left,0,1/S,top),resample=Image.BILINEAR)
```
- ZR zoom table (42): s3 push-in (1.06→1.17) · s4 sprite-track (1.045→1.105) · s5 pull-out reveal (1.16→1.06) · s6 push (1.05→1.12) · s7 push+pan-up 55px (1.04→1.11) · s8 halka (1.04→1.06)
- **Smoothness metric:** raw render pe consecutive-diff std/mean **< 0.05** (42 = 0.037)

## 5) LIFE LAYERS (har scene mein kam se kam 2)
- **God-rays:** 4 tilted polygons blur(42), alpha 58 → animate: `a=amp*(0.55+0.45*sin(t*0.45))`, x-shift `26*sin(t*0.22)` (s3 amp 0.75, s5 amp 1.0)
- **Embers (s3):** 12 points, upar uthte `(t*0.055*es)%0.32`, sway `0.014*sin(t*1.7)`, warm (255,190,110), twinkle sin²
- **Jugnu/fireflies (s5):** 16 points, alpha `190*(0.15+0.85*max(0,sin(t*1.1s+ph))**3)`, dheere drift
- **Diya flicker (s3):** brightness `1+0.035*sin(9.1t)+0.022*sin(23.7t)` clamp [0.96,1.06] — **smooth sines ONLY**
- **Lightning (s6):** `fl=1+0.55*max(0,sin(7.3t)*sin(3.1t)-0.58)` → continuous ramp, hard cut BANNED
- **Glow pulses:** `glow_sprite(r)`, alpha `0.60+0.40*sin(2π·0.4t+1.1)`; s8 pe crescendo ×(1+0.5pr)
- **Global (har frame):** smoke scroll (5% alpha, 14px/s x, 5px/s y) + gold particles (PART: rise+sway+twinkle) + vignette + **grain ±3** (rng seed=frame index)
- **STATIC HOLD BANNED** — har scene mein element-level + camera-level dono motion

## 6) TYPOGRAPHY — WORD-POP (unka font-grammar)
- 3 tiers: **0** = Tiro Devanagari small white (stroke 3, LH 80) · **1** = Teko-Bold bada YELLOW (stroke 7, LH 160) · **2** = Teko-Med (stroke 5, LH 126); yellow sirf power-words pe
- Timing **char-weighted**: `t_word = vs + vd*len(word)/total_chars` cumulative — VO ke saath word-sync
- Shadow sirf tier>0: offset (+5,+6) black 160 · y=0.555H default
- **s8/CTA exception: y=0.775H** (card ke neeche) — caption-card overlap BANNED (test mein pakda tha)
- Title (s1): TITLE font + GaussianBlur(14) halo ×2, scale-settle 1.045→1.0 in 0.9s, sub-title PAPER 235

## 7) CTA BLOCK (s8, locked sequence)
1. Mandala art + **orbiting light-glints** (2 glints, r=0.165W ellipse 0.95, speed 0.9 rad/s, phases 0/π, alpha pulse) — **mandala khud ghumana BANNED** (petals smear — test-proof, lotus ghost bana tha)
2. Card: papercut-style, slide-in 45.2s ease-out-cubic `1-(1-e)^3` drop 500px, SHAD offset +14
3. SUBSCRIBE pill: (226,56,38), pulse `1+0.03*sin(3.2t)`, center y=0.575H
4. Caption y=0.775H · glow crescendo · last 0.8s fade-out

## 8) AUDIO (locked recipe, change BANNED)
- VO: voice-06, Devanagari text hi do (Latin = kharab uchchaaran)
- Bed: `assets/ram36/music_bed.mp3` offset 60s se, **flat gain = 0.105/rms**
- Ducking: `bed *= 1 - 0.38*min(env*3, 1)` (env = VO envelope smooth)
- VO fades 0.1s in / 2.6s out tail · master: `tanh(x*1.1)` → normalize 0.97
- `.srt` hamesha export (scene VO lines, vo_start→vo_start+vo_dur)

## 9) RENDER + MUX (locked)
- Frames: JPG q87, `/var/tmp/reel50/frames/%05d.jpg`, **skip-if-exists** (resumable; renderer change ke baad affected range `rm` karo — range math: scene [a,b) + prev-tail b+0.5s)
- Render via `start_process` + `wait_for` (1530fr ≈ 3.5min)
- Mux: `-framerate 30 -i frames -i audio -vf "eq=contrast=1.05:saturation=1.14,unsharp=5:5:0.35:3:3:0" -c:v libx264 -preset veryfast -threads 2 -crf 26 -pix_fmt yuv420p -movflags +faststart`
- FF path: `/var/tmp/pydeps/imageio_ffmpeg/.../ffmpeg-linux-x86_64-v7.0.2` · reset ke baad: pip target reinstall + `cp fonts → /var/tmp/fonts/tiro.ttf`

## 10) QC GATES (order mein, skip BANNED)
1. **Probe-sheet** sab scenes ka 1-1 frame → positions check (galat center = abhi fix, render ke baad nahi)
2. Sprite-bind scenes: zoom ke **dono extremes** pe probe (ghost check)
3. Swirl scenes: full-res crop probe (seam/smear check) + 0.3s-apart delta > 8
4. Full render → **POST-MUX QC:** duration exact · scene-motion (fps=2 diff) sab ≥ ~7 (hero LTX 12+) · dead-air ZERO · smoothness: 30fps 1s window har scene uniformity < 0.25 (pulse-heavy CTA chhod ke)
5. User ke flagged timestamp = full-res frame nikaal ke dekh ke hi "fixed" bolo

## 11) BANNED LIST (10+ testo ka khoon-paseena — repeat mat karna)
| # | BANNED | Kyun (test-proof) |
|---|---|---|
| 1 | Rigid rotpatch non-symmetric content pe | galaxy 186° → planet displaced, kala gaddha (0:39 bug) |
| 2 | Integer-pixel camera crop | 1px steps = judder; affine float hi smooth |
| 3 | Mandala/ornate art ka rotation | petals seam-smear, lotus ghost (0:47 bug) |
| 4 | Background zoom + fixed unbound sprite | painted disc jhaankta hai (0:22 bug) — math-bind karo |
| 5 | Caption 0.555H CTA card ke saath | overlap (जुड़े card ke peeche dab gaya) |
| 6 | Approved reel mein naya art generate | user order: "isi mein edit kar" |
| 7 | Static image holds | "ANIMATION HI MAIN CHEEZ HAI" |
| 8 | Stepped/judder motion, hard flash cuts | smooth continuous only |
| 9 | Code se soft-cheez animation (pankh/kapda) | dead lagta hai — LTX use karo |
| 10 | Rigid patch >~11° (ghoomna ho toh) | seams — sprite ya swirl engine |
| 11 | `_flame` alpha < 0.7 | invisible |
| 12 | Fixed-coord FX camera-move scene pe | positions toot-te hain — art-fraction map karo |
| 13 | Latin text TTS / "human voice" dawa | Devanagari-only · hamesha bolo AI voice hai |
| 14 | Comparison videos, movie promotion | user orders |

## 12) NAYA REEL BANANE KA ORDER (steps)
1. Script: hook → 6 beats → CTA (tagdi script, no "case khula hai" ending)
2. VO record (voice-06) → durations → timeline table lock
3. Art: har beat ka bespoke vivid still (768x1376) + grid-overlay se motion-centers note karo
4. Motion-plan har scene: LTX / sprite-bind / swirl + life-layers chuno (hybrid rule)
5. LTX hero shots pehle daag do (quota hai toh) → frames extract
6. Renderer ko 42 se copy karo, SC/ZR/WPS/centers bhar do
7. QC gate 1–3 (probe) → render → mux → QC gate 4 → tab present
