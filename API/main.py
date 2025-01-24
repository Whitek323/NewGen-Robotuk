from flask import Flask, request, jsonify
from QR_Codes.qrcode import QRCodeHandler
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
text_simi = TextSimilarity("pg16.txt")
qr_handler = QRCodeHandler()

# Initialize embeddings
paragraphs = []
embeddings = []

first_request = True
model = WhisperModel("small", device="cuda")

@app.route("/")
def hello():
    return "Hello from Flask!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
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

    return jsonify({"transcription": transcription})


@app.before_request
def initialize_embeddings():
    global paragraphs, embeddings
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

    audio_file_path = "static/audio/response.wav"  # Save audio in a static folder
    # Process TTS
    tts_text = response["message"]["content"]
    tts = TTS(tts_text,audio_file_path)
    # tts.vistts(TTS_MODEL)
    tts.gtts()

    # Check for QR code in the response
    qr_path = qr_handler.find_qr_in_response(response["message"]["content"])
    return jsonify({
        "response": response["message"]["content"],
        "qr_path": qr_path,
        "audio_path": audio_file_path  # Include the audio file path in the response
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
