#!/usr/bin/env python3
"""CLI wrapper: python tools/make_preview.py --run out/<topic-slug>"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from factshorts.preview import build      # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True)
    print(f"wrote {build(ap.parse_args().run)}")
