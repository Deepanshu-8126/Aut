# Skill 07 — Blender 3D & Cloud-CPU 3D Jugaad Pipeline (`@zackdfilms` Style)

## 1. Zero-Local-GPU Cloud Workspace 3D Jugaad Architecture (Active in `/home/user/explainer-pipeline`)
Because this cloud workspace runs on a **2-vCPU Intel Xeon CPU without a local NVIDIA/Vulkan GPU**, running `BLENDER_EEVEE_NEXT` or local `Wan 2.1 14B` directly on CPU OOMs. To get **real 3D Zack D. Films (`@zackdfilms`) animation & 3D perspective camera orbit** entirely inside this cloud workspace with **zero local GPU**, our pipeline combines **3 Cloud-CPU Jugaad Engines**:

1. **Engine 1 — Cloud H200 ZeroGPU `LTX-Video-Distilled` Image-to-Video (`tools/cloud_ltx_i2v.py`)**:
   - Sends our full-screen 3D cutaway plates (`assets/zack3d/zack_shot*.jpg`) to `Lightricks/LTX-Video-Distilled` (the exact model used inside `tin2tin/Pallaidium` and `laurentvv/generator-assets`) via HuggingFace ZeroGPU SSE API, generating true 30fps 3D AI-animated video clips (`assets/zack3d_videos/zack_shot01..03.mp4`) in ~7 seconds per shot.
2. **Engine 2 — Local CPU `Depth-Anything-V2-Small` ONNX Neural 3D Depth Maps (`tools/build_3d_depth_maps.py`)**:
   - Runs `onnx-community/depth-anything-v2-small` (`model_quantized.onnx`, 26 MB) locally on CPU via `onnxruntime` (~2.8s per plate) to produce true monocular 3D depth maps (`assets/zack3d_depth/zack_shot01..10_*_depth.png`) + macro-smoothed relief depth maps (`*_depth_smooth.png`).
3. **Engine 3 — Headless Blender 4.3 (`xvfb-run -a blender -b`) 3D Displaced Mesh & Orbiting Perspective Camera (`tools/blender_cloud_jugaad.py`)**:
   - Runs **Blender 4.3.2** headlessly using `BLENDER_WORKBENCH` (`FLAT` texture mode to preserve 100% of the Octane 3D render colors without gray-clay cavity artifacts).
   - Subdivides each 9:16 plate into a **57,600-polygon 3D mesh (`180×320`)**, applies a **Blender `Displace` Modifier** driven by the `Depth-Anything-V2` neural 3D depth map, applies a **Blender `Wave` Modifier** for organic 3D anatomical pulsing/flapping, and animates a **real Blender 3D Perspective Camera (`cam.location`, `cam.rotation_euler`)** orbiting across 30 frames per shot (`assets/zack3d_videos/zack_shot04..10_*.mp4`).
4. **Full-Screen 1080×1920 Compositor (`tools/render_zack3d.py`)**:
   - Keeps the **clean Full-Screen 1080×1920 3D Cutaway layout** (no upper 2 split-screen boxes).
   - Streams the 3D animated video clips (`assets/zack3d_videos/zack_shot01..10_*.mp4`), applies a **dynamic 3D Surface-Normal Specular Rim-Light Sweep** (`Sobel` gradients of the `Depth-Anything-V2` depth map), and layers glowing 3D medical vector callouts, synced word-by-word captions, and Kokoro Hindi VO + SFX into `renders/zack-3d-explainer.mp4`.

### Quick Commands (Inside Cloud Workspace)
```bash
# 1. Generate Neural 3D Depth Maps on CPU (Depth-Anything-V2 ONNX)
python3 /home/user/explainer-pipeline/tools/build_3d_depth_maps.py

# 2. (Optional) Generate Cloud H200 LTX-Video 3D clips when ZeroGPU quota is available
python3 /home/user/explainer-pipeline/tools/cloud_ltx_i2v.py

# 3. Render 3D Displaced Mesh Camera Orbit clips in Headless Blender 4.3
xvfb-run -a blender -b -P /home/user/explainer-pipeline/tools/blender_cloud_jugaad.py

# 4. Render Full-Screen 1080x1920 30fps Zack 3D Explainer MP4
python3 /home/user/explainer-pipeline/tools/render_zack3d.py /home/user/explainer-pipeline/work/zack-3d-explainer-timeline.json
```

