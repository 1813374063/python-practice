# 1.5_卡点专练.py
# ------------------------------------------------------------------
# 针对 1.3 复盘表里的 3 个卡点，做定向练习：
#   A. pd.to_numeric / 清洗     ← 第 1 题
#   B. Series.quantile          ← 第 3、4 题
#   C. 布尔筛选 + 排序           ← 第 4、5 题
#   D. 综合（不看答案，从零写）    ← 第 5、6、7 题
#
# 做法：
#   1. 把每个函数里的  ______  换成你自己写的代码（只改有 ______ 的行）
#   2. 运行本文件
#   3. 全部 ✅ 就算通关
#
# ⚠️ 不要打开 1.3_练习.md 的答案区。断言会告诉你对不对，不需要看答案。
# 运行： .venv\Scripts\python.exe 1.5_卡点专练.py
# ------------------------------------------------------------------

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "wait_times.csv", encoding="utf-8")

# 共用：清洗好的 Series（126 条有效值）
def _clean():
    return pd.to_numeric(df["等候时长"], errors="coerce").dropna()


# ============ 评测器（不用改）============
def run(no, fn, hint=""):
    try:
        fn()
    except NotImplementedError:
        print(f"⬜ {no}  还没做")
        return False
    except AssertionError:
        print(f"❌ {no}  断言没过       提示: {hint}")
        return False
    except Exception as e:
        print(f"❌ {no}  报错 {type(e).__name__}: {e}   提示: {hint}")
        return False
    else:
        print(f"✅ {no}")
        return True


# ==================================================================
# A. 卡点一：清洗（pd.to_numeric）
# ==================================================================

def a1():
    """把「等候时长」这一列转成数字，转不了的变成 NaN。"""
    d = df.copy()
    d["等候时长"] = pd.to_numeric(d["等候时长"],errors= 'coerce')         # ← 补全这一行
    assert d["等候时长"].isna().sum() == 1, "脏值应该只有 1 个"


def a3():
    """转成数字后，去掉空值，得到一个干净的 Series，赋给 s。"""
    d = df.copy()
    d["等候时长"] = pd.to_numeric(d["等候时长"], errors="coerce")
    s = d['等候时长'].dropna()                      # ← 补全这一行
    assert isinstance(s, pd.Series), "结果应该是 Series，不是 DataFrame"
    assert len(s) == 126


def a4():
    """不用 dropna。用布尔筛选留下「等候时长不为空」的行 —— 结果要是 DataFrame。"""
    d = df.copy()
    d["等候时长"] = pd.to_numeric(d["等候时长"], errors="coerce")
    clean = d[d["等候时长"].notna()]                   # ← 补全这一行
    assert isinstance(clean, pd.DataFrame), "用布尔筛选取行，结果应该是 DataFrame"
    assert len(clean) == 126


# ==================================================================
# B. 卡点二：分位数（Series.quantile）
# ==================================================================

def b1():
    """用【一次】quantile 调用，同时拿到 0.25 / 0.5 / 0.75 三个分位数。"""
    s = _clean()
    q = s.quantile([0.25,0.5,0.75])                   # ← 补全这一行
    assert list(q.index) == [0.25, 0.5, 0.75], "传列表进去，返回的 Series 索引就是这些分位点"
    assert abs(q.loc[0.25] - 19.25) < 1e-9


def b2():
    """分别取 Q1 和 Q3（两次 quantile，每次传一个数）。"""
    s = _clean()
    q1 = s.quantile(0.25)                     # ← 补全这一行
    q3 = s.quantile(0.75)                          # ← 补全这一行
    assert abs(q1 - 19.25) < 1e-9 and abs(q3 - 31.0) < 1e-9


def b3():
    """用 Q1、Q3 算出 IQR。"""
    s = _clean()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = s.quantile(0.75)-s.quantile(0.25)              # ← 补全这一行
    assert abs(iqr - 11.75) < 1e-9


def b4():
    """算 P90 分位数。"""
    s = _clean()
    p90 =  s.quantile(0.9)                   # ← 补全这一行
    assert abs(p90 - 37.0) < 1e-9


# ==================================================================
# C. 卡点三：布尔筛选 + 排序
# ==================================================================

