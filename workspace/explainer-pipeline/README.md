# Explainer Pipeline (`/home/user/explainer-pipeline`)

2.5D Hindi Science / Anatomy / History Facts Explainer Pipeline (`1080 × 1920`, 30 fps).

## Quick Commands

```bash
cd /home/user/explainer-pipeline

# 1. Storyboard stills + phone-size contact sheet (Mandatory Approval Gate)
bash make.sh scripts/ear-hearing.json --stills

# 2. Fast preview render (after approving stills)
bash make.sh scripts/ear-hearing.json --fast

# 3. Full 30fps render (with -14 LUFS audio mastering & ffprobe QA)
bash make.sh scripts/ear-hearing.json

# 4. Custom voice/speed or reuse existing VO
bash make.sh scripts/ear-hearing.json --voice hf_beta --speed 1.18
bash make.sh scripts/ear-hearing.json --no-tts
```

## Persistent Outputs (`renders/`)
Because workspace snapshots exclude `out/` and `.cache/`, all final deliverables are automatically saved to `renders/`:
- `renders/ear-hearing-stills-sheet.png` — 11-shot phone-size contact sheet
- `renders/ear-hearing.srt` — word-aligned Hindi SRT captions
- `renders/ear-hearing.mp4` — final `1080 × 1920` video with VO, ducked ambient bed, SFX, and synchronized callout labels
