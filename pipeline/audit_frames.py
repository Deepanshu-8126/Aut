"""Rendered video ke frames (10/25/50/75/90%) nikal kar ek contact sheet banata hai.
Ye 3brown1blue ke audit_video ka idea hai: render ke baad jaldi visual check.

Usage: python3 pipeline/audit_frames.py <video.mp4>
Output: output/audit/<name>/sheet.png
"""
import subprocess
import sys
from pathlib import Path

PCTS = [10, 25, 50, 75, 90]


def duration(video: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main(video: Path):
    d = duration(video)
    out_dir = Path(__file__).resolve().parent.parent / "output" / "audit" / video.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    for i, p in enumerate(PCTS):
        f = out_dir / f"f{i}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d * p / 100:.2f}", "-i", str(video),
                        "-frames:v", "1", str(f)], check=True)
        frames.append(f)
    sheet = out_dir / "sheet.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(out_dir / "f%d.png"),
                    "-vf", f"scale=640:-1,tile={len(PCTS)}x1", "-frames:v", "1", str(sheet)], check=True)
    print("sheet:", sheet)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
