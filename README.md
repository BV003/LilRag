# LilRag

### 🚀 Introduction

LilRAG is a lightweight Retrieval-Augmented Generation (RAG) framework designed for rapid experimentation and easy integration.  
It provides a simple interface to connect retrievers and large language models (LLMs), enabling developers to build intelligent applications that combine knowledge retrieval with generative reasoning.  

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

激活虚拟环境并设置 Key放在 .env




构建向量库
```
python scripts/build_vectorstore.py
```


运行 QA（交互式）
```
python scripts/run_qa.py --query "什么是 RAG？"


```

### 🧪 Demo


### 🔥 For Beginners

**This is an independent educational project, designed for learning and practice.**

If you are new to open source:
- Don’t worry! This project is meant to be beginner-friendly 
- You can start small (update README, add comments, fix small bugs) 
- You can build on top of this project, customize it, and even use it as part of your course assignments or personal practice projects.🤪

### 🎉 License
This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.