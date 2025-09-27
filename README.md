# LilRag

<div align="center">

<!-- Keep these links. Translations will automatically update with the README. -->
[Deutsch](https://zdoc.app/de/BV003/LilRag) | 
[English](https://zdoc.app/en/BV003/LilRag) | 
[Español](https://zdoc.app/es/BV003/LilRag) | 
[français](https://zdoc.app/fr/BV003/LilRag) | 
[日本語](https://zdoc.app/ja/BV003/LilRag) | 
[한국어](https://zdoc.app/ko/BV003/LilRag) | 
[Português](https://zdoc.app/pt/BV003/LilRag) | 
[Русский](https://zdoc.app/ru/BV003/LilRag) | 
[中文](https://zdoc.app/zh/BV003/LilRag)
</div>


### 🚀 Introduction

LilRAG is a lightweight Retrieval-Augmented Generation (RAG) framework designed for rapid experimentation and easy integration.  
It provides a simple interface to connect retrievers and large language models (LLMs), enabling developers to build intelligent applications that combine knowledge retrieval with generative reasoning.  

---

In LilRAG, users can define the core settings in config.yaml, including the document storage path, embedding model, FAISS vector store, and large language model (LLM) parameters.

The workflow begins by converting raw documents into dense vector representations using the all-MiniLM-L6-v2 embedding model. These vectors are then stored in FAISS, an efficient similarity search library.

When a query is issued, the RAG pipeline retrieves the most relevant vectors from the FAISS store and forwards them, along with the user’s query, to the selected LLM. The LLM integrates both the retrieved context and the query to generate an informed, context-aware answer.

This design ensures that the system not only relies on the LLM’s general knowledge but also grounds its responses in the user’s own document collection, making the answers both accurate and domain-specific.

---

- [Retrieval Augmented Generation](https://scriv.ai/guides/retrieval-augmented-generation-overview/)

### ✨ Features
- **Lightweight & Fast** — designed for rapid prototyping with minimal dependencies.  
- **Customizable Pipeline** — flexible components for building and extending RAG workflows.  


### 📂 Project Structure

```
LilRag/
├── data/                        # 原始文档（pdf, md, txt等）| Original documents (pdf, md, txt, etc.)
├── configs/                     # 配置文件（模型、数据库参数等）| Configuration files (model, database parameters, etc.)
│   ├── config.yaml
├── src/                         # 核心源码 | Core source code
│   ├── __init__.py
│   ├── embeddings/              # 向量化相关 | Embedding related
│   │   ├── __init__.py
│   │   └── embedder.py
│   ├── vectorstore/             # 向量数据库 | Vector database
│   │   ├── __init__.py
│   │   └── faiss_store.py
│   ├── retriever/               # 检索模块 | Retrieval module
│   │   ├── __init__.py
│   │   └── retriever.py
│   ├── llm/                     # 大模型调用（OpenAI / 本地模型）| LLM calls (OpenAI / local models)
│   │   ├── __init__.py
│   │   └── openai_llm.py
│   ├── pipeline/                # RAG 主流程 | RAG main workflow
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   └── utils/                   # 工具类 | Utility classes
│       ├── __init__.py
│       └── text_splitter.py
├── tests/                       # 单元测试 | Unit tests
│   └── test_pipeline.py
├── scripts/                     # 脚本（数据导入/构建向量库/运行demo）| Scripts (data import/build vector store/run demo)
│   ├── build_vectorstore.py
│   └── run_qa.py
├── requirements.txt             # Python依赖 | Python dependencies
├── README.md
└── .env                         # 存放API key（环境变量）| Store API keys (environment variables)
```





### ⚡ Quick Start

Clone the Repository

```
git clone https://github.com/BV003/LilRag.git
cd LilRag
```

Create and Activate Virtual Environment.
We recommend using conda for dependency management.

```
conda create -n lilrag python=3.10 -y
conda activate lilrag
```

Install Dependencies

```
pip install -r requirements.txt
```

Create a .env file in the project root directory and add your API Keys (e.g., OpenAI or other LLM providers) You can also use other models, as long as you implement the corresponding class under /llm.

```
OPENAI_API_KEY=your_api_key_here  //openai
ARK_API_KEY=your_api_key_here //doubao
```

Place your raw documents under the data/raw folder

```
data/raw/text
  ├── example.txt
  └── ...
```

Build the Vector Store

```
python scripts/build_vectorstore.py
```
This will read the files under data/raw and generate a vector index stored in:

```
data/store/
```

Run QA (Interactive)

```
python scripts/run_qa.py --query "什么是 RAG？"
```

### 🧪 Demo
I conducted a simple experiment.
I placed a test.json file under data/raw/rag-mini-bioasq, which contains 30 professional medical knowledge items.
A sample data item is as follows:
```
{
         "body": "Is Hirschsprung disease a mendelian or a multifactorial disorder?", 
         "documents": [
            "http://www.ncbi.nlm.nih.gov/pubmed/15858239", 
            "http://www.ncbi.nlm.nih.gov/pubmed/15829955", 
            "http://www.ncbi.nlm.nih.gov/pubmed/6650562", 
            "http://www.ncbi.nlm.nih.gov/pubmed/12239580", 
            "http://www.ncbi.nlm.nih.gov/pubmed/21995290", 
            "http://www.ncbi.nlm.nih.gov/pubmed/23001136", 
            "http://www.ncbi.nlm.nih.gov/pubmed/15617541", 
            "http://www.ncbi.nlm.nih.gov/pubmed/8896569", 
            "http://www.ncbi.nlm.nih.gov/pubmed/20598273"
         ], 
         "ideal_answer": [
            "Coding sequence mutations in RET, GDNF, EDNRB, EDN3, and SOX10 are involved in the development of Hirschsprung disease. The majority of these genes was shown to be related to Mendelian syndromic forms of Hirschsprung's disease, whereas the non-Mendelian inheritance of sporadic non-syndromic Hirschsprung disease proved to be complex; involvement of multiple loci was demonstrated in a multiplicative model."
         ], 
         "concepts": [
            "http://www.disease-ontology.org/api/metadata/DOID:10487", 
            "http://www.nlm.nih.gov/cgi/mesh/2015/MB_cgi?field=uid&exact=Find+Exact+Term&term=D006627", 
            "http://www.nlm.nih.gov/cgi/mesh/2015/MB_cgi?field=uid&exact=Find+Exact+Term&term=D020412", 
            "http://www.disease-ontology.org/api/metadata/DOID:11372"
         ], 
         "type": "summary", 
         "id": "55031181e9bde69634000014", 
         "snippets": [
            {
               "offsetInBeginSection": 131, 
               "offsetInEndSection": 358, 
               "text": "Hirschsprung disease (HSCR) is a multifactorial, non-mendelian disorder in which rare high-penetrance coding sequence mutations in the receptor tyrosine kinase RET contribute to risk in combination with mutations at other genes", 
               "beginSection": "abstract", 
               "document": "http://www.ncbi.nlm.nih.gov/pubmed/15829955", 
               "endSection": "abstract"
            }, 
            ......
         ]
      }, 
```

ran the following commands:
```
python scripts/build_vectorstore.py
python scripts/localtest.py
```

The results are as follows:
```
=== Evaluation Results ===
No RAG: {'bleu_avg': 0.021502071709305383, 'rouge_l_f1_avg': 0.19045467608115832, 'bertscore_f1_avg': 0.17610591650009155}
With RAG: {'bleu_avg': 0.09911253919776065, 'rouge_l_f1_avg': 0.2799770875273718, 'bertscore_f1_avg': 0.21979865431785583}
```
It is evident that RAG is effective.  
The experimental results were recorded under log/rag-mini-bioasq.

### 🔥 For Beginners

**This is an independent educational project, designed for learning and practice.**

If you are new to open source:
- Don’t worry! This project is meant to be beginner-friendly 
- You can start small (update README, add comments, fix small bugs) 
- You can build on top of this project, customize it, and even use it as part of your course assignments or personal practice projects.🤪

### 🎉 License
This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.