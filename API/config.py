EMBEDDING_MODEL = 'nomic-embed-text'

# LLM_MODEL = 'llama3.2:3b-instruct-q5_1'
LLM_MODEL = 'llama3.1:8b-instruct-q5_1'
# LLM_MODEL = 'llama3.2:latest'
# LLM_MODEL = 'llama3.1-ut0.3:latest'
TTS_MODEL = 'chuubjak/vits-tts-thai'
# TTS_MODEL = 'facebook/mms-tts-tha'


SYSTEM_PROMPT = """คุณคือโรโบตุ้คเป็นหุ่นยนต์มัคคุเทศก์แนะนำสถานที่ท่องเที่ยวในประเทศไทยที่ตอบคำถาม
                    โดยอ้างอิงจากข้อความ ที่ให้ไว้ในบริบท และไม่ต้องบอกข้อผิดพลาดของคุณและข้อมูล
                    ตอบอย่างกระชับระหว่างไม่ควรเกิน 80 ตัวอักษรและตีความข้อมูลจากผู้ใช้ตามที่ตั้งใจไว้ แม้ว่าจะมีข้อผิดพลาดในการสะกดคำ
                    หากคำสะกดผิดแต่ฟังดูคล้ายกันหรือมีความหมายใกล้เคียงกับคำที่รู้จัก
                    ให้ถือว่าคำนั้นเป็นคำที่ตั้งใจไว้และตอบกลับตามนั้น
                    หากผู้ใช้ถามเกี่ยวกับ วิธีไป หรือ เดินทางไปยังสถานที่นั้น หรือถามทิศทาง
                    ให้ส่ง ชื่อไฟล์คิวอาโค้ด.png โดยไม่ต้องให้ข้อมูลเพิ่มเติม
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
import logging
from flask import request

# Configure logging to print to console
logging.basicConfig(level=logging.INFO, 
                    format='[API Performance] %(message)s')

def api_timer(func):
    """
    Decorator to measure and log web API request processing time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Capture start time using high-resolution timer
        start_time = time.perf_counter()
        
        try:
            # Execute the original function
            response = func(*args, **kwargs)
            
            # Calculate execution time
            execution_time = time.perf_counter() - start_time
            
            # Log timing information
            logging.info(f"{request.method} {request.path} - Processing Time: {execution_time:.4f} seconds")
            
            return response
        
        except Exception as e:
            # Log any errors during processing
            logging.error(f"{request.method} {request.path} - Error: {str(e)}")
            raise

    return wrapper

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
