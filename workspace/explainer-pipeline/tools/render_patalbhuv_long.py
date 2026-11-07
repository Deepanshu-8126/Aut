#!/usr/bin/env python3
# PATAL BHUVANESHWAR v2 — detailed inside-the-cave journey. Word-sync paper-cut
# props, dynamic diagrams (4 gates, 4 yug stones, stalactites), strong hook,
# NO case-open ending. Hindi VO voice-06, Devanagari captions.
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/pb2"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
PT = os.path.join(ASSETS, "patal")
PR = os.path.join(ASSETS, "props")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FPS = 30
W, H = 1920, 1080
ORDER = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']
DUR = [32.86, 20.69, 27.86, 19.70, 25.18, 25.90, 26.18, 25.73, 22.30, 20.18]
LEAD, GAP = 0.5, 1.0
BEATS = []
_t = 0.0
for d in DUR:
    BEATS.append(round(_t, 2)); _t += LEAD + d + GAP
TOTAL = round(_t + 2.5, 2)

VOTXT = [
 "उत्तराखंड के पहाड़ों में एक दरवाज़ा है… जो सीधे पाताल में खुलता है। लोहे की ज़ंजीरें पकड़कर… नब्बे फीट नीचे… अंधेरे में उतरो… तो सामने आता है वो दृश्य, जिसे देखकर रोंगटे खड़े हो जाते हैं। भगवान गणेश का कटा हुआ सिर… और उसके ऊपर, चट्टान से टपकती अमृत की बूँदें। ये कोई कहानी नहीं… ये जगह आज भी मौजूद है। नाम है — पाताल भुवनेश्वर। और आज हम इसके अंदर चलेंगे… आखिरी कोने तक।",
 "हिंदू ग्रंथ कहते हैं — ब्रह्मांड में चौदह लोक हैं। सात ऊपर… सात नीचे। और सबसे नीचे के लोकों में एक है पाताल — नागों की दुनिया। पुराणों में इसे डरावना नहीं… बेहद समृद्ध बताया गया है। महल… रत्न… और शेषनाग — जिसके फन पर धरती टिकी है।",
 "स्कंद पुराण के मानस खंड में… इस गुफा का पूरा वर्णन मिलता है। कथा कहती है — त्रेता युग में सूर्यवंशी राजा ऋतुपर्ण यहाँ आए। गुफा के द्वार पर उन्हें मिले… खुद शेषनाग। और वही उन्हें अंदर लेकर गए — देवताओं की उस दुनिया में। द्वापर युग में पांडव यहाँ ध्यान करने आए। और फिर… आदि शंकराचार्य ने इस गुफा को फिर से खोजा। तब से आज तक… यहाँ पूजा कभी नहीं रुकी।",
 "मान्यता है — इस गुफा के चार द्वार थे। रणद्वार… पापद्वार… धर्मद्वार… और मोक्षद्वार। कहते हैं, रावण की मृत्यु के बाद… पापद्वार बंद हो गया। और महाभारत के युद्ध के बाद — रणद्वार भी। अब बचे हैं सिर्फ दो रास्ते… धर्म… और मोक्ष।",
 "अब चलो अंदर। एक सँकरी सुरंग… लोहे की ज़ंजीरें… और नब्बे फीट की गहराई। नीचे उतरते ही पैरों के नीचे महसूस होती हैं… पसलियों जैसी चट्टानें। मान्यता है — ये शेषनाग की पीठ है। वही शेषनाग… जो धरती, स्वर्ग और पाताल — तीनों को थामे हुए है। और तुम… उसकी पीठ पर चल रहे हो।",
 "थोड़ा और अंदर… और सामने आता है इस गुफा का सबसे बड़ा रहस्य। आदि गणेश — वो कटा हुआ सिर। पुराण कहते हैं — शिव ने गणेश का जो सिर काटा था… उसे इसी गुफा में रखा। और ऊपर चट्टान में बना है ब्रह्मकमल… जिससे बूँद-बूँद जल… सीधे गणेश जी के सिर पर गिरता है। हज़ारों सालों से… बिना रुके।",
 "छत पर चमकते हैं छोटे-छोटे पत्थर — मान्यता है, ये तैंतीस कोटि देवी-देवता हैं। आगे मिलती हैं शिव की जटाएँ… ऐरावत हाथी के हज़ार पैर… और एक ही गुफा में — केदारनाथ, बद्रीनाथ और अमरनाथ के दर्शन। और फिर… कालभैरव की जीभ। कहते हैं — जो उसके मुँह से होकर पूँछ तक पहुँच जाए… उसे मोक्ष मिल जाता है।",
 "और अब… वो चीज़ जो सबसे ज़्यादा हैरान करती है। चार पत्थर — चार युगों के प्रतीक। सतयुग… त्रेता… द्वापर… और कलियुग। पहले तीन शांत हैं। लेकिन चौथा पत्थर — कलियुग का — धीरे-धीरे बढ़ रहा है। मान्यता है… जिस दिन ये पत्थर छत को छू लेगा… उस दिन कलियुग का अंत होगा।",
 "विज्ञान इसे कहता है — चूना-पत्थर की गुफा। लाखों सालों से टपकता पानी… स्टैलेक्टाइट और स्टैलेग्माइट आकृतियाँ बनाता है। धीरे-धीरे बढ़ते पत्थर… विज्ञान के लिए प्रकृति का धैर्य हैं… और आस्था के लिए — देवताओं का घर। सच ये है… दोनों ही इस गुफा को खास बनाते हैं।",
 "पाताल भुवनेश्वर आज भी खुला है — पिथौरागढ़ के पास, गंगोलीहाट से चौदह किलोमीटर। अगर कभी जाओ… तो याद रखना — तुम सिर्फ एक गुफा में नहीं… हज़ारों साल पुरानी कहानियों के अंदर उतर रहे हो। ऐसी ही जगहों की कहानियों के लिए — सब्सक्राइब ज़रूर कर लेना। मिलते हैं… अगली यात्रा में।",
]

def strip_p(w): return w.strip("।…—,.?!-")

def wtimes(bi):
    ws = VOTXT[bi].split()
    cl = [len(w) + 1 for w in ws]
    tot = float(sum(cl)); acc = 0; out = []
    for w, c in zip(ws, cl):
        out.append((strip_p(w), round(LEAD + DUR[bi] * acc / tot, 2)))
        acc += c
    return out

def kt(bi, key, occ=1):
    k = 0
    for w, t in wtimes(bi):
        if w == key:
            k += 1
            if k == occ: return t
    raise ValueError("%d %s" % (bi, key))

# keyword local-times per chapter (word-sync anchors)
KT = {
 0: {"ft90": kt(0,"नब्बे"), "ganesh": kt(0,"गणेश"), "title": kt(0,"भुवनेश्वर"), "last": kt(0,"आखिरी"), "chain": kt(0,"ज़ंजीरें")},
 1: {"lok": kt(1,"चौदह"), "patal": kt(1,"पाताल"), "mahal": kt(1,"महल"), "ratn": kt(1,"रत्न"), "shesh": kt(1,"शेषनाग")},
 2: {"puran": kt(2,"स्कंद"), "raja": kt(2,"ऋतुपर्ण"), "shesh": kt(2,"शेषनाग"), "pandav": kt(2,"पांडव"), "shankar": kt(2,"शंकराचार्य")},
 3: {"g1": kt(3,"रणद्वार"), "g2": kt(3,"पापद्वार"), "g3": kt(3,"धर्मद्वार"), "g4": kt(3,"मोक्षद्वार"),
     "band1": kt(3,"पापद्वार",2), "band2": kt(3,"रणद्वार",2), "two": kt(3,"दो")},
 4: {"chain": kt(4,"ज़ंजीरें"), "ft": kt(4,"नब्बे"), "ribs": kt(4,"पसलियों"), "shesh": kt(4,"शेषनाग"), "back": kt(4,"पीठ",2)},
 5: {"ganesh": kt(5,"गणेश"), "kamal": kt(5,"ब्रह्मकमल"), "years": kt(5,"हज़ारों")},
 6: {"koti": kt(6,"तैंतीस"), "jata": kt(6,"जटाएँ"), "ked": kt(6,"केदारनाथ"), "bad": kt(6,"बद्रीनाथ"),
     "amar": kt(6,"अमरनाथ"), "bhair": kt(6,"कालभैरव"), "moksh": kt(6,"मोक्ष")},
 7: {"y1": kt(7,"सतयुग"), "y2": kt(7,"त्रेता"), "y3": kt(7,"द्वापर"), "y4": kt(7,"कलियुग"),
     "grow": kt(7,"बढ़"), "touch": kt(7,"छू"), "ant": kt(7,"अंत")},
 8: {"lime": kt(8,"चूना-पत्थर") if False else kt(8,"गुफा"), "sta": kt(8,"स्टैलेक्टाइट"), "stg": kt(8,"स्टैलेग्माइट"), "dono": kt(8,"दोनों")},
 9: {"map": kt(9,"भुवनेश्वर"), "km": kt(9,"चौदह"), "sub": kt(9,"सब्सक्राइब")},
}

