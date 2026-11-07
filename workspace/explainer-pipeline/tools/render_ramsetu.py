# RAM SETU SHORT - code scenes renderer (s1,s2,s5,s6,s7,s8; s3/s4 = WAN clips)
# 1080x1920 @30fps, sub-pixel smooth only. Frames -> /var/tmp/ramsetu/fr/%05d.jpg
import os, sys, math
sys.path.insert(0, '/var/tmp/pydeps')
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
FR = '/var/tmp/ramsetu/fr'; os.makedirs(FR, exist_ok=True)
A = '/home/user/explainer-pipeline/assets/ramsetu'
IMS = '/home/user/image-search'
GOLD = (212, 175, 55); GOLD_B = (255, 216, 102); INKW = (240, 234, 220)

TIRO = lambda s: ImageFont.truetype('/var/tmp/fonts/tiro.ttf', s)
F_WP, F_WP_HI, F_SM, F_BIG, F_MONO = TIRO(66), TIRO(74), TIRO(34), TIRO(130), TIRO(46)

def ease(u): return u*u*(3-2*u)
def easeo(u): return 1-(1-u)**3

# ---------- assets ----------
NASA = Image.open(f'{IMS}/adam-s-bridge-ram-setu-nasa-satellite-im-1.jpg').convert('RGB')
AER = Image.open(f'{IMS}/adam-s-bridge-ram-setu-nasa-satellite-im-2.jpg').convert('RGB')
AER = AER.resize((AER.width*2, AER.height*2), Image.LANCZOS)
H1 = Image.open(f'{A}/h1_vanar_still.jpg').convert('RGB')
H2 = Image.open(f'{A}/h2_stone_still.jpg').convert('RGB')

def cover(img, cx, cy, zoom):
    """sub-pixel cover-crop: cx,cy normalized center in source; zoom>=1 extra over cover scale"""
    sw, sh = img.size
    base = max(W/sw, H/sh)
    s = base*zoom
    x0 = cx*sw - W/(2*s); y0 = cy*sh - H/(2*s)
    x0 = min(max(x0, 0), sw - W/s); y0 = min(max(y0, 0), sh - H/s)
    return img.transform((W, H), Image.AFFINE, (1/s, 0, x0, 0, 1/s, y0), resample=Image.BICUBIC)

# vignette
_yy, _xx = np.mgrid[0:H, 0:W]
_r = np.sqrt(((_xx-W/2)/(W/2))**2 + ((_yy-H/2)/(H/2))**2)
VIG = (np.clip((_r-0.55)/0.9, 0, 1)**1.8 * 95).astype(np.uint8)
VIGIMG = Image.fromarray(VIG, 'L')
BLACK = Image.new('RGB', (W, H), (0, 0, 0))

