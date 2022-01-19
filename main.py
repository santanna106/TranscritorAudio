from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
from types import SimpleNamespace
import os
import wave

SetLogLevel(0)

if not os.path.exists("models"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

src = "./audio/test.mp3"
dst = "./audio/test.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

wf = wave.open('./audio/test.wav', "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("models/pt")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

while True:
    data = wf.readframes(1000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        data = rec.Result()
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(x.text)







