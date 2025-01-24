import tkinter as tk
from Device import Face
import keyboard
import threading
from recorder import Recorder
import requests
from config import *

class Main:
    def __init__(self):
        self.current_animation_state = "idle"
        self.is_recording = False
        self.recorder = Recorder(sample_rate=16000, channels=1)
        
        # Initialize root and face
        self.root = tk.Tk()
        self.root.title("AI Assistant Frontend")
        self.face = Face(self.root)
        
        # Bind escape key
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        
        # Set up keyboard listener
        keyboard.on_press(self.key_event_listener)

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recorder.start()
        else:
            self.is_recording = False
            wav_file = self.recorder.stop()
            if wav_file:
                transcription = self.recorder.transcribe_audio(wav_file)
                self.start_chat_thread(transcription)

    def handle_chat(self, prompt):
        self.current_animation_state = "work"
        self.face.set_animation_state("work")
        
        data = {"prompt": prompt}
        response = requests.post(API_URL, json=data).json()

        self.current_animation_state = "speak"
        self.face.set_animation_state("speak")
        
        qr_path = response.get("qr_path")
        if qr_path:
            self.face.display_qr(API_PATH + "static/QRIMG/" + qr_path)
        else:
            self.face.hide_qr()

        print(f"AI Response: {response['response']}")

        audio_path = response.get("audio_path")
        if audio_path:
            self.face.play_audio(API_PATH + audio_path)

        self.current_animation_state = "idle"
        self.face.set_animation_state("idle")

    def start_chat_thread(self, prompt):
        threading.Thread(target=self.handle_chat, args=(prompt,), daemon=True).start()

    def key_event_listener(self, event):
        if event.name == 's':
            prompt = input("What do you want to ask? -> ")
            self.start_chat_thread(prompt)
        elif event.name == 'r':
            self.toggle_recording()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()