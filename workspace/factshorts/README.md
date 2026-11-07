# FACTSHORTS — White-Box Shorts Pipeline (Python)

A complete, runnable Python pipeline that turns **one line of topic text** into a locked-style
**7-part vertical Short (1080×1920 PNG stills + animated MP4 with SFX)**.

Style: *White Minimal Box* — pure white canvas, dot grid, black top pill, Inter Black headline,
yellow annotation boxes, black PART bar, Vox-style pop/typewriter/count-up animation.

```bash
python run.py doctor --deep                   # which free provider stage is alive right now
python run.py demo --full                     # 7 PNGs + 7 MP4s + FULL-short.mp4 with SFX
python run.py video  --topic "How Suez Canal Was Built" --episode 45 --category "WORLD FACTS"
python run.py bridge --port 8077              # local UI: free AI / paste any chatbot reply
python run.py fill --script out/<run>/script.json    # re-generate placeholder parts only
python run.py scaffold --topic "…"            # write script.json + a paste-into-chatbot prompt
python run.py video --script out/<run>/script.json --only 5   # re-render just one part
```

Output lands in `out/<topic-slug>/`:

```
script.json                 the generated 7-part content pack
prompts/MASTER_AGENT_PROMPT.md   system prompt for Antigravity / Veo / any external agent
prompts/ui_spec.json             style tokens (identical to what the renderer draws)
prompts/animation_spec.json      timing tokens
prompts/image_prompts.md         one image prompt per part
part-1-hook.png … part-7-payoff.png   1080×1920 final stills
part-1-hook.mp4 … part-7-payoff.mp4   animated parts with SFX
FULL-short.mp4                        all 7 concatenated (~30s Short)
```

## Why this design

| Concern | How it is solved here |
|---|---|
| **"Get high-quality scripts for free, automatically"** | Done properly — see *How the free brain works* below. Driving LM Arena / Meta AI / ChatGPT *web UIs* with a bot is deliberately **not** done: it breaks their terms and dies on the next UI change. Instead: a free key-less API chain **+** the bridge (your browser, one paste) **+** a free-key slot **+** a placeholder-repair loop. |
| **Style drifting between parts** | One `style.py` token file feeds the renderer **and** the prompt factory → the MP4 and any external agent produce the same look. |
| **Text cutoff** | `textutil.autofit()` shrinks the title to fit 3 lines inside the safe area; captions are clamped to the canvas; the bottom bar is untouchable. |
| **No API keys available** | `vectorart.py` draws the brain / eye / chip / moon / shield / map illustrations in pure PIL maths, and the SFX bed is synthesised procedurally. Zero cost, zero latency, offline. |
| **Missing AI art is fine** | `art.py` order: local file → AI provider (if a token exists) → vector engine. A slide is never shipped empty. |

## How the free brain works (`FREE_KEYS.md` has the long version)

| Stage | What it is | Fails how | Handled by |
|---|---|---|---|
| 1 | `POST text.pollinations.ai/openai` — free, key-less, GPT-OSS 20B | HTTP 402 bursts | retry + model rotation → stage 2 |
| 2 | `GET text.pollinations.ai/<prompt>?model=openai-fast` | 402 bursts | model rotation → stage 3 |
| 3 | any OpenAI-compatible key (Gemini / Groq / OpenRouter / Ollama) | only if absent | used when present |
| 4 | 7 **small** chunked requests instead of one big one | never (each part padded) | `_src` marks what is real |
| 5 | `run.py bridge` — copy prompt → free chat site → paste reply | never | validates, repairs JSON, renders |
| 6 | offline template | never | ships a valid Short anyway |

Two reliability details that matter in practice:

* **Cache is bypassed on retries.** A cached bad reply must never be replayed as if it were a new
  attempt (that bug is fixed: `use_cache=(a == 0)` in `spec._one_part`).
* **Every part records its origin.** `script.json` keeps `_src: "llm" | "template"`, and
  `run.py fill` re-asks only the template ones — so a burst-limited hour costs you one command,
  not a re-run.

## Providers (all optional)

