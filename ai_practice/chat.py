from openai import OpenAI

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

# 对话历史：只初始化一次，它在整个对话里持续累加
history = [
    {"role": "system", "content": "你是一位医院信息科的资深工程师，你是给非技术人员讲课的科普作者，多用比喻，口语化。"}
]

print("开始对话吧，输入 exit 退出。\n")

while True:
    question = input("我：")
    if question == "exit":
        break

    # 第1步：把用户这句话加进历史
    history.append({"role": "user", "content": question})

    # 第2步：把完整历史打包发给模型
    response = client.chat.completions.create(model=MODEL, messages=history)
    answer = response.choices[0].message.content

    # 第3步：把模型的回答也存回历史（关键！）
    history.append({"role": "assistant", "content": answer})

    print("AI：" + answer + "\n")
