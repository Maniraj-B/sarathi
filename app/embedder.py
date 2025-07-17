import os
import os
import json
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from chromadb import HttpClient

CHUNKS_DIR = "data/chunks"
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Connect to running Chroma server
chroma_client = HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection("sarathi_books")

# === Function to embed one book ===
def embed_chunks_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    texts, metadatas, ids = [], [], []
    filename = Path(filepath).stem

    for i, line in enumerate(lines):
        entry = json.loads(line)
        chunk_id = f"{filename}_{i}"
        texts.append(entry["text"])
        ids.append(chunk_id)
        metadatas.append({
            "book": entry.get("book", filename),
            "source": entry.get("source", "unknown")
        })

    print(f"📦 Embedding {len(texts)} chunks from {filename}")
    embeddings = model.encode(texts, show_progress_bar=True)
    collection.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)

# === Embed all JSONL books ===
def embed_all_chunks():
    chunk_files = [f for f in os.listdir(CHUNKS_DIR) if f.endswith(".jsonl")]
    for file in tqdm(chunk_files, desc="🔗 Embedding all books"):
        embed_chunks_from_file(os.path.join(CHUNKS_DIR, file))

if __name__ == "__main__":
    embed_all_chunks()
