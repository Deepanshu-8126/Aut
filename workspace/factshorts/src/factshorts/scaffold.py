"""Scaffold workflow: get a script from any free chatbot (no keys, no scraping).

    python run.py scaffold --topic "Why We Forget Dreams" --episode 44

writes into out/<topic>/:
    script.json              a valid 7-part pack you can edit directly
    PROMPT_FOR_CHATBOT.md    paste this into ChatGPT / Gemini / Claude / Meta AI,
                             then paste the JSON it returns back into script.json
    prompts/                 the style + animation tokens for external video agents

Then render with:  python run.py video --script out/<topic>/script.json
"""
from __future__ import annotations

import json
from pathlib import Path

from . import spec as S


def write_scaffold(topic: str, out_dir: Path, episode: int = 43,
                   category: str = "BRAIN FACTS", template: bool = True) -> dict:
    pack = S.build_pack(topic, episode=episode, category=category, offline=template)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "script.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False))

    prompt_doc = f"""# Get the script for: {topic}

Any free chatbot works (ChatGPT, Gemini, Claude, Meta AI, Copilot…). No API key needed —
you paste once, you paste back once.

## 1. Paste this into the chatbot

```
{S.SYSTEM}

TOPIC = "{topic}"
EPISODE = {episode}
CATEGORY = {category}
Write the 7-part FACTSHORTS pack as JSON now.
```

## 2. Paste its reply back here

Open `script.json` in this folder, replace the whole file with the JSON it returned, save.

## 3. Render

```
python run.py video --script "{out_dir / 'script.json'}"
```

Checks the pipeline runs for you: 7 parts, title <= 60 chars, subtitle <= 48 chars,
bottom <= 48 chars, layout in hook/diagram/chart/timeline/payoff, CTA only in part 7.
Anything missing is padded automatically, so a slightly sloppy reply still renders.
"""
    (out_dir / "PROMPT_FOR_CHATBOT.md").write_text(prompt_doc)
    return pack
