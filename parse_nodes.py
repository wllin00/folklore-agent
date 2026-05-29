import re
import pandas as pd
import pickle
from langchain_core.documents import Document

# 文件路径
NODES_CSV = "data/nodes.csv"
REL_CSV = "data/relationships.csv"
OUTPUT_PKL = "data/parsed_projects.pkl"

def parse_node_line(line):
    """解析类似 '(:非遗项目 {name: xxx, category: xxx, ...})' 的文本"""
    match = re.search(r'{([^}]+)}', line)
    if not match:
        return None
    content = match.group(1)
    pairs = re.findall(r'(\w+):\s*(.+?)(?=,\s*\w+:|$)', content)
    d = {}
    for k, v in pairs:
        d[k.strip()] = v.strip()
    return d

# ---------- 1. 解析 nodes.csv ----------
df_nodes = pd.read_csv(NODES_CSV)
node_docs = []
for idx, row in df_nodes.iterrows():
    line = row['n']
    if not line.startswith('(:非遗项目'):
        continue
    data = parse_node_line(line)
    if not data:
        continue
    name = data.get('name', '未知项目')
    category = data.get('category', '未知类别')
    region = data.get('region', '未知地区')
    batch = data.get('batch', '未知批次')
    protection_unit = data.get('protection_unit', '未知保护单位')
    
    text = f"非遗项目【{name}】，类别为{category}，位于{region}，{batch}被列入国家级非物质文化遗产，保护单位为{protection_unit}。"
    node_docs.append(Document(page_content=text, metadata={"source": "nodes", "name": name}))
print(f"解析节点文档：{len(node_docs)} 条")

# ---------- 2. 解析 relationships.csv ----------
df_rel = pd.read_csv(REL_CSV)
relation_docs = []
# 先查看列名（根据实际输出调整）
print("relationships.csv 列名：", df_rel.columns.tolist())
# 假设列名为 ['source', 'target', 'type']，如果不是请按实际修改
for _, row in df_rel.iterrows():
    src = str(row.get('source', ''))
    tgt = str(row.get('target', ''))
    rel_type = str(row.get('type', ''))
    
    if rel_type == 'hasInheritor':
        text = f"非遗项目【{src}】的代表性传承人是【{tgt}】。"
    elif rel_type == 'belongsToCategory':
        text = f"非遗项目【{src}】属于【{tgt}】类别。"
    elif rel_type == 'locatedInRegion':
        text = f"非遗项目【{src}】位于【{tgt}】。"
    else:
        # 其他关系类型可自行扩展
        continue
    relation_docs.append(Document(page_content=text, metadata={"source": "relationships", "type": rel_type}))
print(f"解析关系文档：{len(relation_docs)} 条")

# 3. 合并所有文档
all_docs = node_docs + relation_docs
print(f"总文档数：{len(all_docs)}")

# 4. 保存为 pkl
with open(OUTPUT_PKL, 'wb') as f:
    pickle.dump(all_docs, f)
print(f"已保存到 {OUTPUT_PKL}")