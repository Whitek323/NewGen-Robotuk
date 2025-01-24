import tkinter as tk
from PIL import Image, ImageTk
import json,re
import requests
from io import BytesIO
class QRCodeHandler:
    def __init__(self):
        pass
      
    # def find_keyword_in_prompt(self, prompt):
        
    #     keywords = ["วิธีไป", "QR Code", "คิวอาร์โค้ด"]

    #     # ใช้ any() เพื่อตรวจสอบว่ามีคำใดใน prompt หรือไม่
    #     if any(keyword in prompt for keyword in keywords):
    #         return True
        
    def find_qr_in_response(self,text):
        match = re.search(r'(?::|\s|\b)([\w-]+\.png)', text)
        if match:
            return match.group(1)
        return ""





