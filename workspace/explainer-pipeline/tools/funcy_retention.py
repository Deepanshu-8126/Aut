# FUNCYOUS RETENTION LAYER - LOCKED 2026-10-23
# Import into every Funcyous assembler. Fights the new-channel freeze:
#   #1 swipe-away killer = HOOK CARD (big bold text, 0 -> 1.6s)
#   #2 completion killer = CTA policy (OFF during growth phase)
# Usage in composite loop (tt = global time of frame):
#   from funcy_retention import draw_hook_card
#   draw_hook_card(im, tt, "YOUR CEILING IS", "RADIOACTIVE")
from PIL import Image, ImageDraw, ImageFont

FD = '/home/user/explainer-pipeline/assets/fonts'
_F_BIG   = ImageFont.truetype(f'{FD}/Montserrat-Black.ttf', 96)
_F_BIG2  = ImageFont.truetype(f'{FD}/Montserrat-Black.ttf', 112)

HOOK_T0   = 0.00   # visible from first frame (critical: frame 1 IS the thumbnail in feed)
HOOK_T1   = 1.60   # gone before VO caption flow needs the eye
HOOK_FADE = 0.30   # fade-out tail

AMBER = (255, 196, 64)
WHITE = (255, 255, 255)

def _scale(t):
    # pop-in: 1.12 -> 1.00 in first 0.22s (sub-pixel smooth), then hold
    if t >= 0.22: return 1.0
    u = t / 0.22
    u = u * u * (3 - 2 * u)
    return 1.12 - 0.12 * u

def draw_hook_card(im, tt, line1, line2=None, y=430):
    """Big bold hook text, upper third. line2 (optional) gets amber + bigger.
    Draw AFTER captions/chips so it sits on top. No-op outside its window."""
    if tt < HOOK_T0 or tt > HOOK_T1 + HOOK_FADE:
        return
    a = 1.0
    if tt > HOOK_T1:
        a = max(0.0, 1.0 - (tt - HOOK_T1) / HOOK_FADE)
    s = _scale(tt)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    rows = [(line1, _F_BIG, WHITE)]
    if line2:
        rows.append((line2, _F_BIG2, AMBER))
    # soft dark plate behind text for readability on any footage
    heights = []
    maxw = 0
    for txt, f, col in rows:
        w = dr.textlength(txt, font=f)
        maxw = max(maxw, w)
        heights.append(f.size + 18)
    total_h = sum(heights)
    pad = 46
    x0 = (im.width - maxw) / 2 - pad
    y0 = y - 34
    dr.rounded_rectangle([x0, y0, x0 + maxw + pad * 2, y0 + total_h + 52], 28,
                         fill=(0, 0, 0, int(150 * a)))
    yy = y
    for txt, f, col in rows:
        w = dr.textlength(txt, font=f)
        x = (im.width - w) / 2
        dr.text((x + 3, yy + 4), txt, font=f, fill=(0, 0, 0, int(190 * a)))
        dr.text((x, yy), txt, font=f, fill=col + (int(255 * a),))
        yy += f.size + 18
    if s != 1.0:
        cx, cy = im.width / 2, y0 + total_h / 2
        nw, nh = int(im.width * s), int(im.height * s)
        layer = layer.resize((nw, nh), Image.LANCZOS)
        layer = layer.crop((int(cx * s - im.width / 2), int(cy * s - cy),
                            int(cx * s - im.width / 2) + im.width,
                            int(cy * s - cy) + im.height))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'), (0, 0))

# CTA POLICY (growth phase): DO NOT concat the 3.2s CTA ender.
# Instead the last clip must loop into frame 1 (seamless rewatch).
# Re-enable CTA only after channel passes 1,000 subscribers.
CTA_ENABLED = False

# ============== PRO CAPTIONS (LOCKED upgrade 2026-10-23) ==============
# Professional-editor style: all Montserrat-Black, black stroke outline
# (readable on LIGHT and dark footage), active word amber + bigger.
_F_CAPN = ImageFont.truetype(f'{FD}/Montserrat-Black.ttf', 58)
_F_CAPA = ImageFont.truetype(f'{FD}/Montserrat-Black.ttf', 66)

