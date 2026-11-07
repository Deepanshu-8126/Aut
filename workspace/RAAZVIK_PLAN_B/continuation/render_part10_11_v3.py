from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import cv2,subprocess,imageio_ffmpeg,sys,json,math
P=Path('/home/user/RAAZVIK_PLAN_B/continuation');A=P/'assets';O=P/'v3_work';O.mkdir(exist_ok=True);F=Path('/home/user/explainer-pipeline/assets/fonts');ff=imageio_ffmpeg.get_ffmpeg_exe();W,H=1280,720
hi=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),40);mid=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),29);small=ImageFont.truetype(str(F/'NotoSansDevanagari-Bold.ttf'),20);en=ImageFont.truetype(str(F/'Inter-Bold.ttf'),27);enbig=ImageFont.truetype(str(F/'Inter-Bold.ttf'),36)
# Each tuple: absolute start, kind, source, explicit on-screen context, headline; next start defines end.
B=[
(433.625,'ai','p10_search_plans','एआई दृश्य  काल्पनिक खोज तैयारी','खोज की तैयारी'),
(435.47,'ai','search','एआई दृश्य  काल्पनिक खोज',''),
(439.55,'video','857196','आधुनिक फुटेज  वास्तविक खोज नहीं',''),
(443.08,'video','13171168','स्विस ग्लेशियर  संदर्भ फुटेज','इलाका बहुत बड़ा था'),
(446.62,'ai','search_crevasse_new','एआई दृश्य  काल्पनिक खोज',''),
(450.70,'real','nanda_west','नंदा देवी  बाद की संदर्भ तस्वीर','ठिकाना तय नहीं'),
(452.46,'ai','p10_search_scan','एआई दृश्य  काल्पनिक खोज','खोज मुश्किल क्यों थी?'),
(456.23,'ai','snow_rocks_new','एआई दृश्य  काल्पनिक बर्फ और चट्टानें',''),
(459.06,'ai','winter_weather_new','एआई दृश्य  काल्पनिक सर्दी',''),
(462.12,'ai','p10_rope_team','एआई दृश्य  काल्पनिक ग्लेशियर',''),
(465.50,'real','camp95','नंदा देवी कैंप १९९५  मिशन नहीं','इलाका बदल सकता है'),
(470.25,'ai','return','एआई दृश्य  काल्पनिक खोज',''),
(476.40,'ai','different_roles','एआई दृश्य  काल्पनिक टीम',''),
(480.26,'ai','cache','एआई दृश्य  काल्पनिक सामान','सुरक्षा भी जरूरी'),
(486.55,'ai','search_instrument_new','एआई दृश्य  काल्पनिक जांच उपकरण',''),
(491.26,'video','climber_new','आधुनिक फुटेज  वास्तविक खोज नहीं',''),
(494.76,'real','nanda_north','नंदा देवी  बाद की संदर्भ तस्वीर','सटीक ठिकाना नहीं मिला'),
(497.56,'graphic','hypothesis','सांकेतिक चित्र  वास्तविक घटना नहीं',''),
(504.62,'graphic','uncertainty','सांकेतिक चित्र  साबित तस्वीर नहीं','संभावना  पक्का सबूत नहीं'),
(509.50,'video','weather_extra','संदर्भ फुटेज  स्थान अज्ञात','सटीक ठिकाना अज्ञात'),
(516.38,'real','nanda_outer','नंदा देवी  बाद की संदर्भ तस्वीर',''),
(518.49,'graphic','two_devices','सांकेतिक चित्र  असली उपकरण नहीं','एक दूसरी मशीन भी थी'),
(524.85,'real','nanda_kot','नंदा कोट  १९९२  संदर्भ तस्वीर','अलग पहाड़  अलग मशीन'),
(529.28,'graphic','memo_second','स्रोत: अमेरिकी विदेश विभाग  १४ अप्रैल १९७८',''),
(537.47,'graphic','contrast','सांकेतिक चित्र  असली उपकरण नहीं','गलतफहमी यहाँ होती है'),
(542.54,'graphic','contrast_reveal','सांकेतिक चित्र  असली उपकरण नहीं','दूसरी मशीन हटना'),
(545.50,'graphic','contrast_missing','सांकेतिक चित्र  असली उपकरण नहीं','पहली मशीन मिलने का सबूत नहीं'),
(549.30,'graphic','two_mountains','सांकेतिक चित्र  भौगोलिक नक्शा नहीं','दो पहाड़  दो अलग मशीनें'),
(552.54,'graphic','memo_awareness','स्रोत: अमेरिकी विदेश विभाग  १४ अप्रैल १९७८',''),
(558.16,'real','desai','कार्टर और देसाई  जून १९७८  अलग अवसर',''),
(561.83,'ai','p10_report_compare','एआई दृश्य  काल्पनिक अध्ययन','खबर के बाद नए सवाल'),
(565.35,'graphic','questions','सांकेतिक चित्र','किसे क्या पता था?'),
(572.25,'real','nanda2016','नंदा देवी  २०१६  संदर्भ तस्वीर',''),
(576.28,'graphic','press_scrutiny','सांकेतिक चित्र  असली अखबार नहीं','१९७८ में खबर सामने आई'),
(580.09,'ai','recording','एआई दृश्य  वास्तविक खबर की तस्वीर नहीं',''),
(585.45,'graphic','questions_india','सांकेतिक चित्र','भारत में भी सवाल उठे'),
(588.78,'graphic','memo_reporting','स्रोत: अमेरिकी विदेश विभाग  १४ अप्रैल १९७८',''),
(600.12,'real','parliament','संसद में कार्टर  जनवरी १९७८  अलग अवसर',''),
(605.61,'video','river139','संदर्भ फुटेज  नदी का स्थान स्थापित नहीं',''),
(608.14,'video','river548','संदर्भ फुटेज  नदी की पहचान नहीं','नदियों की चिंता'),
(614.76,'graphic','capsule_question','सांकेतिक चित्र  असली कैप्सूल नहीं','अगर कैप्सूल टूटे?'),
(620.83,'graphic','concern_proof','सांकेतिक चित्र','चिंता और सबूत अलग हैं'),
(626.62,'ai','p10_field_sample','एआई दृश्य  काल्पनिक नमूना जांच',''),
(630.49,'ai','samples_lab_new','एआई दृश्य  काल्पनिक प्रयोगशाला','जाँचे गए नमूनों में प्रदूषण नहीं मिला'),
(635.26,'graphic','sample_limit','सांकेतिक चित्र','कैप्सूल की हालत अज्ञात'),
(640.85,'video','lab412','आधुनिक लैब  वास्तविक जांच नहीं','नतीजा उसी नमूने और समय का'),
]
C=[
(650.625,'ai','p11_report_reader','एआई दृश्य  काल्पनिक अध्ययन','सालों बाद एक सुराग'),
(654.35,'graphic','week','स्रोत सारांश  यह असली अखबार की तस्वीर नहीं','द वीक की रिपोर्ट'),
(660.62,'ai','emptybox','एआई दृश्य  वास्तविक खोज की वस्तु नहीं','१९९३ का अभियान'),
(666.73,'graphic','case_possible','सांकेतिक चित्र  असली हिस्सा नहीं','संभावित बाहरी हिस्सा'),
(671.61,'graphic','week_account','स्रोत सारांश  काल्पनिक प्रस्तुति','बयान में खाली बक्सों का जिक्र'),
(675.61,'graphic','outside_box','सांकेतिक चित्र  असली बॉक्स नहीं','बाहरी डिब्बा'),
(680.00,'graphic','capsule_diff','सांकेतिक चित्र  असली कैप्सूल नहीं','कैप्सूल अलग चीज है'),
(684.62,'graphic','capsule_no','सांकेतिक चित्र  बरामदगी का सबूत नहीं','कैप्सूल मिलने की पुष्टि नहीं'),
(688.45,'ai','research_archive_new','एआई दृश्य  काल्पनिक अध्ययन','पहचान लोगों के अनुमान पर आधारित'),
(694.14,'graphic','report_not_final','स्रोत सारांश  अंतिम प्रमाण नहीं','संभावित सुराग'),
(699.38,'ai','p11_waterlab','एआई दृश्य  काल्पनिक जल जांच',''),
(704.52,'video','lab832','आधुनिक लैब  वास्तविक जांच नहीं','नमूनों से ठिकाना तय नहीं'),
(708.88,'graphic','question_scrutiny','सांकेतिक चित्र','अगर हिस्सा उसी मशीन का हो'),
(713.88,'graphic','unknown_evidence','सांकेतिक चित्र','पूरा जवाब नहीं'),
(716.42,'graphic','clue_year','सांकेतिक चित्र','१९९३ की रिपोर्ट में एक और बात'),
(719.84,'graphic','week_member2','स्रोत सारांश  वास्तविक दस्तावेज नहीं','एक सदस्य का बयान'),
(725.32,'ai','p11_box_hand','एआई दृश्य  काल्पनिक खाली बॉक्स',''),
(731.34,'ai','p11_box_carry','एआई दृश्य  काल्पनिक उदाहरण','एक बॉक्स नीचे लाने का बयान'),
(734.80,'ai','old_box_new','एआई दृश्य  वास्तविक वस्तु नहीं','लोगों का अनुमान'),
(741.34,'graphic','source_limits','स्रोत सारांश  स्वतंत्र पहचान बाकी','अनुमान को अनुमान ही समझें'),
(749.18,'graphic','no_capsule','सांकेतिक चित्र  कोई बरामद कैप्सूल नहीं','कैप्सूल मिलने का सार्वजनिक सबूत नहीं'),
(756.04,'graphic','no_capsule2','सांकेतिक चित्र  कोई बरामद कैप्सूल नहीं','रिपोर्ट: कैप्सूल नहीं मिले'),
(760.22,'graphic','image_proof','सांकेतिक चित्र  असली बॉक्स की तस्वीर नहीं','तस्वीर को बिना जांच अंतिम सबूत नहीं'),
(767.12,'graphic','clue_possible2','सांकेतिक चित्र','संभावित सुराग  अंतिम जवाब नहीं'),
(776.50,'ai','p11_unknown2','एआई दृश्य  वास्तविक ठिकाना नहीं','आज कितना खतरा?'),
(780.40,'graphic','unknown_three','सांकेतिक चित्र','पक्के जवाब के लिए क्या जानना होगा?'),
(785.08,'graphic','unknown_where','सांकेतिक चित्र','कैप्सूल कहाँ हैं?'),
(787.50,'graphic','unknown_shell','सांकेतिक चित्र','सुरक्षा परत किस हालत में है?'),
(790.98,'graphic','unknown_release','सांकेतिक चित्र','पदार्थ बाहर निकला या नहीं?'),
(794.58,'graphic','health_breath','सामान्य स्वास्थ्य जानकारी  वास्तविक संपर्क नहीं','कण सांस से शरीर में जाएं'),
(798.16,'graphic','health_ingest','सामान्य स्वास्थ्य जानकारी  वास्तविक संपर्क नहीं','या खाने से शरीर में जाएं'),
(801.90,'video','river596','संदर्भ फुटेज  नदी की पहचान नहीं','बिना सबूत पानी जहरीला नहीं कह सकते'),
(806.72,'ai','water','एआई दृश्य  काल्पनिक जलधारा','बाढ़ का कारण साबित नहीं'),
(811.70,'graphic','known_unknown','सांकेतिक चित्र','जो पता है  और जो नहीं'),
(818.85,'ai','route_team','एआई दृश्य  असली टीम नहीं','भारत और अमेरिका का मिशन'),
(821.74,'ai','storm','एआई दृश्य  वास्तविक तूफान नहीं','खराब मौसम में वापसी'),
(824.60,'real','nanda2009','नंदा देवी  २००९  संदर्भ तस्वीर','अगले साल सामान नहीं मिला'),
(827.48,'real','nanda_kot2','नंदा कोट और चंगुच  २०११  संदर्भ तस्वीर','दूसरे पहाड़ पर अलग मशीन'),
(830.10,'graphic','recap_parts','सांकेतिक चित्र  असली हिस्सा नहीं','संभावित हिस्सों की रिपोर्ट'),
(833.48,'graphic','end_capsules','सांकेतिक चित्र  बरामदगी का सबूत नहीं','मूल कैप्सूलों का अंतिम जवाब नहीं'),
(839.76,'real','nanda_west2','नंदा देवी  बाद की संदर्भ तस्वीर',''),
(845.76,'graphic','end_question','सांकेतिक चित्र','वो गई कहाँ?'),
]
# Repeating an illustration at a different point of the same narrative uses a different crop/composition.
IMAGES={
'nanda2016':Path('/home/user/RAAZVIK_PLAN_B/chapter03/new_assets/nanda_2016.jpg'),'nanda2009':Path('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_2009.jpg'),'nanda1936':Path('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_1936.jpg'),'different_roles':Path('/home/user/RAAZVIK_PLAN_B/chapter06/assets/different_roles.png'),'water':A/'water.png','nanda_west':A/'nanda_west.jpg','nanda_west2':A/'nanda_slope_ref.jpg','nanda_north':Path('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_north_1980.jpg'),'nanda_outer':Path('/home/user/RAAZVIK_PLAN_B/chapter05/assets/nanda_outer_1980.jpg'),'camp95':Path('/home/user/RAAZVIK_PLAN_B/chapter04/assets/nanda_camp_1995.jpg'),'nanda_kot':A/'nanda_kot_1992.jpg','nanda_kot2':A/'kot_changuch_2011.jpg','desai':A/'desai_carter_1978.jpg','parliament':A/'parliament_jan1978.jpg',
'p11_report_reader2':A/'p11_report_reader.png','p11_box_hand2':A/'p11_box_hand.png','p11_box_hand3':A/'p11_box_hand.png','old_box_new2':A/'old_box_new.png','return2':A/'return.png','emptybox2':A/'emptybox.png'}
for n in ['p10_search_plans','search','search_crevasse_new','p10_search_scan','snow_rocks_new','winter_weather_new','p10_rope_team','return','cache','search_instrument_new','p11_unknown','p10_report_compare','research_archive_new','recording','p10_field_sample','samples_lab_new','p11_report_reader','emptybox','old_box_new','p11_waterlab','p11_box_hand','p11_box_carry','p11_unknown2','route_team','storm']:
 IMAGES[n]=A/((n.replace('unknown2','unknown'))+'.png')
