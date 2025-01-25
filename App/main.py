import tkinter as tk
import keyboard
from devices import *
from ui import *
from service import AIService

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Assistant Frontend")
        # Initialize components
        self.face = Display(self.root)
        self.speaker = Speaker()
        self.microphone = Microphone()
        self.service = AIService()
        self.face.set_text("")
        # Bind escape key
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        
        # Setup keyboard listener
        keyboard.on_press(self.key_event_listener)

    def key_event_listener(self, event):
        if event.name == 's':
            prompt = input("What do you want to ask? -> ")
            self.handle_chat(prompt)
        elif event.name == 'r':
            self.microphone.toggle_recording(self.handle_chat)

    def handle_chat(self, prompt):
        self.face.set_state("work")
        # self.face.set_text("กำลังประมวลผล")
        # Get response from API
        response = self.service.send_prompt(prompt)
        
        # Handle QR code if present
        qr_path = self.service.get_qr_path(response.get("qr_path"))
        self.face.handle_qr(qr_path)
        
        print(f"AI Response: {response['response']}")
        
        # Play audio if present
        audio_path = response.get("audio_path")
        if audio_path:
            self.face.set_state("speak")
            self.speaker.play_audio(audio_path, self.service)
        
        self.face.set_state("idle")

    def run(self):
        self.face.start_animation()
        self.root.mainloop()
        self.face.stop_animation()

if __name__ == "__main__":
    app = MainApplication()
    app.run()