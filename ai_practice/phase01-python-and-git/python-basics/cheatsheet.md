# Python 语法急救卡片

用法：做题时放在旁边随便翻。卡片上有的东西不用背，工作里大家都是随手查的。

## 热身示例（先照着敲一遍，找回手感）

新建一个文件 `warmup.py`，把下面代码敲进去（是敲，不是复制），然后运行它：

```python
# 求 1 到 10 的和
total = 0
for i in range(1, 11):
    total = total + i
print("结果是:", total)
```

运行方法：在这个文件夹里打开终端（或命令行），输入 `python warmup.py` 回车，看到 `结果是: 55` 就说明环境和你都没问题。

---

## 打印与变量

```python
print("你好")
print("结果是:", 42)

name = "内科"      # 字符串
count = 12         # 数字
```

## 循环

```python
# 遍历列表里的每一项
waiting = [12, 5, 23]
for num in waiting:
    print(num)

# 从 1 循环到 100（range 不包含终点）
for i in range(1, 101):
    print(i)
```

## 条件判断

```python
if count > 10:
    print("多")
elif count > 5:
    print("一般")
else:
    print("少")

# 判断倍数用取余：i 能被 3 整除
if i % 3 == 0:
    print("3的倍数")
```

## 列表

```python
waiting = [12, 5, 23, 8]
waiting[0]       # 取第1个 → 12
len(waiting)     # 长度 → 4
sum(waiting)     # 求和 → 48
max(waiting)     # 最大值 → 23（第1关要求你自己用循环实现，不许用这个）
```

## 字典

```python
record = {"科室": "内科", "接诊量": 32}
record["科室"]         # 取值 → "内科"
record["接诊量"] = 35  # 改值

# 遍历字典
for key, value in record.items():
    print(key, value)
```

## 函数

```python
def add(a, b):
    return a + b

result = add(3, 5)   # 调用 → 8
```

## 字符串

```python
line = "2026-09-20 08:15:32"
parts = line.split(" ")    # 按空格切开 → ["2026-09-20", "08:15:32"]
"警告" in "[警告]"          # 是否包含 → True
s = "[警告]"
s.strip("[]")              # 去掉两端的方括号 → "警告"
```

## 读文件

```python
with open("data/workload.csv", encoding="utf-8") as f:
    for line in f:
        line = line.strip()      # 去掉行尾的换行符
        print(line)
```

## 写文件

```python
with open("result.txt", "w", encoding="utf-8") as f:
    f.write("内科: 平均工作量 120\n")   # \n 表示换行
```

## 异常处理（遇到脏数据不崩溃）

```python
try:
    x = int("暂无")        # 这行会出错
except ValueError:
    print("这行是脏数据，跳过")

# 文件不存在的情况
try:
    f = open("不存在的文件.csv", encoding="utf-8")
except FileNotFoundError:
    print("找不到数据文件，请检查路径")
```

## 数字与字符串互转

```python
int("118")    # 字符串 → 数字 118
str(118)      # 数字 → 字符串 "118"
round(3.14159, 1)   # 保留1位小数 → 3.1
```

---

做到第4关（sqlite3）之前，先只做前3关，做完发给我批改。第4关等热身完成后我单独验收。
