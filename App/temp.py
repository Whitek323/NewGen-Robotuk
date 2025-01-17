import tkinter as tk
from PIL import Image, ImageTk
import threading
import requests
import time
import keyboard  # For keyboard event listening
import requests
import sounddevice as sd
import numpy as np
import soundfile as sf
import io
from recorder import Recorder

# Backend API URL
API_URL = "http://127.0.0.1:5000/chat"
API_PATH = "http://127.0.0.1:5000/"


# Animation states
MODES = {
    "speak": ["./QR_Codes/F_IMG/1.png", "./QR_Codes/F_IMG/2.png", "./QR_Codes/F_IMG/3.png"],
    "idle": ["./QR_Codes/F_IMG/4.png", "./QR_Codes/F_IMG/5.png", "./QR_Codes/F_IMG/6.png"],
    "work": ["./QR_Codes/F_IMG/7.png", "./QR_Codes/F_IMG/8.png", "./QR_Codes/F_IMG/9.png"],
}

current_animation_state = "idle"
stop_animation = False
qr_displayed = False  # Track if a QR code is currently displayed


def load_images():
    """Preload all animation frames."""
    images = {}
    for mode, paths in MODES.items():
        images[mode] = [ImageTk.PhotoImage(Image.open(path)) for path in paths]
    return images


def display_qr(qr_path, label):
    """Display QR code in the label."""
    qr_image = Image.open(qr_path)
    qr_photo = ImageTk.PhotoImage(qr_image)
    label.config(image=qr_photo)
    label.image = qr_photo  # Save a reference to prevent garbage collection


def animation_loop(images, label):
    """Animation loop that updates the frame based on the current state."""
    global stop_animation, qr_displayed
    frame_index = 0

    while not stop_animation:
        if qr_displayed:  # Skip animation if a QR code is displayed
            time.sleep(0.5)
            continue

        current_images = images[current_animation_state]
        label.config(image=current_images[frame_index])
        frame_index = (frame_index + 1) % len(current_images)
        time.sleep(0.8)


def handle_chat(prompt, label):
    global current_animation_state, qr_displayed

    current_animation_state = "work"
    data = {"prompt": prompt}
    response = requests.post(API_URL, json=data).json()

    current_animation_state = "speak"
    qr_path = response.get("qr_path")
    if qr_path:  # Check if a QR code path is found
        qr_displayed = True
        display_qr(qr_path, label)
    else:
        qr_displayed = False

    print(f"AI Response: {response['response']}")

    # Play audio
    audio_path = response.get("audio_path")
    if audio_path:
        play_audio(audio_path)

    current_animation_state = "idle"

def play_audio(audio_url):
    try:
        print("กำลังดาวน์โหลดเสียงจากเซิร์ฟเวอร์...")
        # Fetch the audio data as a byte stream
        response = requests.get(API_PATH+audio_url)
        response.raise_for_status()  # Check for HTTP errors

        # Decode the audio from the byte stream
        audio_data, sampling_rate = sf.read(io.BytesIO(response.content))

        # Play the audio
        print("กำลังเล่นเสียง...")
        sd.play(audio_data, samplerate=sampling_rate)
        sd.wait()  # Wait for playback to finish
        print("เสียงเล่นเสร็จสิ้น")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดขณะเล่นเสียง: {e}")


def start_chat_thread(label):
    """Start a new thread for handling chat without blocking animation."""
    prompt = input("What do you want to ask? -> ")
    threading.Thread(target=handle_chat, args=(prompt, label), daemon=True).start()


def main():
    global stop_animation
    root = tk.Tk()
    root.title("AI Assistant Frontend")

    # Preload images
    images = load_images()

    # Setup Tkinter label
    image_label = tk.Label(root)
    image_label.pack(expand=True)  # Center image in the window

    # Start animation thread
    animation_thread = threading.Thread(target=animation_loop, args=(images, image_label))
    animation_thread.daemon = True
    animation_thread.start()

    # Keypress handler for chat
    def on_keypress(event):
        if event.name == 's':
            start_chat_thread(image_label)

    keyboard.on_press(on_keypress)

    root.mainloop()
    stop_animation = True


if __name__ == "__main__":
    main()