from pathlib import Path
p=Path('/home/user/outputs/fcy-chimera');s=(p/'test_adam.html').read_text()
old="cshot(IM.HK,zz,hpx,0);ctx.filter='none';\n ctx.save();ctx.globalCompositeOperation='lighter';"
new="""cshot(IM.HK,zz,hpx,0);ctx.filter='none';
 // Story-led hook beat: reveal the person, not just a moving graphic.
 const person=ez((tt-0.58)/0.14)*(1-ez((tt-1.40)/0.18));
 if(person>0){ctx.save();ctx.globalAlpha=person*0.90;
  cshot(IM.BD,1.14+0.025*ez((tt-0.58)/0.95),0,-25);ctx.restore();}
 ctx.save();ctx.globalCompositeOperation='lighter';"""
assert old in s;s=s.replace(old,new,1)
(p/'test_v4_working.html').write_text(s)
r=(p/'adam/render_adam.py').read_text().replace('/var/tmp/fcyc_adam','/var/tmp/fcyc_v4base').replace('chimera/test_adam.html','chimera/test_v4_working.html')
(p/'adam/render_v4.py').write_text(r)
