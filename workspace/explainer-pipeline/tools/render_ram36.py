#!/usr/bin/env python3
# VIDEO 36 — RAVAN KI LANKA: SACH KAHAN HAI? (MODE 1C locked formula + MODE 3D windows)
# Bespoke: line-art golden Lanka, map route, 7 nishan papercuts (REAL/AI tags),
# Mahavamsa twist, teen-gawah verdict. 3D: underwater setu glide + Ravana cave dolly.
import os, sys, io, json, base64, time, subprocess, wave
import numpy as np
from PIL import Image

ROOT = "/var/tmp/ram36"
TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(TOOLS, "..", "assets")
FONTS = os.path.join(ASSETS, "fonts")
RM = os.path.join(ASSETS, "ram36")
FF = "/var/tmp/pydeps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
CHROME = "/var/tmp/pwbrowsers/chromium-1248/chrome-linux64/chrome"
LOGO = "/home/user/uploads/file_00000000036082118b69837cc0b5e16e.png"
FPS = 30
W, H = 1920, 1080
DUR = [33.34, 28.06, 33.65, 36.46, 32.18, 40.54, 43.18, 42.10, 27.29, 14.69]
LEAD, GAP = 0.5, 1.0
BEATS = []
_t = 0.0
for d in DUR:
    BEATS.append(round(_t, 2)); _t += LEAD + d + GAP
TOTAL = round(_t + 2.5, 2)

