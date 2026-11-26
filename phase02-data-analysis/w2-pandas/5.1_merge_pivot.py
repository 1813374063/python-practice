# Lesson 4：merge（多表关联）+ pivot_table（交叉表）
# 运行： .venv\Scripts\python.exe 5.1-merge_pivot.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
work = pd.read_csv(BASE_DIR / "data" / "workload.csv", encoding="utf-8")
depts = pd.read_csv(BASE_DIR / "data" / "departments.csv", encoding="utf-8")

work["接诊量"] = pd.to_numeric(work["接诊量"], errors="coerce")

print("=== workload 表（接诊量，24 行）===")
print(work.head(3))
print("行数:", work.shape[0])
print()

print("=== departments 表（科室维度，7 行，含没数据的护理部）===")
print(depts)
print("行数:", depts.shape[0])
print()

# 1. merge：按「科室」把两张表拼起来（内连接，只保留两表都有的科室）
print("=== 1. merge 内连接 how='inner'（等价 SQL JOIN）===")
merged = pd.merge(work, depts, on="科室", how="inner")
print(merged.head(3))
print("行数:", merged.shape[0])   # 24（护理部被排除）
print()

# 2. how 参数对比：看行数变化
print("=== 2. how 参数对比（行数）===")
for hows in ["inner", "left", "right", "outer"]:
    n = pd.merge(work, depts, on="科室", how=hows).shape[0]
    print(f"{hows:5s}: {n} 行")
print("→ right/outer 会多 1 行：护理部没有接诊量，接诊量位置是 NaN")
print()

# 3. pivot_table：科室 × 月份 交叉表（等价 Excel 数据透视表）
print("=== 3. pivot_table：科室 × 月份 总接诊量 ===")
pivot = merged.pivot_table(index="科室", columns="月份", values="接诊量", aggfunc="sum")
print(pivot)
print()

# 4. aggfunc 换成 mean：每科每月平均
print("=== 4. pivot_table aggfunc='mean'（每科每月平均）===")
print(merged.pivot_table(index="科室", columns="月份", values="接诊量", aggfunc="mean"))
print()

# 5. 综合：merge 后按门诊楼汇总接诊量
print("=== 5. 按门诊楼汇总接诊量 ===")
print(merged.groupby("门诊楼")["接诊量"].sum())
