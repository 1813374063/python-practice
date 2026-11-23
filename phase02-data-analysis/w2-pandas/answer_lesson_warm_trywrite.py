#11.见 `4.0-warmup_rewrite.py`：用 pandas 重写旧的 for 循环版 warmup.py，输出一致即可。
print("见 `4.0-warmup_rewrite.py`：用 pandas 重写旧的 for 循环版 warmup.py，输出一致即可。")

import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
dps = pd.read_csv(base_dir/"data" / "workload.csv",encoding= 'utf-8')

dps['接诊量'] = pd.to_numeric(dps['接诊量'],errors = 'coerce')
avg = dps.groupby('科室',sort = False)['接诊量'].mean().round().astype(int)
dirty = dps['接诊量'].isna().sum()

for dept, v in avg.items():
    print(f"{dept},平均值为：{v}")
print(f"跳过脏数据 {dirty} 行")     