---

## 2. Verified Reference GitHub Repositories (Blender + AI Video/3D)
1. **`tin2tin/Pallaidium`** (`https://github.com/tin2tin/Pallaidium`, 1,548★) — Generative AI Movie Studio integration for Blender VSE (`Wan 2.1`, `LTX-Video`, `HunyuanVideo`, `CogVideoX`, `Depth-Anything`).
2. **`laurentvv/generator-assets`** (`https://github.com/laurentvv/generator-assets`, 7★) — Headless automated pipeline generating `.glb` 3D meshes (`TRELLIS`, `Hunyuan3D 2.1`), `LTX-Video` clips, and `Kokoro` TTS audio.
3. **`scenario-labs/blender-plugin`** (`https://github.com/scenario-labs/blender-plugin`, 513★) — Scenario AI add-on + MCP Server for Blender rendering viewport depth/normal maps to 3D plates & PBR textures.
4. **`animatica-ai/animatica-blender-plugin`** (`https://github.com/animatica-ai/animatica-blender-plugin`, 27★) — Text-to-3D humanoid character & armature motion generator (`NVIDIA Kimodo`) inside Blender.
5. **`ahujasid/blender-mcp`** (`https://github.com/ahujasid/blender-mcp`, 31,448★) — Model Context Protocol (MCP) server connecting Claude/Cursor to Blender via Python `bpy`.

---

## 3. Reverse-Engineered `@webuilthistory` 3D Mechanical & In-World Billboard Engine (`Dee1WTNhtfy` & `DepEHOqBGzI` — 99% Visual Accuracy Spec)

> **Analyzed Frame-by-Frame from:**
> - **Reel 1 (`Dee1WTNhtfy`, `67.15s`):** *"How a car works the simple way"* (Garage pegboard tin can ──► upside-down glass cylinder piston ──► crankshaft & flywheel ──► fuel mist + spark plug ignition ──► 1-cylinder to 4-cylinder inline engine ──► house water pipe cooling & radiator fan ──► car chassis assembly & drive-out).
> - **Reel 2 (`DepEHOqBGzI`, `87.77s`):** *"How a Tesla Roadster works"* (2008 Lotus chassis + 7,000 laptop cells ──► Falcon Heavy rocket launch ──► 2017 Circular Spotlight Stage with overhead 3D Truss LED Scoreboard flipping `INTRODUCING ROADSTER` / `RANGE 620 MI` / `WEIGHT 1 TON` / `BATTERY DENSER` / `PRICE $200K` ──► Literal 3D visual metaphors: glowing stove `back burner` + giant `cherry on top of the dessert` sundae + red `DELAYED` stamp across `2020 -> 2023 -> 2024 -> 2026` ──► Translucent glass X-Ray Roadster showing internal compressed-air tank & pipes ──► 3D cyan downward force arrows ──► Giant steel truss roller-coaster loop where the Roadster hangs **upside-down** under the overhead bridge with X-ray underbody fans & rear thrusters firing!).

### The 6 Golden Laws of `@webuilthistory` 3D Design (Apply to Every Pure-Code 3D Video):

1. **One Persistent 3D World / Diorama (Continuous Spatial Geography):**
   - Never put objects in an empty black void that resets every 5 seconds.
   - Build **one continuous 3D environment** (with a ground plane, asphalt roads with dashed yellow centerlines, steel lattice truss towers, garage/stage bays, and atmospheric sky/background locked to our channel theme) where all stations exist simultaneously in 3D space.
   - Transition between beats via **smooth 3D camera pans, dollies, and whip-zooms (`cubic-bezier` ease-in-out)** from one physical station to the next inside the same 3D world.

2. **In-World 3D Truss LED Billboards Instead of Floating 2D Screen Stickers:**
   - Instead of slapping 2D HTML/SVG text boxes on top of the screen, place **physical 3D Steel Lattice Truss Portals & Matte-Black 3D LED Scoreboards (`THREE.CanvasTexture` on a 3D `BoxGeometry` screen mounted on `THREE.CylinderGeometry` steel truss towers with volumetric spotlight cones)** *inside* the 3D scene right behind/above the subject!
   - Flip the 3D LED scoreboard dynamically on each spoken beat:
     - Top small kicker (`RANGE`, `WEIGHT`, `BATTERY`, `PRICE`, `YEAR`, `THRUST`)
     - Huge bold center value (`620 MI`, `1 TON`, `DENSER`, `$200K`, `2026`, `0.81 SEC`)
     - Optional angled red rubber-stamp overlay (`[ DELAYED ]` / `[ POSTPONED ]` / `[ RECORD ]`) slamming onto the 3D scoreboard!

