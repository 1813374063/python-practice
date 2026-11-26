# Lesson 3：groupby + agg（分组聚合）
# 运行： .venv\Scripts\python.exe 3.1-groupby_agg.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "workload.csv", encoding="utf-8")

# 先把「暂无」转成 NaN（干净的数字列才能聚合）
df["接诊量"] = pd.to_numeric(df["接诊量"], errors="coerce")

# 1. 单列分组求和：每个科室的总接诊量
print("=== 1. 每科总接诊量：groupby('科室')['接诊量'].sum() ===")
print(df.groupby("科室")["接诊量"].sum())
print()

# 2. agg 一次算多个指标：sum / mean / max / min / count
print("=== 2. 每科 多指标 agg(['sum','mean','max','min','count']) ===")
print(df.groupby("科室")["接诊量"].agg(["sum", "mean", "max", "min", "count"]))
print()

# 3. count（跳过 NaN） vs size（数所有行）
print("=== 3. count 跳过 NaN，size 数所有行 ===")
count_series = df.groupby("科室")["接诊量"].count()
size_series = df.groupby("科室").size()
print("count:", count_series.tolist())   # 外科/骨科/眼科 会因为 NaN 少 1
print("size :", size_series.tolist())    # 都是 4
print()

# 4. 多列分组：科室 × 月份
print("=== 4. 科室×月份 的总接诊量 ===")
print(df.groupby(["科室", "月份"])["接诊量"].sum())
print()

# 5. reset_index 变回普通表，再 sort_values 排序
print("=== 5. reset_index + 按总接诊量从高到低排序 ===")
result = df.groupby("科室")["接诊量"].sum().reset_index()
print(result.sort_values("接诊量", ascending=False))
