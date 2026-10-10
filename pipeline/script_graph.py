"""LangGraph script workflow: draft -> lint -> critique -> repair (loop) -> save.

Har series / topic / language ke liye same graph. Teaching rules prompts/gemini_teacher_prompt.md mein hain.

Usage:
  GEMINI_API_KEY=... python3 pipeline/script_graph.py --series java-100-days --day 2 --topic "Variables" --lang en
  python3 pipeline/script_graph.py --series java-100-days --day 1 --lang en --mock tests/lesson_java_100_days_d001_en.json

--mock: LLM ki jagah ek fixed JSON file use karta hai (graph structure test ke liye, koi API call nahi).
"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_to_lesson import build_prompt, gemini_json, lint  # noqa: E402

from langgraph.graph import END, StateGraph  # noqa: E402

MAX_ROUNDS = 3
CRITIQUE_PROMPT = """You are a strict reviewer of a beginner programming lesson script.
Check the JSON below against these rules and return ONLY JSON: {"issues": ["..."]}.
Rules:
1. Concept before code: scenes 1-3 explain the idea (what, why, analogy) before any code.
2. Every new term (class, object, JVM, compiler, variable, method...) is defined in plain words the first time it appears, with an analogy.
3. Each scene is one idea, 25-45 words, spoken, no jargon dump.
4. Code is correct and runnable, output matches what the code prints.
5. Camera keyframes (remotion.camera) zoom on the right word and line; zoom out for diagrams.
6. Ends with recap and a practice task.
Empty list if everything passes.

LESSON JSON:
"""

REPAIR_PROMPT = """Fix the lesson JSON below. Keep the same schema and scene types. Fix these problems:
{problems}

Return ONLY the full corrected JSON.

LESSON JSON:
{lesson}
"""


class S(TypedDict, total=False):
    topic: str
    series_name: str
    series_id: str
    day: int
    lang: str
    key: str
    lesson: dict
    errors: list
    issues: list
    rounds: int
    status: str


def make_graph(llm):
    """llm(prompt: str) -> dict. Gemini ya mock dono yahi interface dete hain."""

    def draft(s: S) -> dict:
        prompt = build_prompt(s["topic"], s["series_name"], s["lang"], s["day"])
        return {"lesson": llm(prompt), "rounds": 0}

    def check_lint(s: S) -> dict:
        return {"errors": lint(s["lesson"], s["lang"])}

    def critique(s: S) -> dict:
        body = json.dumps(s["lesson"], ensure_ascii=False)
        res = llm(CRITIQUE_PROMPT + body)
        return {"issues": [str(x) for x in res.get("issues", [])]}

    def repair(s: S) -> dict:
        problems = s.get("errors", []) + s.get("issues", [])
        prompt = REPAIR_PROMPT.format(problems="\n".join(f"- {p}" for p in problems),
                                      lesson=json.dumps(s["lesson"], ensure_ascii=False))
        return {"lesson": llm(prompt), "rounds": s.get("rounds", 0) + 1}

    def save(s: S) -> dict:
        name = f"{s['series_id'].replace('-', '_')}_d{s['day']:03d}_{s['lang']}"
        path = ROOT / "tests" / f"lesson_{name}.json"
        path.write_text(json.dumps(s["lesson"], ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": f"saved {path.relative_to(ROOT)}"}

    def give_up(s: S) -> dict:
        return {"status": "failed: " + "; ".join(s.get("errors", []) + s.get("issues", []))[:500]}

    def after_lint(s: S) -> str:
        if s.get("errors"):
            return "repair" if s.get("rounds", 0) < MAX_ROUNDS else "give_up"
        return "critique"

    def after_critique(s: S) -> str:
        if s.get("issues"):
            return "repair" if s.get("rounds", 0) < MAX_ROUNDS else "give_up"
        return "save"

    g = StateGraph(S)
    g.add_node("draft", draft)
    g.add_node("lint", check_lint)
    g.add_node("critique", critique)
    g.add_node("repair", repair)
    g.add_node("save", save)
    g.add_node("give_up", give_up)
    g.set_entry_point("draft")
    g.add_edge("draft", "lint")
    g.add_conditional_edges("lint", after_lint, {"repair": "repair", "critique": "critique", "give_up": "give_up"})
    g.add_conditional_edges("critique", after_critique, {"repair": "repair", "save": "save", "give_up": "give_up"})
    g.add_edge("repair", "lint")
    g.add_edge("save", END)
    g.add_edge("give_up", END)
    return g.compile()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", required=True, help="series id, jaise java-100-days")
    ap.add_argument("--series-name", default=None)
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--topic", default=None)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--mock", default=None, help="LLM ki jagah ye JSON file (test)")
    a = ap.parse_args()

    topic, name = a.topic, a.series_name
    if not topic or not name:
        cfg = json.loads((ROOT / "config" / "series.json").read_text(encoding="utf-8"))
        sr = next(x for x in cfg["series"] if x["id"] == a.series)
        name = name or sr["name"]
        if not topic:
            cur = json.loads((ROOT / sr["curriculum"]).read_text(encoding="utf-8"))["topics"]
            topic = cur[a.day - 1]["topic"]

    if a.mock:
        fixed = json.loads(Path(a.mock).read_text(encoding="utf-8"))
        llm = lambda prompt: fixed  # noqa: E731
    else:
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            raise SystemExit("GEMINI_API_KEY nahi hai (ya --mock use karo)")
        llm = lambda prompt: gemini_json(prompt, key)  # noqa: E731

    app = make_graph(llm)
    out = app.invoke({"topic": topic, "series_name": name, "series_id": a.series, "day": a.day, "lang": a.lang})
    print(out.get("status"), "| rounds:", out.get("rounds", 0))


if __name__ == "__main__":
    main()
