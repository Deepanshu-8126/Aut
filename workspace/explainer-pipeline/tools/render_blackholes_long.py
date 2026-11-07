#!/usr/bin/env python3
# HIDDEN BLACK HOLES — 16:9 long-form (~6 min), space-doc grammar.
# 10 FIG chapters, VO-lockstep pulses, generative ambient score w/ VO ducking,
# AI hero plates + 100% code-drawn motion. Hindi VO (voice-06).
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/bh"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
BH = os.path.join(ASSETS, "bh")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FPS = 30
W, H = 1920, 1080
ORDER = ['s1','s2','s3','s4','sA','s5','s6','s7','s8','sB','s9','s10']
DUR = [31.69, 27.29, 26.44, 26.04, 28.08, 28.68, 28.68, 27.16, 28.04, 25.8, 29.43, 17.94]
LEAD, GAP = 0.5, 1.0
BEATS = []
_t = 0.0
for d in DUR:
    BEATS.append(round(_t, 2)); _t += LEAD + d + GAP
TOTAL = round(_t + 2.5, 2)

SHOTS = {
 0:[["bh",9,1.2,.5,.45,.08,0],["worm",7,1.1,.5,.5,.3,0],["trav",8,1.08,.5,.5,.28,0],["bh",10,1.35,.5,.45,.1,2]],
 1:[["shower",6,1.1,.5,.4,.35,0],["stars",7,1.06,.5,.5,.45,0],["cosmos",7,1.1,.5,.5,.5,0],["stars",9,1.15,.4,.5,.5,5]],
 2:[["trav",7,1.1,.5,.5,.5,2],["stars",6,1.12,.4,.5,.5,3],["cosmos",7,1.15,.6,.4,.55,3],["stars",8,1.2,.5,.6,.5,8]],
 3:[["mw",7,1.04,.5,.5,.42,0],["shower",6,1.08,.5,.35,.45,2],["mw",7,1.2,.4,.5,.45,4],["cosmos",8,1.1,.5,.5,.5,5]],
 4:[["mw",8,1.5,.5,.42,.52,0],["worm",7,1.15,.5,.5,.45,2],["mw",8,1.3,.6,.45,.5,6],["trav",7,1.1,.5,.5,.5,4]],
 5:[["neb",8,1.1,.5,.5,.62,0],["stars",7,1.1,.6,.4,.6,6],["neb",8,1.2,.4,.55,.6,4],["trav",8,1.08,.5,.5,.6,6]],
 6:[["stars",8,1.06,.5,.5,.55,9],["neb",7,1.12,.55,.45,.6,2],["stars",8,1.15,.45,.55,.55,1],["shower",8,1.1,.5,.4,.6,4]],
 7:[["sat",7,1.06,.5,.5,.4,0],["stars",6,1.1,.5,.4,.55,4],["sat",8,1.2,.45,.55,.45,3],["cosmos",8,1.1,.5,.5,.55,6]],
 8:[["neb",7,1.1,.5,.5,.55,5],["worm",6,1.12,.5,.5,.45,3],["trav",8,1.1,.5,.5,.5,1],["neb",9,1.2,.45,.5,.55,0]],
 9:[["earth",9,1.06,.42,.5,.22,0],["sat",6,1.1,.5,.5,.3,2],["earth",13,1.08,.42,.5,.25,1]],
 10:[["stars",7,1.1,.6,.5,.55,2],["sat",6,1.08,.5,.45,.5,5],["stars",8,1.15,.5,.6,.55,7],["neb",10,1.1,.5,.5,.6,3]],
 11:[["bh",11,1.3,.5,.45,.3,0],["bh",10,1.45,.5,.42,.32,3]],
}
def cut_times():
    out=[]
    for bi,shots in SHOTS.items():
        acc=0.0
        for sh in shots[:-1]:
            acc+=sh[1]
            end=(BEATS[bi+1] if bi+1<len(BEATS) else TOTAL)-BEATS[bi]
            if acc<end-1.0: out.append(BEATS[bi]+acc)
    return sorted(out)

CAPTXT = [
 ["Ye video dekhte hue... tumhare sir ke upar, andhere mein CRORES rakshas tair rahe hain.",
  "Hamari galaxy mein 1 CRORE se zyada BLACK HOLES chhupe hain.",
  "Aur humein location pata hai... sirf 70 ki. Baaki sab — GAYAB.",
  "Aur madad ke liye jise bulaya gaya hai... wo ho TUM.",
  "Ye is waqt ki sabse badi COSMIC khoj hai."],
 ["Pehle samjho — ye rakshas banta kaise hai.",
  "Suraj se 20-30 guna bada taara marta hai... ek dhamake mein — SUPERNOVA.",
  "Bacha hua dil apne hi wazan se sikudta jaata hai... sikudta jaata hai...",
  "Jab tak gravity itni taakatwar na ho jaye... ki ROSHNI bhi na nikal sake.",
  "Is kaali sarhad ka naam — EVENT HORIZON. Wapsi ki aakhri rekha."],
 ["Aur yahin se shuru hoti hai musibat.",
  "Jo cheez roshni hi nahi chhodti... use telescope se dekhoge KAISE?",
  "Jo 70 mile — wo isliye mile kyunki wo KHA rahe the.",
  "Gas nigalte waqt wo itni garam hoti hai ki X-RAY mein chamak uthti hai.",
  "Lekin zyadatar black holes SHANT hain. Bhookhe nahi. Isliye... ADRISHYA."],
 ["Ab ginti karo. Hamari galaxy 13 ARAB saal purani hai.",
  "In 13 arab saalon mein, arabon vishal taare paida hue... aur mare.",
  "Models saaf kehte hain — 1 CRORE se zyada black holes banne chahiye.",
  "Kuch scientists kehte hain... 10 CRORE tak.",
  "Matlab — 99.999% rakshas... abhi bhi LAPATA hain."],
 ["Aur in sabke beech — galaxy ke theek CENTER mein betha hai inka BADSHAH.",
  "SAGITTARIUS A-STAR. Ek SUPERMASSIVE black hole.",
  "Suraj se 43 LAKH guna bhari.",
  "Poori galaxy usi ke chakkar kaat rahi hai. HUM BHI. Abhi bhi... isi pal.",
  "Ghabrao mat — wo 26,000 prakash varsh door hai. Asli rahasya wo hain... jo PAAS chhupe hain."],
 ["Lekin 100 saal pehle ek aadmi ne inka pata lagane ka hathiyar de diya — EINSTEIN.",
  "Bhari cheezein SPACE ko mod deti hain...",
  "Aur jab space mudta hai — ROSHNI bhi mud jaati hai.",
  "Matlab: black hole ek LENS ki tarah kaam kar sakta hai.",
  "Adrishya rakshas... khud apni CHUGLI kar deta hai."],
 ["Ab socho — ek black hole kisi taare ke chakkar kaat raha hai.",
  "Jab wo hamare aur taare ke theek BEECH se guzarta hai...",
  "Taare ki roshni achanak thodi si BADH jaati hai. Ek jhapki jitni chamak.",
  "Ise kehte hain — GRAVITATIONAL SELF-LENSING.",
  "Graph par ek nanhi si SPIKE... jo cheekh kar kehti hai: yahan kuch ADRISHYA hai."],
 ["Aur yahin se shuru hota hai mission.",
  "Southampton University ka project — BLACK HOLE HUNTERS.",
  "NASA ke TESS telescope ne lakhon taaron ki chamak saalon tak record ki.",
  "Pehle AI ne lakhon jagahein chhaani... ab kaam saunpa gaya hai — AAM logon ko.",
  "Ab tak 23,000 volunteers... 1.2 CRORE classifications kar chuke hain."],
 ["Aur ye tareeka KAAM karta hai.",
  "2022 — GAIA BH1. Sirf 1,560 prakash varsh door. Shant. Adrishya.",
  "2024 — GAIA BH3. Suraj se 33 GUNA bhari.",
  "Aur HUBBLE ne akela bhatakta rakshas pakda — 5,000 prakash varsh door.",
  "Andhere ke khilaf... pehli JEETEIN."],
 ["Ab dimag mein ek sawaal chal raha hoga —",
  "Kya koi chhupa black hole... DHARTI ki taraf bhi aa sakta hai?",
  "Sach ye hai: space itna vishal hai ki takkar ki sambhavna LAGBHAG ZERO hai.",
  "Sabse paas wala black hole bhi 1,500 prakash varsh door hai.",
  "Lekin... LAGBHAG zero, ZERO nahi hota. Yahi baat scientists ko raat mein jagaye rakhti hai."],
 ["Aur ab... TUMHARI baari.",
  "Na degree chahiye, na telescope. Sirf ek LAPTOP... aur 5 minute.",
  "Screen par graph aayega — tumhe bas wo khaas SPIKE dhoondhni hai.",
  "Pattern pakadne mein insaani AANKH aaj bhi machine ko takkar deti hai.",
  "Ho sakta hai... itihas ka agla black hole TUMHARI screen par mile."],
 ["To batao — kya tum ye COSMIC shikar join karoge?",
  "COMMENT mein likho: 1 — agar HUNTER banoge. 2 — agar sirf tamasha dekhoge.",
  "SUBSCRIBE kar lo... kyunki 1 CRORE rakshas abhi bhi azaad ghoom rahe hain.",
  "Aur ye case... abhi bhi KHULA hai."],
]
HI = set(("CRORES CRORE BLACK HOLES HOLE 70 GAYAB TUM COSMIC SUPERNOVA EVENT HORIZON KAISE "
          "KHA X-RAY SHANT ADRISHYA 13 ARAB 10 99.999% LAPATA EINSTEIN SPACE ROSHNI LENS CHUGLI "
          "BEECH BADH GRAVITATIONAL SELF-LENSING SPIKE HUNTERS TESS AI AAM 23,000 1.2 2022 2024 "
          "GAIA BH1 BH3 33 GUNA HUBBLE 5,000 1,560 JEETEIN TUMHARI LAPTOP AANKH COMMENT "
          "SUBSCRIBE KHULA HUNTER 1 2 20-30 CENTER BADSHAH SAGITTARIUS A-STAR SUPERMASSIVE 43 LAKH HUM BHI "
          "PAAS DHARTI LAGBHAG ZERO 1,500 26,000").split())


