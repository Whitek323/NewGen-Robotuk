from pythaitts import TTS

tts = TTS(pretrained="lunarlist_onnx")
file = tts.tts("ภาษาไทย ง่าย มาก มาก", filename="cat.wav") # It will get wav file path.
wave = tts.tts("ภาษาไทย ง่าย มาก มาก",return_type="waveform") # It will get waveform.