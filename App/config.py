# Backend API URL
# API_URL = "http://192.168.42.69:5000/chat"
# API_PATH = "http://192.168.42.69:5000/"
API_URL = "http://127.0.0.1:5000/chat"
API_PATH = "http://127.0.0.1:5000/"
# We’ll assume /transcribe is called from recorder.py

# Animation states
MODES = {
    "speak": ["./Device/img/5.jpg", "./Device/img/4.jpg"],
    "idle": ["./Device/img/5.jpg","./Device/img/4.jpg","./Device/img/6.jpg"],
    "work": ["./Device/img/3.jpg", "./Device/img/2.jpg", "./Device/img/1.jpg"],
}