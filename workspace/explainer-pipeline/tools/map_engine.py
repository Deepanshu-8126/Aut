#!/usr/bin/env python3
"""
CHRONIC OF HISTORIC — Template 1A v2 REUSABLE VOX-STYLE MAP ANIMATION ENGINE
=============================================================================
Real Natural-Earth coastlines + borders (Web-Mercator) rendered in the locked
black-gold CHRONIC OF HISTORIC style with:
  - Camera keyframes (pan + log-zoom), smoothstep eased
  - Animated golden route line (comet head + glow) along real lat/lon waypoints
  - Pin pops with pulse rings + label chips when the route head arrives
  - Title chip, era chip, live distance counter, compass rose
  - Graticule, coast glow, dashed borders, vignette + film grain

USAGE:
  PYTHONPATH=/var/tmp/pydeps python3 map_engine.py                  # built-in Mansa Musa demo
  PYTHONPATH=/var/tmp/pydeps python3 map_engine.py --config my.json # custom route/camera
  PYTHONPATH=/var/tmp/pydeps python3 map_engine.py --preview        # 4 snapshot JPGs only

CONFIG SCHEMA (JSON):
{
  "width": 1080, "height": 1920, "fps": 24, "dur": 10.5,
  "out": "/home/user/renders/map_scene.mp4",
  "title": "THE ROYAL CARAVAN", "subtitle": "NIANI - MECCA  •  4,000 MILES",
  "era_chip": "MALI EMPIRE  •  1324 AD",
  "counter": {"label": "MILES TRAVELED", "max": 4000},
  "camera": [ {"t":0,"lon":-9.0,"lat":13.5,"scale":8200}, ... ],   # scale = world-width px
  "route":  {"start":0.9,"end":8.8,
             "points":[{"lon":-9.6,"lat":11.4,"name":"NIANI"}, ...]}
}
Integrate into any Template 1A renderer: render a map MP4 segment with this CLI,
or copy buildMapScene() JS into the master HTML and call drawMap(ctx, t).
"""

import os
import sys
import json
import base64
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ASSETS = "/home/user/explainer-pipeline/assets"
LAND_GEOJSON = os.path.join(ASSETS, "world_110m.geojson")
BORDERS_GEOJSON = os.path.join(ASSETS, "world_borders_110m.geojson")
FONT_BEBAS = os.path.join(ASSETS, "fonts", "BebasNeue-Regular.ttf")
FONT_INTER = os.path.join(ASSETS, "fonts", "Inter-SemiBold.ttf")
CHROME_BIN = "/opt/playwright/browsers/chromium-1247/chrome-linux64/chrome"
WORK_DIR = "/var/tmp/map_engine"

