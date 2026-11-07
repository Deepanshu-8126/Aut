# `/home/user/skills` — Clean Modular Skill Architecture

Yeh folder saare video creation skills ko **5 clean categories** mein organize karta hai taaki har video bante waqt (`explainer-pipeline` aur `factshorts` dono mein) automatically inka use ho:

```text
/home/user/skills/
├── README.md                          # Master architecture & usage guide
├── run_skill.py                       # Unified CLI runner (used automatically inside make.sh & run.py)
│
├── 01-youtube/                        # YouTube Agent Skills (Jakeschincariol/youtube-agent-skill)
│   ├── yt-script/                     # hookscore.py + hooks.json + SKILL.md
│   ├── yt-package/                    # title.py (Title & Thumbnail check) + SKILL.md
│   ├── yt-edit/                       # deadair.py (SRT pacing & dead-air check) + SKILL.md
│   ├── yt-chapters/                   # chapters.py (Auto chapters from SRT) + SKILL.md
│   ├── yt-retention/                  # retention.py + SKILL.md
│   ├── yt-viral/                      # swipe.py + SKILL.md
│   ├── yt-shorts/                     # Shorts pacing & hook rules
│   ├── yt-seo/                        # Tags, metadata & description rules
│   ├── yt-plan/                       # Topic planning
│   ├── yt-comment/                    # Pinned comment strategy
│   └── yt-audit/                      # Pre-publish audit
│
├── 02-remotion/                       # Official Remotion Skills (remotion-dev/skills)
│   ├── remotion-best-practices/       # Official Remotion composition & timing rules
│   ├── remotion-captions/             # @remotion/captions word-level grouping & SRT rules
│   ├── remotion-render/               # Rendering & encoding rules
│   ├── remotion-multimedia/           # Audio/video stream rules
│   ├── template-tiktok/               # Official TikTok caption template reference
│   └── remotion-(create|docs|interactivity|maps|markup|saas|studio|upgrade)/
│
├── 03-motion-directing/               # Motion Directing, HyperMotion & MotionMaxxing
│   ├── motion_presets.json            # Live presets loaded directly by render_explainer.py
│   ├── motionmaxxing/SKILL.md         # 2.5D camera moves, causal path, -14 LUFS audio ducking
│   ├── hypermotion/SKILL.md           # Spring callout pops, optical flash cuts, kinetic captions
│   └── remotion-motion-graphics/SKILL.md # 1080x1920 safe margins (90px) & lower-third caption band
│
├── 04-voice-and-captions/             # Voice Synthesis & Word Alignment Repos
│   ├── kokoro/                        # hexgrad/kokoro model reference
│   ├── kokoro-onnx/                   # thewh1teagle/kokoro-onnx runtime (hf_beta Hindi VO)
│   ├── whisperX/                      # m-bain/whisperX word-level alignment reference
│   └── chatterbox/                    # resemble-ai/chatterbox voice cloning reference
│
├── 05-pipeline-guides/                # Production & QA Playbooks
│   ├── SCRIPT-PIPELINE.md
│   ├── VIDEO-PIPELINE.md
│   └── PIPELINE-LESSONS.md
│
└── 06-stock-media/                    # Real B-Roll Video, Historical Photos, No-Copyright Music & SFX
    ├── SKILL.md                       # Mixkit + Pexels + Wikimedia integration rules
    └── stock_fetcher.py               # Live scraper/fetcher cached in /home/user/.cache/stock/
```

---

## Kaise Use Hota Hai Video Bante Waqt (Automatic Integration)

1. **`explainer-pipeline/make.sh`** har run mein:
   - Step 1: `tools/align.py` (`04-voice-and-captions`: Kokoro `hf_beta` + word alignment + `.srt`)
   - Step 2: `/home/user/skills/run_skill.py audit` (`01-youtube` hook/title/deadair checks + `03-motion-directing` presets check → `renders/<slug>-skill-report.md`)
   - Step 3: `tools/render_explainer.py` (`03-motion-directing/motion_presets.json` se `motionmaxxing` + `hypermotion` + `remotion-motion-graphics` parameters load karke `1080×1920` render + `ffprobe` QA)

2. **`factshorts/run.py`** har run mein:
   - `01-youtube/yt-script/hookscore.py` aur `01-youtube/yt-package/title.py` chala kar `publish.md` banata hai aur `renders/<slug>/` mein persist karta hai.