VOTXT = [
 "हिंद महासागर में एक देश है... जहाँ रावण आज भी ज़िंदा है। झरनों में उसका नाम... गुफाओं में उसकी कहानी... और लोगों की कसमों में उसकी याद। लेकिन उसी देश की सबसे पुरानी इतिहास की किताब में... रावण का नाम तक नहीं मिलता। पच्चीस मीटर चौड़ा झरना... तेरह सौ मीटर ऊँची गुफा... और जली हुई लाल ज़मीन — सात निशान आज भी वहाँ खड़े हैं। तो सवाल ये है — रावण की लंका... सच कहाँ है? चलिए... ज़मीन से पूछते हैं।",
 "इन दिनों हर तरफ़ रामायण की चर्चा है — बड़े परदे पर एक नई फ़िल्म आ रही है। लेकिन आज हम परदे की नहीं... ज़मीन की बात करेंगे। श्रीलंका — जहाँ हर साल लाखों यात्री रामायण ट्रेल पर निकलते हैं। चौदह से ज़्यादा जगहें... जो इस महाकाव्य से जुड़ी मानी जाती हैं। और आज हम इनमें से सात सबसे रहस्यमयी निशान देखेंगे — परंपरा, ग्रंथ, और पुरातत्व — तीनों गवाहों के साथ।",
 "पहले ग्रंथ खोलते हैं। वाल्मीकि रामायण कहती है — लंका त्रिकूट पर्वत पर बसी थी... सोने की नगरी। विश्वकर्मा की बनाई... पहले कुबेर की... फिर रावण की। ऊँची दीवारें, भव्य द्वार, और आसमान में उड़ता पुष्पक विमान। सुंदरकांड में हनुमान जी इसे देखकर ठिठक जाते हैं — ऐसी नगरी उन्होंने पहले कभी नहीं देखी थी। यानी ग्रंथ हमें एक नक्शा देता है — पहाड़ पर बसा एक स्वर्ण नगर। अब सवाल ये — क्या ज़मीन पर ऐसा कुछ मिलता है?",
 "भारत के दक्षिणी छोर से चलिए। रामेश्वरम... फिर धनुषकोडी — एक उजड़ा हुआ कस्बा, जहाँ सड़क समंदर में खो जाती है। और उसके आगे... पानी के नीचे... अड़तालीस किलोमीटर लंबी एक रेखा — जो सीधे श्रीलंका तक जाती है। नासा की सैटेलाइट तस्वीरों में ये रेखा आज भी साफ़ दिखती है। कोई इसे राम सेतु कहता है... विज्ञान इसे रेत और चूना-पत्थर की शृंखला। पर हैरानी की बात — ये रेखा ठीक वहीं है, जहाँ ग्रंथ कहता है कि पुल बना था। चलिए... पानी के अंदर चलते हैं।",
 "श्रीलंका के पहाड़ों में, क़रीब सत्रह सौ मीटर की ऊँचाई पर... सीता एलिया। यहाँ है दुनिया का इकलौता सीता मंदिर — सीता अम्मन कोविल। परंपरा कहती है — यही थी अशोक वाटिका। मंदिर के पास बहती धारा के पार, चट्टान पर बने गड्ढे... जिन्हें श्रद्धालु हनुमान जी के पदचिह्न मानकर पूजते हैं। और पास ही हकगला — मान्यता है कि ये संजीवनी पर्वत का गिरा हुआ टुकड़ा है। और हैरानी ये... कि यहाँ हिमालय जैसी जड़ी-बूटियाँ आज भी उगती हैं।",
 "अब चलिए एला की घाटी में। रावण एला झरना — पच्चीस मीटर चौड़ा... श्रीलंका के सबसे चौड़े झरनों में से एक। परंपरा कहती है — बंदी सीता यहीं स्नान करती थीं। झरने से कुछ दूर, चट्टान में एक काला मुँह — रावण गुफा। और यहीं छिपा है पहला बड़ा चौंकाने वाला सच — पुरातत्वविदों को इस गुफा में प्रागैतिहासिक इंसान के निशान मिले हैं। यानी ये गुफा... कहानी से भी पुरानी है। और पास ही नील दिया पोकुना — ज़मीन के नीचे नीले पानी का रहस्यमयी कुंड... जिसे अभी आम लोगों के लिए बंद कर दिया गया है। वजह? आधिकारिक जवाब है — संरक्षण। लेकिन सवाल... सवाल तो उठते ही हैं।",
 "और अब सबसे बड़ा दावेदार। सिगिरिया — क़रीब दो सौ मीटर ऊँची चट्टान पर बसा किला। पुरातत्व कहता है — पाँचवीं सदी में राजा कश्यप ने इसे बनवाया। लेकिन परंपरा कुछ और कहती है — ये था रावण का आकाश महल... पहले कुबेर की नगरी। चट्टान के नीचे की कुछ गुफाएँ... कश्यप से भी पुरानी बताई जाती हैं। और फिर दक्षिणी तट पर... उस्सनगोडा। लाल, जली हुई, बंजर ज़मीन। परंपरा कहती है — यहाँ पुष्पक विमान उतरता था... और हनुमान जी की जलती पूँछ ने इसे झुलसा दिया। विज्ञान कहता है — यहाँ की मिट्टी सर्पेन्टाइन है, इसीलिए कुछ नहीं उगता। दो जवाब... एक ही ज़मीन।",
 "और अब वो सवाल... जो सब कुछ पलट देता है। महावंश — श्रीलंका की सबसे पुरानी इतिहास की किताब, क़रीब पाँचवीं सदी में लिखी गई। इसमें राजाओं की पूरी सूची है... लेकिन रावण का नाम... कहीं नहीं। तो क्या सब सिर्फ़ कहानी है? रुकिए। दिवुरुमपोला गाँव चलिए — परंपरा कहती है, यहीं हुई थी सीता माता की अग्नि परीक्षा। और आज भी... आपसी झगड़ों में लोग इसी जगह आकर कसम खाते हैं — और समाज उस कसम को मानता आया है। सोचिए — किताब में नाम नहीं... पर ज़िंदगी में भरोसा पूरा। शायद कुछ चीज़ें किताबों में नहीं... ज़िंदगी में लिखी जाती हैं।",
 "तो फ़ैसला क्या है? पत्थर गवाह हैं — झरना, गुफा, लाल ज़मीन, पदचिह्न। किताब ख़ामोश है — महावंश में नाम नहीं। और परंपरा... परंपरा ज़िंदा है — मंदिरों में, कसमों में, और उन लाखों क़दमों में जो हर साल इन रास्तों पर चलते हैं। आस्था अपनी जगह... शोध अपनी जगह — और दोनों का सम्मान। बाक़ी फ़ैसला... आपका।",
 "अगर ये सफ़र अच्छा लगा... तो कमेंट में बताइए — इन सात निशानों में से आप सबसे पहले कौन सा देखने जाएँगे? ऐसे ही ज़मीन से जुड़े रहस्यों के लिए — सब्सक्राइब ज़रूर कर दीजिए। मिलते हैं... अगली यात्रा में।",
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

KT = {
 0: {"jhar": kt(0,"झरनों"), "kitab": kt(0,"किताब"), "sev": kt(0,"सात"),
     "title": kt(0,"लंका"), "zameen": kt(0,"ज़मीन",2), "naam": kt(0,"नाम",2)},
 1: {"film": kt(1,"फ़िल्म"), "sri": kt(1,"श्रीलंका"), "trail": kt(1,"ट्रेल"),
     "sev": kt(1,"सात"), "pur": kt(1,"पुरातत्व")},
 2: {"valmiki": kt(2,"वाल्मीकि"), "trikut": kt(2,"त्रिकूट"), "sone": kt(2,"सोने"),
     "vim": kt(2,"विमान"), "hanu": kt(2,"हनुमान"), "nagar": kt(2,"नगर"), "sawal": kt(2,"सवाल")},
 3: {"ram": kt(3,"रामेश्वरम"), "dhan": kt(3,"धनुषकोडी"), "line": kt(3,"अड़तालीस"),
     "nasa": kt(3,"नासा"), "setu": kt(3,"सेतु"), "vigyan": kt(3,"विज्ञान"), "pani": kt(3,"अंदर")},
 4: {"sita": kt(4,"सीता"), "mandir": kt(4,"मंदिर"), "vatika": kt(4,"वाटिका"),
     "pad": kt(4,"पदचिह्न"), "hak": kt(4,"हकगला"), "sanj": kt(4,"संजीवनी"), "herbs": kt(4,"जड़ी-बूटियाँ")},
 5: {"falls": kt(5,"झरना"), "snan": kt(5,"स्नान"), "cave": kt(5,"गुफा"),
     "prag": kt(5,"प्रागैतिहासिक"), "purani": kt(5,"पुरानी"), "pok": kt(5,"पोकुना"), "band": kt(5,"बंद")},
 6: {"sig": kt(6,"सिगिरिया"), "kash": kt(6,"कश्यप"), "mahal": kt(6,"महल"),
     "uss": kt(6,"उस्सनगोडा"), "vim": kt(6,"विमान"), "serp": kt(6,"सर्पेन्टाइन"), "do": kt(6,"दो",2)},
 7: {"mv": kt(7,"महावंश"), "naam": kt(7,"नाम"), "div": kt(7,"दिवुरुमपोला"),
     "agni": kt(7,"अग्नि"), "kasam": kt(7,"कसम"), "likhi": kt(7,"लिखी")},
 8: {"gawah": kt(8,"गवाह"), "kham": kt(8,"ख़ामोश"), "zinda": kt(8,"ज़िंदा"),
     "aastha": kt(8,"आस्था"), "faisla": kt(8,"फ़ैसला",2)},
 9: {"comment": kt(9,"कमेंट"), "sub": kt(9,"सब्सक्राइब"), "yatra": kt(9,"यात्रा")},
}
# 3D windows (absolute time)
T3A0 = round(BEATS[3] + KT[3]["pani"] - 3.0, 2); T3A1 = round(BEATS[4] + 1.2, 2)
T3B0 = round(BEATS[5] + KT[5]["cave"] + 0.3, 2); T3B1 = round(T3B0 + 8.0, 2)

CLIPMAP = {
 "ocean":"15169","sea":"15209","under":"44974","fallsA":"45315","fallsB":"46384",
 "river":"49334","forest":"20986","ray":"19212","cavein":"47722","torch":"45321",
 "him1":"16130","him2":"45414","cavesky":"26323","cavetun":"9758","incense":"47620",
 "jungle":"32977","cliffco":"13000","tallfall":"11185","cliffwav":"6973","atemple":"11072",
 "sunsetco":"36577","turqcliff":"16131","hidfall":"48006","rainfor":"22728","iguazu":"11060",
 "rockfall":"25542","ocliff":"3503","creek":"51585",
 "sig1":"px_sig1","sig2":"px_sig2","dhan":"px_dhan","gopuram":"px_gopuram",
 "nuwara":"px_nuwara","tea":"px_tea","ellarock":"px_ellarock","ellahill":"px_ellahill",
 "highland":"px_highland","coastr":"px_coastr","mirissa":"px_mirissa","stupa":"px_stupa",
 "misttemple":"px_misttemple"}
SHOTS = {
 0:[["torch",7,1.1,.5,.5,.35,0],["fallsA",7,1.08,.5,.45,.3,0],["cavesky",7,1.08,.5,.45,.3,0],["cliffwav",7,1.07,.5,.5,.32,0],["ocean",7,1.08,.5,.5,.3,0]],
 1:[["sig2",6.3,1.08,.5,.45,.28,0,"SIGIRIYA \u00b7 SRI LANKA \u00b7 REAL"],["highland",8.5,1.06,.5,.5,.3,0,"SRI LANKA HIGHLANDS \u00b7 REAL"],["jungle",7.2,1.08,.5,.5,.4,0],["mirissa",8,1.06,.5,.45,.3,0,"MIRISSA \u00b7 SRI LANKA \u00b7 REAL"]],
 2:[["ANIM",13,1,0,0,0,0],["atemple",8,1.09,.5,.45,.42,0],["ray",7,1.1,.5,.5,.5,0],["sunsetco",8,1.07,.5,.5,.42,0]],
 3:[["gopuram",9,1.08,.5,.45,.3,0,"HINDU TEMPLE \u00b7 REAL DRONE"],["dhan",10,1.06,.5,.5,.28,0,"DHANUSHKODI \u00b7 REAL DRONE"],["turqcliff",7.3,1.07,.5,.5,.35,0],["under",12,1.1,.5,.5,.5,0]],
 4:[["nuwara",8.5,1.07,.5,.45,.3,0,"NUWARA ELIYA \u00b7 REAL DRONE"],["tea",8,1.07,.5,.5,.3,0,"SRI LANKA TEA HILLS \u00b7 REAL"],["him2",8,1.07,.5,.45,.3,0],["him1",9.5,1.07,.5,.45,.35,0]],
 5:[["tallfall",9,1.08,.5,.45,.28,0],["ellarock",8,1.07,.5,.4,.32,0,"ELLA ROCK \u00b7 SRI LANKA \u00b7 REAL"],["cavetun",9,1.1,.5,.5,.4,0],["hidfall",8,1.08,.5,.5,.32,0],["cavein",8.5,1.12,.5,.45,.45,0]],
 6:[["sig1",9,1.07,.5,.45,.28,0,"SIGIRIYA \u00b7 REAL DRONE"],["ellahill",9.5,1.07,.5,.5,.32,0,"ELLA \u00b7 SRI LANKA \u00b7 REAL"],["coastr",7.5,1.07,.5,.5,.32,0,"REAL FOOTAGE"],["cliffco",9.5,1.08,.45,.5,.35,0],["sea",9.5,1.1,.5,.45,.4,0]],
 7:[["rainfor",9,1.08,.5,.5,.45,0],["forest",9,1.08,.5,.45,.45,0],["incense",9,1.1,.5,.45,.45,0],["stupa",8.5,1.08,.5,.45,.35,0,"STUPA \u00b7 REAL DRONE"],["misttemple",8.5,1.07,.5,.45,.4,0,"REAL FOOTAGE"]],
 8:[["iguazu",8,1.07,.5,.45,.3,0],["rockfall",7,1.08,.5,.5,.3,0],["ocliff",7,1.08,.5,.6,.4,0],["river",7,1.08,.5,.5,.3,0]],
 9:[["fallsB",8,1.07,.5,.45,.3,0],["creek",11,1.06,.5,.45,.3,0]],
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
 ["हिंद महासागर में एक देश… जहाँ *रावण आज भी *ज़िंदा है।",
  "*झरनों में उसका नाम… *गुफाओं में उसकी कहानी… *कसमों में उसकी याद।",
  "पर उसी देश की सबसे पुरानी *किताब में… रावण का *नाम तक नहीं।",
  "25 मीटर चौड़ा *झरना… 1300 मीटर ऊँची *गुफा… जली हुई *लाल ज़मीन…",
  "*सात निशान आज भी खड़े हैं। तो *रावण की *लंका… सच कहाँ है?",
  "चलिए… *ज़मीन से पूछते हैं।"],
 ["इन दिनों हर तरफ़ *रामायण की चर्चा है — परदे पर नई *फ़िल्म आ रही है।",
  "पर आज हम परदे की नहीं… *ज़मीन की बात करेंगे।",
  "*श्रीलंका — जहाँ लाखों यात्री *रामायण *ट्रेल पर निकलते हैं।",
  "आज देखेंगे *सात सबसे रहस्यमयी निशान —",
  "*परंपरा… *ग्रंथ… और *पुरातत्व — तीनों गवाहों के साथ।"],
 ["पहले *ग्रंथ खोलते हैं। *वाल्मीकि रामायण कहती है —",
  "लंका *त्रिकूट पर्वत पर बसी थी… *सोने की नगरी।",
  "ऊँची दीवारें… भव्य द्वार… उड़ता *पुष्पक *विमान।",
  "*हनुमान जी भी इसे देखकर ठिठक गए थे।",
  "ग्रंथ का नक्शा — पहाड़ पर *स्वर्ण *नगर।",
  "अब सवाल — क्या *ज़मीन पर ऐसा कुछ है?"],
 ["भारत के दक्षिणी छोर से चलिए — *रामेश्वरम… फिर *धनुषकोडी।",
  "उजड़ा कस्बा… जहाँ सड़क *समंदर में खो जाती है।",
  "आगे पानी के नीचे — *अड़तालीस किलोमीटर लंबी *रेखा… सीधे श्रीलंका तक।",
  "*नासा की तस्वीरों में आज भी साफ़ दिखती है।",
  "कोई कहे *राम *सेतु… विज्ञान कहे चूना-पत्थर की शृंखला।",
  "पर रेखा *ठीक वहीं है… जहाँ ग्रंथ कहता है। चलिए *पानी के अंदर।"],
 ["श्रीलंका के पहाड़ों में… 1700 मीटर ऊँचाई पर — *सीता *एलिया।",
  "दुनिया का *इकलौता सीता मंदिर — सीता अम्मन कोविल।",
  "परंपरा कहती है — यही थी *अशोक *वाटिका।",
  "चट्टान पर बने गड्ढे… *हनुमान जी के *पदचिह्न माने जाते हैं।",
  "पास ही *हकगला — *संजीवनी पर्वत का टुकड़ा?",
  "यहाँ *हिमालय जैसी जड़ी-बूटियाँ आज भी उगती हैं।"],
 ["एला की घाटी — *रावण *एला झरना… 25 मीटर चौड़ा।",
  "परंपरा — बंदी सीता यहीं *स्नान करती थीं।",
  "चट्टान में काला मुँह — *रावण *गुफा।",
  "यहाँ मिले *प्रागैतिहासिक इंसान के निशान —",
  "ये गुफा… *कहानी से भी *पुरानी है।",
  "और *नील दिया पोकुना — नीला कुंड… अभी *बंद। वजह? *संरक्षण।"],
 ["सबसे बड़ा दावेदार — *सिगिरिया… 200 मीटर ऊँचा किला।",
  "*पुरातत्व — पाँचवीं सदी… राजा *कश्यप।",
  "*परंपरा — रावण का *आकाश *महल… कुबेर की नगरी।",
  "दक्षिणी तट — *उस्सनगोडा… लाल जली ज़मीन।",
  "परंपरा — *पुष्पक विमान… हनुमान जी की जलती *पूँछ।",
  "विज्ञान — *सर्पेन्टाइन मिट्टी। *दो जवाब… एक ज़मीन।"],
 ["अब वो सवाल… जो सब *पलट देता है।",
  "*महावंश — श्रीलंका की सबसे पुरानी इतिहास की किताब।",
  "राजाओं की पूरी सूची… पर रावण का *नाम… *कहीं *नहीं।",
  "तो क्या सब कहानी है? रुकिए — *दिवुरुमपोला चलिए।",
  "परंपरा — यहीं हुई *अग्नि *परीक्षा। आज भी लोग यहाँ *कसम खाते हैं।",
  "कुछ चीज़ें किताबों में नहीं… *ज़िंदगी में *लिखी जाती हैं।"],
 ["तो फ़ैसला? *पत्थर *गवाह हैं — झरना… गुफा… लाल ज़मीन।",
  "*किताब *ख़ामोश है — महावंश में नाम नहीं।",
  "और *परंपरा *ज़िंदा है — मंदिरों में… कसमों में… लाखों क़दमों में।",
  "*आस्था अपनी जगह… *शोध अपनी जगह — दोनों का *सम्मान।",
  "बाक़ी *फ़ैसला… *आपका।"],
 ["*कमेंट में बताइए — सात निशानों में से *पहले कौन सा देखेंगे?",
  "ऐसे रहस्यों के लिए *सब्सक्राइब कर दीजिए।",
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
def shankh(a=0.2):
    d = 2.6
    t = np.arange(_n(d)) / SR
    x = (np.sin(2*np.pi*(196*t + 30*t*t)) + 0.5*np.sin(2*np.pi*(392*t + 60*t*t)))
    e = np.minimum(t/0.7, 1.0) * np.exp(-np.maximum(t-1.4, 0)*2.2)
    return a * x * e

def gate(n, t0, t1, f=0.8):
    t = np.arange(n) / SR
    return np.clip(np.minimum((t - t0) / f, (t1 - t) / f), 0, 1)

def music_bed(n):
    t = np.arange(n) / SR
    m = np.zeros(n)
    inten = np.zeros(n)
    I = [0.85, 0.6, 0.66, 0.72, 0.62, 0.72, 0.68, 0.8, 0.62, 0.68]
    for i, b in enumerate(BEATS):
        e = BEATS[i + 1] if i + 1 < len(BEATS) else TOTAL
        inten[_n(b):min(_n(e), n)] = I[i]
    inten = box(inten, _n(2.2))
    for f, g2 in [(73.42, 1.0), (110.0, 0.45), (36.71, 0.6)]:
        m += g2 * (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.0045 * t + 0.9)) * 0.5
    m *= 0.046 * (0.65 + 0.35 * np.sin(2 * np.pi * 0.035 * t))
    pad = (np.sin(2 * np.pi * 293.66 * t) + np.sin(2 * np.pi * 295.1 * t)
           + np.sin(2 * np.pi * 440.0 * t) * 0.5)
    m += pad * 0.0055 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * t + 2.0))
    rs = np.random.RandomState(41)
    for bi in (0, 5, 7):
        for _ in range(8):
            at = BEATS[bi] + 2 + rs.rand() * (DUR[bi] - 2)
            x = ping(1800 + rs.rand() * 1600, 0.018, 0.5); i0 = _n(at)
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

