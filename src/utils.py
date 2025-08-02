import os
import re
import unicodedata
from pathlib import Path

def detect_file_type(file_name: str) -> str:
    if not file_name or not isinstance(file_name, str):
        return ""
    suffix = Path(file_name).suffix
    return suffix[1:].lower() if suffix else ""


def clean_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""

    text = unicodedata.normalize('NFKC', text)

    text = text.lower()

    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    text = re.sub(r'<.*?>', '', text)

    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    text = re.sub(r'\s+', ' ', text)

    return text.strip()