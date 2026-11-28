import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
pds = pd.read_csv(BASE_DIR/'data'/'workload.csv',encoding = 'utf-8')


#1. 读 CSV，打印 `shape`、`dtypes`、前 3 行。
print()
print('1. 读 CSV，打印 `shape`、`dtypes`、前 3 行。')
print(pds.shape)
print(pds.dtypes)
print(pds.head(3))

#2. 用 `value_counts()` 统计每个科室各有多少行。
print()
print('2.用 `value_counts()` 统计每个科室各有多少行。')
print(pds['科室'].value_counts())

#3. 数据 `data/workload.csv`。第 3 题起先 `pd.to_numeric(errors="coerce")` 把接诊量转数字。
print()
print(' 接诊量 > 120 的行有多少？（提示：转数字后筛，用 `shape[0]` 或 `len` 计数）')
pds['接诊量'] = pd.to_numeric(pds['接诊量'],errors = 'coerce')
print(pds.dtypes)
print(pds[pds['接诊量'] > 120 ].shape[0])
print(len(pds[pds['接诊量'] > 120]))

#4. 找出「儿科」且「接诊量 > 130」的行，打印整行。
print()
dps_2 = pds[(pds['科室'] == '儿科') & (pds['接诊量'] > 130)]
print(dps_2)

#5. 用 `isin` 找出「骨科」「眼科」两科，打印这两科一共几行。
print()
pds_3 = pds[pds['科室'].isin(['骨科','眼科'])].shape[0]
print(pds_3)

#6. 用 `loc` 取出「接诊量最高」的那一整行。（提示：`dps['接诊量'].idxmax()` 返回最大值的行号）
print()
print("6. 用 `loc` 取出「接诊量最高」的那一整行。（提示：`dps['接诊量'].idxmax()` 返回最大值的行号）")
print(pds.loc[[pds["接诊量"].idxmax()]])

# 7.接诊量 < 90 的科室有哪些？打印去重后的科室名。
print()
print("7.接诊量 < 90 的科室有哪些？打印去重后的科室名。")

pds_4 = pds[pds['接诊量'] < 90]['科室'].unique()
print(pds_4)

#8. 分别 各科室每月总接诊量。（提示：4 次布尔筛选 + `sum()`）
print()
print("分别 各科室每月总接诊量。（提示：4 次布尔筛选 + `sum()`）")

for i in pds['月份'].unique():
    for m in pds['科室'].unique():
        print(f"第{i}月{m}:{pds[(pds["月份"] == i) & (pds["科室"] == m)]["接诊量"].sum()}")


#9.两种填法对比：分别用 `fillna(0)` 和 `fillna(mean)` 填缺失值，各算一次总接诊量 `sum()`，看差多少。
print()
pds_5 = pds.fillna(0)
print(pds['接诊量'].fillna(0).sum())

print(pds['接诊量'].fillna(pds['接诊量'].mean()).sum())

#10.用 `dropna(subset=["接诊量"])` 删干净后，平均接诊量是多少？和「不删、靠 mean() 自动跳过 NaN」的结果一样吗？
pds_6 = pds.dropna(subset = '接诊量')
print(pds.dropna(subset = '接诊量')['接诊量'].mean())
print(pds['接诊量'].mean())


#11. 为什么「填 0」会让**平均接诊量变小**，而「填平均值」平均接诊量**不变**？



