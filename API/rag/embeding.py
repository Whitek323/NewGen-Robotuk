import json
import os
import ollama

class EmbeddingM:
    # Method สำหรับบันทึก embeddings
    def save_embedding(self, filename, embeddings):
        if not os.path.exists("embeddings"):
            os.makedirs("embeddings")
        with open(f"embeddings/{filename}.json", "w") as f:
            json.dump(embeddings, f)

    # Method สำหรับโหลด embeddings
    def load_embeddings(self, filename):
        if not os.path.exists(f"embeddings/{filename}.json"):
            return False
        with open(f"embeddings/{filename}.json", "r") as f:
            return json.load(f)

    # Method สำหรับดึง embeddings
    def get_embeddings(self, filename, modelname, chunks):
        # เรียกใช้ method load_embeddings ด้วย self
        if (embeddings := self.load_embeddings(filename)) is not False:
            return embeddings
        
        # ถ้าไม่มี embeddings ในไฟล์ ให้คำนวณ embeddings ใหม่
        embeddings = [
            ollama.embeddings(model=modelname, prompt=chunk)["embedding"]
            for chunk in chunks
        ]
        
        # บันทึก embeddings ที่คำนวณได้
        self.save_embedding(filename, embeddings)
        return embeddings
