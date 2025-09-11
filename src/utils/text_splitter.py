# src/utils/text_splitter.py
import re

def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200):
    """
    非常简单的分块器：按字符切分并做重叠。
    更复杂的版本可以按句子边界或使用 nltk/split。
    """
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + max_chars, L)
        chunk = text[start:end].strip()
        chunks.append(chunk)
        if end == L:
            break
        start = max(0, end - overlap)
    return chunks
