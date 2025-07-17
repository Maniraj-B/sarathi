import os
import json
from pathlib import Path
from tqdm import tqdm
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# ===== PATHS =====
RAW_DIR = "data/raw_books"
TEXT_DIR = "data/extracted_texts"
CHUNK_DIR = "data/chunks"
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(CHUNK_DIR, exist_ok=True)

# ===== OCR & Poppler Setup =====
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Release-24.08.0-0\poppler-24.08.0\Library\bin"  # 👈 Your actual path to poppler's bin

# ===== Extract text with OCR fallback =====
def extract_text_with_ocr_fallback(pdf_path, dpi=300):
    text_output = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        if not text or len(text.strip()) < 20:
            print(f"🔍 OCR fallback for page {page_num + 1}")
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=page_num + 1,
                last_page=page_num + 1,
                poppler_path=POPPLER_PATH
            )
            ocr_text = pytesseract.image_to_string(images[0], lang='eng')
            text_output.append(ocr_text.strip())
        else:
            text_output.append(text.strip())

    return "\n\n".join(text_output)

# ===== Split into chunks =====
def split_text_into_chunks(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# ===== Process and save chunks =====
def process_pdf(file_path):
    filename = Path(file_path).stem
    print(f"📖 Processing: {filename}")

    text = extract_text_with_ocr_fallback(file_path)
    if not text.strip():
        print(f"⚠️ No text found in {filename}")
        return

    txt_path = os.path.join(TEXT_DIR, f"{filename}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    chunks = split_text_into_chunks(text)
    chunk_json_path = os.path.join(CHUNK_DIR, f"{filename}.jsonl")
    with open(chunk_json_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            entry = {
                "chunk_id": i,
                "book": filename,
                "text": chunk,
                "source": f"{filename}_page_unknown"
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Saved {len(chunks)} chunks → {chunk_json_path}")

# ===== Run all PDFs =====
if __name__ == "__main__":
    pdf_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]
    for pdf_file in tqdm(pdf_files, desc="📚 Chunking all books"):
        process_pdf(os.path.join(RAW_DIR, pdf_file))