def c1():
    """筛出所有小于 10 的值，转成 Python 列表并从小到大排序。"""
    s = _clean()
    got = sorted(s[s<10].tolist())                    # ← 补全这一行
    assert got == [-5.0, 3.0, 7.0, 8.0, 9.0, 9.0], "注意要 .tolist() 和 sorted()"


def c2():
    """IQR 法则：算出下界/上界，筛出落在区间外的值，排序输出。"""
    s = _clean()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo =  q1 - 1.5*iqr                  # ← 补全这一行
    hi =  q3 + 1.5*iqr                      # ← 补全这一行
    got = sorted(s[(s<lo)|(s>hi)].tolist())                  # ← 补全这一行
    assert got == [-5.0, 158.0, 164.0, 179.0, 181.0, 222.0]


def c3():
    """3σ 法则：用 mean / std 算出上下界，筛出区间外的值。"""
    s = _clean()
    lo = s.mean()-3*(s.std())                      # ← 补全这一行
    hi = s.mean()+3*(s.std())                       # ← 补全这一行
    got = sorted(s[(s<lo)|(s>hi)].tolist())                    # ← 补全这一行
    assert got == [158.0, 164.0, 179.0, 181.0, 222.0], "3σ 会漏掉 -5，这是正确结果"


def c4():
    """用 IQR 法则，返回异常值的【个数】和【占比（百分数，保留 2 位）】。"""
    s = _clean()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    out = s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)]
    cnt = len(out)                  # ← 补全这一行
    pct = round((len(out)/len(s))*100,2)                   # ← 补全这一行
    assert cnt == 6
    assert abs(pct - 4.76) < 0.01, "占比 = 个数 / 总数 * 100，要 round(...,2)"


# ==================================================================
# D. 综合：从这里开始没有 ______，自己从零写
# ==================================================================

def d1():
    """按科室分组，一次算出 人数(count) / 均值(mean) / 中位数(median)，
    保留 2 位小数，返回一个 DataFrame。"""
    d = df.copy()
    d["等候时长"] = pd.to_numeric(d["等候时长"], errors="coerce")
    got = d.groupby('科室')['等候时长'].agg(['count','mean','median']).round(2)                       # ← 用 None 占位，把这行改成你的答案
    assert got is not None, "还没写"
    assert got.shape == (6, 3), "应该是 6 行 3 列"
    assert abs(got.loc["内科", "mean"] - 32.81) < 1e-9


def d2():
    """领导问「我们平均候诊多久？」。
    给出三个能说明真相的数字：中位数、P90、超过 120 分钟的人数。"""
    s = _clean()
    med = s.median()                      # ← 改成你的答案
    p90 = s.quantile(0.9)                     # ← 改成你的答案
    long_cnt = (s>120).sum()                # ← 改成你的答案 len(s[s>120])
    assert None not in (med, p90, long_cnt), "还有没写的"
    assert abs(med - 25.0) < 1e-9
    assert abs(p90 - 37.0) < 1e-9
    assert long_cnt == 5


# ==================================================================
# 运行（不用改）
# ==================================================================
if __name__ == "__main__":
    cases = [
        ("A1", a1, "pd.to_numeric(列, errors='coerce')"),
        ("A3", a3, "Series.dropna()"),
        ("A4", a4, "布尔筛选：d[条件]，条件用 notna()"),
        ("B1", b1, "quantile 传一个列表"),
        ("B2", b2, "quantile 传一个数"),
        ("B3", b3, "IQR = Q3 - Q1"),
        ("B4", b4, "P90 → 传 0.90"),
        ("C1", c1, "布尔筛选 + .tolist() + sorted()"),
        ("C2", c2, "下界/上界 + 用 | 连两个条件"),
        ("C3", c3, "mean() / std()"),
        ("C4", c4, "len(out) 和 个数/总数*100"),
        ("D1", d1, "groupby + agg 传列表 + round"),
        ("D2", d2, "median / quantile(0.90) / (s > 120).sum()"),
    ]
    ok = 0
    for no, fn, hint in cases:
        ok += run(no, fn, hint)

    print()
    print("=" * 50)
    print(f"  通过 {ok}/{len(cases)}")
    if ok == len(cases):
        print("  🎉 通关！去写 1.3 的第 5、6、7 题，应该能不卡了。")
    else:
        print("  只看 ❌ 那几条的提示，不要重读整章。")
    print("=" * 50)
