# 阶段 2 收口产出：月度运营报表
# 目标：读数据 → 清洗 → merge 维度 → 科室×月份透视 → 导出 CSV
# 用法：把每个 `...` 换成 TODO 注释里说的代码，然后运行

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WORK_PATH = BASE_DIR / "data" / "workload.csv"
DEPT_PATH = BASE_DIR / "data" / "departments.csv"
OUT_PATH = BASE_DIR / "report_monthly.csv"

# STEP 1：读两张表（已写好，不用改）
work = pd.read_csv(WORK_PATH, encoding="utf-8")
depts = pd.read_csv(DEPT_PATH, encoding="utf-8")

# STEP 2：清洗接诊量（把「暂无」转成 NaN）
# TODO: 用 pd.to_numeric(work["接诊量"], errors="coerce")
work["接诊量"] = pd.to_numeric(work['接诊量'],errors = 'coerce')

# STEP 3：merge 维度表，拿到「门诊楼」
# TODO: 用 pd.merge(work, depts, on="科室", how="inner")
merged = pd.merge(work, depts, on="科室", how="inner")

# STEP 4：科室 × 月份 的总接诊量透视表
# TODO: 用 merged.pivot_table(index="科室", columns="月份", values="接诊量", aggfunc="sum")
pivot = merged.pivot_table(index = '科室',columns = '月份',values = '接诊量',aggfunc = 'sum')

# STEP 5：导出 CSV
# TODO: 用 pivot.to_csv(OUT_PATH, encoding="utf-8")
pivot.to_csv(OUT_PATH,encoding = 'utf-8')

# 打印结果 + 确认导出
print(pivot)
print("已导出:", OUT_PATH)

# 加分项：每科汇总（sum / mean / max / min）
print()
print("=== 每科汇总 ===")
print(merged.groupby('科室')['接诊量'].agg(['sum','mean' ,'max' , 'min']))   

# TODO: 用 merged.groupby("科室")["接诊量"].agg(["sum","mean","max","min"])
