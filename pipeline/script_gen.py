"""Generate a structured video script with Gemini."""
import json
import os
import re
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT = (ROOT / "prompts" / "script_system_prompt.md").read_text(encoding="utf-8")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")




def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    return json.loads(text)


def _load_dotenv():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def generate_script(series_name: str, fmt: str, topic: str, language: str) -> dict:
    _load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable set nahi hai.")


    client = genai.Client(api_key=api_key)
    prompt = (
        SYSTEM_PROMPT.replace("{series_name}", series_name)
        .replace("{format}", fmt)
        .replace("{topic}", topic)
        .replace("{language}", language)
    )
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    script = _extract_json(resp.text)
    validate(script)
    return script


def validate(script: dict) -> None:
    for key in ("title", "scenes"):
        if key not in script:
            raise ValueError(f"script mein '{key}' missing hai")
    if not script["scenes"]:
        raise ValueError("script mein koi scene nahi hai")
    for s in script["scenes"]:
        if not s.get("narration"):
            raise ValueError(f"scene {s.get('id')} mein narration nahi hai")
