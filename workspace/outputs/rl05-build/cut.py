import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
def cut(src,dst,shadow_band=0.14):
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(int); H,W,_=a.shape
    edge=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); med=np.median(edge,axis=0)
    diff=np.abs(a-med).sum(axis=2)
    bg=diff<48
    # flood fill from borders
    lbl,n=ndimage.label(bg)
    border=set(lbl[0]).union(lbl[-1]).union(lbl[:,0]).union(lbl[:,-1]); border.discard(0)
    bgm=np.isin(lbl,list(border))
    fg=~bgm
    # largest component
    l2,n2=ndimage.label(fg)
    if n2>1:
        sizes=ndimage.sum(fg,l2,range(1,n2+1)); fg=l2==(np.argmax(sizes)+1)
    # fill holes with ring test
    filled=ndimage.binary_fill_holes(fg)
    holes,nh=ndimage.label(filled&~fg)
    for h in range(1,nh+1):
        hm=holes==h; sz=hm.sum()
        if sz<8: fg|=hm; continue
        ring=ndimage.binary_dilation(hm,iterations=3)&fg
        if ring.sum()==0: continue
        rc=np.median(a[ring],axis=0)
        if rc[1]>rc[0]+8 and rc[1]>rc[2]+8: fg|=hm          # green ring -> body highlight, refill
        elif abs(rc[0]-rc[1])<14 and abs(rc[1]-rc[2])<14 and 140<rc.mean()<250: pass  # grey ring -> genuine gap
        else: fg|=hm
    # neutral shadow strip bottom band
    band=np.zeros_like(fg); band[int(H*(1-shadow_band)):]=True
    neutral=(np.abs(a[:,:,0]-a[:,:,1])<16)&(np.abs(a[:,:,1]-a[:,:,2])<16)&(a.mean(axis=2)>120)&(a.mean(axis=2)<246)
    fg&=~(band&neutral)
    l3,n3=ndimage.label(fg)
    if n3>1:
        sizes=ndimage.sum(fg,l3,range(1,n3+1)); fg=l3==(np.argmax(sizes)+1)
    m=Image.fromarray((fg*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    out=im.convert('RGBA'); out.putalpha(m)
    bb=out.getbbox(); out=out.crop(bb); out.save(dst)
    print(dst,out.size)
for s,d,sb in [('h_sheet/H_WALK_B_RAW.png','h_sheet/H_WALK_B.png',0.10),
               ('h_sheet/H_FLEX_B_RAW.png','h_sheet/H_FLEX_B.png',0.10),
               ('h_sheet/H_PUNCH_A_RAW.png','h_sheet/H_PUNCH_A.png',0.10),
               ('h_sheet/H_KNEES_B_RAW.png','h_sheet/H_KNEES_B.png',0.12),
               ('g_sheet/G_ROAR_B_RAW.png','g_sheet/G_ROAR_B.png',0.10),
               ('g_sheet/G_SMUG_B_RAW.png','g_sheet/G_SMUG_B.png',0.10)]:
    cut(s,d,sb)
