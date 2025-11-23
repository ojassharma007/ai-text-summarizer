import streamlit as st 
import requests
from config import HF_API_KEY


MODEL_NAME = "facebook/bart-large-cnn"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def chunk_text(text, max_words=120):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

def summarize(text):
    chunks = list(chunk_text(text))
    summaries = []
    for chunk in chunks:
        payload = {
            "inputs": chunk,
            "parameters": {
                "min_length": 50,
                "max_length": 150,
                "do_sample": False
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            summaries.append(response.json()[0]["summary_text"])
        except:
            summaries.append("⚠️ Error: Could not generate summary for this chunk.")
    return " ".join(summaries)

# ----- STREAMLIT UI -----
st.set_page_config(
    page_title=" AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Model",
    ["facebook/bart-large-cnn"],
    index=0
)

max_chunk_words = st.sidebar.slider("Chunk Size (words)", min_value=50, max_value=300, value=120, step=10)
min_summary_length = st.sidebar.slider("Min Summary Length", 30, 200, 50)
max_summary_length = st.sidebar.slider("Max Summary Length", 100, 500, 150)

# Update API URL if model changed
API_URL = f"https://api-inference.huggingface.co/models/{model_choice}"


st.markdown("<h1 style='text-align: center; color: green;'>📰 AI Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Paste your story or text below and get a complete summary</p>", unsafe_allow_html=True)


with st.expander("ℹ️ How to use"):
    st.write("""
        1. Paste your story or text in the box below.  
        2. Adjust the chunk size and summary length from the sidebar if needed.   
        3. Click 'Summarize' to generate a full summary.  
    """)


user_input = st.text_area("📄 Paste your text here:", height=300)

if st.button("✨ Summarize"):
    if user_input.strip():
        with st.spinner("Summarizing your story... ⏳"):
            # chunk size from slider
            chunks = list(chunk_text(user_input, max_words=max_chunk_words))
            summaries = []
            for chunk in chunks:
                payload = {
                    "inputs": chunk,
                    "parameters": {
                        "min_length": min_summary_length,
                        "max_length": max_summary_length,
                        "do_sample": False
                    }
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                try:
                    summaries.append(response.json()[0]["summary_text"])
                except:
                    summaries.append("⚠️ Error in this chunk.")
            final_summary = " ".join(summaries)

        st.markdown("<h3 style='color: green;'>📝 Summary:</h3>", unsafe_allow_html=True)
        st.success(final_summary)
    else:
        st.warning("⚠️ Please enter some text to summarize.")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ in Streamlit</p>", unsafe_allow_html=True)
