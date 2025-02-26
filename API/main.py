from flask import Flask, request, jsonify
from features.qrcode import QRCodeHandler
from rag import *
from config import *
from sound import TTS
import ollama
import os
from faster_whisper import WhisperModel
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Initialize necessary objects
embed_m = EmbeddingM()
qr_handler = QRCodeHandler()

# Initialize embeddings
paragraphs = []
embeddings = []

first_request = True
model = WhisperModel("small", device="cpu")

@app.route("/")
def hello():
    return "Hello from Flask!"


@app.route('/transcribe', methods=['POST'])
def transcribe():
    stt_start_time = time.perf_counter()
    # Check if a file is sent
    if 'file' not in request.files:
        return "No file provided", 400

    # Save the uploaded file
    audio_file = request.files['file']
    audio_path = "uploaded_audio.wav"
    audio_file.save(audio_path)

    # Transcribe the audio
    print("Transcribing audio...")
    segments, info = model.transcribe(audio_path)

    # Combine transcription segments
    transcription = " ".join([segment.text for segment in segments])
    print(f"Transcription completed: {transcription}")
    stt_time_counter = round(time.perf_counter() - stt_start_time,2)
    return jsonify({
        "transcription": transcription,
        "time_use": stt_time_counter
        })


@app.before_request
def initialize_embeddings():
    global paragraphs, embeddings, text_simi
    files = [f for f in os.listdir("upload") if f.endswith(".txt")]
    for filename in files:
        text_simi = TextSimilarity(filename)
        file_paragraphs = text_simi.parse_file()
        file_paragraphs = ["".join(file_paragraphs[i : i + 2]) for i in range(0, len(file_paragraphs), 2)]
        file_embeddings = embed_m.get_embeddings(filename, EMBEDDING_MODEL, file_paragraphs)
        paragraphs.extend(file_paragraphs)
        embeddings.extend(file_embeddings)
        
@app.route('/chat', methods=['POST'])
def handle_chat():
    llm_start_time = time.perf_counter()
    data = request.json
    prompt = data.get("prompt", "")

    # Generate embeddings for the prompt
    prompt_embedding = ollama.embeddings(model=EMBEDDING_MODEL, prompt=prompt)["embedding"]
    most_similar_chunks = text_simi.find_most_similar(prompt_embedding, embeddings)[:5]

    # Generate response using Ollama
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT + "\n".join(paragraphs[item[1]] for item in most_similar_chunks),
            },
            {"role": "user", "content": prompt},
        ],
    )
    llm_processing_time = time.perf_counter() - llm_start_time
    tts_start_time = time.perf_counter()
    audio_file_path = "static/audio/response.wav"  # Save audio in a static folder
    # Process TTS
    tts_text = response["message"]["content"]
    tts = TTS(tts_text,audio_file_path)
    tts.vistts(TTS_MODEL)
    # tts.gtts()

    tts_processing_time = time.perf_counter() - tts_start_time
    # Check for QR code in the response
    qr_path = qr_handler.find_qr_in_response(response["message"]["content"])
    return jsonify({
        "response": response["message"]["content"],
        "qr_path": qr_path,
        "audio_path": audio_file_path,  # Include the audio file path in the response
        "llm_time_couter": round(llm_processing_time, 2),
        "tts_time_couter": round(tts_processing_time,2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
