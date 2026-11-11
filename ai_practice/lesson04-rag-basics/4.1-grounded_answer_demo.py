import argparse
import json
import runpy
from pathlib import Path

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
COMMON_PATH = BASE_DIR / "2.1-retrieval_common.py"
KEY_PATH = BASE_DIR.parent / "key.txt"
PREVIEW_PATH = BASE_DIR / "3.1-grounded_prompt_preview.json"
ANSWER_PATH = BASE_DIR / "4.2-grounded_answer_smoke.json"

common = runpy.run_path(str(COMMON_PATH))
build_grounded_messages = common["build_grounded_messages"]
load_knowledge_data = common["load_knowledge_data"]
retrieve = common["retrieve"]

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

QUESTION = "门诊日报汇总数和明细数不一致，应该核对哪些内容？"


def collect_usage(response, finish_reason):
    usage = response.usage
    completion_details = getattr(usage, "completion_tokens_details", None)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    reasoning_tokens = int(
        getattr(completion_details, "reasoning_tokens", 0) or 0
    )

    return {
        "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
        "completion_tokens": completion_tokens,
        "reasoning_tokens": reasoning_tokens,
        "visible_completion_tokens": max(
            completion_tokens - reasoning_tokens,
            0,
        ),
        "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
        "prompt_cache_hit_tokens": int(
            getattr(usage, "prompt_cache_hit_tokens", 0) or 0
        ),
        "prompt_cache_miss_tokens": int(
            getattr(usage, "prompt_cache_miss_tokens", 0) or 0
        ),
        "finish_reason": finish_reason,
    }


def validate_answer(answer, retrieved_ids):
    required_keys = {
        "answer",
        "used_sources",
        "insufficient",
        "need_human_review",
    }
    missing_keys = required_keys - answer.keys()

    if missing_keys:
        raise ValueError(f"回答缺少必要字段：{sorted(missing_keys)}")

    invalid_sources = set(answer["used_sources"]) - set(retrieved_ids)
    if invalid_sources:
        raise ValueError(f"回答引用了未检索到的资料：{sorted(invalid_sources)}")


def main():
    parser = argparse.ArgumentParser(description="RAG grounded prompt 演示")
    parser.add_argument(
        "--call",
        action="store_true",
        help="调用一次模型；不传时只生成本地预览，不消耗 API token",
    )
    args = parser.parse_args()

    knowledge_data = load_knowledge_data()
    documents = knowledge_data["documents"]
    query_terms, retrieved_documents = retrieve(QUESTION, documents)
    messages = build_grounded_messages(QUESTION, retrieved_documents)
    retrieved_ids = [document["id"] for _, document in retrieved_documents]

    preview = {
        "question": QUESTION,
        "query_terms": query_terms,
        "retrieved_ids": retrieved_ids,
        "messages": messages,
    }

    with open(PREVIEW_PATH, "w", encoding="utf-8") as f:
        json.dump(preview, f, ensure_ascii=False, indent=2)

    print(f"检索词：{query_terms}")
    print(f"召回资料：{retrieved_ids}")
    print("\nSystem：")
    print(messages[0]["content"])
    print("\nUser：")
    print(messages[1]["content"])

    if not args.call:
        print(f"\n仅生成本地预览，未调用模型：{PREVIEW_PATH.name}")
        return

    with open(KEY_PATH, encoding="utf-8") as f:
        api_key = f.read().strip()

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=4000,
    )

    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    if not content:
        raise RuntimeError(
            f"模型返回空内容，finish_reason={finish_reason}"
        )

    answer = json.loads(content)
    validate_answer(answer, retrieved_ids)
    usage = collect_usage(response, finish_reason)

    result = {
        "question": QUESTION,
        "retrieved_ids": retrieved_ids,
        "answer": answer,
        "usage": usage,
    }

    with open(ANSWER_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n模型回答：")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