3. **Translucent Glass-Shell Mechanical Cutaways (`opacity: 0.22` Outer Shell + Solid Internal Organs):**
   - When explaining how a machine/car/engine works inside, do NOT just draw abstract wireframe lines.
   - Switch the outer car body or engine cylinder to **clear refractive glass (`MeshPhysicalMaterial` / `MeshStandardMaterial` with `transparent: true, opacity: 0.24`)** while keeping the **4 wheels, chassis rails, internal silver/orange pressure tank, bent metal plumbing pipes, spinning underbody fans, and pistons 100% solid and physically connected** inside the shell!
   - When the car is **upside-down** on the overhead steel truss track (`DepEHOqBGzI` `78s–85s`), zoom the camera directly to the **side-underbody profile of the upside-down car**, make the shell glass-transparent so the internal battery/air tank and spinning fans are visible, and fire **downward/upward volumetric mist & thruster cones**!

4. **Progressive Step-by-Step Mechanical Assembly (1 Part ──► 4 Parts ──► Full Machine):**
   - Just like `Dee1WTNhtfy` starts with **1 tin can**, turns it into **1 glass cylinder + piston**, adds **1 crankshaft**, adds **1 fuel nozzle + spark plug**, and then **clones it into 4 cylinders firing in sequence (`1-3-4-2`)** before adding cooling pipes, a radiator grid, and dropping the car body on top — always **build complex machines piece-by-piece in front of the viewer's eyes** as the narrator names each part!

5. **Literal 3D Visual Metaphors & Physical Force Props:**
   - Whenever the script uses an idiom or physics concept, spawn a **literal 3D physical prop** right on or under the object:
     - *"Put on the back burner"* ──► Car sits on a literal glowing **3D orange electric stove coil burner** with rising steam!
     - *"Cherry on top of the dessert"* ──► A literal **3D swirled white whipped-cream dollop + glossy red cherry on a stem** pops onto the roof of the car!
     - *"Stuffed 7,000 batteries inside"* ──► Hundreds of **3D yellow cylindrical battery cells** physically rain down into the open yellow chassis!
     - *"Pinned to the ground / sucked to the ceiling"* ──► Thick **3D extruded cyan/blue arrows** physically press down on the roof while white airflow streaks rush through the underbody fans!

6. **Ultra-Clean Screen Space (Zero Cluttered HUD Boxes):**
   - Keep the 2D screen overlay **99% empty** — only the crisp, high-contrast **center/lower word-synced caption** (`Inter-Black` white text with heavy black stroke/shadow) so the viewer's eyes never leave the 3D mechanical animation and the in-world 3D LED Truss Billboards!

---

## 4. The 5 Claude-Code Pure-Code 3D Realism & Fast CPU Render Laws (`vipi-n/tesla-roadster` + `sebayaki/roadster` + `@webuilthistory`)

> **Why Pure-Code 3D Looks Either Like a Toy OR Like a Real Studio Render:**
> Without an external `.glb`/`.blend` file, pure-code Three.js scenes look "cartoonish" if lighting is over-exposed (blowing out panel creases), surfaces lack environment reflections, ramps use primitive `TubeGeometry` pipes, or thruster smoke uses hard `ConeGeometry` shapes. Conversely, naive `MeshStandardMaterial` + `PMREMGenerator` CubeUV reflections take `1.46s/frame` on CPU SwiftShader.
> **Always apply these 5 Claude-Code Engineering Laws (`tools/render_complete_tesla_webuilthistory.py`) to achieve 100% studio realism at `~0.35s–0.50s/frame` on CPU:**

1. **Zero White-Clipping Exposure (`THREE.NeutralToneMapping` + Balanced `1.5x` Lighting):**
   - Never stack `HemisphereLight(1.45) + DirectionalLight(1.65) + RimLight(0.85)` under `ACESFilmicToneMapping` — cumulative intensity `> 3.5x` clips light/white car paint (`#E8E6E0`) to flat `#FFFFFF`, erasing every door crease, hood seam, and wheel arch!
   - Lock `renderer.toneMapping = THREE.NeutralToneMapping`, `renderer.toneMappingExposure = 1.04`, `HemisphereLight(..., 0.58)`, `DirectionalLight(0xFFF3E0, 1.52)`, and `RimLight(0xFFE0B2, 0.48)` so every lofted cross-section and BVH panel seam has deep 3D studio shading.

