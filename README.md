Sarathi — Your Spiritual AI Guide
Sarathi is a Retrieval-Augmented Generation (RAG) chatbot inspired by the timeless wisdom of Indian scriptures like the Bhagavad Gita, Ayurveda, Upanishads, Chanakya Niti, and Vedic stories. Powered by a local LLM (Phi-2) and a custom-built RAG pipeline, Sarathi responds in a compassionate, Krishna-like tone — giving advice that is both spiritually grounded and practically helpful.

🌟 Features
🧠 Searches across 5 ancient Indian knowledge sources

🔍 Intelligent keyword extraction and AND-based search

💬 Generates Krishna-style compassionate responses

📚 Uses a local lightweight LLM (Phi-2)

🌿 Personalized answers including Ayurveda, Gita, Niti & more

🖥️ Beautiful dark-themed Streamlit UI with typing animation

📚 Knowledge Sources
Bhagavad Gita

JSON includes: Chapter, Verse, Translation, Purport

Ayurveda

Problems, doshas, diet recommendations, herbal remedies

Chanakya Niti

Practical and ethical wisdom slokas

Upanishads

Philosophical quotes and teachings on soul, mind, and duty

Vedic Stories

Mythological stories with morals (e.g., Nachiketa and Yama)

⚙️ How It Works
Sarathi uses a RAG pipeline:

User inputs a query (e.g., “I have a stomach ache”)

The query is cleaned → stopwords removed → keywords extracted.

Keyword search runs on:

ChromaDB collection (for general Vedic wisdom)

Gita JSON (translation + purport)

Ayurveda JSON (problem field)

Chanakya Niti, Upanishads, and Vedic stories

The top results are stitched into a context block

That context + original query becomes a custom prompt

The prompt is sent to a local Phi-2 LLM (via llm_wrapper.py)

LLM returns a Krishna-style answer full of warmth and insight ✨

🖥️ UI (Streamlit)
Built with Streamlit

Includes dark mode + golden theme

Shows "Sarathi is thinking..." spinner

Displays animated typing effect like a real conversation

📂 Project Structure
pgsql
Copy
Edit
sarathi/
├── app/
│   ├── rag_pipeline.py           # RAG logic & search functions
│   ├── llm_wrapper.py            # Loads and runs Phi-2 LLM
│   └── data/                      # JSON wisdom files
│       ├── gita_verses.json
│       ├── ayurveda_principles.json
│       ├── chanakya_niti.json
│       ├── upanishads_quotes.json
│       └── vedic_stories.json
├── ui.py                         # Streamlit UI
├── requirements.txt
└── README.md
📦 Installation
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/your-username/sarathi.git
cd sarathi

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run ChromaDB separately
chromadb run --path ./chroma_store

# 5. Populate ChromaDB if empty (optional script)

# 6. Run the LLM locally
python app/llm_wrapper.py

# 7. Launch the UI
streamlit run ui.py
