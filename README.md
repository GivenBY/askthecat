# AskTheCat – AI Study Assistant

AskTheCat is an AI study assistant that reads study materials and answers questions based on their content. It supports PDFs, DOCX, PPTX, and images, including OCR for scanned files. It uses Groq LLMs, sentence-transformers, and FAISS, and runs on Streamlit.

---

## Features

* Upload PDFs, DOCX, PPTX, and image files
* Extract text and perform OCR on scanned or image-based content
* Generate embeddings using sentence-transformers
* Store and search content using FAISS
* Answer questions using Groq LLMs
* Streamlit-based chat interface

---

## Tech Stack

* Frontend: Streamlit
* Backend: Python 3.10+
* LLM: Groq API
* Embeddings: sentence-transformers
* Vector Store: FAISS
* File Processing: PyMuPDF, python-docx, python-pptx
* OCR: Tesseract

---

## Setup

Clone the repository:

```bash
git clone https://github.com/givenby/askthecat
cd askthecat
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY="your_api_key"
```

Run the app:

```bash
streamlit run ui/app.py
```

Open in browser:

```
http://localhost:8501
```

---

## License
MIT [LICENSE](LICENSE)