def load_track(n):
    """Real music bed (Mixkit #188, free license) looped with crossfade to n samples."""
    wv = os.path.join(ROOT, "music.wav")
    if not os.path.exists(wv):
        subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(RM, "music_bed.mp3"),
                        "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
    w = wave.open(wv)
    trk = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0
    w.close()
    xf = _n(2.0)
    out = trk.copy()
    while len(out) < n + xf:
        a = out[:-xf]; tail = out[-xf:]
        head = trk[:xf] * np.linspace(0, 1, xf) + tail * np.linspace(1, 0, xf)
        out = np.concatenate([a, head, trk[xf:]])
    out = out[:n].copy()
    fo = _n(7.0)
    out[-fo:] *= np.linspace(1, 0, fo)
    fi = _n(1.5)
    out[:fi] *= np.linspace(0, 1, fi)
    return out

def build_audio():
    n = _n(TOTAL)
    sfx = np.zeros(n); B = BEATS
    def put(x, at, g2=1.0):
        i = _n(at)
        if 0 <= i < n:
            L = min(len(x), n - i); sfx[i:i + L] += x[:L] * g2
    for b in B[1:]: put(whoosh(0.7, 0.32), b - 0.35)
    for ct in cut_times(): put(whoosh(0.35, 0.16), ct - 0.12)
    # ambient beds
    amb = np.zeros(n)
    wavesn = box(noise(TOTAL, 31), 300) * 7
    amb += wavesn * 0.35 * gate(n, B[3], B[4] + 2)
    hiss = noise(TOTAL, 33); hiss = (hiss - box(hiss, 6)) * 0.2
    amb += hiss * gate(n, B[5], B[5] + 14)
    amb += (0.07 * np.sin(2*np.pi*50*np.arange(n)/SR) + box(noise(TOTAL, 35), 900) * 5 * 0.22) * gate(n, T3A0, T3A1, 0.5)
    # papercut pops
    PCUT = [(0,"jhar"),(0,"title"),(1,"sri"),(2,"sone"),(3,"dhan"),(3,"nasa"),(4,"sita"),(4,"hak"),
            (5,"falls"),(5,"cave"),(6,"sig"),(6,"uss"),(6,"serp"),(7,"agni"),(9,"comment")]
    for bi, k in PCUT:
        at = B[bi] + KT[bi][k]
        put(paper(0.65), at - 0.04); put(thud(0.5), at)
    # ch0 hook
    put(subboom(0.7), 0.3)
    put(thud(0.9), B[0] + KT[0]["sev"]); put(ping(294, 0.2, 1.4), B[0] + KT[0]["sev"] + 0.05)
    put(subboom(0.8), B[0] + KT[0]["title"]); put(shankh(0.22), B[0] + KT[0]["title"] + 0.1)
    put(tickk(500, 0.35, 0.08), B[0] + KT[0]["naam"])
    # ch2 granth
    put(bell(523, 0.12), B[2] + KT[2]["valmiki"])
    for k in range(5): put(tickk(800 + k*70, 0.15, 0.04), B[2] + KT[2]["trikut"] + k*0.4)
    put(ping(660, 0.16, 0.9), B[2] + KT[2]["vim"])
    # ch3 route
    for k0 in ("ram","dhan"): put(ping(523, 0.18, 0.9), B[3] + KT[3][k0])
    for k in range(6): put(tickk(900 - k*50, 0.14, 0.04), B[3] + KT[3]["line"] + k*0.3)
    put(subboom(0.6), B[3] + KT[3]["pani"])
    for k in range(4): put(drip(0.15), T3A0 + 1.2 + k*1.4)
    # ch4
    put(bell(660, 0.13), B[4] + KT[4]["mandir"])
    put(ping(880, 0.16, 1.0), B[4] + KT[4]["pad"])
    # ch5 cave
    put(subboom(0.6), B[5] + KT[5]["cave"])
    for k in range(5): put(drip(0.16), T3B0 + 1.0 + k*1.4)
    put(thud(0.8), B[5] + KT[5]["purani"]); put(bell(494, 0.16), B[5] + KT[5]["purani"] + 0.05)
    put(tickk(460, 0.35, 0.08), B[5] + KT[5]["band"])
    # ch6
    put(thud(0.7), B[6] + KT[6]["sig"])
    put(ping(392, 0.18, 1.1), B[6] + KT[6]["mahal"])
    put(thud(0.6), B[6] + KT[6]["uss"])
    put(ping(700, 0.15, 0.8), B[6] + KT[6]["do"])
    # ch7 twist
    put(subboom(0.75), B[7] + KT[7]["mv"])
    put(thud(1.0), B[7] + KT[7]["naam"]); put(tickk(420, 0.4, 0.1), B[7] + KT[7]["naam"] + 0.06)
    put(bell(587, 0.15), B[7] + KT[7]["kasam"])
    put(ping(880, 0.18, 1.2), B[7] + KT[7]["likhi"])
    # ch8 verdict stamps
    for k0 in ("gawah","kham","zinda"): put(thud(0.6), B[8] + KT[8][k0])
    put(subboom(0.7), B[8] + KT[8]["faisla"]); put(shankh(0.2), B[8] + KT[8]["faisla"] + 0.1)
    # ch9 cta
    put(pop(0.5), B[9] + KT[9]["sub"]); put(pop(0.55), B[9] + KT[9]["sub"] + 0.7)
    # VO
    vo = np.zeros(n)
    for i in range(10):
        wv = os.path.join(ROOT, "vo%02d.wav" % (i+1))
        if not os.path.exists(wv):
            subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(RM, "vo%02d.mp3" % (i+1)),
                            "-ar", str(SR), "-ac", "1", wv], check=True, capture_output=True)
        wf = wave.open(wv); dat = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16) / 32768.0
        wf.close()
        i0 = _n(BEATS[i] + LEAD); L = min(len(dat), n - i0)
        vo[i0:i0 + L] += dat[:L] * 1.3
    mus = music_bed(n)
    trk = load_track(n)
    env = box(np.abs(vo), _n(0.25)); env /= (env.max() + 1e-9)
    duck = (1.0 - 0.55 * np.minimum(env * 3.0, 1.0))
    tduck = (1.0 - 0.62 * np.minimum(env * 3.0, 1.0))
    mus *= duck * 0.45; amb *= duck
    trk *= tduck * 1.15
    mix = vo + sfx * 0.8 + mus + trk + amb
    mx = np.max(np.abs(mix))
    if mx > 0.97: mix = mix / mx * 0.95
    w = wave.open(os.path.join(ROOT, "master.wav"), "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    print("audio ok %.1fs" % TOTAL)

# ================= HTML =================
def build_html(sel=None):
    sel = set(SHOTS) if sel is None else set(sel)
    caps = make_caps()
    three = open("/var/tmp/three/three.min.js").read()
    fonts = {"Anton": FONTS + "/Anton-Regular.ttf", "InterB": FONTS + "/Inter-Black.ttf",
             "Mono": FONTS + "/JetBrainsMono-Bold.ttf", "Deva": "/var/tmp/ujjain/TiroDeva.ttf"}
    ff = "\n".join("@font-face{font-family:'%s';src:url('file://%s');}" % (k, v) for k, v in fonts.items())
    html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTFACES
body{margin:0;background:#000}</style></head><body><script>THREELIB</script><script>
window.__err=''; window.onerror=function(m,s,l){window.__err=m+' @'+l; return true;};
try{
const W=1920,H=1080,TOTAL=__TOT__,B=BEATSJ,DUR=DURJ,LEAD=0.5,CAPS=CAPSJ,KT=KTJ;
const T3A0=__A0__,T3A1=__A1__,T3B0=__B0__,T3B1=__B1__;
const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const ss=(a,b,x)=>{x=clamp((x-a)/(b-a),0,1);return x*x*(3-2*x)};
const ov=x=>{x=clamp(x,0,1);const c=1.7,u=x-1;return 1+u*u*((c+1)*u+c)};
function rng(seed){let s=seed>>>0||1;return()=>{s=Math.imul(s^s>>>15,s|1);s^=s+Math.imul(s^s>>>7,s|61);return((s^s>>>14)>>>0)/4294967296}}
const CYAN='#4dd8ff',ORG='#ff8c3b',PAPER='#eef2f8',RED='#e8503a',GOLD='#e8b24a';
const IMGS={};let nimg=0,want=17;
function ld(k,s){const im=new Image();im.onload=()=>nimg++;im.src=s;IMGS[k]=im;}
ld('sita','data:image/jpeg;base64,SITA64');
ld('hak','data:image/jpeg;base64,HAK64');
ld('fallsP','data:image/jpeg;base64,FALLSP64');
ld('fallsQ','data:image/jpeg;base64,FALLSQ64');
ld('caveIn','data:image/jpeg;base64,CAVEIN64');
ld('caveSt','data:image/jpeg;base64,CAVEST64');
ld('sigG','data:image/jpeg;base64,SIGG64');
ld('sigW','data:image/jpeg;base64,SIGW64');
ld('ussC','data:image/jpeg;base64,USSC64');
ld('ussS','data:image/jpeg;base64,USSS64');
ld('setuL','data:image/jpeg;base64,SETUL64');
ld('setuE','data:image/jpeg;base64,SETUE64');
ld('dhanC','data:image/jpeg;base64,DHANC64');
ld('dhanS','data:image/jpeg;base64,DHANS64');
ld('engL','data:image/jpeg;base64,ENGL64');
ld('engV','data:image/jpeg;base64,ENGV64');
ld('logo','data:image/png;base64,LOGO64');
const VIDS={};let nvid=0;const wantvid=WANTVID;
function lv(k,b){const v=document.createElement('video');v.muted=true;v.preload='auto';
 v.addEventListener('loadeddata',()=>nvid++);v.src='data:video/mp4;base64,'+b;VIDS[k]=v;}
/*VIDLOADS*/
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
   return {v:arr[i][0],lt2:lt-acc,z:arr[i][2],cx:arr[i][3],cy:arr[i][4],dim:arr[i][5],off:arr[i][6],lab:arr[i][7]||null,since:lt-acc};
  acc+=d;}
 return null;}
const DUST=[];{const r=rng(55);for(let i=0;i<80;i++)DUST.push([r()*W,r()*H,r()*2.2+0.6,r()*6.28,0.14+r()*0.28]);}
function codeBG(t){
 g.fillStyle='#07050a';g.fillRect(0,0,W,H);
 for(let i=0;i<3;i++){
  const bx=((i*650+t*(8+5*i))%(W+800))-400, by=250+i*280+30*Math.sin(t*0.25+i*2);
  const gr=g.createRadialGradient(bx,by,40,bx,by,520);
  const col=i===1?'rgba(90,60,30,0.10)':'rgba(40,55,70,0.10)';
  gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=gr;g.fillRect(0,0,W,H);}
 for(const s of DUST){
  const x=(s[0]+t*6*(1+s[2]*0.3))%W, y=(s[1]+t*3)%H;
  const a=s[4]*(0.5+0.5*Math.sin(t*1.1+s[3]));
  g.save();g.globalAlpha=a;g.fillStyle='#d8c9a8';
  g.beginPath();g.arc(x,y,s[2],0,6.29);g.fill();g.restore();}}
function drawBG(sh,t){
 if(!sh){g.fillStyle='#07050a';g.fillRect(0,0,W,H);return;}
 if(sh.v==='ANIM'){codeBG(t);return;}
 const punch=1+0.06*Math.exp(-sh.since*5);
 const v=VIDS[sh.v];
 if(v&&v.videoWidth)coverV(v,sh.z*punch+0.02*Math.sin(t*0.2),sh.cx,sh.cy,sh.dim);
 else codeBG(t);
 if(sh.lab){const a=ss(0.5,1.1,sh.since)*0.6;
  if(a>0){g.save();g.globalAlpha=a;g.font='22px Mono';g.fillStyle='#eef2f8';g.textAlign='right';
   g.fillText(sh.lab,W-60,124);
   g.fillStyle='#4dd8ff';g.fillRect(W-60-g.measureText(sh.lab).width-16,112,6,16);g.restore();}}}
// ============ THREE.JS 3D ============
const GW=1280,GH=720;
const glc=document.createElement('canvas');glc.width=GW;glc.height=GH;
const bl3=document.createElement('canvas');bl3.width=320;bl3.height=180;const bl3g=bl3.getContext('2d');
const renderer=new THREE.WebGLRenderer({canvas:glc,antialias:false});
renderer.setSize(GW,GH,false);renderer.outputEncoding=THREE.sRGBEncoding;
const cam3=new THREE.PerspectiveCamera(46,GW/GH,0.1,200);
function vn2(x,y){const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;
 function hsh(a,b){let n=(a*374761393+b*668265263)|0;n=Math.imul(n^(n>>>13),1274126177);return(((n^(n>>>16))>>>0)%1000)/1000;}
 const sx=xf*xf*(3-2*xf),sy=yf*yf*(3-2*yf);
 const a=hsh(xi,yi),b2=hsh(xi+1,yi),c=hsh(xi,yi+1),d=hsh(xi+1,yi+1);
 return a+(b2-a)*sx+(c-a)*sy+(a-b2-c+d)*sx*sy;}
function fbm2(x,y){let v=0,amp=1,f=1,s=0;for(let o=0;o<3;o++){v+=amp*vn2(x*f,y*f);s+=amp;amp*=0.5;f*=2.1;}return v/s;}
// Scene U: underwater setu ridge
const scU=new THREE.Scene();
scU.background=new THREE.Color(0x07323a);scU.fog=new THREE.FogExp2(0x07323a,0.05);
{const sc2=document.createElement('canvas');sc2.width=sc2.height=256;
 const c2=sc2.getContext('2d');c2.fillStyle='#7a6a4e';c2.fillRect(0,0,256,256);
 const r=rng(31);for(let i=0;i<2400;i++){const v=40+r()*70;
 c2.fillStyle='rgba('+(90+v|0)+','+(78+v*0.9|0)+','+(55+v*0.7|0)+',0.5)';
 c2.fillRect(r()*256,r()*256,1.7,1.7);}
 const tx=new THREE.CanvasTexture(sc2);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(6,6);
 const geo=new THREE.PlaneGeometry(70,70,52,52);
 const pos=geo.attributes.position;
 for(let i=0;i<pos.count;i++)pos.setZ(i,fbm2(pos.getX(i)*0.12+1,pos.getY(i)*0.12+5)*1.0-0.3);
 geo.computeVertexNormals();
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({map:tx,roughness:0.95}));
 m.rotation.x=-Math.PI/2;scU.add(m);}
{const r=rng(47);const pmat=new THREE.MeshStandardMaterial({color:0x6a6a58,roughness:0.92});
 for(let i=0;i<16;i++){const z=8-i*3.4,x=Math.sin(i*0.5)*1.6;
  const st=new THREE.Mesh(new THREE.SphereGeometry(0.9+r()*0.9,9,7),pmat);
  st.position.set(x,0.35+r()*0.35,z);st.scale.y=0.6;st.rotation.y=r()*3;scU.add(st);
  if(r()>0.4){const st2=new THREE.Mesh(new THREE.SphereGeometry(0.5+r()*0.5,8,6),pmat);
   st2.position.set(x+1.4*(r()-0.5)*2,0.3,z+1.1);st2.scale.y=0.55;scU.add(st2);}}}
