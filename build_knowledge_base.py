import os
# ========== 关键：设置镜像地址（必须在导入 sentence_transformers 之前）==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# ============================================================================

import pickle
from glob import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# 配置路径
MANUAL_TEXTS_DIR = "data/texts"
PARSED_PKL_PATH = "data/parsed_projects.pkl"

# 1. 加载手工文本
manual_docs = []
if os.path.exists(MANUAL_TEXTS_DIR):
    for file_path in glob(os.path.join(MANUAL_TEXTS_DIR, "*.txt")):
        loader = TextLoader(file_path, encoding='utf-8')
        manual_docs.extend(loader.load())
    print(f"已加载手工文本：{len(manual_docs)} 个文件")
else:
    print("警告：手工文本目录 data/texts 不存在，跳过。")

# 2. 加载解析的结构化项目
parsed_docs = []
if os.path.exists(PARSED_PKL_PATH):
    with open(PARSED_PKL_PATH, "rb") as f:
        parsed_docs = pickle.load(f)
    print(f"已加载结构化项目：{len(parsed_docs)} 条")
else:
    print("警告：parsed_projects.pkl 不存在，请先运行 parse_nodes.py")

all_docs = manual_docs + parsed_docs
print(f"总文档数：{len(all_docs)}")

# 3. 切分文本
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(all_docs)
print(f"切分后块数：{len(docs)}")

# 4. 向量化（使用镜像自动下载模型）
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

# 5. 构建向量库
vectordb = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
vectordb.persist()

print("知识库构建完成！")