VIDS={'weather_extra':Path('/home/user/RAAZVIK_PLAN_B/chapter01/pexels_weather_11279478.mp4'),'lab832':A/'pexels_8327076_clip.mp4','lab412':A/'pexels_4120946_clip.mp4','857196':A/'pexels_857196_clip.mp4','13171168':A/'pexels_13171168_clip.mp4','climber_new':Path('/home/user/RAAZVIK_PLAN_B/chapter07/assets/climber_clip.mp4'),'river139':A/'pexels_river_13979212.mp4','river139_b':A/'pexels_river_13979212.mp4','river548':A/'pexels_5485160_clip.mp4','river548_b':A/'pexels_5485160_clip.mp4','river596':A/'pexels_5966051_clip.mp4'}

def txt(d,p,s,font=hi,fill='#f8f5e9'):
 d.text(p,s,font=font,fill=fill,stroke_width=2,stroke_fill='#08151a')
def foot(d,s):
 b=d.textbbox((0,0),s,font=small);d.rounded_rectangle((28,662,min(1250,56+b[2]),705),radius=5,fill=(6,20,23,235));txt(d,(38,666),s,small)
def image(p,alt=False):
 src=Image.open(p).convert('RGB');
 # Conservative alternate framing for a repeated concept, never a fake moving photo.
 if alt:
  w,h=src.size;src=src.crop((int(w*.10),int(h*.03),int(w*.96),int(h*.94)))
 return ImageEnhance.Brightness(ImageOps.fit(src,(W,H),Image.Resampling.LANCZOS)).enhance(.82).convert('RGBA')
