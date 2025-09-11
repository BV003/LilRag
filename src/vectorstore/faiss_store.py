# src/vectorstore/faiss_store.py
import faiss
import numpy as np
import pickle
import os

class FaissStore:
    def __init__(self, index=None, metadata=None):
        self.index = index
        self.metadata = metadata or []

    @classmethod
    def build(cls, embeddings: np.ndarray, metadatas: list):
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype("float32")
        dim = embeddings.shape[1]
        # 使用内积（需先 normalize 嵌入）
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        return cls(index=index, metadata=metadatas)

    def search(self, query_embedding: np.ndarray, k=5):
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        results = []
        for scores, idxs in zip(D, I):
            hits = []
            for score, idx in zip(scores, idxs):
                if idx < 0:
                    continue
                meta = self.metadata[idx]
                hits.append({"score": float(score), "metadata": meta})
            results.append(hits)
        return results

    def add(self, embeddings: np.ndarray, metadatas: list):
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def save(self, index_path, meta_path):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls, index_path, meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
        return cls(index=index, metadata=metadata)
