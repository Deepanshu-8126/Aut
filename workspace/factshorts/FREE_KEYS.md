# FREE_KEYS.md — getting high-quality scripts without paying

The pipeline is free by default. This file is the map of what is free, what each option costs
you (time, not money), and where to drop a key if you want a permanent, rate-limit-free brain.

## Stage 0 — nothing at all (works right now)

```bash
python run.py doctor --deep     # shows which free stage is alive today
python run.py bridge            # local UI: free AI or copy/paste any chatbot
python run.py video --topic "Why We Yawn" --episode 43
```

* **Text** — the free key-less chain: `POST https://text.pollinations.ai/openai` (GPT-OSS 20B)
  and a GET fallback. It is *community-funded*, so it rate-limits (HTTP 402) in bursts.
  That is why the pipeline retries, rotates models, caches every answer on disk, and falls back
  to **7 small chunked requests** — small requests get served far more often than one big one.
* **Images** — the same free service generates FLUX images; `providers.py` also retries and
  rotates models. If it is down, the offline vector art engine takes over so a slide is never blank.
* **Repair workflow** — if a part came out as placeholder text, mark it and fix it later:

```bash
python run.py fill --script out/<topic>/script.json          # only re-asks for stale parts
python run.py fill --script out/<topic>/script.json --parts 4,5
```
  `script.json` keeps a `_src` field per part (`llm` **or** `template`) so you always know what
  is real content and what is still the example text. The bridge UI shows the same as AI/amber badges.

## Stage 1 — the bridge (zero keys, best quality/effort ratio)

```bash
python run.py bridge --port 8077
```

Open the page, hit **Copy prompt**, paste it into a chat you already use (ChatGPT, Gemini, Claude,
Meta AI, LM Arena, Copilot — it links them all), then paste the reply back and press
**Validate & save** → **Render video**.

The bridge does the boring parts: it ships the exact style-locked prompt, repairs sloppy JSON
(fences, truncation, missing parts), validates every field against the schema, pads what is
missing, writes `script.json`, and streams the render log. Nothing automates the chat sites
themselves — you are the transport, so their terms are respected and nothing breaks when they
change their UI.

## Stage 2 — a free API key (recommended if you post daily)

All of these speak the OpenAI format, so the pipeline picks one up from the environment only.
Put whichever key you get in `~/.factshorts.env` (or export it) — no code change.

| Provider | Free tier | Env var | Notes |
|---|---|---|---|
| Google AI Studio (Gemini) | generous | `GEMINI_API_KEY` | fastest, best free JSON quality |
| Groq | generous, very fast | `GROQ_API_KEY` | Llama 3.3 70B, great for 7 small chunks |
| OpenRouter | `:free` models | `OPENROUTER_API_KEY` | model choice; set `FACTSHORTS_TEXT_MODEL` |
| Cerebras | free tier | `OPENAI_API_KEY` + `OPENAI_BASE_URL=https://api.cerebras.ai/v1` | very fast |
| Ollama (local) | free forever | `OPENAI_BASE_URL=http://localhost:11434/v1` | no network needed at all |

```bash
export GEMINI_API_KEY=...        # AI Studio key
export FACTSHORTS_TEXT_MODEL=gemini-2.5-flash       # optional override
python run.py doctor --deep      # the key stage should now show up top
python run.py video --topic "How Suez Canal Was Built" --episode 45 --category "WORLD FACTS"
```

The chain order is: **free key-less → your key → offline template**, so adding a key never
breaks the free path — it just means you stop seeing placeholder parts.

## Image quality upgrade

Same idea for art. With any image-capable key (OpenAI `gpt-image-1`, or a Pollinations token)
the illustrations switch from the vector engine to generator output, then get the same white
knockout + trim + glow treatment:

```bash
export OPENAI_API_KEY=...
export FACTSHORTS_ART=ai        # auto | ai | vector
python run.py stills --demo     # watch assets/illustrations/*.png change source
```

Bring your own art any time (a Midjourney/Flux render, a crop out of a reference frame):

```bash
python tools/import_art.py --src ~/downloads/brain.png --key brain_hero --no-knockout
```

## Honest capability matrix

| What you want | Free path | Cost | Stability |
|---|---|---|---|
| 7-part script | key-less chain / bridge paste | ₹0 | key-less: rate-limited; bridge: never fails |
| Script, every day, no babysitting | Gemini or Groq free key | ₹0 | high (per-minute limits, not per-burst) |
| Illustrations | vector engine | ₹0 | 100% offline |
| Illustrations, AI quality | free FLUX endpoint or a key | ₹0 | free endpoint: best-effort |
| Voice-over | any TTS key, or record yourself | ₹0–₹X | add `tools/tts.py` (see README backlog) |
| Scraping LM Arena / Meta AI UIs | — | — | not offered: breaks their ToS and their UI |
