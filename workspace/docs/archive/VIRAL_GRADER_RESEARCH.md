# VIRAL GRADER — RESEARCH BASE (Oct 2026, verified via web)
> Foundation for tools/preflight.py. FAIR = based on measured/community-verified data, not guesses.
> HONESTY LAW: no system can GUARANTEE virality. This predicts FREEZE-risk, not success.

## THE ALGORITHM'S REAL PIPELINE (2026)
1. **SEED TEST** — Short shown to small sample pool (~200-500 impressions)
2. **VELOCITY RANK** — how fast engaged views accumulate
3. **CROSS-SURFACE** — home / search / shelf expansion if both pass
(Source: veefly, gyre.pro, usefastlane — all Oct 2026)

## RANKING SIGNALS, IN ORDER OF WEIGHT (verified)
| # | Signal | Benchmark | Grader proxy |
|---|--------|-----------|--------------|
| 1 | **Viewed vs Swiped Away** (first 1-2s) | >70% stay = workable, >80% = strong, <30% stay = DEAD | First-frame readability + motion in 0-1s + hook promise |
| 2 | **Avg % Viewed / completion** | sub-35s: 80-90%+, loop >100% = best | No static holds, pacing ≤3s, loop seam, duration |
| 3 | First-3s retention | >80% | Pattern-interrupt present before 1s |
| 4 | Rewatch/loop + shares | loop counts twice | Ending flows into opening |
| 5 | Engagement (likes 3-6%/view) | emotional spike near payoff | Payoff lands late + strong |

- **Views = OUTPUT not input** since Mar-2025 view-count change; engaged views = revenue metric.
- **CTR/thumbnail ≈ irrelevant in feed** — first frame IS the thumbnail. Thumbnail matters only for profile/search surfaces.

## METADATA — FAIR WEIGHTS (verified)
| Element | Real impact | Rule |
|---------|------------|------|
| **Title** | HIGHEST metadata signal | 40-70 chars, hook-first, primary keyword integrated, no answer-leak |
| Description | Medium | keyword in first sentence, 100-200 words enough |
| Hashtags | Small (classification only) | 3-5 incl #shorts; >15 = ALL voided |
| Backend tags | ~Zero (misspellings only) | 90 seconds max effort |
| **Spoken keyword** | Real — YT auto-transcribes VO | say the topic word in first seconds |
| **On-screen text** | Real — YT runs OCR | key terms visible as text |
| Metadata's true job | decides WHICH audience gets the seed test | mismatch = wrong pool = freeze at 0 |

## DURATION (conflicting sources — recorded honestly)
- usefastlane: 22-45s band outperforms (retention math: longer clip needs lower % hold)
- our channel data + taletok: 15-20s sweet spot for single-concept
- RESOLUTION: completion% is what's scored → 15-20s single-concept with loop >100% beats a padded 35s. Keep 15-20s law for Chronic, 40-50s Funcyous.

## WHAT CANNOT BE PREDICTED (honesty)
- Seed-pool audience mood, competition that hour, topic luck.
- NO tool can guarantee views. Services claiming this = snake oil.
- Multi-account test uploads = reused-content ban risk. NEVER.

## THE FAIR SYSTEM = 3 GATES
1. **TOPIC GATE** (before build, manual): winner-DNA match? search demand? gap vs saturation? curiosity title possible without answer-leak?
2. **PRE-FLIGHT SCORE** (tools/preflight.py, automated): 0-100 on hook/retention/packaging/tech proxies. <60 KILL, 60-74 FIX, ≥75 SHIP.
3. **HUMAN 3-SECOND TEST**: show first 3s to 5 people, stop, count who asks "phir kya hua?" — 4/5 = pass.
+ POST-FLIGHT: log @72h actual vs predicted in docs/GRADER_LOG.md → grader learns from OUR channel data.
