# # 打印 1 到 100 的所有数字，但：
# # - 遇到 3 的倍数改打印"病"
# # - 遇到 5 的倍数改打印"历"
# # - 同时是 3 和 5 的倍数打印"病历"

# total = []
# for i in range(1,101):
#     if i % 3 == 0 and i % 5  == 0:
#         total.append('病历')
#     elif i % 3 == 0:
#         total.append('病')
#     elif i % 5 == 0:
#         total.append('历')
#     else:
#         total.append(i)

# print(total)

# # ---------------------------------------------------

# # 各科室今天上午的候诊人数：

# # ```python
# # waiting = [12, 5, 23, 8, 16, 3, 9]
# # ```

# # 要求：不使用 sort() 或 sorted()，用循环找出其中的最大值和最小值，并算出平均值（保留1位小数）。
# waiting = [12, 5, 23, 8, 16, 3, 9]
# max_waiting = waiting[0]
# min_waiting = waiting[0]
# total_waiting = 0

# for num in waiting:
#     total_waiting += num  #用于计算平均值
#     if num > max_waiting:
#         max_waiting = num
#     if num < min_waiting:
#         min_waiting = num

# average_waiting = total_waiting / len(waiting)

# print(f"最大值: {max_waiting}")
# print(f"最小值: {min_waiting}")
# print(f"平均值: {average_waiting:.1f}")

# #-------------------------------------------------------------

# # ```python
# records = [
#     {"科室": "内科", "接诊量": 32},
#     {"科室": "外科", "接诊量": 27},
#     {"科室": "内科", "接诊量": 18},
#     {"科室": "儿科", "接诊量": 41},
#     {"科室": "外科", "接诊量": 22},
# ]
# # ```

# # 写两个函数：
# # - `total_by_dept(records)`：返回每个科室的总接诊量，形如 `{"内科": 50, "外科": 49, "儿科": 41}`
# # - `top_dept(records)`：返回总接诊量最高的科室名称

# def total_by_dept(records):
#     dept_totals = {}
#     for record in records:
#         dept = record["科室"]
#         count = record["接诊量"]
#         if dept in dept_totals:
#             dept_totals[dept] += count
#         else:
#             dept_totals[dept] = count
#     return dept_totals
# print(total_by_dept(records))  # 输出: {'内科': 50, '外科': 49, '儿科': 41}

# #   以下为两种写法，第一种是手动循环找最大值
# def top_dept(records): 
#     dept_totals = total_by_dept(records)
#     best_dept = None
#     best_total = -1
#     for dept, total in dept_totals.items():
#         if total > best_total:
#             best_dept = dept
#             best_total = total
#     return best_dept
# #以下为这是一个空字典，Pylance 不知道你打算往里面装什么（键是什么类型、值是什么类型），于是它记成"未知"（截图里那句 (variable) dept_totals: dict[Unknown, Unknown] 就是这个意思）。 而 max(...) 这个函数对 key= 参数有要求：你交给它的"换算工具"必须返回能比较大小的东西。Pylance 拿到一个"未知类型"的字典，无法确认 dept_totals.get 返回的是不是可比较的值，就按最保守的方式报警了。
# def top_dept(records):
#     dept_totals = total_by_dept(records)
#     return max(dept_totals, key=dept_totals.get)
    

#  #-------------------------------------------------------------
# # 系统日志里有一行：

# # ```python
# line = "2026-09-20 08:15:32 [警告] 接口HIS01响应超时"
# # ```

# # 写函数 `parse_log(line)`，把它解析成字典返回：

# # ```python
# # {"日期": "2026-09-20", "时间": "08:15:32", "级别": "警告", "内容": "接口HIS01响应超时"}

# def parse_log(line):
#     date, time, rest = line.split(' ', 2)
#     level_start = rest.find('[') + 1
#     level_end = rest.find(']')
#     level = rest[level_start:level_end]
#     content = rest[level_end + 2:]  # Skip the space after the closing bracket
#     return {"日期": date, "时间": time, "级别": level, "内容": content}

# print(parse_log(line))


# # -------------------------------------------------------------
# 数据文件在本文件夹的 C:\Users\15634\Documents\New_project/python_test/data/workload.csv`（提示：open 时加上 `encoding="utf-8"`，否则中文可能乱码）。

### 3-1 计算平均工作量

# 读取该 CSV，计算每个科室的月平均工作量（按有效数据计算，结果取整数），按下面的格式写入 `result.txt`：

# ```
# 内科: 平均工作量 120
# 外科: 平均工作量 100


# 数据里混了一行脏数据（工作量一栏是"暂无"）。要求：
# - 处理时跳过它，程序结束前打印"跳过脏数据 X 行"
# - 如果数据文件不存在，程序打印"找不到数据文件，请检查路径"后正常退出，而不是直接报错崩溃

import sys


sums = {}
counts = {}
skipped = 0
try:
    with open("python-test/data/workload.csv", encoding="utf-8") as f:
        next(f)  # 跳过表头
        for line in f:
            dept,mouth,workload = line.strip().split(',')
            try:
                workload = int(workload)
            except ValueError:
                skipped += 1
                continue   # 如果 counts 不是整数，跳过该行    

            if dept in sums:
                sums[dept] += workload
                counts[dept] += 1
            else:                                # 第一次见
                sums[dept] = workload
                counts[dept] = 1
except FileNotFoundError:
    print("文件未找到，请检查路径是否正确。")
    sys.exit()

with open('python-test/result.txt', 'w', encoding='utf-8') as f:
    for dept in sums:
        avg = round(sums[dept]/counts[dept])
        f.write(f'{dept},平均值为：{avg}\n')
        print(f'{dept},平均值为：{avg}')
    print(f"跳过脏数据 {skipped} 行")



                

            
       
    

