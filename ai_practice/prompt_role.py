from openai import OpenAI

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

question = (
    "门诊医生反馈系统很慢，但同岗位的护士说操作正常。"
    "作为现场实施人员，下一步应该怎么排查？"
)

weak_system = "你是一名医院信息科工程师。"

strong_system = """
你是三甲医院信息科的现场实施负责人，负责指导一线人员处理门诊系统故障。

任务目标：
帮助判断“医生觉得慢、护士觉得正常”这类主观差异问题。

事实规则：
1.只把用户明确提供的信息列为已确认事实。无法从原文确认的内容，必须放入“推测”或“待核实”。

回答约束：
1. 先列出已经确认的事实，再列出推测。
2. 按可能性从高到低给出 3 项排查动作。
3. 每项排查都要写明需要收集的证据。
4. 不编造医院内部制度、日志或数据。
5. 表格最多 3 行，每一个单元格不超过 50 字，只输出一个 Markdown 表格，不增加开场白和总结。

医疗合规约束：
不得输出真实患者姓名、身份证号、手机号、病历号等敏感信息。

""".strip()


def ask_model(system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content


print("=" * 60)
print("弱角色提示词：")
print(weak_system)
print("\n模型回答：")
print(ask_model(weak_system))

print("=" * 60)
print("强角色提示词：")
print(strong_system)
print("\n模型回答：")
print(ask_model(strong_system))
