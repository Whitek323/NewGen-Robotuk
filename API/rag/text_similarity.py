import numpy as np
from numpy.linalg import norm
import os

class TextSimilarity:
    def __init__(self, filename=None):
        self.filename = filename
        self.paragraphs = []

    def parse_file(self):
        if not self.filename:
            raise ValueError("No filename provided.")

        # อ่านไฟล์จากโฟลเดอร์ `upload/`
        filepath = os.path.join("upload", self.filename)
        with open(filepath, encoding="utf-8") as f:
            buffer = []
            for line in f.readlines():
                line = line.strip()
                if line:
                    buffer.append(line)
                elif len(buffer):
                    self.paragraphs.append(" ".join(buffer))
                    buffer = []
            if len(buffer):
                self.paragraphs.append("".join(buffer))
        return self.paragraphs


    def find_most_similar(self, needle, haystack):
        """หาความคล้ายคลึงระหว่าง 'needle' และรายการ 'haystack'"""
        needle_norm = norm(needle)
        similarity_scores = [
            np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
        ]
        return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)