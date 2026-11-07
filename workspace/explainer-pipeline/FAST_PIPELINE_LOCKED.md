# ⚡ FAST PIPELINE — ONE-SHOT RULES (LOCKED 2026-10-22)
*User directive: "ek baari mein video banke ready" — single order → final MP4 presented. Baar-baar puchna NAHI.*

## ONE-SHOT FLOW (order milte hi, bina ruke)
```
USER: "short bana [topic]"  (ya "Connect bhai")
  ↓ sab automatic, koi beech ka sawal nahi:
1. Script + shot list (7-part formula / reel format jo applicable ho)
2. VO generate (voice-06, Devanagari) — chunks PARALLEL
3. Stills generate (jahan chahiye) — hero stills pehle
4. GPU jobs push (run_factory.py) ─────────┐ PARALLEL
5. Code-engine shots render (start_process)┤ (GPU render hote waqt
6. Stock B-roll fetch (Pexels/Mixkit)      │  yahan edit chalti hai)
7. Audio bed + SFX mix                 ────┘
8. GPU clips download → timeline assembly → mux → QC → present_file
```
**Sirf 2 jagah user input:** topic dete waqt + final approve. Bas.

## PARALLEL RULES (sab proven, skills saved)
| Trick | Detail |
|---|---|
| **GPU ∥ local** | GPU jobs push karke LOCAL kaam turant shuru — GPU time overlap hota hai, add nahi |
| **Dual-T4 split** | worker.py `SPLIT=2` → aadhe jobs GPU0, aadhe GPU1 = **2× speed** (chhote models; RAM dekh ke) |
| **Batch jobs** | Ek kernel run mein SAARE shots ka jobs.json — per-job kernel push nahi (startup overhead × 1) |
| **Resume-skip** | Worker existing .mp4 skip karta hai — crash pe dubara push = sirf bache jobs |
| **TTS parallel** | VO chunks sentence-split karke parallel generate |
| **Frames resumable** | JPEG frames /var/tmp pe; renderer crash = wahi se resume |
| **Mux standard** | `-preset veryfast -threads 2 -crf 26` + eq/unsharp (LOCKED recipe) |
| **start_process** | Lambi renders background mein; poll nahi, wait_for log |

## SPEED BUDGET (1 integrated short ~60s)
```
Script+VO+stills:        ~45 min   ┐
GPU hero shots (2-3):    ~30-60 min│ overlap
Code shots + stock:      ~30 min   ┘
Assembly+mux+QC:         ~30 min
────────────────────────────────
TOTAL: ~2-3 ghante, EK HI BAITHAK, EK HI ORDER
```

## QUALITY GATES (one-shot ke andar bhi, skip NAHI)
- Frame inspection se render verify (claim se pehle)
- QC: duration + motion smoothness + tile check
- .srt export + AI RECREATION tag (photoreal) + locked style rules
- Ek hi baar present — final, approved-format mein

## INFRA STATE
- Kaggle: `ukboy7u787`, token `~/.kaggle/access_token` (permanent), 2×T4 verified
- Worker: `kaggle_ltx/worker/worker.py` (Wan 2.2 5B, SPLIT mode) | Driver: `kaggle_ltx/run_factory.py`
- Sandbox reset recovery (mera kaam, ~2 min): pip pydeps reinstall + kaggle CLI + tiro.ttf copy

## ⭐ ENGINE WINNER (2026-10-22 16:05 UTC): LTX-2.5 22B DISTILLED on Kaggle T4x2
- Kernel: ukboy7u787/factory-ltx-2-5-22b-distilled (worker5/ = community recipe unlockbulk/ltx-2-5-22b-distilled-video-generator, UI stripped, factory-jobs batch driver appended)
- STOPWATCH (proven): **152 s/clip** (5s, 512x896, 121f@24fps, 8-step, i2v) + 169s model load + ~10min setup/40GB download. Whole 2-clip kernel = 14 min.
- OUTPUT = VIDEO + 48kHz STEREO AUDIO (vocoder) — H3-class quality, no collapse. Test clips: outputs/49-ltx25-test-vanar.mp4 + -stone.mp4.
- Capacity: 30 GPU-h/wk ≈ 300+ clips/week → THIS is the unlimited daily engine. Wan 5B = premium long-form only. SkyReels+LTX-2B = REJECTED (slow-offload / quality collapse).
- Weights: DeepBeepMeep/LTX-2 (public, no token), INT8 convrot, MODELS_DIR=/kaggle/tmp.
- LESSONS: (1) kernel clones Wan2GP into /kaggle/working → output has 1000s of files → `kaggle kernels output` CLI chokes + API 429s. FIX NEXT VERSION: clone into /kaggle/tmp. Fetch selectively: python KaggleApi.kernels_output(file_pattern=r".*\.mp4$", page_size=500), retry on 429 with 60-90s backoff.
- H3 free Space (bonus hero shots): hugging-apps/minimax-h3-flashgen-4step /generate api, canvas '640x1152 · 9:16', ~45s/clip, video+audio; anon = 1 run/IP/day; HF token → 3-5/day.

## SHOT-DISTANCE RULE (user-verified, 2026-10-22, video 50)
- LTX-2.5 22B @ 512x896: WIDE / establishing shots = believable, close-ups = artifacts risk.
- Prompt framing MUST specify: "wide shot", "aerial view", "distant view" for hero clips.
- Avoid: face close-ups, hand close-ups, readable text in frame.
- AI RECREATION tag: REMOVED from videos per user order 2026-10-22 (YouTube synthetic-content checkbox at upload covers disclosure). tag_ai() stays in code but is not called.

## ENHANCE STEP — STANDARD (user order 2026-10-22, "real enhanced type")
- ON-DEMAND ONLY (user correction 2026-10-22): enhance SIRF jab user bole ("enhance kar"). Default ship = raw clips, fast. Recipe ready rehti hai, 1 command pe chal jaati hai.
- Recipe: worker8 pattern (kaggle_ltx/worker8/) — raw clips as dataset -> kernel: inline RRDBNet (basicsr key-compatible, no basicsr pip needed), weights github xinntao/Real-ESRGAN v0.1.0 RealESRGAN_x4plus.pth, fp16, 2 threads = 1 clip-queue per T4, OOM fallback = split-half tiling.
- Per frame: x4 upscale -> PIL LANCZOS down to 1080x1920 -> jpg q95 -> encode CRF16 + audio copy from raw clip.
- PROVEN: 481 frames (4x 5s clips) = 754s kernel total (~6 min/clip, dono GPU parallel). ZERO fails.
- Assembly unchanged — bas SRC ko enh/outputs pe point karo (enh_ prefix).
- 4K export skip: YouTube Shorts 1080x1920 hi serve karta hai; enhanced-1080p = "real enhanced" look.
- H3-on-Kaggle PASSED 2026-10-22: worker6 v2 (PIL fix), 210s/clip 480x832 24fps + audio, INT8 dual-T4. Dono engine live: LTX-2.5 (fast/bigger) + H3 (motion king).

## INPUT-STILL QUALITY RULE (user-locked 2026-10-22)
- i2v output quality = input still quality. Engine detail ko amplify karta hai, create nahi.
- MANDATORY: stills hamesha max-detail generate karo (768x1376+, "ultra detailed photoreal"),
  fir LANCZOS downscale karke engine res do (480x832 H3 / 512x896 LTX) = supersampling, extra crisp.
- Kabhi bhi soft/low-res image seedha engine mein mat do.
- Optional boost: still ko Real-ESRGAN se pehle enhance karo agar source soft hai (worker8 pattern, single image = seconds).
