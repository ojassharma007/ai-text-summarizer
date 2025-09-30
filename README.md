# 📰 AI Text Summarizer

A **Streamlit application** that summarizes long texts using the Hugging Face `facebook/bart-large-cnn` model. The app automatically splits texts that exceed the model’s input limit into chunks and summarizes each chunk individually.

---

## 🚀 Features

- **Text Summarization:** Uses a pre-trained Hugging Face model for abstractive summarization.  
- **Text Chunking:** Automatically splits large texts into smaller chunks (default: 120 words).  
- **Customizable Settings:** Adjust chunk size and summary length for precise control.  
- **Simple Web UI:** Intuitive interface built with Streamlit.  

---

## 🛠️ Setup Instructions

1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

2. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Configure Hugging Face API Key

Create a .env file in the project root.

Add your Hugging Face API key:
```bash
HF_API_KEY=your_hugging_face_api_key_here
```

5. Run the Application
```bash
streamlit run app.py

```
---
🔑 Setup API Key

This project uses the Hugging Face API for model access.

Create a .env file in the root directory.

Add your Hugging Face API key:
```bash
HF_API_KEY=your_hugging_face_api_key_here
```

Running the App
```bash
streamlit run app.py
```
---
📝 How to Use

- Paste your text into the main text area labeled 📄 Paste your text here:.
- Optional sidebar adjustments:
- Chunk Size (words): Controls text chunking before summarization.
- Min/Max Summary Length: Controls the size of the output summary.
- Click ✨ Summarize.
- The final summary appears below the input box.

📦 Dependencies

The minimal dependencies required to run the app are:

- streamlit
- requests
- python-dotenv
- transformers
- torch
  
⚡ Notes
Handles long texts by chunking and summarizing each part separately.
Designed for simplicity and easy deployment.





