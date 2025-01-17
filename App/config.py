# Backend API URL
API_URL = "http://192.168.42.69:5000/chat"
API_PATH = "http://192.168.42.69:5000/"
# We’ll assume /transcribe is called from recorder.py

# Animation states
MODES = {
    "speak": ["./Display/img/5.jpg", "./Display/img/4.jpg"],
    "idle": ["./Display/img/5.jpg","./Display/img/4.jpg","./Display/img/6.jpg"],
    "work": ["./Display/img/3.jpg", "./Display/img/2.jpg", "./Display/img/1.jpg"],
}