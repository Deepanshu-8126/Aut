# yt-automator

Topic series se script (Gemini), narration (voice API), Manim math scenes aur HyperFrames
animation ke saath YouTube videos banata hai. Hindi aur English ke liye alag voice aur alag playlist.

## Setup (pehli baar)
1. Repo par jaake **Settings → Secrets and variables → Actions** mein ye secrets daalo:
   - `GEMINI_API_KEY`
   - `VOICE_API_TOKEN`
   - `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (upload ke liye)
2. **Actions** tab → **Render video** → **Run workflow**.

## Local run
```
npm install
pip install manim edge-tts
python3 pipeline/run.py --series dsa --lang en --topic "Binary search"
```

## Status
- [x] Manim templates (halving, derivation, graph, tree)
- [x] HyperFrames composition + easing
- [ ] Voice adapter (Indic Parler-TTS / Chatterbox) — abhi Edge/Kokoro code hai
- [ ] Word-level timing se sync
- [ ] vdo components (ComparisonCard, TerminalSplit, CodeExplainer) port
- [ ] YouTube upload + playlists
