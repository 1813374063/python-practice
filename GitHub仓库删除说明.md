# GitHub 仓库手动删除说明

> 适用：手动删除你自己的 GitHub 仓库，以及清空学习仓库重新开始。
> 本文档覆盖三个仓库：
> - https://github.com/1813374063/python-practice（**清空重来**：删除后重建）
> - https://github.com/1813374063/WebPRA（直接删除）
> - https://github.com/rddmwmddr/android-ad-cleaner（直接删除，需能登录 rddmwmddr 账户）

---

## 一、删除前必读（重要）

1. **删除不可逆。** GitHub 不会回收已删除的仓库，删除后代码、提交历史、Issues、PR、Wiki、Release、Settings 全部消失。
2. `WebPRA` 约 110MB，2026-05 停更；`android-ad-cleaner` 昨天（11-10）还在更新。删前务必确认这两个项目不再需要。
3. 只有仓库的 **Owner（所有者）** 才能删除；协作者无删除权限。
4. `android-ad-cleaner` 属于账户 `rddmwmddr`，不是 `1813374063`。若你无法登录 `rddmwmddr`，则无法删除它，只能联系该账户所有者。

---

## 二、网页端删除步骤（每个仓库重复一遍）

1. 用浏览器登录仓库所属的 GitHub 账户。
2. 打开仓库首页（就是上面两个链接）。
3. 点击顶部右侧的 **Settings**（设置）标签页。
   - 注意：如果看不到 Settings，说明你不是 Owner，没有删除权限。
4. 在 Settings 页面**滚动到最底部**，找到 **Danger Zone**（危险区域）。
5. 点击 **Delete this repository**（删除此仓库）按钮。
6. 在弹出的确认框中，先点击按钮 **"I have read and understand these effects"**（我已阅读并理解这些后果）。
7. 在输入框里输入**完整的仓库名**（区分大小写）：
   - 删 WebPRA → 输入 `WebPRA`
   - 删 android-ad-cleaner → 输入 `android-ad-cleaner`
8. 点击 **Delete this repository** 确认。
9. 若 GitHub 要求，输入账户密码或进行二次验证（2FA）。
10. 页面跳转后，仓库即已删除。

> 提示：仓库下有多个分支（如 android-ad-cleaner 有几十个 release 分支、WebPRA 有 main 和 master）不影响删除，删除是针对整个仓库，不是单个分支。

---

## 三、命令行 API 方式（可选，替代网页）

如果你更愿意用命令删除，需要准备一个勾选 **`delete_repo`** 权限的经典 PAT（Personal Access Token），然后执行：

```bash
curl -X DELETE \
  -H "Authorization: Bearer 你的TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/所有者/仓库名
```

示例（删除 WebPRA）：

```bash
curl -X DELETE \
  -H "Authorization: Bearer ghp_xxxxxxxxxxxx" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/1813374063/WebPRA
```

返回 `204 No Content` 即删除成功；返回 `404` 是仓库不存在；返回 `403` 是 TOKEN 无 `delete_repo` 权限或你不是所有者。

---

## 四、注意事项

| 情况 | 处理 |
|---|---|
| 看不到 Settings 标签 | 你不是 Owner，无删除权限 |
| 确认框输错仓库名 | 删除按钮保持不可点，核对后重输 |
| 提示需要二次验证 | 按要求完成 2FA / 输入密码 |
| 删完想找回 | 个人账户一般不可找回；除非走 GitHub Support（不保证） |
| `android-ad-cleaner` 登录不了 rddmwmddr | 无法删除，只能让账户所有者处理 |

---

## 五、python-practice：清空学习内容、重新开始

你想保留仓库名和地址，但把旧的 14 个提交历史清空、从头开始。**网页端无法直接清空提交历史**，所以最省事的手动做法是「删除旧仓库 → 重建同名空仓库」。

### 第一步：删除旧仓库

按上面「二、网页端删除步骤」操作，仓库名输入 `python-practice`，把它删掉。

### 第二步：重建同名空仓库

1. 仍登录 `1813374063` 账户。
2. 点右上角 **+** → **New repository**。
3. **Repository name** 填 `python-practice`（与原来同名）。
4. **Public / Private** 按需选择（原来的是 Public，想公开就选 Public）。
5. **不要勾选** "Add a README / .gitignore / license"（保持完全空白，方便下一步从本地推）。
6. 点 **Create repository**。

> 也可以在重建时勾选 "Add a README file"，GitHub 会生成一个含 README 的空仓库，效果一样（只是多一个初始提交）。

### 第三步：本地仓库重新连上新的远程（关键）

你本地的 `E:\study_project\python-test` 还是旧历史、旧提交。重建后有两个选择：

**选择 A（推荐，彻底重开）：保留本地学习文件，但重置 git 历史**

```bash
cd E:\study_project\python-test
# 本地已有完整备份 repo-backup-20261111.bundle，下面操作不影响备份
# 1. 删除旧的 .git（仅删 git 历史元数据，不动你的 .py/.md 学习文件）
# 2. 重新初始化
# 3. 把新的远程地址接上
# 4. 正常 add / commit / push
```

具体命令：

```bash
cd E:\study_project\python-test
git remote -v        # 确认记住原地址 https://github.com/1813374063/python-practice.git

# 删除旧 git 历史（学习文件本身保留在磁盘上）
Remove-Item -Recurse -Force .git

git init
git branch -M main
git remote add origin https://github.com/1813374063/python-practice.git
git add .
git commit -m "重新开始：AI+数据分析学习"
git push -u origin main
```

> 执行前确认 `.gitignore` 里已有 `key.txt`、`*.db`、`__pycache__/`，避免把密钥或临时文件推上去。

**选择 B：保留旧历史，只往后继续提交**

如果你还想要那 14 个旧提交，就不删旧仓库，直接继续用现在的本地仓库往后 commit、push 即可，无需任何操作。

### 说明

- 以上「选择 A」会清空**本地 git 历史**，但你的 `.py`、`.md`、`.json` 等学习文件都还在磁盘上，不会丢。
- 旧内容随时可从备份还原：`git clone repo-backup-20261111.bundle 旧目录` 即可把旧历史整体恢复出来。
- 如果你不想自己敲这些命令，**本地这一步我可以直接帮你做**（纯本地操作，不需要任何 token），你只需告诉我选 A 还是选 B。

---

## 六、建议操作顺序

```text
1. 登录 1813374063 → 删除 python-practice（并按第五节重建）
2. 登录 1813374063 → 删除 WebPRA
3. 登录 rddmwmddr → 删除 android-ad-cleaner（若你掌握该账户）
4. 每删一个之前，各自确认一遍：代码里有没有还需要的文件/密钥/数据
5. 完成后，本地 python-test 按第五节「第三步」决定重开或保留
```
