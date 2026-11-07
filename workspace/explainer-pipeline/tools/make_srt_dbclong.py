import json,re,subprocess,glob
AST='/home/user/explainer-pipeline/assets/dbclong'
TL=json.load(open(f'{AST}/tl.json'))
# final VO texts (keep in sync with generated audio!)
texts=[open(f'{AST}/SCRIPT.md').read()]
# extract from SCRIPT.md sections "### voN"
md=texts[0]
chunks=[]
for i in range(1,7):
    m=re.search(rf'### vo{i}[^\n]*\n(.*?)(?=\n###|\n---|\Z)',md,re.S)
    chunks.append(m.group(1).strip().replace('\n',' '))
def fmt(t):
    h=int(t//3600);m=int(t%3600//60);s=t%60
    return f'{h:02d}:{m:02d}:{s//1:02.0f},{int(s%1*1000):03d}'.replace('.',':',0) if False else f'{h:02d}:{m:02d}:{int(s):02d},{int(s%1*1000):03d}'
idx=1;out=[]
for i,s in enumerate(TL['s']):
    sents=re.split(r'(?<=[.!?]) +',chunks[i])
    total=sum(len(x) for x in sents)
    t=s['vo']
    for sn in sents:
        d=s['vod']*len(sn)/total
        # split long sentences into <=90 char cues
        parts=[sn[j:j+90] for j in range(0,len(sn),90)] if len(sn)>90 else [sn]
        pd=d/len(parts)
        for p_ in parts:
            out.append(f"{idx}\n{fmt(t)} --> {fmt(min(t+pd,s['vo']+s['vod']))}\n{p_.strip()}\n")
            t+=pd;idx+=1
open('/home/user/outputs/dbcooper-complete-file.srt','w').write('\n'.join(out))
print('srt cues',idx-1)
