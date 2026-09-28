# ai_practice 学习文件规则

1. 基础阶段使用 `phaseNN-topic`，每门基础内容单独建文件夹。
2. 大模型课程使用 `lessonNN-topic`，每一课一个独立文件夹。
3. 课程脚本、数据、测试结果、笔记和知识卡片统一放在对应课程文件夹中。
4. `key.txt` 保留在 `ai_practice` 根目录，作为所有课程共享的本地密钥。
5. 不在 `ai_practice` 根目录继续堆放新课文件。

当前目录结构：

```text
ai_practice/
├── key.txt
├── LEARNING_RULES.md
├── phase01-python-and-git/
│   ├── python-basics/
│   └── git-github/
├── lesson01-llm-api-basics/
├── lesson02-multi-turn-chat/
├── lesson03-prompt-engineering/
└── lesson04-rag-basics/
```