| Env var | Effect |
|---|---|
| *(none)* | `pollinations` free text API for the script + offline vector art. Default. |
| `POLLINATIONS_TOKEN` or `HF_TOKEN` | switches `FACTSHORTS_ART=auto` to AI illustrations (Pollinations FLUX). Then `python run.py demo --full`. |
| `OPENAI_API_KEY` + `OPENAI_BASE_URL` | any OpenAI-compatible text/image API — OpenAI, Groq, OpenRouter, Gemini-compat, local Ollama. |
| `FACTSHORTS_TEXT_PROVIDER` / `FACTSHORTS_IMAGE_PROVIDER` | `pollinations` \| `openai` \| `groq` \| `openrouter` \| `ollama` \| `gemini` |
| `FACTSHORTS_ART` | `vector` (default when no token) \| `ai` \| `auto` |
| `GEMINI_API_KEY` / `GROQ_API_KEY` / `OPENROUTER_API_KEY` | free API keys — auto-detected, see `FREE_KEYS.md` |
| `FACTSHORTS_NOCACHE=1` | ignore the disk cache in `assets/cache/` |
| `FACTSHORTS_CHUNK_DELAY` / `FACTSHORTS_CHUNK_BACKOFF` | pacing for the free tier (seconds) |
| `FFMPEG_BIN` | use a system ffmpeg instead of the bundled `imageio-ffmpeg` binary |

Bring your own art: drop a transparent PNG into `assets/illustrations/<key>.png`
(keys: `brain_hero`, `brain_glow`, `brain_flat`, `brain_dark`, `brain_cut`, `eye`,
`clock_brain`, `chip`, `sleep`, `shield_brain`, `world_map`, `suez`) and it is used as-is.

## Layout

```
factshorts/
├── run.py                     CLI (doctor / stills / video / demo)
├── config/
│   ├── style.json             human-editable mirror of the style tokens
│   ├── animation.json         human-editable mirror of the timing tokens
│   └── topics.json            topic backlog
├── src/factshorts/
│   ├── style.py               design tokens (colours, type scale, geometry)
│   ├── textutil.py            measure / wrap / autofit / typewriter draw
│   ├── providers.py           free & BYO-key text+image providers (no scraping)
│   ├── vectorart.py           offline illustration engine (brain, eye, icons…)
│   ├── art.py                 asset resolution: file → AI → vector
│   ├── renderer.py            composition + animation timeline
│   ├── video.py               frame rendering, ffmpeg encode, concat, SFX synthesis
│   ├── spec.py                topic → 7-part pack (chunked LLM + JSON repair + stale tracking)
│   ├── bridge.py              local web UI: free AI or paste-back → validate → render
│   └── prompts.py             prompt factory for external agents
├── assets/
│   ├── fonts/Inter-*.ttf      5 static weights sliced from the Inter variable font
│   └── illustrations/         generated RGBA art cache
└── tools/make_fonts.py        rebuild the static Inter weights
```

## Animation timeline (locked)

| t | Event |
|---|---|
| 0.00–0.35 | pill pops `0.8→1.0` (out-back), title slides up 40px + fades (easeOutCubic) |
| 0.15–0.50 | subtitle fades + rises |
| 0.42–1.20 | hero pops `0.7→1.0` elastic, yellow glow breathes; blue trail draws with a glow head |
| 1.20–2.00 | yellow boxes pop elastic, text types at **25 ms/char** |
| 2.00–2.80 | metrics count up 0→target, yellow underline draws left→right |
| 0.50+ | black PART bar slides up, progress dots fill |
| 2.80–5.00 | hold, 1.02 breathing pulse |
| audio | whoosh on title, pop per box, glitch on trails, typewriter ticks, 110/165 Hz pad, ding on CTA |

## 7-part formula

`1 HOOK → 2 FACT 1 → 3 FACT 2 → 4 FACT 3 (timeline) → 5 FACT 4 (chart) → 6 FACT 5 (twist) → 7 PAYOFF (CTA)`

## The bridge (zero-key, highest-quality free path)

```bash
python run.py bridge --port 8077      # open http://localhost:8077
```

1. Pick a topic → **Copy prompt**
2. Paste into ChatGPT / Gemini / Claude / Meta AI / LM Arena / Copilot (all linked on the page)
3. Paste the reply back → **Validate & save** (fences, truncation, missing parts all get repaired)
4. **Render 7 stills** or **Render video + SFX** — the log streams live
5. Amber badge on a part = still placeholder → **Repair placeholder parts** (one small free call each)

The bridge never drives those sites itself, so there is nothing to break when they redesign —
and no terms are bent in the process.

## Next steps / backlog

- [ ] Publish a keyword + hook A/B sheet for the first 10 topics.
- [ ] Whisper/TTS voice-over layer (hook script → narration) with ducking under the SFX bed.
- [ ] Reels/TikTok safe-area overlay check (`tools/safe_area.py`).
- [ ] Batch mode: read `config/topics.json`, emit a whole week of Shorts unattended
      (`python tools/batch.py --limit 5 --video`, already wired).
- [x] `python run.py bridge` — free-chatbot bridge with validation, repair and render jobs.
- [x] `python run.py fill` — placeholder repair that re-asks only the stale parts.
- [x] `python run.py doctor --deep` — per-stage provider health, `--models` lists live models.
