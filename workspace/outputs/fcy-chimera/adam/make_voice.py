from kokoro_onnx import Kokoro
import soundfile as sf
k=Kokoro('/var/tmp/kok/kokoro-v1.0.onnx','/var/tmp/kok/voices-v1.0.bin')
text="Her blood doesn't match her body. After a miscarriage, doctors in Brazil tested a woman's blood and found male X Y chromosomes. But her skin and her mouth had female X X chromosomes. She wasn't sick. The test wasn't wrong. Before birth, her twin brother's blood flowed into her veins, and his cells never left. Today, her blood cells carry her brother's DNA. One body, two people's DNA."
a,sr=k.create(text,voice='am_adam',speed=1.12,lang='en-us')
sf.write('/home/user/outputs/fcy-chimera/adam/voice_raw.wav',a,sr)
print('rate',sr,'duration',len(a)/sr)
