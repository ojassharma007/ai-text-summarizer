📰 AI Text Summarizer
This is a Streamlit application that provides an interactive interface for summarizing long texts using a pre-trained Hugging Face model. It automatically handles texts longer than the model's maximum input size by chunking the text and summarizing each chunk individually.

🚀 Features
Text Summarization: Uses the powerful facebook/bart-large-cnn model from Hugging Face for abstractive summarization.

Text Chunking: Automatically breaks down large texts into smaller chunks (default: 120 words) to handle model input limits.

Customizable Settings: Allows users to adjust:

Chunk Size: Control the word limit for each text chunk.

Summary Length: Set minimum and maximum word lengths for the generated summary.

Simple Web UI: An intuitive interface built with Streamlit.

🛠️ Installation
Prerequisites
You need Python 3.8+ installed on your system.

Steps
Clone the repository (if it were a git repo):

Bash

git clone <repository_url>
cd <repository_name>
Create a virtual environment and activate it (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
Install the dependencies from requirements.txt:

Bash

pip install -r requirements.txt
The main dependencies for the app's functionality are 

streamlit, requests, and python-dotenv.

Set up your API Key:

This project uses a Hugging Face API key for accessing the summarization model.

Create a file named .env in the root directory.

Add your Hugging Face API key to the file in the following format:

Ini, TOML

HF_API_KEY=your_hugging_face_api_key_here

Note: The .env file is excluded from version control by the .gitignore file for security.

▶️ How to Run
Make sure your virtual environment is active and dependencies are installed.

Run the Streamlit application from your terminal:

Bash

streamlit run app.py
The application will open in your default web browser (usually at http://localhost:8501).

📝 How to Use the App
Paste your text into the main text area labeled "📄 Paste your text here:".

(Optional) Adjust settings in the sidebar:

Use the "Chunk Size (words)" slider to change how large the text chunks are before they are sent to the model (default is 120 words).

Adjust "Min Summary Length" and "Max Summary Length" to control the size of the output summary.

Click the "✨ Summarize" button.

The final, complete summary will appear below the input box under the "📝 Summary:" heading.
