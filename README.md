# 🐱 AskTheCat – Your Lazy Study Buddy

So you’ve got too many study materials and not enough brain RAM? Throw your notes at this cat. It reads all your crap and answers like it’s been secretly doing 10x engineering while napping.

Built with Streamlit because React is too much work. Powered by Groq LLMs 'cause they’re turbo fast.

---

## ✨ Features

* **Upload Your Mess**:

  * PDFs
  * Word Docs (.docx)
  * PowerPoints (.pptx)
  * Image files (.png, .jpg, etc.)

* **Reads Literally Anything**:

  * Text? Easy.
  * Images inside slides or scanned PDFs? OCR handles it like a champ.

* **RAG Magic**:

  * Smart embeddings via sentence-transformers
  * FAISS = fancy text search engine on roids
  * Groq-powered LLMs reply like it knows everything (almost)

* **Chat Like It’s 2025**:

  * Streamlit chat UI, no weird CSS
  * Dropdown to choose your LLM weapon (Llama, Mixtral, Gemma, etc.)

---

## 🛠️ Tech Stack

* Frontend: Streamlit (no React, we’re chill)
* Backend: Python 3.10+
* LLMs: Groq API (Llama 3, Mixtral, Gemma 2, and more)
* Embeddings: sentence-transformers
* Vector Store: FAISS
* File Reading:

  * PyMuPDF, python-docx, python-pptx
  * Tesseract OCR (for image-based suffering)

---

## 🚀 Getting Started

### Prereqs

* Python 3.10+ (yes, it matters)
* Git
* Tesseract-OCR (seriously, install it)

```bash
git clone https://github.com/givenby/askthecat
cd askthecat
```

### Virtual Env Setup:

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### Install the Goods:

```bash
pip install -r requirements.txt
```

### Add Your Secrets Like a Spy:

Create `.streamlit/secrets.toml` with:

```toml
GROQ_API_KEY="gsk_yourSuperSecretGroqKey"
```

### Run It Like a Boss:

```bash
streamlit run ui/app.py
```

Then open `http://localhost:8501` in your browser. It just works™.

---

## 🚢 Deploying Because You’re Fancy

### Streamlit Cloud

* Add `packages.txt`:

  ```
  tesseract-ocr
  poppler-utils
  ```
* Push code to GitHub
* Add your Groq API key in Streamlit secrets

### Hugging Face Spaces (if you like chaos)

* Docker is ready to go. Use this from root:

```bash
docker build -t askthecat . && docker run -p 7860:7860 askthecat
```

---

## 🔮 What’s Cooking (Coming Soon)

* Citations so you can pretend it's research
* See the chunks it retrieved (for nerds)
* Save your vector DB like save game files
* Semantic chunking (because fixed-size is dumb)
* Docker that actually works

---

## 📄 License

[MIT](LICENSE) – Basically, do what you want, just don’t blame the cat.
