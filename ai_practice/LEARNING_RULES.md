# ai_practice 学习文件规则

1. 基础阶段使用 `phaseNN-topic`，每门基础内容单独建文件夹。
2. 大模型课程使用 `lessonNN-topic`，每一课一个独立文件夹。
3. 课程脚本、数据、测试结果、笔记和知识卡片统一放在对应课程文件夹中。
4. `key.txt` 保留在 `ai_practice` 根目录，作为所有课程共享的本地密钥。
5. 不在 `ai_practice` 根目录继续堆放新课文件。
6. 本课文件直接放在课程文件夹根目录，不额外建立子目录。
7. 文件名统一使用 `x.x-原文件名.扩展名`。
8. 第一个 `x` 表示学习部分的编号，第二个 `x` 表示该部分内文件的生成顺序。

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
    ├── 0.1-CODE_READING_NOTES.md
    ├── 1.1-rag_knowledge.json
    ├── 1.2-chunking_demo.py
    ├── 2.1-retrieval_common.py
    ├── 2.2-rag_retrieval.py
    ├── 3.1-grounded_prompt_preview.json
    └── 4.1-grounded_answer_demo.py
```
