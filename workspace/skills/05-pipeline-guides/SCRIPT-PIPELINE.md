# Script Pipeline Guide (`SCRIPT-PIPELINE.md`)

1. **Hook First:** Score 3–5 candidate hooks using `/home/user/skills/yt-script/hookscore.py`. Pick a hook with a concrete number, physical mechanism, or counter-intuitive myth break.
2. **Sourced Facts Only:** Every measurement, duration, or count must be documented in `scripts/<topic>.md` with primary textbook/scientific references. Never invent numbers.
3. **Single Physical/Causal Journey:** Connect each shot causally (`Shot N` causes `Shot N+1`), rather than listing disconnected facts.
4. **Word-Level Label Triggers:** In `scripts/<topic>.json`, attach `labels` with `at: "word:<spoken_word>"` so visual callouts lock onto the narrator's exact spoken word.
5. **Publish Kit:** Always deliver `scripts/<topic>-publish.md` checked with `/home/user/skills/yt-package/title.py`.
