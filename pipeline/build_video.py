"""One-command lesson video builder (Remotion engine).

Steps: lesson JSON -> Remotion props (to_remotion.py) -> validate -> render MP4 -> audit frames.
Har step fail hone par ruk jaata hai aur error dikhata hai.

Usage:
  python3 pipeline/build_video.py tests/lesson_python_lists.json --name lists_v5 --lang en --theme light-grid
  python3 pipeline/build_video.py tests/lesson_python_tuples.json --name tuples_v5 --no-audit

Output: output/remotion/<name>.mp4 (+ output/audit/<name>/ if audit on)
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "pipeline"
REMOTION = ROOT / "remotion"
OUT = ROOT / "output" / "remotion"


def step(title: str, cmd: list[str], cwd: Path) -> None:
    print(f"\n==> {title}", flush=True)
    t0 = time.time()
    is_win = sys.platform == "win32"
    shell = is_win and (cmd[0] in ["npm", "npx", "node", "remotion"] or any("remotion" in x for x in cmd[:2]))
    res = subprocess.run(cmd, cwd=cwd, shell=shell)
    if res.returncode != 0:
        print(f"!! FAILED: {title} (exit {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)
    print(f"   ok ({time.time() - t0:.0f}s)", flush=True)


def comp_for(props: Path) -> str:
    """9:16 props -> Shorts composition (1080x1920), warna Landscape (1920x1080)."""
    proj = json.loads(props.read_text(encoding="utf-8")).get("project", {})
    return "Shorts" if proj.get("aspectRatio") == "9:16" else "Landscape"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("lesson", help="lesson JSON (tests/*.json)")
    ap.add_argument("--name", required=True, help="output name, e.g. lists_v5")
    ap.add_argument("--lang", default="en", choices=["en", "hi"])
    ap.add_argument("--theme", default="light-grid", choices=["light-grid", "dark-vdo"])
    ap.add_argument("--voice", default="hf_beta", help="Kokoro voice (hf_beta, hm_omega)")
    ap.add_argument("--fast", action="store_true", help="Fast mode: skip stills QA & frame audit for maximum speed")
    ap.add_argument("--no-audit", action="store_true", help="frame audit skip karo")
    ap.add_argument("--skip-qa", action="store_true", help="layout QA gate skip karo (default: ON, fail par render ruk jaata hai)")
    a = ap.parse_args()

    if a.fast:
        a.skip_qa = True
        a.no_audit = True

    if not (REMOTION / "node_modules").exists():
        step("0/4 npm install (remotion deps)", ["npm", "install", "--no-audit", "--no-fund", "--prefer-offline"], REMOTION)

    props = REMOTION / f"props_{a.name}.json"
    mp4 = OUT / f"{a.name}.mp4"
    OUT.mkdir(parents=True, exist_ok=True)

    step("1/4 Lesson -> Remotion props (TTS + word timing)",
         [sys.executable, str(PIPE / "to_remotion.py"), a.lesson, a.lang, str(props),
          "--theme", a.theme, "--voice", a.voice], ROOT)
    step("2/4 Validate props",
         [sys.executable, str(PIPE / "validate_props.py"), str(props)], ROOT)
    if not a.skip_qa:
        step("2b/4 Layout QA gate (stills, blank/overflow check)",
             [sys.executable, str(PIPE / "qa_gate.py"), str(props), a.name, "--composition", comp_for(props)], ROOT)

    # High-speed optimized Remotion render
    is_win = sys.platform == "win32"
    concurrency = "4" if is_win else "2"
    render_cmd = [
        "npx", "remotion", "render", comp_for(props), str(mp4),
        f"--props={props.name}",
        f"--concurrency={concurrency}",
        "--jpeg-quality=85",
        "--pixel-format=yuv420p",
        "--log=warn"
    ]
    if is_win:
        render_cmd.append("--gl=angle")
    step("3/4 Render MP4 (High-Speed Remotion Engine)", render_cmd, REMOTION)

    if not a.no_audit:
        step("4/4 Frame audit",
             [sys.executable, str(PIPE / "audit_frames.py"), str(mp4), str(props)], ROOT)

    print(f"\nDONE -> {mp4.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