const cauCv=document.createElement('canvas');cauCv.width=cauCv.height=256;
{const cc=cauCv.getContext('2d');cc.fillStyle='#000';cc.fillRect(0,0,256,256);
 const r=rng(77);cc.strokeStyle='rgba(255,255,255,0.55)';cc.lineWidth=2.2;
 for(let i=0;i<46;i++){cc.beginPath();
  cc.ellipse(r()*256,r()*256,8+r()*26,6+r()*20,r()*3.14,0,6.29);cc.stroke();}
 cc.filter='blur(3px)';cc.drawImage(cauCv,0,0);}
const CAUS=[];
for(const[yy,op]of[[0.12,0.2],[0.22,0.14]]){
 const tx=new THREE.CanvasTexture(cauCv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(3.2,3.2);
 const m=new THREE.Mesh(new THREE.PlaneGeometry(60,60),
  new THREE.MeshBasicMaterial({map:tx,transparent:true,opacity:op,color:0x9fe8e0,
   blending:THREE.AdditiveBlending,depthWrite:false}));
 m.rotation.x=-Math.PI/2;m.position.y=yy;scU.add(m);CAUS.push(tx);}
const SHAFTS=[];
{const r=rng(88);for(let i=0;i<3;i++){
 const sh=new THREE.Mesh(new THREE.ConeGeometry(1.6+r()*1.4,14,16,1,true),
  new THREE.MeshBasicMaterial({color:0x8fd8d0,transparent:true,opacity:0.05,
   blending:THREE.AdditiveBlending,side:THREE.DoubleSide,depthWrite:false}));
 sh.position.set(-5+i*5+r()*2,7.5,-4-r()*6);sh.rotation.z=0.12-i*0.1;scU.add(sh);SHAFTS.push(sh);}}
let BUB,BUBD=[];
{const r=rng(99),N=260,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){p[i*3]=(r()-0.5)*18;p[i*3+1]=r()*9;p[i*3+2]=10-r()*34;
  BUBD.push([p[i*3],r()*9,0.35+r()*0.8,r()*6.28]);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 BUB=new THREE.Points(geo,new THREE.PointsMaterial({color:0xcfeef2,size:0.07,transparent:true,opacity:0.55,sizeAttenuation:true}));
 scU.add(BUB);}
{const d=new THREE.DirectionalLight(0xaee2f0,0.95);d.position.set(6,20,4);scU.add(d);}
scU.add(new THREE.AmbientLight(0x0e3a42,1.15));
// Scene C: ravana cave
const scC=new THREE.Scene();
scC.background=new THREE.Color(0x050308);scC.fog=new THREE.FogExp2(0x050308,0.08);
{const geo=new THREE.CylinderGeometry(10,10,14,48,16,true);
 const pos=geo.attributes.position,r=rng(21);
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i);
  const d=1-0.15*r()-0.06*Math.sin(y*1.7+x*0.8)*Math.cos(z*0.9);
  pos.setX(i,x*d);pos.setZ(i,z*d);}
 geo.computeVertexNormals();
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:0x332820,roughness:1.0,side:THREE.BackSide}));
 m.position.y=5;scC.add(m);}
{const r=rng(66);const bmat=new THREE.MeshStandardMaterial({color:0x4a3a2e,roughness:0.95});
 for(let i=0;i<10;i++){const a=r()*6.28,rad=2.2+r()*5.8;
  const b=new THREE.Mesh(new THREE.SphereGeometry(0.5+r()*1.1,8,6),bmat);
  b.position.set(Math.cos(a)*rad,0.3+r()*0.25,Math.sin(a)*rad);
  b.scale.y=0.55+r()*0.2;b.rotation.y=r()*3;scC.add(b);}}
{const geo=new THREE.CircleGeometry(10.5,40);
 const pos=geo.attributes.position,r=rng(33);
 for(let i=0;i<pos.count;i++){const d=Math.hypot(pos.getX(i),pos.getY(i));
  if(d>1.8)pos.setZ(i,0.22*r()-0.11);}
 geo.computeVertexNormals();
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:0x3c3028,roughness:0.95}));
 m.rotation.x=-Math.PI/2;scC.add(m);}
{const r=rng(55);
 for(let i=0;i<12;i++){
  const a=r()*6.28,rad=3+r()*5.5,hh=1.2+r()*2.4;
  const cone=new THREE.Mesh(new THREE.ConeGeometry(0.28+r()*0.45,hh,7),
   new THREE.MeshStandardMaterial({color:0x56453a,roughness:0.9}));
  cone.position.set(Math.cos(a)*rad,11-hh/2,Math.sin(a)*rad);
  cone.rotation.x=Math.PI;scC.add(cone);}}
