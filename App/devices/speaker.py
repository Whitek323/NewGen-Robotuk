import sounddevice as sd
import soundfile as sf
import io

class Speaker:
    def __init__(self):
        pass
        
    def play_audio(self, audio_url, service): 
        try:
            print("กำลังดาวน์โหลดเสียงจากเซิร์ฟเวอร์...")
            response = service.get_audio_content(audio_url)
            if not response:
                return

            audio_data, sampling_rate = sf.read(io.BytesIO(response.content))
            print("กำลังเล่นเสียง...")
            sd.play(audio_data, samplerate=sampling_rate)
            sd.wait()
            print("เสียงเล่นเสร็จสิ้น")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดขณะเล่นเสียง: {e}")