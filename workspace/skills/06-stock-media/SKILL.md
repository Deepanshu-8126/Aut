# Stock Media & Real Assets Skill (`06-stock-media/SKILL.md`)

## Purpose
Automatically fetches real, royalty-free B-roll videos, historical/scientific photos, no-copyright background music, and sound effects directly inside the sandbox for **Hindi (`hi`)**, **English (`en`)**, or **Hinglish** Facts, History, and Story (`Kahani`) videos.

## Connected Providers (`stock_fetcher.py`)
1. **Mixkit Free Stock Video (`https://mixkit.co/free-stock-video/<query>/`):**
   - Keyless HD `.mp4` B-roll clips scraped directly from Mixkit CDN (`assets.mixkit.co/videos/...`).
2. **Pexels Video/Photo API (`PEXELS_API_KEY`):**
   - Uses `PEXELS_API_KEY` when present; automatically falls back to Mixkit + Wikimedia Commons when keyless.
3. **Wikimedia Commons (`commons.wikimedia.org/w/api.php`):**
   - Keyless real historical photographs, maps, monuments, portraits, and scientific images (`gsrnamespace=6`).
4. **Mixkit No-Copyright Music (`https://mixkit.co/free-stock-music/tag/<mood>/`):**
   - Keyless `.mp3` background tracks (`cinematic`, `mystery`, `ambient`, `dramatic`, `chill`) mixed at `-14 LUFS` with automatic voiceover ducking.
5. **Mixkit Sound Effects (`https://mixkit.co/free-sound-effects/<effect>/`):**
   - Keyless `.mp3` transition whooshes, clicks, and cinematic hits synced to shot cuts and `at: "word:..."` callout labels.

## Snapshot-Safe Caching
All downloaded media is stored in `/home/user/.cache/stock/{videos,images,music,sfx}/` so the workspace snapshot never exceeds the 128 MB cap.

## Script Schema Fields (`scripts/<topic>.json`)
```json
{
  "slug": "ancient-nalanda-history",
  "language": "hi",
  "voice": "hf_beta",
  "music_mood": "cinematic",
  "sfx_pack": "mixkit",
  "shots": [
    {
      "id": 1,
      "stage": "HOOK",
      "broll_query": "fire flames night",
      "wiki_query": "Nalanda University ruins",
      "vo": "...",
      "labels": [{"text": "9 MILLION BOOKS", "at": "word:90"}]
    }
  ]
}
```
