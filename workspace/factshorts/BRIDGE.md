# BRIDGE.md — the zero-key way to write scripts with any free chatbot

```bash
python run.py bridge --port 8077      # then open http://localhost:8077
```

## What it does

| Step | You | The bridge |
|---|---|---|
| 1 | pick a topic from `config/topics.json` | builds the exact style-locked prompt (same tokens the renderer uses) |
| 2 | **Copy prompt** → paste into ChatGPT / Gemini / Claude / Meta AI / LM Arena / Copilot | links all six sites, opens in your logged-in browser |
| 3 | paste the model's reply | `_extract_json` handles code fences, truncation, message-wrapper JSON and reasoning-only replies; `_clean_part` validates every field; missing parts get padded |
| 4 | **Validate & save** | writes `out/<topic>/script.json` + the `prompts/` folder, shows a per-part table |
| 5 | **Render 7 stills** / **Render video + SFX** | spawns the render job, streams the log, lists output files |
| 6 | amber badge on a part? | **Repair placeholder parts** re-asks just those (one small free request each) |

## API (if you want to script it)

```bash
curl "http://localhost:8077/api/prompt?topic=Why%20We%20Yawn&episode=43"      # the prompt
curl "http://localhost:8077/api/generate?topic=Why%20We%20Yawn&episode=43"    # free chain
curl -X POST http://localhost:8077/api/save   -d '{"topic":"…","json":"…"}'   # validate+save
curl -X POST http://localhost:8077/api/fill   -d '{"script":"out/…/script.json"}'
curl -X POST http://localhost:8077/api/render -d '{"kind":"video","script":"out/…/script.json"}'
curl "http://localhost:8077/api/status?id=<job id>"                          # live render log
```

## Why not a scraper

Automating those chat UIs means driving someone else's front-end with a bot: terms violations,
Cloudflare, and a rewrite every time they ship a redesign. The bridge flips it — the human is the
transport, the machine does the validation. It has no moving parts that can break on their side,
and your rate limits are your own.
