import os
import re
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch
from transformers import VitsTokenizer, VitsModel, set_seed


class TTS:
    def __init__(self, model_name, text):
        self.model_name = model_name
        self.text = self.clean_text(text)

        tokenizer = VitsTokenizer.from_pretrained(self.model_name)
        model = VitsModel.from_pretrained(self.model_name)

        inputs = tokenizer(text=self.text, return_tensors="pt")

        # Set seed for reproducibility
        set_seed(555)

        # Process with model
        with torch.no_grad():
            outputs = model(**inputs)

        # Extract waveform
        self.waveform = outputs.waveform[0].cpu().numpy()
        self.sampling_rate = model.config.sampling_rate

    def save_audio(self, file_path):
        from scipy.io.wavfile import write
        write(file_path, self.sampling_rate, self.waveform)


    def clean_text(self,text):
        # ตรวจสอบว่ามี 'q' ถึง '.png' หรือไม่
        if re.search(r'q.*?\.png', text, flags=re.IGNORECASE):
            # ใช้ regex เพื่อลบข้อความตั้งแต่ตัว 'q' ถึง '.png'
            cleaned_text = re.sub(r'q.*?\.png', '', text, flags=re.IGNORECASE)
            return cleaned_text
        # ถ้าไม่มี 'q' ถึง '.png' ให้ return ข้อความเดิม
        return text
