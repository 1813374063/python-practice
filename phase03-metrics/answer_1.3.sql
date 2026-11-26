 '''**1.1** 用两种口径算「工单解决率」，看差多少：
 口径 A：`status = 'resolved'` 的数量 / 总工单数
 口径 B：`status IN ('resolved','closed')` 的数量 / 总工单数'''

select
round(count(*)filter(where status = 'resolved')* 100.0/count(*),2),
round(count(*)filter(where status in('resolved','closed'))* 100.0 /count(*),2)

 from tickets t
'**1.2** 这两个数差这么多，如果你在报表里只写「解决率 70%」（不写口径），可能会出什么问题？'

print('实际解决率较低。')

'**2.1** 算出 8–11 月每个月的**总接诊量**（按月份汇总）。'

select v.visit_month,sum(v.patient_count) from visits v group by v.visit_month order by v.visit_month desc 

'**2.2** 算出每个科室的**接诊量占比**（4 个月合计 / 总接诊量），按占比降序。'
'对比：'

SELECT d.dept_name,
       SUM(v.patient_count) AS 接诊量,
       ROUND(SUM(v.patient_count) * 100.0 / (SELECT SUM(patient_count) FROM visits), 2) AS 占比
FROM visits v
JOIN departments d ON d.dept_id = v.dept_id
GROUP BY d.dept_name
ORDER BY 接诊量 DESC;

'**2.3** 算出**工单状态分布**（每个 status 有多少条）。'
select status,count(ticket_id) from tickets 
    group by status 
    order by count(ticket_id) desc

'**2.4** 算出 **P1 工单占比**（P1 数 / 总工单数）。'
SELECT ROUND(COUNT(*) FILTER (WHERE priority = 'P1') * 100.0 / COUNT(*), 2) AS p1占比
FROM tickets;

'**2.5** 算出每个科室的**工单数**（按上报科室 dept_id 统计，含没有工单的科室）。'

select d.dept_id,count(t.ticket_id) 
from departments d
left join tickets t on d.dept_id = t.dept_id
group by t.dept_id

'**3.1** 用「加法拆解」：11 月比 10 月，每个科室的接诊量**变化了多少**（列：科室、10月、11月、变化）。'
SELECT d.dept_name,
       SUM(CASE WHEN v.visit_month = '2026-10-01' THEN v.patient_count ELSE 0 END) AS 十月,
       SUM(CASE WHEN v.visit_month = '2026-11-01' THEN v.patient_count ELSE 0 END) AS 十一月,
       SUM(CASE WHEN v.visit_month = '2026-11-01' THEN v.patient_count ELSE 0 END)
         - SUM(CASE WHEN v.visit_month = '2026-10-01' THEN v.patient_count ELSE 0 END) AS 变化
FROM visits v
JOIN departments d ON d.dept_id = v.dept_id
WHERE v.visit_month IN ('2026-10-01','2026-11-01')
GROUP BY d.dept_name
ORDER BY 变化;
------------------------------------------------------------------------------
'每个科室的每月接诊量占每科室总接诊量的占比'
select dept_id,
       visit_month,
       monthly_total,
       sum(monthly_total) over (partition by dept_id) as dept_total
from (
    select v.dept_id,
           date_trunc('month',visit_month)::date as visit_month,
           sum(v.patient_count) as monthly_total
    from visits v
    group by v.dept_id, date_trunc('month',visit_month)::date
) t
order by dept_id, visit_month;

'**3.2** 从 3.1 的结果看，**哪个科室对总下降贡献最大**？它贡献了多少？'
'内科贡献最大， 下降了300'

'**3.3** 总接诊量 11 月 vs 10 月，**环比**是多少（百分比）？'

select *,
lag(monthly_total)over() ,
round((monthly_total-lag(monthly_total)over())::numeric * 100.0/(lag(monthly_total)over())::numeric,2) 占比
from
( select 
           date_trunc('month',visit_month)::date as visit_month,
           sum(v.patient_count) as monthly_total

    from visits v
    where visit_month in ('2026-10-01','2026-11-01')
    group by  date_trunc('month',visit_month)::date
    order by date_trunc('month',visit_month)::date
    ) 

'4.把「为什么本月（11月）门诊量下降？」按金字塔结构写出来：

```text
结论：11 月门诊量 9860，环比 10 月（10480）下降 5.92%，主因是内科（-300 人次，贡献约 48% 的降幅）。

数据支撑：
- 总量：10月 10480 → 11月 9860，环比 -620（-5.92%）
- 拆解：内科 -300、门诊部 -150、急诊科 -70、外科 -30、检验科 -30、儿科 -50、放射科 -20、药房 +30

建议：核查内科 11 月排班/停诊/系统故障记录；对比去年同期判断是否季节性；对门诊部同步排查。

要求：结论里要说出「下降多少 + 主要是谁拖累的」，并引用你 3.1/3.2/3.3 算出的数。'


'5.业务问题：**「这个月信息科的工单压力是不是变大了？」**

请写出至少 3 个指标（+ 每个指标一句 SQL 思路），并说明你会用哪 1 个指标下结论。'
"
指标 1：**工单总量**——`SELECT COUNT(*) FROM tickets WHERE created_at >= '2026-11-01';`
指标 2：**P1 工单占比**——P1 数 / 总工单数（P1 代表高压力）。
指标 3：**未解决工单数**——`status IN ('open','processing')` 的数量（积压 = 压力）。
指标 4：**工单平均处理时长**——`AVG(resolved_at - created_at)`（效率下降 = 压力）。
指标 5：**工程师人均负载**——按 engineer_id 分组的工单数。
"