import json
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "2.2-vector_similarity_results.json"

DOCUMENTS = [
    {
        "id": "DOC-001",
        "text": "检验报告查询失败",
        "vector": [0.90, 0.10, 0.05],
    },
    {
        "id": "DOC-002",
        "text": "预约挂号流程说明",
        "vector": [0.10, 0.90, 0.10],
    },
    {
        "id": "DOC-003",
        "text": "药房处方打印故障",
        "vector": [0.05, 0.20, 0.90],
    },
]

QUERY = {
    "text": "检验结果为什么打不开",
    "vector": [0.95, 0.05, 0.05],
}


def cosine_similarity(left, right):
    dot_product = sum(a * b for a, b in zip(left, right))
    left_length = math.sqrt(sum(value * value for value in left))
    right_length = math.sqrt(sum(value * value for value in right))

    if left_length == 0 or right_length == 0:
        return 0.0

    return dot_product / (left_length * right_length)


ranked = []

for document in DOCUMENTS:
    score = cosine_similarity(QUERY["vector"], document["vector"])
    ranked.append(
        {
            "id": document["id"],
            "text": document["text"],
            "vector": document["vector"],
            "similarity": round(score, 4),
        }
    )

ranked.sort(key=lambda item: item["similarity"], reverse=True)

result = {
    "notice": "向量为教学示意值，不是实际 Embedding 模型输出。",
    "query": QUERY,
    "ranked_documents": ranked,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"问题：{QUERY['text']}")
print(f"问题示意向量：{QUERY['vector']}")
print("\n排序结果：")

for rank, item in enumerate(ranked, start=1):
    print(
        f"{rank}. [{item['id']}] {item['text']} "
        f"相似度={item['similarity']:.4f}"
    )

print(f"\n结果已保存到：{OUTPUT_PATH.name}")
