EMBEDDING_MODEL = 'nomic-embed-text'

LLM_MODEL = 'llama3.2:3b-instruct-q5_1'
# LLM_MODEL = 'llama3.2:latest'
# LLM_MODEL = 'llama3.1-ut0.3:latest'
TTS_MODEL = 'chuubjak/vits-tts-thai'
# TTS_MODEL = 'facebook/mms-tts-tha'

DATA_TXT = "pg16.txt"

SYSTEM_PROMPT = """คุณเป็นผู้ช่วยอ่านที่เป็นประโยชน์และมัคคุเทศก์แนะนำสถานที่ท่องเที่ยวในประเทศไทยที่ตอบคำถาม
โดยอ้างอิงจากข้อความ ที่ให้ไว้ในบริบท
ตอบอย่างกระชับและตีความข้อมูลจากผู้ใช้ตามที่ตั้งใจไว้ แม้ว่าจะมีข้อผิดพลาดในการสะกดคำ
หากคำสะกดผิดแต่ฟังดูคล้ายกันหรือมีความหมายใกล้เคียงกับคำที่รู้จัก
ให้ถือว่าคำนั้นเป็นคำที่ตั้งใจไว้และตอบกลับตามนั้น
หากผู้ใช้ต้องการเดินทางไปยังสถานที่นั้น หรือถามทิศทาง
ให้ตอบเฉพาะ ชื่อไฟล์คิวอาโค้ด.png โดยไม่ต้องให้ข้อมูลเพิ่มเติม
        บริบท:
    """

# SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions 
#         based on snippets of text provided in context. 
#         Answer concisely and interpret user input as intended, even if there are spelling mistakes. 
#         If a word is misspelled but sounds similar or has a close meaning to a known word, 
#         assume it is the intended word and respond accordingly. 
#         Context:
#     """

import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use time.perf_counter() for high-resolution timing
        start_time = time.perf_counter()
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        # Calculate total execution time
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Optional: print or log execution time
        print(f"{func.__name__} took {execution_time:.2f} s")
        
        return result
    
    return wrapper
