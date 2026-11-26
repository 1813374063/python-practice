import pandas as pd
from pathlib import Path

# 关键修复：用 __file__ 定位脚本所在目录，路径就不再受「在哪个目录运行」影响
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "workload.csv", encoding="utf-8")

print(df.shape)
print()
print(df.head(3))
print()
print(df[df['科室']=='外科'])
print()

df['接诊量_nums'] = pd.to_numeric(df['接诊量'],errors= 'coerce')
print(df[df['接诊量_nums']>120])
print()

print(df[(df['科室']=='儿科') & (df['接诊量_nums']>130)])
print()

a= df.loc[2,'月份']
print(a)
print()
b = df.iloc[2,2]
print(b)
print()

print(df[df['接诊量'] == '暂无'].shape[0])

'现在是string类型'
 
print(df[df['科室'].isin(['骨科','眼科'])])