DEMO_CONFIG = {
    "width": 1080, "height": 1920, "fps": 24, "dur": 10.5,
    "out": "/home/user/renders/map_engine_demo_mansa_route.mp4",
    "title": "THE ROYAL CARAVAN",
    "subtitle": "NIANI - MECCA  \u2022  4,000 MILES",
    "era_chip": "MALI EMPIRE  \u2022  1324 AD",
    "counter": {"label": "MILES TRAVELED", "max": 4000},
    "camera": [
        {"t": 0.0,  "lon": -9.0, "lat": 13.5, "scale": 8200},
        {"t": 4.2,  "lon": 3.0,  "lat": 21.0, "scale": 6200},
        {"t": 7.4,  "lon": 30.0, "lat": 28.5, "scale": 8600},
        {"t": 10.5, "lon": 14.0, "lat": 22.0, "scale": 5000},
    ],
    "route": {
        "start": 0.9, "end": 8.8,
        "points": [
            {"lon": -9.6,  "lat": 11.4,  "name": "NIANI"},
            {"lon": -7.0,  "lat": 17.3,  "name": "WALATA"},
            {"lon": -3.6,  "lat": 23.7,  "name": "TAGHAZA"},
            {"lon": 5.5,   "lat": 26.5},
            {"lon": 13.9,  "lat": 25.9},
            {"lon": 21.5,  "lat": 27.8},
            {"lon": 25.5,  "lat": 29.0},
            {"lon": 31.24, "lat": 30.05, "name": "CAIRO"},
            {"lon": 32.9,  "lat": 29.3},
            {"lon": 35.4,  "lat": 28.6},
            {"lon": 37.4,  "lat": 25.3},
            {"lon": 38.4,  "lat": 23.2},
            {"lon": 39.83, "lat": 21.42, "name": "MECCA"},
        ],
    },
}

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @font-face { font-family: 'BebasNeue'; src: url('data:font/ttf;base64,__FONT_BEBAS__') format('truetype'); }
  @font-face { font-family: 'InterSemi'; src: url('data:font/ttf;base64,__FONT_INTER__') format('truetype'); }
  html, body { margin: 0; padding: 0; background: #000; }
  canvas { display: block; }
</style></head>
<body>
<canvas id="cv"></canvas>
<script>
const CFG = __CONFIG__;
const LAND = __LAND__;
const BORDERS = __BORDERS__;

const W = CFG.width, H = CFG.height;
const cv = document.getElementById('cv');
cv.width = W; cv.height = H;
const ctx = cv.getContext('2d');

// ---------- helpers ----------
function clamp01(v) { return Math.max(0, Math.min(1, v)); }
function smoothstep(a, b, t) { const x = clamp01((t - a) / (b - a)); return x * x * (3 - 2 * x); }
function lerp(a, b, u) { return a + (b - a) * u; }

// ---------- Web-Mercator ----------
function mercX(lon) { return lon / 360 + 0.5; }
function mercY(lat) {
  const p = Math.max(-85, Math.min(85, lat)) * Math.PI / 180;
  return 0.5 - Math.log(Math.tan(Math.PI / 4 + p / 2)) / (2 * Math.PI);
}

// ---------- flatten geojson into rings / lines (merc space) ----------
function flatten(geo) {
  const out = [];
  for (const f of geo.features) {
    const g = f.geometry;
    const polys = g.type === 'Polygon' ? [g.coordinates]
                : g.type === 'MultiPolygon' ? g.coordinates
                : g.type === 'LineString' ? [[g.coordinates]]
                : g.type === 'MultiLineString' ? [g.coordinates] : [];
    for (const poly of polys) {
      for (const ring of poly) {
        const r = ring.map(c => [mercX(c[0]), mercY(c[1])]);
        let x0 = 9, x1 = -9, y0 = 9, y1 = -9;
        for (const p of r) { x0 = Math.min(x0, p[0]); x1 = Math.max(x1, p[0]); y0 = Math.min(y0, p[1]); y1 = Math.max(y1, p[1]); }
        out.push({ pts: r, bbox: [x0, y0, x1, y1] });
      }
    }
  }
  return out;
}
const landRings = flatten(LAND);
const borderLines = flatten(BORDERS);

// ---------- camera ----------
function cameraAt(t) {
  const K = CFG.camera;
  if (t <= K[0].t) return K[0];
  for (let i = 0; i < K.length - 1; i++) {
    if (t <= K[i + 1].t) {
      const u = smoothstep(K[i].t, K[i + 1].t, t);
      return {
        lon: lerp(K[i].lon, K[i + 1].lon, u),
        lat: lerp(K[i].lat, K[i + 1].lat, u),
        scale: Math.exp(lerp(Math.log(K[i].scale), Math.log(K[i + 1].scale), u))
      };
    }
  }
  return K[K.length - 1];
}
let CAM = cameraAt(0);
function px(mx, my) { return [(mx - mercX(CAM.lon)) * CAM.scale + W / 2, (my - mercY(CAM.lat)) * CAM.scale + H / 2]; }

// ---------- route: Catmull-Rom resample + arc lengths ----------
const RPTS = CFG.route.points.map(p => [mercX(p.lon), mercY(p.lat)]);
function catmull(pts, n) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let s = 0; s < n; s++) {
      const u = s / n, u2 = u * u, u3 = u2 * u;
      out.push([
        0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
        0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)
      ]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
}
const PATH = catmull(RPTS, 90);
const CUM = [0];
for (let i = 1; i < PATH.length; i++) {
  CUM.push(CUM[i - 1] + Math.hypot(PATH[i][0] - PATH[i - 1][0], PATH[i][1] - PATH[i - 1][1]));
}
const TOTAL = CUM[CUM.length - 1];
// arrival fraction per waypoint
const WP_FRAC = RPTS.map(wp => {
  let best = 0, bd = 9;
  for (let i = 0; i < PATH.length; i++) {
    const d = Math.hypot(PATH[i][0] - wp[0], PATH[i][1] - wp[1]);
    if (d < bd) { bd = d; best = i; }
  }
  return CUM[best] / TOTAL;
});

