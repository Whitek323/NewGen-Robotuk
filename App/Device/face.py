import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import sounddevice as sd
import soundfile as sf
import io
import requests
from config import MODES

class Face:
    def __init__(self, root):
        self.root = root
        self.stop_animation = False
        self.qr_displayed = False
        self.current_animation_state = "idle"
        
        # Create and pack the label
        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True, fill="both")
        
        # Load images and start animation
        self.images = self.load_images()
        self.start_animation()

    def load_images(self):
        """Preload all animation frames and resize to full screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        images = {}
        for mode, paths in MODES.items():
            mode_frames = []
            for path in paths:
                img = Image.open(path)
                ratio = min(screen_width / img.width, screen_height / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)

                resized_img = img.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(resized_img)
                mode_frames.append(img_tk)
            images[mode] = mode_frames
        return images

    def animation_loop(self):
        frame_index = 0
        while not self.stop_animation:
            if self.qr_displayed:
                time.sleep(0.5)
                continue
            current_images = self.images[self.current_animation_state]
            self.image_label.config(image=current_images[frame_index])
            frame_index = (frame_index + 1) % len(current_images)
            time.sleep(0.8)

    def start_animation(self):
        self.animation_thread = threading.Thread(target=self.animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()

    def set_animation_state(self, state):
        self.current_animation_state = state

    def display_qr(self, qr_path):
        self.qr_displayed = True
        qr_image = Image.open(qr_path)
        qr_photo = ImageTk.PhotoImage(qr_image)
        self.image_label.config(image=qr_photo)
        self.image_label.image = qr_photo

    def hide_qr(self):
        self.qr_displayed = False

    def play_audio(self, audio_url):
        try:
            print("กำลังดาวน์โหลดเสียงจากเซิร์ฟเวอร์...")
            response = requests.get(audio_url)
            response.raise_for_status()

            audio_data, sampling_rate = sf.read(io.BytesIO(response.content))
            print("กำลังเล่นเสียง...")
            sd.play(audio_data, samplerate=sampling_rate)
            sd.wait()
            print("เสียงเล่นเสร็จสิ้น")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดขณะเล่นเสียง: {e}")

    def cleanup(self):
        self.stop_animation = True