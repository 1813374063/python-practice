# Lesson 1：描述统计与分布
# 运行： .venv\Scripts\python.exe 1.2_描述统计练习.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "data" / "wait_times.csv"

df = pd.read_csv(DATA, encoding="utf-8")

# 1. 清洗：把脏数据转成 NaN，再去掉
df["等候时长"] = pd.to_numeric(df["等候时长"], errors="coerce")
s = df["等候时长"].dropna()
print(s)
print(f"总行数 {len(df)}，有效值 {len(s)}，脏数据 {df['等候时长'].isna().sum()}")
print()

# 2. 集中趋势与离散程度
print("=== 均值 / 中位数 / 标准差 ===")
print(f"均值 mean   : {s.mean():.2f}")
print(f"中位数 median: {s.median():.2f}")
print(f"标准差 std   : {s.std():.2f}")
print("→ 均值比中位数高，说明有极端值把均值拉高了")
print()

# 3. 分位数 + IQR
print("=== 分位数 P25/P50/P75 ===")
q1, q2, q3 = s.quantile([0.25, 0.5, 0.75])
print(f"P25={q1:.2f}  P50={q2:.2f}  P75={q3:.2f}")
iqr = q3 - q1
print(f"IQR = Q3-Q1 = {iqr:.2f}")
print()

# 4. IQR 法则找异常值
print("=== IQR 异常值（更稳健）===")
lo_iqr, hi_iqr = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"正常区间: [{lo_iqr:.2f}, {hi_iqr:.2f}]")
out_iqr = s[(s < lo_iqr) | (s > hi_iqr)]
print("异常值:", sorted(out_iqr.tolist()))
print()

# 5. 3σ 法则找异常值（3西格玛 法则）
print("=== 3σ 异常值（受极端值影响）===")
lo_3s, hi_3s = s.mean() - 3 * s.std(), s.mean() + 3 * s.std()
print(f"正常区间: [{lo_3s:.2f}, {hi_3s:.2f}]")
out_3s = s[(s < lo_3s) | (s > hi_3s)]
print("异常值:", sorted(out_3s.tolist()))
print("→ 对比一下：3σ 漏掉了谁？为什么？")
print()

# 6. 各科对比：均值 vs 中位数
print("=== 各科 均值 vs 中位数 ===")
print(df.groupby("科室")["等候时长"].agg(["count", "mean", "median"]).round(2))
print()
print("→ 内科均值32.81、中位数23.0，差距最大，说明内科有极端长候诊")