// ---------- film grain ----------
const noiseCv = document.createElement('canvas');
noiseCv.width = 256; noiseCv.height = 256;
(function () {
  const g = noiseCv.getContext('2d');
  const img = g.createImageData(256, 256);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = 110 + Math.random() * 90;
    img.data[i] = v; img.data[i + 1] = v; img.data[i + 2] = v; img.data[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
})();

function roundRect(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }

function chip(cx, cy, text, big, sub) {
  ctx.font = (big ? '600 30px' : '600 24px') + ' InterSemi';
  const tw = ctx.measureText(text).width;
  const w = tw + 46, h = big ? 64 : 50;
  // SAFE-MARGIN CLAMP: chips kabhi screen edge par cut nahi honge (90px safe area)
  cx = Math.max(90 + w / 2, Math.min(W - 90 - w / 2, cx));
  cy = Math.max(90 + h / 2, Math.min(H - 90 - h / 2, cy));
  ctx.fillStyle = 'rgba(10,12,18,0.88)';
  ctx.strokeStyle = 'rgba(212,168,67,0.85)';
  ctx.lineWidth = 2.5;
  roundRect(cx - w / 2, cy - h / 2, w, h, 12); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#F4E9D0';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, cx, cy + 1);
}

// ---------- master draw ----------
window.renderFrameDataUrl = function (t) {
  CAM = cameraAt(t);

  // 1. SEA
  const sea = ctx.createLinearGradient(0, 0, 0, H);
  sea.addColorStop(0, '#0C1322'); sea.addColorStop(0.5, '#0E1728'); sea.addColorStop(1, '#090E18');
  ctx.fillStyle = sea; ctx.fillRect(0, 0, W, H);
  const rad = ctx.createRadialGradient(W / 2, H * 0.44, 80, W / 2, H * 0.5, H * 0.75);
  rad.addColorStop(0, 'rgba(46,58,86,0.35)'); rad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = rad; ctx.fillRect(0, 0, W, H);

  // 2. GRATICULE every 10 deg
  ctx.strokeStyle = 'rgba(212,168,67,0.07)'; ctx.lineWidth = 1;
  for (let lon = -180; lon <= 180; lon += 10) {
    const x = px(mercX(lon), 0)[0];
    if (x < -50 || x > W + 50) continue;
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }
  for (let lat = -80; lat <= 80; lat += 10) {
    const y = px(0, mercY(lat))[1];
    if (y < -50 || y > H + 50) continue;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }

  // 3. LAND (coast glow pass + fill pass)
  const vx0 = mercX(CAM.lon) - (W / 2 + 80) / CAM.scale, vx1 = mercX(CAM.lon) + (W / 2 + 80) / CAM.scale;
  const vy0 = mercY(CAM.lat) - (H / 2 + 80) / CAM.scale, vy1 = mercY(CAM.lat) + (H / 2 + 80) / CAM.scale;
  function visible(b) { return !(b[2] < vx0 || b[0] > vx1 || b[3] < vy0 || b[1] > vy1); }
  ctx.save();
  for (const ring of landRings) {
    if (!visible(ring.bbox)) continue;
    ctx.beginPath();
    for (let i = 0; i < ring.pts.length; i++) {
      const p = px(ring.pts[i][0], ring.pts[i][1]);
      if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
    }
    ctx.closePath();
    ctx.fillStyle = '#191510';
    ctx.fill();
    ctx.strokeStyle = 'rgba(245,197,66,0.16)'; ctx.lineWidth = 7; ctx.stroke();
    ctx.strokeStyle = '#C9A14E'; ctx.lineWidth = 2.2; ctx.stroke();
  }
  ctx.restore();

  // 4. BORDERS (faint dashed)
  ctx.save();
  ctx.setLineDash([7, 6]);
  ctx.strokeStyle = 'rgba(201,161,78,0.20)'; ctx.lineWidth = 1.3;
  for (const ln of borderLines) {
    if (!visible(ln.bbox)) continue;
    ctx.beginPath();
    for (let i = 0; i < ln.pts.length; i++) {
      const p = px(ln.pts[i][0], ln.pts[i][1]);
      if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
    }
    ctx.stroke();
  }
  ctx.restore();

  // 5. ROUTE
  const u = smoothstep(CFG.route.start, CFG.route.end, t);
  const lenNow = u * TOTAL;
  // faint full path preview
  ctx.save();
  ctx.setLineDash([3, 9]); ctx.strokeStyle = 'rgba(245,197,66,0.22)'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  for (let i = 0; i < PATH.length; i++) {
    const p = px(PATH[i][0], PATH[i][1]);
    if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
  }
  ctx.stroke();
  ctx.restore();
  // progressed golden line + glow
  if (u > 0.001) {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    for (const pass of [[14, 'rgba(245,197,66,0.14)'], [5.5, '#F5C542']]) {
      ctx.strokeStyle = pass[1]; ctx.lineWidth = pass[0];
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.beginPath();
      let started = false;
      for (let i = 0; i < PATH.length; i++) {
        if (CUM[i] > lenNow) break;
        const p = px(PATH[i][0], PATH[i][1]);
        if (!started) { ctx.moveTo(p[0], p[1]); started = true; } else ctx.lineTo(p[0], p[1]);
      }
      ctx.stroke();
    }
    // comet head
    let hi = 0; while (hi < CUM.length - 1 && CUM[hi] < lenNow) hi++;
    const hp = px(PATH[hi][0], PATH[hi][1]);
    if (u < 0.999) {
      const hg = ctx.createRadialGradient(hp[0], hp[1], 2, hp[0], hp[1], 34);
      hg.addColorStop(0, 'rgba(255,240,190,0.95)'); hg.addColorStop(0.35, 'rgba(245,197,66,0.55)'); hg.addColorStop(1, 'rgba(245,197,66,0)');
      ctx.fillStyle = hg; ctx.beginPath(); ctx.arc(hp[0], hp[1], 34, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#FFF4D0'; ctx.beginPath(); ctx.arc(hp[0], hp[1], 6, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }

  // 6. PINS + LABEL CHIPS (unnamed via-waypoints = sirf route shaping, no pin/label)
  for (let w = 0; w < RPTS.length; w++) {
    if (!CFG.route.points[w].name) continue;
    if (u < WP_FRAC[w] - 0.001) continue;
    const arriveT = CFG.route.start + WP_FRAC[w] * (CFG.route.end - CFG.route.start);
    const age = t - arriveT;
    if (age < 0) continue;
    const pop = smoothstep(0, 0.35, age);
    const p = px(RPTS[w][0], RPTS[w][1]);
    // Pin OFF-SCREEN ya edge par? Pura skip — orphan/detached floating chips BAN!
    if (p[0] < 30 || p[0] > W - 30 || p[1] < 30 || p[1] > H - 30) continue;
    // pulse ring
    if (age < 1.1) {
      const pr = 10 + age * 55;
      ctx.strokeStyle = 'rgba(245,197,66,' + (0.55 * (1 - age / 1.1)).toFixed(3) + ')';
      ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(p[0], p[1], pr, 0, Math.PI * 2); ctx.stroke();
    }
    // gold diamond pin
    ctx.save();
    ctx.translate(p[0], p[1]); ctx.rotate(Math.PI / 4); ctx.scale(pop, pop);
    ctx.fillStyle = '#F5C542'; ctx.fillRect(-9, -9, 18, 18);
    ctx.fillStyle = '#141018'; ctx.fillRect(-4, -4, 8, 8);
    ctx.restore();
    // label chip (per-point "ldx"/"ldy" config offsets for collision-free placement)
    if (pop > 0.65) {
      chip(p[0] + (CFG.route.points[w].ldx || 0),
           p[1] - 52 + (CFG.route.points[w].ldy || 0),
           CFG.route.points[w].name, false);
    }
  }

  // 7. TITLE + ERA CHIP + COUNTER + COMPASS
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(10,12,18,0.90)';
  ctx.strokeStyle = 'rgba(212,168,67,0.9)'; ctx.lineWidth = 3;
  roundRect(W / 2 - 330, 120, 660, 150, 20); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#F4E9D0'; ctx.font = '68px BebasNeue';
  ctx.fillText(CFG.title, W / 2, 178);
  ctx.fillStyle = '#D4A843'; ctx.font = '600 26px InterSemi';
  ctx.fillText(CFG.subtitle, W / 2, 234);
  chip(W / 2, 330, CFG.era_chip, true);

  if (CFG.counter) {
    const miles = Math.round(u * CFG.counter.max);
    ctx.fillStyle = 'rgba(10,12,18,0.88)';
    ctx.strokeStyle = 'rgba(212,168,67,0.85)'; ctx.lineWidth = 2.5;
    roundRect(70, H - 320, 380, 130, 16); ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    ctx.fillStyle = '#D4A843'; ctx.font = '600 24px InterSemi';
    ctx.fillText(CFG.counter.label, 100, H - 282);
    ctx.fillStyle = '#F4E9D0'; ctx.font = '74px BebasNeue';
    ctx.fillText(miles.toLocaleString('en-US'), 100, H - 226);
  }

  // compass rose
  ctx.save();
  ctx.translate(W - 120, H - 250); ctx.strokeStyle = 'rgba(212,168,67,0.75)'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(0, 0, 44, 0, Math.PI * 2); ctx.stroke();
  ctx.fillStyle = 'rgba(245,197,66,0.9)';
  ctx.beginPath(); ctx.moveTo(0, -38); ctx.lineTo(9, 0); ctx.lineTo(0, 38); ctx.lineTo(-9, 0); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#F4E9D0'; ctx.font = '600 22px InterSemi'; ctx.textAlign = 'center';
  ctx.fillText('N', 0, -58);
  ctx.restore();

  // 8. VIGNETTE + GRAIN
  const vg = ctx.createRadialGradient(W / 2, H * 0.47, H * 0.28, W / 2, H * 0.52, H * 0.80);
  vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.42)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  ctx.save();
  ctx.globalAlpha = 0.045;
  ctx.translate(-Math.floor(Math.random() * 256), -Math.floor(Math.random() * 256));
  ctx.fillStyle = ctx.createPattern(noiseCv, 'repeat');
  ctx.fillRect(0, 0, W + 256, H + 256);
  ctx.restore();

  return cv.toDataURL('image/jpeg', 0.92);
};
</script>
</body></html>
"""


def b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def main():
    cfg = dict(DEMO_CONFIG)
    if "--config" in sys.argv:
        with open(sys.argv[sys.argv.index("--config") + 1]) as f:
            cfg.update(json.load(f))
    preview = "--preview" in sys.argv

    frames_dir = os.path.join(WORK_DIR, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    with open(LAND_GEOJSON) as f:
        land = f.read()
    with open(BORDERS_GEOJSON) as f:
        borders = f.read()

    html = (HTML_TEMPLATE
            .replace("__FONT_BEBAS__", b64_file(FONT_BEBAS))
            .replace("__FONT_INTER__", b64_file(FONT_INTER))
            .replace("__CONFIG__", json.dumps(cfg))
            .replace("__LAND__", land)
            .replace("__BORDERS__", borders))
    html_path = os.path.join(WORK_DIR, "index.html")
    with open(html_path, "w") as f:
        f.write(html)

    total_frames = int(round(cfg["dur"] * cfg["fps"]))

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_BIN, headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = browser.new_page(viewport={"width": cfg["width"], "height": cfg["height"], "device_scale_factor": 1})

        def handle_route(route):
            if route.request.url.endswith("/index.html"):
                route.fulfill(path=html_path, content_type="text/html")
            else:
                route.continue_()
        page.route("**/*", handle_route)
        page.goto("http://localhost/index.html", wait_until="load")
        page.wait_for_function("typeof window.renderFrameDataUrl === 'function'")
        # Warm up canvas + wait for BebasNeue/Inter to be fully loaded (first-frame font race fix)
        page.evaluate("window.renderFrameDataUrl(0)")
        page.wait_for_function("document.fonts.status === 'loaded'")
        page.evaluate("window.renderFrameDataUrl(0)")

        if preview:
            for st in [0.4, 1.6, 2.8, 4.6, 6.2, 7.8, 9.3, 10.4]:
                durl = page.evaluate("window.renderFrameDataUrl(%f)" % st)
                out = os.path.join(WORK_DIR, "snap_%04.1fs.jpg" % st)
                with open(out, "wb") as f:
                    f.write(base64.b64decode(durl.split(",", 1)[1]))
                print("Saved", out)
            browser.close()
            return

        import time
        t0 = time.time()
        for i in range(total_frames):
            fp = os.path.join(frames_dir, "%05d.jpg" % i)
            if os.path.exists(fp):
                continue
            durl = page.evaluate("window.renderFrameDataUrl(%f)" % (i / cfg["fps"]))
            with open(fp, "wb") as f:
                f.write(base64.b64decode(durl.split(",", 1)[1]))
            if i % 48 == 0:
                print("Frame %d/%d (%.1f fps)" % (i + 1, total_frames, (i + 1) / max(0.01, time.time() - t0)))
        browser.close()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    out = cfg["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([
        ffmpeg, "-nostdin", "-y",
        "-framerate", str(cfg["fps"]), "-i", os.path.join(frames_dir, "%05d.jpg"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "24",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", out
    ], check=True, capture_output=True)
    print("SUCCESS:", out, "%.2f MB" % (os.path.getsize(out) / 1e6))


if __name__ == "__main__":
    main()
