import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "1.1-rag_knowledge.json"

KEYWORDS = [
    "门诊",
    "叫号",
    "大屏",
    "黑屏",
    "接口",
    "超时",
    "病历",
    "保存",
    "账号",
    "权限",
    "登录",
    "排班",
    "护士",
    "医生",
    "打印机",
    "处方",
    "药房",
    "检验",
    "报告",
    "数据库",
    "变更",
    "日报",
    "报表",
    "明细",
    "汇总",
    "电脑",
    "内网",
    "网络",
    "录入",
]


def normalize(text):
    return re.sub(r"\s+", "", text).lower()


def load_knowledge_data(path=DEFAULT_DATA_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_query_terms(question):
    normalized_question = normalize(question)
    return [keyword for keyword in KEYWORDS if keyword in normalized_question]


def score_document(query_terms, document):
    title = normalize(document["title"])
    text = normalize(document["text"])

    return sum(
        title.count(term) * 4 + text.count(term)
        for term in query_terms
    )


def retrieve(question, documents, top_k=3):
    query_terms = extract_query_terms(question)
    ranked = []

    for document in documents:
        score = score_document(query_terms, document)
        if score > 0:
            ranked.append((score, document))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return query_terms, ranked[:top_k]


def build_grounded_messages(question, retrieved_documents):
    context_parts = []

    for _, document in retrieved_documents:
        context_parts.append(
            f"[{document['id']}] {document['title']}\n"
            f"{document['text']}"
        )

    context = "\n\n".join(context_parts) if context_parts else "没有检索到资料"

    system_prompt = """
你是医院信息科的 RAG 问答助手。

规则：
1. 只能根据用户提供的参考资料回答。
2. 不得补充参考资料中没有的院内制度、数据或处理结果。
3. used_sources 只能填写参考资料中真实出现的编号。
4. 如果资料不足，answer 必须说明“现有资料不足，需要人工核实”，
   insufficient 为 true，used_sources 保持为空。
5. 涉及患者安全时，need_human_review 必须为 true。
6. 只输出 JSON，不要输出 Markdown 代码块或额外解释。

JSON 格式：
{
  "answer": "根据资料整理的回答",
  "used_sources": ["KB-001"],
  "insufficient": false,
  "need_human_review": false
}
""".strip()

    user_prompt = f"""
参考资料：
{context}

问题：
{question}
""".strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
