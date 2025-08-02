# src/embedder.py

import logging
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logging.info(f"Using device: {self.device}")

        try:
            logging.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name, device=self.device)
            logging.info("Embedding model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load SentenceTransformer model '{model_name}'. Error: {e}")
            raise

    def embed(self, texts: list[str], batch_size: int = 32, normalize_embeddings: bool = True) -> np.ndarray:
        if not texts or not isinstance(texts, list):
            logging.warning("Input to embed is empty or not a list, returning empty array.")
            return np.array([])
            
        logging.info(f"Generating embeddings for {len(texts)} chunks...")
        
        try:
            embeddings = self.model.encode(
                texts, 
                batch_size=batch_size,
                show_progress_bar=True, 
                convert_to_numpy=True,
                normalize_embeddings=normalize_embeddings
            )
            logging.info("Embeddings generated successfully.")
            return embeddings
        except Exception as e:
            logging.error(f"An error occurred during embedding generation: {e}")
            return np.array([])