SHOTS = {
 0:[["fog",8,1.1,.5,.5,.3,0],["pit",7,1.08,.5,.45,.3,0],["fire",7,1.12,.5,.45,.25,0],["ray",8,1.1,.5,.5,.3,0],["rock",6,1.1,.5,.5,.4,0]],
 1:[["ANIM",12,1,0,0,0,0],["gold",10,1.15,.5,.5,.5,1]],
 2:[["him",8,1.06,.5,.45,.35,0],["forest",7,1.08,.5,.45,.4,0],["snk1",7,1.1,.55,.45,.5,0],["pan",8,1.08,.5,.45,.4,0]],
 3:[["ANIM",11,1,0,0,0,0],["fire",10,1.12,.5,.5,.45,1]],
 4:[["rock",9,1.12,.45,.5,.45,1],["fog",9,1.15,.5,.45,.65,3],["pit",9,1.1,.5,.5,.4,2]],
 5:[["ray",9,1.12,.5,.5,.4,1],["rock",9,1.15,.55,.5,.45,0],["fire",10,1.1,.5,.45,.4,2]],
 6:[["pit",7,1.1,.5,.45,.4,0],["gold",7,1.12,.5,.5,.5,3],["fire",7,1.15,.5,.5,.45,4],["ray",7,1.12,.45,.5,.4,2]],
 7:[["ANIM",14,1,0,0,0,0],["rock",6,1.12,.5,.55,.68,0],["fog",8,1.1,.5,.5,.6,4]],
 8:[["valley",8,1.06,.5,.5,.3,0],["ray",8,1.15,.5,.5,.4,3],["forest",8,1.08,.5,.45,.35,2]],
 9:[["him",8,1.06,.5,.45,.3,2],["valley",8,1.1,.45,.5,.3,2],["pan",9,1.08,.5,.45,.35,0]],
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
 ["उत्तराखंड के पहाड़ों में एक *दरवाज़ा है… जो सीधे *पाताल में खुलता है।",
  "लोहे की *ज़ंजीरें पकड़कर… *नब्बे *फीट नीचे… अंधेरे में उतरो…",
  "सामने आता है वो दृश्य… जिसे देखकर *रोंगटे खड़े हो जाते हैं।",
  "भगवान *गणेश का कटा हुआ *सिर… ऊपर चट्टान से टपकती *अमृत की बूँदें।",
  "ये कोई कहानी नहीं… ये जगह *आज भी मौजूद है।",
  "नाम है — *पाताल *भुवनेश्वर। आज हम इसके *अंदर चलेंगे… आखिरी कोने तक।"],
 ["ग्रंथ कहते हैं — ब्रह्मांड में *चौदह लोक हैं। सात ऊपर… सात नीचे।",
  "सबसे नीचे के लोकों में एक है *पाताल — *नागों की दुनिया।",
  "पुराणों में ये *डरावना नहीं… बेहद *समृद्ध है।",
  "महल… *रत्न… और *शेषनाग — जिसके फन पर *धरती टिकी है।"],
 ["*स्कंद *पुराण के मानस खंड में… इस गुफा का पूरा वर्णन है।",
  "त्रेता युग में सूर्यवंशी राजा *ऋतुपर्ण यहाँ आए।",
  "द्वार पर उन्हें मिले… खुद *शेषनाग। वही उन्हें *अंदर लेकर गए।",
  "द्वापर में *पांडव यहाँ ध्यान करने आए।",
  "फिर *आदि *शंकराचार्य ने इसे फिर से खोजा। तब से *पूजा कभी नहीं रुकी।"],
 ["मान्यता है — गुफा के *चार द्वार थे।",
  "*रणद्वार… *पापद्वार… *धर्मद्वार… और *मोक्षद्वार।",
  "रावण की मृत्यु के बाद — *पापद्वार बंद। महाभारत के बाद — *रणद्वार भी।",
  "अब बचे सिर्फ दो रास्ते… *धर्म… और *मोक्ष।"],
 ["अब चलो *अंदर। सँकरी सुरंग… लोहे की *ज़ंजीरें… *नब्बे फीट की गहराई।",
  "नीचे उतरते ही पैरों के नीचे… *पसलियों जैसी चट्टानें।",
  "मान्यता है — ये *शेषनाग की पीठ है।",
  "वही शेषनाग… जो *धरती, *स्वर्ग और *पाताल — तीनों को थामे है।",
  "और तुम… उसकी *पीठ पर चल रहे हो।"],
 ["थोड़ा और अंदर… सामने है इस गुफा का सबसे बड़ा *रहस्य।",
  "*आदि *गणेश — वो *कटा हुआ सिर।",
  "शिव ने गणेश का जो सिर काटा… उसे *इसी गुफा में रखा।",
  "ऊपर है *ब्रह्मकमल… जिससे *बूँद-बूँद जल गणेश जी के सिर पर गिरता है।",
  "*हज़ारों सालों से… बिना रुके।"],
 ["छत पर चमकते छोटे-छोटे पत्थर — *तैंतीस *कोटि देवी-देवता।",
  "आगे — शिव की *जटाएँ… *ऐरावत के हज़ार पैर…",
  "एक ही गुफा में — *केदारनाथ, *बद्रीनाथ और *अमरनाथ के दर्शन।",
  "और फिर… *कालभैरव की *जीभ।",
  "जो मुँह से पूँछ तक पहुँच जाए… उसे *मोक्ष मिल जाता है।"],
 ["अब वो चीज़… जो सबसे ज़्यादा *हैरान करती है।",
  "चार पत्थर — *चार *युगों के प्रतीक।",
  "*सतयुग… *त्रेता… *द्वापर… और *कलियुग।",
  "पहले तीन शांत हैं। चौथा — कलियुग का — *बढ़ रहा है।",
  "जिस दिन ये छत को *छू लेगा… उस दिन *कलियुग का *अंत होगा।"],
 ["विज्ञान कहता है — *चूना-पत्थर की गुफा।",
  "लाखों सालों से टपकता *पानी… *स्टैलेक्टाइट और *स्टैलेग्माइट बनाता है।",
  "विज्ञान के लिए — प्रकृति का *धैर्य। आस्था के लिए — देवताओं का *घर।",
  "सच ये है… *दोनों इसे खास बनाते हैं।"],
 ["पाताल भुवनेश्वर *आज भी खुला है — *पिथौरागढ़, गंगोलीहाट से *चौदह किलोमीटर।",
  "अगर जाओ… तो याद रखना —",
  "तुम हज़ारों साल पुरानी *कहानियों के अंदर उतर रहे हो।",
  "ऐसी कहानियों के लिए… *सब्सक्राइब ज़रूर कर लेना।",
  "मिलते हैं… *अगली *यात्रा में।"],
]

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
def bell(f, a, d=2.4):
    t = np.arange(_n(d)) / SR
    x = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2.76*t) + 0.25*np.sin(2*np.pi*f*5.4*t))
    return a * x * np.exp(-t * 2.1)
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
def paper(a=0.5):
    x = noise(0.16, 23); hp = x - box(x, 18)
    return envad(hp * 2.2, 0.004, 0.1) * a