def post(im, fi):
    im = Image.composite(BLACK, im, VIGIMG)
    g = np.random.default_rng(fi).integers(-3, 4, (H//4, W//4, 1), np.int16)
    g = np.repeat(np.repeat(g, 4, 0), 4, 1)
    arr = np.asarray(im, np.int16) + g
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ---------- word-pop ----------
def mkwords(text, t0, dur):
    ws = text.replace('—', ' ').replace('...', '…').split()
    tot = sum(len(w) for w in ws)
    out, c = [], 0
    for w in ws:
        out.append((w, t0 + 0.05 + (c/tot)*dur*0.88)); c += len(w)
    return out

def pages(words, maxch=14):
    pg, cur, n = [], [], 0
    for w, ts in words:
        if n + len(w) > maxch*2 and cur: pg.append(cur); cur, n = [], 0
        cur.append((w, ts)); n += len(w)+1
    if cur: pg.append(cur)
    return pg

def draw_wordpop(d, im, pgs, t, y=1560):
    cur = None
    for pg in pgs:
        if t >= pg[0][1]: cur = pg
    if not cur: return
    vis = [(w, ts) for w, ts in cur if t >= ts]
    if not vis: return
    # wrap into lines maxch 14
    lines, ln, n = [], [], 0
    for w, ts in vis:
        if n + len(w) > 15 and ln: lines.append(ln); ln, n = [], 0
        ln.append((w, ts)); n += len(w)+1
    if ln: lines.append(ln)
    yy = y - (len(lines)-1)*86
    for ln in lines:
        txts = ' '.join(w for w, _ in ln)
        bb = d.textbbox((0, 0), txts, font=F_WP)
        x = (W - (bb[2]-bb[0]))//2
        for i, (w, ts) in enumerate(ln):
            u = min(1, (t-ts)/0.16)
            last = (w, ts) == vis[-1]
            f = F_WP_HI if (last and u < 1) else F_WP
            col = GOLD_B if last else INKW
            # shadow
            d.text((x+3, yy+3), w, font=f, fill=(0, 0, 0))
            d.text((x, yy - int((1-easeo(u))*14)), w, font=f, fill=col)
            x += d.textbbox((0, 0), w+' ', font=F_WP)[2]
        yy += 86
    return

VO = {  # scene: (text, vo_abs_start, vo_dur)
 1: ("अंतरिक्ष से दिखने वाली ये लकीर कोई मामूली चट्टान नहीं है", 0.4, 4.6),
 2: ("भारत और श्रीलंका के बीच अड़तालीस किलोमीटर लंबा राम सेतु", 5.7, 6.0),
 5: ("कुछ रिसर्च कहती हैं ऊपर के पत्थर नीचे की रेत से हज़ारों साल पुराने हैं", 25.4, 6.0),
 6: ("ये कैसे मुमकिन है प्रकृति ऐसा सीधा पुल खुद नहीं बनाती", 32.1, 5.6),
 7: ("तो क्या वाकई वानर सेना ने इतिहास लिख दिया था", 38.4, 4.6),
 8: ("ऐसे रहस्य हर हफ़्ते क्रॉनिक ऑफ़ हिस्टोरिक सब्सक्राइब दबाओ", 43.7, 5.4),
}
PG = {k: pages(mkwords(*VO[k])) for k in VO}

# ---------- scenes ----------
def s1(t, fi):  # 0-5.3 NASA zoom; bridge at ~(0.47,0.53)
    u = ease(min(1, t/5.3))
    z = 1.0 + 0.55*u
    cx = 0.5 + (0.47-0.5)*u; cy = 0.5 + (0.53-0.5)*u
    im = cover(NASA, cx, cy, z)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    d = ImageDraw.Draw(im, 'RGBA')
    if t > 2.6:  # pulsing ring on bridge line
        p = min(1, (t-2.6)/0.5); pulse = 1 + 0.06*math.sin((t-2.6)*5.2)
        rw, rh = 330*pulse*p, 150*pulse*p
        bx, by = W*0.50, H*0.52
        d.ellipse((bx-rw, by-rh, bx+rw, by+rh), outline=(255, 216, 102, int(230*p)), width=5)
    d.text((W-250, H-64), "IMAGE: NASA", font=F_SM, fill=(255, 255, 255, 150))
    draw_wordpop(d, im, PG[1], t)
    return post(im, fi)

# map base (bespoke)
def _mapbase():
    im = Image.new('RGB', (W, H), (8, 22, 38))
    d = ImageDraw.Draw(im, 'RGBA')
    india = [(0,0),(700,0),(640,150),(540,300),(470,430),(445,520),(520,585),(575,625),(545,665),(440,600),(330,585),(180,520),(0,420)]
    lanka = [(700,1285),(760,1215),(830,1185),(960,1205),(1070,1290),(1080,1480),(1030,1660),(900,1760),(770,1725),(700,1580),(672,1420)]
    for poly, col in ((india,(30,48,38)),(lanka,(30,48,38))):
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        gd.polygon(poly, fill=(80, 140, 120, 90))
        im.paste(Image.new('RGB',(W,H),(60,110,95)), (0,0), glow.filter(ImageFilter.GaussianBlur(18)))
        d.polygon(poly, fill=col, outline=(120, 180, 150), width=3)
    return im
MAPBASE = _mapbase()
P_A, P_B = (575, 625), (700, 1285)  # Dhanushkodi -> Talaimannar

def s2(t, fi):  # 5.3-12.0 map + dashed line + 48 KM
    tl = t - 5.3
    z = 1.0 + 0.05*ease(min(1, tl/6.7))
    im = cover(MAPBASE, 0.5, 0.5, z)
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((120, 330), "भारत", font=TIRO(58), fill=INKW)
    d.text((790, 1555), "श्रीलंका", font=TIRO(58), fill=INKW)
    prog = easeo(min(1, max(0, (tl-0.6)/2.6)))
    if prog > 0:
        dx, dy = P_B[0]-P_A[0], P_B[1]-P_A[1]
        L = math.hypot(dx, dy); n = int(L/46)
        for i in range(int(n*prog)):
            u0 = i/n
            x, y = P_A[0]+dx*u0, P_A[1]+dy*u0
            x2, y2 = P_A[0]+dx*(u0+0.5/n), P_A[1]+dy*(u0+0.5/n)
            d.line((x, y, x2, y2), fill=GOLD_B, width=9)
        # endpoint glow dot
        ex, ey = P_A[0]+dx*prog, P_A[1]+dy*prog
        d.ellipse((ex-12, ey-12, ex+12, ey+12), fill=(255, 230, 140))
    if tl > 1.2:
        km = int(48*min(1, (tl-1.2)/2.2))
        txt = f"{km} KM"
        d.rounded_rectangle((700, 880, 1010, 985), 18, fill=(0, 0, 0, 160), outline=GOLD, width=3)
        d.text((730, 898), txt, font=TIRO(64), fill=GOLD_B)
    draw_wordpop(d, im, PG[2], t)
    return post(im, fi)

SAND = None
def _sand():
    global SAND
    rng = np.random.default_rng(5)
    g = np.linspace(120, 70, 980).reshape(-1, 1)
    base = np.stack([g*1.0, g*0.82, g*0.55], -1)
    sp = rng.integers(-14, 15, (980, W, 3))
    SAND = Image.fromarray(np.clip(base+sp, 0, 255).astype(np.uint8))
_sand()

def s5(t, fi):  # 25.0-31.7 dating split
    tl = t - 25.0
    im = Image.new('RGB', (W, H), (10, 10, 12))
    stone = cover(H2, 0.5, 0.60 - 0.02*ease(min(1, tl/6.7)), 1.6)
    im.paste(stone.crop((0, 0, W, 940)), (0, 0))
    sn = SAND.crop((0, int(10*ease(min(1, tl/6.7))), W, 940+int(10*ease(min(1, tl/6.7)))))
    im.paste(sn, (0, 960))
    d = ImageDraw.Draw(im, 'RGBA')
    pulse = 1 + 0.25*math.sin(tl*3.0)
    d.rectangle((0, 942, W, 958), fill=(212, 175, 55, 255))
    d.rectangle((0, 942-int(4*pulse), W, 942), fill=(255, 216, 102, 120))
    d.text((73, 123), "पत्थर", font=TIRO(72), fill=(0,0,0)); d.text((70, 120), "पत्थर", font=TIRO(72), fill=GOLD_B)
    d.text((70, 1010), "रेत", font=TIRO(72), fill=(50, 38, 20))
    if tl > 0.8:
        val = int(7000*easeo(min(1, (tl-0.8)/2.0)))
        txt = f"{val:,}+ साल ?"
        bb = ImageDraw.Draw(Image.new('RGB',(10,10))).textbbox((0,0), txt, font=F_BIG)
        x = (W-(bb[2]-bb[0]))//2
        d.text((x+4, 760+4), txt, font=F_BIG, fill=(0,0,0))
        d.text((x, 760), txt, font=F_BIG, fill=GOLD_B)
    draw_wordpop(d, im, PG[5], t)
    return post(im, fi)

CHAIN = [(0.08,0.27),(0.17,0.30),(0.27,0.37),(0.37,0.46),(0.47,0.55),(0.57,0.62),(0.68,0.66),(0.79,0.67),(0.88,0.64),(0.95,0.60)]
def s6(t, fi):  # 31.7-38.0 aerial trace
    tl = t - 31.7
    u = ease(min(1, tl/6.3))
    im = cover(AER, 0.35+0.3*u, 0.5, 1.10)
    im = ImageEnhance.Color(im).enhance(1.12)
    d = ImageDraw.Draw(im, 'RGBA')
    # map chain normalized coords -> current view: recompute via same cover math
    sw, sh = AER.size; base = max(W/sw, H/sh); s = base*1.10
    cx = (0.35+0.3*u)*sw; x0 = cx - W/(2*s); y0 = 0.5*sh - H/(2*s)
    x0 = min(max(x0, 0), sw-W/s); y0 = min(max(y0, 0), sh-H/s)
    prog = easeo(min(1, max(0, (tl-0.5)/3.4)))
    pts = [((px*sw-x0)*s, (py*sh-y0)*s) for px, py in CHAIN]
    npts = int(len(pts)*prog)
    for i in range(max(0, npts-1)):
        d.line((*pts[i], *pts[i+1]), fill=(255, 216, 102, 220), width=7)
    for i in range(npts):
        x, y = pts[i]
        d.ellipse((x-10, y-10, x+10, y+10), fill=(255, 230, 140, 240))
    d.text((W-430, H-64), "SATELLITE IMAGERY", font=F_SM, fill=(255,255,255,150))
    draw_wordpop(d, im, PG[6], t)
    return post(im, fi)

def s7(t, fi):  # 38.0-43.3 epic question on h1 top crop
    tl = t - 38.0
    z = 1.32 - 0.20*ease(min(1, tl/5.3))
    im = cover(H1, 0.5, 0.30, z)
    im = ImageEnhance.Brightness(im).enhance(0.84)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((40, H-120, 330, H-66), 12, fill=(0, 0, 0, 150))
    d.text((60, H-112), "AI RECREATION", font=F_SM, fill=(255, 255, 255, 190))
    draw_wordpop(d, im, PG[7], t, y=1500)
    return post(im, fi)

def s8(t, fi):  # 43.3-49.0 CTA
    tl = t - 43.3
    im = Image.new('RGB', (W, H), (14, 13, 16))
    # gold radial glow
    gl = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(gl)
    r = 500 + 30*math.sin(tl*2.4)
    gd.ellipse((W/2-r, 770-r, W/2+r, 770+r), fill=70)
    im.paste(Image.new('RGB', (W, H), (90, 70, 20)), (0, 0), gl.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im, 'RGBA')
    # emblem ring 520px
    u0 = easeo(min(1, tl/0.7))
    R = 260*u0
    pulse = 1 + 0.03*math.sin(tl*3.2)
    R *= pulse
    if R > 40:
        d.ellipse((W/2-R, 770-R, W/2+R, 770+R), outline=GOLD, width=10)
        d.ellipse((W/2-R+22, 770-R+22, W/2+R-22, 770+R-22), outline=(212, 175, 55, 110), width=3)
    if u0 > 0.5:
        ch = "CH"
        bb = d.textbbox((0, 0), ch, font=TIRO(190))
        d.text(((W-(bb[2]-bb[0]))//2, 770-(bb[3]-bb[1])//2-150), ch, font=TIRO(190), fill=GOLD_B)
    t1 = "CHRONIC OF HISTORIC"
    bb = d.textbbox((0, 0), t1, font=F_MONO)
    d.text(((W-(bb[2]-bb[0]))//2, 1095), t1, font=F_MONO, fill=INKW)
    # subscribe pill spring pop at 1.2
    if tl > 1.2:
        v = min(1, (tl-1.2)/0.6)
        sc = 1 + 0.28*math.exp(-4*v)*math.sin(10*v)
        pw, ph = 460*sc, 120*sc
        d.rounded_rectangle((W/2-pw/2, 1270-ph/2, W/2+pw/2, 1270+ph/2), int(30*sc), fill=(255, 216, 102))
        st = "SUBSCRIBE"
        f2 = TIRO(int(58*min(1.08, sc)))
        bb = d.textbbox((0, 0), st, font=f2)
        d.text(((W-(bb[2]-bb[0]))//2, 1270-(bb[3]-bb[1])//2-12), st, font=f2, fill=(20, 16, 8))
    # gold sparks
    rng = np.random.default_rng(9)
    for i in range(26):
        sx = rng.uniform(60, W-60); sy0 = rng.uniform(0, H)
        sy = (sy0 - tl*rng.uniform(18, 48)) % H
        a = int(120+90*math.sin(tl*2+i))
        rr = rng.uniform(2.5, 5)
        d.ellipse((sx-rr, sy-rr, sx+rr, sy+rr), fill=(255, 216, 102, max(40, a)))
    draw_wordpop(d, im, PG[8], t, y=1610)
    return post(im, fi)

SCENES = [(0, 159, s1), (159, 360, s2), (750, 951, s5), (951, 1140, s6), (1140, 1299, s7), (1299, 1470, s8)]

if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for a, b, fn in SCENES:
        if only and fn.__name__ != only: continue
        for fi in range(a, b):
            p = f'{FR}/{fi:05d}.jpg'
            if os.path.exists(p): continue
            t = fi/FPS
            fn(t, fi).save(p, quality=90)
            if fi % 60 == 0: print('fr', fi, flush=True)
    print('CODE SCENES DONE')
