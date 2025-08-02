import os
import faiss
import numpy as np
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorStore:
    def __init__(self, dim: int, store_dir: str = "vector_store"):
        self.dim = dim
        self.store_path = Path(store_dir)
        self.store_path.mkdir(exist_ok=True)

        self.index_path = self.store_path / "faiss.index"
        self.meta_path = self.store_path / "metadata.json"

        self.index = None
        self.metadata = []
        self._load()

    def _load(self):
        if self.index_path.exists() and self.meta_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                
                if self.index.d != self.dim:
                    logging.warning(
                        f"Stored index dimension ({self.index.d}) differs from "
                        f"configured dimension ({self.dim}). Re-initializing."
                    )
                    self._initialize_new_index()
                else:
                    logging.info(f"Loaded existing vector index with {self.index.ntotal} vectors.")
            except Exception as e:
                logging.error(f"Failed to load existing index or metadata: {e}. Re-initializing.")
                self._initialize_new_index()
        else:
            logging.info("No existing index found. Initializing a new one.")
            self._initialize_new_index()

    def _initialize_new_index(self):
        self.index = faiss.IndexFlatIP(self.dim)
        self.metadata = []

    def add(self, vectors: np.ndarray, texts: list[str]):
        if vectors.shape[0] != len(texts):
            raise ValueError("The number of vectors and texts must be the same.")
        
        if vectors.shape[1] != self.dim:
            raise ValueError(f"Vector dimension mismatch. Expected {self.dim}, got {vectors.shape[1]}.")

        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.metadata.extend(texts)
        logging.info(f"Added {len(vectors)} new vectors to the index.")

    def save(self):
        try:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.meta_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=4)
            logging.info(f"Saved vector index and metadata to {self.store_path}.")
        except Exception as e:
            logging.error(f"Failed to save index or metadata: {e}")
            raise

    def search(self, query_vector: np.ndarray, k: int = 5) -> list[tuple[float, str]]:
        if self.index.ntotal == 0:
            logging.warning("Search attempted on an empty index.")
            return []

        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        if query_vector.shape[1] != self.dim:
            raise ValueError(f"Query vector dimension mismatch. Expected {self.dim}, got {query_vector.shape[1]}.")

        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i in range(min(k, len(indices[0]))):
            idx = indices[0][i]
            if idx != -1:
                results.append((float(distances[0][i]), self.metadata[idx]))
        
        return results