def drip(a=0.14):
    t = np.arange(_n(0.3)) / SR
    return a * np.sin(2 * np.pi * (2200 - 1400 * t) * t) * np.exp(-t * 26)

def music_bed(n):
    t = np.arange(n) / SR
    m = np.zeros(n)
    inten = np.zeros(n)
    I = [0.82, 0.58, 0.62, 0.66, 0.68, 0.72, 0.66, 0.78, 0.56, 0.70]
    for i, b in enumerate(BEATS):
        e = BEATS[i + 1] if i + 1 < len(BEATS) else TOTAL
        inten[_n(b):min(_n(e), n)] = I[i]
    inten = box(inten, _n(2.2))
    for f, g in [(73.42, 1.0), (110.0, 0.45), (36.71, 0.6)]:
        m += g * (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.0045 * t + 0.9)) * 0.5
    m *= 0.046 * (0.65 + 0.35 * np.sin(2 * np.pi * 0.035 * t))
    pad = (np.sin(2 * np.pi * 293.66 * t) + np.sin(2 * np.pi * 295.1 * t)
           + np.sin(2 * np.pi * 440.0 * t) * 0.5)
    m += pad * 0.0055 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * t + 2.0))
    rs = np.random.RandomState(41)
    for bi in (0, 4, 5):
        for _ in range(9):
            at = BEATS[bi] + 2 + rs.rand() * (DUR[bi] - 2)
            x = ping(1800 + rs.rand() * 1600, 0.02, 0.5); i0 = _n(at)
            if i0 + len(x) < n: m[i0:i0 + len(x)] += x
    for b in BEATS[1:]:
        r = envad(box(noise(1.3, 13), 8) - box(noise(1.3, 13), 100), 1.1, 0.18) * 1.6
        i0 = _n(b - 1.3)
        if i0 >= 0:
            ln = min(len(r), n - i0); m[i0:i0 + ln] += r[:ln] * 0.15
    m *= inten
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
    # word-sync paper pops + thuds
    PCUT = [(0,"chain"),(0,"ganesh"),(0,"title"),(1,"shesh"),(1,"ratn"),(2,"puran"),(2,"shesh"),
            (4,"shesh"),(5,"ganesh"),(6,"jata"),(6,"bhair"),(9,"map")]
    put(paper(0.6), BEATS[8] + 2.0); put(thud(0.45), BEATS[8] + 2.05)
    for bi, k in PCUT:
        at = B[bi] + KT[bi][k]
        put(paper(0.65), at - 0.04); put(thud(0.5), at)
    # ch0 hook
    put(subboom(0.7), 0.3)
    put(thud(0.9), B[0] + KT[0]["ft90"]); put(ping(294, 0.2, 1.4), B[0] + KT[0]["ft90"] + 0.05)
    put(subboom(0.8), B[0] + KT[0]["title"]); put(bell(587, 0.18), B[0] + KT[0]["title"] + 0.1)
    # ch1 lok bars
    for k in range(7): put(tickk(900 + k * 60, 0.18, 0.04), B[1] + 2.2 + k * 0.3)
    for k in range(7): put(tickk(700 - k * 40, 0.18, 0.04), B[1] + 5.4 + k * 0.3)
    put(thud(0.8), B[1] + KT[1]["patal"])
    # ch2 timeline pings
    for k0 in ("raja","pandav","shankar"): put(ping(523, 0.18, 0.9), B[2] + KT[2][k0])
    put(bell(523, 0.12), B[2] + KT[2]["shankar"] + 0.4)
    # ch3 gates
    for k0 in ("g1","g2","g3","g4"): put(thud(0.55), B[3] + KT[3][k0])
    put(tickk(500, 0.35, 0.08), B[3] + KT[3]["band1"]); put(tickk(460, 0.35, 0.08), B[3] + KT[3]["band2"])
    put(ping(392, 0.2, 1.2), B[3] + KT[3]["two"])
    # ch4 chains + ribs
    for k in range(6): put(tickk(620 - k * 30, 0.16, 0.05), B[4] + KT[4]["chain"] + k * 0.5)
    put(subboom(0.6), B[4] + KT[4]["back"])
    # ch5 drips
    for k in range(8): put(drip(0.16), B[5] + KT[5]["kamal"] + 0.8 + k * 1.1)
    put(bell(660, 0.14), B[5] + KT[5]["ganesh"] + 0.2)
    # ch6 chips + moksha
    for k0 in ("ked","bad","amar"): put(pop(0.5), B[6] + KT[6][k0])
    put(ping(880, 0.2, 1.0), B[6] + KT[6]["moksh"])
    # ch7 yug stones
    for k0 in ("y1","y2","y3"): put(thud(0.5), B[7] + KT[7][k0])
    put(subboom(0.75), B[7] + KT[7]["y4"])
    put(envad(tone(2.2, 160, 60, 0.12), 0.3, 1.4), B[7] + KT[7]["touch"])
    put(thud(1.0), B[7] + KT[7]["ant"]); put(bell(494, 0.2), B[7] + KT[7]["ant"] + 0.05)
    # ch8 drips + ticks
    for k in range(6): put(drip(0.14), B[8] + 3.0 + k * 1.6)
    # ch9 cta
    put(pop(0.5), B[9] + KT[9]["sub"]); put(pop(0.55), B[9] + KT[9]["sub"] + 0.7)
    put(bell(587, 0.16), B[9] + KT[9]["km"])
    # VO
    vo = np.zeros(n)
    for i, nm in enumerate(ORDER):
        wv = os.path.join(ROOT, "qvo_%s.wav" % nm)
        if not os.path.exists(wv):
            subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(PT, "vo2", "qvo_%s.mp3" % nm),
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
const W=1920,H=1080,TOTAL=__TOT__,B=BEATSJ,DUR=DURJ,LEAD=0.5,CAPS=CAPSJ,KT=KTJ;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const ov=x=>{x=clamp(x,0,1);const c=1.7,u=x-1;return 1+u*u*((c+1)*u+c)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
const CYAN='#4dd8ff',ORG='#ff8c3b',PAPER='#eef2f8',RED='#e8503a',GOLD='#e8b24a';
const IMGS={};let nimg=0,want=14;
function ld(k,s){const im=new Image();im.onload=()=>nimg++;im.src=s;IMGS[k]=im;}
ld('shesh','data:image/jpeg;base64,SHESH64');
ld('ganesh','data:image/jpeg;base64,GAN64');
ld('bhair','data:image/jpeg;base64,BHAIR64');
ld('naag','data:image/jpeg;base64,NAAG64');
ld('khz','data:image/jpeg;base64,KHZ64');
ld('map','data:image/jpeg;base64,MAP64');
ld('shrine','data:image/jpeg;base64,SHRINE64');
ld('temple','data:image/jpeg;base64,TEMPLE64');
ld('logo','data:image/png;base64,LOGO64');
ld('rshesh','data:image/jpeg;base64,RSHESH64');
ld('rganesh','data:image/jpeg;base64,RGAN64');
ld('rchain','data:image/jpeg;base64,RCHAIN64');
ld('rshiv','data:image/jpeg;base64,RSHIV64');
ld('rdome','data:image/jpeg;base64,RDOME64');
const VIDS={};let nvid=0;const wantvid=12;
function lv(k,b){const v=document.createElement('video');v.muted=true;v.preload='auto';
 v.addEventListener('loadeddata',()=>nvid++);v.src='data:video/mp4;base64,'+b;VIDS[k]=v;}
lv('fog','VFOG64');lv('fire','VFIRE64');lv('ray','VRAY64');lv('rock','VROCK64');
lv('pit','VPIT64');lv('gold','VGOLD64');lv('forest','VFOREST64');lv('him','VHIM64');
lv('pan','VPAN64');lv('valley','VVALLEY64');lv('snk1','VSNK164');lv('snk2','VSNK264');
function seekV(v,t){return new Promise(r=>{const tt=Math.max(0.04,Math.min(t,v.duration-0.06));
 if(Math.abs(v.currentTime-tt)<0.001)return r();
 const h=()=>{v.removeEventListener('seeked',h);r();};v.addEventListener('seeked',h);v.currentTime=tt;});}
function coverV(v,zoom,cx,cy,dim){
 const vw=v.videoWidth,vh=v.videoHeight;if(!vw)return;
 const sc=Math.max(W/vw,H/vh)*zoom;
 g.drawImage(v,W*cx-vw*sc*cx,H*cy-vh*sc*cy,vw*sc,vh*sc);
 if(dim>0){g.save();g.globalAlpha=dim;g.fillStyle='#050308';g.fillRect(0,0,W,H);g.restore();}}
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
const DUST=[];{const r=rng(55);for(let i=0;i<90;i++)DUST.push([r()*W,r()*H,r()*2.2+0.6,r()*6.28,0.15+r()*0.3]);}
function caveBG(t){
 g.fillStyle='#07050a';g.fillRect(0,0,W,H);
 for(let i=0;i<3;i++){
  const bx=((i*650+t*(8+5*i))%(W+800))-400, by=250+i*280+30*Math.sin(t*0.25+i*2);
  const gr=g.createRadialGradient(bx,by,40,bx,by,520);
  const col=i===1?'rgba(90,60,30,0.10)':'rgba(50,35,70,0.10)';
  gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=gr;g.fillRect(0,0,W,H);}
 for(const s of DUST){
  const x=(s[0]+t*6*(1+s[2]*0.3))%W, y=(s[1]+t*3)%H;
  const a=s[4]*(0.5+0.5*Math.sin(t*1.1+s[3]));
  g.save();g.globalAlpha=a;g.fillStyle='#d8c9a8';
  g.beginPath();g.arc(x,y,s[2],0,6.29);g.fill();g.restore();}}
function drawBG(sh,t){
 if(!sh){g.fillStyle='#07050a';g.fillRect(0,0,W,H);return;}
 if(sh.v==='ANIM'){caveBG(t);return;}
 const punch=1+0.06*Math.exp(-sh.since*5);
 const v=VIDS[sh.v];
 if(v&&v.videoWidth)coverV(v,sh.z*punch+0.02*Math.sin(t*0.2),sh.cx,sh.cy,sh.dim);
 else caveBG(t);}
const noiseCv=document.createElement('canvas');noiseCv.width=480;noiseCv.height=270;
{const nc=noiseCv.getContext('2d');const id=nc.createImageData(480,270);const rn=rng(9);
for(let i=0;i<id.data.length;i+=4){const v=rn()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=13;}nc.putImageData(id,0,0);}
const vig=document.createElement('canvas');vig.width=W;vig.height=H;
{const vc=vig.getContext('2d');const gr=vc.createRadialGradient(W/2,H*0.46,H*0.4,W/2,H*0.5,H*1.05);
gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(4,2,6,0.58)');vc.fillStyle=gr;vc.fillRect(0,0,W,H);}
function T(x,y,txt,font,size,color,align,alpha,ls){
 g.save();g.globalAlpha=alpha==null?1:alpha;g.fillStyle=color;g.font=size+'px '+font;
 g.textAlign=align||'center';g.textBaseline='middle';
 if(ls){let tw=0;for(const ch of txt)tw+=g.measureText(ch).width+ls;tw-=ls;
  let cx=(align==='left')?x:(align==='right'?x-tw:x-tw/2);g.textAlign='left';
  for(const ch of txt){g.fillText(ch,cx,y);cx+=g.measureText(ch).width+ls;}}
 else g.fillText(txt,x,y);g.restore();}
function rrect(x,y,w2,h2,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w2,y,x+w2,y+h2,r);g.arcTo(x+w2,y+h2,x,y+h2,r);g.arcTo(x,y+h2,x,y,r);g.arcTo(x,y,x+w2,y,r);g.closePath();}
function figbar(lt,left,right){
 const a=ss(0.2,0.8,lt);if(a<=0)return;
 g.save();g.globalAlpha=a;g.strokeStyle='rgba(222,234,248,0.6)';g.lineWidth=2;
 g.beginPath();g.moveTo(140,86);g.lineTo(140+1640*ss(0.2,1.1,lt),86);g.stroke();
 g.font='26px Mono';g.textBaseline='bottom';
 g.fillStyle=GOLD;g.textAlign='left';g.fillText(left,140,76);
 g.fillStyle='rgba(222,234,248,0.6)';g.textAlign='right';g.fillText(right,1780,76);g.restore();}
function kickerD(lt,t0,small,big,col){
 const p=ss(t0,t0+0.4,lt);if(p<=0)return;
 g.save();g.globalAlpha=p;
 T(140,176,small,'Mono',30,GOLD,'left',1,6);
 T(140,266,big,'Deva',72,col||PAPER,'left');g.restore();}
function tornPath(w2,h2,seed,m){
 const r=rng(seed);const pts=[];
 const step=46;
 for(let x=-w2/2;x<w2/2;x+=step)pts.push([x+r()*10,-h2/2-m+(r()-0.5)*14]);
 for(let y=-h2/2;y<h2/2;y+=step)pts.push([w2/2+m+(r()-0.5)*14,y+r()*10]);
 for(let x=w2/2;x>-w2/2;x-=step)pts.push([x-r()*10,h2/2+m+(r()-0.5)*14]);
 for(let y=h2/2;y>-h2/2;y-=step)pts.push([-w2/2-m+(r()-0.5)*14,y-r()*10]);
 g.beginPath();g.moveTo(pts[0][0],pts[0][1]);
 for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);
 g.closePath();}