def doc_card(d,title,english1,english2):
 txt(d,(55,55),title,hi);txt(d,(55,115),'१४ अप्रैल १९७८',mid,fill='#efc793');d.rounded_rectangle((55,200,1225,495),radius=12,fill='#e5e2d6');d.text((88,222),'MEMORANDUM TO PRESIDENT CARTER',font=enbig,fill='#25343a');d.text((88,317),english1,font=en,fill='#25343a');d.text((88,365),english2,font=en,fill='#25343a')
def graphic(key,t,start,title):
 im=Image.new('RGBA',(W,H),(14,31,38,255));d=ImageDraw.Draw(im)
 if key.startswith('memo_'):
  if key=='memo_second':doc_card(d,'अमेरिकी विदेश विभाग का नोट','“the second did function for several years','and was later removed.”')
  elif key=='memo_awareness':doc_card(d,'अमेरिकी विदेश विभाग का नोट','“Assertions ... that the Indian Government was','not informed ... are incorrect”')
  else:doc_card(d,'अमेरिकी विदेश विभाग का नोट','“Recent press stories ... are correct','in major respects.”')
 elif key=='uncertainty':
  txt(d,(50,55),'क्या सच में ऐसा हुआ?',hi);d.ellipse((380,155,850,565),outline='#9db4b4',width=5);txt(d,(565,240),'?',hi,fill='#efc793');txt(d,(375,540),'यह अनुमान है, साबित घटना नहीं',mid)
 elif key=='hypothesis':
  txt(d,(50,60),'मशीन की गर्मी और बर्फ',hi);d.rounded_rectangle((115,235,470,420),radius=20,outline='#e9b980',width=4,fill='#3d5053');txt(d,(170,300),'गर्मी',hi,fill='#e9b980');d.line((490,326,745,326),fill='#e8cfa4',width=5);d.polygon([(745,326),(720,313),(720,339)],fill='#e8cfa4');d.polygon([(800,410),(900,210),(1030,410)],fill='#bcd1d4');phase=((t-start)*.55)%1;cx=490+int(230*phase);d.ellipse((cx-7,319,cx+7,333),fill='#fff0c8');txt(d,(1070,245),'?',hi,fill='#e9b980');txt(d,(60,530),'अनुमान  साबित घटना नहीं',mid,fill='#efc793')
 elif key in ['two_devices','contrast','contrast_reveal','contrast_missing','two_mountains']:
  if key!='contrast' or t>=539.71:txt(d,(48,56),title or 'अलग पहाड़  अलग मशीन',hi)
  if key in ['two_devices','contrast']:
   d.rounded_rectangle((80,205,570,475),radius=20,outline='#93adb4',width=3,fill='#2b454d');d.rounded_rectangle((710,205,1200,475),radius=20,outline='#d5bd8b',width=3,fill='#34444a');txt(d,(165,250),'नंदा देवी',hi);txt(d,(810,250),'नंदा कोट',hi,fill='#edcb93');txt(d,(165,340),'पहली मशीन',mid);txt(d,(810,340),'दूसरी मशीन',mid,fill='#edcb93')
  elif key=='contrast_reveal':
   d.polygon([(180,480),(420,190),(660,480)],fill='#5a747a');txt(d,(260,515),'नंदा कोट',mid);d.rounded_rectangle((820,235,1060,385),radius=22,fill='#d2bf98');phase=min(1,max(0,(t-start)/2));x=int(phase*120);d.line((800,430,1060+x,430),fill='#e5d0a1',width=4);d.polygon([(1060+x,430),(1040+x,420),(1040+x,440)],fill='#e5d0a1');txt(d,(820,505),'दूसरी मशीन हटाई',mid,fill='#edcb93')
  elif key=='contrast_missing':
   d.polygon([(100,480),(365,200),(630,480)],fill='#49656e');txt(d,(230,515),'नंदा देवी',mid);d.rounded_rectangle((800,235,1070,385),radius=22,outline='#9fb3b0',width=3);txt(d,(920,270),'?',hi,fill='#edcb93');txt(d,(735,505),'पहली मशीन का ठिकाना अज्ञात',mid)
  else:
   d.polygon([(90,470),(300,220),(510,470)],fill='#49656e');d.polygon([(760,470),(970,220),(1180,470)],fill='#6e7775');txt(d,(160,510),'नंदा देवी',mid);txt(d,(830,510),'नंदा कोट',mid,fill='#edcb93')
 elif key=='week_member2':
  txt(d,(50,55),title,hi);d.ellipse((145,180,330,365),outline='#c0ceca',width=5);d.arc((105,320,370,535),180,360,fill='#c0ceca',width=5);d.rounded_rectangle((470,185,1120,410),radius=24,fill='#e7e5da');d.text((520,225),'THE WEEK',font=enbig,fill='#293940');d.text((520,310),'अभियान के सदस्य का बयान',font=mid,fill='#293940')
 elif key in ['week','week_account','report_not_final','source_limits']:
  txt(d,(50,55),title or 'रिपोर्ट और दावा',hi)
  if key=='week':
   d.rounded_rectangle((75,185,1200,475),radius=15,fill='#e8e5da');d.text((110,220),'THE WEEK',font=enbig,fill='#2a363a');d.text((110,310),'संबंधित लोगों का बयान',font=hi,fill='#293940');d.text((110,380),'संभावित सुराग  अंतिम प्रमाण नहीं',font=mid,fill='#293940')
  elif key=='week_account':
   d.rounded_rectangle((85,195,590,460),radius=15,fill='#e8e5da');d.text((115,230),'THE WEEK',font=enbig,fill='#293940');d.text((115,320),'एक सदस्य का बयान',font=mid,fill='#293940');d.rounded_rectangle((730,270,1080,385),radius=12,outline='#b6c4be',width=4,fill='#566c70');txt(d,(780,475),'अभियान का बयान',mid)
  elif key=='report_not_final':
   d.ellipse((100,180,340,420),outline='#b6c9c6',width=5);txt(d,(175,235),'?',hi,fill='#efc793');txt(d,(410,220),'संभावित सुराग',hi);txt(d,(410,310),'अंतिम पहचान नहीं',hi,fill='#efc793')
  else:
   d.rounded_rectangle((100,190,1180,455),radius=14,outline='#a1b6b5',width=3);txt(d,(150,245),'अभियान में शामिल लोगों का अनुमान',mid);txt(d,(150,335),'स्वतंत्र पुष्टि जरूरी',hi,fill='#efc793')
 elif key=='no_capsule2':
  txt(d,(50,55),title,hi);d.rounded_rectangle((80,190,1200,475),radius=14,fill='#e5e2d6');d.text((115,225),'THE WEEK',font=enbig,fill='#28373c');d.text((115,330),'रिपोर्ट के मुताबिक कैप्सूल नहीं मिले',font=hi,fill='#28373c')
 elif key in ['outside_box','capsule_diff','capsule_no','no_capsule','end_capsules','capsule_question']:
  txt(d,(50,55),title,hi);d.rounded_rectangle((100,235,525,425),radius=18,fill='#3c535b',outline='#a6b9b7',width=3);d.rounded_rectangle((160,290,460,380),radius=8,fill='#829297');txt(d,(175,475),'बाहरी डिब्बा',mid)
  if key!='outside_box':
   d.rounded_rectangle((760,280,1100,368),radius=44,fill='#798b93',outline='#d3d8c5',width=3);txt(d,(820,475),'कैप्सूल',mid);d.text((600,290),'≠',font=enbig,fill='#efca92')
  if key in ['capsule_no','no_capsule','end_capsules']:
   d.rounded_rectangle((785,395,1115,445),radius=5,outline='#e4c694',width=2);txt(d,(797,396),'बरामदगी अज्ञात',small,fill='#e4c694')
 elif key in ['case_possible','possible_clue','clue_possible2','image_proof','clue_year','unknown_evidence','press_scrutiny','question_scrutiny']:
  txt(d,(50,55),title,hi)
  if key in ['case_possible','possible_clue']:
   d.rounded_rectangle((260,240,800,450),radius=20,fill='#697e80',outline='#b4c3bc',width=4);d.line((260,300,800,300),fill='#cad2bf',width=4);txt(d,(930,245),'?',hi,fill='#efc793')
  elif key=='question_scrutiny':
   d.rounded_rectangle((130,260,440,430),radius=15,outline='#b4c3bc',width=4);d.line((505,345,725,345),fill='#e9c48d',width=4);d.polygon([(725,345),(705,335),(705,355)],fill='#e9c48d');d.rounded_rectangle((785,220,1100,450),radius=18,outline='#a9bcba',width=4);txt(d,(925,285),'?',hi,fill='#efc793')
  elif key=='image_proof':
   d.rounded_rectangle((165,170,730,480),radius=14,outline='#a6b9b7',width=5);d.polygon([(215,430),(400,245),(560,430)],fill='#597781');d.ellipse((850,210,1050,410),outline='#e5c792',width=7);d.line((1020,375,1130,485),fill='#e5c792',width=9)
  elif key=='clue_year':
   d.rounded_rectangle((120,210,1160,440),radius=16,fill='#314b53');d.text((200,260),'1993',font=enbig,fill='#efc793');txt(d,(440,255),'अभियान का बयान',hi)
  elif key=='press_scrutiny':
   d.rounded_rectangle((160,190,730,470),radius=12,outline='#a9bcba',width=4);d.line((220,260,660,260),fill='#a9bcba',width=5);d.line((220,315,570,315),fill='#a9bcba',width=5);txt(d,(910,265),'?',hi,fill='#efc793')
  elif key=='unknown_evidence':
   d.rounded_rectangle((220,170,1060,480),radius=15,outline='#a9bcba',width=4);txt(d,(290,240),'पूरा जवाब अभी नहीं',hi);txt(d,(590,345),'?',hi,fill='#efc793')
  else:
   d.polygon([(80,450),(330,220),(520,450)],fill='#54727a');d.polygon([(540,450),(790,170),(1090,450)],fill='#6e7e7d');txt(d,(1080,190),'?',hi,fill='#efc793')
 elif key in ['unknown_where','unknown_shell','unknown_release','unknown_three']:
  txt(d,(50,55),title,hi)
  if key=='unknown_three':
   d.rounded_rectangle((150,245,430,370),radius=45,outline='#afc4bf',width=4);d.arc((520,185,800,435),200,340,fill='#e2c08e',width=7);txt(d,(1010,235),'?',hi,fill='#efc793')
  elif key=='unknown_where':
   d.polygon([(90,440),(320,210),(445,350),(600,180),(900,440)],fill='#597781');d.line([(90,440),(320,210),(445,350),(600,180),(900,440)],fill='#b8d0ce',width=4)
   txt(d,(970,235),'?',hi,fill='#efc793')
  else:
   d.rounded_rectangle((270,265,920,370),radius=50,fill='#71888c',outline='#d2dad0',width=4)
   if key=='unknown_shell':d.arc((205,175,985,480),190,350,fill='#e2c08e',width=7);txt(d,(1000,245),'?',hi,fill='#efc793')
   else:
    for i in range(5):
     x=1000+i*28;y=310+int(20*math.sin(i));d.ellipse((x-5,y-5,x+5,y+5),fill='#e2c08e')
    txt(d,(1100,205),'?',hi,fill='#efc793')
 elif key in ['health_breath','health_ingest']:
  txt(d,(55,55),'प्लूटोनियम के कण',hi);d.rounded_rectangle((80,220,580,420),radius=15,fill='#34505a',outline='#91adb0',width=3);d.rounded_rectangle((700,220,1200,420),radius=15,fill='#34505a',outline='#91adb0',width=3);txt(d,(150,290),'सांस से अंदर',hi,fill='#e9c48d' if key=='health_breath' else '#f6f1df');txt(d,(785,290),'खाने से अंदर',hi,fill='#e9c48d' if key=='health_ingest' else '#f6f1df');txt(d,(65,500),'शरीर के अंदर जाना चिंता का विषय',mid)
 else:
  txt(d,(55,60),title or 'क्या पता है?',hi);d.rounded_rectangle((75,220,1205,455),radius=18,fill='#2b454d',outline='#91a8a7',width=3)
  if key in ['unknown_three','unknown_where','unknown_shell','unknown_release']:
   if key=='unknown_three':txt(d,(120,285),'स्थान  सुरक्षा परत  पदार्थ',hi,fill='#efc793')
   else:txt(d,(120,285),title,hi,fill='#efc793')
  elif key=='known_unknown':txt(d,(150,290),'पता है',hi);txt(d,(760,290),'पता नहीं',hi,fill='#efc793')
  elif key=='sample_limit':txt(d,(125,285),'नमूने का नतीजा  कैप्सूल का ठिकाना नहीं',mid,fill='#efc793')
  elif key=='sample_location':txt(d,(125,285),'नमूनों से मौजूदा ठिकाना तय नहीं',mid,fill='#efc793')
  elif key in ['questions','questions_india']:txt(d,(125,285),'जानकारी?    खोज?    पानी की जांच?',hi,fill='#efc793')
  elif key=='concern_proof':txt(d,(140,285),'चिंता होना और प्रदूषण साबित होना अलग हैं',mid,fill='#efc793')
  elif key=='end_question':txt(d,(125,280),'वो गई कहाँ?',hi,fill='#efc793')
  else:txt(d,(125,285),title,mid,fill='#efc793')
 return im

