import json
import sys
import time
from pathlib import Path

from openai import OpenAI

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

KEY_PATH = Path(__file__).resolve().parents[1] / "key.txt"

with open(KEY_PATH, encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

SYSTEM_PROMPT = """
你是医院信息科的工单分类助手。

请把工单分类为一个固定类别和一个优先级，并输出 JSON。

category 只能选择：
- 终端与外设
- 网络与通信
- 账号与权限
- 业务系统
- 接口与集成
- 数据与报表
- 需求与流程

priority 只能选择：
- P1：影响关键诊疗，且没有替代方案
- P2：影响单点或单岗位，但有替代方案
- P3：需求、咨询或低影响问题

JSON 格式：
{
  "category": "固定类别",
  "priority": "P1、P2 或 P3",
  "reason": "分类和定级依据",
  "need_human_review": false
}

当信息不足、无法可靠判断或可能涉及患者安全时，
need_human_review 必须为 true。

只输出 JSON，不要输出 Markdown 代码块或额外解释。
""".strip()

EXAMPLES = [
    (
        "门诊叫号大屏黑屏，但诊室电脑和叫号声音正常。",
        {"category": "终端与外设", "priority": "P2"},
    ),
    (
        "医生保存病历时提示接口超时，当前无法完成保存。",
        {"category": "接口与集成", "priority": "P1"},
    ),
    (
        "护士希望新增护理记录批量导出字段，目前没有故障。",
        {"category": "需求与流程", "priority": "P3"},
    ),
]

TEST_CASES = [
    {
        "ticket": "门诊叫号大屏黑屏，但诊室电脑和叫号声音正常。",
        "expected_category": "终端与外设",
        "expected_priority": "P2",
    },
    {
        "ticket": "新入职医生登录系统后看不到自己的排班，其他医生正常。",
        "expected_category": "账号与权限",
        "expected_priority": "P2",
    },
    {
        "ticket": "医生保存病历时提示第三方接口超时，当前无法完成保存。",
        "expected_category": "接口与集成",
        "expected_priority": "P1",
    },
    {
        "ticket": "护理部要求新增三个护理记录导出字段，目前没有故障。",
        "expected_category": "需求与流程",
        "expected_priority": "P3",
    },
    {
        "ticket": "门诊日报汇总数与明细数不一致，需要核对统计结果。",
        "expected_category": "数据与报表",
        "expected_priority": "P2",
    },
    {
        "ticket": "部分科室无法查询当日检验报告，检验接口返回超时。",
        "expected_category": "接口与集成",
        "expected_priority": "P1",
    },
    {
        "ticket": "新入职护士无法登录移动护理系统，同科室其他护士正常。",
        "expected_category": "账号与权限",
        "expected_priority": "P2",
    },
    {
        "ticket": "体检中心新电脑无法连接内网，其他电脑可以正常访问。",
        "expected_category": "网络与通信",
        "expected_priority": "P2",
    },
]

ALLOWED_CATEGORIES = {
    "终端与外设",
    "网络与通信",
    "账号与权限",
    "业务系统",
    "接口与集成",
    "数据与报表",
    "需求与流程",
}

ALLOWED_PRIORITIES = {"P1", "P2", "P3"}

EVALUATION_MODES = {
    "smoke": {
        "label": "冒烟测试",
        "indexes": [2],
    },
    "fast": {
        "label": "快速测试，覆盖接口、终端和账号问题",
        "indexes": [0, 2, 6],
    },
    "full": {
        "label": "完整测试",
        "indexes": list(range(len(TEST_CASES))),
    },
}


def get_usage_value(usage, name):
    return int(getattr(usage, name, 0) or 0)


def collect_usage(response, finish_reason):
    usage = response.usage
    completion_details = getattr(usage, "completion_tokens_details", None)

    prompt_tokens = get_usage_value(usage, "prompt_tokens")
    completion_tokens = get_usage_value(usage, "completion_tokens")
    reasoning_tokens = int(
        getattr(completion_details, "reasoning_tokens", 0) or 0
    )

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "reasoning_tokens": reasoning_tokens,
        "visible_completion_tokens": max(
            completion_tokens - reasoning_tokens,
            0,
        ),
        "total_tokens": get_usage_value(usage, "total_tokens"),
        "prompt_cache_hit_tokens": get_usage_value(
            usage,
            "prompt_cache_hit_tokens",
        ),
        "prompt_cache_miss_tokens": get_usage_value(
            usage,
            "prompt_cache_miss_tokens",
        ),
        "finish_reason": finish_reason,
    }


def build_messages(ticket):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for example_input, example_result in EXAMPLES:
        messages.append({"role": "user", "content": f"工单：{example_input}"})
        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(example_result, ensure_ascii=False),  #  python 字典转 json 字符串
            }
        )

    messages.append(
        {
            "role": "user",
            "content": f"请分类下面这张新工单，并只输出 json：\n工单：{ticket}",
        }
    )

    return messages