2. **Fast 1-Lookup Equirectangular Studio Softbox Reflections (`buildFastStudioEnvTex` on `MeshPhongMaterial`):**
   - On CPU SwiftShader, `MeshStandardMaterial` with PMREM (`textureCubeUV`) performs 8 trilinear lookups per pixel (`1.46s/frame`), while `MeshPhongMaterial` without an `envMap` looks like flat matte plastic.
   - Generate a procedural `512×256` `THREE.EquirectangularReflectionMapping` studio softbox `CanvasTexture` (`buildFastStudioEnvTex()` with dark studio ceiling, 3 feathered white/warm overhead softbox strips, horizon band, and dark floor reflection) and bind it to `MeshPhongMaterial` (`envMap: fastEnvTex`, `combine: THREE.MixOperation`, `reflectivity: 0.52` on glass, `0.28` on car paint, `0.38` on metal).
   - Override `0x8f7350` warm glass tints to smoked automotive cockpit glass (`0x111622`, `opacity: 0.78`) so the overhead softbox strips gleam across the windshield and roof at `~0.38s/frame`!

3. **Real Pure-Code CAD Structures (`buildCurl('high')`) & Volumetric Particle Plumes (`Plumes` + Feathered Sprites):**
   - Never use a plain white `TubeGeometry` circle for a stunt loop or solid `ConeGeometry` triangles for rocket exhaust!
   - Use real procedural CAD geometry (`window.RealTesla.buildCurl('high')`: segmented concrete track panels, black structural backing shell, glowing red LED edge strips, concrete support piers, and full galvanized steel lattice truss tower with diagonal X-bracing) and real volumetric particle/sprite plumes (`window.RealTesla.plumes.Plumes` + radial-gradient feathered additive sprites where `alpha = 0` on all 4 edges).

4. **Procedural Micro-Grain Surface Textures (`makeNoiseTex`) + Soft Radial Contact Shadows (`addBlobShadow`):**
   - Never leave ground grass (`#5A9E3E`) or asphalt (`#262932`) as a single flat unlit RGB color.
   - Generate `256×256` procedural micro-grain `CanvasTexture`s (`RepeatWrapping`) for turf (`#3E6B2A`), asphalt (`#20242D`), and concrete (`#CBD5E1`), and place soft radial-gradient blob shadows (`addBlobShadow(w, d, opacity)`) underneath every car, stage, truss tower, barrier, cone, and tree to ground every object without expensive per-frame `PCFSoftShadowMap` CPU passes.

5. **Long-Lens `32°`–`48°` Portrait Camera & Single-Hero PBR/Studio Mesh Discipline:**
   - Use a `32°` vertical FOV lens for outdoor vehicle tracks (`tools/render_complete_tesla_webuilthistory.py`) and a `48°` portrait diorama lens for the indoor Floating Island Garage (`tools/render_car_engine_dee1.py`).
   - Keep **1 hero high-poly `Roadster` mesh** in the scene (sharing geometries for ghost/translucent cutaways) so SwiftShader CPU vertex processing stays below `0.45s/frame`.

---

## 5. Locked Dual-Stage `@webuilthistory` 3D Production Templates (For All Future Dynamic Videos)

Every new `@webuilthistory`-style 3D explainer video dynamically selects between our **2 Pre-Built 3D Diorama Stages**:

