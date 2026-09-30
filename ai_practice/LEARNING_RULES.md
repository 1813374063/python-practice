# ai_practice 学习文件规则

1. 基础阶段使用 `phaseNN-topic`，每门基础内容单独建文件夹。
2. 大模型课程使用 `lessonNN-topic`，每一课一个独立文件夹。
3. 课程脚本、数据、测试结果、笔记和知识卡片统一放在对应课程文件夹中。
4. `key.txt` 保留在 `ai_practice` 根目录，作为所有课程共享的本地密钥。
5. 不在 `ai_practice` 根目录继续堆放新课文件。
6. 本课文件直接放在课程文件夹根目录，不额外建立子目录。
7. 文件名统一使用 `x.x-原文件名.扩展名`。
8. 第一个 `x` 表示学习部分的编号，第二个 `x` 表示该部分内文件的生成顺序。
9. 每生成一个新文件，必须先说明它的用途、输入、输出、是否调用模型和运行方式。
10. 每课维护一个文件导航，记录已有文件的阅读顺序和用途。
11. 一部分原则上只生成一个主要代码文件，通过参数控制可选行为，避免堆叠重复脚本。
12. 代码文件和运行结果要区分：代码用于执行，JSON、数据库和图片属于结果或资料。
13. 代码阅读只要求掌握入口、输入、输出和核心函数，不要求逐行理解全部语法。

新文件说明模板：

```text
文件名称：
学习部分：
主要用途：
输入：
输出：
是否调用模型：
运行方式：
建议阅读顺序：
```

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
    ├── 0.2-文件导航.md
    ├── 1.1-rag_knowledge.json
    ├── 1.2-chunking_demo.py
    ├── 1.3-chunks.json
    ├── 2.1-retrieval_common.py
    ├── 2.2-rag_retrieval.py
    ├── 2.3-rag_retrieval_results.json
    ├── 3.1-grounded_prompt_preview.json
    └── 4.1-grounded_answer_demo.py
```
