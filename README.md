# RAG

### 项目代码结构

```
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
```



### 运行流程

激活虚拟环境并设置 Key放在 .env




构建向量库
```
python scripts/build_vectorstore.py
```


运行 QA（交互式）
```
python scripts/run_qa.py --query "什么是 RAG？"
```

### 调参与扩展建议

chunk size：max_chars 和 overlap 根据文档类型调整（长文档建议 800–1200，较短可 400）

reranker：检索后可用 cross-encoder reranker（例如 sentence-transformers 的 cross-encoder）对 top-k 重新排序

混合检索：BM25 + vector hybrid 对事实性查询更稳

持久化：上面把 metadata 用 pickle 保存；生产可以改成 sqlite 或向量 DB（Milvus/Pinecone/Weaviate）