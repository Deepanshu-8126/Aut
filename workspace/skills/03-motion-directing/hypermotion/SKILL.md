# HyperMotion Skill (`03-motion-directing/hypermotion/SKILL.md`)

## Purpose
High-retention kinetic typography, spring-physics callout pops, micro-shake/flash transitions, and visual beat synchronization for vertical (`1080 × 1920`) Shorts and long-form explainers.

## Core Rules Applied During Video Generation
1. **Spring Callout Pop (`damping: 14, stiffness: 180`):**
   - Every callout label (`at: "word:<token>"`) and metric badge scales from `0.72 → 1.04 → 1.00` over `220 ms` (`easeOutBack` / critically damped spring).
2. **Active-Word Kinetic Highlight:**
   - Captions group into `4–5` words maximum per phrase inside the safe lower-third band (`y = 1420..1600`, `x = 90..990`).
   - The currently spoken word receives a `#FFD60A` pill background + `#0A0E16` bold text synchronized to word timestamps.
3. **Transition Flash & Sub-Whoosh Lock:**
   - First `120 ms` (`3–4` frames at `30 fps`) of every shot transition applies an `alpha = 110 → 0` optical flash paired with a `160 Hz → 65 Hz` sub-bass whoosh.
4. **Micro-Motion Alive State:**
   - Never leave a frame completely static: combine slow camera push (`1.00 → 1.14` cubic ease-out) with radial wave rings (`1.8 Hz` pulse) and travelling signal particles.
