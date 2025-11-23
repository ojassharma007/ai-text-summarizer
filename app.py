import os
import streamlit as st
import requests
from transformers import AutoTokenizer


HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    try:
        from config import HF_API_KEY as _k
        HF_API_KEY = HF_API_KEY or _k
    except Exception:
        pass

MODEL_NAME = "facebook/bart-large-cnn"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# --- Load tokenizer once ---
@st.cache_resource
def load_tokenizer(name):
    return AutoTokenizer.from_pretrained(name)

tokenizer = load_tokenizer(MODEL_NAME)

# --- Helper: make simple token-safe chunks (hidden complexity) ---
def _chunk_text(text, max_tokens=900, overlap=60):
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    step = max_tokens - overlap
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokenizer.decode(tokens[start:end], skip_special_tokens=True, clean_up_tokenization_spaces=True).strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks

# --- Helper: call HF Router with basic retry ---
def _summarize_chunk(chunk, min_len=20, max_len=120):
    payload = {"inputs": chunk, "parameters": {"min_length": min_len, "max_length": max_len, "do_sample": False}}
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        except Exception as e:
            if attempt == 2:
                return f"⚠️ Network error: {e}"
            continue
        if r.status_code != 200:
            # show simple helpful message
            return f"⚠️ HF error {r.status_code}: {r.text[:200]}"
        try:
            data = r.json()
            if isinstance(data, list) and data and "summary_text" in data[0]:
                return data[0]["summary_text"]
            return f"⚠️ Unexpected HF response: {str(data)[:200]}"
        except Exception as e:
            return f"⚠️ Response parse error: {e}"
    return "⚠️ Failed after retries."

# --- Streamlit UI (very simple) ---
st.set_page_config(page_title="Summarizer", page_icon="📝")
st.title("AI Text Summarizer")
st.write("Paste text, click Summarize. (Keep defaults for best results and paste less than 800 words.)")

user_text = st.text_area("Your text", height=300)
max_summary = st.slider("Max summary length (words)", 50, 300, 120)

if st.button("Summarize"):
    if not user_text.strip():
        st.warning("Please paste some text first.")
    elif not HF_API_KEY:
        st.error("HF_API_KEY not found. Set environment variable HF_API_KEY or create config.py with HF_API_KEY.")
    else:
        with st.spinner("Working... this may take a moment for long texts"):
            chunks = _chunk_text(user_text)
            st.info(f"Processing {len(chunks)} chunks")
            summaries = []
            for i, ch in enumerate(chunks, 1):
                s = _summarize_chunk(ch, min_len=20, max_len=max_summary)
                summaries.append(s)
                st.write(f"Chunk {i}: {s[:200]}")

            final = " ".join(summaries)
            # final short pass if not an error
            if any(x.startswith("⚠️") for x in summaries):
                st.warning("One or more chunks returned errors; see above. Result below may be partial.")
            else:
                final_short = _summarize_chunk(final, min_len=30, max_len=max(80, int(max_summary/2)))
                final = final_short or final

            st.subheader("Summary")
            st.success(final)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Made with 💚 in Streamlit</p>", unsafe_allow_html=True)
