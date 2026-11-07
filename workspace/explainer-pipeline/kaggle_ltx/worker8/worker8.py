# FACTORY ENHANCE - Real-ESRGAN x4plus video upscaler, 2x T4 parallel - AIQUEST
import os, sys, time, glob, subprocess, threading, urllib.request, shutil
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from PIL import Image

T0 = time.time()
def log(*a): print("[fenh]", *a, flush=True)

WORK = "/kaggle/tmp/enh"; os.makedirs(WORK, exist_ok=True)
OUT = "/kaggle/working/outputs"; os.makedirs(OUT, exist_ok=True)
FFM = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
log("ffmpeg:", FFM, "| gpus:", torch.cuda.device_count())

SRC = None
for r, _, fs in os.walk("/kaggle/input"):
    if any(f.endswith(".mp4") for f in fs):
        SRC = r; break
assert SRC, "no clips found"
clips = sorted(glob.glob(os.path.join(SRC, "*.mp4")))
log("clips:", [os.path.basename(c) for c in clips])

WPATH = "/kaggle/tmp/x4plus.pth"
urllib.request.urlretrieve(
    "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth", WPATH)
log("weights:", os.path.getsize(WPATH) // 1048576, "MB")

# ---- RRDBNet (basicsr-compatible key names) ----
class ResidualDenseBlock(nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, True)
    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x

class RRDB(nn.Module):
    def __init__(self, nf, gc=32):
        super().__init__()
        self.rdb1 = ResidualDenseBlock(nf, gc)
        self.rdb2 = ResidualDenseBlock(nf, gc)
        self.rdb3 = ResidualDenseBlock(nf, gc)
    def forward(self, x):
        return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x

class RRDBNet(nn.Module):
    def __init__(self, nf=64, nb=23, gc=32):
        super().__init__()
        self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        self.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, True)
    def forward(self, x):
        fea = self.conv_first(x)
        fea = fea + self.conv_body(self.body(fea))
        fea = self.lrelu(self.conv_up1(F.interpolate(fea, scale_factor=2, mode="nearest")))
        fea = self.lrelu(self.conv_up2(F.interpolate(fea, scale_factor=2, mode="nearest")))
        return self.conv_last(self.lrelu(self.conv_hr(fea)))

SD = torch.load(WPATH, map_location="cpu")["params_ema"]

def upscale(model, dev, img):
    x = torch.from_numpy(np.array(img)).permute(2, 0, 1).float().div_(255).unsqueeze(0).to(dev).half()
    with torch.no_grad():
        try:
            y = model(x)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            _, _, H, Wd = x.shape
            pad = 16; mid = H // 2
            top = model(x[:, :, :mid + pad, :])
            bot = model(x[:, :, mid - pad:, :])
            y = torch.cat((top[:, :, :mid * 4, :], bot[:, :, pad * 4:, :]), 2)
    y = y.clamp_(0, 1).mul_(255).round_().byte()[0].permute(1, 2, 0).cpu().numpy()
    return Image.fromarray(y)

FAILED = []
def process(my_clips, dev_id):
    try:
        dev = f"cuda:{dev_id}"
        model = RRDBNet(); model.load_state_dict(SD, strict=True)
        model = model.half().to(dev).eval()
        for clip in my_clips:
            name = os.path.basename(clip)
            fr = os.path.join(WORK, name + ".fr"); os.makedirs(fr, exist_ok=True)
            subprocess.run([FFM, "-nostdin", "-y", "-i", clip, "-qscale:v", "2",
                            fr + "/%05d.jpg"], check=True, capture_output=True)
            frames = sorted(glob.glob(fr + "/*.jpg"))
            log(name, "->", len(frames), "frames on", dev)
            t1 = time.time()
            for i, fp in enumerate(frames):
                img = Image.open(fp).convert("RGB")
                out = upscale(model, dev, img).resize((1080, 1920), Image.LANCZOS)
                out.save(fp, quality=95)
                if i % 30 == 0:
                    log(name, f"{i}/{len(frames)}", f"{time.time() - t1:.0f}s")
            outp = os.path.join(OUT, "enh_" + name)
            subprocess.run([FFM, "-nostdin", "-y", "-framerate", "24", "-i", fr + "/%05d.jpg",
                            "-i", clip, "-map", "0:v", "-map", "1:a?",
                            "-c:v", "libx264", "-preset", "fast", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest",
                            "-movflags", "+faststart", outp], check=True, capture_output=True)
            shutil.rmtree(fr, ignore_errors=True)
            log("DONE", name, int(time.time() - t1), "s <<< STOPWATCH")
    except Exception as e:
        import traceback; traceback.print_exc()
        FAILED.append((dev_id, repr(e)))

th = [threading.Thread(target=process, args=(clips[0::2], 0)),
      threading.Thread(target=process, args=(clips[1::2], 1))]
for t in th: t.start()
for t in th: t.join()
log("FAILED:", FAILED)
log("ALL DONE in", int(time.time() - T0), "s | outputs:", os.listdir(OUT))
print("=== FENH ALL DONE ===", flush=True)