function papercut(t,t0,im,x,y,wpx,rot,labL,labR,labCol,seed){
 const p=ss(t0,t0+0.38,t);if(p<=0)return;
 const hpx=wpx*im.height/im.width;
 const drop=(1-ov(p))*-90;
 const ga0=g.globalAlpha;g.save();g.globalAlpha=Math.min(1,p*1.2)*ga0;
 g.translate(x,y+drop);g.rotate(rot+0.01*Math.sin(t*1.1+seed));
 const sc=0.92+0.08*ov(p);g.scale(sc,sc);
 g.shadowColor='rgba(0,0,0,0.65)';g.shadowBlur=34;g.shadowOffsetY=14;
 g.fillStyle='#f3eee0';tornPath(wpx,hpx,seed,20);g.fill();
 g.shadowColor='transparent';
 g.save();tornPath(wpx,hpx,seed+1,2);g.clip();
 g.drawImage(im,-wpx/2,-hpx/2,wpx,hpx);g.restore();
 g.fillStyle='rgba(232,226,200,0.55)';g.strokeStyle='rgba(180,170,140,0.4)';g.lineWidth=1;
 g.save();g.rotate(-0.06);g.fillRect(-70,-hpx/2-34,140,36);g.strokeRect(-70,-hpx/2-34,140,36);g.restore();
 g.fillStyle='#2a2318';g.font='26px Mono';g.textAlign='left';g.textBaseline='middle';
 g.fillText(labL,-wpx/2+6,hpx/2+44);
 g.font='19px Mono';g.fillStyle=labCol;g.textAlign='right';
 g.fillText(labR,wpx/2-4,hpx/2+44);
 g.restore();}
function kword(t,t0,txt,x,y,col){
 const p=ss(t0,t0+0.2,t);if(p<=0)return;
 const a=p*(1-ss(t0+1.7,t0+2.2,t));if(a<=0)return;
 const sc=1.7-0.7*ov(p);
 g.save();g.globalAlpha=a;g.translate(x,y);g.scale(sc,sc);g.rotate(-0.03);
 g.font='60px Deva';g.textAlign='center';g.textBaseline='middle';
 g.lineWidth=10;g.strokeStyle='rgba(5,3,8,0.85)';g.strokeText(txt,0,0);
 g.fillStyle=col;g.fillText(txt,0,0);g.restore();}
