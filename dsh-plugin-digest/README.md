# DSH 插件雷达（每日）

每天扫一遍三个指定站点 + 两条机器可读源，产出 1 份 `<日期>.md`，只报"今天新出现、且能装进 DSH"的东西。

## 文件

| 文件 | 内容 |
|---|---|
| `YYYY-MM-DD.md` | 当日报告（第 1 期：`2026-11-27.md`） |

## 每天的采集管道

1. **star-history/top-committers**（可抓）
   - `https://www.star-history.com/top-committers/`
   - 取人，不取仓库；只用来更新"值得盯的维护者"名单。
   - 注意 GitHub REST 未认证限流 60/小时，超了改抓网页。

2. **trendshift weekly / monthly**（抓不到列表）
   - `https://trendshift.io/weekly`、`https://trendshift.io/monthly` —— Next.js 客户端渲染，HTTP 200 但正文只有骨架。
   - 官方 API `api.trendshift.io`（OpenAPI 3.1）全部端点需 `Authorization: Bearer ts_live_…`（Signal 订阅），限速 100 req/min：
     `GET /v1/trending/weekly`、`/v1/trending/monthly`、`/v1/trending/weekly/{year}/{week}`、`/v1/trending/monthly/{year}/{month}`、`/v1/github-trending/{date}`
   - 替代口径：GitHub Search `created:>过去7天 stars:>50` / `created:>过去30天 stars:>800`，按 star 排序。缺点：只覆盖新仓库，抓不到老仓库突然涨星。

3. **机器可读源（真正的插件来源）**
   - `https://awesome-dsh-plugin.com/plugins.json` —— 13,445 条，字段：`name / owner / category / npm / stars / downloads / capabilities / capabilityRedLines / install`。
   - `https://registry.npmjs.org/-/v1/search?text=dsh-plugin&size=25` —— 补新发布。
   - `https://api.github.com/search/repositories?q=topic:dsh-plugin&sort=stars` —— 35,282 个仓库（限流时改用网页）。

## 筛选标准（按顺序）

1. 能不能装：有 `dsh.bundle`（npm 包）或 `SKILL.md`（技能）或 MCP server。
2. 有没有人用：npm 周下载量 > 300，或目录 downloads 字段靠前。
3. 是不是真做事的：仓库有测试/CI/provenance；README 不是纯营销。
4. 是否补了 DSH 的空白：代码理解、记忆、通知、体检、研究、设计。
5. 红线：`capabilities` 里出现 `network` + `env` + `shell` 全齐时要写明；AGPL/CC-BY 要标。
6. 星数只作参考：本期样本里出现过 7 个月 47.9 万星、4 周 4.4 万星、5KB 文件 1.2 万星。

## 输出的固定结构

0. 结论先说（≤4 条）
1. 三个源本期可用性（有变化才写）
2. 今日精选：3–6 个，每个含 作者 / 版本 / 许可 / 下载量 / 场景 / 为什么选它 / 装法 / 风险
3. 技能与 MCP（若有）
4. 风险与红线
5. 明日待办

## 安装路径（本机）

- `DSH_PROFILE=desktop`，`dsh` 不在 PATH → 不能用 `dsh plugin add`。
- 首选：应用内 设置 → 插件（`dshmarket`）→ 搜包名 → 安装 → 重启。
- 其次：让 agent 用 `plugin_manager` 装（会请求授权）。
- 技能：`C:\Users\15634\.dsh\skills\<name>\SKILL.md`（用户级）或 `<项目>\.dsh\skills\`（项目级），保存即生效。