def draw_captions_pro(im, tt, times, words, y=1690):
    """times = [(word, start, end)]; 3-word chunks; call every frame."""
    dr = ImageDraw.Draw(im, 'RGBA')
    wi = next((k for k, (w, s, e) in enumerate(times) if s <= tt < e), None)
    if wi is None:
        return
    c = wi // 3
    chunk = words[c*3:(c+1)*3]
    base = c * 3
    meas = [dr.textlength(w + '  ', font=(_F_CAPA if (base+k) == wi else _F_CAPN))
            for k, w in enumerate(chunk)]
    x = (im.width - sum(meas)) / 2
    for k, wd in enumerate(chunk):
        active = (base + k) == wi
        f = _F_CAPA if active else _F_CAPN
        col = (255, 196, 64, 255) if active else (255, 255, 255, 255)
        yy = y - (5 if active else 0)
        dr.text((x, yy), wd, font=f, fill=col,
                stroke_width=6, stroke_fill=(0, 0, 0, 230))
        x += meas[k]

# ============== CALLOUTS on real footage (LOCKED upgrade) ==============
# Clean pro highlight: ring draw-on + leader line + mono label. Max 2 per video.
import math as _math
_F_CALL = ImageFont.truetype(f'{FD}/JetBrainsMono-Bold.ttf', 32)

def draw_callout(im, tt, t0, t1, cx, cy, r, label, side='right'):
    """Animated ring at (cx,cy) radius r with leader line + label, t0..t1 window."""
    if tt < t0 or tt > t1:
        return
    a = min(1.0, (tt - t0) / 0.25) * min(1.0, (t1 - tt) / 0.25)
    draw_frac = min(1.0, (tt - t0) / 0.35)          # ring draws itself on
    pulse = 1.0 + 0.03 * _math.sin((tt - t0) * 6.0)
    rr_ = r * pulse
    dr = ImageDraw.Draw(im, 'RGBA')
    # ring (draw-on arc)
    bbox = [cx - rr_, cy - rr_, cx + rr_, cy + rr_]
    dr.arc(bbox, start=-90, end=-90 + 360 * draw_frac,
           fill=(255, 255, 255, int(235 * a)), width=5)
    dr.arc([b + (3 if i < 2 else -3) for i, b in enumerate(bbox)],
           start=-90, end=-90 + 360 * draw_frac,
           fill=(0, 0, 0, int(90 * a)), width=2)
    if draw_frac < 1.0:
        return
    # leader line + label
    dx = 1 if side == 'right' else -1
    lx1 = cx + dx * rr_
    lx2 = cx + dx * (rr_ + 70)
    ly2 = cy - rr_ * 0.55
    dr.line([lx1, cy, lx2, ly2], fill=(255, 255, 255, int(220 * a)), width=4)
    tw = dr.textlength(label, font=_F_CALL)
    tx = lx2 + 14 if dx == 1 else lx2 - 14 - tw
    dr.line([lx2, ly2, lx2 + dx * (tw + 24), ly2],
            fill=(255, 255, 255, int(220 * a)), width=4)
    dr.text((tx, ly2 - 48), label, font=_F_CALL,
            fill=(255, 255, 255, int(255 * a)),
            stroke_width=4, stroke_fill=(0, 0, 0, 220))

# IMAGE BRIGHTNESS RULE (LOCKED): scene ke hisaab se light/dark —
# bank/ATM/kitchen/day-object = BRIGHT daylight stills; night-native (streets,
# stations) = dark cinematic. Default dark NAHI hai.


# ============================================================
# SUBSCRIBE TAP (LOCKED 2026-10-23, user order: "proper real")
# Realistic YouTube subscribe interaction, MID-VIDEO (loop stays
# intact - ender CTA still banned till 1K subs).
# Timeline (2.6s): slide-in -> red SUBSCRIBE -> finger-dot tap ->
# flips to dark SUBSCRIBED + check -> bell shake -> slide-out.
# Place at a high-retention beat (~55-65% of video). Max 1/video.
# ============================================================
_F_SUB  = ImageFont.truetype(FD + '/Montserrat-Black.ttf', 42)
_F_SUBS = ImageFont.truetype(FD + '/Montserrat-Black.ttf', 38)