let CDUST,CDUSTD=[];
{const r=rng(77),N=240,p=new Float32Array(N*3);
 for(let i=0;i<N;i++){const a=r()*6.28,rad=r()*7,y=0.3+r()*8;
  p[i*3]=Math.cos(a)*rad;p[i*3+1]=y;p[i*3+2]=Math.sin(a)*rad;
  CDUSTD.push([r()*6.28,0.08+r()*0.2]);}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(p,3));
 CDUST=new THREE.Points(geo,new THREE.PointsMaterial({color:0xd8c9a8,size:0.045,transparent:true,opacity:0.6,sizeAttenuation:true}));
 scC.add(CDUST);}
const cShaft=new THREE.Mesh(new THREE.ConeGeometry(2.4,10,20,1,true),
 new THREE.MeshBasicMaterial({color:0x8fb8d8,transparent:true,opacity:0.07,
  blending:THREE.AdditiveBlending,side:THREE.DoubleSide,depthWrite:false}));
cShaft.position.set(-2,6,-2);scC.add(cShaft);cShaft.material.opacity=0.11;
scC.add(new THREE.AmbientLight(0x2a2436,0.8));
const cWarm=new THREE.PointLight(0xffa04a,2.6,26,1.6);cWarm.position.set(-1,1.8,-1);scC.add(cWarm);
const cRim=new THREE.DirectionalLight(0x3a6a9a,0.5);cRim.position.set(-6,8,-4);scC.add(cRim);
function draw3D(t){
 let sc,u;
 if(t>=T3A0&&t<T3A1){
  u=ss(0,T3A1-T3A0-0.3,t-T3A0);sc=scU;
  const shx=0.05*Math.sin(t*7.3),shy=0.04*Math.sin(t*9.1);
  cam3.position.set(2.2-1.2*u+shx,5.8-3.4*u+shy,9.5-13*u);
  cam3.lookAt(Math.sin((9.5-13*u-10)*0.5*0.1)*1.6,0.9,9.5-13*u-9);
  CAUS[0].offset.set(t*0.025,t*0.018);CAUS[1].offset.set(-t*0.021,t*0.028);
  for(let i=0;i<SHAFTS.length;i++){SHAFTS[i].rotation.y=t*0.12+i;
   SHAFTS[i].material.opacity=0.045+0.02*Math.sin(t*0.8+i*2);}
  const bp=BUB.geometry.attributes.position;
  for(let i=0;i<BUBD.length;i++){const d=BUBD[i];
   bp.array[i*3+1]=((d[1]+d[2]*t)%9+9)%9+0.2;
   bp.array[i*3]=d[0]+0.35*Math.sin(t*1.8+d[3]);}
  bp.needsUpdate=true;
 }else{
  u=ss(0,T3B1-T3B0-0.3,t-T3B0);sc=scC;
  const shx=0.05*Math.sin(t*7.3),shy=0.04*Math.sin(t*9.1);
  const ang=-0.35+0.75*u,rad=7.8-4.0*u;
  cam3.position.set(Math.sin(ang)*rad+shx,2.5-0.5*u+shy,Math.cos(ang)*rad);
  cam3.lookAt(-2,2.8,-2);
  cWarm.intensity=2.6+0.4*Math.sin(t*11)+0.25*Math.sin(t*29)+0.15*Math.sin(t*47);
  cShaft.rotation.y=t*0.1;
  const pos=CDUST.geometry.attributes.position;
  for(let i=0;i<CDUSTD.length;i++){
   pos.array[i*3]+=Math.sin(t*0.5+CDUSTD[i][0])*0.0012;
   pos.array[i*3+1]+=CDUSTD[i][1]*0.004*Math.sin(t*0.3+i);}
  pos.needsUpdate=true;}
 renderer.render(sc,cam3);
 g.drawImage(glc,0,0,W,H);
 bl3g.drawImage(glc,0,0,320,180);
 g.save();g.globalCompositeOperation='lighter';g.globalAlpha=0.17;g.drawImage(bl3,0,0,W,H);g.restore();
 g.save();g.font='22px Mono';g.fillStyle='rgba(238,242,248,0.5)';g.textAlign='right';
 g.fillText('REAL-TIME 3D \u00b7 CODE SE',W-60,120);g.restore();}
function in3D(t){return (t>=T3A0&&t<T3A1)||(t>=T3B0&&t<T3B1);}
// ============ 2D layers ============
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
// line-art helpers
function inkPath(pts,prog,col,lw){
 if(prog<=0)return;
 const n=Math.max(2,Math.floor(pts.length*clamp(prog,0,1)));
 g.save();g.strokeStyle=col;g.lineWidth=lw||3;g.lineJoin='round';g.lineCap='round';
 g.beginPath();g.moveTo(pts[0][0],pts[0][1]);
 for(let i=1;i<n;i++)g.lineTo(pts[i][0],pts[i][1]);
 g.stroke();g.restore();}
