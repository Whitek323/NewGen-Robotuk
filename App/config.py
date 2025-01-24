# Backend API URL
# API_URL = "http://192.168.42.69:5000/chat"
# API_PATH = "http://192.168.42.69:5000/"
API_URL = "http://127.0.0.1:5000/chat"
API_PATH = "http://127.0.0.1:5000/"
# We’ll assume /transcribe is called from recorder.py

# Animation states
MODES = {
    "speak": ["./Assets/face/5.jpg", "./Assets/face/4.jpg"],
    "idle": ["./Assets/face/5.jpg","./Assets/face/4.jpg","./Assets/face/6.jpg"],
    "work": ["./Assets/face/3.jpg", "./Assets/face/2.jpg", "./Assets/face/1.jpg"],
}