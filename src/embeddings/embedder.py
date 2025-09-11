# src/embeddings/embedder.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2", device="auto"):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed(self, texts, batch_size=32):
        """
        texts: list[str]
        returns: np.ndarray (n, dim) float32, L2-normalized
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        # normalize to unit vectors for cosine-sim via inner product
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        embeddings = embeddings / norms
        return embeddings.astype("float32")
