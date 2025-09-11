# scripts/run_qa.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from src.vectorstore.faiss_store import FaissStore
from src.embeddings.embedder import Embedder
from src.llm.openai_llm import OpenAILLM
from src.llm.doubao_llm import DouBaoLLM
from src.pipeline.rag_pipeline import RAGPipeline

def main(args):
    store = FaissStore.load(args.index_path, args.meta_path)
    embedder = Embedder(model_name=args.embed_model, device=args.device)
    # llm = OpenAILLM(model=args.openai_model, temperature=args.temperature)
    llm = DouBaoLLM(model=args.openai_model, temperature=args.temperature)
    rag = RAGPipeline(store, embedder, llm, max_retrieval=args.max_retrieval)

    if args.query:
        resp = rag.answer(args.query)
        print("=== ANSWER ===")
        print(resp["answer"])
        print("\n=== SOURCES ===")
        for s in resp["sources"]:
            print(s)
        return

    # interactive loop
    print("Enter question (empty to quit):")
    while True:
        q = input("> ").strip()
        if not q:
            break
        resp = rag.answer(q)
        print("\n--- Answer ---")
        print(resp["answer"])
        print("\n--- Sources ---")
        for s in resp["sources"]:
            print(s)
        print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-path", default="data/store/faiss.index")
    parser.add_argument("--meta-path", default="data/store/meta.pkl")
    parser.add_argument("--embed-model", default="all-MiniLM-L6-v2")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--openai-model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-retrieval", type=int, default=5)
    parser.add_argument("--query", default=None, help="one-shot query and exit")
    args = parser.parse_args()
    main(args)
