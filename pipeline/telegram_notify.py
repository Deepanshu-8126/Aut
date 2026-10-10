"""Telegram par video bhejta hai (title + caption + Google Trends CTA).

Env (GitHub Actions secrets / local env):
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

Usage:
  python3 pipeline/telegram_notify.py --video output/x.mp4 --meta output/x.meta.json
  python3 pipeline/telegram_notify.py --text "hello"          # sirf test message

Caption Telegram limit: 1024 chars (sendVideo). Isliye caption ko safe length tak kaat ke
Trends CTA hamesha end mein rakhte hain.
"""
import argparse
import json
import mimetypes
import os
import sys
import urllib.request
import uuid
from pathlib import Path

CAPTION_LIMIT = 1024
TRENDS_CTA = "\n\n🔥 Trending topics dekhne ke liye: https://trends.google.com/trending?geo=IN"
API = "https://api.telegram.org/bot{token}/{method}"


def _env():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        sys.exit("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID set nahi hain")
    return token, chat


def build_caption(title: str, description: str) -> str:
    head = f"🎬 {title.strip()}\n\n"
    room = CAPTION_LIMIT - len(head) - len(TRENDS_CTA)
    desc = description.strip()
    if len(desc) > room:
        desc = desc[: max(room - 1, 0)].rstrip() + "…"
    return head + desc + TRENDS_CTA


def _post(method: str, fields: dict, file_field: tuple | None = None) -> dict:
    token, _ = _env()
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode("utf-8"))
    if file_field:
        name, path = file_field
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{Path(path).name}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n".encode("utf-8")
        )
        parts.append(Path(path).read_bytes())
        parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(parts)
    req = urllib.request.Request(
        API.format(token=token, method=method),
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        res = json.loads(r.read().decode("utf-8"))
    if not res.get("ok"):
        raise RuntimeError(f"Telegram error: {res}")
    return res


def send_text(text: str) -> dict:
    _, chat = _env()
    return _post("sendMessage", {"chat_id": chat, "text": text})


def send_video(video: Path, title: str, description: str) -> dict:
    _, chat = _env()
    caption = build_caption(title, description)
    return _post(
        "sendVideo",
        {"chat_id": chat, "caption": caption, "supports_streaming": "true"},
        file_field=("video", str(video)),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video")
    ap.add_argument("--meta", help="meta.json (title, description)")
    ap.add_argument("--text")
    a = ap.parse_args()
    if a.text:
        send_text(a.text)
        print("text sent")
        return
    if not a.video or not a.meta:
        sys.exit("--video aur --meta dono chahiye (ya --text)")
    meta = json.loads(Path(a.meta).read_text(encoding="utf-8"))
    send_video(Path(a.video), meta["title"], meta.get("description", ""))
    print("video sent")


if __name__ == "__main__":
    main()
