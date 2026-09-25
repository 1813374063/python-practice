from openai import OpenAI

BASE_URL = "https://api.deepseek.com"   # 平台地址
MODEL = "deepseek-flash"                # 模型名，必须和平台支持的完全一致

with open("key.txt", encoding="utf-8") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key, base_url=BASE_URL)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "用一句话解释什么是RAG"}
    ],
)

print(response.choices[0].message.content)