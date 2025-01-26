import requests
from config import *

class AIService:
    def __init__(self):
        self.api_path = API_PATH

    def send_prompt(self, prompt):
        """
        Send prompt to API and get response
        Returns: dict containing response, qr_path, and audio_path
        """
        try:
            data = {"prompt": prompt}
            response = requests.post(self.api_path+"chat", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการติดต่อ API: {e}")
            return {
                "response": "ขออภัย เกิดข้อผิดพลาดในการติดต่อกับเซิร์ฟเวอร์",
                "qr_path": None,
                "audio_path": None
            }

    def get_audio_content(self, audio_url):
        """
        Download audio content from server
        Returns: Response object containing audio data
        """
        try:
            response = requests.get(self.api_path + audio_url)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดาวน์โหลดเสียง: {e}")
            return None

    def get_qr_path(self, qr_path):
        """
        Get complete QR image path
        """
        if qr_path:
            return self.api_path + "static/QRIMG/" + qr_path
        return None
    
    def transcribe_audio(self, wav_file):
        """
        Send audio file to backend for transcription
        Returns: Transcribed text or empty string
        """
        try:
            url = self.api_path+"transcribe"
            print("[Recorder] Uploading audio to backend for transcription...")
            
            with open(wav_file, 'rb') as f:
                response = requests.post(url, files={"file": f})
            
            response.raise_for_status()
            json_data = response.json()
            transcription = json_data.get("transcription", "")
            time_use = json_data.get("time_use","")
            print(f"[Recorder] Transcription: {transcription}")
            print(f"stt process: {time_use} s")
            return transcription
        
        except Exception as e:
            print(f"[Recorder] Transcription Error: {e}")
            return ""