function stampD(t,t0,x,y,txt,color,size,rot){
 const p=ss(t0,t0+0.22,t);if(p<=0)return;
 const s=2.0-1.0*ov(p);
 g.save();g.translate(x,y);g.rotate(rot||-0.06);g.scale(s,s);g.globalAlpha=p*0.95;
 g.strokeStyle=color;g.fillStyle=color;g.lineWidth=6;
 g.font=size+'px Deva';g.textAlign='center';g.textBaseline='middle';
 const tw=g.measureText(txt).width;
 rrect(-tw/2-28,-size*0.88,tw+56,size*1.76,10);g.stroke();g.fillText(txt,0,3);g.restore();}
function typew(lt,t0,txt,cps,x,y,font,size,color,align){
 if(lt<t0)return;const n=Math.floor((lt-t0)*cps);const s=txt.slice(0,n);
 const c=(n<txt.length)&&(Math.floor(lt*3)%2===0);
 T(x,y,s+(c?'_':''),font,size,color,align||'left',Math.min(1,(lt-t0)*4));}
function chip(t,t0,x,y,txt,col,w2){
 const p=ss(t0,t0+0.4,t);if(p<=0)return;
 g.save();g.globalAlpha=p;g.translate(x,y+(1-ov(p))*40);
 g.fillStyle='rgba(10,8,16,0.8)';g.strokeStyle=col;g.lineWidth=2;
 rrect(-w2/2,-42,w2,84,14);g.fill();g.stroke();
 T(0,2,txt,'Deva',36,col,'center');g.restore();}