// ============ CHAPTERS ============
function fig0(t,lt){
 const K=KT[0];
 figbar(lt,'HIND MAHASAGAR \u00b7 EK DESH','FIG. 01 \u00b7 CHRONIC JOURNAL');
 typew(lt,0.8,'JAHAN RAVAN AAJ BHI...',13,140,176,'Mono',32,'rgba(238,242,248,0.9)','left');
 if(IMGS.fallsP.width)papercut(lt,K.jhar,IMGS.fallsP,350,500,420,-0.03,'RAVANA ELLA \u00b7 25M','REAL PHOTO','#2a6a3a',11);
 const kb=ss(K.kitab,K.kitab+0.4,lt);
 if(kb>0){g.save();g.globalAlpha=kb;g.translate(1520,420+(1-ov(kb))*50);g.rotate(0.03);
  g.fillStyle='#1a1510';g.strokeStyle=GOLD;g.lineWidth=3;
  rrect(-150,-190,300,380,8);g.fill();g.stroke();
  g.strokeStyle='rgba(232,178,74,0.5)';rrect(-128,-168,256,336,5);g.stroke();
  T(0,-60,'\u092e\u0939\u093e\u0935\u0902\u0936','Deva',48,GOLD,'center');
  T(0,10,'5th CENTURY','Mono',22,'rgba(238,242,248,0.6)','center',1,2);
  const nm=ss(K.naam,K.naam+0.3,lt);
  if(nm>0){g.rotate(-0.09);g.globalAlpha=nm;
   g.strokeStyle=RED;g.lineWidth=5;rrect(-130,60,260,70,8);g.stroke();
   T(0,95,'\u0928\u093e\u092e \u0928\u0939\u0940\u0902',' Deva'.trim(),40,RED,'center');}
  g.restore();}
 const f7=ss(K.sev,K.sev+0.3,lt)*(1-ss(K.title-0.8,K.title-0.3,lt));
 if(f7>0){g.save();const sc=1.8-0.8*ov(f7);g.globalAlpha=f7;
  g.translate(900,0);g.scale(sc,sc);
  T(0,400/sc,'7 NISHAN','Anton',140,ORG,'center');g.restore();
  T(900,520,'\u0906\u091c \u092d\u0940 \u0935\u0939\u093e\u0901 \u0916\u0921\u093c\u0947 \u0939\u0948\u0902','Deva',36,PAPER,'center',ss(K.sev+0.3,K.sev+0.7,lt));}
 const ti=ss(K.title,K.title+0.5,lt);
 if(ti>0){g.save();const sc=1.5-0.5*ov(ti);g.globalAlpha=ti;
  g.translate(900,0);g.scale(sc,sc);
  T(0,700/sc,'\u0930\u093e\u0935\u0923 \u0915\u0940 \u0932\u0902\u0915\u093e','Deva',110,PAPER,'center');g.restore();
  T(900,806,'SACH KAHAN HAI?','Mono',30,GOLD,'center',ss(K.title+0.4,K.title+0.8,lt),6);}
 typew(lt,K.zameen,'ZAMEEN SE POOCHTE HAIN \u2192',12,140,620,'Mono',30,CYAN,'left');
}
function fig1(t,lt){
 const K=KT[1];
 figbar(lt,'RAMAYANA SEASON \u00b7 2026','FIG. 02');
 kickerD(lt,0.5,'PARDE KI NAHI \u00b7 ZAMEEN KI','\u0936\u094d\u0930\u0940\u0932\u0902\u0915\u093e');
 if(IMGS.sigW.width)papercut(lt,K.sri,IMGS.sigW,480,560,560,-0.03,'SRI LANKA \u00b7 RAMAYANA TRAIL','REAL PHOTO','#2a6a3a',21);
 const tr=ss(K.trail,K.trail+0.4,lt);
 if(tr>0){g.save();g.globalAlpha=tr;
  g.fillStyle='rgba(10,8,16,0.8)';g.strokeStyle=ORG;g.lineWidth=2;
  rrect(260,830,440,76,14);g.fill();g.stroke();
  T(480,868,'14+ JAGAHEIN \u00b7 LAKHS YATRI','Mono',24,ORG,'center',1,1);g.restore();}
 chip(lt,K.pur,1130,520,'\u092a\u0930\u0902\u092a\u0930\u093e',GOLD,280);
 chip(lt,K.pur+0.25,1440,520,'\u0917\u094d\u0930\u0902\u0925',CYAN,280);
 chip(lt,K.pur+0.5,1750-120,660,'\u092a\u0941\u0930\u093e\u0924\u0924\u094d\u0935',ORG,300);
 T(1400,380,'\u0924\u0940\u0928 \u0917\u0935\u093e\u0939',' Deva'.trim(),56,PAPER,'center',ss(K.pur-0.3,K.pur+0.1,lt));
 const s7=ss(K.sev,K.sev+0.4,lt);
 if(s7>0)T(1400,830,'7 \u0930\u0939\u0938\u094d\u092f\u092e\u092f\u0940 \u0928\u093f\u0936\u093e\u0928','Deva',44,ORG,'center',s7);
}
function fig2(t,lt){
 const K=KT[2];
 figbar(lt,'VALMIKI RAMAYANA \u00b7 SUNDARKAND','FIG. 03');
 kickerD(lt,0.5,'GRANTH KYA KEHTA HAI','\u0938\u094b\u0928\u0947 \u0915\u0940 \u0932\u0902\u0915\u093e');
 // line-art trikuta city (draws in)
 const lp=ss(K.trikut,K.trikut+2.6,lt);
 if(lp>0){
  const base=[[340,760],[480,560],[560,660],[700,470],[820,640],[940,540],[1060,760]];
  inkPath(base,lp,'rgba(238,242,248,0.75)',4);
  if(lp>0.5){const p2=(lp-0.5)*2;
   const city=[[560,560],[560,480],[620,480],[620,520],[680,520],[680,420],[760,420],[760,500],[820,500],[820,560]];
   inkPath(city,p2,GOLD,4);
   const flag=[[700,420],[700,370],[740,385],[700,400]];
   inkPath(flag,p2,ORG,3);}
  T(700,820,'\u0924\u094d\u0930\u093f\u0915\u0942\u091f \u092a\u0930\u094d\u0935\u0924','Deva',32,PAPER,'center',ss(K.trikut+0.8,K.trikut+1.2,lt));}
 if(IMGS.engL.width)papercut(lt,K.sone,IMGS.engL,1450,480,620,0.03,'SONE KI NAGRI \u00b7 KALPANA','AI ART','#7a5a20',31);
 kword(lt,K.sone,'\u0938\u094b\u0928\u0947 \u0915\u0940 \u0928\u0917\u0930\u0940',1450,150,GOLD);
 // flying vimana line icon
 if(lt>K.vim){const vx=300+((lt-K.vim)*110)%1500,vy=200+18*Math.sin(lt*2.2);
  g.save();g.globalAlpha=0.8;g.strokeStyle=GOLD;g.lineWidth=3;g.lineCap='round';
  g.beginPath();g.moveTo(vx-46,vy);g.quadraticCurveTo(vx,vy-26,vx+46,vy);
  g.quadraticCurveTo(vx,vy+12,vx-46,vy);g.stroke();
  g.beginPath();g.moveTo(vx-14,vy-18);g.lineTo(vx,vy-40);g.lineTo(vx+14,vy-18);g.stroke();g.restore();}
 typew(lt,K.sawal,'KYA ZAMEEN PAR AISA KUCH HAI?',13,140,930,'Mono',30,CYAN,'left');
}
function fig3(t,lt){
 const K=KT[3];
 figbar(lt,'BHARAT \u2192 LANKA \u00b7 48 KM','FIG. 04');
 kickerD(lt,0.5,'RAASTA \u00b7 SAMANDAR KE NEECHE','\u0930\u093e\u092e \u0938\u0947\u0924\u0941');
 const hA=1-ss(T3A0-B[3]-0.5,T3A0-B[3],lt);
 if(hA>0.03){
 g.save();g.globalAlpha=hA;
 // map line-art
 const mp=ss(1.2,3.0,lt);
 if(mp>0){
  const india=[[300,330],[380,360],[430,430],[470,520],[500,600],[520,660],[540,700],[560,720]];
  const lanka=[[760,800],[830,780],[890,810],[910,880],[860,950],[780,960],[730,900],[740,840],[760,800]];
  inkPath(india,mp,'rgba(238,242,248,0.7)',4);
  inkPath(lanka,ss(1.8,3.4,lt),'rgba(238,242,248,0.7)',4);
  const rm=ss(K.ram,K.ram+0.3,lt);
  if(rm>0){g.save();g.globalAlpha=rm;g.fillStyle=GOLD;
   g.beginPath();g.arc(560,720,9,0,6.29);g.fill();
   T(430,700,'\u0930\u093e\u092e\u0947\u0936\u094d\u0935\u0930\u092e','Deva',28,GOLD,'left');g.restore();}
  const dn=ss(K.dhan,K.dhan+0.3,lt);
  if(dn>0){g.save();g.globalAlpha=dn;g.fillStyle=ORG;
   g.beginPath();g.arc(600,742,8,0,6.29);g.fill();
   T(620,716,'\u0927\u0928\u0941\u0937\u0915\u094b\u0921\u0940','Deva',26,ORG,'left');g.restore();}
  const ln=ss(K.line,K.line+1.6,lt);
  if(ln>0){g.save();g.strokeStyle=CYAN;g.lineWidth=4;g.setLineDash([12,10]);
   g.globalAlpha=0.9;
   g.beginPath();g.moveTo(600,742);
   const ex=600+(755-600)*ln, ey=742+(812-742)*ln;
   g.lineTo(ex,ey);g.stroke();g.setLineDash([]);
   g.restore();
   T(560,860,'48 KM \u00b7 REKHA','Mono',24,CYAN,'left',ss(K.line+0.8,K.line+1.2,lt),2);}
  const lk=ss(2.6,3.0,lt);
  if(lk>0)T(820,1000,'\u0936\u094d\u0930\u0940\u0932\u0902\u0915\u093e','Deva',30,PAPER,'center',lk);}
 if(IMGS.dhanC.width)papercut(lt,K.dhan,IMGS.dhanC,1420,330,520,0.03,'DHANUSHKODI \u00b7 UJDA KASBA','REAL PHOTO','#2a6a3a',41);
 if(IMGS.setuL.width)papercut(lt,K.nasa,IMGS.setuL,1380,760,600,-0.02,'ADAM\u0027S BRIDGE \u00b7 SATELLITE','NASA/USGS','#2a6a3a',43);
 kword(lt,K.setu,'\u0930\u093e\u092e \u0938\u0947\u0924\u0941',1380,520,CYAN);
 const vg=ss(K.vigyan,K.vigyan+0.4,lt)*hA;
 if(vg>0)T(400,960,'\u0906\u0938\u094d\u0925\u093e \u2014 \u0938\u0947\u0924\u0941 \u00b7 \u0935\u093f\u091c\u094d\u091e\u093e\u0928 \u2014 \u0936\u0943\u0902\u0916\u0932\u093e','Deva',34,GOLD,'center',vg);
 g.restore();}
}
function fig4(t,lt){
 const K=KT[4];
 figbar(lt,'SEETHA ELIYA \u00b7 1700 M','FIG. 05 \u00b7 NISHAN 1-2');
 kickerD(lt,0.5,'DUNIYA KA IKLAUTA','\u0938\u0940\u0924\u093e \u092e\u0902\u0926\u093f\u0930');
 if(IMGS.sita.width)papercut(lt,K.sita,IMGS.sita,480,520,620,-0.03,'SITA AMMAN KOVIL','REAL PHOTO','#2a6a3a',51);
 kword(lt,K.vatika,'\u0905\u0936\u094b\u0915 \u0935\u093e\u091f\u093f\u0915\u093e',480,180,GOLD);
 chip(lt,K.pad,1180,380,'\u0939\u0928\u0941\u092e\u093e\u0928 \u092a\u0926\u091a\u093f\u0939\u094d\u0928 \u00b7 \u092e\u093e\u0928\u094d\u092f\u0924\u093e',GOLD,560);
 if(IMGS.hak.width)papercut(lt,K.hak,IMGS.hak,1430,680,520,0.04,'HAKGALA \u00b7 SANJEEVANI?','REAL PHOTO','#2a6a3a',53);
 kword(lt,K.sanj,'\u0938\u0902\u091c\u0940\u0935\u0928\u0940',1430,420,CYAN);
 typew(lt,K.herbs,'HIMALAYA JAISI HERBS... YAHAN?',13,140,930,'Mono',30,CYAN,'left');
}
function fig5(t,lt){
 const K=KT[5];
 figbar(lt,'ELLA VALLEY \u00b7 UVA','FIG. 06 \u00b7 NISHAN 3-4');
 kickerD(lt,0.5,'PARAMPARA KA JHARNA','\u0930\u093e\u0935\u0923 \u090f\u0932\u093e');
 const b0=T3B0-B[5],b1=T3B1-B[5];
 const hB=Math.min(1,1-ss(b0-0.5,b0,lt)+ss(b1-0.1,b1+0.5,lt));
 if(hB>0.03){g.save();g.globalAlpha=hB;
  if(IMGS.fallsQ.width)papercut(lt,K.falls,IMGS.fallsQ,430,500,520,-0.03,'RAVANA FALLS \u00b7 25M','REAL PHOTO','#2a6a3a',61);
  if(IMGS.caveSt.width)papercut(lt,K.cave,IMGS.caveSt,1440,420,540,0.03,'RAVANA CAVE \u00b7 1370M','REAL PHOTO','#2a6a3a',63);
  g.restore();}
 kword(lt,K.cave,'\u0930\u093e\u0935\u0923 \u0917\u0941\u092b\u093e',1440,140,ORG);
 chip(lt,K.prag,430,880,'\u092a\u094d\u0930\u093e\u0917\u0948\u0924\u093f\u0939\u093e\u0938\u093f\u0915 \u0928\u093f\u0936\u093e\u0928 \u092e\u093f\u0932\u0947',CYAN,620);
 stampD(lt,K.purani,1200,820,'\u0915\u0939\u093e\u0928\u0940 \u0938\u0947 \u092d\u0940 \u092a\u0941\u0930\u093e\u0928\u0940',GOLD,40,-0.05);
 const bd=ss(K.band,K.band+0.4,lt);
 if(bd>0){g.save();g.globalAlpha=bd;g.translate(1620,860);
  g.fillStyle='rgba(10,8,16,0.85)';g.strokeStyle=RED;g.lineWidth=3;
  rrect(-240,-50,480,100,14);g.fill();g.stroke();
  T(0,-8,'NIL DIYA POKUNA','Mono',24,RED,'center',1,2);
  T(0,28,'\u0905\u092d\u0940 \u092c\u0902\u0926 \u00b7 \u0938\u0902\u0930\u0915\u094d\u0937\u0923','Deva',26,PAPER,'center');g.restore();}
}
function fig6(t,lt){
 const K=KT[6];
 figbar(lt,'SIGIRIYA + USSANGODA','FIG. 07 \u00b7 NISHAN 5-6');
 kickerD(lt,0.5,'SABSE BADA DAVEDAR','\u0938\u093f\u0917\u093f\u0930\u093f\u092f\u093e');
 if(IMGS.sigG.width)papercut(lt,K.sig,IMGS.sigG,520,460,640,-0.02,'SIGIRIYA \u00b7 200M \u00b7 UNESCO','REAL PHOTO','#2a6a3a',71);
 const kb=ss(K.kash,K.kash+0.4,lt);
 if(kb>0){g.save();g.globalAlpha=kb;
  g.fillStyle='rgba(10,8,16,0.82)';g.strokeStyle=CYAN;g.lineWidth=2;
  rrect(170,760,560,110,14);g.fill();g.stroke();
  T(450,800,'\u092a\u0941\u0930\u093e\u0924\u0924\u094d\u0935','Deva',28,CYAN,'center');
  T(450,842,'\u0930\u093e\u091c\u093e \u0915\u0936\u094d\u092f\u092a \u00b7 5\u0935\u0940\u0902 \u0938\u0926\u0940','Deva',30,PAPER,'center');g.restore();}
 const mh=ss(K.mahal,K.mahal+0.4,lt);
 if(mh>0){g.save();g.globalAlpha=mh;
  g.fillStyle='rgba(10,8,16,0.82)';g.strokeStyle=GOLD;g.lineWidth=2;
  rrect(170,890,560,110,14);g.fill();g.stroke();
  T(450,930,'\u092a\u0930\u0902\u092a\u0930\u093e','Deva',28,GOLD,'center');
  T(450,972,'\u0930\u093e\u0935\u0923 \u0915\u093e \u0906\u0915\u093e\u0936 \u092e\u0939\u0932','Deva',30,PAPER,'center');g.restore();}
 if(IMGS.ussC.width)papercut(lt,K.uss,IMGS.ussC,1420,400,560,0.03,'USSANGODA \u00b7 LAAL ZAMEEN','REAL PHOTO','#2a6a3a',73);
 kword(lt,K.vim,'\u092a\u0941\u0937\u094d\u092a\u0915 \u0935\u093f\u092e\u093e\u0928',1420,150,GOLD);
 if(IMGS.ussS.width)papercut(lt,K.serp,IMGS.ussS,1500,800,380,-0.03,'SERPENTINE SOIL','REAL PHOTO','#2a6a3a',75);
 const dd=ss(K.do,K.do+0.4,lt);
 if(dd>0)T(960,330,'\u0926\u094b \u091c\u0935\u093e\u092c\u2026 \u090f\u0915 \u0939\u0940 \u095b\u092e\u0940\u0928','Deva',46,ORG,'center',dd);
}
function fig7(t,lt){
 const K=KT[7];
 figbar(lt,'MAHAVAMSA \u00b7 5TH CENTURY','FIG. 08 \u00b7 TWIST');
 kickerD(lt,0.5,'WO SAWAL \u00b7 JO SAB PALTE','\u0915\u093f\u0924\u093e\u092c \u0916\u093e\u092e\u094b\u0936');
 const mv=ss(K.mv,K.mv+0.5,lt);
 if(mv>0){g.save();g.globalAlpha=mv;g.translate(430,500+(1-ov(mv))*60);
  g.fillStyle='#14100c';g.strokeStyle=GOLD;g.lineWidth=4;
  rrect(-190,-240,380,480,10);g.fill();g.stroke();
  g.strokeStyle='rgba(232,178,74,0.45)';rrect(-164,-214,328,428,6);g.stroke();
  T(0,-120,'\u092e\u0939\u093e\u0935\u0902\u0936','Deva',56,GOLD,'center');
  T(0,-50,'PALI CHRONICLE','Mono',22,'rgba(238,242,248,0.6)','center',1,2);
  T(0,10,'\u0930\u093e\u091c\u093e\u0913\u0902 \u0915\u0940','Deva',30,PAPER,'center');
  T(0,56,'\u092a\u0942\u0930\u0940 \u0938\u0942\u091a\u0940','Deva',30,PAPER,'center');
  g.restore();}
 const nm=ss(K.naam,K.naam+0.3,lt);
 if(nm>0){g.save();const sc=1.7-0.7*ov(nm);g.globalAlpha=nm;
  g.translate(430,0);g.scale(sc,sc);g.rotate(-0.05);
  g.strokeStyle=RED;g.lineWidth=7;g.font='52px Deva';g.textAlign='center';g.textBaseline='middle';
  const txt='\u0930\u093e\u0935\u0923 \u0915\u093e \u0928\u093e\u092e \u2014 \u0928\u0939\u0940\u0902';
  const tw=g.measureText(txt).width;
  rrect(-tw/2-30,820/sc-50,tw+60,100,12);g.stroke();
  g.fillStyle=RED;g.fillText(txt,0,824/sc);g.restore();}
 if(IMGS.engV.width)papercut(lt,K.agni,IMGS.engV,1430,480,560,0.03,'SITA KATHA \u00b7 KALPANA','AI ART','#7a5a20',81);
 kword(lt,K.div,'\u0926\u093f\u0935\u0941\u0930\u0941\u092e\u092a\u094b\u0932\u093e',1430,150,GOLD);
 chip(lt,K.kasam,1430,840,'\u0906\u091c \u092d\u0940 \u0915\u0938\u092e \u092f\u0939\u0940\u0902 \u0916\u093e\u0908 \u091c\u093e\u0924\u0940 \u0939\u0948',GOLD,620);
 typew(lt,K.likhi,'KITABON MEIN NAHI... ZINDAGI MEIN',12,140,960,'Mono',30,CYAN,'left');
}
function fig8(t,lt){
 const K=KT[8];
 figbar(lt,'TEEN GAWAH \u00b7 EK FAISLA','FIG. 09 \u00b7 VERDICT');
 stampD(lt,K.gawah,480,400,'\u092a\u0924\u094d\u0925\u0930 \u0917\u0935\u093e\u0939',GOLD,46,-0.05);
 stampD(lt,K.kham,960,560,'\u0915\u093f\u0924\u093e\u092c \u0916\u093c\u093e\u092e\u094b\u0936',CYAN,46,0.04);
 stampD(lt,K.zinda,1440,400,'\u092a\u0930\u0902\u092a\u0930\u093e \u095b\u093f\u0902\u0926\u093e',ORG,46,-0.03);
 const aa=ss(K.aastha,K.aastha+0.5,lt);
 if(aa>0){g.save();g.globalAlpha=aa;
  g.fillStyle='rgba(8,8,14,0.82)';rrect(560,700,800,140,14);g.fill();
  g.strokeStyle=GOLD;g.lineWidth=2;rrect(560,700,800,140,14);g.stroke();
  T(960,750,'\u0906\u0938\u094d\u0925\u093e + \u0936\u094b\u0927','Deva',40,GOLD,'center');
  T(960,806,'\u0926\u094b\u0928\u094b\u0902 \u0915\u093e \u0938\u092e\u094d\u092e\u093e\u0928','Deva',32,PAPER,'center');g.restore();}
 const ff2=ss(K.faisla,K.faisla+0.4,lt);
 if(ff2>0){g.save();const sc=1.4-0.4*ov(ff2);g.globalAlpha=ff2;
  g.translate(960,0);g.scale(sc,sc);
  T(0,930/sc,'\u092c\u093e\u0915\u093c\u0940 \u092b\u093c\u0948\u0938\u0932\u093e\u2026 \u0906\u092a\u0915\u093e','Deva',54,PAPER,'center');g.restore();}
}
function fig9(t,lt){
 const K=KT[9];
 figbar(lt,'AAPKI BAARI','FIG. 10 \u00b7 YOUR TURN');
 chip(lt,K.comment,480,380,'\u0915\u094c\u0928 \u0938\u093e \u0928\u093f\u0936\u093e\u0928 \u092a\u0939\u0932\u0947?',ORG,560);
 const names=['\u0938\u0940\u0924\u093e \u092e\u0902\u0926\u093f\u0930','\u0939\u0915\u0917\u0932\u093e','\u091d\u0930\u0928\u093e','\u0917\u0941\u092b\u093e','\u092a\u094b\u0915\u0941\u0928\u093e','\u0938\u093f\u0917\u093f\u0930\u093f\u092f\u093e','\u0909\u0938\u094d\u0938\u0928\u0917\u094b\u0921\u093e'];
 for(let i=0;i<7;i++){
  const p=ss(K.comment+0.3+i*0.14,K.comment+0.6+i*0.14,lt);if(p<=0)continue;
  g.save();g.globalAlpha=p;g.translate(230+(i%4)*228,530+Math.floor(i/4)*88+(1-ov(p))*30);
  g.fillStyle='rgba(10,8,16,0.8)';g.strokeStyle=i%2?GOLD:CYAN;g.lineWidth=2;
  rrect(-102,-33,204,66,12);g.fill();g.stroke();
  T(0,2,names[i],'Deva',24,i%2?GOLD:CYAN,'center');g.restore();}
 if(IMGS.logo.width){
  g.save();const pu=1+0.012*Math.sin(t*2.2);
  g.translate(1430,680);g.scale(pu,pu);g.translate(-1430,-680);
  papercut(lt,1.4,IMGS.logo,1430,680,520,0.025,'CHRONIC OF HISTORIC','HAMARA SAFAR',GOLD,91);
  g.restore();}
 const sb=ss(K.sub,K.sub+0.5,lt);
 if(sb>0){const pu=1+0.05*Math.sin(t*3.4)*(0.5+0.5*Math.sin(t*0.9));
  g.save();g.globalAlpha=sb;g.translate(620,860);g.scale(pu,pu);
  g.fillStyle=RED;rrect(-190,-44,380,88,16);g.fill();
  T(0,2,'\u25bc SUBSCRIBE','InterB',38,'#fff','center');g.restore();}
 const by=ss(K.yatra,K.yatra+0.6,lt);
 if(by>0)T(620,960,'\u092e\u093f\u0932\u0924\u0947 \u0939\u0948\u0902\u2026 \u0905\u0917\u0932\u0940 \u092f\u093e\u0924\u094d\u0930\u093e \u092e\u0947\u0902','Deva',40,GOLD,'center',by);
 const out=ss(DUR[9]+1.6,DUR[9]+3.0,lt);
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
 if(in3D(t)){draw3D(t);}
 else{
  const sh=shotAt(bi,lt);
  if(sh&&sh.v!=='ANIM'){const v=VIDS[sh.v];
   if(v&&v.duration)await seekV(v,(sh.off+sh.lt2*0.9)%(v.duration-0.12));}
  drawBG(sh,t);}
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
 ['Anton','InterB','Mono','Deva'].forEach(f=>{g.font='30px '+f;g.fillText('Ag \u0905',-100,-100);});
 const wait=()=>{if(nimg>=want&&nvid>=wantvid){
  Promise.resolve().then(async()=>{await draw(1);await draw(80);await draw(T3A0+2);await draw(T3B0+2);await draw(300);window.__ready=true;}).catch(e=>{window.__err=''+(e.stack||e);});
 }else setTimeout(wait,60);};
 wait();}catch(e){window.__err=''+(e.stack||e);}});
}catch(e){window.__err=''+(e.stack||e);}
</script></body></html>"""
    html = html.replace("FONTFACES", ff).replace("THREELIB", three)
    html = html.replace("__TOT__", str(TOTAL)).replace("BEATSJ", json.dumps(BEATS)).replace("DURJ", json.dumps(DUR))
    html = html.replace("CAPSJ", json.dumps(make_caps())).replace("KTJ", json.dumps(KT))
    html = html.replace("__A0__", str(T3A0)).replace("__A1__", str(T3A1))
    html = html.replace("__B0__", str(T3B0)).replace("__B1__", str(T3B1))
    keys = sorted({sh[0] for bi in sel for sh in SHOTS[bi] if sh[0] != "ANIM"})
    loads = "\n".join("lv('%s','%s');" % (k, b64("/var/tmp/ram36/clips2/%s.mp4" % CLIPMAP[k]))
                      for k in keys)
    html = html.replace("WANTVID", str(len(keys))).replace("/*VIDLOADS*/", loads)
    html = html.replace("SHOTSJ", json.dumps(SHOTS))
    for tok, f in [("SITA64","ph_sita_temple.jpg"),("HAK64","ph_hakgala.jpg"),
                   ("FALLSP64","ph_falls_people.jpg"),("FALLSQ64","ph_falls_main.jpg"),
                   ("CAVEIN64","ph_cave_inside.jpg"),("CAVEST64","ph_cave_steps.jpg"),
                   ("SIGG64","ph_sigiriya_gold.jpg"),("SIGW64","ph_sigiriya_wide.jpg"),
                   ("USSC64","ph_ussangoda_coast.jpg"),("USSS64","ph_ussangoda_soil.jpg"),
                   ("SETUL64","ph_setu_landsat.jpg"),("SETUE64","ph_setu_esa.jpg"),
                   ("DHANC64","ph_dhanushkodi_church.jpg"),("DHANS64","ph_dhanushkodi_sand.jpg"),
                   ("ENGL64","eng_lanka.jpg"),("ENGV64","eng_vatika.jpg")]:
        html = html.replace(tok, b64(os.path.join(RM, f)))
    html = html.replace("LOGO64", b64(LOGO))
    hp = os.path.join(ROOT, "page_%s.html" % os.environ.get("HALF", "ALL"))
    open(hp, "w").write(html)
    return hp, make_caps()

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
    half = os.environ.get("HALF", "ALL")
    sel = {0, 1, 2, 3, 4} if half == "A" else ({5, 6, 7, 8, 9} if half == "B" else set(SHOTS))
    n_all = int(round(TOTAL * FPS))
    f0 = 0 if half in ("A", "ALL") else int(round(BEATS[5] * FPS))
    f1 = int(round(BEATS[5] * FPS)) if half == "A" else n_all
    hp, caps = build_html(sel)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True,
                                    args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 200, "height": 200})
        page.goto("file://" + hp)
        try:
            page.wait_for_function("window.__ready === true || window.__err", timeout=240000)
        except Exception:
            pass
        err = page.evaluate("window.__err||''")
        if err:
            print("PAGE ERROR:", err); browser.close(); return
        if mode == "--preview":
            chk = os.environ.get("CHK_TIMES")
            TSL = ([float(x) for x in chk.split(",")] if chk
                   else [BEATS[i] + DUR[i] * 0.72 for i in range(len(DUR))] + [T3A0 + 3, T3B0 + 3.5])
            TSL = [t for t in TSL if f0 / FPS <= t < f1 / FPS]
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
        t0 = time.time(); i = f0
        while i < f1:
            batch = [k for k in range(i, min(i + 10, f1))
                     if not os.path.exists(os.path.join(FR, "%05d.jpg" % k))]
            if batch:
                urls = page.evaluate("ts => window.renderBatch(ts)", [k / FPS for k in batch])
                for k, d in zip(batch, urls):
                    open(os.path.join(FR, "%05d.jpg" % k), "wb").write(base64.b64decode(d.split(",", 1)[1]))
            i += 10
            if (i // 10) % 40 == 0:
                print("frame %d/%d (%.1f fps)" % (i, f1, (i - f0) / max(0.01, time.time() - t0)), flush=True)
        browser.close()
    print("FRAMES DONE half=%s range=%d-%d" % (half, f0, f1), flush=True)
    if half in ("B", "ALL"):
        build_audio()
        write_srt(caps, os.path.join(ROOT, "final.srt"))
        print("AUDIO+SRT DONE TOTAL=%.2f" % TOTAL)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "--render")
