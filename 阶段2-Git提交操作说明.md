# 阶段 2 Git 提交操作说明

> 目的：把「阶段 1–2 的学习成果 + 项目结构整理」提交到 GitHub。
> 操作环境：PowerShell（Windows）。逐条复制执行即可。

---

## 一、本次提交范围

### ✅ 要提交（新增）

| 文件 / 目录 | 说明 |
|---|---|
| `phase02-data-analysis/` | SQL 练习（w1）+ pandas 全部课程与练习（w2） |
| `LEARNING_PLAN_V2.md` | 学习计划 V2 |
| `requirements.txt` | pandas / matplotlib / jupyterlab 依赖 |
| `求职/L1-实施顾问数据方向-简历骨架.md` | 简历骨架 |
| `GitHub仓库删除操作说明.md` | 仓库重建说明 |

### ✅ 要提交（修改 / 删除）

| 文件 | 动作 |
|---|---|
| `.gitignore` | 修改（新增忽略规则） |
| `README.md` | 修改 |
| `ai_practice/` 下所有旧文件 | 删除（已归档到本地 `history_file/`，不在 repo 里） |
| `GitHub仓库删除说明.md` | 删除（已改名为「操作说明」） |

### ❌ 不提交

| 文件 | 原因 |
|---|---|
| `now_file_list.jpg` | 临时截图（205KB），不是学习成果 |

---

## 二、操作步骤（PowerShell 逐条执行）

```powershell
# 0. 进入项目目录
cd E:\study_project\python-test

# 1. 添加所有改动（新增 + 修改 + 删除，一次搞定）
git add -A

# 2. 把临时截图从暂存区撤出（不提交它）
git reset -- now_file_list.jpg

# 3. 检查「即将提交」的内容：确认列表里没有 now_file_list.jpg
git status

# 4. 提交
git commit -m "阶段2收口：pandas 全部课程 + 月度报表脚本 + 项目结构整理"

# 5. 推送到 GitHub
git push
```

---

## 三、怎么确认成功

执行完 **第 3 步 `git status`** 后，应该看到：

- `Changes to be committed:` 里出现一大堆文件（`.gitignore`、`README.md`、`phase02-data-analysis/...`、`LEARNING_PLAN_V2.md` 等）
- `ai_practice/...` 显示为 `deleted:`
- **`Untracked files:` 里只剩下 `now_file_list.jpg` 一个**

看到这个状态，就可以放心执行第 4、5 步。

执行完第 5 步，终端最后几行类似：

```text
To https://github.com/1813374063/python-practice.git
   xxxxxxxx..yyyyyyyy  main -> main
```

再刷新 GitHub 仓库页面，能看到 `phase02-data-analysis/` 就成功了。

---

## 四、常见问题

**Q1：`git push` 报 SSL / 证书错误**
先试：

```powershell
git -c http.sslBackend=openssl push
```

**Q2：`git push` 提示要账号密码 / 认证失败**
说明本地没存 GitHub 凭据。用 Personal Access Token 作为密码登录，或先执行：

```powershell
git config --global credential.helper manager
```

再 push，会弹窗让你登录 GitHub。

**Q3：不想提交 `report_monthly.csv` / `result_pandas.txt`（生成的中间结果）**
这两个是 pandas 跑出来的「结果」文件，按你「三件套：md + py + 结果(csv)」的习惯**提交是合理的**。
若确实不想提交，在第 2 步再加一行：

```powershell
git reset -- phase02-data-analysis/w2-pandas/report_monthly.csv phase02-data-analysis/w2-pandas/result_pandas.txt
```

**Q4：`now_file_list.jpg` 每次 `git status` 都冒出来很烦**
直接删掉它，或在 `.gitignore` 末尾加一行：

```text
now_file_list.jpg
```

---

## 五、提交后的下一步

- 阶段 2 正式收口（M2 里程碑达成）。
- 进入 **阶段 3｜指标体系**：把 5 年业务经验写成《医院运营指标体系》，这是简历的核心资产。
