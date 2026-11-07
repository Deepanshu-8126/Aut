#!/usr/bin/env python3
"""
VIRAL AGENT v2 — evidence extractor for AI-judge review (pairs with the agent's own vision).
Architecture = same as paid tools (PreViral/ViralWatch): metrics + frames + AI judge. Free.
Usage: python3 viral_agent.py --video X.mp4 [--out /var/tmp/agentX] [--ffmpeg ..] [--ffprobe ..]
Produces in --out:
  hook_strip.jpg      0 / 0.5 / 1 / 2 / 3 s   (the swipe-decision window)
  contact_sheet.jpg   12 frames across full duration (structure/pacing view)
  motion_curve.jpg    per-0.5s visual-change bars + cut markers + static-hold flags
  audio_curve.jpg     per-0.5s RMS energy bars (dead-air finder)
  report.json         all raw metrics for the AI judge
"""
import argparse, json, math, os, shutil, subprocess, sys, tempfile

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout + r.stderr

def find_tool(name, override):
    if override and os.path.exists(override): return override
    p = shutil.which(name)
    if p: return p
    c = f"/var/tmp/ffstatic/{name}"
    if os.path.exists(c): return c
    sys.exit(f"{name} not found")

def grab(ffmpeg, video, t, path, scale=None):
    cmd = [ffmpeg, "-nostdin", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1"]
    if scale: cmd += ["-vf", f"scale={scale}"]
    sh(cmd + [path])
    return os.path.exists(path)

def main():
    from PIL import Image, ImageChops, ImageDraw, ImageStat
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--ffmpeg", default=None); ap.add_argument("--ffprobe", default=None)
    a = ap.parse_args()
    ffmpeg = find_tool("ffmpeg", a.ffmpeg); ffprobe = find_tool("ffprobe", a.ffprobe)
    out = a.out or os.path.join("/var/tmp", "agent_" + os.path.splitext(os.path.basename(a.video))[0])
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="va_")

    meta = json.loads(sh([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", a.video]))
    dur = float(meta["format"]["duration"])

    # ---- hook strip: the swipe-decision window ----
    hts = [0.03, 0.5, 1.0, 2.0, 3.0]
    strip = Image.new("RGB", (5 * 216, 384 + 26), (12, 12, 14))
    d = ImageDraw.Draw(strip)
    for i, t in enumerate(hts):
        p = os.path.join(tmp, f"h{i}.jpg"); grab(ffmpeg, a.video, t, p)
        strip.paste(Image.open(p).resize((216, 384)), (i * 216, 26))
        d.text((i * 216 + 6, 6), f"{t:.1f}s", fill=(255, 196, 64))
    strip.save(os.path.join(out, "hook_strip.jpg"), quality=88)

    # ---- contact sheet: 12 frames across duration ----
    cs = Image.new("RGB", (4 * 216, 3 * 384 + 3 * 26), (12, 12, 14))
    d = ImageDraw.Draw(cs)
    for i in range(12):
        t = dur * (i + 0.5) / 12
        p = os.path.join(tmp, f"c{i}.jpg"); grab(ffmpeg, a.video, t, p)
        x, y = (i % 4) * 216, (i // 4) * (384 + 26)
        cs.paste(Image.open(p).resize((216, 384)), (x, y + 26))
        d.text((x + 6, y + 6), f"{t:.1f}s", fill=(255, 196, 64))
    cs.save(os.path.join(out, "contact_sheet.jpg"), quality=86)

    # ---- motion curve per 0.5s ----
    n = int(dur * 2) - 1
    prev = None; diffs = []
    for i in range(n):
        p = os.path.join(tmp, f"m{i}.jpg"); grab(ffmpeg, a.video, i * 0.5, p, scale="96:170")
        im = Image.open(p).convert("L")
        if prev is not None:
            diffs.append(ImageStat.Stat(ImageChops.difference(prev, im)).mean[0])
        prev = im
    W2, H2 = max(600, n * 14), 240
    mc = Image.new("RGB", (W2, H2), (12, 12, 14)); d = ImageDraw.Draw(mc)
    mx = max(diffs) if diffs else 1
    cuts, holds = [], []
    run = 0.0
    for i, v in enumerate(diffs):
        h = int((v / mx) * 170)
        col = (224, 52, 36) if v > 14 else ((90, 90, 100) if v < 1.2 else (120, 180, 120))
        d.rectangle([i * 14 + 2, H2 - 30 - h, i * 14 + 12, H2 - 30], fill=col)
        if v > 14: cuts.append(round((i + 1) * 0.5, 1))
        if v < 1.2:
            run += 0.5
            if run >= 2.0: holds.append(round((i + 1) * 0.5, 1))
        else: run = 0.0
        if i % 4 == 0: d.text((i * 14, H2 - 22), f"{(i+1)*0.5:.0f}", fill=(160, 160, 160))
    d.text((6, 4), "MOTION/0.5s  red=cut  green=alive  grey=near-static", fill=(240, 240, 240))
    mc.save(os.path.join(out, "motion_curve.jpg"), quality=88)

    # ---- audio energy per 0.5s ----
    import re as _re
    astat = sh([ffmpeg, "-nostdin", "-i", a.video, "-af",
                "astats=metadata=1:reset=24,ametadata=print:key=lavfi.astats.Overall.RMS_level",
                "-f", "null", "-"])
    rms = [float(x) for x in _re.findall(r"RMS_level=(-?[\d.]+)", astat) if x != "-inf"][:400]
    if rms:
        W3 = max(600, len(rms) * 6); ac = Image.new("RGB", (W3, 200), (12, 12, 14))
        d = ImageDraw.Draw(ac)
        for i, v in enumerate(rms):
            h = int(max(0, (v + 60) / 60) * 150)
            col = (90, 90, 100) if v < -45 else (120, 180, 220)
            d.rectangle([i * 6, 180 - h, i * 6 + 4, 180], fill=col)
        d.text((6, 4), "AUDIO RMS  grey=dead-air", fill=(240, 240, 240))
        ac.save(os.path.join(out, "audio_curve.jpg"), quality=88)
    dead = sum(1 for v in rms if v < -45) / max(1, len(rms))

    report = {
        "video": a.video, "duration": round(dur, 2),
        "cuts_at": cuts, "cut_rate_per10s": round(len(cuts) / dur * 10, 2),
        "static_holds_at": holds,
        "motion_mean": round(sum(diffs) / max(1, len(diffs)), 2),
        "hook_motion_0_1s": round(max(diffs[:2]) if len(diffs) >= 2 else 0, 2),
        "hook_motion_0_2s": round(max(diffs[:4]) if len(diffs) >= 4 else 0, 2),
        "hook_weakest_halfsec_0_2s": round(min(diffs[:4]) if len(diffs) >= 4 else 0, 2),
        "SWIPE_GATE": ("PASS" if (len(diffs) >= 4 and max(diffs[:2]) >= 20 and min(diffs[:4]) >= 6)
                        else "FAIL — first 2s must carry continuous motion (>=20 peak, no half-sec below 6). 50-60% of swipes happen here."),
        "loop_seam_diff": None,
        "dead_air_ratio": round(dead, 3),
    }
    f0 = os.path.join(tmp, "h0.jpg"); fl = os.path.join(tmp, "last.jpg")
    for back in (0.3, 0.6, 1.0):
        if grab(ffmpeg, a.video, max(0, dur - back), fl): break
    if os.path.exists(fl):
        A = Image.open(f0).convert("L").resize((96, 170)); B = Image.open(fl).convert("L").resize((96, 170))
        report["loop_seam_diff"] = round(ImageStat.Stat(ImageChops.difference(A, B)).mean[0], 1)
    with open(os.path.join(out, "report.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report, indent=1))
    print("EVIDENCE →", out)
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
