# MODE 3D — "REAL CAMERA" LAYER (LOCKED 2026-10-21)

## STATUS
- NEW standalone mode (user directive: "yeh bhi lock karo, new mode mein daalna").
- NOT merged into 1C. Use when a scene needs a real moving camera inside a 3D space
  (cave interiors, temple walk-around, fly-through, diorama dives).
- Voice stays OURS (voice-06 Hindi / voice-01), SFX synthesized by us. Zero paid APIs.

## PROVEN BASE (test 34, outputs/34-three3d-gufa-test.mp4)
- three.min.js r128 classic build (local copy /var/tmp/three/three.min.js; re-download
  from unpkg if sandbox reset — it's MIT/free).
- SwiftShader headless Chromium, GL offscreen 1280x720 -> drawImage onto 1920x1080 2D
  composite (band + grain + vignette). ~4.2 fps for modest scene. Shadows OFF, fog ON,
  antialias:false, low-poly.
- Reference implementation: tools/render_three_gufa_test.py
- Spec discipline: skills/10-3d-scene-spec (ZEUS 10-section spec, BUILD BUDGET, proof
  renders before claiming done).

## ENHANCE DIRECTIVE (user: "thoda enhance ho, real feeling aaye")
Mandatory upgrades over test 34 before first production use:
1. ROCK REALISM — multi-octave noise displacement on cave/terrain meshes (not plain
   cones); procedural canvas textures (color + bump via THREE.CanvasTexture) so rock
   has grain, wet sheen patches, color variation.
2. MATERIAL DEPTH — MeshStandardMaterial with roughness/metalness variation + bump map;
   subtle envMap-style specular on wet/metal surfaces.
3. PARTICLE POLISH — droplet gets splash micro-particles on impact (not just ripple);
   dust motes get size/opacity variation; optional ember/firefly particles near flames.
4. LIGHT REALISM — torch flicker uses layered noise (not single sine); colored bounce
   fill; fake volumetric: additive cones + 2D composite glow pass.
5. 2D COMPOSITE GRADE — fake bloom (bright-pass blur on canvas), lift-gamma-gain color
   grade, chromatic edge touch, stronger depth haze bands. Cheap in 2D, sells realism.
6. CAMERA FEEL — handheld micro-shake (perlin, tiny), ease-in-out on dolly segments,
   rack-focus fake via 2D blur layers when subject changes.
7. PHOTO INTEGRATION — real place photos / AI engravings as textured plates INSIDE the
   3D set (2.5D diorama trick) — keep "AI ART" tag rule for AI stills.

## BANNED IN THIS MODE
- Shadows ON (SwiftShader cost), r160+ ESM builds, EffectComposer post chain (do grade
  in 2D composite instead), antialias:true, scenes above ~40 meshes + ~600 particles,
  cuts inside a single 3D shot (one continuous camera per shot).

## WORKFLOW (unchanged discipline)
Spec (10 sections) -> preview sheet (6 checkpoints) -> frame-verify -> batch render via
start_process -> mux with locked recipe -> frame-verify final MP4 -> then claim done.
