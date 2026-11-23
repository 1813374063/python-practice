import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
pds = pd.read_csv(base_dir/"data"/"workload.csv",encoding = "utf-8")

pds['接诊量'] =pd.to_numeric(pds['接诊量'],errors = 'coerce')
print()
#1. 每个科室的总接诊量（`groupby('科室')['接诊量'].sum()`）。
print("1. 每个科室的总接诊量（`groupby('科室')['接诊量'].sum()")
pds_1 = pds.groupby('科室')['接诊量'].sum()
print(pds_1)
print()

#2. 每个科室的平均接诊量（`mean()`）。
print("2. 每个科室的平均接诊量（`mean()`）。")

print(pds.groupby('科室')['接诊量'].mean())
print()

#3. 用 `agg` 一次算出每科的 `sum / mean / max / min`。
print("3. 用 `agg` 一次算出每科的 `sum / mean / max / min`。")

print(pds.groupby('科室')['接诊量'].agg(['sum','mean','max','min']))
print()


#4. 每个科室有几个**有效**接诊量（`count()`，跳过 NaN）？
print("4. 每个科室有几个**有效**接诊量（`count()`，跳过 NaN）？")
print(pds.groupby('科室')['接诊量'].count())
print()

#5. 每个科室有几**行**（`size()`）？和上一题对比，哪几个科室不一样，为什么？
print("5. 每个科室有几**行**（`size()`）？和上一题对比，哪几个科室不一样，为什么？")
print(pds.groupby('科室')['接诊量'].size())   #size()只会考虑实际的行数（包含NAN数据）
print()


#6. 全公司总接诊量是多少（不分科室）？
print('sum:',pds['接诊量'].sum())
print()

#7. 「科室 × 月份」的总接诊量（多列 `groupby(['科室','月份'])`）。
print("7. 「科室 × 月份」的总接诊量（多列 `groupby(['科室','月份'])`）。")
print(pds.groupby(['科室','月份'])['接诊量'].sum())
print()

#8. 接诊量**最高**的科室是哪个（用 `sort_values(ascending=False).head(1)`）？   --ascending = True/False  升序/降序排序
print("8. 接诊量**最高**的科室是哪个（用 `sort_values(ascending=False).head(1)`）？")
pds_2 = pds.groupby('科室')['接诊量'].sum().reset_index()
print(pds_2.sort_values('接诊量',ascending=False).head(1))
print()

#9. 用 `reset_index()` 把第 1 题结果变回普通表，再按总接诊量从高到低排序。
print("9. 用 `reset_index()` 把第 1 题结果变回普通表，再按总接诊量从高到低排序。")

print(pds_1.reset_index().sort_values('接诊量',ascending = False))
print()

#10. 每个科室的「月均接诊量」（提示：`mean()` 自动跳过 NaN，直接 `groupby().mean()` 即可）。  -- 如果要计算全年(某月无值也要计算)
print("10. 每个科室的「月均接诊量」（提示：`mean()` 自动跳过 NaN，直接 `groupby().mean()` 即可）。")
print(pds.groupby('科室')['接诊量'].mean())
print()
'-----------------------------------------'
print('如果要计算全年(某月无值也要计算)')
pds['接诊量'] = pds['接诊量'].fillna(0)
print(pds.groupby('科室')['接诊量'].mean())
print()



