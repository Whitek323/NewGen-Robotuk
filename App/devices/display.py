from io import BytesIO
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

import requests
from config import *

class Display:
    def __init__(self, root):
        self.root = root
        self.current_state = "idle"
        self.stop_animation = False
        self.qr_displayed = False
        
        # Create and pack the label
        self.label = tk.Label(root)
        self.label.pack(expand=True, fill="both")
        
        # Load images
        self.images = self.load_images()
        
    def load_images(self):
        """Preload all animation frames and resize to full screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        images = {}
        for mode, paths in MODES.items():
            mode_frames = []
            if not paths:  # ตรวจสอบว่ามี paths หรือไม่
                print(f"Warning: No image paths found for mode {mode}")
                continue
                
            for path in paths:
                try:
                    img = Image.open(path)
                    ratio = min(screen_width / img.width, screen_height / img.height)
                    new_width = int(img.width * ratio)
                    new_height = int(img.height * ratio)
                    
                    resized_img = img.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(resized_img)
                    mode_frames.append(img_tk)
                except Exception as e:
                    print(f"Error loading image {path}: {e}")
                    
            if mode_frames:  # เพิ่มเฟรมเข้า images เมื่อมีการโหลดสำเร็จ
                images[mode] = mode_frames
                
        if not images:
            raise ValueError("No images were loaded successfully")
            
        return images
            
    def animation_loop(self):
        frame_index = 0
        while not self.stop_animation:
            if self.qr_displayed:
                time.sleep(0.5)
                continue
                
            if self.current_state not in self.images:  # ตรวจสอบว่ามี state นี้หรือไม่
                print(f"Warning: No images for state {self.current_state}")
                time.sleep(0.5)
                continue
                
            current_images = self.images[self.current_state]
            if not current_images:  # ตรวจสอบว่ามีภาพหรือไม่
                print(f"Warning: Empty image list for state {self.current_state}")
                time.sleep(0.5)
                continue
                
            frame_index = frame_index % len(current_images)  # ป้องกัน index out of range
            self.label.config(image=current_images[frame_index])
            frame_index += 1
            time.sleep(0.8)
            
    def set_state(self, state):
        if state not in self.images:  # ตรวจสอบว่ามี state ที่ต้องการหรือไม่
            print(f"Warning: Attempting to set invalid state: {state}")
            return
        self.current_state = state
        
    def handle_qr(self, qr_path):
        self.display_qr(qr_path)
        
    def display_qr(self, qr_path):
        if qr_path:
            try:
                # ถ้าเป็น URL
                if qr_path.startswith('http'):
                    response = requests.get(qr_path)
                    qr_image = Image.open(BytesIO(response.content))
                # ถ้าเป็น local path
                else:
                    qr_image = Image.open(qr_path)
                    
                qr_photo = ImageTk.PhotoImage(qr_image)
                self.label.config(image=qr_photo)
                self.label.image = qr_photo
                self.qr_displayed = True
                
            except Exception as e:
                print(f"Error displaying QR code: {e}")
                self.qr_displayed = False
        else:
            self.qr_displayed = False

    def start_animation(self):
        self.animation_thread = threading.Thread(target=self.animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def stop_animation(self):
        self.stop_animation = True