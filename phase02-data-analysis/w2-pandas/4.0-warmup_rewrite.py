# 核心练习：用 pandas 重写旧 warmup.py（for 循环版）
# 目标：输出「每科平均接诊量」+「跳过脏数据 X 行」，逻辑与旧版一致
# 旧版 60 行 → 这里 15 行

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "workload.csv"
RESULT_PATH = BASE_DIR / "result_pandas.txt"

df = pd.read_csv(DATA_PATH, encoding="utf-8")

# ① 转数字：转不动的（暂无）→ NaN；顺手数出脏数据行数
df["接诊量"] = pd.to_numeric(df["接诊量"], errors="coerce")
dirty = int(df["接诊量"].isna().sum())

# ② 按科室分组算平均（mean 自动跳过 NaN），round 取整
#    sort=False：保持科室首次出现的顺序（和旧版字典顺序一致）
avg = df.groupby("科室", sort=False)["接诊量"].mean().round().astype(int)

# ③ 输出
with open(RESULT_PATH, "w", encoding="utf-8") as f:
    for dept, v in avg.items():
        line = f"{dept},平均值为：{v}"
        f.write(line + "\n")
        print(line)
print(f"跳过脏数据 {dirty} 行")
