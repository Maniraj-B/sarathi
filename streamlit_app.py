import sys
import os
import time

# Add app folder to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
from rag_pipeline import ask_sarathi

import streamlit as st
import textwrap

# 🌟 Page Setup
st.set_page_config(
    page_title="Sarathi — Your Spiritual AI Guide",
    page_icon="",
    layout="centered"
)


st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0b0c10;
    color: #f4c430;
    font-family: 'Georgia', serif;
}

h1, h2, h3, h4 {
    color: #ffd700;
    text-align: center;
}

.stTextInput > div > div > input {
    background-color: #1f1f1f;
    color: #f4c430;
    border: 1px solid #f4c430;
}

.stButton > button {
    background-color: #3a2e1e;
    color: #f4c430;
    border: 1px solid #f4c430;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #564d2d;
}

.stMarkdown {
    font-size: 1.1rem;
    line-height: 1.7;
}

.blockquote {
    background: #1f1f1f;
    border-left: 4px solid #f4c430;
    margin: 1em 0;
    padding: 1em;
    font-style: italic;
    color: #f4f4f4;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## Sarathi — Your Spiritual Guide", unsafe_allow_html=True)
st.markdown("#### Merging Bhagavad Gita, Ayurveda, Upanishads, and more into divine wisdom ✨", unsafe_allow_html=True)
st.markdown("---")


with st.form("ask_form"):
    user_query = st.text_input(" What's troubling your soul today?")
    submitted = st.form_submit_button("✨ Ask Sarathi")

if submitted and user_query.strip():
    with st.spinner("⚡ Summoning divine insight..."):
        response = ask_sarathi(user_query, return_only_response=True)
    
    # Format response better if it's too long or includes weird markdown
    formatted_response = textwrap.fill(response, width=100)
    
    st.markdown("###  Sarathi says:")
    placeholder = st.empty()
    typed_text = ""

    for word in response.split():
        typed_text += word + " "
        placeholder.markdown(f"<div class='blockquote'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(0.05)  # typing speed (adjust if needed)


st.markdown("---")