"""Rendered video ke frames (10/25/50/75/90%) nikal kar ek contact sheet banata hai.
Ye 3brown1blue ke audit_video ka idea hai: render ke baad jaldi visual check.

Usage: python3 pipeline/audit_frames.py <video.mp4> [props.json]
 - props.json diya to har scene ke MIDDLE par frame (koi scene miss nahi hoga)
 - nahi diya to 10/25/50/75/90% (scene chhoot sakte hain)
Output: output/audit/<name>/sheet.png
"""
import json
import subprocess
import sys
from pathlib import Path

PCTS = [10, 25, 50, 75, 90]


def duration(video: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def sample_times(video: Path, props: Path | None) -> list[float]:
    if props:
        scenes = json.loads(props.read_text(encoding="utf-8"))["project"]["scenes"]
        t, times = 0.0, []
        for s in scenes:
            n = s["durationInFrames"] / 30
            times.append(t + n / 2)  # scene ka beech
            t += n
        return times
    d = duration(video)
    return [d * p / 100 for p in PCTS]


def main(video: Path, props: Path | None):
    times = sample_times(video, props)
    out_dir = Path(__file__).resolve().parent.parent / "output" / "audit" / video.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("f*.png"):
        old.unlink()
    for i, t in enumerate(times):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video),
                        "-frames:v", "1", str(out_dir / f"f{i}.png")], check=True)
    sheet = out_dir / "sheet.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(out_dir / "f%d.png"),
                    "-vf", f"scale=640:-1,tile={len(times)}x1", "-frames:v", "1", str(sheet)], check=True)
    print("sheet:", sheet, f"({len(times)} frames)")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None)
