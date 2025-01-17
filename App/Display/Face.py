# face.py
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class Face:
    def __init__(self, root, images, on_keypress):
        self.root = root
        self.images = images
        self.current_animation_state = "idle"
        self.stop_animation = False
        self.qr_displayed = False
        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True, fill="both")

        # Bind keypress events
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        threading.Thread(target=self.animation_loop, daemon=True).start()

        # Keyboard event listener
        self.root.bind_all("<Key>", on_keypress)

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

    def display_qr(self, qr_path):
        qr_image = Image.open(qr_path)
        qr_photo = ImageTk.PhotoImage(qr_image)
        self.image_label.config(image=qr_photo)
        self.image_label.image = qr_photo

    def set_animation_state(self, state):
        self.current_animation_state = state

    def stop(self):
        self.stop_animation = True