// ============ CHAPTERS ============
function fig0(t,lt){
 const K=KT[0];
 figbar(lt,'UTTARAKHAND \u00b7 EK DARWAZA','FIG. 01 \u00b7 CHRONIC JOURNAL');
 typew(lt,0.8,'PAHADON MEIN CHHUPA...',13,140,176,'Mono',32,'rgba(238,242,248,0.9)','left');
 const f9=ss(K.ft90,K.ft90+0.3,lt)*(1-ss(K.title-1.0,K.title-0.4,lt));
 if(f9>0){g.save();const sc=1.8-0.8*ov(f9);g.globalAlpha=f9;
  g.translate(300,0);g.scale(sc,sc);
  T(0,400/sc,'90 FT','Anton',150,ORG,'center');
  g.restore();
  T(300,510,'\u0928\u0940\u091a\u0947\u2026 \u0905\u0902\u0927\u0947\u0930\u0947 \u092e\u0947\u0902','Deva',36,PAPER,'center',ss(K.ft90+0.3,K.ft90+0.7,lt));}
 g.save();g.globalAlpha=1-ss(K.title-1.3,K.title-0.6,lt);
 if(IMGS.rchain.width)papercut(lt,K.chain,IMGS.rchain,390,690,560,-0.025,'ZANJEER \u00b7 SANKRI SURANG','REAL PHOTO','#2a6a3a',29);
 g.restore();g.globalAlpha=1;
 if(IMGS.ganesh.width)papercut(lt,K.ganesh,IMGS.ganesh,1380,470,560,0.04,'ADI GANESH','AI ART','#7a5a20',31);
 kword(lt,K.ganesh,'\u0917\u0923\u0947\u0936 \u0915\u093e \u0938\u093f\u0930',1380,140,ORG);
 const ti=ss(K.title,K.title+0.5,lt);
 if(ti>0){g.save();const sc=1.5-0.5*ov(ti);g.globalAlpha=ti;
  g.translate(620,0);g.scale(sc,sc);
  T(0,760/sc,'\u092a\u093e\u0924\u093e\u0932 \u092d\u0941\u0935\u0928\u0947\u0936\u094d\u0935\u0930','Deva',104,PAPER,'center');g.restore();
  T(620,862,'THE CAVE OF THE UNDERWORLD','Mono',26,GOLD,'center',ss(K.title+0.4,K.title+0.8,lt),5);}
 typew(lt,K.last,'AAKHRI KONE TAK \u2192',12,140,620,'Mono',30,CYAN,'left');
}
function fig1(t,lt){
 const K=KT[1];
 figbar(lt,'14 LOK \u00b7 HINDU GRANTH','FIG. 02');
 kickerD(lt,0.5,'BRAHMAND KA NAKSHA','\u091a\u094c\u0926\u0939 \u0932\u094b\u0915');
 const cx=640,midY=520,bw=340,bh2=30,gap=9;
 g.save();
 const pl=ss(1.5,2.2,lt);
 if(pl>0){g.globalAlpha=pl;g.strokeStyle='rgba(238,242,248,0.7)';g.lineWidth=3;
  g.beginPath();g.moveTo(cx-bw/2-50,midY);g.lineTo(cx+bw/2+50,midY);g.stroke();
  T(cx+bw/2+70,midY,'\u0927\u0930\u0924\u0940','Deva',28,PAPER,'left',pl);}
 for(let i=0;i<7;i++){
  const p=ss(2.2+i*0.3,2.6+i*0.3,lt);if(p<=0)continue;
  const y=midY-16-(i+1)*(bh2+gap);
  g.globalAlpha=p*(0.35+0.09*i);g.fillStyle=CYAN;
  rrect(cx-bw/2,y,bw*p,bh2,6);g.fill();}
 for(let i=0;i<7;i++){
  const p=ss(5.4+i*0.3,5.8+i*0.3,lt);if(p<=0)continue;
  const y=midY+16+i*(bh2+gap);
  const last=(i===6);
  g.globalAlpha=p*(last?0.95:(0.8-0.09*i));g.fillStyle=last?ORG:GOLD;
  if(last){const pu=0.75+0.25*Math.sin(t*3);g.globalAlpha=p*pu;}
  rrect(cx-bw/2,y,bw*p,bh2,6);g.fill();}
 g.restore();
 const pp=ss(K.patal,K.patal+0.4,lt);
 if(pp>0){const y2=midY+16+6*(bh2+gap)+bh2/2;
  g.save();const sc=1.5-0.5*ov(pp);g.globalAlpha=pp;
  g.translate(cx+bw/2+55,y2);g.scale(sc,sc);
  T(0,0,'\u092a\u093e\u0924\u093e\u0932','Deva',50,ORG,'left');g.restore();}
 if(IMGS.shesh.width)papercut(lt,K.shesh,IMGS.shesh,1430,540,560,-0.04,'SHESHNAG \u00b7 DHARTI','AI ART','#7a5a20',41);
 kword(lt,K.shesh,'\u0936\u0947\u0937\u0928\u093e\u0917',1430,170,GOLD);
 if(IMGS.khz.width)papercut(lt,K.ratn,IMGS.khz,1180,850,330,0.05,'RATN','AI ART','#7a5a20',43);
}
function fig2(t,lt){
 const K=KT[2];
 figbar(lt,'SKAND PURAN \u00b7 MANAS KHAND','FIG. 03');
 kickerD(lt,0.5,'KATHA \u00b7 TEEN YUG','\u0917\u0941\u092b\u093e \u0915\u0940 \u0915\u0939\u093e\u0928\u0940');
 const y=560,x0=220,x1=1700;
 const tl=ss(1.8,3.2,lt);
 if(tl>0){g.save();g.globalAlpha=0.9;g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=3;
  g.beginPath();g.moveTo(x0,y);g.lineTo(x0+(x1-x0)*tl,y);g.stroke();g.restore();}
 const stops=[[K.raja,'\u0924\u094d\u0930\u0947\u0924\u093e \u092f\u0941\u0917','\u0930\u093e\u091c\u093e \u090b\u0924\u0941\u092a\u0930\u094d\u0923',0.18,GOLD],
              [K.pandav,'\u0926\u094d\u0935\u093e\u092a\u0930','\u092a\u093e\u0902\u0921\u0935',0.5,CYAN],
              [K.shankar,'\u0915\u0932\u093f\u092f\u0941\u0917','\u0906\u0926\u093f \u0936\u0902\u0915\u0930\u093e\u091a\u093e\u0930\u094d\u092f',0.82,ORG]];
 for(const[t0,era,who,fx,col]of stops){
  const p=ss(t0,t0+0.4,lt);if(p<=0)continue;
  const x=x0+(x1-x0)*fx;
  g.save();g.globalAlpha=p;
  g.fillStyle=col;g.beginPath();g.arc(x,y,10,0,6.29);g.fill();
  const ph=(t*0.7)%1;g.globalAlpha=p*(1-ph);g.strokeStyle=col;g.lineWidth=3;
  g.beginPath();g.arc(x,y,12+ph*44,0,6.29);g.stroke();
  g.globalAlpha=p;
  T(x,y-66,era,'Mono',24,col,'center',p,2);
  T(x,y+70,who,'Deva',34,PAPER,'center',p);g.restore();}
 if(IMGS.naag.width)papercut(lt,K.shesh,IMGS.naag,1490,850,360,0.04,'SHESHNAG DWAR PAR','AI ART','#7a5a20',52);
 typew(lt,K.shankar+2.5,'TAB SE PUJA KABHI NAHI RUKI',12,140,900,'Mono',28,'rgba(238,242,248,0.85)','left');
}
function fig3(t,lt){
 const K=KT[3];
 figbar(lt,'CHAR DWAR','FIG. 04');
 kickerD(lt,0.5,'GUFA KE RASTE','\u091a\u093e\u0930 \u0926\u094d\u0935\u093e\u0930');
 const names=['\u0930\u0923\u0926\u094d\u0935\u093e\u0930','\u092a\u093e\u092a\u0926\u094d\u0935\u093e\u0930','\u0927\u0930\u094d\u092e\u0926\u094d\u0935\u093e\u0930','\u092e\u094b\u0915\u094d\u0937\u0926\u094d\u0935\u093e\u0930'];
 const ts=[K.g1,K.g2,K.g3,K.g4];
 for(let i=0;i<4;i++){
  const p=ss(ts[i],ts[i]+0.45,lt);if(p<=0)continue;
  const x=430+i*360,y=560;
  const closed=(i<2)&&lt>(i===0?K.band2:K.band1);
  g.save();g.globalAlpha=p;g.translate(x,y+(1-ov(p))*60);
  // arch gate
  g.strokeStyle=closed?'rgba(232,80,58,0.9)':GOLD;g.lineWidth=7;
  g.beginPath();g.moveTo(-85,150);g.lineTo(-85,-40);g.arc(0,-40,85,Math.PI,0);g.lineTo(85,150);g.stroke();
  g.strokeStyle=closed?'rgba(232,80,58,0.45)':'rgba(232,178,74,0.4)';g.lineWidth=3;
  g.beginPath();g.moveTo(-60,150);g.lineTo(-60,-36);g.arc(0,-36,60,Math.PI,0);g.lineTo(60,150);g.stroke();
  if(!closed){const gl=0.25+0.2*Math.sin(t*2+i);
   const gr=g.createRadialGradient(0,30,10,0,30,130);
   gr.addColorStop(0,'rgba(232,178,74,'+gl+')');gr.addColorStop(1,'rgba(0,0,0,0)');
   g.fillStyle=gr;g.fillRect(-90,-130,180,290);}
  if(closed){g.strokeStyle=RED;g.lineWidth=10;
   g.beginPath();g.moveTo(-70,-90);g.lineTo(70,120);g.moveTo(70,-90);g.lineTo(-70,120);g.stroke();}
  T(0,210,names[i],'Deva',34,closed?RED:PAPER,'center');
  if(closed)T(0,-160,'BAND',' Mono'.trim(),26,RED,'center',1,4);
  g.restore();}
 const tw2=ss(K.two,K.two+0.5,lt);
 if(tw2>0)T(960,900,'\u0905\u092c \u0938\u093f\u0930\u094d\u092b \u0926\u094b \u0930\u093e\u0938\u094d\u0924\u0947 \u2014 \u0927\u0930\u094d\u092e\u2026 \u0914\u0930 \u092e\u094b\u0915\u094d\u0937','Deva',42,GOLD,'center',tw2);
}
function fig4(t,lt){
 const K=KT[4];
 figbar(lt,'90 FT NEECHE','FIG. 05');
 kickerD(lt,0.5,'SANKRI SURANG \u00b7 ZANJEER','\u0909\u0924\u0930\u093e\u0908 \u0936\u0941\u0930\u0942');
 // depth meter + chain
 const dm=ss(K.chain,K.chain+0.5,lt);
 if(dm>0){const x=190,y0=360,y1=880;
  g.save();g.globalAlpha=dm;
  g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=3;
  g.beginPath();g.moveTo(x,y0);g.lineTo(x,y1);g.stroke();
  for(let k=0;k<10;k++){const yy=y0+28+k*52+8*Math.sin(t*1.4+k);
   g.strokeStyle='rgba(200,210,225,0.55)';g.lineWidth=5;
   g.beginPath();g.ellipse(x+60,yy,10,16,0,0,6.29);g.stroke();}
  g.font='22px Mono';g.fillStyle='rgba(238,242,248,0.7)';g.textAlign='left';
  [['0 FT',y0],['45 FT',(y0+y1)/2],['90 FT',y1]].forEach(p2=>{
   g.strokeStyle='rgba(238,242,248,0.5)';g.lineWidth=3;
   g.beginPath();g.moveTo(x-10,p2[1]);g.lineTo(x+10,p2[1]);g.stroke();
   g.fillText(p2[0],x-66,p2[1]+7);});
  const prog=clamp((lt-K.chain)/8,0,1);
  g.fillStyle=ORG;g.beginPath();g.arc(x,y0+(y1-y0)*prog,10,0,6.29);g.fill();
  g.restore();}
 // ribs waves
 const rb=ss(K.ribs,K.ribs+0.6,lt);
 if(rb>0){g.save();g.globalAlpha=rb*0.85;g.strokeStyle=GOLD;g.lineWidth=4;
  for(let k=0;k<7;k++){const y=700+k*34;
   g.beginPath();
   for(let x=420;x<=1180;x+=20){
    const yy=y+10*Math.sin((x-420)*0.02+k*0.7+t*0.6);
    if(x===420)g.moveTo(x,yy);else g.lineTo(x,yy);}
   g.stroke();}
  T(800,640,'\u092a\u0938\u0932\u093f\u092f\u094b\u0902 \u091c\u0948\u0938\u0940 \u091a\u091f\u094d\u091f\u093e\u0928\u0947\u0902','Deva',34,GOLD,'center',rb);
  g.restore();}
 if(IMGS.rshesh.width)papercut(lt,K.shesh,IMGS.rshesh,1460,500,600,0.03,'SHESHNAG SHILA \u00b7 ASLI CHATTAN','REAL PHOTO','#2a6a3a',61);
 kword(lt,K.shesh,'\u0936\u0947\u0937\u0928\u093e\u0917 \u0915\u0940 \u092a\u0940\u0920',1480,160,GOLD);
 const bk=ss(K.back,K.back+0.5,lt);
 if(bk>0)T(760,920,'\u0914\u0930 \u0924\u0941\u092e\u2026 \u0909\u0938\u0915\u0940 \u092a\u0940\u0920 \u092a\u0930 \u091a\u0932 \u0930\u0939\u0947 \u0939\u094b','Deva',40,ORG,'center',bk);
}
function fig5(t,lt){
 const K=KT[5];
 figbar(lt,'SABSE BADA RAHASYA','FIG. 06');
 kickerD(lt,0.5,'GUFA KA GARBH','\u0906\u0926\u093f \u0917\u0923\u0947\u0936');
 if(IMGS.rganesh.width)papercut(lt,K.ganesh+0.6,IMGS.rganesh,420,470,400,-0.03,'ADI GANESH SHILA','REAL PHOTO','#2a6a3a',72);
 if(IMGS.ganesh.width)papercut(lt,K.ganesh,IMGS.ganesh,1180,520,700,0.02,'ADI GANESH \u00b7 BRAHMAKAMAL','AI ART','#7a5a20',71);
 kword(lt,K.ganesh,'\u0906\u0926\u093f \u0917\u0923\u0947\u0936',1180,140,ORG);
 // falling droplet loop after kamal
 if(lt>K.kamal){
  const ph=((lt-K.kamal)%1.1)/1.1;
  const dx=1180,dy0=240,dy1=760;
  const y=dy0+(dy1-dy0)*ph*ph;
  g.save();g.globalAlpha=0.9*(1-ss(0.92,1,ph));
  g.fillStyle='rgba(150,220,255,0.9)';
  g.beginPath();g.ellipse(dx,y,7,12,0,0,6.29);g.fill();g.restore();
  if(ph>0.92){g.save();g.globalAlpha=(1-ph)*8*0.5;g.strokeStyle=CYAN;g.lineWidth=3;
   g.beginPath();g.ellipse(dx,dy1+10,30*(ph-0.9)*12,10*(ph-0.9)*12,0,0,6.29);g.stroke();g.restore();}}
 kword(lt,K.kamal,'\u092c\u094d\u0930\u0939\u094d\u092e\u0915\u092e\u0932',520,300,CYAN);
 const yr=ss(K.years,K.years+0.5,lt);
 if(yr>0)T(420,915,'\u0939\u095b\u093e\u0930\u094b\u0902 \u0938\u093e\u0932\u094b\u0902 \u0938\u0947\u2026 \u092c\u093f\u0928\u093e \u0930\u0941\u0915\u0947','Deva',42,ORG,'center',yr);
}
function fig6(t,lt){
 const K=KT[6];
 figbar(lt,'DEVTAON KA GHAR','FIG. 07');
 kickerD(lt,0.5,'EK HI GUFA MEIN','33 \u0915\u094b\u091f\u093f \u0926\u0947\u0935\u0924\u093e');
 // ceiling sparkle stars
 if(lt>K.koti){const r=rng(17);
  for(let i=0;i<40;i++){
   const x=300+r()*1350,y=150+r()*210;
   const a=(0.3+0.7*Math.sin(t*2.2+i*1.3)**2)*ss(K.koti,K.koti+1.2,lt);
   g.save();g.globalAlpha=Math.max(0,a*0.9);g.fillStyle=i%3?GOLD:'#fff';
   g.translate(x,y);g.rotate(0.785);g.fillRect(-4,-4,8,8);g.restore();}}
 chip(lt,K.ked,560,480,'\u0915\u0947\u0926\u093e\u0930\u0928\u093e\u0925',CYAN,300);
 chip(lt,K.bad,900,480,'\u092c\u0926\u094d\u0930\u0940\u0928\u093e\u0925',GOLD,300);
 chip(lt,K.amar,1240,480,'\u0905\u092e\u0930\u0928\u093e\u0925',ORG,300);
 if(IMGS.rshiv.width)papercut(lt,K.jata,IMGS.rshiv,420,720,340,0.03,'SHIV MAHASHAKTI','REAL PHOTO','#2a6a3a',82);
 if(IMGS.bhair.width)papercut(lt,K.bhair,IMGS.bhair,1360,790,560,-0.03,'KALBHAIRAV KI JEEBH','AI ART','#7a5a20',81);
 kword(lt,K.bhair,'\u0915\u093e\u0932\u092d\u0948\u0930\u0935',1360,560,RED);
 stampD(lt,K.moksh,790,860,'\u092e\u094b\u0915\u094d\u0937 \u0915\u093e \u0930\u093e\u0938\u094d\u0924\u093e',CYAN,38,-0.05);
}
function fig7(t,lt){
 const K=KT[7];
 figbar(lt,'SABSE BADA SAWAL','FIG. 08');
 kickerD(lt,0.5,'CHAR PATTHAR \u00b7 CHAR YUG','\u0915\u0932\u093f\u092f\u0941\u0917 \u0915\u093e \u092a\u0924\u094d\u0925\u0930');
 const names=['\u0938\u0924\u092f\u0941\u0917','\u0924\u094d\u0930\u0947\u0924\u093e','\u0926\u094d\u0935\u093e\u092a\u0930','\u0915\u0932\u093f\u092f\u0941\u0917'];
 const ts=[K.y1,K.y2,K.y3,K.y4];
 const baseY=820,ceilY=330;
 // ceiling line
 const cl=ss(K.y4,K.y4+0.6,lt);
 if(cl>0){g.save();g.globalAlpha=cl*0.8;g.setLineDash([14,10]);g.strokeStyle='rgba(238,242,248,0.6)';g.lineWidth=3;
  g.beginPath();g.moveTo(320,ceilY);g.lineTo(1600,ceilY);g.stroke();g.setLineDash([]);
  T(1620,ceilY,'\u091b\u0924','Deva',28,PAPER,'left',cl);g.restore();}
 g.save();g.strokeStyle='rgba(238,242,248,0.4)';g.lineWidth=3;
 const gl=ss(K.y1,K.y1+0.4,lt);
 if(gl>0){g.globalAlpha=gl;g.beginPath();g.moveTo(320,baseY);g.lineTo(1600,baseY);g.stroke();}
 g.restore();
 for(let i=0;i<4;i++){
  const p=ss(ts[i],ts[i]+0.5,lt);if(p<=0)continue;
  const x=480+i*320;
  let h2=120+i*26;
  if(i===3){const gr2=ss(K.grow,K.grow+6,lt);h2=200+gr2*200+6*Math.sin(t*1.8);}
  g.save();g.globalAlpha=p;
  const hot=i===3;
  g.fillStyle=hot?'rgba(232,80,58,0.85)':'rgba(180,160,120,0.7)';
  if(hot){const pu=0.7+0.3*Math.sin(t*3.2);g.globalAlpha=p*pu;}
  rrect(x-55,baseY-h2*p,110,h2*p,16);g.fill();
  g.globalAlpha=p;
  T(x,baseY+52,names[i],'Deva',34,hot?RED:PAPER,'center');
  if(hot&&lt>K.grow){
   g.strokeStyle=RED;g.lineWidth=3;g.setLineDash([8,8]);
   g.beginPath();g.moveTo(x,baseY-h2);g.lineTo(x,ceilY+8);g.stroke();g.setLineDash([]);
   const arr=0.5+0.5*Math.sin(t*4);
   T(x+70,(baseY-h2+ceilY)/2,'\u2191','Anton',50,RED,'center',arr);}
  g.restore();}
 stampD(lt,K.ant,1250,560,'\u0915\u0932\u093f\u092f\u0941\u0917 \u0915\u093e \u0905\u0902\u0924?',RED,44,0.04);
 const fl=ss(K.ant,K.ant+0.12,lt)*(1-ss(K.ant+0.12,K.ant+0.6,lt));
 if(fl>0){g.save();g.globalAlpha=fl*0.25;g.fillStyle=RED;g.fillRect(0,0,W,H);g.restore();}
}
function fig8(t,lt){
 const K=KT[8];
 figbar(lt,'VIGYAN KI NAZAR','FIG. 09');
 kickerD(lt,0.5,'LIMESTONE \u00b7 LAKHON SAAL','\u0935\u093f\u091c\u094d\u091e\u093e\u0928 \u0915\u094d\u092f\u093e \u0915\u0939\u0924\u093e \u0939\u0948');
 // stalactite/stalagmite diagram
 const cx=1280,topY=240,botY=900;
 const d1=ss(K.sta,K.sta+0.8,lt), d2=ss(K.stg,K.stg+0.8,lt);
 if(d1>0){g.save();g.globalAlpha=d1;
  g.fillStyle='rgba(120,104,76,0.85)';g.fillRect(cx-430,topY-26,860,26);
  g.fillStyle='rgba(180,160,120,0.75)';
  for(const[ox,w2,h2]of[[-160,60,180],[0,80,260],[150,55,150]]){
   g.beginPath();g.moveTo(cx+ox-w2,topY);g.lineTo(cx+ox+w2,topY);g.lineTo(cx+ox,topY+h2*d1);g.closePath();g.fill();}
  T(cx-380,topY+110,'STALACTITE \u2193','Mono',26,CYAN,'right',d1,2);
  g.restore();}
 if(d2>0){g.save();g.globalAlpha=d2;
  g.fillStyle='rgba(120,104,76,0.85)';g.fillRect(cx-430,botY,860,26);
  g.fillStyle='rgba(160,140,100,0.75)';
  for(const[ox,w2,h2]of[[-140,70,160],[20,90,230],[170,60,130]]){
   g.beginPath();g.moveTo(cx+ox-w2,botY);g.lineTo(cx+ox+w2,botY);g.lineTo(cx+ox,botY-h2*d2);g.closePath();g.fill();}
  T(cx-380,botY-90,'STALAGMITE \u2191','Mono',26,ORG,'right',d2,2);
  g.restore();}
 if(IMGS.rdome.width)papercut(lt,2.0,IMGS.rdome,480,470,460,-0.02,'ASLI AAKRITI \u00b7 GUFA KE ANDAR','REAL PHOTO','#2a6a3a',83);
 // dripping water between
 if(lt>K.sta){
  const ph=((lt-K.sta)%0.9)/0.9;
  const y=topY+270+(botY-230-(topY+270))*ph*ph;
  g.save();g.globalAlpha=0.85;g.fillStyle='rgba(150,220,255,0.85)';
  g.beginPath();g.ellipse(cx,y,6,10,0,0,6.29);g.fill();g.restore();}
 const vd=ss(K.dono,K.dono+0.5,lt);
 if(vd>0){g.save();g.globalAlpha=vd;
  g.fillStyle='rgba(8,8,14,0.82)';rrect(180,760,840,150,14);g.fill();
  g.strokeStyle=GOLD;g.lineWidth=2;rrect(180,760,840,150,14);g.stroke();
  T(600,812,'\u0906\u0938\u094d\u0925\u093e + \u0935\u093f\u091c\u094d\u091e\u093e\u0928','Deva',40,GOLD,'center');
  T(600,868,'\u0926\u094b\u0928\u094b\u0902 \u0905\u092a\u0928\u0940 \u091c\u0917\u0939 \u0938\u091a','Deva',32,PAPER,'center');g.restore();}
}
function fig9(t,lt){
 const K=KT[9];
 figbar(lt,'AGAR TUM JANA CHAHO','FIG. 10 \u00b7 YOUR TURN');
 if(IMGS.map.width)papercut(lt,K.map,IMGS.map,520,470,620,-0.03,'PITHORAGARH \u00b7 GANGOLIHAT','AI ART','#7a5a20',91);
 const km=ss(K.km,K.km+0.4,lt);
 if(km>0){g.save();g.globalAlpha=km;
  g.fillStyle='rgba(10,8,16,0.8)';g.strokeStyle=ORG;g.lineWidth=2;
  rrect(360,770,330,76,14);g.fill();g.stroke();
  T(525,810,'14 KM \u00b7 GANGOLIHAT','Mono',26,ORG,'center',1,1);g.restore();}
 if(IMGS.shrine.width)papercut(lt,1.2,IMGS.shrine,1430,330,480,0.04,'GUFA KE ANDAR','REAL PHOTO','#2a6a3a',93);
 const lg=ss(3.0,3.8,lt);
 if(lg>0&&IMGS.logo.width){const s2=520;
  g.save();g.globalAlpha=lg;
  const pu=1+0.012*Math.sin(t*2.2);
  g.translate(1430,760);g.scale(pu,pu);
  g.drawImage(IMGS.logo,-s2/2,-s2/2,s2,s2);g.restore();}
 const sb=ss(K.sub,K.sub+0.5,lt);
 if(sb>0){const pu=1+0.05*Math.sin(t*3.4)*(0.5+0.5*Math.sin(t*0.9));
  g.save();g.globalAlpha=sb;g.translate(960,940);g.scale(pu,pu);
  g.fillStyle=RED;rrect(-190,-44,380,88,16);g.fill();
  T(0,2,'\u25bc SUBSCRIBE','InterB',38,'#fff','center');g.restore();}
 const by=ss(DUR[9]+0.8,DUR[9]+1.6,lt);
 if(by>0)T(520,940,'\u092e\u093f\u0932\u0924\u0947 \u0939\u0948\u0902\u2026 \u0905\u0917\u0932\u0940 \u092f\u093e\u0924\u094d\u0930\u093e \u092e\u0947\u0902','Deva',40,GOLD,'center',by);
 const out=ss(DUR[9]+2.4,DUR[9]+3.8,lt);
 if(out>0){g.save();g.globalAlpha=out;g.fillStyle='#000';g.fillRect(0,0,W,H);g.restore();}
}
const FIGS=[fig0,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9];
function captions(t){
 let cur=null;
 for(const c of CAPS)if(t>=c.start&&t<c.end){cur=c;break;}
 if(!cur)return;
 const n=cur.words.length,prog=(t-cur.start)/(cur.end-cur.start);
 g.save();g.font='38px Deva';g.textBaseline='middle';
 const meas=cur.words.map(w=>g.measureText(w.replace('*','')+' ').width);
 let tw=0;for(const m of meas)tw+=m;
 let x=W/2-tw/2;const y=1006;
 g.shadowColor='rgba(0,0,0,0.75)';g.shadowBlur=10;
 cur.words.forEach((w,i)=>{
  const on=prog*n>=i;const hot=w[0]==='*';const txt=hot?w.slice(1):w;
  g.fillStyle=hot?ORG:'#ffffff';
  g.globalAlpha=on?1:0.3;g.textAlign='left';g.fillText(txt,x,y);x+=meas[i];});
 g.restore();}
