"""YouTube upload + playlist add (YouTube Data API v3, OAuth refresh token).

Env (GitHub Actions secrets / local env):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Playlist: config/series.json mein youtube_playlist.{en,hi} null ho to pehli baar playlist
ban jaati hai aur ID config mein likh di jaati hai.

NOTE: ye code abhi test nahi hua (credentials nahi hain). Pehle ek private video se test karo.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "series.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]


def _service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def _ensure_playlist(yt, series_id: str, lang: str) -> str | None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    for s in cfg["series"]:
        if s["id"] != series_id:
            continue
        pid = s["youtube_playlist"].get(lang)
        if pid:
            return pid
        name = f"{s['name']} ({lang.upper()})"
        res = yt.playlists().insert(part="snippet,status", body={
            "snippet": {"title": name, "description": f"{s['name']} - daily episodes"},
            "status": {"privacyStatus": "public"},
        }).execute()
        s["youtube_playlist"][lang] = res["id"]
        CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  playlist created: {name} -> {res['id']}")
        return res["id"]
    return None


def upload_one(meta_path: Path) -> str:
    from googleapiclient.http import MediaFileUpload
    meta = json.loads(Path(meta_path).read_text(encoding="utf-8"))
    yt = _service()
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"],
                    "tags": meta["tags"], "categoryId": "27",  # Education
                    "defaultLanguage": "hi" if meta["lang"] == "hi" else "en"},
        "status": {"privacyStatus": meta["privacy"], "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(ROOT / meta["video"]), mimetype="video/mp4",
                            chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    thumb = meta.get("thumbnail")
    if thumb and (ROOT / thumb).exists():
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(ROOT / thumb), mimetype="image/png")).execute()
            print(f"  thumbnail set: {thumb}")
        except Exception as e:  # custom thumbnail ke liye channel verify hona zaroori hai
            print(f"  [warn] thumbnail set fail (channel verify check karo): {e}")
    pid = meta.get("playlist_id") or _ensure_playlist(yt, meta["series"], meta["lang"])
    if pid:
        yt.playlistItems().insert(part="snippet", body={
            "snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}},
        }).execute()
    return vid
