"""FAST WORKER v2 - Wan 2.2 5B dual-GPU (device_map balanced), short shots."""
import os, json, gc, subprocess, sys
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
JOBS_DIR = None
for root, _, files in os.walk("/kaggle/input"):
    if "jobs.json" in files: JOBS_DIR = root; break
assert JOBS_DIR, "jobs.json not found"
print("[w2] JOBS_DIR =", JOBS_DIR, flush=True)

subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "diffusers>=0.35", "transformers", "accelerate", "ftfy", "imageio[ffmpeg]"], check=True)
import torch
from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
from diffusers.utils import export_to_video, load_image

MODEL = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
vae = AutoencoderKLWan.from_pretrained(MODEL, subfolder="vae", torch_dtype=torch.float32)
pipe = None
try:
    pipe = WanImageToVideoPipeline.from_pretrained(MODEL, vae=vae, torch_dtype=torch.float16, device_map="balanced")
    print("[w2] device_map balanced OK", flush=True)
except Exception as e:
    print("[w2] balanced fail:", str(e)[:200], flush=True)
    pipe = WanImageToVideoPipeline.from_pretrained(MODEL, vae=vae, torch_dtype=torch.float16)
    pipe.enable_model_cpu_offload()
try:
    dev = getattr(pipe, "_execution_device", "cuda:0")
    pipe.vae.to(dev)
    print("[w2] vae ->", dev, flush=True)
except Exception as e:
    pipe.vae.to("cuda:0"); print("[w2] vae -> cuda:0 (fb)", flush=True)
try: pipe.vae.enable_tiling()
except Exception: pass
try: pipe.vae.enable_slicing()
except Exception: pass

jobs = json.load(open(f"{JOBS_DIR}/jobs.json"))
for j in jobs:
    name = j["name"]; out = f"{OUT}/{name}.mp4"
    if os.path.exists(out): continue
    print("[w2 run]", name, flush=True)
    kw = dict(prompt=j["prompt"],
              negative_prompt=j.get("negative", "blurry, distorted, low quality, watermark"),
              height=j.get("h", 1152), width=j.get("w", 640),
              num_frames=81, num_inference_steps=24,
              guidance_scale=j.get("cfg", 5.0),
              generator=torch.Generator("cuda").manual_seed(j.get("seed", 42)),
              image=load_image(f"{JOBS_DIR}/{j['image']}"))
    try:
        fr = pipe(**kw).frames[0]
    except torch.OutOfMemoryError:
        print("[w2 oom] seq offload retry", flush=True)
        gc.collect(); torch.cuda.empty_cache()
        pipe.enable_sequential_cpu_offload()
        fr = pipe(**kw).frames[0]
    export_to_video(fr, out, fps=24)
    print("[w2 done]", name, flush=True)
    gc.collect(); torch.cuda.empty_cache()
print("=== W2 ALL DONE ===")
