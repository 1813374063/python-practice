from openai import OpenAI

# 从文件读Key（这个文件不会上传到GitHub）
with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",   # ← 换成你注册平台的地址
)

response = client.chat.completions.create(
    model="DeepSeek-V4.1-Flash",          # ← 换成你选的模型名
    messages=[
        {"role": "user", "content": "用一句话解释什么是RAG"}
    ],
)

print(response.choices[0].message.content)