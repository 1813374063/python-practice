'A1:查出所有科室的名称和类别，按 `dept_id` 升序排列 | SELECT / ORDER BY |'
select * from departments order by dept_id 

'A2 统计每个科室的工单数量，按数量降序 | GROUP BY + COUNT |'
select d.dept_name,count(t.ticket_id) from tickets t  
left join departments d  on d.dept_id  = t.dept_id 
group by t.dept_id,d.dept_name   order by count(t.ticket_id) desc 

'A3 找出 2026 年 10 月创建的工单（注意日期口径用「闭开区间」） | WHERE + 日期范围 |'
select * from visits v where v.visit_month >='2026-10-01' and v.visit_month <='2026-10-31'

'A4 各优先级（P1/P2/P3）的工单分别有多少 | GROUP BY priority |'
select t.priority,COUNT(T.ticket_id ) from tickets T group by t.priority   order by t.priority

'A5 已解决工单（resolved / closed）的平均处理天数 | 日期相减 + 口径 |'
SELECT AVG(resolved_at - created_at)*24 AS 平均处理天数
FROM tickets
WHERE status IN ('resolved', 'closed');

---------------------------------------------------------------
'按照小时计算 首先这个"1 天"实际可能只过了 2 小时（10-20 23:59 提交、10-21 00:01 解决），也可能过了 40 小时所以"0.4 个自然日 × 24 = 9.6 小时"是没有意义的——它把"跨了 1 个自然日"粗暴当成"耗时 24 小时"了。正确结论：用 date 类型，只能回答"平均处理天数 = 0.4 天"，算不出真实的"小时"。要算小时，列得是 timestamp 类型（带时分秒），那时 resolved_at - created_at 会返回 interval，再换算成小时'


'B1 列出每张工单的科室名称、类别、优先级、状态 | 内连接 |'
select d.dept_name ,t.category , t.priority  ,t.status  from departments d
join tickets t   on t.dept_id   = d.dept_id 
order by d.dept_name 

'B2 找出**没有任何工单**的科室 | LEFT JOIN + IS NULL / NOT EXISTS |  
    "EXISTS (子查询)    → 子查询有没有返回至少 1 行？有 → TRUE，没有 → FALSE
    NOT EXISTS (子查询) → 反过来：一行都没有 → TRUE"'

select * from departments d
left join  tickets t  on t.dept_id  = d.dept_id 
where t.ticket_id  is null

---------------------------------------------------------
' 为什么写 SELECT 1 而不是 SELECT *？

因为 EXISTS 只关心"有没有行"，不关心行里是什么内容。SELECT 1 是约定俗成的写法，意思是"有就随便返回个 1，占位而已"。写 SELECT * 也能跑，但 SELECT 1 语义更清楚（"我只要知道存不存在"）。'
SELECT dept_name FROM departments d
WHERE NOT EXISTS (
    SELECT 1 FROM tickets t WHERE t.dept_id = d.dept_id
);


'B3 每个科室的工单数，**包含 0 工单的科室**（共 9 行） | LEFT JOIN + COUNT(字段) 而非 COUNT(*) |'
select d.dept_name,count(t.ticket_id ) from departments d 
left join  tickets t on t.dept_id  = d.dept_id 
group by d.dept_id,d.dept_name 
order by count(t.ticket_id ) desc




'B4 每个工程师处理的工单数，**包含没处理过工单的工程师** | engineers LEFT JOIN tickets |'
select e.name,count(t.ticket_id ) from engineers e 
left join tickets t  on e.engineer_id  = t.engineer_id 
group by e.engineer_id,e.name
order by e.engineer_id



'C1 找出工单数量最多的科室（并列也要都列出来） | 子查询 + MAX / HAVING |  筛选分组后的各组数据'

SELECT d.dept_name, sub.cnt
FROM (
    SELECT dept_id, COUNT(*) AS cnt
    FROM tickets
    GROUP BY dept_id
    HAVING COUNT(*) = (
        SELECT COUNT(*) FROM tickets GROUP BY dept_id ORDER BY COUNT(*) desc limit 1
    )
) sub
JOIN departments d ON d.dept_id = sub.dept_id;


'C2 | 找出「有 P1 工单」的科室名称 | EXISTS / IN |'

select distinct(d.dept_name )  from tickets t  
left join 
departments d  on t.dept_id  = d.dept_id 
where t.priority  in ('P1')
--------------------------------------------
select d.dept_name from departments d 
where exists(select * from tickets t where t.dept_id = d.dept_id and t.priority in ('P1') )


'C3 | 找出工单数量**高于所有科室平均值**的科室 | 子查询 AVG |'

select t2.dept_id ,count(*) as sd from tickets t2 
group by t2.dept_id 
having count(*) > (select AVG(c) from (select d.dept_id,count(t.ticket_id) as c from departments d left join  tickets t on t.dept_id = d.dept_id group by d.dept_id )as sub) 



' D1 | 给每个科室的工单按创建时间从早到晚编号（每科内部 1,2,3…） | ROW_NUMBER + PARTITION BY |'

SELECT d.dept_name,row_number()over(partition by t.dept_id order by t.created_at ) as rn from tickets t  
left join departments d  on d.dept_id  = t.dept_id 

' D2 | 各科室按工单量排名，并列同名次（第 1、2、2、4…） | RANK |'
SELECT dept_id, COUNT(*) AS cnt,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rk
FROM tickets
GROUP BY dept_id
ORDER BY dept_id;

'd3 内科每个月的接诊量，以及环比增长率（%）'
SELECT visit_month, patient_count,
       LAG(patient_count) OVER (ORDER BY visit_month) AS prev_count,
       ROUND(
         (patient_count - LAG(patient_count) OVER (ORDER BY visit_month))::numeric
         / LAG(patient_count) OVER (ORDER BY visit_month) * 100, 2
       )  AS pct_change
FROM visits
WHERE dept_id = 1
ORDER BY visit_month;

'D4 每个科室接诊量的累计值（按时间累积） |（累计：加 ORDER BY 才逐行累加）'
SELECT D.dept_name , V.visit_month, V.patient_count,
       SUM(v.patient_count) OVER (PARTITION BY v.dept_id ORDER BY v.visit_month) AS running_total
FROM visits V
left join departments d on d.dept_id = V.dept_id 
ORDER BY v.dept_id, v.visit_month;



'E1 | 用 `WITH`（CTE）拆解：算出各科室**月均接诊量**，列出 Top 3 | WITH + GROUP BY + ORDER BY + LIMIT |'
with practice_visit AS(select v.dept_id,v.visit_month ,sum(v.patient_count ) as vi_count from visits v  group by v.dept_id ,v.visit_month order by v.dept_id ,v.visit_month)

select dept_id,avg(vi_count) from practice_visit group by dept_id order by avg(vi_count) limit 3 desc



'E2 | 口径讨论题（写文字，不写 SQL）：同一个月的「工单量」和「接诊量」有没有可比性？如果领导要一张"科室运营总览"，你会怎么定义每列的指标口径？ | 指标口径 / 业务判断 |'

同一个月的工单量和接诊量没有可比性，是两个不同的指标，工单量指的是所提交的工单数量，而接诊量是指的医生对患者的诊疗量。
首先科室运营总览表，肯定存在：接诊量(医生实际保存病历的数量)、处方数(处方有效签名的数量)、分科室收入及当日总收(药品、诊疗、诊查费等收入及及每日相加汇总)，收入、接诊人数的每月环比增长率(以上个月的诊疗人数为分母，（本月的诊疗人次减去上月的诊疗人次）/ 上月的诊疗人次*100，保留2位小数）
