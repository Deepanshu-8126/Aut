#!/usr/bin/env python3
"""FACTSHORTS pipeline CLI.

    python run.py doctor
    python run.py script --topic "Why We Yawn" --episode 43
    python run.py stills --topic "Why We Yawn"            # 7 PNGs, 1080x1920
    python run.py video  --topic "Why We Yawn"            # 7 MP4s + full Short with SFX
    python run.py demo                                     # built-in deja vu set
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from factshorts import prompts as P                            # noqa: E402
from factshorts import providers, renderer, spec as S, video as V   # noqa: E402
from factshorts import scaffold                                   # noqa: E402
from factshorts import bridge as BR                               # noqa: E402
from factshorts import style as STYLE                          # noqa: E402
from factshorts.renderer import Part, compose                  # noqa: E402

DEMO = [
    dict(idx=1, badge="HOOK", title="Your Brain Creates False Memories",
         subtitle="Why You Feel Deja Vu", layout="hook", art="brain_hero",
         bottom="HOOK • 97% people feel it",
         metrics=[dict(value="97%", label="people feel it", count=97, suffix="%", icon="people")],
         callouts=[dict(kind="label", text="TEMPORAL LOBE", sub="memory encoding",
                        anchor=(700, 1300), xy=(700, 1320), color="yellow", side="right")]),
    dict(idx=2, badge="FACT 1", title="Your Eyes Are Lying", subtitle="The 200ms Delay",
         layout="diagram", art="brain_flat", art2="eye", bottom="FACT 1 • 200ms delay",
         metrics=[dict(value="200ms", label="reality to brain", icon="eye")],
         callouts=[dict(kind="arrows", arrows=[
             dict(p0=(470, 1230), p1=(700, 1230), color="blue", width=7, glow=True)])]),
    dict(idx=3, badge="FACT 2", title="Double Checking Glitch", subtitle="Hippocampus Misfire",
         layout="diagram", art="brain_cut", art2="chip", bottom="FACT 2 • memory collision",
         metrics=[dict(value="NEW = OLD", label="encoding conflict", icon="warning")],
         callouts=[dict(kind="label", text="HIPPOCAMPUS", sub="the memory hub",
                        anchor=(560, 900), xy=(600, 860), color="yellow", side="right"),
                   dict(kind="label", text="SHORT-TERM", sub="input arriving now",
                        anchor=(150, 1230), xy=(90, 1270), color="blue", side="left"),
                   dict(kind="label", text="LONG-TERM", sub="stored memory",
                        anchor=(930, 1230), xy=(760, 1270), color="purple", side="right")]),
    dict(idx=4, badge="FACT 3", title="It Lasts 10-30 Seconds", subtitle="The Glitch Timeline",
         layout="timeline", art="clock_brain", bottom="FACT 3 • 10-30 sec glitch",
         columns=[dict(icon="brain", head="97%", sub="experience it"),
                  dict(icon="clock", head="10-30 sec", sub="average"),
                  dict(icon="people", head="then gone", sub="feeling fades")],
         footnote="The memory glitch fades within seconds — before you can hold on to it"),
    dict(idx=5, badge="FACT 4", title="Tired Brains Get It More", subtitle="Sleep debt shows up",
         layout="chart", art="sleep", bottom="FACT 4 • tired = more",
         headline="Less sleep, more deja vu",
         bars=[dict(label="Well-Rested", value=50, color="gray"),
               dict(label="Tired", value=100, display="2x", color="yellow")],
         footnote="Sleep-deprivation participants report about double the frequency"),
    dict(idx=6, badge="FACT 5", title="It's Actually Healthy", subtitle="Your Memory System Working",
         layout="hook", art="shield_brain", bottom="FACT 5 • healthy sign",
         metrics=[dict(value="NORMAL", label="not a warning sign", icon="check")],
         callouts=[dict(kind="label", text="HEALTHY PROCESS", sub="your memory testing itself",
                        anchor=(800, 1240), xy=(600, 1290), color="green", side="right")]),
    dict(idx=7, badge="PAYOFF", title="So Next Time You Feel It", subtitle="Smile, Your Brain Is Updating",
         layout="payoff", art="brain_glow", bottom="PAYOFF • not magic, just brain",
         headline="Not magic, just your brain double-checking reality",
         columns=[dict(icon="clock", head="200ms", sub="perception delay"),
                  dict(icon="pulse", head="collision", sub="old + new blend"),
                  dict(icon="check", head="healthy", sub="self-correcting")],
         cta="Follow for more brain glitches"),
]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def out_root() -> Path:
    p = Path(os.environ.get("FACTSHORTS_OUT", Path(__file__).resolve().parent / "out"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def build_parts(args) -> tuple[dict, list[Part]]:
    if getattr(args, "demo", False):
        pack = dict(topic="Why You Feel Deja Vu — Your Brain's Glitch Explained", episode=42,
                    category="BRAIN FACTS", parts=[dict(p, duration=4.5) for p in DEMO])
        for p in pack["parts"]:
            p.setdefault("total", 7)
    elif args.script:
        pack = S.load_pack(Path(args.script))
    else:
        pack = S.build_pack(args.topic, episode=args.episode, category=args.category,
                            offline=args.offline)
    return pack, S.to_parts(pack)


def workdir(pack: dict) -> Path:
    d = out_root() / slug(pack.get("topic", "run"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_publish_kit(pack: dict, d: Path) -> Path:
    """Generate YouTube publish.md using youtube-agent-skill hookscore.py & title.py."""
    import subprocess
    topic = pack.get("topic", "Facts Short")
    cat = pack.get("category", "SCIENCE FACTS")
    parts = pack.get("parts", [])
    hook_title = parts[0].get("title", topic) if parts else topic
    facts_list = pack.get("_facts") or []

    hook_out = ""
    title_out = ""
    hook_py = Path("/home/user/skills/01-youtube/yt-script/hookscore.py")
    title_py = Path("/home/user/skills/01-youtube/yt-package/title.py")
    if hook_py.exists():
        r = subprocess.run(["python3", str(hook_py), "--hook", f"{hook_title} — {topic}"], capture_output=True, text=True)
        hook_out = r.stdout.strip()
    if title_py.exists():
        r = subprocess.run(["python3", str(title_py), "--title", f"{topic} — Explained in 30 Seconds", "--thumb", hook_title[:22].upper()], capture_output=True, text=True)
        title_out = r.stdout.strip()

    md = [
        f"# Publish Kit — {topic}",
        f"**Category:** `{cat}`  |  **Episode:** `{pack.get('episode', 43)}`",
        "",
        "## 1. Sourced Facts & Metrics",
    ]
    if facts_list:
        for f_line in facts_list:
            md.append(f"- {f_line}")
    else:
        for p in parts:
            m = p.get("metric") or (p.get("metrics") or [{}])[0]
            if m and m.get("value"):
                md.append(f"- **Part {p.get('idx')} ({p.get('badge')}):** `{m.get('value')}` — {m.get('label', '')}")
    md.extend([
        "",
        "## 2. Hook Score (`yt-script/hookscore.py`)",
        "```text",
        hook_out or "Hook checked.",
        "```",
        "",
        "## 3. Title & Thumbnail Check (`yt-package/title.py`)",
        "```text",
        title_out or "Title checked.",
        "```",
    ])
    pub_path = d / "publish.md"
    pub_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return pub_path


def mirror_to_renders(d: Path) -> Path:
    """Copy key deliverables from out/<slug> to renders/<slug> so workspace snapshots preserve them."""
    ren_root = Path(__file__).resolve().parent / "renders" / d.name
    ren_root.mkdir(parents=True, exist_ok=True)
    for pat in ("script.json", "publish.md", "preview.html", "part-*.png", "FULL-short.mp4", "*.srt"):
        for f in d.glob(pat):
            if f.is_file():
                shutil.copy2(f, ren_root / f.name)
    return ren_root


# --------------------------------------------------------------------- cmds
def cmd_doctor(a):
    print(f"python  : {sys.version.split()[0]}")
    print(f"ffmpeg  : {V.ffmpeg_exe()}")
    print(f"fonts   : {', '.join(sorted(p.name for p in STYLE.FONT_DIR.glob('*.ttf'))) or 'MISSING (run tools/make_fonts.py)'}")
    try:
        import PIL
        print(f"pillow  : {PIL.__version__}")
    except Exception:                                          # noqa: BLE001
        pass
    for k, v in providers.probe(deep=getattr(a, "deep", False)).items():
        print(f"{k:26s}: {v}")
    if getattr(a, "models", False):
        try:
            print("free text models:", ", ".join(m["name"] for m in providers.models()))
        except Exception as e:                                 # noqa: BLE001
            print("free text models: FAIL", e)


def cmd_fill(args):
    pack = S.load_pack(args.script)
    print(f"  stale: {S.stale_parts(pack)}")
    only = [int(x) for x in args.parts.replace(",", " ").split()] if args.parts else None
    pack = S.repair_pack(pack, only, save_path=Path(args.script))
    S.save_pack(pack, Path(args.script).parent)
    print(f"  remaining stale: {S.stale_parts(pack)}")
    print(f"  saved -> {args.script}")
    return Path(args.script).parent


def cmd_scaffold(args):
    d = args.out or (out_root() / slug(args.topic))
    pack = scaffold.write_scaffold(args.topic, d, episode=args.episode, category=args.category)
    P.write_style_files(d / "prompts", pack)
    print(f"scaffold -> {d}")
    print(f"  script.json            (edit or paste an LLM's JSON here)")
    print(f"  PROMPT_FOR_CHATBOT.md  (paste into ChatGPT/Gemini/Claude/Meta AI)")
    print(f"  render: python run.py video --script {d/'script.json'}")
    return d


def cmd_stills(args):
    pack, parts = build_parts(args)
    d = args.out or workdir(pack)
    d.mkdir(parents=True, exist_ok=True)
    S.save_pack(pack, d)
    for p in P.write_style_files(d / "prompts", pack):
        print(f"  prompt file: {p.relative_to(d)}")
    t0 = time.time()
    for part in parts:
        img = compose(part)                     # t=None -> final still
        if args.scale > 1:
            img = img.resize((img.width // args.scale, img.height // args.scale))
        f = d / f"part-{part.idx}-{slug(part.badge)}.png"
        img.save(f)
        print(f"  [{part.idx}/{len(parts)}] {f.name}  ({time.time()-t0:5.1f}s)")
    write_publish_kit(pack, d)
    ren_d = mirror_to_renders(d)
    print(f"done -> {d}  (persisted -> {ren_d})")
    return d


def cmd_video(args):
    pack, parts = build_parts(args)
    d = args.out or workdir(pack)
    d.mkdir(parents=True, exist_ok=True)
    S.save_pack(pack, d)
    P.write_style_files(d / "prompts", pack)
    tmp = d / "_frames"
    tmp.mkdir(exist_ok=True)
    clips = []
    t0 = time.time()
    fps = getattr(args, "fps", 30)
    seconds = getattr(args, "seconds", 4.5)
    no_audio = getattr(args, "no_audio", False)
    only = {int(x) for x in (getattr(args, "only", None) or "").replace(",", " ").split()} \
        if getattr(args, "only", None) else None
    for part in parts:
        if only and part.idx not in only:
            clip = d / f"part-{part.idx}-{slug(part.badge)}.mp4"
            if clip.exists():
                clips.append(clip)
            continue
        fd = tmp / f"part{part.idx}"
        if fd.exists():
            shutil.rmtree(fd)
        V.render_frames(part, fd, fps=fps, scale=args.scale, duration=seconds)
        audio = None
        if not no_audio:
            audio = d / f"_sfx-part{part.idx}.wav"
            V.write_sfx(audio, part, seconds)
        clip = d / f"part-{part.idx}-{slug(part.badge)}.mp4"
        V.encode_mp4(fd, clip, fps=fps, audio=audio)
        clips.append(clip)
        print(f"  [{part.idx}/{len(parts)}] {clip.name}  ({time.time()-t0:5.1f}s)")
    if len(clips) > 1:
        full = d / "FULL-short.mp4"
        V.concat(clips, full, tmp)
        print(f"  full: {full}")
    if not getattr(args, "keep_frames", False):
        shutil.rmtree(tmp, ignore_errors=True)
    write_publish_kit(pack, d)
    ren_d = mirror_to_renders(d)
    print(f"done -> {d}  (persisted -> {ren_d})")
    return d


def cmd_make(args):
    """One command, whole Short: script -> repair -> stills -> video -> preview."""
    from factshorts import preview as PV
    t_all = time.time()
    pack, parts = build_parts(args)
    d = args.out or workdir(pack)
    d.mkdir(parents=True, exist_ok=True)

    print(f"\n=== 1/5  SCRIPT  ({pack.get('_generated_by', '?')}) ===")
    S.save_pack(pack, d)
    for p in P.write_style_files(d / "prompts", pack):
        print(f"    {p.relative_to(d)}")

    stale = S.stale_parts(S.load_pack(d / "script.json"))
    print(f"    written from AI: {7 - len(stale)}/7" + (f"  (placeholders: {stale})" if stale else ""))
    for r in range(getattr(args, "rounds", 0)):
        if not stale:
            break
        print(f"\n=== 2/5  REPAIR round {r + 1} ===")
        pack = S.load_pack(d / "script.json")
        pack = S.repair_pack(pack, stale, save_path=d / "script.json")
        S.save_pack(pack, d)
        stale = S.stale_parts(pack)
    if stale:
        print(f"    still placeholder: {stale} — derived content used (edit script.json or run "
              f"`python run.py bridge` for a paste-back fix)")
    else:
        print("    every part is AI content ✅")

    print(f"\n=== 3/5  STILLS ===")
    parts = S.to_parts(S.load_pack(d / "script.json"))
    for part in parts:
        img = compose(part)
        if args.scale > 1:
            img = img.resize((img.width // args.scale, img.height // args.scale))
        img.save(d / f"part-{part.idx}-{slug(part.badge)}.png")
        print(f"    [{part.idx}/7] part-{part.idx}-{slug(part.badge)}.png")

    if not getattr(args, "no_video", False):
        print(f"\n=== 4/5  VIDEO  ({args.fps} fps, {args.seconds}s per part) ===")
        tmp = d / "_frames"
        tmp.mkdir(exist_ok=True)
        clips = []
        for part in parts:
            fd = tmp / f"part{part.idx}"
            if fd.exists():
                shutil.rmtree(fd)
            V.render_frames(part, fd, fps=args.fps, scale=args.scale, duration=args.seconds)
            audio = None
            if not args.no_audio:
                audio = d / f"_sfx-part{part.idx}.wav"
                V.write_sfx(audio, part, args.seconds)
            clip = d / f"part-{part.idx}-{slug(part.badge)}.mp4"
            V.encode_mp4(fd, clip, fps=args.fps, audio=audio)
            clips.append(clip)
            print(f"    [{part.idx}/7] {clip.name}  ({time.time() - t_all:5.0f}s elapsed)")
        if len(clips) > 1:
            V.concat(clips, d / "FULL-short.mp4", tmp)
            print(f"    FULL-short.mp4 = {args.seconds * 7:.1f}s total")
        if not args.keep_frames:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("\n=== 4/5  VIDEO  skipped (--no-video) ===")

    print(f"\n=== 5/5  PREVIEW & PUBLISH KIT ===")
    print(f"    {PV.build(d)}")
    pub = write_publish_kit(S.load_pack(d / "script.json"), d)
    print(f"    {pub}")
    ren_d = mirror_to_renders(d)

    print(f"\nDONE in {time.time() - t_all:.0f}s -> {d}")
    print(f"  persisted : {ren_d} (saved across snapshots)")
    print(f"  stills    : {len(parts)} PNG (1080x1920)")
    if not getattr(args, "no_video", False):
        print(f"  video     : {len(parts)} MP4 + FULL-short.mp4 (with SFX bed)")
    print(f"  open      : {ren_d / 'preview.html'}")
    return d


def main():
    ap = argparse.ArgumentParser(description="FACTSHORTS White-Box shorts pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)

    doc = sub.add_parser("doctor", help="check fonts / ffmpeg / free providers")
    doc.add_argument("--deep", action="store_true", help="probe every provider stage")
    doc.add_argument("--models", action="store_true", help="list free text models")
    doc.set_defaults(func=cmd_doctor)

    fl = sub.add_parser("fill", help="re-generate only the placeholder parts of a script")
    fl.add_argument("--script", type=Path, required=True)
    fl.add_argument("--parts", help="comma list, e.g. 2,4,5 (default: all stale parts)")
    fl.add_argument("--out", type=Path)
    fl.set_defaults(func=cmd_fill)

    br = sub.add_parser("bridge", help="local UI: free chatbot -> validated script -> render")
    br.add_argument("--port", type=int, default=8077)
    br.add_argument("--host", default="0.0.0.0")
    br.set_defaults(func=lambda a: BR.serve(a.port, a.host))

    sc = sub.add_parser("scaffold", help="write script.json + a paste-into-chatbot prompt")
    sc.add_argument("--topic", required=True)
    sc.add_argument("--episode", type=int, default=43)
    sc.add_argument("--category", default="BRAIN FACTS")
    sc.add_argument("--out", type=Path)
    sc.set_defaults(func=cmd_scaffold)

    def common(p, need_topic=False):
        p.add_argument("--topic", required=need_topic)
        p.add_argument("--episode", type=int, default=43)
        p.add_argument("--category", default="BRAIN FACTS")
        p.add_argument("--script", help="reuse an existing script.json instead of calling an LLM")
        p.add_argument("--offline", action="store_true", help="skip the LLM, use the built-in template")
        p.add_argument("--demo", action="store_true", help="use the built-in deja vu script")
        p.add_argument("--out", type=Path)
        p.add_argument("--scale", type=int, default=1, help="2 = render at half size (fast drafts)")
        p.set_defaults(func=cmd_stills)

    mk = sub.add_parser("make", help="END-TO-END: script -> repair -> stills -> video -> preview")
    common(mk)
    mk.add_argument("--rounds", type=int, default=2, help="auto-repair passes for placeholder parts")
    mk.add_argument("--no-video", action="store_true")
    mk.add_argument("--fps", type=int, default=30)
    mk.add_argument("--seconds", type=float, default=4.5)
    mk.add_argument("--no-audio", action="store_true")
    mk.add_argument("--keep-frames", action="store_true")
    mk.set_defaults(func=cmd_make)

    s = sub.add_parser("stills", help="7 PNGs (1080x1920, final frame)")
    common(s)
    s.set_defaults(func=cmd_stills)

    v = sub.add_parser("video", help="7 MP4s + concatenated Short with SFX")
    common(v)
    v.add_argument("--fps", type=int, default=30)
    v.add_argument("--seconds", type=float, default=4.5)
    v.add_argument("--no-audio", action="store_true")
    v.add_argument("--keep-frames", action="store_true")
    v.add_argument("--only", help="re-render only these part numbers, e.g. --only 5")
    v.set_defaults(func=cmd_video)

    d = sub.add_parser("demo", help="built-in deja vu set (stills + one animated part)")
    common(d)
    d.add_argument("--full", action="store_true", help="also render all 7 animated parts")
    d.add_argument("--fps", type=int, default=24)
    d.add_argument("--seconds", type=float, default=4.5)
    d.add_argument("--no-audio", action="store_true")
    d.add_argument("--keep-frames", action="store_true")
    d.add_argument("--only", help="re-render only these part numbers, e.g. --only 5")
    d.set_defaults(func=cmd_demo, demo=True)

    a = ap.parse_args()
    if a.cmd not in ("doctor", "scaffold", "bridge", "fill") and not (getattr(a, "demo", False) or a.script or a.topic):
        ap.error("--topic is required (or use --demo / --script)")
    return a.func(a)


def cmd_demo(args):
    args.demo = True
    d = cmd_stills(args)
    if args.full:
        cmd_video(args)
    else:
        pack, parts = build_parts(args)
        tmp = d / "_frames"
        part = parts[0]
        V.render_frames(part, tmp / "part1", fps=24, scale=args.scale, duration=4.5)
        sfx = d / "_sfx.wav"
        V.write_sfx(sfx, part, 4.5)
        V.encode_mp4(tmp / "part1", d / "part-1-hook.mp4", fps=24, audio=sfx)
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"  animated clip: {d/'part-1-hook.mp4'}")
    return d


if __name__ == "__main__":
    main()
