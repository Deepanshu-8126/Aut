"""Status dashboard: ek HTML page jo dikhata hai ki kya set hai, kya chal raha hai, kya missing hai.

Usage: python3 pipeline/dashboard.py   -> output/dashboard.html kholo (browser mein)
Secret values kabhi nahi dikhte, sirf "SET" ya "MISSING".
"""
import html
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IST = timezone(timedelta(hours=5, minutes=30))

KEYS = [
    ("GEMINI_API_KEY", "Script banane ke liye (Gemini AI)", "GitHub Secrets"),
    ("YT_CLIENT_ID", "YouTube upload ke liye (Google app)", "GitHub Secrets"),
    ("YT_CLIENT_SECRET", "YouTube upload ke liye (Google app)", "GitHub Secrets"),
    ("YT_REFRESH_TOKEN", "YouTube upload ke liye (login)", "GitHub Secrets"),
    ("HF_TOKEN", "Hindi awaaz ke liye (Hugging Face)", "GitHub Secrets"),
    ("TELEGRAM_BOT_TOKEN", "Telegram par notification ke liye", "GitHub Secrets"),
    ("TELEGRAM_CHAT_ID", "Telegram chat ka ID", "GitHub Secrets"),
]

PIPELINE = [
    ("1. Topic", "Series ka agla topic (config/curriculum ya chat se)"),
    ("2. Script", "Gemini AI se teacher-style script (en/hi)"),
    ("3. Awaaz + timing", "Narration aur word-by-word sync"),
    ("4. QA gate", "Layout check: blank/overflow frames pakdta hai"),
    ("5. Render", "Remotion se MP4 banana"),
    ("6. Thumbnail", "Auto thumbnail (series ke color/motif ke saath)"),
    ("7. Upload + playlist", "YouTube par upload, sahi playlist mein"),
]


def env_status(name: str) -> bool:
    if os.environ.get(name):
        return True
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith(name + "=") and line.split("=", 1)[1].strip():
                return True
    return False


def next_run(slot: str, now: datetime) -> str:
    hh, mm = (int(x) for x in slot.split(":"))
    t = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if t <= now:
        t += timedelta(days=1)
    return t.strftime("%d %b, %H:%M IST")


def badge(text: str, color: str) -> str:
    return f'<span class="badge" style="background:{color}">{html.escape(text)}</span>'


