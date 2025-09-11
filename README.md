# RAG

## 项目代码结构

rag-baseline/
├── data/                        # 原始文档（pdf, md, txt等）
├── configs/                     # 配置文件（模型、数据库参数等）
│   ├── config.yaml
├── src/                         # 核心源码
│   ├── __init__.py
│   ├── embeddings/              # 向量化相关
│   │   ├── __init__.py
│   │   └── embedder.py
│   ├── vectorstore/             # 向量数据库
│   │   ├── __init__.py
│   │   └── faiss_store.py
│   ├── retriever/               # 检索模块
│   │   ├── __init__.py
│   │   └── retriever.py
│   ├── llm/                     # 大模型调用（OpenAI / 本地模型）
│   │   ├── __init__.py
│   │   └── openai_llm.py
│   ├── pipeline/                # RAG 主流程
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   └── utils/                   # 工具类
│       ├── __init__.py
│       └── text_splitter.py
├── tests/                       # 单元测试
│   └── test_pipeline.py
├── scripts/                     # 脚本（数据导入/构建向量库/运行demo）
│   ├── build_vectorstore.py
│   └── run_qa.py
├── requirements.txt             # Python依赖
├── README.md
└── .env                         # 存放API key（环境变量）
