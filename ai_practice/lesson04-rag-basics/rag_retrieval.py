import json
import re
from pathlib import Path


DATA_PATH = Path(__file__).with_name("rag_knowledge.json")
RESULT_PATH = Path(__file__).with_name("rag_retrieval_results.json")

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
]

TEST_QUESTIONS = [
    "医生保存病历时接口超时，当前无法保存，应该怎么处理？",
    "门诊叫号大屏黑屏，但诊室电脑正常，按什么级别处理？",
    "新入职护士无法登录，也看不到自己的排班，怎么办？",
    "药房打印机无法打印处方，涉及患者用药时需要做什么？",
    "门诊日报汇总数和明细数不一致，应该核对哪些内容？",
]


def normalize(text):
    return re.sub(r"\s+", "", text).lower()


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


def build_grounded_prompt(question, retrieved_documents):
    context_parts = []

    for score, document in retrieved_documents:
        context_parts.append(
            f"[{document['id']}] {document['title']}\n"
            f"{document['text']}\n"
            f"检索分数：{score}"
        )

    context = "\n\n".join(context_parts) if context_parts else "没有检索到资料"

    system_prompt = """
你是医院信息科问答助手。
只能根据提供的参考资料回答。
如果资料不足，必须回答“现有资料不足，需要人工核实”。
回答中要保留资料编号，不能补充资料中没有的院内制度。
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


with open(DATA_PATH, encoding="utf-8") as f:
    knowledge_data = json.load(f)

documents = knowledge_data["documents"]
results = []

print(knowledge_data["notice"])
print(f"知识库文档数量：{len(documents)}")

for question in TEST_QUESTIONS:
    query_terms, retrieved_documents = retrieve(question, documents)
    grounded_messages = build_grounded_prompt(question, retrieved_documents)

    result = {
        "question": question,
        "query_terms": query_terms,
        "retrieved": [
            {
                "id": document["id"],
                "title": document["title"],
                "score": score,
            }
            for score, document in retrieved_documents
        ],
        "grounded_prompt": grounded_messages,
    }
    results.append(result)

    print("\n" + "=" * 60)
    print(f"问题：{question}")
    print(f"提取关键词：{query_terms}")

    if not retrieved_documents:
        print("没有检索到资料")
        continue

    for rank, (score, document) in enumerate(retrieved_documents, start=1):
        print(
            f"{rank}. [{document['id']}] {document['title']} "
            f"检索分数={score}"
        )

    print("已生成带资料编号的提示词，但本实验不调用大模型。")

with open(RESULT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n检索结果已保存到：{RESULT_PATH.name}")
