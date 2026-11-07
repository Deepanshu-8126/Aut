#!/usr/bin/env python3
"""Batch mode: render a whole week of Shorts from config/topics.json.

    python tools/batch.py --limit 3 --video
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--episode", type=int, default=50, help="first episode number")
    a = ap.parse_args()
    topics = json.loads((ROOT / "config" / "topics.json").read_text())["topics"]
    if a.limit:
        topics = topics[:a.limit]
    for i, t in enumerate(topics):
        cmd = [sys.executable, str(ROOT / "run.py"), "video" if a.video else "stills",
               "--topic", t, "--episode", str(a.episode + i)]
        print(f"\n=== {t}")
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
