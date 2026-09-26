import json

from openai import OpenAI

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

system_prompt = """
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

examples = [
    (
        "门诊叫号大屏黑屏，但诊室电脑和叫号声音正常。",
        '{"category":"终端与外设","priority":"P2","reason":"仅叫号大屏异常，诊室业务仍可运行","need_human_review":false}',
    ),
    (
        "医生保存病历时提示接口超时，当前无法完成保存。",
        '{"category":"接口与集成","priority":"P1","reason":"病历保存受阻，可能影响门诊连续诊疗","need_human_review":true}',
    ),
    (
        "护士希望新增护理记录批量导出字段，目前没有故障。",
        '{"category":"需求与流程","priority":"P3","reason":"属于新需求，不是现网故障","need_human_review":false}',
    ),
    (
        "新入职医生登录系统后看不到自己的排班，其他医生正常。",
        '{"category":"账号与权限","priority":"P2","reason":"仅该医生账号异常，其他医生正常","need_human_review":false}',
),
]

new_ticket =input('请输入新工单内容： ')   #"新入职护士无法登录移动护理系统，同科室其他护士可以正常登录。"

messages = [{"role": "system", "content": system_prompt}]

for example_input, example_output in examples:
    messages.append({"role": "user", "content": f"工单：{example_input}"})
    messages.append({"role": "assistant", "content": example_output})

messages.append(
    {
        "role": "user",
        "content": f"请分类下面这张新工单，并只输出 json：\n工单：{new_ticket}",
    }
)

for attempt in range(1, 4):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
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
    raise RuntimeError("连续 3 次未返回 JSON 内容")

data = json.loads(content)

required_keys = {"category", "priority", "reason", "need_human_review"}
missing_keys = required_keys - data.keys()

if missing_keys:
    raise ValueError(f"JSON 缺少必要字段：{sorted(missing_keys)}")

allowed_categories = {
    "终端与外设",
    "网络与通信",
    "账号与权限",
    "业务系统",
    "接口与集成",
    "数据与报表",
    "需求与流程",
}
allowed_priorities = {"P1", "P2", "P3"}

if data["category"] not in allowed_categories:
    raise ValueError(f"非法 category：{data['category']}")

if data["priority"] not in allowed_priorities:
    raise ValueError(f"非法 priority：{data['priority']}")

print("新工单：")
print(new_ticket)
print("\n模型返回的原始 JSON：")
print(content)
print("\n解析并校验后的结果：")
print(json.dumps(data, ensure_ascii=False, indent=2))
