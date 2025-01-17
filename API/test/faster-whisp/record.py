import sounddevice as sd
import wave
import numpy as np
import keyboard

# กำหนดค่าความถี่และช่องสัญญาณ
SAMPLE_RATE = 16000  # ความถี่เสียง (Hz)
CHANNELS = 1  # จำนวนช่องสัญญาณ (1 = Mono, 2 = Stereo)
recording = False
audio_data = []


def record_audio_callback(indata, frames, time, status):
    """Callback ฟังก์ชันสำหรับบันทึกเสียง"""
    if recording:
        audio_data.append(indata.copy())


def save_audio_to_wav(filename, data, sample_rate):
    """บันทึกข้อมูลเสียงเป็นไฟล์ WAV"""
    data = np.concatenate(data, axis=0)  # รวมข้อมูลเสียงทั้งหมด
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(CHANNELS)  # Mono
        wav_file.setsampwidth(2)  # 16-bit PCM
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((data * 32767).astype(np.int16).tobytes())
    print(f"บันทึกไฟล์เสียงเรียบร้อย: {filename}")


def main():
    global recording, audio_data

    print("กด 'r' เพื่อเริ่มบันทึกเสียง, กด 's' เพื่อหยุดบันทึก, และกด 'q' เพื่อออกจากโปรแกรม")

    # สร้าง Stream สำหรับบันทึกเสียง
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=record_audio_callback):
        while True:
            if keyboard.is_pressed('r') and not recording:
                print("เริ่มบันทึกเสียง...")
                recording = True
                audio_data = []  # ล้างข้อมูลเสียงเก่า

            elif keyboard.is_pressed('s') and recording:
                print("หยุดบันทึกเสียง...")
                recording = False

                # บันทึกเสียงลงไฟล์ WAV
                save_audio_to_wav("output.wav", audio_data, SAMPLE_RATE)

            elif keyboard.is_pressed('q'):
                print("ออกจากโปรแกรม...")
                break


if __name__ == "__main__":
    main()
