import sounddevice as sd
import wave
import numpy as np
import keyboard # type: ignore
from faster_whisper import WhisperModel

class Recorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate  # ความถี่เสียง (Hz)
        self.channels = channels  # จำนวนช่องสัญญาณ (1 = Mono, 2 = Stereo)
        self.recording = False  # สถานะการบันทึก
        self.audio_data = []  # เก็บข้อมูลเสียง
        self.stream = None  # ตัวจัดการ Stream

    def record_audio_callback(self, indata, frames, time, status):
        """Callback ฟังก์ชันสำหรับบันทึกเสียง"""
        if self.recording:
            self.audio_data.append(indata.copy())

    def save_audio_to_wav(self, filename):
        """บันทึกข้อมูลเสียงเป็นไฟล์ WAV"""
        data = np.concatenate(self.audio_data, axis=0)  # รวมข้อมูลเสียงทั้งหมด
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)  # Mono
            wav_file.setsampwidth(2)  # 16-bit PCM
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes((data * 32767).astype(np.int16).tobytes())
        print(f"บันทึกไฟล์เสียงเรียบร้อย: {filename}")

    def start_recording(self):
        """เริ่มบันทึกเสียง"""
        print("เริ่มบันทึกเสียง...")
        self.recording = True
        self.audio_data = []  # ล้างข้อมูลเสียงเก่า

    def stop_recording(self):
        """หยุดบันทึกเสียง"""
        print("หยุดบันทึกเสียง...")
        self.recording = False

    def run(self):
        """เริ่มต้นโปรแกรม"""
        print("กด 'r' เพื่อเริ่มบันทึกเสียง, กด 's' เพื่อหยุดบันทึก, และกด 'q' เพื่อออกจากโปรแกรม")

        # สร้าง Stream สำหรับบันทึกเสียง
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self.record_audio_callback):
            self.stream = sd.InputStream
            while True:
                if keyboard.is_pressed('r') and not self.recording:
                    self.start_recording()

                elif keyboard.is_pressed('s') and self.recording:
                    self.stop_recording()
                    self.save_audio_to_wav("output.wav")

                elif keyboard.is_pressed('q'):
                    print("ออกจากโปรแกรม...")
                    break
    def faster_whisper(self):
        """ใช้ฟังก์ชัน whisper ของ OpenAI"""
        
        model = WhisperModel("small", device="cuda") 
        audio_path = "output.wav"
        segments, info = model.transcribe(audio_path)

        for segment in segments:
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

        return segment.text






# if __name__ == "__main__":
#     recorder = Recorder(sample_rate=16000, channels=1)
#     recorder.run()
#     recorder.faster_whisper()
