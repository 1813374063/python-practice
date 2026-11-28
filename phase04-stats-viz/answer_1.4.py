import pandas as pd
from pathlib import Path

base_dir= Path(__file__).resolve().parent
pds = pd.read_csv(base_dir/'data'/'wait_times.csv',encoding='utf-8')

print('1. 清洗数据：把「等候时长」转成数字（脏数据变 NaN），打印有效值条数和脏数据条数。')

pds['等候时长'] = pd.to_numeric(pds['等候时长'],errors='coerce')
s = pds['等候时长'].dropna()
s2 = pds['等候时长'].isna().sum()
print(f"有效值条数：{len(s)},脏数据条数：{s2}")
print()

print('2. 算出均值、中位数、标准差，并说明「均值为什么比中位数高」。')
s3 = s.agg(['mean','median','std'])
print(s3)
print('因为均值存在极端值，拉高了均值的整体量')
print()

print('3. 算出 P25 / P50 / P75 和 IQR。')
q1,q2,q3 = s.quantile([0.25,0.5,0.75])
print(f"IQR:{q3-q1},\n正常值区间：{q1-1.5*(q3-q1),q3+1.5*(q3-q1)}")
print()

print('4. 用 IQR 法则找出异常值，列出具体数字。.tolist()：把 Series 转成 Python 列表，sorted()：从小到大排序，方便阅读')

s4 =s[(s<q1-1.5*(q3-q1)) | (s > q3+1.5*(q3-q1))]
print(s4)
print(sorted(s4.tolist()))
print()

print('5. 用 3σ 法则找出异常值，和第 4 题对比：**哪种方法多抓到了哪个值？为什么？**')

low,high = s.mean()- 3 * s.std(), s.mean() + 3*s.std()
s5 = s[(s<low) | (s>high)]
print(sorted(s5.tolist()))
print('3σ 漏了 -5：因为 5 个极端值把 std 撑到 32.15，下界被拉到 -65.66，-5 不算异常。数据有极端值时，IQR 比 3σ 更稳健')
print()

print('6. 各科「均值 vs 中位数」对比，哪个科室两者差距最大？说明了什么？')

print(pds.groupby("科室")["等候时长"].agg(['mean','median']).round(2))

print()

print('7. 思考：领导问「我们平均候诊多久？」，你只回「30.79 分钟」有什么问题？你会怎么补充？')

print('补充：均值在30.79，但是我们看到数据的中位数在25，说明存在极端值，拉大了均值数，说明多数人时存在25分钟左右，但是存在少数人极端大的情况')
