import sounddevice as sd
import numpy as np
import wave
import tempfile
from faster_whisper import WhisperModel
import keyboard  # ไลบรารีสำหรับตรวจจับการกดปุ่ม

# โหลดโมเดล Whisper
model = WhisperModel("small", device="cuda")

# กำหนดค่า
SAMPLE_RATE = 16000  # ความถี่เสียงที่โมเดลรองรับ

def record_audio_until_stopped(sample_rate):
    """บันทึกเสียงจากไมโครโฟนจนกว่าจะกดหยุด"""
    print("กด 'r' เพื่อเริ่มบันทึกเสียง และกด 's' เพื่อหยุด")
    
    # รอจนกว่าผู้ใช้กด 'r'
    keyboard.wait('r')
    print("เริ่มบันทึกเสียง...")
    
    # เริ่มบันทึก
    recording = []
    stream = sd.InputStream(samplerate=sample_rate, channels=1, dtype=np.float32, callback=lambda indata, frames, time, status: recording.append(indata.copy()))
    stream.start()
    
    # รอจนกว่าผู้ใช้กด 's'
    keyboard.wait('s')
    print("หยุดบันทึกเสียง")
    
    # หยุดการบันทึก
    stream.stop()
    stream.close()
    
    # รวมข้อมูลเสียงทั้งหมดเป็น 1D array
    audio_data = np.concatenate(recording, axis=0).flatten()
    return audio_data

def save_audio_to_wav(audio_data, sample_rate):
    """บันทึกข้อมูลเสียงเป็นไฟล์ WAV ชั่วคราว"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)  # โมโน
        wav_file.setsampwidth(2)  # 16-bit PCM
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    return temp_file.name

# บันทึกเสียงจนกว่าผู้ใช้จะหยุด
audio_data = record_audio_until_stopped(SAMPLE_RATE)

# บันทึกเสียงเป็นไฟล์ WAV
audio_path = save_audio_to_wav(audio_data, SAMPLE_RATE)

# ใช้ Whisper ประมวลผลเสียง
segments, info = model.transcribe(audio_path, language="th")

# แสดงผลลัพธ์
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
