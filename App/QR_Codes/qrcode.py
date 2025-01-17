import tkinter as tk
from PIL import Image, ImageTk
import json,re

class QRCodeHandler:
    def __init__(self):
        pass

    def show_qr_code(self, image_path):
        """
        Display the QR code image using Tkinter.
        """
        window = tk.Tk()
        window.title("QR Code")
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=photo)
        label.image = photo
        label.pack()
        window.mainloop()
    
    # def find_keyword_in_prompt(self, prompt):
        
    #     keywords = ["วิธีไป", "QR Code", "คิวอาร์โค้ด"]

    #     # ใช้ any() เพื่อตรวจสอบว่ามีคำใดใน prompt หรือไม่
    #     if any(keyword in prompt for keyword in keywords):
    #         return True
        
    def find_qr_in_response(self,text):
        match = re.search(r'(?::|\s|\b)([\w-]+\.png)', text)
        if match:
            return "./QR_Codes/IMG/"+match.group(1)
        return ""