function flash(lt){const a=1-ss(0,0.14,lt);if(a>0){g.save();g.globalAlpha=a*0.4;g.fillStyle='#ffe9cf';g.fillRect(0,0,W,H);g.restore();}}
async function draw(t){
 t=clamp(t,0,TOTAL-0.034);
 let bi=0;for(let i=0;i<B.length;i++)if(t>=B[i])bi=i;
 const lt=t-B[bi];
 const sh=shotAt(bi,lt);
 if(sh&&sh.v!=='ANIM'){const v=VIDS[sh.v];
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
  Promise.resolve().then(async()=>{await draw(1);await draw(60);await draw(150);await draw(250);window.__ready=true;}).catch(e=>{window.__err=''+(e.stack||e);});
 }else setTimeout(wait,60);};
 wait();}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff)
    html = html.replace("__TOT__", str(TOTAL)).replace("BEATSJ", json.dumps(BEATS)).replace("DURJ", json.dumps(DUR))
    html = html.replace("CAPSJ", json.dumps(caps)).replace("KTJ", json.dumps(KT))
    for tok, f in [("VFOG64","19212.mp4"),("VFIRE64","45321.mp4"),("VRAY64","47722.mp4"),
                   ("VROCK64","9758.mp4"),("VPIT64","26323.mp4"),("VGOLD64","32990.mp4"),
                   ("VFOREST64","20986.mp4"),("VHIM64","16130.mp4"),("VPAN64","45414.mp4"),
                   ("VVALLEY64","15919.mp4"),("VSNK164","11348.mp4"),("VSNK264","28368.mp4")]:
        html = html.replace(tok, b64("/var/tmp/stock/" + f))
    html = html.replace("SHOTSJ", json.dumps(SHOTS))
    html = html.replace("RSHESH64", b64(PT + "/real_shesh.jpg"))
    html = html.replace("RGAN64", b64(PT + "/real_ganesh.jpg"))
    html = html.replace("RCHAIN64", b64(PT + "/real_chain.jpg"))
    html = html.replace("RSHIV64", b64(PT + "/real_shiv.jpg"))
    html = html.replace("RDOME64", b64(PT + "/real_dome.jpg"))
    html = html.replace("SHESH64", b64(PT + "/card_sheshnag.jpg"))
    html = html.replace("GAN64", b64(PT + "/card_adiganesh.jpg"))
    html = html.replace("BHAIR64", b64(PT + "/card_kalbhairav.jpg"))
    html = html.replace("NAAG64", b64(PT + "/card_naag.jpg"))
    html = html.replace("KHZ64", b64(PR + "/prop_khazana.jpg"))
    html = html.replace("MAP64", b64(PR + "/prop_map.jpg"))
    html = html.replace("SHRINE64", b64(PT + "/photo_shrine.jpg"))
    html = html.replace("TEMPLE64", b64(PT + "/photo_temple.jpg"))
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
                                          " ".join(w.lstrip('*') for w in c["words"])))
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