def _ease_out(p):  return 1 - (1 - p) ** 3
def _ease_in(p):   return p ** 3

def draw_subscribe_tap(im, tt, t0, cy=1452):
    u = tt - t0
    if u < 0 or u > 2.6:
        return
    dr = ImageDraw.Draw(im, 'RGBA')
    # --- global slide/fade ---
    if u < 0.28:
        k = _ease_out(u / 0.28); dy = int((1 - k) * 160); a = k
    elif u > 2.25:
        k = _ease_in((u - 2.25) / 0.35); dy = int(k * 160); a = 1 - k
    else:
        dy = 0; a = 1.0
    cx = 540; y = cy + dy
    pressed = 0.98 if 0.92 <= u < 1.12 else 1.0   # press squash
    flipped = u >= 1.12
    # --- button pill ---
    bw, bh = int(430 * pressed), int(104 * pressed)
    x0, y0 = cx - bw // 2 - 36, y - bh // 2
    if flipped:
        fill = (38, 40, 46, int(242 * a)); txt = 'SUBSCRIBED'; f = _F_SUBS
        tcol = (225, 228, 233, int(255 * a))
    else:
        fill = (255, 1, 50, int(245 * a)); txt = 'SUBSCRIBE'; f = _F_SUB
        tcol = (255, 255, 255, int(255 * a))
    dr.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], bh // 2, fill=fill)
    tw = dr.textlength(txt, font=f)
    tx = x0 + (bw - tw) / 2 + (14 if flipped else 0)
    dr.text((tx, y0 + bh / 2 - (f.size * 0.62)), txt, font=f, fill=tcol)
    if flipped:  # green check before text
        chx = tx - 34; chy = y0 + bh / 2
        dr.line([chx - 12, chy, chx - 3, chy + 10], fill=(80, 220, 120, int(255 * a)), width=7)
        dr.line([chx - 3, chy + 10, chx + 14, chy - 12], fill=(80, 220, 120, int(255 * a)), width=7)
    # --- bell (right of pill), shakes after flip ---
    bellx = x0 + bw + 62; ang = 0.0
    if 1.25 <= u < 2.1:
        import math as _m
        ang = 26 * _m.sin((u - 1.25) * 18) * (1 - (u - 1.25) / 0.85)
    bell = Image.new('RGBA', (120, 120), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bell)
    col = (255, 210, 60, int(255 * a)) if flipped else (235, 238, 242, int(235 * a))
    bd.pieslice([30, 26, 90, 86], 180, 360, fill=col)
    bd.rectangle([30, 56, 90, 78], fill=col)
    bd.rounded_rectangle([22, 74, 98, 86], 6, fill=col)
    bd.ellipse([52, 88, 68, 104], fill=col)
    if ang: bell = bell.rotate(ang, resample=Image.BICUBIC, center=(60, 30))
    im.paste(bell, (bellx - 60, y - 60), bell)
    # --- finger-dot tap (0.62-1.30): lands on button, press, ripple ---
    if 0.62 <= u < 1.35:
        bx, by = cx - 20, y + 6
        if u < 0.92:                     # approach from lower-right
            p = _ease_out((u - 0.62) / 0.30)
            fx = bx + (1 - p) * 190; fy = by + (1 - p) * 230; r, fa = 40, 120 + 80 * p
        elif u < 1.12:                   # press
            fx, fy = bx, by; r = 34; fa = 230
        else:                            # lift + fade
            p = (u - 1.12) / 0.23
            fx, fy = bx, by - p * 60; r = 38 + p * 10; fa = 200 * (1 - p)
        dr.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 255, 255, int(fa * 0.55 * a)))
        dr.ellipse([fx - r*0.55, fy - r*0.55, fx + r*0.55, fy + r*0.55], fill=(255, 255, 255, int(fa * a)))
    if 1.12 <= u < 1.55:                 # ripple ring on flip
        p = (u - 1.12) / 0.43
        rr2 = 50 + p * 150
        dr.ellipse([cx - 20 - rr2, y + 6 - rr2, cx - 20 + rr2, y + 6 + rr2],
                   outline=(255, 255, 255, int(190 * (1 - p) * a)), width=5)
