# LTX img2vid worker — Kaggle free T4 (fp16 + cpu-offload + vae tiling)
# Input: attached dataset mein jobs.json + images | Output: /kaggle/working/*.mp4
import json, os, glob, torch
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import load_image, export_to_video
DS=glob.glob('/kaggle/input/*/jobs.json')[0]; ROOT=os.path.dirname(DS)
jobs=json.load(open(DS))
pipe=LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.float16)
pipe.enable_model_cpu_offload(); pipe.vae.enable_tiling()
for j in jobs:
    img=load_image(os.path.join(ROOT,j["image"]))
    out=pipe(image=img, prompt=j["prompt"], negative_prompt=j.get("neg","worst quality, static, watermark, text"),
             width=j.get("w",704), height=j.get("h",1216), num_frames=j.get("frames",161),
             num_inference_steps=j.get("steps",30), guidance_scale=j.get("cfg",3.0),
             generator=torch.Generator().manual_seed(j.get("seed",42))).frames[0]
    export_to_video(out, f'/kaggle/working/{j["name"]}.mp4', fps=24)
    print("DONE", j["name"], flush=True)
print("ALL-DONE")
