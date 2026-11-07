#!/usr/bin/env python3
"""
PRE-FLIGHT GRADER v1 — fair, research-based shorts audit (docs/VIRAL_GRADER_RESEARCH.md)
Usage:
  python3 preflight.py --video out.mp4 --title "..." [--desc "..."] [--hashtags "#a #b"]
                       [--keyword antarctica] [--ffmpeg /path/ffmpeg] [--ffprobe /path/ffprobe]
Scores 0-100:  HOOK 30 | RETENTION 35 | PACKAGING 25 | TECH 10
Verdict: >=75 SHIP | 60-74 FIX | <60 KILL
Honesty: predicts FREEZE-RISK, never guarantees virality.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout + r.stderr

def find_tool(name, override):
    if override and os.path.exists(override): return override
    p = shutil.which(name)
    if p: return p
    for c in (f"/var/tmp/ffstatic/{name}", f"/usr/local/bin/{name}"):
        if os.path.exists(c): return c
    sys.exit(f"ERROR: {name} not found; pass --{name}")

def probe(ffprobe, video):
    out = sh([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", video])
    return json.loads(out)

def extract_frame(ffmpeg, video, t, path, scale=None):
    cmd = [ffmpeg, "-nostdin", "-y", "-ss", str(t), "-i", video, "-frames:v", "1"]
    if scale: cmd += ["-vf", f"scale={scale}"]
    cmd += [path]
    sh(cmd)
    return os.path.exists(path)

def frame_stats(path):
    from PIL import Image, ImageFilter, ImageStat
    im = Image.open(path).convert("L")
    st = ImageStat.Stat(im)
    edges = im.filter(ImageFilter.FIND_EDGES)
    est = ImageStat.Stat(edges)
    return {"mean": st.mean[0], "std": st.stddev[0], "edge": est.mean[0]}

def frame_diff(p1, p2):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p1).convert("L").resize((96, 170))
    b = Image.open(p2).convert("L").resize((96, 170))
    return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", default="")
    ap.add_argument("--hashtags", default="")
    ap.add_argument("--keyword", default="")
    ap.add_argument("--ffmpeg", default=None)
    ap.add_argument("--ffprobe", default=None)
    a = ap.parse_args()
    ffmpeg = find_tool("ffmpeg", a.ffmpeg); ffprobe = find_tool("ffprobe", a.ffprobe)
    tmp = tempfile.mkdtemp(prefix="preflight_")
    checks = []   # (section, name, points_got, points_max, note)

    meta = probe(ffprobe, a.video)
    dur = float(meta["format"]["duration"])
    vstream = next(s for s in meta["streams"] if s["codec_type"] == "video")
    wpx, hpx = int(vstream["width"]), int(vstream["height"])
    fps = eval(vstream.get("avg_frame_rate", "30/1"))

    # ---------------- HOOK (30) : proxies for viewed-vs-swiped ----------------
    f0 = os.path.join(tmp, "f0.jpg"); f05 = os.path.join(tmp, "f05.jpg"); f1 = os.path.join(tmp, "f1.jpg")
    extract_frame(ffmpeg, a.video, 0.03, f0); extract_frame(ffmpeg, a.video, 0.5, f05); extract_frame(ffmpeg, a.video, 1.0, f1)
    s0 = frame_stats(f0)
    # 1. first frame contrast/readability (first frame IS the thumbnail in feed)
    pts = 10 if (s0["std"] > 45 and s0["edge"] > 8) else (6 if s0["std"] > 28 else 2)
    checks.append(("HOOK", "First-frame punch (contrast+detail)", pts, 10,
                   f"std={s0['std']:.0f} edge={s0['edge']:.1f} (need std>45, edge>8)"))
    # 2. motion inside 0-1s (pattern interrupt — static open = swipe)
    d01 = frame_diff(f0, f05); d02 = frame_diff(f05, f1)
    mv = max(d01, d02)
    pts = 10 if mv > 6 else (6 if mv > 2.5 else 1)
    checks.append(("HOOK", "Motion in first second", pts, 10, f"maxdiff={mv:.1f} (need >6)"))
    # 3. not too dark / not blown at open
    pts = 5 if 25 < s0["mean"] < 215 else 2
    checks.append(("HOOK", "First-frame exposure", pts, 5, f"mean={s0['mean']:.0f}"))
    # 4. hook text/title promise appears early — proxy: edge density jump by 1s (text adds edges)
    s1 = frame_stats(f1)
    pts = 5 if s1["edge"] >= s0["edge"] * 0.8 else 2
    checks.append(("HOOK", "Visual info holds through 1s", pts, 5, f"edge 0s={s0['edge']:.1f} 1s={s1['edge']:.1f}"))

    # ---------------- RETENTION (35) : completion proxies ----------------
    # 5. duration band
    if dur <= 21: pts, note = 10, f"{dur:.1f}s — single-concept band (loop>100% possible)"
    elif dur <= 46: pts, note = 8, f"{dur:.1f}s — ok band, needs mid-video re-hooks"
    elif dur <= 60: pts, note = 5, f"{dur:.1f}s — long; completion% hard"
    else: pts, note = 0, f"{dur:.1f}s — not a short"
    checks.append(("RETENTION", "Duration band", pts, 10, note))
    # 6. static-hold scan: sample every 0.5s, find runs of near-zero change >2.5s
    times = [round(t * 0.5, 2) for t in range(int(dur * 2) - 1)]
    paths = []
    for i, t in enumerate(times):
        p = os.path.join(tmp, f"s{i:03d}.jpg")
        extract_frame(ffmpeg, a.video, t, p, scale="96:170")
        paths.append(p)
    run, worst, cuts = 0.0, 0.0, 0
    for i in range(1, len(paths)):
        d = frame_diff(paths[i - 1], paths[i])
        if d < 1.2: run += 0.5; worst = max(worst, run)
        else: run = 0.0
        if d > 14: cuts += 1
    pts = 15 if worst < 1.5 else (9 if worst < 2.5 else 3)
    checks.append(("RETENTION", "No static holds (NO STATIC HOLDS law)", pts, 15,
                   f"longest frozen stretch={worst:.1f}s (need <1.5s)"))
    # 7. pacing — visual events per 10s
    rate = cuts / dur * 10
    pts = 5 if rate >= 2 else (3 if rate >= 1 else 1)
    checks.append(("RETENTION", "Pacing (hard visual events)", pts, 5, f"{cuts} cuts, {rate:.1f}/10s (need >=2)"))
    # 8. loop seam — last frame vs first frame
    fl = os.path.join(tmp, "fl.jpg")
    for back in (0.3, 0.6, 1.0, 1.5):
        if extract_frame(ffmpeg, a.video, max(0, dur - back), fl): break
    seam = frame_diff(f0, fl) if os.path.exists(fl) else 99
    pts = 5 if seam < 18 else (3 if seam < 35 else 1)
    checks.append(("RETENTION", "Loop seam (ending→opening)", pts, 5, f"diff={seam:.1f} (lower=smoother loop)"))

    # ---------------- PACKAGING (25) : title is king ----------------
    tl = len(a.title)
    pts = 8 if 40 <= tl <= 75 else (5 if 25 <= tl <= 90 else 2)
    checks.append(("PACKAGING", "Title length", pts, 8, f"{tl} chars (ideal 40-75)"))
    curio = sum([bool(re.search(r"\?", a.title)), bool(re.search(r"\d", a.title)),
                 bool(re.search(r"\b(this|why|how|what|never|no one|nobody|secret|hidden|still|something)\b", a.title, re.I)),
                 bool(re.search(r"[—–-]", a.title))])
    pts = 7 if curio >= 2 else (4 if curio == 1 else 1)
    checks.append(("PACKAGING", "Curiosity markers in title", pts, 7, f"{curio}/4 markers (?, number, trigger-word, dash)"))
    kw = a.keyword.lower().strip()
    if kw:
        hit_t = kw in a.title.lower(); hit_d = kw in a.desc.lower()
        pts = 5 if hit_t else (3 if hit_d else 0)
        checks.append(("PACKAGING", "Primary keyword placement", pts, 5,
                       f"'{kw}' in title={hit_t} desc={hit_d} (seeds the right test audience)"))
    else:
        checks.append(("PACKAGING", "Primary keyword placement", 2, 5, "no --keyword given; cannot verify seeding"))
    tags = re.findall(r"#\w+", (a.hashtags + " " + a.desc))
    n = len(tags); has_shorts = any(t.lower() == "#shorts" for t in tags)
    pts = 5 if (1 <= n <= 5 and has_shorts) else (3 if 1 <= n <= 8 else (0 if n > 15 else 1))
    checks.append(("PACKAGING", "Hashtags (3-5 incl #shorts)", pts, 5, f"{n} tags, #shorts={has_shorts} (>15 voids ALL)"))

    # ---------------- TECH (10) ----------------
    pts = 4 if (wpx, hpx) == (1080, 1920) else (2 if hpx > wpx else 0)
    checks.append(("TECH", "Resolution 1080x1920", pts, 4, f"{wpx}x{hpx} @ {fps:.0f}fps"))
    loud = sh([ffmpeg, "-nostdin", "-i", a.video, "-af", "ebur128=peak=true", "-f", "null", "-"])
    ms = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", loud); mps = re.findall(r"Peak:\s*(-?[\d.]+)\s*dBFS", loud)
    lufs = float(ms[-1]) if ms else None; peak = float(mps[-1]) if mps else None
    pts = 4 if (lufs and -17 <= lufs <= -10) else 2
    checks.append(("TECH", "Loudness (-14 LUFS target)", pts, 4, f"I={lufs} LUFS"))
    pts = 2 if (peak is not None and peak <= -0.8) else 0
    checks.append(("TECH", "True peak <= -1 dB", pts, 2, f"peak={peak} dBFS"))

    # ---------------- REPORT ----------------
    total = sum(c[2] for c in checks); mx = sum(c[3] for c in checks)
    score = round(total / mx * 100)
    verdict = "SHIP ✅" if score >= 75 else ("FIX 🔧" if score >= 60 else "KILL ❌")
    print("=" * 74)
    print(f"PRE-FLIGHT GRADER v1   |   {os.path.basename(a.video)}   |   {dur:.1f}s")
    print("=" * 74)
    sec = None
    for s, name, p, pm, note in checks:
        if s != sec: print(f"\n[{s}]"); sec = s
        flag = "✅" if p == pm else ("⚠️ " if p >= pm * 0.5 else "❌")
        print(f"  {flag} {name:<42} {p:>2}/{pm:<2}  {note}")
    print("\n" + "=" * 74)
    print(f"SCORE: {score}/100   →   VERDICT: {verdict}")
    print("=" * 74)
    print("""
MANUAL GATES (machine can't judge — tick before upload):
  [ ] TOPIC GATE: winner-DNA match? real search demand? gap not saturation?
  [ ] Title does NOT answer its own question (no answer-leak)
  [ ] Spoken keyword lands in first 2s of VO (YT transcribes)
  [ ] HUMAN 3-SECOND TEST: 4/5 people ask "phir kya hua?"
HONESTY: this predicts freeze-risk only. The real judge is the seed pool @72h.
Log actual results in docs/GRADER_LOG.md so the grader learns YOUR channel.""")
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
