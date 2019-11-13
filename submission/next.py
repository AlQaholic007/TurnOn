# from pocketsphinx import LiveSpeech
# from pocketsphinx import Pocketsphinx
#
# #speech = LiveSpeech()
# ps = Pocketsphinx(verbose=False)
# ps.decode()
#
# print(ps.hypothesis())

import os
from pocketsphinx import LiveSpeech, get_model_path
import subprocess

model_path = get_model_path()
print(model_path)
speech = LiveSpeech(lm=False, keyphrase='next page', kws_threshold=1e-25)
#speech = LiveSpeech(kws = os.path.join(model_path,'keyphrase.list'))
    #buffer_size=2048,
    #hmm=os.path.join(model_path, 'en-us'),
    #lm=os.path.join(model_path, 'en-us.lm.bin'),
    #dic=os.path.join(model_path, 'cmudict-en-us.dict'),
    #keyphrase='hey page turner',
    #kws_threshold = 1e20)
for phrase in speech:
    print(phrase.segments(detailed=True))
    subprocess.Popen("python mechanical_trigger.py next", shell=True)
