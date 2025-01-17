# recorder.py

import sounddevice as sd
import numpy as np
import wave
import requests
import io

class Recorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.stream = None

    def _record_audio_callback(self, indata, frames, time, status):
        """Callback to append audio data."""
        if self.recording:
            self.audio_data.append(indata.copy())

    def start(self):
        """Start recording audio."""
        if self.stream is not None:
            self.stream.stop()
        self.recording = True
        self.audio_data = []  # Clear previous data
        print("[Recorder] Recording started...")

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._record_audio_callback
        )
        self.stream.start()

    def stop(self):
        """Stop recording audio and return the WAV filename."""
        if not self.recording:
            return None
        self.recording = False
        print("[Recorder] Recording stopped...")

        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        # Save the recorded data as a WAV file
        wav_file = "output.wav"
        data = np.concatenate(self.audio_data, axis=0)
        with wave.open(wav_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(self.sample_rate)
            wf.writeframes((data * 32767).astype(np.int16).tobytes())
        print(f"[Recorder] WAV saved: {wav_file}")
        return wav_file

    def transcribe_audio(self, wav_file):
        """Send the recorded audio to the backend for transcription."""
        url = "http://127.0.0.1:5000/transcribe"  # Backend endpoint
        print("[Recorder] Uploading audio to backend for transcription...")
        with open(wav_file, 'rb') as f:
            response = requests.post(url, files={"file": f})
        if response.status_code == 200:
            json_data = response.json()
            transcription = json_data.get("transcription", "")
            print(f"[Recorder] Transcription: {transcription}")
            return transcription
        else:
            print(f"[Recorder] Error: {response.text}")
            return ""
