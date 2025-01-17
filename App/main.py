import tkinter as tk
import threading
import keyboard
from Device import Face
from PIL import Image, ImageTk
from config import *


def load_images(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
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


def on_keypress(event, face_instance):
    if event.name == 's':
        prompt = input("What do you want to ask? -> ")
        # Start chat logic here
        print(f"Prompt entered: {prompt}")
    elif event.name == 'r':
        # Toggle recording logic here
        print("Toggle recording")


def key_event_listener(event, face_instance):
    on_keypress(event, face_instance)


def main():
    root = tk.Tk()
    root.title("AI Assistant Frontend")

    face_instance = Face(
        root=root,
        load_images_callback=load_images,
        animation_states={"idle": "idle", "work": "work", "speak": "speak"},
        on_keypress_callback=on_keypress
    )

    keyboard.on_press(lambda event: key_event_listener(event, face_instance))

    root.mainloop()
    face_instance.stop()


if __name__ == "__main__":
    main()
