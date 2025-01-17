from faster_whisper import WhisperModel
from pythainlp.spell import correct
import re
import time

# เริ่มจับเวลา
start_time = time.time()
# ฟังก์ชันแก้ข้อความ
def fix_text(text):
    corrections = {
        "อัมเภอ": "อำเภอ",
        "อูท้อง": "อู่ทอง",
        "จังวัติ": "จังหวัด",
        "สุขันบุริ": "สุพรรณบุรี"
    }
    # รวม regex เพื่อความเร็ว
    pattern = re.compile('|'.join(re.escape(k) for k in corrections.keys()))
    return correct(pattern.sub(lambda m: corrections[m.group(0)], text))

# โหลดโมเดลครั้งเดียว
model = WhisperModel("base", device="cuda", compute_type="float16")

# ประมวลผลไฟล์เสียง
audio_path = "../upload/w.wav"
segments, info = model.transcribe(audio_path)

# รวมข้อความและแก้ไข
raw_text = " ".join([segment.text for segment in segments])
corrected_text = fix_text(raw_text)
print(corrected_text)
# สิ้นสุดจับเวลา
end_time = time.time()

# คำนวณเวลาที่ใช้
elapsed_time = end_time - start_time
print(f"เวลาในการ compile program: {elapsed_time:.2f} วินาที")