def call_model(messages):
    for attempt in range(1, 4):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=4000,
        )

        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason

        if content:  #这次模型返回的内容是不是有效的非空内容
            json_result = json.loads(content)  # json字符串转python字典
            return json_result, collect_usage(
                response,
                finish_reason,
            )

        if finish_reason == "length":
            raise RuntimeError(
                "达到 max_tokens 或上下文长度上限，原样重试不会解决，"
                "请先调大 max_tokens、关闭 thinking 或精简提示词"
            )

        print(f"第 {attempt} 次请求返回空内容，finish_reason={finish_reason}")

    raise RuntimeError("连续 3 次未返回 JSON 内容")


def validate_result(result):
    required_keys = {"category", "priority", "reason", "need_human_review"}
    missing_keys = required_keys - result.keys()

    if missing_keys:
        raise ValueError(f"JSON 缺少必要字段：{sorted(missing_keys)}")

    if result["category"] not in ALLOWED_CATEGORIES:
        raise ValueError(f"非法 category：{result['category']}")

    if result["priority"] not in ALLOWED_PRIORITIES:
        raise ValueError(f"非法 priority：{result['priority']}")


if len(sys.argv) != 2 or sys.argv[1].lower() not in EVALUATION_MODES:
    print("请选择评估模式：")
    print("  python prompt_eval.py smoke   # 1 条工单")
    print("  python prompt_eval.py fast    # 3 条代表性工单")
    print("  python prompt_eval.py full    # 8 条完整测试")
    raise SystemExit(0)

mode_name = sys.argv[1].lower()
mode = EVALUATION_MODES[mode_name]
selected_cases = [TEST_CASES[index] for index in mode["indexes"]]

evaluation_results = []
total_started_at = time.perf_counter()

for index, case in enumerate(selected_cases, start=1):
    started_at = time.perf_counter()
    messages = build_messages(case["ticket"])

    try:
        result, usage_info = call_model(messages)
        validate_result(result)
        elapsed_seconds = round(time.perf_counter() - started_at, 2)

        category_correct = result["category"] == case["expected_category"]
        priority_correct = result["priority"] == case["expected_priority"]

        evaluation_results.append(
            {
                "index": index,
                "ticket": case["ticket"],
                "expected_category": case["expected_category"],
                "actual_category": result["category"],
                "expected_priority": case["expected_priority"],
                "actual_priority": result["priority"],
                "category_correct": category_correct,
                "priority_correct": priority_correct,
                "reason": result["reason"],
                "need_human_review": result["need_human_review"],
                "elapsed_seconds": elapsed_seconds,
                "usage": usage_info,
            }
        )

        print(
            f"[{index}/{len(selected_cases)}] "
            f"类别={'正确' if category_correct else '错误'} "
            f"优先级={'正确' if priority_correct else '错误'} "
            f"耗时={elapsed_seconds}s "
            f"tokens={usage_info['total_tokens']} "
            f"推理tokens={usage_info['reasoning_tokens']}"
        )
    except Exception as exc:
        evaluation_results.append(
            {
                "index": index,
                "ticket": case["ticket"],
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        print(
            f"[{index}/{len(selected_cases)}] 执行失败："
            f"{type(exc).__name__}: {exc}"
        )

completed_results = [
    item for item in evaluation_results if "error" not in item
]

category_correct_count = sum(
    item["category_correct"] for item in completed_results
)
priority_correct_count = sum(
    item["priority_correct"] for item in completed_results
)

summary = {
    "mode": mode_name,
    "mode_label": mode["label"],
    "total_cases": len(selected_cases),
    "completed_cases": len(completed_results),
    "failed_cases": len(selected_cases) - len(completed_results),
    "category_correct": category_correct_count,
    "priority_correct": priority_correct_count,
    "category_accuracy": round(
        category_correct_count / len(selected_cases),
        4,
    ),
    "priority_accuracy": round(
        priority_correct_count / len(selected_cases),
        4,
    ),
    "elapsed_seconds_total": round(
        time.perf_counter() - total_started_at,
        2,
    ),
    "usage_totals": {
        "prompt_tokens": sum(
            item["usage"]["prompt_tokens"] for item in completed_results
        ),
        "completion_tokens": sum(
            item["usage"]["completion_tokens"] for item in completed_results
        ),
        "reasoning_tokens": sum(
            item["usage"]["reasoning_tokens"] for item in completed_results
        ),
        "visible_completion_tokens": sum(
            item["usage"]["visible_completion_tokens"]
            for item in completed_results
        ),
        "total_tokens": sum(
            item["usage"]["total_tokens"] for item in completed_results
        ),
        "prompt_cache_hit_tokens": sum(
            item["usage"]["prompt_cache_hit_tokens"]
            for item in completed_results
        ),
        "prompt_cache_miss_tokens": sum(
            item["usage"]["prompt_cache_miss_tokens"]
            for item in completed_results
        ),
    },
    "results": evaluation_results,
}

output_paths = {
    "smoke": Path(__file__).resolve().parent
    / "4.3-prompt_eval_results_smoke.json",
    "fast": Path(__file__).resolve().parent
    / "4.4-prompt_eval_results_fast.json",
    "full": Path(__file__).resolve().parent
    / "4.5-prompt_eval_results_full.json",
}
output_path = output_paths[mode_name]

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("\n评估汇总：")
print(json.dumps(summary, ensure_ascii=False, indent=2))