1. **Stage A — The Floating Low-Poly Island & Pegboard Garage (`tools/render_car_engine_dee1.py`):**
   - **Use For:** *"How [X] Works the Simple Way"* (Engines, Jet Turbines, Turbochargers, Batteries, Guns, Nuclear Reactors, Refrigerators, Hydraulic Presses).
   - **Built-In 3D World:** Sunset purple-peach sky gradient + inverted brown low-poly cliff cone with dangling roots + green turf lawn & grey stepping stones + open-front white gable-roof garage + brown timber roof rafters & hanging fluorescent tube light + left red workbench with spare tire + back-wall perforated wooden pegboard with hanging red/green/yellow tools.
   - **Dynamic 10-Beat "Toy-to-Machine" Formula:**
     1. Start with **1 everyday household object** on the concrete garage floor (e.g., Soup Can, Balloon, Tea Kettle, Bicycle Pump) that fails Spectacularly (blasts through the wooden garage roof into the sky).
     2. Drop in a **Clear Refractive Glass Housing (`glassTubeMat`)** on an open-front black C-channel stand so the viewer can see inside.
     3. Morph the household object into the **First Machined Metal Part** (Piston / Rotor / Turbine Blade).
     4. Add **Real Trigonometric Kinematics** (Slider-Crank / Gear Train / Camshaft) + 1 spinning wheel/shaft.
     5. Zoom in to add **Fuel/Fluid Mist + Ignition/Spark + Compression Squeeze**.
     6. Show a **Physical Failure/Limit** (Violent Vibration / Loud Noise / Extreme Orange Heat Glow).
     7. Clone `1 → 4` units + pan along **Pipes / Glass-Fronted Baffled Boxes / Blue Cooling Loops / Radiator Grids**.
     8. Scale the completed internal mechanism down into the **Full 3D Vehicle/Machine Shell** dropping onto the chassis in the Floating Island wide payoff shot!

2. **Stage B — The Outdoor Proving Ground, Spotlight Stage & McGregor Stunt Loop (`tools/render_complete_tesla_webuilthistory.py`):**
   - **Use For:** Supercars, Rockets, Aircraft, High-Speed Trains, & Historical Engineering Stunts.
   - **Built-In 3D World:** Micro-grain turf & asphalt drag strip + circular spotlight stage + 3D steel lattice truss portals with dynamic flipping LED scoreboards (`RANGE`, `0-60 MPH`, `THRUST`) + real CAD McGregor 90-ft inverted "Curl" loop ramp (`buildCurl('high')`) + X-ray translucent glass car/vehicle cutaways.




---

## 6. 🔒 The 11 LOCKED Zack D. 3D Anatomical REALISM Laws (Template 3 Gold Standard)

> **Gold Master:** `/home/user/outputs/15-how-human-eye-works-zack3d.mp4` (37.62s)
> **Gold Renderer:** `/home/user/explainer-pipeline/tools/render_eye_zack3d.py`
> **Rule:** HAR naye Zack D. 3D Science/Human-Body video mein yeh 11 laws MANDATORY hain.
> User verdict: *"ab real feel aa raha hai"* — isi look ko replicate karna hai, kabhi downgrade nahi.

### LAW 1 — Organic Branching Textures (NEVER zig-zag doodles!)
Koi bhi biological surface (sclera veins, retina vessels, leaf veins, lightning, roots) hamesha
**recursive tapering random-walk** se banao — kabhi `Math.sin` zig-zag ya fixed bezier loops nahi:
```js
function vessel(x, y, ang, w, len) {
  if (w < 0.35 || len <= 0) return;
  const branches = [];                       // children ko stroke() ke BAAD draw karo
  g.lineWidth = w; g.beginPath(); g.moveTo(x, y);
  let cx = x, cy = y, ca = ang;
  for (let s = 0; s < len; s++) {
    ca += (Math.random() - 0.5) * 0.6;       // wandering angle
    const nx = cx + Math.cos(ca) * (8 + Math.random() * 7);
    const ny = cy + Math.sin(ca) * (8 + Math.random() * 7);
    g.quadraticCurveTo(cx, cy, (cx + nx) / 2, (cy + ny) / 2);  // smooth curve
    cx = nx; cy = ny;
    if (s > 1 && Math.random() < 0.3) branches.push([cx, cy, ca ± 0.85, w * 0.6, len - s - 1]);
  }
  g.stroke();
  branches.forEach(b => vessel(...b));       // thinner child branches
}
```

### LAW 2 — Brain/Organ Folds = Lumpy Silhouette + Ridge/Shadow Worm Texture
- **Silhouette:** `lumpyGeo(sphereGeo, amp 0.05, freq 7.2)` — vertex displacement with layered
  trig noise + `computeVertexNormals()`. Smooth balloon sphere = FAKE; lumpy bumps = REAL.
- **Texture:** meandering worm-paths, 3-pass stroke: (1) dark sulcus shadow offset +3,+5px
  width 30, (2) raised pink gyrus ridge width 22, (3) bright crest highlight width 9.

