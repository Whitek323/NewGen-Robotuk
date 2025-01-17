import tkinter as tk
from PIL import Image, ImageTk
import threading
import time


class Face:
    def __init__(self, root, load_images_callback, animation_states, on_keypress_callback):
        self.root = root
        self.images = load_images_callback(root)
        self.current_animation_state = animation_states["idle"]
        self.stop_animation = False
        self.qr_displayed = False

        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True, fill="both")

        self.animation_thread = threading.Thread(target=self.animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.on_keypress_callback = on_keypress_callback

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

    def stop(self):
        self.stop_animation = True
