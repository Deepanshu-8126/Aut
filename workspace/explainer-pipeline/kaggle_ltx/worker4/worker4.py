"""LTX TEST - LTX-Video 2B i2v on Kaggle T4 (open weights, speed test with stopwatch)."""
import os, json, gc, subprocess, sys, time
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
JOBS_DIR = None
for root, _, files in os.walk("/kaggle/input"):
    if "jobs.json" in files: JOBS_DIR = root; break
assert JOBS_DIR
print("[ltx] JOBS_DIR =", JOBS_DIR, flush=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "diffusers>=0.35", "transformers", "accelerate", "sentencepiece", "imageio[ffmpeg]"], check=True)
import torch
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import export_to_video, load_image

t0 = time.time()
pipe = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.float16)
pipe.enable_model_cpu_offload()
try: pipe.vae.enable_tiling()
except Exception: pass
print(f"[ltx] LOADED in {time.time()-t0:.0f}s", flush=True)

jobs = json.load(open(f"{JOBS_DIR}/jobs.json"))
for j in jobs:
    name = "ltx_" + j["name"]; out = f"{OUT}/{name}.mp4"
    if os.path.exists(out): continue
    t1 = time.time()
    print("[ltx run]", name, flush=True)
    fr = pipe(image=load_image(f"{JOBS_DIR}/{j['image']}"),
              prompt=j["prompt"],
              negative_prompt="worst quality, inconsistent motion, blurry, jittery, distorted, watermark",
              width=576, height=1024, num_frames=121,
              num_inference_steps=30, guidance_scale=3.0, decode_timestep=0.03, decode_noise_scale=0.025,
              generator=torch.Generator("cuda").manual_seed(j.get("seed", 42))).frames[0]
    export_to_video(fr, out, fps=24)
    print(f"[ltx done] {name} in {time.time()-t1:.0f}s  <<< STOPWATCH", flush=True)
    gc.collect(); torch.cuda.empty_cache()
print("=== LTX ALL DONE ===")
