from faster_whisper import WhisperModel
import time

# เริ่มจับเวลา
start_time = time.time()

model = WhisperModel("small", device="cuda") 

audio_path = "../upload/w.wav"

segments, info = model.transcribe(audio_path)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")


# สิ้นสุดจับเวลา
end_time = time.time()

# คำนวณเวลาที่ใช้
elapsed_time = end_time - start_time
print(f"เวลาในการ compile program: {elapsed_time:.2f} วินาที")