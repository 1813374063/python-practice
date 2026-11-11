import json
import runpy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COMMON_PATH = BASE_DIR / "2.1-retrieval_common.py"
RESULT_PATH = BASE_DIR / "2.3-rag_retrieval_results.json"

common = runpy.run_path(str(COMMON_PATH))
build_grounded_messages = common["build_grounded_messages"]
load_knowledge_data = common["load_knowledge_data"]
retrieve = common["retrieve"]

TEST_QUESTIONS = [
    "医生保存病历时接口超时，当前无法保存，应该怎么处理？",
    "门诊叫号大屏黑屏，但诊室电脑正常，按什么级别处理？",
    "新入职护士无法登录，也看不到自己的排班，怎么办？",
    "药房打印机无法打印处方，涉及患者用药时需要做什么？",
    "门诊日报汇总数和明细数不一致，应该核对哪些内容？",
]


def main():
    knowledge_data = load_knowledge_data()
    documents = knowledge_data["documents"]
    results = []

    print(knowledge_data["notice"])
    print(f"知识库文档数量：{len(documents)}")

    for question in TEST_QUESTIONS:
        query_terms, retrieved_documents = retrieve(question, documents)
        grounded_messages = build_grounded_messages(
            question,
            retrieved_documents,
        )

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
            "grounded_messages": grounded_messages,
        }
        results.append(result)

        print("\n" + "=" * 60)
        print(f"问题：{question}")
        print(f"提取关键词：{query_terms}")

        if not retrieved_documents:
            print("没有检索到资料")
            continue

        for rank, (score, document) in enumerate(
            retrieved_documents,
            start=1,
        ):
            print(
                f"{rank}. [{document['id']}] {document['title']} "
                f"检索分数={score}"
            )

        print("已生成带资料编号的提示词，但本实验不调用大模型。")

    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n检索结果已保存到：{RESULT_PATH.name}")


if __name__ == "__main__":
    main()