### LAW 3 — Cutaway = OPAQUE Sagittal Slice (translucent layer-mess BAN!)
Multi-layer translucent shells (`opacity 0.5` + `depthWrite:false`) overlap hokar intestine-web
mess banate hain. Sahi tarika: **near-side half CUT** (scale 0.0001), baaki opaque, aur hero
object ko slice ke SAAMNE `AdditiveBlending` glow-window ke saath float karao.

### LAW 4 — Wet-Eye / Wet-Surface Catchlights
Har glossy organic surface (eye, tongue, organ) par radial-gradient white **catchlight plane**
(big soft upper + small lower-opposite) `depthWrite:false` — instantly "wet & alive" feel.

### LAW 5 — Round Apertures Need HEAD-ON Optical-Axis Camera
Iris/pupil/barrel/nozzle macro shots mein camera ko axis ke ~25° ke andar rakho warna circle
ellipse ban jata hai. Blocking props ko hard-cut par `scale.set(0.0001)` kar do.
Aperture disc ka radius hamesha hole se bada rakho har animation extreme par (gap-ring bug!).

### LAW 6 — envMap Reflectivity KILLS Saturated Colors
`MixOperation` + `reflectivity 0.3+` red/green ko beige-brown wash kar deta hai.
Vivid organic colors (apple red, blood red, leaf green): **`reflectivity ≤ 0.12`**.
Metals/glass: 0.25–0.62 theek hai. + streaked skin texture (vertical bezier streaks + blush
gradient) flat color se 10x real lagta hai.

### LAW 7 — Interior Chambers = Radial Depth Gradient + Detail Layer (flat fill BAN!)
Hollow organ/chamber interior kabhi flat saturated color nahi: **fundus-style radial gradient**
(lit center → dark vignette edge) + surface detail (radiating vessels/striations) + bright
focal spot + low-opacity glassy inner sphere (vitreous sheen, `opacity 0.10`).

### LAW 8 — Light Rays & Energy = Additive Core + Volumetric Halo
Har beam = bright core cylinder + `3.1x` radius halo cylinder, dono
`AdditiveBlending + depthWrite:false`. Focal points par core orb + additive halo sphere.
Thin opaque pencil-lines = FAKE.

### LAW 9 — Signals INSIDE Translucent Sheaths, Elongated Streaks
Nerve/cable/pipe: smooth `TubeGeometry` (96 tubular × 22 radial segments minimum) with
`opacity ~0.56, depthWrite:false`; signals = core sphere `scale.x 2.6` + halo `scale.x 3.1`
elongated along travel (flat pea-discs / bulging caterpillar lumps BAN).

### LAW 10 — Muscles/Straps HUG the Surface
Attachment anatomy = flattened `TorusGeometry` arc ribbons (`scale.z 3.4`) jo parent sphere ke
radius se +0.04 bahar curve hug karein. Floating `BoxGeometry` blobs = FAKE.
Ciliary-type bodies = rounded scaled-sphere pads + thin fiber fans (zonules), arrow-cones nahi.

### LAW 11 — Studio Depth Pass (har video mein, har frame)
1. Soft radial **contact shadow blobs** under every grounded object (canvas radial texture plane).
2. 2D compositor **cinematic vignette**: `createRadialGradient` corners `rgba(44,32,18,0.27)`.
3. **Story-reactive lighting**: smoothstep ramps on `hemiLight`/`keyLight` + white-flash
   (max alpha 0.12) / dark-dip overlay (max 0.5) — kabhi hard light jumps nahi.
4. Scene cameras: cinematic high 3/4 angle (lookAt y thoda neeche), straight-on flat view sirf
   LAW 5 aperture shots ke liye.
5. Scene 1 wide establish: `camera.fov` lerp 50→36 + `updateProjectionMatrix()` per frame.

### ⚙️ Render Pipeline Constants (SwiftShader CPU)
- `antialias:false` on 720x1280 GL canvas → composite to 1080x1920 with `imageSmoothingQuality:'high'`.
- Sab meshes scene mein `scale 0.0001` hide trick (zero shader recompilation).
- Textures: `CanvasTexture` + `SRGBColorSpace`; biological canvases 1024px tak.
- Run: `PYTHONPATH=/var/tmp/pydeps python3 render_*.py [--preview]`, frames resumable on disk,
  mux via imageio-ffmpeg, verify with PyAV frame extraction + `read_file` sheets.
