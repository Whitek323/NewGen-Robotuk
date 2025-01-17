#เฉพาะเสียงเท่านั้น
import torch
import sounddevice as sd
from transformers import VitsModel, AutoTokenizer


# โหลดโมเดลและ tokenizer
model_name = "chuubjak/vits-tts-thai"
model = VitsModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# ข้อความที่ต้องการแปลงเป็นเสียง
text = "สวัสดีครับ ฉันคือไกด์นำเที่ยวอำเภออู่ทอง จังหวัดสุพรรณบุรี ฉันยินดีที่จะแนะนำสถานที่ท่องเที่ยวและข้อมูลเกี่ยวกับอำเภอของฉันต่อไปนี้: อุทยานแห่งชาติอู่ทอง คลองตัน ถ้ำป่าช้าง เกาะลึก เป็นต้น"
inputs = tokenizer(text, return_tensors="pt")


# สร้างเสียงพูด
with torch.no_grad():
   output = model(**inputs).waveform


# แปลงข้อมูลเสียงให้อยู่ในช่วงที่ถูกต้อง
output = output.squeeze().cpu().numpy()
output = output * 32767  # ปรับสเกลให้เป็นช่วงของ int16
output = output.astype("int16")  # แปลงเป็น int16


# เล่นเสียง
sampling_rate = model.config.sampling_rate
sd.play(output, samplerate=sampling_rate)
sd.wait()  # รอจนกว่าเสียงจะเล่นเสร็จ