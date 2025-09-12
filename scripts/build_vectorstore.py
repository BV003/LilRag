# scripts/build_vectorstore.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore
from src.utils.text_splitter import chunk_text
from PyPDF2 import PdfReader
import glob
import numpy as np
import pickle
from tqdm import tqdm
import yaml



def load_config(path=None):
    """加载 YAML 配置文件"""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "configs", "config.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_file_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".pdf":
        try:
            reader = PdfReader(path)
            text = []
            for p in reader.pages:
                t = p.extract_text()
                if t:
                    text.append(t)
            return "\n".join(text)
        except Exception as e:
            print(f"Failed to read pdf {path}: {e}")
            return ""
    else:
        return ""

def main(args):
    files = []
    for ext in ["*.txt", "*.md", "*.pdf"]:
        files += glob.glob(os.path.join(args.data_dir, "**", ext), recursive=True)
    print(f"Found {len(files)} files")
    chunks = []
    metadatas = []
    for path in files:
        text = load_file_text(path)
        if not text:
            continue
        c_list = chunk_text(text, max_chars=args.max_chars, overlap=args.overlap)
        for i, c in enumerate(c_list):
            chunks.append(c)
            metadatas.append({"source": os.path.relpath(path, args.data_dir), "chunk_id": i, "text": c})

    print(f"Total chunks: {len(chunks)}")

    embedder = Embedder(model_name=args.model, device=args.device)
    batch_size = args.batch_size
    embeddings = []
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i+batch_size]
        emb = embedder.embed(batch, batch_size=batch_size)
        embeddings.append(emb)
    embeddings = np.vstack(embeddings)

    store = FaissStore.build(embeddings, metadatas)
    os.makedirs(os.path.dirname(args.index_path), exist_ok=True)
    store.save(args.index_path, args.meta_path)
    print("Saved index and metadata.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    config = load_config()
    parser.add_argument("--data-dir", default=config["data"]["data_dir"], help="directory with docs")
    parser.add_argument("--model", default=config["embedding"]["model"])
    parser.add_argument("--device", default=config["embedding"]["device"])
    parser.add_argument("--max-chars", type=int, default=config["embedding"]["max_chars"])
    parser.add_argument("--overlap", type=int,default=config["embedding"]["overlap"])
    parser.add_argument("--batch-size", type=int, default=config["embedding"]["batch_size"])
    parser.add_argument("--index-path", default=config["faiss"]["index_path"])
    parser.add_argument("--meta-path", default=config["faiss"]["meta_path"])
    args = parser.parse_args()
    main(args)
