# Pipeline Lessons & Quality Gates (`PIPELINE-LESSONS.md`)

1. **Never Claim Fixed Without Reviewing Output:** Always inspect the generated contact sheet (`stills-sheet.png`) and run `ffprobe` on the final `.mp4`.
2. **Workspace Snapshot Exclusions:** `out/`, `.cache/`, `.venv/`, and `node_modules/` are excluded from workspace snapshots. Store heavy TTS/Whisper model caches in `/home/user/.cache/` (so the workspace never hits the 128 MB limit) and copy final `.mp4`, `.srt`, and contact-sheet deliverables into `renders/` so they persist.
3. **Authoritative Script Words Over Raw ASR:** Whisper can misspell Hindi words or output Urdu script on short clips; always align Whisper word timestamps back onto the authoritative Devanagari/Hinglish tokens from `scripts/<topic>.json`.
4. **Caption Safe Band:** Keep burned-in captions inside `x = 90..990, y = 1420..1580` so they never collide with focal diagrams or mobile platform UI.
5. **No Fake Numbers:** Every metric on screen must come from verified facts in `scripts/<topic>.md`.
