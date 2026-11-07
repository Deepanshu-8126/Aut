MANIFEST={'nanda-kot-and-changuch-img2-cropped-gout-1.jpg': 'dc0218ad6a8b52eb369a239549798514a8a862a1a14b76521d75d48c35063626', 'nanda-kot-and-changuch-img2-cropped-gout-2.jpg': 'ac43321b404950715ccc9e351fca98dca891e04897f4873ddf633dacfca7b6f6', 'nanda-kot-and-changuch-img2-cropped-gout-3.jpg': '69ae516f14eb3e79db93f1be6d67e6fdd51defc563c7cd711d6375456919cbe4', 'site-commons-wikimedia-org-nanda-devi-fi-1.jpg': 'c850c1c84c7a202129ba92b15363aa29eb138500278fa0eb053c4176db9fb705', 'site-commons-wikimedia-org-nanda-devi-fi-2.jpg': '322b8d9b235f3595aa767f3bf668e17e59b17b0775a3306679c431d5b26deca2', 'site-commons-wikimedia-org-nanda-devi-fi-3.jpg': '63683b0d41e3b631bb50ba68c14248a5d2d5ccff0b863ed36dafcd79875accdd', 'site-commons-wikimedia-org-nanda-devi-fi-4.jpg': '09760ff7747e0cd73e58cb2ff2184024a76e479d185c91056dd1355f3d4c8e23', 'site-commons-wikimedia-org-nanda-devi-fi-5.jpg': '71f4a0c53ba12d7554270d3426918ed5f2dcbe9bcc404c38ea81a46bafa76076', 'site-commons-wikimedia-org-nanda-devi-pe-1.jpg': '63683b0d41e3b631bb50ba68c14248a5d2d5ccff0b863ed36dafcd79875accdd', 'site-commons-wikimedia-org-nanda-devi-pe-2.jpg': 'cae28da605eb6ea68c52094fbeb1e3665ac129dd836b3940a89085e1109c57ed', 'site-commons-wikimedia-org-nanda-devi-pe-3.jpg': '3f72fbdca63d2c7d20c3186ebd2c1f6e9164952641eaef12caa229309587ea0c', 'site-commons-wikimedia-org-nanda-devi-pe-4.jpg': '322b8d9b235f3595aa767f3bf668e17e59b17b0775a3306679c431d5b26deca2', 'site-commons-wikimedia-org-nanda-devi-pe-5.jpg': '5529df448cba7e7c564df94e22499d728eb73ba9b47adae75cc6d7d761e3470f'}
import pathlib,hashlib,json
D=MANIFEST
root=pathlib.Path('/kaggle/input')
errors=[]
for n,want in D.items():
 candidates=list(root.rglob(n))
 if len(candidates)!=1: errors.append([n,'missing or ambiguous']);continue
 if hashlib.sha256(candidates[0].read_bytes()).hexdigest()!=want: errors.append([n,'mismatch'])
r={'files':len(D),'errors':errors,'pass':not errors};pathlib.Path('/kaggle/working/SEARCH_HOLD_VERIFY.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
if errors:raise RuntimeError('verification failed')
