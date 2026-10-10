"""Render se pehle props JSON check karta hai (galat JSON se render fail hota hai).

Usage: python3 pipeline/validate_props.py remotion/props_lesson.json
Exit 0 = ok, 1 = errors.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    "TitleCard": ["title"],
    "SummaryList": ["items"],
    "MathVisualizer": ["formula"],
    "CodeExplainer": ["code"],
    "TypingCode": ["code"],
    "StatChart": ["title", "kind"],
    "TerminalRun": ["command", "output"],
    "TerminalSplit": ["leftPane"],
    "ComparisonCard": ["leftPoints", "rightPoints"],
    "ManimClip": ["src"],
    "OutroCard": [],
    "ArchitectureFlow": ["steps"],
    "ClassifierCard": [],
    "ClusterGrid": [],
    "BrowserSteps": ["steps"],
    "ArrayViz": ["values", "steps"],
    "TreeViz": ["root", "nodes", "steps"],
    "GraphViz": ["nodes", "edges", "steps"],
    "StackQueueViz": ["kind", "steps"],
    "DiagramFlow": ["nodes", "edges", "steps"],
    "CodeExplainer": ["code"],
}


def validate(props: dict) -> list[str]:
    errs = []
    p = props.get("project", props)
    scenes = p.get("scenes") or []
    if not scenes:
        errs.append("scenes khali hain")
    if p.get("aspectRatio") not in ("16:9", "9:16"):
        errs.append(f"aspectRatio galat: {p.get('aspectRatio')}")
    for i, s in enumerate(scenes, 1):
        tag = f"scene {i} ({s.get('id')})"
        typ = s.get("type")
        if typ not in REQUIRED:
            errs.append(f"{tag}: unknown type '{typ}'")
            continue
        props_ = s.get("props") or {}
        for key in REQUIRED[typ]:
            if not props_.get(key):
                errs.append(f"{tag}: {typ} mein '{key}' missing")
        dur = s.get("durationInFrames") or 0
        if dur <= 0:
            errs.append(f"{tag}: durationInFrames 0 ya missing")
        if s.get("narration") and not s.get("words"):
            errs.append(f"{tag}: narration hai lekin word timing nahi (sync nahi hoga)")
        if s.get("audioFile") and not (ROOT / "remotion" / "public" / s["audioFile"]).exists():
            errs.append(f"{tag}: audio file nahi mili: {s['audioFile']}")
        if typ == "ManimClip" and props_.get("src") and not (ROOT / "remotion" / "public" / props_["src"]).exists():
            errs.append(f"{tag}: clip nahi mili: {props_['src']}")
        dsec = (dur / 30) if dur else 0
        for pp in s.get("popups", []):
            if pp.get("at", 0) > dsec:
                errs.append(f"{tag}: popup '{pp.get('text')}' scene ke bahar hai")
    return errs


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errs = validate(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print("VALIDATION OK")
