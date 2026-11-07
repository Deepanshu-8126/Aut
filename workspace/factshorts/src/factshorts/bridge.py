"""FACTSHORTS BRIDGE — the key-less way to get scripts out of any free chatbot.

    python run.py bridge --port 8077        (then open http://localhost:8077)

Why this exists instead of a scraper
------------------------------------
Automating the LM Arena / Meta AI / ChatGPT web UIs means driving someone else's
front-end with a bot: it breaks their terms, breaks on every UI change, and needs
stealth patching forever.  This bridge does the same job *legitimately* and it never
breaks: it hands you the exact prompt, opens the chat site in **your** browser, and
takes the reply back through one paste — validating it, writing `script.json`, and
kicking off the render for you.

Server-side it also exposes the free key-less chain, so "Generate with free AI"
works with no browser round-trip when the free endpoint is not rate limited.
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from factshorts import prompts as P                       # noqa: E402
from factshorts import spec as S                          # noqa: E402

OUT = ROOT / "out"
CHAT_SITES = [
    ("ChatGPT", "https://chatgpt.com/"),
    ("Gemini", "https://gemini.google.com/app"),
    ("Claude", "https://claude.ai/new"),
    ("Meta AI", "https://www.meta.ai/"),
    ("LM Arena", "https://lmarena.ai/"),
    ("Copilot", "https://copilot.microsoft.com/"),
]

JOBS: dict[str, dict] = {}
LOCK = threading.Lock()


def slug(s: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def topics() -> list[str]:
    try:
        return json.loads((ROOT / "config" / "topics.json").read_text())["topics"]
    except Exception:                                        # noqa: BLE001
        return ["Why You Feel Deja Vu"]


# --------------------------------------------------------------------- jobs
def start_job(kind: str, script_path: Path) -> str:
    jid = f"{kind}-{int(time.time())}"
    log = script_path.parent / f"_{kind}.log"
    cmd = [sys.executable, str(ROOT / "run.py"), kind, "--script", str(script_path)]
    f = log.open("w")
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT)
    with LOCK:
        JOBS[jid] = {"kind": kind, "proc": proc, "log": log, "started": time.time(),
                     "script": str(script_path)}
    return jid


def job_status(jid: str) -> dict:
    j = JOBS.get(jid)
    if not j:
        return {"error": "unknown job"}
    alive = j["proc"].poll() is None
    try:
        tail = j["log"].read_text()[-4000:]
    except Exception:                                        # noqa: BLE001
        tail = ""
    run_dir = Path(j["script"]).parent
    files = sorted(p.name for p in run_dir.glob("part-*.png")) + \
            sorted(p.name for p in run_dir.glob("*.mp4"))
    return {"id": jid, "kind": j["kind"], "running": alive,
            "seconds": round(time.time() - j["started"], 1),
            "log": tail, "files": files}


# -------------------------------------------------------------------- server
class Handler(BaseHTTPRequestHandler):
    server_version = "FACTSHORTS-Bridge/1.0"

    def log_message(self, fmt, *args):                        # quieter console
        if "/api/status" not in (args[0] if args else ""):
            sys.stderr.write("  [bridge] " + (fmt % args) + "\n")

    # -- helpers
    def _send(self, code: int, body: bytes, ctype: str = "application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200):
        self._send(code, json.dumps(obj).encode())

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:                                    # noqa: BLE001
            return {}

    # -- routes
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        if path == "/api/topics":
            return self._json({"topics": topics()})
        if path == "/api/prompt":
            q = self._query()
            return self._json({"prompt": self._build_prompt(q)})
        if path == "/api/status":
            return self._json(job_status(self._query().get("id", "")))
        if path == "/api/generate":
            return self._json(self._free_generate(self._query()))
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/save":
            return self._json(self._save(self._read_json()))
        if path == "/api/fill":
            data = self._read_json()
            sp = Path(data.get("script", ""))
            if not sp.exists():
                return self._json({"error": "script.json not found — save it first"}, 400)
            try:
                pack = S.load_pack(sp)
                before = S.stale_parts(pack)
                pack = S.repair_pack(pack, [int(x) for x in data["parts"]] if data.get("parts") else None)
                S.save_pack(pack, sp.parent)
                return self._json({"ok": True, "repaired": before,
                                   "remaining": S.stale_parts(pack),
                                   "summary": [{"idx": p["idx"], "badge": p["badge"],
                                                "layout": p["layout"], "title": p["title"],
                                                "bottom": p.get("bottom", ""),
                                                "src": p.get("_src", "llm")}
                                               for p in pack["parts"]]})
            except Exception as e:                            # noqa: BLE001
                return self._json({"error": str(e)[:300]}, 500)
        if path == "/api/render":
            data = self._read_json()
            sp = Path(data.get("script", ""))
            if not sp.exists():
                return self._json({"error": "script.json not found — save it first"}, 400)
            jid = start_job(data.get("kind", "stills"), sp)
            return self._json({"job": jid, "status": job_status(jid)})
        return self._json({"error": "not found"}, 404)

    # -- logic
    def _query(self) -> dict:
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        return {k: v[0] for k, v in q.items()}

    def _build_prompt(self, q: dict) -> str:
        topic = q.get("topic", topics()[0])
        ep = int(q.get("episode", 43))
        cat = q.get("category", "BRAIN FACTS")
        return (f"{S.SYSTEM}\n\nTOPIC = \"{topic}\"\nEPISODE = {ep}\nCATEGORY = {cat}\n"
                f"Write the 7-part FACTSHORTS pack as JSON now. Keep every string short "
                f"enough to fit a 1080x1920 frame.")

    def _save(self, data: dict) -> dict:
        topic = (data.get("topic") or "Untitled Topic").strip()
        raw = (data.get("json") or "").strip()
        if not raw:
            return {"error": "paste the model's JSON reply first"}
        d = OUT / slug(topic)
        d.mkdir(parents=True, exist_ok=True)
        try:
            pack = S._extract_json(raw)
        except Exception as e:                               # noqa: BLE001
            return {"error": f"could not read that JSON: {e}"}
        pack["topic"] = pack.get("topic") or topic
        # run it through the same validator/padder the pipeline uses
        try:
            parts = pack.get("parts") or []
            fixed = [S._clean_part(p, i + 1) for i, p in enumerate(parts)]
            have = {p["idx"] for p in fixed}
            fb = S.build_pack(topic, episode=0, offline=True)["parts"]
            fixed += [f for f in fb if f["idx"] not in have]
            fixed = sorted(fixed, key=lambda x: x["idx"])[:7]
            pack["parts"] = fixed
        except Exception as e:                               # noqa: BLE001
            return {"error": f"validation failed: {e}"}
        pack["episode"] = int(data.get("episode") or pack.get("episode") or 43)
        pack["category"] = data.get("category") or pack.get("category") or "BRAIN FACTS"
        S.save_pack(pack, d)
        P.write_style_files(d / "prompts", pack)
        return {"ok": True, "dir": str(d.relative_to(ROOT)),
                "script": str((d / "script.json").relative_to(ROOT)),
                "summary": [{"idx": p["idx"], "badge": p["badge"], "layout": p["layout"],
                             "title": p["title"], "bottom": p.get("bottom", "")}
                            for p in pack["parts"]]}

    def _free_generate(self, q: dict) -> dict:
        topic = q.get("topic", topics()[0])
        ep = int(q.get("episode", 43))
        cat = q.get("category", "BRAIN FACTS")
        try:
            pack = S.build_pack(topic, episode=ep, category=cat)
        except Exception as e:                               # noqa: BLE001
            return {"error": str(e)[:300]}
        d = OUT / slug(topic)
        d.mkdir(parents=True, exist_ok=True)
        S.save_pack(pack, d)
        P.write_style_files(d / "prompts", pack)
        return {"ok": True, "source": pack.get("_generated_by", "llm"),
                "script": str((d / "script.json").relative_to(ROOT)),
                "stale": S.stale_parts(pack),
                "summary": [{"idx": p["idx"], "badge": p["badge"], "layout": p["layout"],
                             "title": p["title"], "bottom": p.get("bottom", ""),
                             "src": p.get("_src", "template" if p.get("idx") in S.stale_parts(pack) else "llm")}
                            for p in pack["parts"]]}


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FACTSHORTS BRIDGE</title>
<style>
  :root{--ink:#0A0A0A;--gray:#555;--yellow:#FFD60A;--blue:#3A86FF;--green:#00C853}
  *{box-sizing:border-box}
  body{margin:0;background:#fff;color:var(--ink);font:15px/1.55 Inter,-apple-system,
       "Segoe UI",Roboto,Arial,sans-serif;
       background-image:radial-gradient(#DEDEDE 1.2px,transparent 1.2px);background-size:24px 24px}
  header{max-width:1080px;margin:0 auto;padding:34px 22px 8px}
  .pill{display:inline-block;background:var(--ink);color:#fff;font-weight:700;font-size:12px;
        letter-spacing:.05em;padding:9px 18px;border-radius:999px}
  .pill b{color:var(--yellow)}
  h1{font-size:38px;line-height:1.05;letter-spacing:-.02em;margin:18px 0 4px}
  p.lede{color:var(--gray);margin:0;max-width:74ch}
  main{max-width:1080px;margin:0 auto;padding:10px 22px 70px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:24px}
  @media(max-width:860px){.grid{grid-template-columns:1fr}}
  .panel{background:#fff;border:1px solid #ECECEC;border-radius:16px;padding:18px 20px;
         box-shadow:0 6px 22px rgba(0,0,0,.05)}
  .panel h2{margin:0 0 12px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;
            color:#8A8A8A}
  label{display:block;font-size:12px;font-weight:700;color:#8A8A8A;margin:10px 0 4px;
        text-transform:uppercase;letter-spacing:.04em}
  input,select,textarea{width:100%;font:inherit;border:1.5px solid #E3E3E3;border-radius:11px;
        padding:10px 12px;background:#fff;color:inherit}
  textarea{min-height:190px;resize:vertical;font-family:ui-monospace,Menlo,Consolas,monospace;
        font-size:12.5px;line-height:1.5}
  textarea.prompt{min-height:150px;background:#FAFAFA}
  .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  button{font:inherit;font-weight:700;border:0;border-radius:999px;padding:11px 20px;
         cursor:pointer;background:var(--ink);color:#fff}
  button.ghost{background:#fff;color:var(--ink);border:1.5px solid #E3E3E3}
  button.yellow{background:var(--yellow);color:var(--ink)}
  button.blue{background:var(--blue);color:#fff}
  button:disabled{opacity:.5;cursor:progress}
  .sites a{display:inline-block;margin:0 8px 8px 0;padding:9px 15px;border-radius:999px;
        border:1.5px solid #E3E3E3;text-decoration:none;color:var(--ink);font-weight:700;
        font-size:13px}
  .sites a:hover{border-color:var(--ink)}
  pre{background:var(--ink);color:#F4F4F4;border-radius:12px;padding:14px 16px;max-height:270px;
      overflow:auto;font-size:12px;line-height:1.55;white-space:pre-wrap}
  .msg{margin-top:12px;font-size:13.5px;font-weight:600}
  .ok{color:#0A8F4D}.err{color:#D32}.warn{color:#B26A00}
  table{width:100%;border-collapse:collapse;font-size:13px;margin-top:10px}
  td{padding:6px 4px;border-bottom:1px dashed #EEE;vertical-align:top}
  td:first-child{font-weight:800;color:#8A8A8A;white-space:nowrap;width:1%}
  .hint{font-size:12.5px;color:#777;margin-top:8px}
  code{background:#F4F4F4;border-radius:5px;padding:1px 5px;font-size:12.5px}
</style></head><body>
<header>
  <div class="pill">FACTSHORTS &bull; <b>BRIDGE</b> &bull; free AI, no keys, no scraping</div>
  <h1>Turn a free chatbot into your scriptwriter</h1>
  <p class="lede">Copy the locked prompt, paste it into any free chat site, paste the reply back
  here. The bridge validates it, writes <code>script.json</code>, and renders the Short.
  Nothing here automates those sites — you stay in the loop, so it never breaks.</p>
</header>
<main>
  <div class="panel">
    <h2>1 &middot; pick the topic</h2>
    <div class="row">
      <select id="topic" style="flex:1 1 320px"></select>
      <input id="episode" type="number" value="43" style="width:110px" title="episode number">
      <input id="category" value="BRAIN FACTS" style="width:190px" title="category">
    </div>
    <div class="hint">Queue comes from <code>config/topics.json</code> — edit that file to add more.</div>
  </div>

  <div class="grid">
    <div class="panel">
      <h2>2 &middot; copy the prompt</h2>
      <textarea id="prompt" class="prompt" readonly></textarea>
      <div class="row" style="margin-top:10px">
        <button class="yellow" onclick="copyPrompt()">Copy prompt</button>
        <button class="ghost" onclick="loadPrompt()">Refresh</button>
      </div>
      <div class="sites" style="margin-top:14px"></div>
      <div class="hint">Opens in your browser, logged in as you — exactly like typing it yourself.</div>
    </div>

    <div class="panel">
      <h2>3 &middot; paste the reply</h2>
      <textarea id="reply" placeholder='Paste the chatbot reply here. Raw JSON, ```json fences, or a half-finished reply all work — the validator repairs what it can and fills the rest.'></textarea>
      <div class="row" style="margin-top:10px">
        <button class="blue" onclick="save()">Validate &amp; save</button>
        <button class="ghost" onclick="freeGen()">Generate with free AI</button>
        <button class="ghost" onclick="fill()">Repair placeholder parts</button>
      </div>
      <div class="msg" id="msg"></div>
      <div id="summary"></div>
    </div>
  </div>

  <div class="panel" style="margin-top:20px">
    <h2>4 &middot; render</h2>
    <div class="row">
      <button class="yellow" onclick="render('stills')">Render 7 stills</button>
      <button onclick="render('video')">Render video + SFX</button>
      <button class="ghost" onclick="status()">Refresh status</button>
    </div>
    <div class="msg" id="jobmsg"></div>
    <pre id="log" style="display:none"></pre>
  </div>
</main>
<script>
const $ = id => document.getElementById(id);
let currentScript = "";

async function jget(url){ const r = await fetch(url); return r.json(); }
async function jpost(url, body){
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'},
                              body: JSON.stringify(body)});
  return r.json();
}
function msg(text, cls){ $('msg').className = 'msg ' + (cls||''); $('msg').textContent = text; }

function sites(){
  const list = [["ChatGPT","https://chatgpt.com/"],["Gemini","https://gemini.google.com/app"],
    ["Claude","https://claude.ai/new"],["Meta AI","https://www.meta.ai/"],
    ["LM Arena","https://lmarena.ai/"],["Copilot","https://copilot.microsoft.com/"]];
  $('.sites') && 0;
  document.querySelector('.sites').innerHTML = list.map(
    ([n,u]) => `<a href="${u}" target="_blank" rel="noopener">${n} &#8599;</a>`).join('');
}

async function loadTopics(){
  const d = await jget('/api/topics');
  $('topic').innerHTML = d.topics.map(t => `<option>${t}</option>`).join('');
  loadPrompt();
}
async function loadPrompt(){
  const q = `topic=${encodeURIComponent($('topic').value)}&episode=${$('episode').value}` +
            `&category=${encodeURIComponent($('category').value)}`;
  const d = await jget('/api/prompt?' + q);
  $('prompt').value = d.prompt;
}
function copyPrompt(){
  $('prompt').select(); document.execCommand('copy');
  navigator.clipboard && navigator.clipboard.writeText($('prompt').value);
  msg('Prompt copied — paste it into any chat site.', 'ok');
}
async function save(){
  msg('Validating…');
  const d = await jpost('/api/save', {topic:$('topic').value, episode:$('episode').value,
    category:$('category').value, json:$('reply').value});
  if(d.error) return msg(d.error, 'err');
  currentScript = d.script;
  msg('Saved to ' + d.script, 'ok');
  drawSummary(d.summary);
}
async function freeGen(){
  msg('Calling the free chain (may take ~20-60s)…');
  const d = await jget('/api/generate?topic=' + encodeURIComponent($('topic').value) +
                       '&episode=' + $('episode').value);
  if(d.error) return msg('Free chain failed: ' + d.error +
      ' — use the copy/paste route instead.', 'warn');
  currentScript = d.script;
  msg('Generated by: ' + d.source + ' → ' + d.script, 'ok');
  drawSummary(d.summary);
}
function drawSummary(rows){
  if(!rows) return;
  const tag = s => s && s !== 'llm'
    ? `<span style="background:#FFF3C4;border-radius:999px;padding:2px 8px;font-size:11px;
        font-weight:800">${s.toUpperCase()}</span>`
    : `<span style="background:#E8F7EE;color:#0A8F4D;border-radius:999px;padding:2px 8px;
        font-size:11px;font-weight:800">AI</span>`;
  $('summary').innerHTML = '<table>' + rows.map(r =>
    `<tr><td>${r.idx}</td><td><b>${r.badge}</b> — ${r.title} ${tag(r.src)}<br>
     <span style="color:#888">${r.layout} · ${r.bottom||''}</span></td></tr>`).join('') + '</table>' +
    (rows.some(r => r.src && r.src !== 'llm')
      ? '<div class="hint">Amber parts are still the built-in example text — hit ' +
        '<b>Repair placeholder parts</b> (free tier, one small request each) or paste a better ' +
        'reply and save again.</div>' : '');
}
async function fill(){
  if(!currentScript) return msg('Save or generate a script first.', 'warn');
  msg('Repairing placeholder parts one by one — this can take a minute…');
  const d = await jpost('/api/fill', {script: currentScript});
  if(d.error) return msg(d.error, 'err');
  msg(`Repaired: ${d.repaired.join(', ') || 'none'} · still placeholder: ` +
      `${d.remaining.join(', ') || 'none'}`, d.remaining.length ? 'warn' : 'ok');
  drawSummary(d.summary);
}
async function render(kind){
  if(!currentScript) return msg('Save or generate a script first.', 'warn');
  const d = await jpost('/api/render', {kind, script: currentScript});
  if(d.error) return msg(d.error, 'err');
  msg(`${kind} render started (${d.job}). Watch the log below.`, 'ok');
  poll(d.job);
}
let timer = null;
async function poll(id){
  clearInterval(timer);
  timer = setInterval(async () => {
    const s = await jget('/api/status?id=' + id);
    $('log').style.display = 'block';
    $('log').textContent = s.log || '';
    $('jobmsg').textContent = (s.running ? 'running' : 'finished') +
      ` · ${s.seconds}s · ${(s.files||[]).length} files`;
    $('jobmsg').className = 'msg ' + (s.running ? 'warn' : 'ok');
    if(!s.running) clearInterval(timer);
  }, 2000);
}
function status(){ msg('Poll /api/status for a job id.', ''); }

sites(); loadTopics();
</script></body></html>"""


def serve(port: int = 8077, host: str = "0.0.0.0"):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"\n  FACTSHORTS BRIDGE  →  http://localhost:{port}\n"
          f"  (copy prompt → free chat site → paste reply → render)\n"
          f"  Ctrl+C to stop\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  bridge stopped")
    finally:
        httpd.server_close()
