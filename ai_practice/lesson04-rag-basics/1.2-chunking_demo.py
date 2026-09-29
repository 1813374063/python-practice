import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "1.3-chunks.json"

POLICY_TEXT = """# 门诊信息系统故障分级与处理办法

## 第一条 适用范围
本办法适用于门诊医生站、护士站、叫号大屏、处方打印和检验报告查询等门诊信息系统故障。真实患者信息不得进入学习样例、公网模型或非授权知识库。

## 第二条 故障分级
P1 表示影响关键诊疗且没有替代方案，需要立即升级。P2 表示影响单点、单岗位或单个外设，但存在替代方案。P3 表示需求、咨询或低影响问题，可按正常工单处理。

## 第三条 处理流程
第一步确认影响范围和具体操作。第二步收集发生时间、终端编号、账号、业务模块、报错信息和耗时。第三步与正常终端或正常账号交叉对比。第四步根据分级规则选择现场处理或升级。

## 第四条 升级条件
同一问题在多台电脑或多位用户处复现时，应升级二线。无法保存病历、无法查询检验报告、无法打印处方并影响诊疗或发药时，应立即通知业务负责人。问题范围持续扩大时，启动应急流程。

## 第五条 合规要求
不得在问答内容、截图、日志或测试数据中暴露患者姓名、证件号、病历号、手机号等敏感信息。知识库必须执行访问权限控制，回答必须保留资料来源，涉及患者安全时必须人工复核。
"""


def split_by_sections(text):
    section_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(section_pattern.finditer(text))
    chunks = []

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section_title = match.group(1).strip()
        chunk_text = text[start:end].strip()

        chunks.append(
            {
                "chunk_id": f"CHUNK-{index + 1:03d}",
                "section": section_title,
                "text": chunk_text,
                "character_count": len(chunk_text),
                "metadata": {
                    "document": "门诊信息系统故障分级与处理办法",
                    "document_type": "虚构教学制度",
                    "access_level": "内部教学",
                    "version": "v1.0",
                },
            }
        )

    return chunks


chunks = split_by_sections(POLICY_TEXT)

result = {
    "notice": "本文档为虚构教学资料，不得作为真实医院制度。",
    "source_character_count": len(POLICY_TEXT),
    "chunk_count": len(chunks),
    "chunks": chunks,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"原文长度：{len(POLICY_TEXT)} 字符")
print(f"切分片段：{len(chunks)} 个")

for chunk in chunks:
    print(
        f"{chunk['chunk_id']} "
        f"{chunk['section']} "
        f"长度={chunk['character_count']}"
    )

print(f"切分结果已保存到：{OUTPUT_PATH.name}")