def main(part):
 scenes=B if part=='10' else C;begin=433.625 if part=='10' else 650.625;end=650.625 if part=='10' else 847.25;N=round((end-begin)*24)
 manifest=[]
 for i,s in enumerate(scenes):manifest.append({'start':s[0],'end':scenes[i+1][0] if i+1<len(scenes) else end,'kind':s[1],'asset':s[2],'disclosure':s[3],'text':s[4]})
 (P/f'PART{part}_V3_SHOTLIST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));assert all(x['end']>x['start'] for x in manifest)
 used={s[2] for s in scenes if s[1] in ['ai','real']};imgs={n:image(IMAGES[n],n.endswith('2') or n.endswith('3')) for n in used};caps={n:cv2.VideoCapture(str(VIDS[n])) for n in {s[2] for s in scenes if s[1]=='video'}}
 out=O/f'part{part}_picture.mp4';enc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-frames:v',str(N),'-vf','scale=1920:1080','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 idx=0;last=-1
 for k in range(N):
  absolute=begin+k/24
  while idx+1<len(scenes) and absolute>=scenes[idx+1][0]:idx+=1
  st,typ,name,disclosure,title=scenes[idx]
  if typ=='video':
   cap=caps[name]
   if idx!=last:cap.set(cv2.CAP_PROP_POS_FRAMES,0)
   ok,b=cap.read()
   if not ok:cap.set(cv2.CAP_PROP_POS_FRAMES,0);ok,b=cap.read()
   assert ok,name
   im=ImageOps.fit(Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)),(W,H)).convert('RGBA')
  elif typ=='graphic':im=graphic(name,absolute,st,title)
  else:im=imgs[name].copy()
  d=ImageDraw.Draw(im)
  if title and typ!='graphic':txt(d,(45,54),title,mid)
  foot(d,disclosure);last=idx;enc.stdin.write(im.convert('RGB').tobytes())
  if k%480==0:print('part',part,'frame',k,'/',N,flush=True)
 enc.stdin.close();assert enc.wait()==0
 for c in caps.values():c.release()
 # Preserve the previously assembled, single original voice + SFX mix without adding layers.
 old=P/('RAAZVIK_CONTINUATION_B_V2_HD.mp4' if part=='10' else 'RAAZVIK_CONTINUATION_C_V2_HD.mp4')
 hd=P/f'RAAZVIK_PART{part}_V3_HD.mp4';subprocess.run([ff,'-v','error','-y','-i',str(out),'-i',str(old),'-map','0:v','-map','1:a','-t',str(end-begin),'-c:v','copy','-c:a','copy','-movflags','+faststart',str(hd)],check=True)
 mob=P/f'RAAZVIK_PART{part}_V3_MOBILE.mp4';subprocess.run([ff,'-v','error','-y','-i',str(hd),'-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-movflags','+faststart',str(mob)],check=True);print('DONE',part,flush=True)
if __name__=='__main__':main(sys.argv[1])
