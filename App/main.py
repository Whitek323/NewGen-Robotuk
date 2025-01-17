import tkinter as tk
from PIL import Image, ImageTk
import threading
import requests
import time
import keyboard
import sounddevice as sd
import numpy as np
import soundfile as sf
import io
from recorder import Recorder
from config import *



current_animation_state = "idle"
stop_animation = False
qr_displayed = False
is_recording = False  # Track recording state

# Initialize the recorder
recorder = Recorder(sample_rate=16000, channels=1)

def load_images(root):
    """Preload all animation frames and resize to full screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    images = {}
    for mode, paths in MODES.items():
        mode_frames = []
        for path in paths:
            img = Image.open(path)
            # Calculate scaling ratio
            ratio = min(screen_width / img.width, screen_height / img.height)
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)

            # Resize the image to fit the screen
            resized_img = img.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized_img)
            mode_frames.append(img_tk)
        images[mode] = mode_frames
    return images


def display_qr(qr_path, label):
    qr_image = Image.open(qr_path)
    qr_photo = ImageTk.PhotoImage(qr_image)
    label.config(image=qr_photo)
    label.image = qr_photo

def animation_loop(images, label):
    global stop_animation, qr_displayed
    frame_index = 0
    while not stop_animation:
        if qr_displayed:
            time.sleep(0.5)
            continue
        current_images = images[current_animation_state]
        label.config(image=current_images[frame_index])
        frame_index = (frame_index + 1) % len(current_images)
        time.sleep(0.8)

def play_audio(audio_url):
    try:
        print("กำลังดาวน์โหลดเสียงจากเซิร์ฟเวอร์...")
        response = requests.get(API_PATH + audio_url)
        response.raise_for_status()  # Check for HTTP errors

        audio_data, sampling_rate = sf.read(io.BytesIO(response.content))
        print("กำลังเล่นเสียง...")
        sd.play(audio_data, samplerate=sampling_rate)
        sd.wait()
        print("เสียงเล่นเสร็จสิ้น")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดขณะเล่นเสียง: {e}")

def handle_chat(prompt, label):
    global current_animation_state, qr_displayed
    current_animation_state = "work"
    data = {"prompt": prompt}
    response = requests.post(API_URL, json=data).json()

    current_animation_state = "speak"
    qr_path = response.get("qr_path")
    if qr_path:
        qr_displayed = True
        display_qr(API_PATH+"static/QRIMG/"+qr_path, label)
    else:
        qr_displayed = False

    print(f"AI Response: {response['response']}")

    # Play TTS audio
    audio_path = response.get("audio_path")
    if audio_path:
        play_audio(audio_path)

    current_animation_state = "idle"


def start_chat_thread(prompt, label):
    """Spawn a new thread to handle the chat."""
    threading.Thread(target=handle_chat, args=(prompt, label), daemon=True).start()

def toggle_recording(label):
    """
    Press 'r' to:
      - Start if not recording
      - Stop if recording, transcribe, pass transcription to handle_chat
    """
    global is_recording
    if not is_recording:
        # Start recording
        is_recording = True
        recorder.start()
    else:
        # Stop recording
        is_recording = False
        wav_file = recorder.stop()
        if wav_file:
            transcription = recorder.transcribe_audio(wav_file)
            # Now pass the transcription to handle_chat
            start_chat_thread(transcription, label)

def on_keypress(event, label):
    """Keyboard handler for all keys."""
    if event.name == 's':
        # 's' => typed input
        prompt = input("What do you want to ask? -> ")
        start_chat_thread(prompt, label)
    elif event.name == 'r':
        # 'r' => record/stop
        toggle_recording(label)

def main():
    global stop_animation
    root = tk.Tk()

    root.title("AI Assistant Frontend")

    # FULL-SCREEN MODE
    # root.attributes('-fullscreen', True)
    # root.overrideredirect(True)         # Remove window manager decorations
    # root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")


    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    # Load images after root is created (so winfo_screenwidth/height have values)
    images = load_images(root)

    image_label = tk.Label(root)
    image_label.pack(expand=True, fill="both")

    animation_thread = threading.Thread(target=animation_loop, args=(images, image_label))
    animation_thread.daemon = True
    animation_thread.start()

    # If you're using the 'keyboard' library (requires root or another approach):
    def key_event_listener(event):
        on_keypress(event, image_label)

    keyboard.on_press(key_event_listener)

    root.mainloop()
    stop_animation = True

if __name__ == "__main__":
    main()
