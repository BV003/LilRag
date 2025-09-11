# src/pipeline/rag_pipeline.py
from typing import List
from src.vectorstore.faiss_store import FaissStore
from src.embeddings.embedder import Embedder
from src.llm.base_llm import BaseLLM
import numpy as np

class RAGPipeline:
    def __init__(self, faiss_store: FaissStore, embedder: Embedder, llm: BaseLLM, max_retrieval=5):
        self.store = faiss_store
        self.embedder = embedder
        self.llm = llm
        self.max_retrieval = max_retrieval

    def answer(self, query: str, return_sources: bool = True):
        q_emb = self.embedder.embed([query])[0]
        hits = self.store.search(q_emb.reshape(1, -1), k=self.max_retrieval)[0]
        # 构建 prompt
        context = []
        sources = []
        for i, h in enumerate(hits):
            meta = h["metadata"]
            txt = meta.get("text", "")
            src = meta.get("source", "unknown")
            chunk_id = meta.get("chunk_id", i)
            context.append(f"[{i+1}] Source: {src} | chunk_id: {chunk_id}\n{txt}")
            sources.append(f"{src}#chunk{chunk_id}")
        context_block = "\n\n---\n\n".join(context)
        prompt = (
            "You are a helpful assistant. Use the provided context to answer the question. "
            "Cite only from the provided context and list sources at the end.\n\n"
            f"CONTEXT:\n{context_block}\n\nQUESTION: {query}\n\nAnswer:"
        )
        answer = self.llm.generate(prompt)
        if return_sources:
            return {"answer": answer, "sources": sources, "hits": hits}
        return {"answer": answer}
