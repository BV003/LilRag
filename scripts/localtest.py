import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tqdm import tqdm
from src.vectorstore.faiss_store import FaissStore
from src.embeddings.embedder import Embedder
from src.llm.openai_llm import OpenAILLM
from src.llm.doubao_llm import DouBaoLLM
from src.pipeline.rag_pipeline import RAGPipeline

# 文本相似度工具
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from bert_score import score as bert_score
import json

def load_medical_data(json_path):
    """加载医疗测试集JSON，返回问题、参考答案列表"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # 加载JSON文件
    
    # 提取问题（body）和参考答案（ideal_answer）
    questions = []
    references = []
    for item in data["questions"]:  # 你的JSON顶层是"questions"列表
        questions.append(item["body"])  # 问题文本
        # 取第一个理想答案作为参考（确保非空）
        if item["ideal_answer"]:
            references.append(item["ideal_answer"][0])
        else:
            references.append("")  # 处理空答案情况
    return questions, references

def evaluate_metrics(preds, refs):
    """计算 BLEU、ROUGE、BERTScore"""
    rouge = Rouge()
    bleu_scores = []
    rouge_scores = []
    all_preds = [p for p in preds]
    all_refs = [r for r in refs]
    
    for p, r in zip(all_preds, all_refs):
        # BLEU
        bleu_scores.append(sentence_bleu([r.split()], p.split()))
        # ROUGE
        rouge_res = rouge.get_scores(p, r)[0]
        rouge_scores.append(rouge_res)
    
    # BERTScore
    P, R, F1 = bert_score(all_preds, all_refs, lang="en", rescale_with_baseline=True)
    
    metrics = {
        "bleu_avg": sum(bleu_scores)/len(bleu_scores),
        "rouge_l_f1_avg": sum([r["rouge-l"]["f"] for r in rouge_scores])/len(rouge_scores),
        "bertscore_f1_avg": F1.mean().item()
    }
    return metrics

def main(args):
    # 1️⃣ 加载数据集
    questions, references = load_medical_data(args.data_path)  # 传入JSON路径，接收两个列表
    print(f"Loaded {len(questions)} medical questions")

    # 2️⃣ 加载文档库
    store = FaissStore.load(args.index_path, args.meta_path)
    embedder = Embedder(model_name=args.embed_model, device=args.device)

    # 3️⃣ 初始化 LLM
    if args.llm_provider == "openai":
        llm = OpenAILLM(model=args.llm_model, temperature=args.temperature)
    elif args.llm_provider == "doubao":
        llm = DouBaoLLM(model=args.llm_model)

    # 4️⃣ 初始化 RAG
    rag = RAGPipeline(store, embedder, llm, max_retrieval=args.max_retrieval)

    # 5️⃣ 批量测试
    preds_no_rag = []
    preds_rag = []

    for q in tqdm(questions, desc="Evaluating"):
        # 无 RAG
        prompt = f"Answer the following question:\n{q}"
        ans_no_rag = llm.generate(prompt)
        preds_no_rag.append(ans_no_rag)

        # 有 RAG
        resp = rag.answer(q)
        ans_rag = resp["answer"]
        preds_rag.append(ans_rag)

    # 6️⃣ 计算指标
    metrics_no_rag = evaluate_metrics(preds_no_rag, references)
    metrics_rag = evaluate_metrics(preds_rag, references)

    # 7️⃣ 输出结果
    print("\n=== Evaluation Results ===")
    print("No RAG:", metrics_no_rag)
    print("With RAG:", metrics_rag)

    # 8️⃣ 保存结果
    # 提取输出文件所在的目录路径
    output_dir = os.path.dirname(args.output_file)
    # 自动创建目录（包括所有不存在的父目录，exist_ok=True避免重复创建报错）
    os.makedirs(output_dir, exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        for q, no_rag, with_rag, ref in zip(questions, preds_no_rag, preds_rag, references):
            f.write(f"Q: {q}\nReference: {ref}\nNo RAG: {no_rag}\nWith RAG: {with_rag}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", help="医疗测试集JSON文件路径",default="data/raw/rag-mini-bioasq/test.json")
    parser.add_argument("--index-path", default="data/store/rag-mini-bioasq/faiss.index")
    parser.add_argument("--meta-path", default="data/store/rag-mini-bioasq/meta.pkl")
    parser.add_argument("--embed-model", default="all-MiniLM-L6-v2")
    parser.add_argument("--llm-provider", choices=["openai", "doubao"], default="doubao")
    parser.add_argument("--llm-model", default="doubao-1-5-lite-32k-250115")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-retrieval", type=int, default=5)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--output-file", default="log/rag-mini-bioasq/rag_experiment_results.txt")

    args = parser.parse_args()
    main(args)