def main() -> None:
    now = datetime.now(IST)
    cfg = json.loads((ROOT / "config/series.json").read_text(encoding="utf-8"))
    state_path = ROOT / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"done": []}
    done = list(reversed(state.get("done", [])))[:12]

    env_rows = []
    missing = 0
    for key, why, where in KEYS:
        ok = env_status(key)
        missing += 0 if ok else 1
        env_rows.append(
            f"<tr><td><code>{key}</code></td><td>{html.escape(why)}</td>"
            f"<td>{badge('SET', '#16a34a') if ok else badge('MISSING', '#dc2626')}</td>"
            f"<td class='muted'>{where}</td></tr>")

    series_cards = []
    for s in cfg["series"]:
        on = s.get("enabled")
        fmt = "Long video" if s.get("format") == "long" else "Shorts"
        pl = s.get("youtube_playlist", {})
        pl_txt = " &middot; ".join(
            f"{l.upper()}: {'playlist set' if pl.get(l) else 'auto-create on upload'}" for l in s.get("langs", []))
        series_cards.append(f"""
        <div class="card" style="border-top:6px solid {s.get('accent', '#64748b')}">
          <div class="row"><h3>{html.escape(s['name'])}</h3>
            {badge('ON', '#16a34a') if on else badge('OFF', '#6b7280')}</div>
          <div class="chips">
            {badge(fmt, '#0f172a')}
            {badge('Roz ' + s.get('daily_slot_ist', '--:--') + ' IST', '#334155')}
            {badge('Langs: ' + ', '.join(s.get('langs', [])), '#334155')}
          </div>
          <p class="muted">Agla run: {next_run(s.get('daily_slot_ist', '00:00'), now) if on else 'band hai (enabled: false)'}</p>
          <p class="muted small">Playlist: {pl_txt}</p>
          <p class="muted small">Curriculum: {html.escape(s.get('curriculum', '-'))}</p>
        </div>""")

    run_rows = []
    for r in done:
        is_test = "test" in (r.get("topic") or "").lower()
        tag = badge("TEST", "#a16207") if is_test else badge("REAL", "#16a34a")
        run_rows.append(
            f"<tr><td>{html.escape(r.get('at', '')[:16])}</td><td>{html.escape(r.get('series', ''))}</td>"
            f"<td>{html.escape(r.get('topic', ''))}</td><td>{', '.join(r.get('langs', []))}</td><td>{tag}</td></tr>")
    if not run_rows:
        run_rows.append("<tr><td colspan='5' class='muted'>Abhi koi run nahi hua.</td></tr>")

    steps = []
    for i, (name, desc) in enumerate(PIPELINE):
        steps.append(f"<div class='step'><div class='num'>{i + 1}</div><b>{html.escape(name)}</b>"
                     f"<div class='muted small'>{html.escape(desc)}</div></div>")

    summary_color = "#16a34a" if missing == 0 else "#dc2626"
    summary = ("Sab keys set hain. Ab daily run chal sakta hai." if missing == 0
               else f"{missing} key(s) missing hain, isliye poora automatic run abhi nahi chalega.")

    page = f"""<!doctype html><html lang="hi"><head><meta charset="utf-8">
<title>YT Automator Dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#f8fafc;color:#0f172a;margin:0;padding:28px}}
h1{{margin:0 0 4px}} h2{{margin:28px 0 12px}} h3{{margin:0}}
.muted{{color:#64748b}} .small{{font-size:13px}}
.banner{{padding:14px 18px;border-radius:12px;color:#fff;font-weight:600;background:{summary_color}}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
.card{{background:#fff;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.row{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.chips{{margin:10px 0;display:flex;flex-wrap:wrap;gap:6px}}
.badge{{display:inline-block;color:#fff;font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid #e2e8f0;font-size:14px}}
th{{background:#f1f5f9}} code{{background:#f1f5f9;padding:2px 6px;border-radius:6px}}
.flow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.step{{background:#fff;border-radius:12px;padding:14px;border-left:5px solid #2563eb}}
.num{{width:26px;height:26px;border-radius:50%;background:#2563eb;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;margin-bottom:6px}}
.box{{background:#eff6ff;border-radius:12px;padding:14px 18px;font-size:14px;line-height:1.6}}
</style></head><body>
<h1>YT Automator &mdash; Status</h1>
<div class="muted">Abhi ka time: {now.strftime('%d %b %Y, %H:%M IST')}</div>
<h2>Summary</h2><div class="banner">{html.escape(summary)}</div>

<h2>Series (kya kis time par banega)</h2>
<div class="grid">{''.join(series_cards)}</div>
<div class="box" style="margin-top:12px">
<b>Config kya hai?</b> <code>config/series.json</code> ek settings ki list hai.
Har block ek "series" hai. <b>enabled: true</b> matlab roz automatically banegi.
<b>format</b> batata hai Long video hai ya Shorts. <b>daily_slot_ist</b> batata hai kis time banegi.
<b>langs</b> batata hai English, Hindi ya dono. Aapko ye file khud edit karne ki zaroorat nahi,
sirf "enabled" ko true/false karna hai jab series chahiye ya nahi.
</div>

<h2>Keys (Environment / Secrets)</h2>
<table><tr><th>Key</th><th>Kis kaam ke liye</th><th>Status</th><th>Kahan daalni hai</th></tr>
{''.join(env_rows)}</table>
<p class="muted small">Values yahan kabhi nahi dikhti, sirf set/missing.</p>

<h2>Pipeline (ek video ke steps)</h2>
<div class="flow">{''.join(steps)}</div>

<h2>Recent runs</h2>
<table><tr><th>Kab</th><th>Series</th><th>Topic</th><th>Language</th><th>Type</th></tr>
{''.join(run_rows)}</table>
</body></html>"""

    out = ROOT / "output" / "dashboard.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"dashboard: {out.relative_to(ROOT)} (missing keys: {missing})")


if __name__ == "__main__":
    main()
