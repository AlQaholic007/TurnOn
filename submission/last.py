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
speech = LiveSpeech(lm=False, keyphrase='flip back', kws_threshold=1e-22)
for phrase in speech:
    print(phrase.segments(detailed=True))
    subprocess.Popen("python mechanical_trigger.py prev", shell=True)
