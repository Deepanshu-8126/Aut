# 3D SCENE SPEC DISCIPLINE (from awesome-3d-prompts analysis, 2026-10-21)
> STATUS: LOCKED as MODE 3D (2026-10-21). Production spec + enhance checklist:
> /home/user/explainer-pipeline/MODE_3D_LOCKED.md
Source pattern: ZEUS "robot bench" verbatim prompt (BeatAPI/awesome-3d-prompts, Web 3D #21)
+ Chinese courtyard staged-build (#2) + image->3D diorama (#1).
Model-independent: WE write the Three.js/GLSL code ourselves (free-only rule).

## Every 3D beat in our videos gets a 10-section spec BEFORE code:
1. WHAT IT IS — one paragraph, one subject, one room/stage. No second room.
2. HOW IT MOVES — numbered motion list (camera path, loops, idle life). Feet don't slide.
3. THE LOOK — palette, light sources (name each), fog, material rules.
4. SHOWN ONLY THROUGH USES — actions demonstrate features; never explain in captions.
5. CAMERA — fixed FOV, framing %, orbit limits, never cuts (or named cuts only).
6. BANNED, EACH ONE NAMED — no lens flare / no hard shadows / no realistic textures /
   no text inside 3D (captions live in our 2D band) / list per project.
7. BUILD BUDGET — hard-no list for this version + time priority order.
   "If time runs out: empty bench + beautiful robot > dressed bench + stiff robot."
8. PROOF WITH RENDERS, NOT WORDS — preview checkpoints (our --preview sheet) before
   full render; silhouette test at small size; state A vs state B side by side.
9. STAGED BUILD LOOP — structure -> inspect in browser -> fix -> then add life
   (droplets, dust, flicker) gradually, subtle and natural.
10. AFTER BUILD — name the 3 things you would fix first.

## Our tech recipe (sandbox, free):
- three.min.js r128 (classic script, THREE global) at /var/tmp/three/three.min.js
  (re-download: unpkg.com/three@0.128.0/build/three.min.js; /var/tmp dies on reset).
- Headless Chromium + SwiftShader: render GL at 1280x720 (or 960x540), composite onto
  2D canvas at 1920x1080 for crisp text/band/grain. Shadows OFF, fog ON, low-poly.
- 2.5D "engraving diorama": our AI engravings as textured planes/billboards inside a
  3D cave, camera dollies IN — the "image -> navigable world" trick, pure free.
- First proof: outputs/34-three3d-gufa-test.mp4 (Patal gufa diorama, 10s).
