#!/usr/bin/env python3
"""
Stock Media Fetcher Skill (`06-stock-media/stock_fetcher.py`)
Scrapes & caches free, no-copyright media directly in the sandbox:
  1. Mixkit Stock Videos (`https://mixkit.co/free-stock-video/<query>/`) — keyless HD MP4
  2. Pexels Stock Videos/Photos (`PEXELS_API_KEY` if set, automatic fallback to Mixkit/Wikimedia)
  3. Wikimedia Commons (`commons.wikimedia.org/w/api.php`) — keyless real historical/science images
  4. Mixkit No-Copyright Music (`https://mixkit.co/free-stock-music/tag/<mood>/`) — keyless MP3
  5. Mixkit Sound Effects (`https://mixkit.co/free-sound-effects/<query>/`) — keyless MP3
All media is cached under `/home/user/.cache/stock/` so workspace snapshots stay lightweight (<128 MB).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_ROOT = Path("/home/user/.cache/stock")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "clip"


def _download(url: str, dest: Path, timeout: int = 25) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 4096:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=timeout).read()
    dest.write_bytes(data)
    return dest


def fetch_mixkit_video(query: str, index: int = 0) -> Path | None:
    """Search Mixkit free stock videos and download an HD .mp4 clip to .cache/stock/videos/."""
    vid_dir = CACHE_ROOT / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)
    key = f"mixkit-{_slug(query)}-{index}"
    cached = vid_dir / f"{key}.mp4"
    if cached.exists() and cached.stat().st_size > 20_000:
        return cached

    # Try full slug first, then individual words as fallback
    words = [w for w in re.split(r"\s+", query.strip().lower()) if len(w) >= 3]
    candidates = [_slug(query)] + [_slug(w) for w in words] + ["nature", "city", "technology", "stars"]
    seen_urls: list[str] = []

    for slug_q in candidates:
        url = f"https://mixkit.co/free-stock-video/{slug_q}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
            # Prefer -720.mp4 or -vertical.mp4 over -360.mp4
            urls_720 = re.findall(r'https://assets\.mixkit\.co/videos/\d+/[^\s"\'<>]+?(?:720|vertical)\.mp4', html)
            urls_any = re.findall(r'https://assets\.mixkit\.co/videos/\d+/[^\s"\'<>]+?\.mp4', html)
            pool = list(dict.fromkeys(urls_720 + urls_any))
            if pool:
                seen_urls = pool
                break
        except Exception:
            continue

    if not seen_urls:
        return None

    chosen = seen_urls[index % len(seen_urls)]
    try:
        return _download(chosen, cached, timeout=30)
    except Exception as e:
        print(f"[stock] mixkit video download failed ({chosen}): {e}")
        return None


def fetch_pexels_or_mixkit_video(query: str, index: int = 0) -> tuple[Path | None, str]:
    """Use Pexels Video API if PEXELS_API_KEY is set; otherwise seamlessly use Mixkit."""
    api_key = os.environ.get("PEXELS_API_KEY", "").strip()
    if api_key:
        vid_dir = CACHE_ROOT / "videos"
        vid_dir.mkdir(parents=True, exist_ok=True)
        cached = vid_dir / f"pexels-{_slug(query)}-{index}.mp4"
        if cached.exists() and cached.stat().st_size > 20_000:
            return cached, "pexels"
        try:
            q = urllib.parse.quote(query)
            url = f"https://api.pexels.com/videos/search?query={q}&orientation=portrait&per_page=5"
            req = urllib.request.Request(url, headers={"Authorization": api_key, "User-Agent": UA})
            data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
            vids = data.get("videos") or []
            if vids:
                v = vids[index % len(vids)]
                files = sorted(v.get("video_files", []), key=lambda f: abs((f.get("height") or 0) - 1280))
                if files and files[0].get("link"):
                    return _download(files[0]["link"], cached, timeout=30), "pexels"
        except Exception as e:
            print(f"[stock] Pexels fallback to Mixkit ({e})")

    p = fetch_mixkit_video(query, index=index)
    return p, "mixkit"


def fetch_wikimedia_image(query: str, index: int = 0) -> Path | None:
    """Fetch a real historical/science image from Wikimedia Commons (keyless API)."""
    img_dir = CACHE_ROOT / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    cached = img_dir / f"wiki-{_slug(query)}-{index}.jpg"
    if cached.exists() and cached.stat().st_size > 5_000:
        return cached

    q = urllib.parse.quote(f"filetype:bitmap {query}")
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrnamespace=6&gsrsearch={q}&gsrlimit=6&prop=imageinfo&iiprop=url"
        f"&iiurlwidth=1280&format=json"
    )
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "FactShortsPipeline/1.0"})
        res = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
        pages = list((res.get("query", {}).get("pages") or {}).values())
        urls = []
        for p in pages:
            ii = (p.get("imageinfo") or [{}])[0]
            u = ii.get("thumburl") or ii.get("url")
            if u and not u.lower().endswith((".svg", ".tif", ".tiff", ".pdf")):
                urls.append(u)
        if urls:
            chosen = urls[index % len(urls)]
            return _download(chosen, cached, timeout=25)
    except Exception as e:
        print(f"[stock] wikimedia fetch failed for '{query}': {e}")
    return None


def fetch_mixkit_music(mood: str = "cinematic", index: int = 0) -> Path | None:
    """Scrape & download a free no-copyright background music MP3 from Mixkit."""
    mus_dir = CACHE_ROOT / "music"
    mus_dir.mkdir(parents=True, exist_ok=True)
    slug_m = _slug(mood)
    cached = mus_dir / f"mixkit-music-{slug_m}-{index}.mp3"
    if cached.exists() and cached.stat().st_size > 20_000:
        return cached

    for tag in [slug_m, "cinematic", "ambient", "dramatic", "chill"]:
        url = f"https://mixkit.co/free-stock-music/tag/{tag}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
            tracks = list(dict.fromkeys(re.findall(r'https://assets\.mixkit\.co/music/\d+/\d+\.mp3', html)))
            if tracks:
                chosen = tracks[index % len(tracks)]
                return _download(chosen, cached, timeout=30)
        except Exception:
            continue
    return None


def fetch_mixkit_sfx(effect: str = "whoosh", index: int = 0) -> Path | None:
    """Scrape & download a free sound effect MP3 from Mixkit."""
    sfx_dir = CACHE_ROOT / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    slug_e = _slug(effect)
    cached = sfx_dir / f"mixkit-sfx-{slug_e}-{index}.mp3"
    if cached.exists() and cached.stat().st_size > 2_000:
        return cached

    for q in [slug_e, "whoosh", "transition", "click"]:
        url = f"https://mixkit.co/free-sound-effects/{q}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
            sfxs = list(dict.fromkeys(re.findall(r'https://assets\.mixkit\.co/[^\s"\'<>]+?\.(?:mp3|wav)', html)))
            if sfxs:
                chosen = sfxs[index % len(sfxs)]
                return _download(chosen, cached, timeout=20)
        except Exception:
            continue
    return None


def main():
    ap = argparse.ArgumentParser(description="Fetch free stock video, historical images, music & SFX")
    ap.add_argument("--video", help="Search query for Mixkit/Pexels stock video")
    ap.add_argument("--wiki", help="Search query for Wikimedia Commons historical/real image")
    ap.add_argument("--music", help="Mood tag for Mixkit no-copyright music (e.g. cinematic, mystery, ambient)")
    ap.add_argument("--sfx", help="Effect query for Mixkit SFX (e.g. whoosh, click, hit)")
    ap.add_argument("--index", type=int, default=0, help="Result index")
    args = ap.parse_args()

    if args.video:
        p, src = fetch_pexels_or_mixkit_video(args.video, args.index)
        print(f"[video:{src}] {p}")
    if args.wiki:
        p = fetch_wikimedia_image(args.wiki, args.index)
        print(f"[wiki] {p}")
    if args.music:
        p = fetch_mixkit_music(args.music, args.index)
        print(f"[music] {p}")
    if args.sfx:
        p = fetch_mixkit_sfx(args.sfx, args.index)
        print(f"[sfx] {p}")


if __name__ == "__main__":
    main()
