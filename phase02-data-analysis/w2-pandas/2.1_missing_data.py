# Lesson 2：缺失值与脏数据清洗
# 运行： .venv\Scripts\python.exe 2.1-missing_data.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "workload.csv"

df = pd.read_csv(DATA_PATH, encoding="utf-8")

# 1. 先识别脏数据
print("=== 接诊量 这一列有哪些取值（注意有 '暂无'）===")
print(df["接诊量"].unique())
print()
print("=== 接诊量 的类型（现在是字符串）===")
print(df["接诊量"].dtype)
print()

# 2. 转成数字：转不动的（'暂无'）变成 NaN
df["接诊量"] = pd.to_numeric(df["接诊量"], errors="coerce")
print("=== 转换后类型（变成 float64，因为 NaN 只能待在小数里）===")
print(df["接诊量"].dtype)
print()
print("=== 转换后前 8 行（看 NaN 出现在哪）===")
print(df.head(8))
print()

# 3. 检测缺失值
print("=== isna() 每一行是不是 NaN ===")
print(df["接诊量"].isna())
print()
print("=== 缺失值个数 isna().sum() ===")
print(df["接诊量"].isna().sum())
print()

# 4. 方式一：不处理，直接算（聚合函数自动跳过 NaN）
print("=== 平均接诊量 mean()（自动跳过 3 个 NaN）===")
print(df["接诊量"].mean())
print()
print("=== 总接诊量 sum() / 最高 max() / 最低 min() ===")
print("sum =", df["接诊量"].sum())
print("max =", df["接诊量"].max())
print("min =", df["接诊量"].min())
print()

# 5. 方式二：dropna 删掉含 NaN 的行 -- 删除整行
df_clean = df.dropna(subset=["接诊量"])
print("=== dropna 后 shape（24 行 → 21 行）===")
print(df_clean.shape)
print()

# 6. 方式三：fillna 填值（这里填 0）
df_filled = df.copy()
print(df_filled)

df_filled["接诊量"] = df_filled["接诊量"].fillna(0)
print("=== fillna(0) 后，原来 NaN 的位置 ===")
print(df_filled[df["接诊量"].isna()])
