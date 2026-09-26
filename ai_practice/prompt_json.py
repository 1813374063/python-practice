import json

from openai import OpenAI

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

issue = """
门诊医生反馈系统很慢，但同岗位的护士说操作正常。
目前只知道问题发生在上午门诊高峰，医生使用 3 号诊室电脑，
具体慢在哪个操作、耗时多少、是否影响其他医生都还没有确认。
""".strip()

system_prompt = """
你是一名医疗信息化现场问题分析助手。

请把用户提供的问题信息整理成 JSON 对象。
只输出 JSON，不要输出 Markdown 代码块，不要增加解释文字。

JSON 必须包含以下字段，格式如下：
{
  "issue": "用一句话概括问题，不添加原文没有的事实",
  "confirmed_facts": ["只写用户明确提供的事实"],
  "unconfirmed": ["列出需要现场核实的信息"],
  "actions": [
    {
      "priority": 1,
      "action": "排查动作",
      "evidence": ["需要收集的证据"],
      "escalation_condition": "满足什么条件需要升级"
    }
  ],
  "contains_sensitive_data": false
}

示例输入：
门诊护士反馈打印处方慢，目前只知道使用 2 号电脑。

示例 JSON 输出：
{
  "issue": "门诊护士反馈处方打印慢",
  "confirmed_facts": ["使用 2 号电脑"],
  "unconfirmed": ["是否所有电脑都慢", "具体耗时"],
  "actions": [
    {
      "priority": 1,
      "action": "现场计时复现",
      "evidence": ["操作时间和耗时"],
      "escalation_condition": "多台电脑均可复现"
    }
  ],
  "contains_sensitive_data": false
}

约束：
1. confirmed_facts 只能来自用户原文。
2. unconfirmed 用于存放推测和尚未确认的信息。
3. actions 最多返回 3 项，并按优先级排序。
4. 不得编造医院内部制度、日志、患者数据或处理结果。
5. 如果用户原文涉及患者姓名、证件号、病历号、手机号等敏感信息，
   contains_sensitive_data 必须为 true。
""".strip()

for attempt in range(1, 4):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析下面的问题，并输出 json：\n{issue}"},
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=4000,
    )

    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    if content:
        break

    print(f"第 {attempt} 次请求返回空内容，finish_reason={finish_reason}")
else:
    raise RuntimeError("连续 3 次未返回 JSON 内容，请检查 max_tokens 或调整提示词")

print("模型原始输出：")
print(content)

try:
    data = json.loads(content)
except json.JSONDecodeError as exc:
    raise ValueError(f"模型没有返回合法 JSON：{exc}") from exc

required_keys = {
    "issue",
    "confirmed_facts",
    "unconfirmed",
    "actions",
    "contains_sensitive_data",
}
missing_keys = required_keys - data.keys()

if missing_keys:
    raise ValueError(f"JSON 缺少必要字段：{sorted(missing_keys)}")

print("\n解析后的 Python 字典：")
print(json.dumps(data, ensure_ascii=False, indent=2))
