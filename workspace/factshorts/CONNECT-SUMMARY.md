# CONNECT ✅ — ek command, poora Short ready

## (a) Ek hi command: `make`
```bash
cd factshorts
python3 run.py make --topic "How The Suez Canal Was Built" --episode 45 --category "WORLD FACTS"
```
Ye khud karta hai: **AI script → auto-repair (stale parts) → 7 stills (1080×1920) → 7 MP4 + FULL-short.mp4 (SFX ke saath) → preview.html**

Flags: `--no-video` (sirf stills), `--rounds 3` (repair kitni baar), `--seconds 4.5` (per part), `--no-audio`, `--offline`
Purane script se: `python3 run.py make --script out/<run>/script.json`
Sirf ek step chahiye? `run.py stills | video | fill --script ...` (video me `--only 7` = sirf part 7 re-render + FULL rebuild)

## (b) Free AI kaise chalta hai (bina key)
Text: **POST** `text.pollinations.ai/openai` → fail ho to **GET** `text.pollinations.ai/<prompt>?model=openai-fast` → phir (agar `.env`/env me key ho) OpenAI-compatible backend → akhir me offline template.
402/429 pe 18s → 45s → 72s backoff, retry cache bypass karti hai, reply reject ho to agli stage.
Images: free **flux/turbo** GET (opt-in `--art ai`); default offline PIL vector art (brain/suez/world_map) — isliye bina internet bhi chalta hai.

## (c) LM Arena / Meta AI ko "crawl" kyu NAHI kiya
Aise sites ko automate/scrape karna unke ToS ke against hai aur unki UI har hafte badalti hai (fragile + account risk). Isliye iska **allowed replacement** banaya:
- **`run.py bridge --port 8077`** → prompt copy karo → *aapke* browser me kisi bhi free chat site me paste → reply wapas paste → validate → render. (Server abhi chal raha hai: http://localhost:8077)
- **`run.py scaffold --topic ...`** → script.json + ek ready-made prompt file — wahi copy/paste flow.

## (d) Quality gate (jo is baar fix hua)
- Metric **sirf real `topic_facts` numbers** se aata hai (pehle "5 numbers" khud AI se puchta hai).
- Weak/fake number ("7 acts", "4 Silt Impact") aur literal `"None"` value/label → **drop**, render nahi hota. *"No number beats a made-up number."*
- Bottom bar ab usi fact se ban'ta hai jo metric bana (`120.7 km length`, `30,000 workers`) — LLM ka junk tail ("7 acts") hamesha ke liye out.
- Ek number do jagah repeat nahi hota (used-set seed).
- `stale`/repair: number-less part + ALL-CAPS title bhi pakde jate hain; facts khatam ho gaye to missing number jayaz hai.

## (e) Is turn ke bug-fixes
| Fix | Kya theek hua |
|---|---|
| `clean_str()` | `'None'`/`'null'`/`'n/a'` strings schema se gaye |
| `short_tail()` | bottom bar fact-value + head-noun se |
| used-set seed | duplicate metric nahi |
| fact regex | `100 million francs`, `12%` (percent) parse hote hain |
| label cap 40 | lambe fact labels drop nahi hote, truncate hote hain |
| `fill_derived` self-heal | `_facts` missing ho to khud fetch karta hai |
| `topic_facts` re-ask | cached reply me number na ho to fresh rephrased ask |
| provider cache | empty/failed reply disk me save nahi hoti |
| `--only N` (video) | missing part + FULL concat (deja-vu ka part-7 isi se banaya) |

## (f) Is turn ka output
| Run | Files | Status |
|---|---|---|
| `out/how-the-suez-canal-was-built/` **EP45** | 7 PNG + 7 MP4 + `FULL-short.mp4` **31.5s** + preview.html | ✅ real metrics: 120.7 km, 24 m, 10 years, 30,000, 100 million |
| `out/why-you-feel-deja-vu-.../` demo | 7 PNG + 7 MP4 + `FULL-short.mp4` **31.5s** | ✅ part-7 + FULL is turn me complete hue |
| `out/why-time-feels-faster-as-you-age/` **EP43** | 7 PNG + preview.html | ✅ real metrics: 12%, 30%, 5%, 200, 15 min |
| EP44 (dreams) | — | ⏸ chaha to apne haath se likha jaayega (bola tha "sirf pooche to") |

> Note: har part 4–6s, total 31.5s (spec 25–32s). Awaaz: whoosh/pop/typewriter/glitch/pad + final ding, lo-fi ~85 BPM.

## Limits (jhooth nahi)
- Free tier **ek waqt me ek job** — parallel jobs se 402 burst aata hai (isliye jobs serialize kiye).
- 402 burbst transient hai; `RATE_LIMIT_WAIT` (default 18s) se handle hota hai.
- Kabhi-kabhi model payoff (part 7) pe 2 attempts me bhi usable reply nahi deta → phir `run.py fill --script ... --parts 7` dobara, ya seedha script.json me edit (EP43 me maine yahi kiya).
- Snapshot reset pe background renders marr jate hain — sirf jo log me "done" dikha, wahi pakka hai.
