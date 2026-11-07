# 🎬 HUMAN EDIT LAYER — "AI na lage, real editor ka kaam lage"
_Har channel pe lagta hai: Funcyous / Chronic / SANNATA-Dadi / ROop_Loop. Yeh VIRAL_CHECKLIST_MASTER.md ka partner doc hai._

## ⚠️ PEHLE POLICY KI SACHAI (2026)
- Jul 2025: YouTube ne "repetitious" → **"inauthentic content"** policy banayi; Jul 16 2026 clarification: 3 cheezein DEMONETIZE hoti hain:
  1. **Generic template mass-production** (same outline, minimal variation, scale pe repeat)
  2. Off-putting/distressing content
  3. **AI personas** health/finance/legal/medical topics pe
- Jan 2026: 16 AI-slop channels TERMINATE hue (4.7B views, $10M/yr revenue gaya).
- **AI use karna offense NAHI hai** — policy bolti hai "significantly original and authentic" chahiye. Human editorial input ka SABOOT chahiye.
- May 2026 se: YouTube **auto-AI-detection** — photorealistic AI pe khud label laga dega. Stylized/cartoon animation ko toggle ki zaroorat bhi nahi, lekin hum honesty law se toggle ON rakhte hain.

### ✅ HAMARI POSITION STRONG HAI — kyunki:
- Animation **hand-coded engine** se hai (canvas code = literal human editorial work, template nahi)
- Har video ka structure alag (13-beat vs dossier vs battle rounds)
- Original research (Chronic facts, mechanism X-rays) — prompt se replicate nahi hota
- **DANGER sirf ek:** ek hi template bar-bar visible ho jana. FIX: har video mein kam se kam 2 naye visual devices (niche section).

---

## 🔍 10 AI-TELLS → HAR EK KA FIX (code mein implementable)

### 1. ⛔ TELL: Robot motion — constant-speed zoom/pan, perfectly smooth
**Human editor:** snappy ease curves, beat pe PUNCH, haath ka wobble.
**FIX (engine):** ✅ already partial (zoom-punch/whip-smear vocab). ADD: **handheld drift** har scene pe — `x += 2*sin(t*1.3)+1.5*sin(t*2.7); y += 2*sin(t*1.7+1)` (2-3px, slow). Zoom hamesha eased (outExpo/outBack), kabhi linear nahi.

### 2. ⛔ TELL: Metronome cuts — har shot same length
**Human editor:** shot lengths vary (0.9s / 2.8s / 1.4s), cut ACTION/SFX pe girta hai.
**FIX:** TL design mein scene durations kabhi equal nahi (rl01 ✅: 2.0/3.3/2.7/2.8/3.2...). Cut exactly SFX hit pe align karo (bell ke saath scene change).

### 3. ⛔ TELL: Text fade-in, center-everything, default look
**Human editor:** pop-in with overshoot, tilt, thick stroke+shadow, word-by-word.
**FIX:** ✅ already law (pop+wobble bigText, 3-word captions). ADD: kabhi-kabhi text ko 2-3° tilt + position vary (har banner same jagah nahi).

### 4. ⛔ TELL: Har scene ek full AI image = slideshow feel
**Human editor:** ek scene ke andar MULTIPLE "camera angles."
**FIX (BADA WALA):** ek hi image se **crop-coverage** banao — wide → punch-in close-up (face crop) → detail crop (burger crop) — 3 "shots" ek image se. Yeh instantly multi-camera shoot jaisa lagta hai. AI hands/edges close-up mein mat dikhana.

### 5. ⛔ TELL: TTS flat, no breaths, perfect diction
**Human editor:** pauses, emphasis, energy shifts.
**FIX:** ✅ VOICE LAW (silenceremove+atempo+gap-cap). ADD: script mein punctuation se emphasis engineer karo; ya rl01-style **NO VO** (music+SFX meme format = sabse human-feel, zero TTS tell).

### 6. ⛔ TELL: Music bed flat constant volume start se end tak
**Human editor:** music DUCKS under SFX/VO, volume automation, drops pe swell.
**FIX:** sidechain feel — SFX hit ke time bed -4dB dip (ffmpeg: volume automation ya duck segments). Ending pe fade/cut on beat.

### 7. ⛔ TELL: Joke ke baad turant cut — no reaction beat
**Human editor:** punchline → 0.4s reaction hold (face) → cut.
**FIX:** payoff ke baad micro push-in on face (static hold nahi — slow zoom 1.0→1.06) + crowd_laugh. rl01 S7 SPLAT ✅ yahi karta hai.

### 8. ⛔ TELL: Clean sterile frames — no editor "junk"
**Human editor:** emoji overlays 🔥😂, white flash frames on impact, shake, speed-lines, vignettes.
**FIX:** ✅ partial (flash/shake helpers). ADD: impact pe 1-frame white flash + 4-frame shake COMBO; emoji stickers jahan comedy beat ho.

### 9. ⛔ TELL: AI over-saturation + har scene same lighting mood
**Human editor:** graded look, scene-to-scene mood shift.
**FIX:** ✅ grade law (eq+unsharp). ADD: scene-wise tint variation (fire scene warm overlay, winner scene cool+bright) — canvas mein 5% color overlay per scene.

### 10. ⛔ TELL: Same template har video — HUD same jagah, same fonts, same beats
**Policy risk BHI yahi hai (inauthentic = template mass-production).**
**FIX LAW:** har nayi video mein **kam se kam 2 naye visual devices** (naya transition / naya gag format / naya camera trick) + structure vary. Signature elements rakho (brand), skeleton mat repeat karo (slop).

---

## 📋 QUICK PRE-UPLOAD "HUMAN TEST" (AI-judge ke saath)
1. Muted dekh ke pucho: "koi editor isko timeline pe kaat raha tha?" — cuts action pe hain ya random?
2. Koi 3-sec clip utha ke dekho: motion mein ease/wobble hai ya robot-linear?
3. Ek scene = ek still image jaisa lag raha hai? → crop-coverage daalo.
4. Music ko alag suno: kahin bhi duck/swell hai ya flat line?
5. Pichli video ke saath side-by-side: structure SAME dikh raha hai? → device badlo.

**LAW: naya engine = tells #1, #4, #6 pehle fix (sabse zyada AI-feel yahi dete hain).**