def make_caps():
    caps = []
    for i, chunks in enumerate(CAPTXT):
        wc = [len(c.split()) for c in chunks]; tot = sum(wc)
        t0 = BEATS[i] + LEAD; acc = 0
        for c, n in zip(chunks, wc):
            s = t0 + DUR[i] * acc / tot
            e = t0 + DUR[i] * (acc + n) / tot
            caps.append({"start": round(s, 2), "end": round(min(e + 0.2, t0 + DUR[i] + 0.8), 2),
                         "words": c.split()})
            acc += n
    return caps


def b64(p): return base64.b64encode(open(p, "rb").read()).decode()

# ================= AUDIO =================
SR = 44100
def _n(d): return int(d * SR)
def box(x, w):
    if w < 2: return x
    c = np.cumsum(np.concatenate(([0.0], x)))
    y = (c[w:] - c[:-w]) / w
    return np.concatenate((y, np.zeros(len(x) - len(y))))
def tone(d, f0, f1=None, a=0.3):
    t = np.arange(_n(d)) / SR; f1 = f1 or f0
    return a * np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * d)))
def envad(x, a, r):
    n = len(x); e = np.ones(n)
    na, nr = max(1, _n(a)), max(1, _n(r))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
    return x * e
def noise(d, seed=7): return np.random.RandomState(seed).standard_normal(_n(d)) * 0.4
def subboom(a):
    d = 1.4
    t = np.arange(_n(d)) / SR
    x = np.sin(2 * np.pi * (46 * t - 14 * t * t)) * np.exp(-t * 3.2)
    nz = envad(box(noise(0.2, 3), 30) * 2.0, 0.005, 0.16)
    x[:len(nz)] += nz
    return a * x
def ping(f, a, d=0.5):
    t = np.arange(_n(d)) / SR
    return a * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)
def click(a=0.5):
    x = noise(0.02, 11); return a * (x - box(x, 40)) * np.exp(-np.arange(len(x)) / 90.0)
def tickk(f=1500, a=0.33, d=0.05):
    return envad(tone(d, f, f * 0.7, a), 0.002, 0.03)
def whoosh(d, a, seed=5):
    x = noise(d, seed); bp = box(x, 10) - box(x, 120)
    t = np.arange(len(bp)) / len(bp)
    return a * bp * np.sin(np.pi * t) ** 2 * 6
def pop(a=0.5):
    return envad(tone(0.12, 420, 880, a), 0.004, 0.06)
def thud(a):
    d = 0.4
    x = tone(d, 85, 38, a) * np.exp(-np.arange(_n(d)) / SR * 9)
    nz = envad(box(noise(0.12, 9), 24) * 2.2, 0.004, 0.1)
    x[:len(nz)] += nz * a
    return x

def music_bed(n):
    t = np.arange(n) / SR
    m = np.zeros(n)
    inten = np.zeros(n)
    I = [0.72, 0.60, 0.55, 0.68, 0.78, 0.58, 0.62, 0.66, 0.70, 0.80, 0.74, 0.88]
    for i, b in enumerate(BEATS):
        e = BEATS[i + 1] if i + 1 < len(BEATS) else TOTAL
        inten[_n(b):min(_n(e), n)] = I[i]
    inten = box(inten, _n(2.2))
    # deep space drone: D2 + A2 + D3, detuned pairs
    for f, g in [(73.42, 1.0), (110.0, 0.5), (146.83, 0.3)]:
        m += g * (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t + 0.9)) * 0.5
    m *= 0.042 * (0.65 + 0.35 * np.sin(2 * np.pi * 0.04 * t))
    # airy pad: high cluster, very soft, slow beating (space wind)
    pad = (np.sin(2 * np.pi * 440.0 * t) + np.sin(2 * np.pi * 442.3 * t)
           + np.sin(2 * np.pi * 587.33 * t) * 0.6)
    m += pad * 0.006 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t + 2.0))
    # heartbeat pulse 60bpm in F6..F9
    pul = np.zeros(n)
    bt = BEATS[6]
    k = 0
    while bt < BEATS[11]:
        i0 = _n(bt); ln = _n(0.14)
        if i0 + ln < n:
            tt = np.arange(ln) / SR
            pul[i0:i0 + ln] += np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 30) * (0.5 if k % 2 == 0 else 0.3)
        bt += 0.5 if k % 2 == 0 else 0.5
        k += 1
    pe = np.zeros(n); pe[_n(BEATS[6]):_n(BEATS[11])] = 1.0
    m += pul * box(pe, _n(1.5)) * 0.8
    m *= inten
    # shimmer sparkles in F8 (discoveries)
    rs = np.random.RandomState(31)
    for _ in range(26):
        at = BEATS[8] + rs.rand() * (BEATS[9] - BEATS[8])
        f = 1200 + rs.rand() * 2400
        x = ping(f, 0.025, 0.7); i0 = _n(at)
        if i0 + len(x) < n: m[i0:i0 + len(x)] += x
    # risers before chapters
    for b in BEATS[1:]:
        r = envad(box(noise(1.3, 13), 8) - box(noise(1.3, 13), 100), 1.1, 0.18) * 1.6
        i0 = _n(b - 1.3)
        if i0 >= 0:
            ln = min(len(r), n - i0); m[i0:i0 + ln] += r[:ln] * 0.15
    # final resolve: D minor-ish swell last 8s
    f0 = _n(TOTAL - 8)
    tt = np.arange(n - f0) / SR
    chord = (np.sin(2 * np.pi * 146.83 * tt) + 0.7 * np.sin(2 * np.pi * 220 * tt)
             + 0.55 * np.sin(2 * np.pi * 293.66 * tt))
    env = np.minimum(tt / 3.5, 1.0) * np.exp(-np.maximum(tt - 5.0, 0) * 0.8)
    fin = np.zeros(n); fin[f0:] = chord * env * 0.028
    return m + fin

