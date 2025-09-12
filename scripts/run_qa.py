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
import yaml
from types import SimpleNamespace

def load_config(path=None):
    """加载 YAML 配置文件"""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "configs", "config.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main(args):
    store = FaissStore.load(args.index_path, args.meta_path)
    embedder = Embedder(model_name=args.embed_model, device=args.device)
    

    if args.llm_provider == "openai":
        llm = OpenAILLM(model=args.llm_model, temperature=args.temperature)
    elif args.llm_provider == "doubao":
        llm = DouBaoLLM(model=args.llm_model, temperature=args.temperature)

    
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
    config = load_config()
    parser.add_argument("--index-path", default=config["faiss"]["index_path"])
    parser.add_argument("--meta-path",default=config["faiss"]["meta_path"])
    parser.add_argument("--embed-model", default=config["embedding"]["model"])
    parser.add_argument("--device", default=config["embedding"]["device"])
    parser.add_argument("--llm-provider", default=config["llm"]["provider"])
    parser.add_argument("--llm-model", default=config["llm"]["model"])
    parser.add_argument("--temperature", type=float, default=config["llm"]["temperature"])
    parser.add_argument("--max-retrieval", type=int, default=config["llm"]["max_retrieval"])
    parser.add_argument("--query", default=None, help="one-shot query and exit")
    args = parser.parse_args()
    main(args)
