from recorder import Recorder
from service import AIService
class Microphone:
    def __init__(self):
        self.recorder = Recorder(sample_rate=16000, channels=1)
        self.service = AIService()
        self.is_recording = False
        
    def toggle_recording(self, callback,face):
        if not self.is_recording:
            self.start_recording()
            face.set_text("[Recorder] เริ่มการบันทึกเสียง...")
        else:
            self.stop_recording(callback)
            face.set_text("[Recorder] หยุดการบันทึกเสียง...")

            
    def start_recording(self):
        self.is_recording = True
        self.recorder.start()
        
    def stop_recording(self, callback):
        self.is_recording = False
        wav_file = self.recorder.stop()
        if wav_file:
            transcription = self.service.transcribe_audio(wav_file)
            callback(transcription)