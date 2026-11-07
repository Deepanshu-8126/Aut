"""Sandbox-side driver: push jobs -> run worker -> poll -> download clips.
Usage: KAGGLE_API_TOKEN=... python3 run_factory.py <jobdir> [outdir]
jobdir must contain jobs.json + input images."""
import sys, os, json, time, subprocess, tempfile, shutil

sys.path.insert(0, '/var/tmp/pydeps')
JOBDIR = sys.argv[1]; OUTDIR = sys.argv[2] if len(sys.argv) > 2 else "/var/tmp/factory_out"
USER = "ukboy7u787"; DS = f"{USER}/factory-jobs"; KERNEL = f"{USER}/factory-gpu-worker-wan"
WORKER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "worker")
K = [sys.executable, "-m", "kaggle"]

def sh(args, **kw): return subprocess.run(K + args, capture_output=True, text=True, **kw)

# 1. dataset (create or version)
meta = {"title": "factory-jobs", "id": DS, "licenses": [{"name": "CC0-1.0"}]}
with tempfile.TemporaryDirectory() as td:
    for f in os.listdir(JOBDIR): shutil.copy(os.path.join(JOBDIR, f), td)
    json.dump(meta, open(os.path.join(td, "dataset-metadata.json"), "w"))
    r = sh(["datasets", "version", "-p", td, "-m", f"jobs {time.strftime('%F %T')}"])
    if "not found" in (r.stdout + r.stderr).lower() or r.returncode != 0:
        r = sh(["datasets", "create", "-p", td]); print("[ds create]", r.stdout.strip()[-200:])
    else: print("[ds version]", r.stdout.strip()[-200:])
time.sleep(30)  # dataset processing

# 2. push worker kernel
r = sh(["kernels", "push", "-p", WORKER_DIR]); print("[push]", r.stdout.strip())

# 3. poll
while True:
    time.sleep(60)
    s = sh(["kernels", "status", KERNEL]).stdout
    print("[poll]", s.strip()[-60:])
    if "COMPLETE" in s or "ERROR" in s or "CANCEL" in s: break

# 4. download outputs
os.makedirs(OUTDIR, exist_ok=True)
r = sh(["kernels", "output", KERNEL, "-p", OUTDIR]); print("[output]", r.stdout.strip())
print("[done] clips in", OUTDIR)
