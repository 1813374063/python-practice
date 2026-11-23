
import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent
dps = pd.read_csv(base / 'data' / 'workload.csv', encoding='utf-8')

print(dps.head())
print(dps.shape)
print(dps['接诊量'].unique())
   # shape[0] 某个表是「有多少个数」（返回（行数，列数）），
   # unique() 某列是「有多少种数」返回列表
#1. 用 `to_numeric(errors="coerce")` 把「接诊量」转成数字，打印新类型。
dps['接诊量'] = pd.to_numeric(dps['接诊量'],errors = 'coerce')
print(dps['接诊量'].dtype)

#2. 有多少个缺失值（NaN）？
print(dps['接诊量'].isna().sum())

#3.接诊量的**总接诊量 / 平均值 / 最高 / 最低**各是多少？（一句话分别打印）
print(dps['接诊量'].sum())
print(dps['接诊量'].mean())
print(dps['接诊量'].max())
print(dps['接诊量'].min())

#4. 用 `dropna` 得到干净数据，打印它的 `shape`。  df.dropna(subset='列') 整行删除
dps_2 = dps.dropna(subset = '接诊量')
print(dps_2) 
#5. 用 `fillna` 把缺失值填成**该列的平均值**，打印原来那 3 行现在变成了什么。
print()
print('#5. 用 `fillna` 把缺失值填成**该列的平均值**，打印原来那 3 行现在变成了什么。')
dps_3 = dps['接诊量'].isna()
dps_4 = dps.copy()
dps_4['接诊量'] = dps_4['接诊量'].fillna(dps['接诊量'].mean())
print(dps_4[dps_3])


#6.哪些科室有脏数据？打印这些科室名（去重）。提示：先筛出 `isna()` 的行，再取「科室」列，再用 `.unique()
dps_5 = dps[dps['接诊量'].isna()]['科室'].unique()
print(dps_5)

#7. `mean()` 自动跳过 NaN，那 `len(df)` 呢？它会计入 NaN 吗？试试 `len(df)` 和 `len(df.dropna(subset=["接诊量"]))` 各是多少，说明区别。

print(len(dps))
print(len(dps.dropna(subset=["接诊量"])))