def build_audio():
    n = _n(TOTAL)
    sfx = np.zeros(n); B = BEATS
    def put(x, at, g=1.0):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); sfx[i:i + L] += x[:L] * g
    for b in B[1:]: put(whoosh(0.7, 0.32), b - 0.35)
    for ct in cut_times(): put(whoosh(0.35, 0.16), ct - 0.12)
    # F1: boom + counter ticks + 70 slam + type
    put(subboom(0.6), 0.3)
    for k in range(18): put(tickk(900 + k * 40, 0.2, 0.03), B[0] + 9.2 + k * 0.1)
    put(thud(1.0), B[0] + 15.6); put(ping(392, 0.2, 1.4), B[0] + 15.65)
    for k in range(10): put(click(0.3), B[0] + 21.5 + k * 0.1)
    # F2: star hum ping, collapse, supernova boom, EH tag
    put(ping(523, 0.15, 1.0), B[1] + 2.0)
    put(envad(tone(1.8, 300, 60, 0.12), 0.2, 0.4), B[1] + 7.2)
    put(subboom(0.9), B[1] + 9.0)
    put(tickk(800, 0.3), B[1] + 13.2); put(thud(0.7), B[1] + 16.6)
    # F3: scan beeps, xray sizzle, dim-out
    for k in range(4): put(ping(1047, 0.1, 0.3), B[2] + 3.0 + k * 1.0)
    put(envad(box(noise(2.2, 17), 6) * 1.5, 0.4, 0.8), B[2] + 10.5, 0.14)
    put(thud(0.6), B[2] + 9.0)
    put(envad(tone(2.4, 220, 90, 0.1), 0.3, 1.6), B[2] + 17.5)
    # F4: timeline draw, counter roll, stamp
    put(envad(tone(1.6, 500, 1000, 0.1), 0.2, 0.5), B[3] + 2.2)
    for k in range(22): put(tickk(1000 + k * 30, 0.16, 0.03), B[3] + 8.8 + k * 0.12)
    put(thud(1.0), B[3] + 17.8); put(ping(330, 0.2, 1.2), B[3] + 17.85)
    # F5: card drop, ray bends, lens ping
    put(thud(0.5), B[5] + 2.6)
    put(envad(tone(1.6, 700, 1400, 0.1), 0.2, 0.6), B[5] + 8.6)
    put(ping(880, 0.22, 0.9), B[5] + 13.4)
    put(thud(0.6), B[5] + 17.0)
    # F6: orbit ticks + spike pings
    put(ping(659, 0.18, 0.8), B[6] + 8.2)
    put(ping(659, 0.22, 0.8), B[6] + 12.4)
    put(ping(880, 0.26, 1.0), B[6] + 16.8)
    put(thud(0.7), B[6] + 19.4)
    # F7: card drop + counter rolls
    put(thud(0.5), B[7] + 6.4)
    for k in range(16): put(tickk(1100 + k * 35, 0.16, 0.03), B[7] + 20.0 + k * 0.1)
    put(pop(0.45), B[7] + 5.2)
    # F8: three card thuds + sparkle
    put(thud(0.6), B[8] + 3.2); put(thud(0.65), B[8] + 9.4); put(thud(0.7), B[8] + 15.2)
    put(ping(1319, 0.2, 1.2), B[8] + 20.6)
    # F9: keyboard, spike ping, eye
    for k in range(12): put(click(0.3), B[10] + 4.2 + k * 0.14)
    put(ping(880, 0.24, 0.8), B[10] + 11.6)
    for k in range(14): put(click(0.28), B[10] + 21.6 + k * 0.09)
    # F10: pops + stamp + bell-ish
    put(pop(0.5), B[11] + 4.8); put(pop(0.55), B[11] + 5.5)
    put(thud(1.0), B[11] + 12.8); put(ping(587, 0.3, 2.0), B[11] + 12.85)
    # F5 SgrA*: deep boom + orbit shimmer + counter ticks
    put(subboom(0.8), B[4] + 3.4)
    for k in range(20): put(tickk(800 + k * 50, 0.18, 0.03), B[4] + 8.0 + k * 0.11)
    put(ping(262, 0.22, 2.0), B[4] + 14.6)
    # F10 danger: tense ticks + heart thumps + red pulse
    for k in range(8): put(tickk(620, 0.22, 0.05), B[9] + 3.0 + k * 0.8)
    put(envad(tone(2.0, 180, 70, 0.1), 0.3, 1.2), B[9] + 9.6)
    put(thud(0.9), B[9] + 19.4); put(ping(220, 0.25, 1.8), B[9] + 19.45)
    # VO
    vo = np.zeros(n)
    for i, nm in enumerate(ORDER):
        wv = os.path.join(ROOT, "bvo_%s.wav" % nm)
        if not os.path.exists(wv):
            subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(ROOT, "bvo_%s.mp3" % nm),
                            "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
        wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
        wf.close()
        i0 = _n(BEATS[i] + LEAD); L = min(len(dat), n - i0)
        vo[i0:i0 + L] += dat[:L] * 1.3
    mus = music_bed(n)
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    mus *= (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    mix = vo + sfx * 0.8 + mus
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok %.1fs" % TOTAL)


# ================= HTML =================
def build_html():
    caps = make_caps()
    fonts = {"Anton": FONTS + "/Anton-Regular.ttf", "InterB": FONTS + "/Inter-Black.ttf",
             "InterS": FONTS + "/Inter-SemiBold.ttf", "Mono": FONTS + "/JetBrainsMono-Bold.ttf",
             "Deva": "/var/tmp/ujjain/TiroDeva.ttf"}
    ff = "\n".join("@font-face{font-family:'%s';src:url('file://%s');}" % (k, v) for k, v in fonts.items())
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body><script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,TOTAL=__TOT__,B=BEATSJ,DUR=DURJ,LEAD=0.5,CAPS=CAPSJ,HI=HIJ;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const ov=x=>{x=clamp(x,0,1);const c=1.7,u=x-1;return 1+u*u*((c+1)*u+c)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
const CYAN='#4dd8ff',ORG='#ff8c3b',PAPER='#eef2f8',RED='#e8503a';
const IMGS={};let nimg=0,want=5;
function ld(k,s){const im=new Image();im.onload=()=>nimg++;im.src=s;IMGS[k]=im;}
ld('hero','data:image/jpeg;base64,HERO64');
ld('gal','data:image/jpeg;base64,GAL64');
ld('ein','data:image/jpeg;base64,EIN64');
ld('tess','data:image/jpeg;base64,TESS64');
ld('logo','data:image/png;base64,LOGO64');
const VIDS={};let nvid=0;const wantvid=11;
function lv(k,b){const v=document.createElement('video');v.muted=true;v.preload='auto';
 v.addEventListener('loadeddata',()=>nvid++);v.src='data:video/mp4;base64,'+b;VIDS[k]=v;}
lv('bh','VBH64');lv('stars','VSTARS64');lv('mw','VMW64');lv('earth','VEARTH64');lv('neb','VNEB64');
lv('worm','VWORM64');lv('trav','VTRAV64');lv('cosmos','VCOSMOS64');lv('shower','VSHOWER64');
lv('sat','VSAT64');lv('rocky','VROCKY64');
function seekV(v,t){return new Promise(r=>{const tt=Math.max(0.04,Math.min(t,v.duration-0.06));
 if(Math.abs(v.currentTime-tt)<0.001)return r();
 const h=()=>{v.removeEventListener('seeked',h);r();};v.addEventListener('seeked',h);v.currentTime=tt;});}
function coverV(v,zoom,cx,cy,dim){
 const vw=v.videoWidth,vh=v.videoHeight;if(!vw)return;
 const sc=Math.max(W/vw,H/vh)*zoom;
 g.drawImage(v,W*cx-vw*sc*cx,H*cy-vh*sc*cy,vw*sc,vh*sc);
 if(dim>0){g.save();g.globalAlpha=dim;g.fillStyle='#01030c';g.fillRect(0,0,W,H);g.restore();}}
const SHOTS=SHOTSJ;
function shotAt(bi,lt){
 const arr=SHOTS[bi]; if(!arr)return null;
 let acc=0;
 for(let i=0;i<arr.length;i++){
  const d=arr[i][1];
  if(lt<acc+d||i===arr.length-1)
   return {v:arr[i][0],lt2:lt-acc,z:arr[i][2],cx:arr[i][3],cy:arr[i][4],dim:arr[i][5],off:arr[i][6],since:lt-acc};
  acc+=d;}
 return null;}
function drawBG(sh,t){
 if(!sh){g.fillStyle='#04060e';g.fillRect(0,0,W,H);return;}
 const punch=1+0.06*Math.exp(-sh.since*5);
 const v=VIDS[sh.v];
 if(v&&v.videoWidth)coverV(v,sh.z*punch+0.02*Math.sin(t*0.2),sh.cx,sh.cy,sh.dim);
 else{g.fillStyle='#04060e';g.fillRect(0,0,W,H);}}
// starfield layers
const STARS=[];{const r=rng(77);for(let i=0;i<240;i++)STARS.push([r()*W,r()*H,r()*1.6+0.4,r()*6.28,0.3+r()*0.7,i%3]);}
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=13;}nc.putImageData(id,0,0);}
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.4,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(2,3,8,0.55)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
function rrect(x,y,w2,h2,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w2,y,x+w2,y+h2,r);g.arcTo(x+w2,y+h2,x,y+h2,r);g.arcTo(x,y+h2,x,y,r);g.arcTo(x,y,x+w2,y,r);g.closePath();}
function space(t,drift){
 g.fillStyle='#04060e';g.fillRect(0,0,W,H);
 for(let i=0;i<3;i++){
  const bx=((i*700+t*(14+6*i))%(W+800))-400, by=220+i*300+40*Math.sin(t*0.3+i*2);
  const gr=g.createRadialGradient(bx,by,40,bx,by,460);
  const col=i===1?'rgba(70,40,90,0.10)':'rgba(30,60,110,0.10)';
  gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=gr;g.fillRect(0,0,W,H);}
 for(const s of STARS){
  const par=(s[5]+1)*0.35, x=(s[0]+t*drift*4.5*par)%W;
  const a=s[4]*(0.5+0.5*Math.sin(t*1.3+s[3]));
  g.save();g.globalAlpha=a;g.fillStyle=s[5]===2?'#bfe6ff':'#ffffff';
  g.beginPath();g.arc(x<0?x+W:x,s[1],s[2],0,6.29);g.fill();g.restore();}}
function cover(im,zoom,cx,cy){
 const sc=Math.max(W/im.width,H/im.height)*zoom;
 g.drawImage(im,W*cx-im.width*sc*cx,H*cy-im.height*sc*cy,im.width*sc,im.height*sc);}
