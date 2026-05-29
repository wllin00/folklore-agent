import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from langchain_classic.chains import RetrievalQA

load_dotenv()

# 配置
persist_dir = "./chroma_db"
model_name = "BAAI/bge-small-zh-v1.5"  # 如果本地有模型可改路径
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# 加载向量库
vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# 初始化大模型（使用 DeepSeek）
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com",
    temperature=0.3
)

# 创建检索问答链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("非遗文化解说员已启动（输入 quit 退出）")
while True:
    query = input("\n你: ")
    if query.lower() == "quit":
        break
    result = qa_chain.invoke({"query": query})
    print(f"\nBot: {result['result']}")
    # 可选打印来源
    # for doc in result['source_documents']:
    #     print(f"来源: {doc.metadata.get('source', '未知')}")