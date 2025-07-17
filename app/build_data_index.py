import os
import json

CHUNKS_DIR = "data/chunks"
DATA_DIR = "data"
INDEX_FILE = "data/data_index.json"

# Tags for core JSON wisdoms
core_json_files = {
    "gita_verses.json": "Gita",
    "ayurveda_principles.json": "Ayurveda",
    "chanakya_niti.json": "Politics",
    "upanishads_quotes.json": "Philosophy",
    "vedic_stories.json": "Stories"
}

index = []

# 📘 Add all chunked book files
for filename in os.listdir(CHUNKS_DIR):
    if filename.endswith(".jsonl"):
        index.append({
            "title": filename.replace(".jsonl", "").replace("-", " ").title(),
            "filename": f"chunks/{filename}",
            "type": "book",
            "subject": "Unknown"
        })

# 📚 Add core wisdom files
for filename, subject in core_json_files.items():
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        index.append({
            "title": filename.replace(".json", "").replace("_", " ").title(),
            "filename": filename,
            "type": "core_json",
            "subject": subject
        })

# 💾 Save it
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print(f"✅ data_index.json created with {len(index)} entries.")
