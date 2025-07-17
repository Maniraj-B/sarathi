import nltk
import json
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
from chromadb import HttpClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from nltk.corpus import stopwords
from llm_wrapper import generate_response

# === Setup ===
nltk.data.path.append(r"C:\Users\manir\AppData\Roaming\nltk_data")
model_name = "all-MiniLM-L6-v2"
embedding_fn = SentenceTransformerEmbeddingFunction(model_name=model_name)
chroma_client = HttpClient(host="localhost", port=8000)
collection = chroma_client.get_collection("sarathi_books")
stop_words = set(stopwords.words("english"))

# === Load Core JSON Files ===
def load_json(name):
    path = Path("data") / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

gita_verses      = load_json("gita_verses.json")
ayurveda_data    = load_json("ayurveda_principles.json")
niti_verses      = load_json("chanakya_niti.json")
upanishad_quotes = load_json("upanishads_quotes.json")
vedic_stories    = load_json("vedic_stories.json")

# === Helpers ===
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word not in stop_words]

# === Search Functions ===
def search_chroma(query, top_k=5):
    results = collection.query(query_texts=[query], n_results=top_k)
    raw_docs = results["documents"][0]
    return [
        doc for doc in raw_docs
        if doc and len(doc) < 500 and "�" not in doc and "@" not in doc and any(c.isalpha() for c in doc)
    ]

def search_gita(query):
    keywords = extract_keywords(query)
    return [
        v for v in gita_verses
        if all(kw in (v["translation"] + v["purport"]).lower() for kw in keywords)
    ]

def search_ayurveda(query):
    keywords = extract_keywords(query)
    results = [
        entry for entry in ayurveda_data
        if all(kw in entry["problem"].lower() for kw in keywords)
    ]
    return results

def search_niti(query):
    keywords = extract_keywords(query)
    return [v for v in niti_verses if all(kw in v["text"].lower() for kw in keywords)]

def search_upanishads(query):
    keywords = extract_keywords(query)
    return [v for v in upanishad_quotes if all(kw in v["quote"].lower() for kw in keywords)]

def search_stories(query):
    keywords = extract_keywords(query)
    return [
        s for s in vedic_stories
        if all(kw in (s["summary"] + s["moral"]).lower() for kw in keywords)
    ]

# === Prompt Builder ===
def build_prompt(user_query, chroma_docs, gita_hits, ayurveda_hits, niti_hits, upanishad_hits, story_hits):
    context = ""

    if chroma_docs:
        context += "\n# 🧠 Wisdom from Books:\n" + "\n".join(["- " + d for d in chroma_docs[:3]])
    if gita_hits:
        context += "\n# 📜 Bhagavad Gita:\n" + "\n".join([
            f"Chapter {v['chapter']}, Verse {v['verse']}: {v['translation']}" for v in gita_hits[:2]
        ])
    if ayurveda_hits:
        context += "\n# 🌿 Ayurveda:\n" + "\n".join([
            f"- {v['problem']} → {v['diet']} | Herbs: {', '.join(v['herbs'])}" for v in ayurveda_hits[:1]
        ])
    if niti_hits:
        context += "\n# 🧠 Chanakya Niti:\n" + "\n".join(["- " + v["text"] for v in niti_hits[:1]])
    if upanishad_hits:
        context += "\n# 🕉️ Upanishads:\n" + "\n".join(["- " + q["quote"] for q in upanishad_hits[:1]])
    if story_hits:
        context += "\n# 📖 Vedic Story:\n" + "\n".join([f"- {s['title']}: {s['moral']}" for s in story_hits[:1]])

    return f"""
You are Sarathi 🕉️ — a guiding AI . 
You help people by blending deep insights from Indian culture ( like health problems ayurveda, emotional problems Bhagvadh Gita ) with practical advice.

Use the following sacred insights as reference( only refer dont fully use or go with):
{context}

Now answer the question below in a warm, compassionate tone:
👉 Question: {user_query}

✍️ Your Answer (quote scripture where helpful only when required, and be practical too):
"""

# === Main Function ===
def ask_sarathi(query, return_only_response=False):
    print("🔍 Starting search...")
    chroma_docs    = search_chroma(query)
    print("✅ Chroma done")
    gita_hits      = search_gita(query)
    print("✅ Gita done")
    ayurveda_hits  = search_ayurveda(query)
    print("✅ Ayurveda done")
    niti_hits      = search_niti(query)
    print("✅ Niti done")
    upanishad_hits = search_upanishads(query)
    print("✅ Upanishads done")
    story_hits     = search_stories(query)
    print("✅ Stories done")


    prompt = build_prompt(query, chroma_docs, gita_hits, ayurveda_hits, niti_hits, upanishad_hits, story_hits)

    if return_only_response:
        return generate_response(prompt)

    print("\n🧘 Final Prompt:\n", prompt)
    response = generate_response(prompt)
    print("\n🔮 Sarathi says:\n", response)
    return response


# === CLI Loop ===
def main_cli():
    while True:
        query = input("Ask Sarathi 🕉️: ")
        if query.lower() in ["exit", "quit"]:
            break
        ask_sarathi(query)

if __name__ == "__main__":
    main_cli()