function figbar(lt,left,right){
 const a=ss(0.2,0.8,lt);if(a<=0)return;
 g.save();g.globalAlpha=a;g.strokeStyle='rgba(222,234,248,0.6)';g.lineWidth=2;
 g.beginPath();g.moveTo(140,86);g.lineTo(140+1640*ss(0.2,1.1,lt),86);g.stroke();
 g.font='26px Mono';g.textBaseline='bottom';
 g.fillStyle=CYAN;g.textAlign='left';g.fillText(left,140,76);
 g.fillStyle='rgba(222,234,248,0.6)';g.textAlign='right';g.fillText(right,1780,76);g.restore();}
function stamp(lt,t0,x,y,txt,color,size,rot){
 const p=ss(t0,t0+0.22,lt);if(p<=0)return;
 const s=2.0-1.0*ov(p);
 g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);g.globalAlpha=p*0.95;
 g.strokeStyle=color;g.fillStyle=color;g.lineWidth=6;
 g.font=size+'px Mono';g.textAlign='center';g.textBaseline='middle';
 const tw=g.measureText(txt).width;
 rrect(-tw/2-28,-size*0.88,tw+56,size*1.76,10);g.stroke();g.fillText(txt,0,3);g.restore();
 const q=ss(t0+0.18,t0+0.8,lt);
 if(q>0&&q<1){g.save();g.globalAlpha=(1-q)*0.6;g.strokeStyle=color;g.lineWidth=3;
 g.beginPath();g.arc(x,y,70+300*q,0,6.29);g.stroke();g.restore();}}
function typew(lt,t0,txt,cps,x,y,font,size,color,align){
 if(lt<t0)return;const n=Math.floor((lt-t0)*cps);const s=txt.slice(0,n);
 const c=(n<txt.length)&&(Math.floor(lt*3)%2===0);
 T(x,y,s+(c?'_':''),font,size,color,align||'left',Math.min(1,(lt-t0)*4));}
function kicker(lt,t0,small,big,col){
 const p=ss(t0,t0+0.4,lt);if(p<=0)return;
 g.save();g.globalAlpha=p;
 T(140,176,small,'Mono',32,CYAN,'left',1,6);
 T(140,256,big,'Anton',88,col||PAPER,'left');g.restore();}
function counterTxt(lt,t0,t1,target,x,y,size,col,pre,post){
 const p=ss(t0,t1,lt);if(p<=0)return;
 const v=Math.round(target*p);
 const s=v.toLocaleString('en-IN');
 g.save();if(p<1){g.translate(x,y);g.translate(-x,-y);}
 T(x,y,(pre||'')+s+(post||''),'InterB',size,col,'left',1);g.restore();}
function polaroid(lt,t0,im,x,y,wpx,rot,labL,labR){
 const p=ss(t0,t0+0.45,lt);if(p<=0)return;
 const drop=(1-ov(p))*-70,hpx=wpx*im.height/im.width;
 g.save();g.globalAlpha=p;g.translate(x,y+drop);g.rotate(rot+0.008*Math.sin(lt*0.9));
 g.shadowColor='rgba(0,0,0,0.6)';g.shadowBlur=30;g.shadowOffsetY=12;
 g.fillStyle='#e8e4d8';g.fillRect(-wpx/2-12,-hpx/2-12,wpx+24,hpx+72);
 g.shadowColor='transparent';g.drawImage(im,-wpx/2,-hpx/2,wpx,hpx);
 g.fillStyle='#1a2030';g.font='30px Mono';g.textAlign='left';g.textBaseline='middle';
 g.fillText(labL,-wpx/2+4,hpx/2+32);
 g.font='20px Mono';g.fillStyle='rgba(26,32,48,0.7)';g.textAlign='right';
 g.fillText(labR,wpx/2-2,hpx/2+32);g.restore();}
function bhIcon(x,y,r,t,hot){
 g.save();
 g.fillStyle='#000';g.beginPath();g.arc(x,y,r,0,6.29);g.fill();
 g.strokeStyle=hot?ORG:CYAN;g.lineWidth=r*0.16;g.globalAlpha=0.9;
 g.beginPath();g.ellipse(x,y,r*1.9,r*0.5,0.12*Math.sin(t*0.7),0,6.29);g.stroke();
 g.lineWidth=r*0.1;g.globalAlpha=0.8;
 g.beginPath();g.arc(x,y,r*1.18,0,6.29);g.stroke();g.restore();}
