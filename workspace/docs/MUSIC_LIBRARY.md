# 🎵 MUSIC LIBRARY — dono channels (LOCKED source list)
Rule: har video ka mood pehle → phir track. Test: "kya track video ko MEHENGA feel karata hai?"

## SOURCES (sab FREE, no copyright, no attribution):
1. **YouTube Audio Library** — YT Studio → Audio Library tab (user khud bhi pick kar sakta hai)
2. **Mixkit** — https://mixkit.co/free-stock-music/ — direct download pattern:
   `curl -sL https://assets.mixkit.co/music/<id>/<id>.mp3`
3. Synth (Python) — sirf SFX/custom pulse ke liye, music ke liye nahi

## ✅ VERIFIED WORKING Mixkit IDs (tested in builds):
- **677 / 679 — "Epical Drums"** — epic percussion, action/reveal shots

## MOOD → MIXKIT CATEGORY MAP (build time pe is page se pick karo):
| Video mood | Mixkit category URL | Shortlist (Oct 2026 homepage) |
|---|---|---|
| Mystery/Chronic (UVB-76, D.B. Cooper, c06) | /free-stock-music/mood/mysterious/ | "Fright Night" = **id 871 ✅ CONFIRMED Oct 29** (`assets.mixkit.co/music/871/871.mp3`, used c06 @vol .16) ⭐, "Silent Descent" (piano+strings, melancholic) |
| Mechanism/Funcyous (curious groove) | /free-stock-music/mood/hypnotic/ | "Deep Urban" (tech house, hypnotic driving), "Tech House vibes" |
| Action/energy (drops, reveals) | /free-stock-music/cinematic/ | "Epical Drums" (677/679 ✅), "Driving Ambition" (uplifting brass) |
| Nostalgia/IG reels (dreamcore) | /free-stock-music/tag/lo-fi/ | song-clean.mp3 (already in outputs/ ✅), "Serene View" (chillout atmospheric) |
| Uplifting/motivational ending | /free-stock-music/mood/uplifting/ | "Driving Ambition", "Hip Hop 02" (relaxed positive) |

## BUILD-TIME SOP:
1. Video mood decide karo (script ke baad, render se PEHLE)
2. Is file ki shortlist se ya mood page fetch karke 2-3 candidates lo
3. Track page fetch → asset id nikalo → curl mp3 → 10-sec preview user ko (bade decisions pe)
4. Mix: continuous bed, VO ke neeche duck (-14 to -18 dB under VO), cuts pe swell
5. Kabhi bhi WhatsApp-compressed ya re-encoded music use nahi — hamesha fresh source MP3

## NOTES:
- Chronic c01 buzz v2 = synth SFX (station sound), uske UPAR ab music bed bhi add hoga (energy patch ke saath)
- IG reels: burned music sirf preview ke liye; final post pe IG native trending audio (reach boost)
- YT Shorts: music VIDEO MEIN burned (YT pe native audio add nahi hota shorts upload pe is flow mein)


## 🔊 SFX PACK (2026-10-24)
20 Mixkit SFX permanent at `explainer-pipeline/assets/sfx/` — full event map + timing law: `docs/SFX_LIBRARY.md`. Library-first, synth fallback.

## #538 — Funcyous dark pulse bed (LOCKED default, used in video 62). URL: assets.mixkit.co/music/538/538.mp3

## 🕵️ ZACK D. FILMS BGM FORMULA — RESEARCHED 2026-10-26 (user order)
**Uska style = "SNEAKY CURIOSITY":** pizzicato/plucked strings + marimba/vibraphone + tiptoe
mystery vibe. NO heavy EDM, NO drums-forward. Music LOW under VO (bed only). Source = Epidemic
Sound (PAID). Signature tracks: "Hide and Sneak"/"Lurking Behind" (The Fly Guy Five),
"Living in a Fantasy" (Pulsed — 50+ shorts me), "Mystical Tension" (Dream Cave),
"Pumping Veins" (Max Anson, marimba), "Hangover Weekend" (vibraphone+pizzicato),
"Pizzicato Comedy" (Rafael Krux). History topics = medieval tracks. Ref: zackdfilms.fandom.com wiki.

### FREE EQUIVALENTS (downloaded, Kevin MacLeod / incompetech, CC-BY):
| File (/var/tmp/assets/music/) | Vibe | Use |
|---|---|---|
| Sneaky_Snitch.mp3 | THE classic sneaky pizzicato (internet-famous) | Funcyous body/quirky mechanisms |
| Scheming_Weasel_faster.mp3 | faster sneaky, comedic tension | fast-paced reveals |
| Investigations.mp3 | pizzicato + mystery pulse | Funcyous secret-reveal sections |
| Spy_Glass.mp3 | noir sneaky jazz-ish | hidden-money / casino topics |
⚠️ CC-BY LAW: description me credit line MANDATORY:
"Music: Kevin MacLeod (incompetech.com), Licensed under CC BY 4.0"
⚠️ Famous tracks = meme-association risk (Sneaky Snitch bahut jagah baja hai) — A/B test vs 538.
Backup free lane: Mixkit mood/quirky + mood/mysterious (scrape method proven).

## 🔒 FUNCYOUS MUSIC LANE — USER LOCKED 2026-10-26 (A/B/C rounds 1-3)
WINNERS (user verdict "e and f sahi hey"):
- **#595 "Secret Garden"** (Film Score) — SNEAKY/REVEAL sections (secret, buried wire, hidden system beats). assets.mixkit.co/music/595/595.mp3
- **#464 "Sci-Fi Score"** (Electronic) — TECH/X-RAY sections (cutaway, mechanism, lock events). assets.mixkit.co/music/464/464.mp3
USAGE LAW (video 65 onward): in-video split allowed — hook/X-ray = 464, secret/payoff = 595 (crossfade at section cut, Wow-style bed swap) YA single-track full video, jo pacing maange. Vol 0.20-0.22, afade in/out, -ss offset rotate per video (no same-slice repeat).
REJECTED in testing: Sneaky Snitch (too cartoon vs dark visuals), Investigations (user: dark/uneasy), Spy Glass (close but no), 538 dark pulse = RETIRED as default (backup only).
Zack formula insight applied: 2 signature tracks ROTATE = channel sound identity (wo bhi 4-5 tracks ghumata hai).
