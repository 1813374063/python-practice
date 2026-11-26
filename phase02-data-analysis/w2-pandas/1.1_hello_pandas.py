# Lesson 1：DataFrame / Series / 索引 / 布尔筛选 / loc / iloc
# 运行： .venv\Scripts\python.exe 1.1-hello_pandas.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "workload.csv"

# 1. 读 CSV → 得到一个 DataFrame（二维表）
df = pd.read_csv(DATA_PATH, encoding="utf-8")
print("=== 整张表前 5 行 ===")
print(df.head())
print()

# 2. 认识这张表：形状、每列类型、空值数量
print("=== 形状 shape ===")
print(df.shape, "(行数, 列数)")
print()
print("=== 每列类型 dtypes ===")
print(df.dtypes)
print()
print("=== info（看非空数量，查脏数据靠它）===")
print(df.info())
print()

# 3. 取一列 → Series；取多列 → DataFrame
print("=== 取一列 df['接诊量']，前 5 个 ===")
print(df["接诊量"].head())
print()
print("=== 取多列 df[['科室','接诊量']]，前 5 行 ===")
print(df[["科室", "接诊量"]].head())
print()

# 4. loc（按标签）和 iloc（按位置）
print("=== loc[0, '科室'] 第一行的科室 ===")
print(df.loc[0, "科室"])
print("=== iloc[0, 0] 第 0 行第 0 列 ===")
print(df.iloc[0, 0])
print()

# 5. 布尔筛选
# (a) 字符串列可以直接比：筛「内科」
neike = df[df["科室"] == "内科"]
print("=== 布尔筛选：科室 == 内科 ===")
print(neike)
print()

# (b) 「接诊量 > 100」暂时比不了！因为列里混了「暂无」，整列成了字符串(str)
print("=== 接诊量 的类型是：", df["接诊量"].dtype, "===")
print("→ 字符串不能和数字比大小，所以 df['接诊量'] > 100 会报 TypeError")
print("→ 这正是 Lesson 2 要解决的「脏数据清洗」，先一句话转成数字：")
print()

# 一句话把「接诊量」转成数字：转不动的（'暂无'）变成 NaN（缺失值）
df["接诊量_数字"] = pd.to_numeric(df["接诊量"], errors="coerce")

# 现在就能比了：内科 且 接诊量 > 100
neike_high = df[(df["科室"] == "内科") & (df["接诊量_数字"] > 100)]
print("=== 内科且接诊量>100 ===")
print(neike_high)
print()

# 6. 认识脏数据「暂无」  -- unique() 取不同值(去重后的值)，shape() 取数量(总个数)
print("=== '接诊量' 这一列有哪些不同取值 ===")
print(df["接诊量"].unique())
print()
print("=== 找出脏数据行（接诊量 == '暂无'）===")
print(df[df["接诊量"] == "暂无"])

print(len(df[df['接诊量'] == '暂无']))
