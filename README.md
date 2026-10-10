# yt-automator

Topic series se script (Gemini), narration (voice API), Manim math scenes aur HyperFrames
animation ke saath YouTube videos banata hai. Hindi aur English ke liye alag voice aur alag playlist.

## Setup (pehli baar)
1. Repo par jaake **Settings → Secrets and variables → Actions** mein ye secrets daalo:
   - `GEMINI_API_KEY`
   - `VOICE_API_TOKEN`
   - `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (upload ke liye)
2. **Actions** tab → **Render video** → **Run workflow**.

## Local run (Remotion lesson video, ek command)
```
cd remotion && npm install && cd ..        # pehli baar
pip install edge-tts soundfile numpy
python3 pipeline/build_video.py tests/lesson_python_lists.json --name lists_v5 --lang en --theme light-grid
```
Output: `output/remotion/lists_v5.mp4` + `output/audit/lists_v5/sheet.png`.
Render ~7 min (2 CPU). Browser ke liye Linux par `libnspr4` jaisi libs chahiye.

Gemini script ke liye system prompt: `prompts/gemini_teacher_prompt.md`.

## Status
- [x] Manim templates (halving, derivation, graph, tree)
- [x] HyperFrames composition + easing
- [ ] Voice adapter (Indic Parler-TTS / Chatterbox) — abhi Edge/Kokoro code hai
- [ ] Word-level timing se sync
- [ ] vdo components (ComparisonCard, TerminalSplit, CodeExplainer) port
- [ ] YouTube upload + playlists
