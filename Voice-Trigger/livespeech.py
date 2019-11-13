# from pocketsphinx import LiveSpeech
# from pocketsphinx import Pocketsphinx
#
# #speech = LiveSpeech()
# ps = Pocketsphinx(verbose=False)
# ps.decode()
#
# print(ps.hypothesis())

from pocketsphinx import LiveSpeech
#speech = LiveSpeech(lm=False, keyphrase='forward', kws_threshold=1e+20)
speech = LiveSpeech(buffer_size=256)
for phrase in speech:
    print(phrase.segments(detailed=True))
    #print(phrase.segments())
    if "next" in phrase.segments() and "page" in phrase.segments():
        print("NEXT")
    elif ("previous" or "last") and "page" in phrase.segments():
        print("PREV")
