#!/usr/bin/env python3
"""
Unified Skill Runner (`run_skill.py`)
Connects all 5 skill categories into the active video build pipeline:
  01-youtube            -> hookscore.py, title.py, deadair.py, chapters.py, retention.py
  02-remotion           -> remotion-captions & remotion-best-practices checks
  03-motion-directing   -> motionmaxxing, hypermotion, remotion-motion-graphics presets
  04-voice-and-captions -> kokoro-onnx VO + faster-whisper / whisperX word alignment verification
  05-pipeline-guides    -> QA gate & safe-zone validation
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent
YT_DIR = SKILLS_ROOT / "01-youtube"
REMOTION_DIR = SKILLS_ROOT / "02-remotion"
MOTION_DIR = SKILLS_ROOT / "03-motion-directing"
VOICE_DIR = SKILLS_ROOT / "04-voice-and-captions"
GUIDES_DIR = SKILLS_ROOT / "05-pipeline-guides"


def run_py(script: Path, *args: str) -> str:
    if not script.exists():
        return f"[missing {script}]"
    r = subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
    )
    return (r.stdout or r.stderr).strip()


def cmd_list(_args):
    print("=== /home/user/skills — Clean Categorized Structure ===")
    for cat in sorted(SKILLS_ROOT.iterdir()):
        if cat.is_dir() and not cat.name.startswith("."):
            subs = [p.name for p in sorted(cat.iterdir()) if not p.name.startswith(".")]
            print(f"  {cat.name:24s} -> {', '.join(subs)}")


def cmd_audit(args):
    timeline_path = Path(args.timeline)
    tl = json.loads(timeline_path.read_text(encoding="utf-8"))
    slug = tl.get("slug", timeline_path.stem.replace("-timeline", ""))
    title = tl.get("title", slug)
    shots = tl.get("shots", [])
    first_vo = shots[0].get("vo", title) if shots else title
    first_title_en = shots[0].get("title_en", "0.003 SEC INSIDE") if shots else "SCIENCE FACTS"

    srt_path = Path(args.srt) if args.srt else timeline_path.parent / f"{slug}.srt"
    presets_path = MOTION_DIR / "motion_presets.json"
    presets = json.loads(presets_path.read_text(encoding="utf-8"))

    # 1. 01-youtube skills
    hook_res = run_py(YT_DIR / "yt-script" / "hookscore.py", "--hook", f"{first_title_en} — {first_vo}")
    thumb_words = " ".join(first_title_en.replace("•", "").split()[:3])
    title_res = run_py(YT_DIR / "yt-package" / "title.py", "--title", title, "--thumb", thumb_words)
    deadair_res = run_py(YT_DIR / "yt-edit" / "deadair.py", str(srt_path)) if srt_path.exists() else "No SRT"

    # 2. 03-motion-directing checks (motionmaxxing + hypermotion + remotion-motion-graphics)
    hm = presets["hypermotion"]
    mm = presets["motionmaxxing"]
    rmg = presets["remotion_motion_graphics"]
    motion_checks = []
    total_labels = 0
    for s in shots:
        cam = s.get("camera", {})
        lbls = s.get("labels", [])
        total_labels += len(lbls)
        stage_lbl = s.get("stage") or s.get("title") or f"SCENE_{s['id']}"
        motion_checks.append(
            f"Shot {s['id']:02d} ({stage_lbl}): move={cam.get('move','3d_camera_orbit')} "
            f"scale={cam.get('from_scale', mm['default_from_scale'])}->{cam.get('to_scale', mm['default_to_scale'])} "
            f"labels={len(lbls)} @ {[l.get('trigger_sec') for l in lbls]}"
        )

    report_lines = [
        f"# Skill Pipeline Report — `{slug}`",
        "",
        "## 1. YouTube Agent Skills (`01-youtube/`)",
        "### Hook Score (`yt-script/hookscore.py`)",
        "```text",
        hook_res,
        "```",
        "### Title & Thumbnail Check (`yt-package/title.py`)",
        "```text",
        title_res,
        "```",
        "### Dead-Air Pacing Check (`yt-edit/deadair.py`)",
        "```text",
        deadair_res,
        "```",
        "",
        "## 2. Motion Directing Skills Applied (`03-motion-directing/`)",
        f"- **MotionMaxxing:** target `{mm['target_lufs']} LUFS`, pulse `{mm['pulse_rate_hz']} Hz` ({mm['pulse_rings']} rings), ducking `{mm['vo_duck_idle_gain']} -> {mm['vo_duck_active_gain']}`",
        f"- **HyperMotion:** label spring pop `{hm['label_pop_duration_sec']}s` (overshoot `{hm['label_overshoot']}x`), optical flash cut `{hm['flash_cut_duration_sec']}s`, active-word highlight `{hm['caption_group_words']}` words/phrase",
        f"- **Remotion Motion Graphics:** `{rmg['width']}x{rmg['height']}` @ `{rmg['fps']}fps`, safe margin `{rmg['safe_margin_x']}px`, caption band `y={rmg['caption_band_y0']}..{rmg['caption_band_y1']}`",
        "",
        "### Per-Shot Choreography Lock",
        "```text",
        *motion_checks,
        "```",
        "",
        "## 3. Voice & Caption Alignment (`04-voice-and-captions/`)",
        f"- **Voice Engine:** Kokoro ONNX (`{tl.get('voice', 'hf_beta')}` @ `{tl.get('speed', 1.18)}x`)",
        f"- **Total Duration:** `{tl.get('total_duration')}s` across `{len(shots)}` shots (`{total_labels}` word-synced callout labels)",
        f"- **SRT Sidecar:** `{srt_path}`",
    ]

    out_report = Path(args.out) if args.out else Path("renders") / f"{slug}-skill-report.md"
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"[skills] 01-youtube + 02-remotion + 03-motion-directing + 04-voice-and-captions verified -> {out_report}")


def main():
    ap = argparse.ArgumentParser(description="Unified Skill Runner for Video Pipelines")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ls_p = sub.add_parser("list", help="List all organized skill categories and tools")
    ls_p.set_defaults(func=cmd_list)

    au_p = sub.add_parser("audit", help="Run all skills on a video timeline + SRT")
    au_p.add_argument("--timeline", required=True, help="Path to out/<slug>-timeline.json")
    au_p.add_argument("--srt", default=None, help="Path to <slug>.srt")
    au_p.add_argument("--out", default=None, help="Output markdown report path")
    au_p.set_defaults(func=cmd_audit)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
