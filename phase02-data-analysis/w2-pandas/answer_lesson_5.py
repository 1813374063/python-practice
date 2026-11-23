import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
pds = pd.read_csv(base_dir/'data'/'workload.csv',encoding= 'utf-8')
depts = pd.read_csv(base_dir/'data'/'departments.csv',encoding= 'utf-8')

#1. 用 `pd.merge(work, depts, on="科室", how="inner")` 内连接，打印行数。
print('1. 用 `pd.merge(work, depts, on="科室", how="inner")` 内连接，打印行数。')
pds_1 = pd.merge(pds ,depts ,on = '科室',how= 'inner')
print("行数:",pds_1.shape[0])
print()

#2改成 `how="right"`，打印行数，并找出「护理部」那一行的接诊量（是不是 NaN？）。
print('2.改成 `how="right"`，打印行数，并找出「护理部」那一行的接诊量（是不是 NaN？）。')

pds_2 = pd.merge(pds ,depts ,on = '科室',how= 'right')
pds_2['接诊量'] = pd.to_numeric(pds_2['接诊量'],errors = 'coerce')
print('行数：',pds_2.shape[0])
print(pds_2)
print()

#3. 用 `how="outer"`，打印行数，回答：为什么比 inner 多 1 行？
print('3. 用 `how="outer"`，打印行数，回答：为什么比 inner 多 1 行？')
print(pd.merge(pds ,depts ,on = '科室',how= 'outer'))
print('outer代表了并集')
print()

#4. 合并后，打印「门诊楼」这一列有哪些不同的值（去重）。
print('4. 合并后，打印「门诊楼」这一列有哪些不同的值（去重）。')
print(pds_2['门诊楼'].unique())
print()

#5. 用 `pivot_table` 做「科室 × 月份」总接诊量交叉表。
print('5. 用 `pivot_table` 做「科室 × 月份」总接诊量交叉表。')
print(pds_2.pivot_table(index = '科室',columns = '月份',values = '接诊量',aggfunc = 'sum'))
print()

#6. 把 `aggfunc` 改成 `"mean"`，看「每科每月平均」交叉表，比较和上一题的区别。
print('6. 把 `aggfunc` 改成 `"mean"`，看「每科每月平均」交叉表，比较和上一题的区别。')

print(pds_2.pivot_table(index = '科室',columns = '月份',values = '接诊量',aggfunc = 'mean'))
print()


#7. 用 `pivot_table` 做「门诊楼 × 月份」的总接诊量（行=门诊楼）。
print('7. 用 `pivot_table` 做「门诊楼 × 月份」的总接诊量（行=门诊楼）。')
print(pds_2.pivot_table(index = '门诊楼',columns = '月份',values = '接诊量',aggfunc = 'sum'))
print()

#8. （进阶）交叉表里，哪个「科室-月份」的接诊量最高？（提示：`.max().max()` 或 `.stack().idxmax()`）
print('8. （进阶）交叉表里，哪个「科室-月份」的接诊量最高？（提示：`.max().max()` 或 `.stack().idxmax()`）')

print(pds_2.pivot_table(index = '科室',columns = '月份',values = '接诊量',aggfunc = 'sum').stack().idxmax())

print('二维表想「找谁最大」，就先 .stack() 摊平，再 .idxmax() 拿坐标；想「最大值多少」就用 .max().max()。') 

'''示例
科室  月份
儿科  1月    132.0
     2月    128.0
     3月    140.0   ← 最大
     4月    135.0
内科  1月    118.0'''