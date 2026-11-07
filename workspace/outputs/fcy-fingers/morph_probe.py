import cv2,numpy as np
from PIL import Image,ImageDraw
p='/home/user/outputs/fcy-fingers/assets/'
a=cv2.resize(cv2.imread(p+'sink_start.png'),(540,960));b=cv2.resize(cv2.imread(p+'sink.png'),(540,960));g=lambda im:cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM);flow=dis.calc(g(a),g(b),None);back=dis.calc(g(b),g(a),None)
y,x=np.mgrid[:960,:540].astype('float32');sheet=Image.new('RGB',(1350,960));d=ImageDraw.Draw(sheet)
for i,u in enumerate([0,.25,.5,.75,1.]):
 aa=cv2.remap(a,x-u*flow[:,:,0],y-u*flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT);bb=cv2.remap(b,x-(1-u)*back[:,:,0],y-(1-u)*back[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT);c=cv2.addWeighted(aa,1-u,bb,u,0);z=Image.fromarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB)).resize((270,480));sheet.paste(z,(i*270,0));d.text((i*270,483),str(u),fill='white')
np.savez_compressed('/home/user/outputs/fcy-fingers/flow.npz',forward=flow,backward=back);sheet.save('/home/user/outputs/fcy-fingers/morph_probe.jpg')
