"""FACTORY GPU WORKER v1 — Wan 2.2 TI2V-5B (i2v/t2v) on Kaggle 2xT4.
Jobs: /kaggle/input/factory-jobs/jobs.json  →  clips: /kaggle/working/out/*.mp4
Job spec: {"name":"s1","task":"i2v"|"t2v","image":"s1.jpg","prompt":"...",
           "negative":"...","w":704,"h":1280,"frames":121,"fps":24,"steps":35,"cfg":5.0,"seed":42}
"""
import os, json, gc, subprocess, sys
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
# find jobs.json anywhere under /kaggle/input (dataset mount layout varies)
JOBS_DIR = "/kaggle/input/factory-jobs"
for root, _, files in os.walk("/kaggle/input"):
    if "jobs.json" in files:
        JOBS_DIR = root; break
else:
    print(os.popen("find /kaggle/input -maxdepth 3 | head -40").read())
    raise SystemExit("jobs.json NOT FOUND under /kaggle/input")
print("[worker] JOBS_DIR =", JOBS_DIR)
JOBS_FILE = os.environ.get("JOBS_FILE", f"{JOBS_DIR}/jobs.json")

# ---- DUAL-GPU SPLIT MODE (SPLIT=2): aadhe jobs GPU0, aadhe GPU1, parallel ----
if os.environ.get("SPLIT", "1") == "2" and "CUDA_VISIBLE_DEVICES" not in os.environ:
    jobs_all = json.load(open(JOBS_FILE))
    halves = [jobs_all[0::2], jobs_all[1::2]]
    procs = []
    for g, half in enumerate(halves):
        jf = f"/kaggle/working/jobs_gpu{g}.json"
        json.dump(half, open(jf, "w"))
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(g), JOBS_FILE=jf, SPLIT="1")
        procs.append(subprocess.Popen([sys.executable, __file__], env=env))
    codes = [pr.wait() for pr in procs]
    print("=== SPLIT DONE ===", codes)
    sys.exit(max(codes))
# NOTE: SPLIT=2 sirf chhote models/low-RAM-safe runs ke liye (2x pipeline = ~2x system RAM).
# Default SPLIT=1 = single process, dono GPU visible, RAM-safe.

subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "diffusers>=0.35", "transformers", "accelerate", "ftfy", "imageio[ffmpeg]"], check=True)

import torch
from diffusers import WanPipeline, WanImageToVideoPipeline, AutoencoderKLWan
from diffusers.utils import export_to_video, load_image

MODEL = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
jobs = json.load(open(JOBS_FILE))
print(f"[worker] {len(jobs)} jobs")

vae = AutoencoderKLWan.from_pretrained(MODEL, subfolder="vae", torch_dtype=torch.float32)
pipe_cls = {"i2v": WanImageToVideoPipeline, "t2v": WanPipeline}
loaded = {}

def get_pipe(task):
    if task not in loaded:
        for k in list(loaded):
            del loaded[k]; gc.collect(); torch.cuda.empty_cache()
        p = pipe_cls[task].from_pretrained(MODEL, vae=vae, torch_dtype=torch.float16)
        p.enable_model_cpu_offload()      # 16GB T4 fit
        for fn in ("enable_vae_tiling",):
            try: getattr(p, fn)()
            except Exception:
                try: p.vae.enable_tiling()
                except Exception as e: print("[warn] tiling:", e)
        try: p.vae.enable_slicing()
        except Exception: pass
        loaded[task] = p
    return loaded[task]

for j in jobs:
    name = j["name"]; task = j.get("task", "i2v")
    out_path = f"{OUT}/{name}.mp4"
    if os.path.exists(out_path):
        print(f"[skip] {name}"); continue
    print(f"[run] {name} ({task})")
    pipe = get_pipe(task)
    kw = dict(
        prompt=j["prompt"],
        negative_prompt=j.get("negative", "blurry, distorted, low quality, watermark, text, extra limbs"),
        height=j.get("h", 1280), width=j.get("w", 704),
        num_frames=j.get("frames", 121),
        num_inference_steps=j.get("steps", 35),
        guidance_scale=j.get("cfg", 5.0),
        generator=torch.Generator("cuda").manual_seed(j.get("seed", 42)),
    )
    if task == "i2v":
        kw["image"] = load_image(f"{JOBS_DIR}/{j['image']}")
    try:
        frames = pipe(**kw).frames[0]
    except torch.OutOfMemoryError:
        print("[oom] switching to sequential offload, retrying", flush=True)
        gc.collect(); torch.cuda.empty_cache()
        pipe.enable_sequential_cpu_offload()
        frames = pipe(**kw).frames[0]
    export_to_video(frames, out_path, fps=j.get("fps", 24))
    print(f"[done] {name} -> {out_path}")
    gc.collect(); torch.cuda.empty_cache()

print("=== ALL JOBS DONE ===")
