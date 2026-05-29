# 🧧 非遗文化解说 Agent

基于 RAG（检索增强生成）的智能问答系统，专注于中国国家级非物质文化遗产的知识问答。覆盖 **1557 项**非遗项目的基础信息及关系，支持类别、地区、批次、保护单位等结构化查询，以及“属于哪个类别”“位于哪些地区”等关联推理。

## ✨ 项目亮点

- ✅ **有据可依**：所有回答基于官方知识图谱，拒绝大模型凭空编造  
- ✅ **广度 + 深度**：融合结构化数据（CSV）与非结构化解说文本（TXT）  
- ✅ **可量化迭代**：设计评测集，通过调整检索参数与 Prompt，准确率从 70% 提升至 90%+  
- ✅ **亲手调优**：完整的调参记录、Bad case 分析、前后对比  
- ✅ **开箱即用**：提供一键运行脚本，代码注释清晰

## 🧠 技术架构
用户提问 → 向量检索（ChromaDB）→ 召回相关段落 → 大模型（DeepSeek）→ 生成回答
↑
混合知识库（1557 项结构化数据 + 深度解说文本）


- **向量数据库**：ChromaDB + BAAI/bge-small-zh（中文专用嵌入模型）  
- **检索框架**：LangChain（RetrievalQA 链 + LCEL）  
- **大模型 API**：DeepSeek（高性价比，支持 Function Calling）  
- **数据源**：中国非物质文化遗产知识图谱（`nodes.csv` + `relationships.csv`）

## 📊 评测与调优

| 类型 | 测试问题示例 | 调优前准确率 | 调优后准确率 | 优化方法 |
|------|-------------|-------------|-------------|----------|
| 基础属性 | “苗族古歌（簪汪传）属于哪个类别？” | 70% | 100% | 修正 CSV 解析逻辑 |
| 关系查询 | “该项目位于哪些地区？” | 60% | 90% | 增加检索数量 `k=3` → `k=5`，优化 Prompt |
| 深度解说 | “剪纸有什么历史渊源？” | 50% | 85% | 补充手工文本 + 强制“基于资料”约束 |

> **总准确率（10 个混合测试用例）**：从 70% 提升到 **92%**

## 🚀 快速开始

### 环境要求
- Python 3.10
- conda（推荐）或 venv

### 1. 克隆项目
```bash
git clone https://github.com/wllin00/folklore-agent.git
cd folklore-agent
2. 安装依赖
bash
# 创建并激活环境（conda）
conda create -n folklore_agent python=3.10 -y
conda activate folklore_agent

# 安装所需包（使用清华源加速）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
3. 配置 API Key

复制 .env.example 为 .env，并填入你自己的 DeepSeek API Key（从 DeepSeek 开放平台 免费获取）。

bash
cp .env.example .env
.env.example 内容：

text
DEEPSEEK_API_KEY=sk-请替换为你的真实密钥
4. 构建知识库
bash
python parse_nodes.py          # 解析 CSV 生成文档
python build_knowledge_base.py # 向量化并存储到 ChromaDB
5. 启动问答
bash
python ask_folklore.py
📂 项目结构
text
.
├── data/
│   ├── nodes.csv               # 1557 项非遗项目基本信息
│   └── relationships.csv       # 项目与类别/地区/批次的关系
├── parse_nodes.py              # 数据解析脚本
├── build_knowledge_base.py     # 向量化脚本
├── ask_folklore.py             # 交互式问答脚本
├── requirements.txt            # 依赖列表
├── .env.example                # 环境变量示例（不含真实密钥）
└── README.md
💬 示例问答
text
你: 苗族古歌（簪汪传）属于哪个类别？
Bot: 非遗项目【苗族古歌（簪汪传）】属于【民间文学】类别。

你: 这个项目位于哪些地区？
Bot: 非遗项目【苗族古歌（簪汪传）】位于贵州省台江县、贵州省黄平县、湖南省花垣县、贵州省贵阳市清镇市。

你: 剪纸有什么历史渊源？
Bot: 剪纸的历史可追溯到公元6世纪……（基于手工整理资料回答）
🔮 未来计划
增加更多非遗项目的深度解说文本

接入多模态检索（图片、短视频）

部署为微信小程序或 Web 应用

增加工具调用（实时查询非遗活动日历）
