# 📚 SnapStudy AI

**SnapStudy AI** is an AI-powered learning assistant that helps students understand their study materials faster.

Users can upload a PDF and use AI to:

* 📝 Summarize study material
* 🧠 Generate practice quizzes
* 💬 Ask questions about the uploaded PDF
* 📖 View extracted document content

## 🚀 Live Demo

https://snapstudy-ai-yzovtttzvcpv3tbq6xalzt.streamlit.app/

## 💡 Problem Statement

Students often spend a lot of time reading lengthy study materials and searching for important information.

SnapStudy AI provides a simple interface where students can upload their study material and interact with it using AI.

## ✨ Key Features

### 📄 PDF Upload

Upload notes, textbooks, or other study material in PDF format.

### 📝 AI Summarization

Generate a simple summary containing:

* Important concepts
* Short explanations
* Key points
* Takeaways

### 🧠 AI Quiz Generation

Generate multiple-choice questions from the uploaded study material for practice.

### 💬 Ask AI

Ask questions about the uploaded PDF and receive answers based on the document content.

### 📖 Extracted Text

View the text extracted from the uploaded PDF.

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API
* PyMuPDF
* Git & GitHub

## 🏗️ How It Works

```text
PDF Study Material
        ↓
   PDF Text Extraction
        ↓
     SnapStudy AI
        ↓
   Google Gemini API
        ↓
 ┌────────┬─────────┬──────────┐
 ↓        ↓         ↓
Summary  Quiz     Ask AI
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shridhar7m/SnapStudy-AI.git
```

### 2. Open the project

```bash
cd SnapStudy-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GOOGLE_API_KEY = "YOUR_API_KEY"
```

Do not upload this file to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🤖 AI Model

SnapStudy AI uses Google Gemini models through the Gemini API.

The application includes model fallback and retry handling to improve reliability when a model is temporarily unavailable.

## 🔐 Security

The Gemini API key is stored using Streamlit secrets and is not included in the GitHub repository.

## 🎯 Use Cases

SnapStudy AI can help:

* College students
* School students
* Competitive exam learners
* Self-learners
* Anyone studying from PDF materials

## 🔮 Future Improvements

Planned improvements include:

* Interactive quiz answering
* Score tracking
* Downloadable summaries
* Support for larger documents
* Local/offline AI model support
* Retrieval-Augmented Generation (RAG)
* Voice-based questions and answers
* Snapdragon/Qualcomm AI Hub optimized model deployment

## 👨‍💻 Developer

**Shridhar M**

BCA Graduate | Data Science & Python Developer Aspirant

GitHub:
https://github.com/Shridhar7m

LinkedIn:
https://www.linkedin.com/in/shridhar-m07/

---

⭐ **SnapStudy AI - Upload → Understand → Learn**