// ============ CHAPTERS ============
function fig1(t,lt){
 figbar(lt,'MILKY WAY \u00b7 ABHI IS WAQT','FIG. 01 \u00b7 CHRONIC JOURNAL');
 typew(lt,0.8,'TUMHARE SIR KE UPAR...',13,140,176,'Mono',34,'rgba(238,242,248,0.92)','left');
 const p1=ss(9.0,9.4,lt);
 if(p1>0){g.save();g.globalAlpha=p1;
  T(140,300,'ANUMAAN','Mono',30,CYAN,'left',1,6);g.restore();
  counterTxt(lt,9.0,11.0,10000000,136,400,128,PAPER,'','+');
  T(140,492,'BLACK HOLES IS GALAXY MEIN','Mono',28,'rgba(238,242,248,0.8)','left',ss(10.6,11,lt),4);}
 const p2=ss(15.5,15.8,lt);
 if(p2>0){g.save();const sc=1.9-0.9*ov(p2);g.globalAlpha=p2;
  g.translate(140,0);g.scale(sc,sc);
  T(0,620/sc,'LOCATION PATA HAI SIRF','Mono',30,'rgba(238,242,248,0.85)','left',1,4);
  T(-6,760/sc,'70','Anton',230,ORG,'left');
  g.restore();}
 typew(lt,21.3,'AUR DHOONDHNE KE LIYE BULAYA HAI... TUMHE.',11,140,900,'Anton',52,PAPER,'left');
}
function fig2(t,lt){
 figbar(lt,'RAKSHAS KA JANM','FIG. 02');
 kicker(lt,0.5,'SURAJ SE 20\u201330 GUNA BADA TAARA','EK TAARE KI MAUT');
 const cx=1280,cy=560;
 const breathe=ss(1.5,2.5,lt), col=ss(7.0,9.0,lt), boom=ss(9.0,9.5,lt), after=ss(9.4,10.4,lt);
 if(breathe>0&&after<1){
  const R=(150+14*Math.sin(t*2.2))*(1-col*0.88);
  g.save();g.globalAlpha=breathe*(1-after);
  const gr=g.createRadialGradient(cx,cy,R*0.1,cx,cy,R*2.2);
  gr.addColorStop(0,'#fff6e0');gr.addColorStop(0.25,'#ffd27a');gr.addColorStop(0.6,'rgba(255,140,60,0.35)');gr.addColorStop(1,'rgba(255,120,40,0)');
  g.fillStyle=gr;g.beginPath();g.arc(cx,cy,R*2.2,0,6.29);g.fill();
  g.fillStyle='#fff2d0';g.beginPath();g.arc(cx,cy,R,0,6.29);g.fill();g.restore();}
 if(boom>0&&boom<1){g.save();g.globalAlpha=(1-boom)*0.9;g.fillStyle='#fff';g.fillRect(0,0,W,H);g.restore();}
 const ring=ss(9.0,10.6,lt);
 if(ring>0&&ring<1){g.save();g.globalAlpha=(1-ring);g.strokeStyle='#ffd9a0';g.lineWidth=10*(1-ring)+2;
  g.beginPath();g.arc(cx,cy,60+900*ring,0,6.29);g.stroke();g.restore();}
 if(after>0){
  g.save();g.globalAlpha=after;
  const rot=t*0.5;
  g.fillStyle='#000';g.beginPath();g.arc(cx,cy,95,0,6.29);g.fill();
  for(let k=0;k<3;k++){
   g.strokeStyle=k===0?ORG:'rgba(255,140,59,'+(0.5-k*0.15)+')';g.lineWidth=16-k*5;
   g.beginPath();g.ellipse(cx,cy,185+k*34,52+k*12,0.10*Math.sin(rot),0,6.29);g.stroke();}
  g.strokeStyle='#ffd9a0';g.lineWidth=5;
  g.beginPath();g.arc(cx,cy,114,0,6.29);g.stroke();
  g.restore();}
 const eh=ss(13.0,13.5,lt);
 if(eh>0){g.save();g.globalAlpha=eh;g.setLineDash([12,10]);g.strokeStyle=CYAN;g.lineWidth=3;
  g.beginPath();g.arc(cx,cy,260,0,6.29);g.stroke();g.setLineDash([]);
  g.font='30px Mono';g.fillStyle=CYAN;g.textAlign='left';g.textBaseline='middle';
  g.beginPath();g.moveTo(cx+184,cy-184);g.lineTo(cx+330,cy-280);g.stroke();
  g.fillText('EVENT HORIZON',cx+344,cy-284);g.restore();}
 typew(lt,16.4,'WAPSI KI AAKHRI REKHA',13,140,430,'Anton',56,ORG,'left');
 typew(lt,17.6,'ROSHNI BHI... BAND.',13,140,510,'Mono',30,'rgba(238,242,248,0.85)','left');
}
function fig3(t,lt){
 figbar(lt,'ADRISHYA PROBLEM','FIG. 03');
 kicker(lt,0.5,'ROSHNI NAHI \u2192 TELESCOPE BEKAAR','DIKHEGA KAISE?');
 // scanning telescope cone
 const sc=ss(2.2,3.0,lt);
 if(sc>0){g.save();g.globalAlpha=sc;
  g.strokeStyle='rgba(238,242,248,0.8)';g.lineWidth=5;
  g.beginPath();g.moveTo(240,930);g.lineTo(330,800);g.stroke();
  g.lineWidth=10;g.beginPath();g.moveTo(300,845);g.lineTo(390,785);g.stroke();
  const ang=-0.9+0.5*Math.sin(t*0.8);
  const gr=g.createLinearGradient(360,790,360+700*Math.cos(ang),790+700*Math.sin(ang));
  gr.addColorStop(0,'rgba(77,216,255,0.28)');gr.addColorStop(1,'rgba(77,216,255,0)');
  g.fillStyle=gr;g.beginPath();g.moveTo(360,790);
  g.lineTo(360+980*Math.cos(ang-0.09),790+980*Math.sin(ang-0.09));
  g.lineTo(360+980*Math.cos(ang+0.09),790+980*Math.sin(ang+0.09));g.closePath();g.fill();g.restore();}
 // X-ray binary (right): star + stream spiral into BH
 const xb=ss(8.4,9.2,lt);
 if(xb>0){const sx=1120,sy=560,bx=1560,by=520;
  g.save();g.globalAlpha=xb;
  const gr2=g.createRadialGradient(sx,sy,10,sx,sy,120);
  gr2.addColorStop(0,'#ffeccc');gr2.addColorStop(0.5,'rgba(255,190,110,0.5)');gr2.addColorStop(1,'rgba(255,170,80,0)');
  g.fillStyle=gr2;g.beginPath();g.arc(sx,sy,120,0,6.29);g.fill();
  g.fillStyle='#fff0d4';g.beginPath();g.arc(sx,sy,56,0,6.29);g.fill();
  // particle stream
  const hot=ss(10.5,11.5,lt);
  for(let i=0;i<46;i++){
   const u=((t*0.5+i/46)%1);
   const px=sx+ (bx-sx)*u + 30*Math.sin(u*9+t), py=sy+(by-sy)*u - 60*Math.sin(u*3.14);
   const sz=2.5+2*u;
   g.save();g.globalAlpha=xb*(0.3+0.7*u);
   g.fillStyle=u>0.7?(hot>0?'#dff4ff':'#ffd9a0'):'#ffd9a0';
   g.beginPath();g.arc(px,py,sz,0,6.29);g.fill();g.restore();}
  bhIcon(bx,by,34,t,true);
  if(hot>0){g.save();g.globalAlpha=hot*(0.6+0.4*Math.sin(t*9));
   g.strokeStyle='#dff4ff';g.lineWidth=3;
   for(let k=0;k<5;k++){const a=-1.4+k*0.26;
    g.beginPath();g.moveTo(bx+Math.cos(a)*54,by+Math.sin(a)*54);
    g.lineTo(bx+Math.cos(a)*(92+14*Math.sin(t*7+k)),by+Math.sin(a)*(92+14*Math.sin(t*7+k)));g.stroke();}
   g.font='28px Mono';g.fillStyle='#dff4ff';g.textAlign='center';g.fillText('X-RAY',bx,by-130);g.restore();}
  g.font='26px Mono';g.fillStyle='rgba(238,242,248,0.75)';g.textAlign='center';
  g.fillText('KHATA HUA BLACK HOLE = DIKHTA HAI',1340,760);
  g.restore();}
 // dim world: quiet BHs appear faint
 const dim=ss(17.3,19.0,lt);
 if(dim>0){g.save();g.globalAlpha=dim*0.68;g.fillStyle='#02030a';g.fillRect(0,0,W,H);g.restore();
  const r=rng(55);
  for(let i=0;i<14;i++){const x=200+r()*1500,y=200+r()*600;
   g.save();g.globalAlpha=dim*0.5*(0.4+0.6*Math.sin(t*1.2+i));
   g.strokeStyle='rgba(120,150,190,0.5)';g.lineWidth=2;
   g.beginPath();g.arc(x,y,16,0,6.29);g.stroke();g.restore();}
  T(960,560,'SHANT. BHOOKHE NAHI. ADRISHYA.','Anton',64,'rgba(222,234,248,0.9)','center',dim);}
}
function fig4(t,lt){
 figbar(lt,'GINTI KARO','FIG. 04');
 kicker(lt,0.5,'HAMARI GALAXY KI UMAR','13 ARAB SAAL');
 const tl=ss(2.0,4.2,lt);
 if(tl>0){g.save();
  g.strokeStyle='rgba(238,242,248,0.75)';g.lineWidth=3;
  g.beginPath();g.moveTo(140,420);g.lineTo(140+1560*tl,420);g.stroke();
  for(let k=0;k<=13;k++){const u=k/13;if(u>tl)break;
   g.beginPath();g.moveTo(140+1560*u,412);g.lineTo(140+1560*u,428);g.stroke();}
  g.font='24px Mono';g.fillStyle='rgba(238,242,248,0.7)';g.textAlign='left';g.textBaseline='top';
  g.fillText('0',132,440);g.textAlign='right';g.fillText('13 ARAB SAAL',1700,440);
  g.restore();}
 // star deaths flickers along timeline
 const fl=ss(4.5,5.0,lt);
 if(fl>0){const r=rng(88);
  for(let i=0;i<26;i++){const u=r(),ph=r()*6.28;
   const a=Math.max(0,Math.sin(t*2.2+ph))*fl*0.9;
   const x=140+1560*u,y=420;
   g.save();g.globalAlpha=a;g.fillStyle='#ffd9a0';
   g.beginPath();g.arc(x,y-30-r()*40,3,0,6.29);g.fill();g.restore();}}
 counterTxt(lt,8.6,11.4,10000000,136,620,150,PAPER,'','+');
 T(140,720,'BLACK HOLES BANNE CHAHIYE THE','Mono',30,CYAN,'left',ss(10.8,11.2,lt),4);
 const dz=ss(13.4,13.8,lt);
 if(dz>0)T(140,810,'KUCH KEHTE HAIN: 10 CRORE TAK','Mono',30,'rgba(238,242,248,0.8)','left',dz,3);
 stamp(lt,17.6,1430,780,'99.999% LAPATA',RED,48,-0.09);
}
function fig5(t,lt){
 figbar(lt,'EINSTEIN \u00b7 1915','FIG. 06');
 kicker(lt,0.4,'100 SAAL PEHLE DIYA GAYA HATHIYAR','GRAVITY = LENS');
 polaroid(lt,2.4,IMGS.ein,330,600,340,-0.05,'EINSTEIN','AI ART');
 // lensing diagram: source star left-center, mass center, observer right
 const dg=ss(6.0,7.0,lt);
 if(dg>0){const sx=700,sy=560,mx=1210,my=560,ex=1740,ey=560;
  g.save();g.globalAlpha=dg;
  // source star
  g.fillStyle='#fff0d4';g.beginPath();g.arc(sx,sy,18,0,6.29);g.fill();
  g.font='24px Mono';g.fillStyle='rgba(238,242,248,0.75)';g.textAlign='center';
  g.fillText('DOOR KA TAARA',sx,sy+56);
  // mass (black hole)
  bhIcon(mx,my,26,t,false);
  g.fillStyle='rgba(238,242,248,0.75)';g.fillText('BLACK HOLE',mx,my+76);
  // observer
  g.strokeStyle=PAPER;g.lineWidth=3;
  g.beginPath();g.arc(ex,ey,22,0,6.29);g.stroke();
  g.beginPath();g.arc(ex,ey,8,0,6.29);g.stroke();
  g.fillText('HUM',ex,ey+58);
  // bending rays
  const rp=ss(8.4,10.4,lt);
  if(rp>0){g.strokeStyle=CYAN;g.lineWidth=3.5;g.shadowColor=CYAN;g.shadowBlur=8;
   [[-1,0.82],[1,0.82]].forEach(cfg=>{
    const dir=cfg[0];
    g.beginPath();
    for(let i=0;i<=60;i++){const u=i/60;if(u>rp)break;
     const x=sx+(ex-sx)*u;
     const bend=Math.sin(Math.PI*u);
     const y=sy+dir*(118*bend)*(1-Math.pow(Math.abs(u-0.5)*2,2)*0.0);
     i?g.lineTo(x,y):g.moveTo(x,y);}
    g.stroke();});
   g.shadowBlur=0;}
  // magnified glow at observer
  const mg=ss(13.2,13.8,lt);
  if(mg>0){g.save();g.globalAlpha=mg*(0.6+0.4*Math.sin(t*5));
   g.fillStyle='rgba(255,240,212,0.9)';g.beginPath();g.arc(ex,ey,30,0,6.29);g.fill();g.restore();
   g.font='28px Mono';g.fillStyle=ORG;g.fillText('ROSHNI TEZ!',ex-10,ey-62);}
  g.restore();}
 typew(lt,16.6,'ADRISHYA RAKSHAS... KHUD CHUGLI KAR DETA HAI.',12,140,900,'Anton',48,PAPER,'left');
}
function fig6(t,lt){
 figbar(lt,'GRAVITATIONAL SELF-LENSING','FIG. 07');
 kicker(lt,0.4,'SIGNAL KAISA DIKHTA HAI?','EK NANHI SI SPIKE');
 // orbit anim top-right
 const ob=ss(1.8,2.6,lt);
 if(ob>0){const cx=1430,cy=330,R=200;
  g.save();g.globalAlpha=ob;
  g.setLineDash([6,8]);g.strokeStyle='rgba(238,242,248,0.35)';g.lineWidth=2;
  g.beginPath();g.ellipse(cx,cy,R,R*0.32,0,0,6.29);g.stroke();g.setLineDash([]);
  const gr=g.createRadialGradient(cx,cy,6,cx,cy,70);
  gr.addColorStop(0,'#fff0d4');gr.addColorStop(1,'rgba(255,200,120,0)');
  g.fillStyle=gr;g.beginPath();g.arc(cx,cy,70,0,6.29);g.fill();
  g.fillStyle='#fff0d4';g.beginPath();g.arc(cx,cy,30,0,6.29);g.fill();
  const ph=t*0.9;
  const bx=cx+Math.cos(ph)*R, by=cy+Math.sin(ph)*R*0.32;
  const front=Math.sin(ph)>0;
  if(!front)bhIcon(bx,by,13,t,false);
  // alignment flash when bh crosses front-center
  const alignGlow=Math.max(0,Math.cos(ph))*(front?1:0)*Math.max(0,1-Math.abs(Math.sin(ph))*3);
  if(front)bhIcon(bx,by,13,t,false);
  if(alignGlow>0.25){g.save();g.globalAlpha=alignGlow;
   g.strokeStyle=CYAN;g.lineWidth=3;
   g.beginPath();g.arc(cx,cy,42+16*alignGlow,0,6.29);g.stroke();g.restore();}
  g.restore();}
 // light curve graph
 const gp=ss(4.0,5.2,lt);
 if(gp>0){const x0=180,x1=1760,y0=880,yb=760;
  g.save();g.globalAlpha=gp;
  g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=2;
  g.beginPath();g.moveTo(x0,560);g.lineTo(x0,y0);g.lineTo(x0+(x1-x0)*ss(4.2,5.6,lt),y0);g.stroke();
  g.font='22px Mono';g.fillStyle='rgba(238,242,248,0.6)';g.textAlign='left';
  g.fillText('CHAMAK',x0-0,540);g.textAlign='right';g.fillText('WAQT \u2192',x1,910);
  const cp=ss(5.6,16.5,lt);
  const r=rng(23);let px=[];
  g.strokeStyle=CYAN;g.lineWidth=3.5;g.shadowColor=CYAN;g.shadowBlur=6;
  g.beginPath();
  const NPT=240;
  for(let i=0;i<=NPT*cp;i++){const u=i/NPT;
   const x=x0+(x1-x0)*u;
   let y=yb+Math.sin(u*40+1)*4+Math.sin(u*97)*3;
   [[0.33,1],[0.72,1.35]].forEach(sp=>{
    const d=(u-sp[0])/0.016;
    y-=Math.exp(-d*d)*120*sp[1];});
   i?g.lineTo(x,y):g.moveTo(x,y);px=[x,y];}
  g.stroke();g.shadowBlur=0;
  // spike tags
  [[0.33,8.1,'SPIKE'],[0.72,12.4,'PHIR SPIKE']].forEach(cfg=>{
   const sp=ss(cfg[1],cfg[1]+0.35,lt);if(sp<=0)return;
   const x=x0+(x1-x0)*cfg[0];
   g.save();g.globalAlpha=sp;
   g.strokeStyle=ORG;g.lineWidth=2.5;
   g.beginPath();g.arc(x,yb-120,34+10*Math.sin(t*5),0,6.29);g.stroke();
   g.font='26px Mono';g.fillStyle=ORG;g.textAlign='center';
   g.fillText(cfg[2],x,yb-186);g.restore();});
  g.restore();}
 typew(lt,16.8,'YE SPIKE CHEEKH KAR KEHTI HAI: YAHAN KUCH ADRISHYA HAI.',13,140,990,'Mono',28,ORG,'left');
}
function fig7(t,lt){
 figbar(lt,'BLACK HOLE HUNTERS \u00b7 ZOONIVERSE','FIG. 08');
 kicker(lt,0.4,'SOUTHAMPTON UNIVERSITY \u00b7 2021','MISSION SHURU');
 const pl=ss(4.8,5.2,lt);
 if(pl>0){g.save();g.globalAlpha=pl;
  g.fillStyle='rgba(10,16,30,0.8)';rrect(140,330,560,64,32);g.fill();
  g.strokeStyle=CYAN;g.lineWidth=2;g.stroke();
  g.font='28px Mono';g.fillStyle=CYAN;g.textAlign='center';g.textBaseline='middle';
  g.fillText('PROJECT: BLACK HOLE HUNTERS',420,364);g.restore();}
 polaroid(lt,6.2,IMGS.tess,1510,470,420,0.045,'NASA TESS','AI ART');
 // funnel
 const fn=ss(13.0,14.2,lt);
 if(fn>0){g.save();g.globalAlpha=fn;
  const steps=[['LAKHON TAARE',700],['AI SCREENING',520],['INSAANI AANKH',340]];
  steps.forEach((s,i)=>{
   const w2=s[1],y=470+i*110,x=440-w2/2;
   g.fillStyle='rgba(10,16,30,0.75)';rrect(x,y,w2,70,12);g.fill();
   g.strokeStyle=i===2?ORG:'rgba(77,216,255,0.7)';g.lineWidth=2.5;g.stroke();
   g.font='26px Mono';g.fillStyle=i===2?ORG:PAPER;g.textAlign='center';g.textBaseline='middle';
   g.fillText(s[0],440,y+37);
   if(i<2){g.strokeStyle='rgba(238,242,248,0.5)';g.beginPath();
    g.moveTo(440,y+74);g.lineTo(440,y+104);g.stroke();
    g.beginPath();g.moveTo(432,y+96);g.lineTo(440,y+108);g.lineTo(448,y+96);g.stroke();}});
  g.restore();}
 // counters
 counterTxt(lt,19.8,21.6,23000,1050,840,86,PAPER,'','');
 T(1054,910,'VOLUNTEERS','Mono',26,CYAN,'left',ss(21.2,21.6,lt),4);
 counterTxt(lt,20.6,22.6,12000000,1460,840,86,PAPER,'','+');
 T(1464,910,'CLASSIFICATIONS','Mono',26,CYAN,'left',ss(22.0,22.4,lt),4);
}
function fig8(t,lt){
 figbar(lt,'PEHLI JEETEIN','FIG. 09');
 kicker(lt,0.4,'TAREEKA KAAM KARTA HAI','SHIKAAR SHURU');
 const cards=[
  ['GAIA BH1','2022','1,560 PRAKASH VARSH',3.1],
  ['GAIA BH3','2024','SURAJ SE 33\u00d7 BHARI',9.3],
  ['HUBBLE KA RAKSHAS','2022','5,000 PRAKASH VARSH \u00b7 AKELA',15.1]];
 cards.forEach((c,i)=>{
  const p=ss(c[3],c[3]+0.45,lt);if(p<=0)return;
  const x=190+i*560,y=430+(1-ov(p))*70;
  g.save();g.globalAlpha=p;
  g.fillStyle='rgba(8,12,26,0.85)';rrect(x,y,480,330,18);g.fill();
  g.strokeStyle='rgba(77,216,255,0.55)';g.lineWidth=2.5;g.stroke();
  bhIcon(x+240,y+104,34+6*Math.sin(t*1.5+i),t+i,i===1);
  g.font='40px InterB';g.fillStyle=PAPER;g.textAlign='center';g.textBaseline='middle';
  g.fillText(c[0],x+240,y+208);
  g.font='26px Mono';g.fillStyle=ORG;g.fillText(c[1],x+240,y+252);
  g.font='24px Mono';g.fillStyle='rgba(238,242,248,0.75)';g.fillText(c[2],x+240,y+292);
  g.restore();});
 stamp(lt,20.4,1560,870,'ANDHERA HAAR RAHA HAI',RED,36,-0.07);
}
function fig9(t,lt){
 figbar(lt,'TUMHARI BAARI','FIG. 11');
 kicker(lt,0.4,'NA DEGREE \u00b7 NA TELESCOPE','SIRF LAPTOP + 5 MINUTE');
 // laptop with light curve inside
 const lp=ss(3.4,4.2,lt);
 if(lp>0){const x=1020,y=330,w2=700,h2=430;
  g.save();g.globalAlpha=lp;
  g.fillStyle='rgba(8,12,26,0.9)';rrect(x,y,w2,h2,14);g.fill();
  g.strokeStyle='rgba(238,242,248,0.6)';g.lineWidth=3;g.stroke();
  g.fillStyle='rgba(20,28,52,0.8)';rrect(x-50,y+h2,w2+100,26,8);g.fill();
  // graph inside
  g.strokeStyle='rgba(238,242,248,0.4)';g.lineWidth=2;
  g.beginPath();g.moveTo(x+50,y+60);g.lineTo(x+50,y+h2-60);g.lineTo(x+w2-40,y+h2-60);g.stroke();
  const cp=ss(4.6,9.0,lt);
  g.strokeStyle=CYAN;g.lineWidth=3;g.beginPath();
  for(let i=0;i<=160*cp;i++){const u=i/160;
   const gx=x+50+(w2-100)*u;
   let gy=y+h2-130+Math.sin(u*33)*5+Math.sin(u*71)*4;
   const d=(u-0.62)/0.02; gy-=Math.exp(-d*d)*150;
   i?g.lineTo(gx,gy):g.moveTo(gx,gy);}
  g.stroke();
  // cursor + click on spike
  const ck=ss(10.6,11.6,lt);
  if(ck>0){const tx=x+50+(w2-100)*0.62,ty=y+h2-270;
   const cxp=x+w2-80+(tx-(x+w2-80))*ck, cyp=y+80+(ty-(y+80))*ck;
   g.fillStyle=PAPER;
   g.beginPath();g.moveTo(cxp,cyp);g.lineTo(cxp+16,cyp+26);g.lineTo(cxp+6,cyp+24);g.lineTo(cxp+10,cyp+38);g.lineTo(cxp+4,cyp+40);g.lineTo(cxp,cyp+26);g.closePath();g.fill();
   const fl2=ss(11.5,11.8,lt);
   if(fl2>0&&lt<13.2){g.save();g.globalAlpha=(0.8-ss(12.6,13.2,lt)*0.8);
    g.strokeStyle=ORG;g.lineWidth=3;
    g.beginPath();g.arc(tx,ty,30+18*Math.sin(t*6),0,6.29);g.stroke();
    g.font='26px Mono';g.fillStyle=ORG;g.textAlign='center';g.fillText('YE RAHA!',tx,ty-54);g.restore();}}
  g.restore();}
 // eye vs machine
 const em=ss(14.6,15.2,lt);
 if(em>0){g.save();g.globalAlpha=em;
  g.strokeStyle=PAPER;g.lineWidth=4;
  g.beginPath();g.ellipse(330,560,110,62,0,0,6.29);g.stroke();
  g.fillStyle=CYAN;g.beginPath();g.arc(330,560,30,0,6.29);g.fill();
  g.fillStyle='#04060e';g.beginPath();g.arc(330,560,13,0,6.29);g.fill();
  g.font='28px Mono';g.fillStyle=PAPER;g.textAlign='center';g.fillText('INSAANI AANKH',330,680);
  g.font='34px InterB';g.fillStyle=ORG;g.fillText('>',520,560);
  g.strokeStyle='rgba(238,242,248,0.7)';g.lineWidth=3;
  rrect(620,500,130,110,10);g.stroke();
  for(let k=0;k<3;k++){g.beginPath();g.moveTo(640+k*34,480);g.lineTo(640+k*34,500);g.stroke();
   g.beginPath();g.moveTo(640+k*34,610);g.lineTo(640+k*34,630);g.stroke();}
  g.font='24px Mono';g.fillText('AI',685,556);
  g.font='28px Mono';g.fillStyle=PAPER;g.fillText('MACHINE',685,680);
  g.restore();}
 typew(lt,21.4,'AGLA BLACK HOLE... TUMHARI SCREEN PAR?',12,140,900,'Anton',52,PAPER,'left');
}
function fig10(t,lt){
 figbar(lt,'CASE FILE \u00b7 BLACK HOLE HUNTERS','FIG. 12 \u00b7 YOUR TURN');
 const lp=ss(1.2,1.7,lt);
 if(lp>0&&IMGS.logo.complete){g.save();const sc=1.6-0.6*ov(lp);g.globalAlpha=lp;
  g.translate(560,430);g.scale(sc,sc);
  g.save();g.beginPath();g.arc(0,0,260,0,6.29);g.clip();
  g.drawImage(IMGS.logo,-260,-260,520,520);g.restore();
  g.strokeStyle=ORG;g.lineWidth=6;g.beginPath();g.arc(0,0,264,0,6.29);g.stroke();
  g.restore();}
 T(560,772,'CHRONIC OF HISTORIC','Anton',56,PAPER,'center',ss(2.1,2.6,lt),3);
 const qp=ss(3.4,3.9,lt);
 if(qp>0){g.save();g.globalAlpha=qp;
  g.fillStyle='rgba(4,6,16,0.72)';rrect(1010,300,800,150,18);g.fill();
  g.font='44px InterB';g.fillStyle=PAPER;g.textAlign='center';g.textBaseline='middle';
  g.fillText('KYA TUM YE COSMIC',1410,355);
  g.fillText('SHIKAAR JOIN KAROGE?',1410,410);g.restore();}
 const q1=ss(4.7,5.05,lt),q2=ss(5.4,5.75,lt);
 [[q1,'1 \u00b7 HUNTER',1210,ORG,'#190e02'],[q2,'2 \u00b7 TAMASHA',1620,PAPER,'#111726']].forEach(cfg=>{
  const [qq,txt,x,bg2,fg]=cfg;if(qq<=0)return;
  g.save();const sc=1.5-0.5*ov(qq);g.globalAlpha=qq;g.translate(x,540);g.scale(sc,sc);
  g.fillStyle=bg2;rrect(-180,-46,360,92,46);g.fill();
  g.fillStyle=fg;g.font='42px InterB';g.textAlign='center';g.textBaseline='middle';
  g.fillText(txt,0,3);g.restore();});
 const sp=ss(8.2,8.6,lt);
 if(sp>0){g.save();const sc=1.4-0.4*ov(sp);g.globalAlpha=sp;g.translate(1410,680);g.scale(sc,sc);
  g.rotate(Math.sin(lt*13)*(lt<10?0.05:0));
  g.fillStyle='#d6361f';rrect(-210,-48,420,96,48);g.fill();
  g.fillStyle='#fff';g.font='46px InterB';g.textAlign='center';g.textBaseline='middle';
  g.fillText('SUBSCRIBE',8,3);
  g.beginPath();g.moveTo(-168,-15);g.lineTo(-142,-15);g.lineTo(-155,13);g.closePath();g.fill();
  g.restore();}
 stamp(lt,12.7,1410,850,'CASE ABHI BHI KHULA HAI',RED,40,-0.07);
 const fo=ss(TOTAL-B[11]-1.3,TOTAL-B[11]-0.1,lt);
 if(fo>0){g.save();g.globalAlpha=fo;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
function figSgra(t,lt){
 figbar(lt,'GALAXY KA CENTER','FIG. 05');
 kicker(lt,0.5,'SABKA BADSHAH','SAGITTARIUS A*');
 const cx=1330,cy=560;
 const ap=ss(2.8,3.8,lt);
 if(ap>0){g.save();g.globalAlpha=ap;
  // orbiting stars spiral
  const r=rng(66);
  for(let i=0;i<40;i++){const R=90+i*9,ph=t*(1.6/Math.sqrt(R/90))+i*2.4;
   const x=cx+Math.cos(ph)*R,y=cy+Math.sin(ph)*R*0.42;
   g.save();g.globalAlpha=ap*(0.25+0.5*r());g.fillStyle=i%4?'#ffffff':'#ffd9a0';
   g.beginPath();g.arc(x,y,1.6+r()*1.6,0,6.29);g.fill();g.restore();}
  bhIcon(cx,cy,64+4*Math.sin(t*1.4),t,true);
  g.restore();}
 counterTxt(lt,7.8,10.2,4300000,140,520,110,PAPER,'','');
 T(144,610,'\u00d7 SURAJ KA WAZAN','Mono',30,CYAN,'left',ss(9.8,10.2,lt),4);
 const pl=ss(13.8,14.3,lt);
 if(pl>0){g.save();g.globalAlpha=pl;
  g.fillStyle='rgba(10,16,30,0.8)';rrect(140,700,560,64,32);g.fill();
  g.strokeStyle='rgba(77,216,255,0.6)';g.lineWidth=2;g.stroke();
  g.font='28px Mono';g.fillStyle=PAPER;g.textAlign='center';g.textBaseline='middle';
  g.fillText('DOORI: 26,000 PRAKASH VARSH',420,734);g.restore();}
 typew(lt,21.0,'ASLI RAHASYA WO HAIN... JO PAAS CHHUPE HAIN.',12,140,880,'Anton',48,ORG,'left');
}
function figDanger(t,lt){
 // red tension pulse late
 const rp=ss(17.5,19.5,lt);
 if(rp>0){g.save();g.globalAlpha=rp*0.14*(0.6+0.4*Math.sin(t*2.4));
  g.fillStyle='#8d1e12';g.fillRect(0,0,W,H);g.restore();}
 figbar(lt,'SAWAAL JO SAB POOCHTE HAIN','FIG. 10');
 kicker(lt,0.5,'KYA DHARTI KO KHATRA HAI?','TAKKAR?');
 // real Earth footage (left) — label it
 const ep=ss(2.6,3.4,lt);
 if(ep>0){g.save();g.globalAlpha=ep;
  g.font='26px Mono';g.fillStyle=PAPER;g.textAlign='center';
  g.fillText('HUM',640,880);
  g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=2;
  g.beginPath();g.moveTo(640,850);g.lineTo(640,790);g.stroke();
  g.restore();}
 // bh top-right + distance link
 const bp=ss(8.6,9.6,lt);
 if(bp>0){const bx=1560,by=330;
  g.save();g.globalAlpha=bp;
  bhIcon(bx,by,30,t,false);
  g.font='26px Mono';g.fillStyle='rgba(238,242,248,0.8)';g.textAlign='center';
  g.fillText('SABSE PAAS WALA',bx,by+108);
  g.setLineDash([10,10]);g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=3;
  g.beginPath();g.moveTo(760,640);g.lineTo(bx-80,by+40);g.stroke();g.setLineDash([]);
  g.fillStyle=CYAN;g.font='34px InterB';g.textAlign='center';
  g.fillText('1,560 PRAKASH VARSH',1160,420);
  g.restore();}
 const zp=ss(11.8,12.3,lt);
 if(zp>0){g.save();g.globalAlpha=zp;
  T(1120,700,'TAKKAR KI SAMBHAVNA \u2248 0','Anton',64,PAPER,'center');
  g.restore();}
 const lk=ss(17.8,18.2,lt);
 if(lk>0){g.save();const sc=1.6-0.6*ov(lk);g.globalAlpha=lk;
  g.translate(1120,0);g.scale(sc,sc);
  T(0,810/sc,"'LAGBHAG' ZERO... ZERO NAHI HOTA.",'Anton',56,'#ff6b52','center');g.restore();}
}
const FIGS=[fig1,fig2,fig3,fig4,figSgra,fig5,fig6,fig7,fig8,figDanger,fig9,fig10];
function captions(t){
 let cur=null;
 for(const c of CAPS)if(t>=c.start&&t<c.end){cur=c;break;}
 if(!cur)return;
 const n=cur.words.length,prog=(t-cur.start)/(cur.end-cur.start);
 g.save();g.font='40px InterS';g.textBaseline='middle';
 const meas=cur.words.map(w=>g.measureText(w+' ').width);
 let tw=0;for(const m of meas)tw+=m;
 let x=W/2-tw/2;const y=1006;
 g.shadowColor='rgba(0,0,0,0.7)';g.shadowBlur=10;
 cur.words.forEach((w,i)=>{
  const on=prog*n>=i;const clean=w.replace(/[^A-Z0-9.%,\-]/g,'');
  g.fillStyle=HI.includes(clean)?ORG:'#ffffff';
  g.globalAlpha=on?1:0.3;g.textAlign='left';g.fillText(w,x,y);x+=meas[i];});
 g.restore();}
function flash(lt){const a=1-ss(0,0.14,lt);if(a>0){g.save();g.globalAlpha=a*0.4;g.fillStyle='#dfefff';g.fillRect(0,0,W,H);g.restore();}}
async function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 let bi=0;for(let i=0;i<B.length;i++)if(t>=B[i])bi=i;
 const lt=t-B[bi];
 const sh=shotAt(bi,lt);
 if(sh){const v=VIDS[sh.v];
  if(v&&v.duration)await seekV(v,(sh.off+sh.lt2*0.9)%(v.duration-0.12));}
 drawBG(sh,t);
 FIGS[bi](t,lt);
 if(bi>0)flash(lt);
 captions(t);
 g.save();g.fillStyle='rgba(255,255,255,0.18)';g.fillRect(0,H-4,W,4);
 g.fillStyle=ORG;g.fillRect(0,H-4,W*(t/TOTAL),4);g.restore();
 g.save();g.globalAlpha=0.4;
 g.drawImage(noiseCv,-(Math.floor(t*13)%19),-(Math.floor(t*7)%23),W+40,H+40);g.restore();
 g.drawImage(vig,0,0);
 const fi=ss(0,0.5,t);
 if(fi<1){g.save();g.globalAlpha=1-fi;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}}
window.renderAt=async function(t){await draw(t);return cv.toDataURL('image/jpeg',0.84);};
window.renderBatch=async function(ts){const out=[];
 for(const t of ts){await draw(t);out.push(cv.toDataURL('image/jpeg',0.84));}return out;};
document.fonts.ready.then(()=>{try{
 ['Anton','InterB','InterS','Mono','Deva'].forEach(f=>{g.font='30px '+f;g.fillText('Ag \u0905',-100,-100);});
 const wait=()=>{if(nimg>=want&&nvid>=wantvid){
  Promise.resolve().then(async()=>{await draw(1);await draw(60);await draw(200);await draw(300);window.__ready=true;}).catch(e=>{window.__err=''+(e.stack||e);});
 }else setTimeout(wait,60);};
 wait();}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff)
    html = html.replace("__TOT__", str(TOTAL)).replace("BEATSJ", json.dumps(BEATS)).replace("DURJ", json.dumps(DUR))
    html = html.replace("CAPSJ", json.dumps(caps)).replace("HIJ", json.dumps(sorted(HI)))
    html = html.replace("HERO64", b64(BH + "/bh_hero_wide.jpg"))
    for tok, f in [("VBH64","45020.mp4"),("VSTARS64","1610.mp4"),("VMW64","19636.mp4"),
                   ("VEARTH64","29351.mp4"),("VNEB64","30889.mp4"),("VWORM64","18791.mp4"),
                   ("VTRAV64","14151.mp4"),("VCOSMOS64","32910.mp4"),("VSHOWER64","14468.mp4"),
                   ("VSAT64","45033.mp4"),("VROCKY64","14540.mp4")]:
        html = html.replace(tok, b64("/var/tmp/stock/" + f))
    html = html.replace("SHOTSJ", json.dumps(SHOTS))
    html = html.replace("GAL64", b64(BH + "/galaxy_wide.jpg"))
    html = html.replace("EIN64", b64(BH + "/card_einstein.jpg"))
    html = html.replace("TESS64", b64(BH + "/card_tess.jpg"))
    html = html.replace("LOGO64", b64(LOGO))
    hp = os.path.join(ROOT, "page.html")
    open(hp, "w").write(html)
    return hp, caps


def ts_srt(x):
    hh = int(x // 3600); mm = int(x % 3600 // 60); s = x % 60
    return ("%02d:%02d:%06.3f" % (hh, mm, s)).replace(".", ",")
def write_srt(caps, path):
    L = []
    for i, c in enumerate(caps):
        L.append("%d\n%s --> %s\n%s\n" % (i + 1, ts_srt(c["start"]), ts_srt(min(c["end"], TOTAL)),
                                          " ".join(c["words"])))
    open(path, "w").write("\n".join(L))


def run(mode):
    os.makedirs(ROOT, exist_ok=True)
    hp, caps = build_html()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True,
                                    args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 200, "height": 200})
        page.goto("file://" + hp)
        try:
            page.wait_for_function("window.__ready === true || window.__err", timeout=180000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            chk = os.environ.get("CHK_TIMES")
            TSL = ([float(x) for x in chk.split(",")] if chk
                   else [BEATS[i] + DUR[i] * 0.74 for i in range(len(DUR))])
            ims = []
            for st in TSL:
                d = page.evaluate("window.renderAt(%f)" % st)
                ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))))
            tw, th = 480, 270
            cols = 3; rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw, rows * th), "black")
            for i, im in enumerate(ims):
                sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
            sheet.save(os.path.join(ROOT, "preview_sheet.jpg"), quality=86)
            browser.close(); print("preview ->", os.path.join(ROOT, "preview_sheet.jpg")); return
        FR = os.path.join(ROOT, "frames"); os.makedirs(FR, exist_ok=True)
        n = int(round(TOTAL * FPS)); t0 = time.time(); i = 0
        while i < n:
            batch = [k for k in range(i, min(i + 10, n))
                     if not os.path.exists(os.path.join(FR, "%05d.jpg" % k))]
            if batch:
                urls = page.evaluate("ts => window.renderBatch(ts)", [k / FPS for k in batch])
                for k, d in zip(batch, urls):
                    open(os.path.join(FR, "%05d.jpg" % k), "wb").write(base64.b64decode(d.split(",", 1)[1]))
            i += 10
            if (i // 10) % 40 == 0:
                print("frame %d/%d (%.1f fps)" % (i, n, i / max(0.01, time.time() - t0)), flush=True)
        browser.close()
    build_audio()
    write_srt(caps, os.path.join(ROOT, "final.srt"))
    print("FRAMES+AUDIO DONE n=%d" % n)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
