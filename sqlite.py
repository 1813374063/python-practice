import sqlite3

conn = sqlite3.connect("study.db")   # 连接数据库，文件不存在会自动创建
cur = conn.cursor()                      # 操作手柄，之后都靠它干活

cur.execute("DROP TABLE IF EXISTS dept_amounts")  #让脚本可以重复运行。现在这张表和数据已经存在了，你再跑一次脚本还会撞主键（就算改成自动编号，也会插进去一堆重复数据）。学习阶段最方便的做法是在建表前加一句：cur.execute("DROP TABLE IF EXISTS 表名") 

# 建表
cur.execute("""
    CREATE TABLE IF NOT EXISTS dept_amounts (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        dept_id INTEGER,
        dept   TEXT,
        month  TEXT,
        amount INTEGER
    )
""")

# 插入数据：? 是占位符，具体值用元组传进去
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (1, "神经内科", "1月", 118))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (2, "心血管外科", "1月", 120))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (3, "心内科", "1月", 122))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (4, "肝胆外科", "1月", 134))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (5, "乳甲外科", "1月", 97))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (1, "神经内科", "1月", 122))
cur.execute("INSERT INTO dept_amounts(dept_id, dept, month, amount) VALUES (?, ?, ?, ?)", (3, "心内科", "2月", 143))
conn.commit()        # ← 增删改之后必须 commit，否则数据不会真正存下去

# 查询
cur.execute("SELECT dept,month,sum(amount) FROM dept_amounts group by dept,month order by month,sum(amount) desc")   # 查询每个科室每月的接诊量总数
rows = cur.fetchall()      # 取回全部结果，形如 [("内科", "1月", 118), ...]
for row in rows:
    print(row[0], row[1], row[2])   # 每行是元组，按位置取值

conn.close()         # 用完关闭

with open("python-test/sqlites.txt", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(f'{row[0]},在{row[1]}的接诊量总数为：{row[2]}\n')