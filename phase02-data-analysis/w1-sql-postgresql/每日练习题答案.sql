'1.1	给 tickets 每行一个全局行号，按 ticket_id 升序'
select *,row_number()over(order by t.ticket_id  ) from tickets t 

'1.2 给每个科室的工单按创建时间从早到晚编号（每科内部 1,2,3…）'
select t.*,d.dept_name,row_number()over(partition by t.dept_id  order by t.created_at  ) from tickets t 
left join departments d  on d.dept_id  = t.dept_id 

'1.3	同上，但按创建时间倒序编号（每科最新的工单是 1）'
select t.*,d.dept_name,row_number()over(partition by t.dept_id  order by t.created_at desc ) from tickets t 
left join departments d  on d.dept_id  = t.dept_id 

'1.4	给每个工程师处理的工单编号（按工程师分组，按时间排序）'
select t.*,e."name" ,row_number()over(partition by t.engineer_id order by t.ticket_id ) from tickets t 
left join engineers e on e.engineer_id  = t.engineer_id 

'1.5	找出每个科室最早的那张工单（编号=1 的）'
with ts as (select t.*,row_number()over(partition by t.dept_id order by t.created_at) as rn from tickets t )

select * from ts where  ts.rn = '1'

'1.6	。1找出每个工程师最新处理的那张工单   -- 最新处理的代表是正在处理的（刚开始未结束）'
with ts as (select t.*,row_number()over(partition by t.engineer_id  order by t.created_at desc) as rn from tickets t where t.status  not in('resolved') )

select * from ts where  ts.rn = '1'

'1.6	.2找出每个工程师最新处理的那张工单   -- 最新处理的代表是已经处理完成了'
with ts as (select t.*,row_number()over(partition by t.engineer_id  order by t.resolved_at desc ) as rn from tickets t  where t.status  = 'resolved')

select * from ts where  ts.rn = '1'

'1.7	按优先级分组给工单编号（P1 内 1,2,3…，P2 内 1,2,3…）'

select t.*,row_number()over(partition by t.priority   order by t.ticket_id ) as rn from tickets t

'1.8	.1 每科室按时间编号后，只保留每科最早的 2 条工单  按照什么时间排序 -- 开始时间'

with ts as (select t.*,row_number()over(partition by t.dept_id  order by t.created_at ) as rn from tickets t )

select * from ts where ts.rn in('1','2')



'2.1	各科室按工单量排名（RANK，降序） --是否存在并列'
select t.dept_id,count(*),rank()over(order by count(*) desc) as se from tickets t group by t.dept_id order by count(*) desc


'2.2	各科室按工单量排名（DENSE_RANK，降序），和 2.1 对比名次'
select t.dept_id,count(*),dense_rank()over(order by count(*) desc) as se from tickets t group by t.dept_id order by count(*) desc

'2.3	各工程师按处理工单量排名'

select t.engineer_id,count(*),dense_rank()over(order by count(*) desc) as se from tickets t group by t.engineer_id order by count(*) desc

'2.4	各优先级（P1/P2/P3）按工单量排名'
select t.priority,count(*),dense_rank()over(order by count(*) desc) as se from tickets t group by t.priority order by count(*) desc

'2.5	各科室按 11 月每天接诊量排名'
select v.dept_id, patient_count,dense_rank()over(order by patient_count desc)
	from visits v  
	where v.visit_month >= '2026-11-01'and v.visit_month < '2026-12-01'
	order by patient_count desc

	
'2.6	找出工单量排名第 1 的科室（RANK=1，注意并列）'
with a as(select t.dept_id,count(*),rank()over(order by count(*) desc) as se from tickets t group by t.dept_id order by count(*) desc)
select * from a where a.se = '1'

'2.7	找出工单量排名第 2 的科室（观察：并列第一时有没有"第 2 名"）'
with a as(select t.dept_id,count(*),rank()over(order by count(*) desc) as se from tickets t group by t.dept_id order by count(*) desc)
select * from a where a.se = '2'



'2.8	工单量排前三名的科室（用 DENSE_RANK<=3）'
with a as(select t.dept_id,count(*),rank()over(order by count(*) desc) as se from tickets t group by t.dept_id order by count(*) desc)
select * from a where se<=3


-- 以下内容新增了每个科室每个月（每月多天的接诊量）数据，重构脚本
'3.1	内科每月接诊量，以及上月接诊量（LAG）'
select *,lag(patient_total)over(partition by dept_name order by dept_name) from (
  select d.dept_name,date_trunc('month',v.visit_month)::date as news_month,sum(v.patient_count) patient_total from visits v 
  left join departments d 	on d.dept_id  = v.dept_id 
  where d.dept_name  = '内科'
  group by d.dept_id,date_trunc('month',v.visit_month))

"3.2	内科每月接诊量的环比增长率 （%）= (本月−上月)/上月×100   \round(公式，保留小数位数) "

select d.dept_name, v1.*,LAG(v1.patient_total)over(order by v1.news_month),
round((v1.patient_total-LAG(v1.patient_total)over(order by v1.news_month))::numeric 
	/LAG(v1.patient_total)over(order by v1.news_month)*100,2) 
  from 
    (select d.dept_id,d.dept_name,date_trunc('month',v.visit_month)::date as news_month,sum(v.patient_count) patient_total from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    where d.dept_name  = '内科'
    group by d.dept_id,date_trunc('month',v.visit_month)
    ) v1
left join departments d 	on d.dept_id  = v1.dept_id 
where d.dept_name  = '内科'
	
	
'3.3	各科室每月接诊量 + 环比增长率（按科室分区）'
select d.dept_name,v1.*,LAG(v1.patient_total)over(partition by v1.dept_id order by v1.news_month),
round((v1.patient_total-LAG(v1.patient_total)over(partition by v1.dept_id order by v1.news_month))::numeric 
	/LAG(v1.patient_total)over(partition by v1.dept_id order by v1.news_month)*100,2) from 
  (
    select d.dept_id,d.dept_name,date_trunc('month',v.visit_month)::date as news_month,sum(v.patient_count) patient_total from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    ) v1
	left join departments d 	on d.dept_id  = v1.dept_id 
	
'3.4	内科每月接诊量，以及下月接诊量（LEAD）'
WITH monthly AS (           -- 第 1 层：按(科室,月)聚合
    SELECT dept_id,
           date_trunc('month', visit_month)::date AS month_start,
           SUM(patient_count)                     AS month_total
    FROM visits
    GROUP BY dept_id, date_trunc('month', visit_month)
    order by dept_id,month_start 
),
monthly_lead AS (           -- 第 2 层：在月粒度上做 LEAD，这里是单层窗口
    SELECT dept_id,
           month_start,
           month_total,
           LEAD(month_total) OVER (
               PARTITION BY dept_id ORDER BY month_start
           ) AS next_month_total
    FROM monthly
)
SELECT d.dept_name,
       ml.month_start, 
       ml.month_total,
       ml.next_month_total
FROM visits v
JOIN departments d ON d.dept_id = v.dept_id
JOIN monthly_lead ml
  ON ml.dept_id     = v.dept_id
 AND ml.month_start = date_trunc('month', v.visit_month)::date   -- 明细行挂回所属月
ORDER BY v.dept_id,  v.visit_month;


'3.5	内科接诊量，以及"两个月前"的接诊量（LAG 偏移 2 行）   '
-- LAG(参数，偏移量)、COALESCE(值, 默认值)  →  NULL 换成默认值、NULLIF(值, 某值)      →  把"某值"变成 NULL（方向相反） '

select d.dept_name,v1.news_month,v1.patient_total,coalesce(LAG(v1.patient_total,2)over(order by v1.news_month),0) 
from (
    select d.dept_id,d.dept_name,v.patient_count,date_trunc('month',v.visit_month)::date as news_month,sum(v.patient_count) patient_total from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,v.patient_count,date_trunc('month',v.visit_month)
    ) v1
left join departments d 	on d.dept_id  = v1.dept_id 
where d.dept_name  = '内科'

'3.6	内科接诊量，以及"本月 − 上月"的差值'

select d.dept_name, v1.news_month,v1.patient_total,LAG(v1.patient_total)over(order by v1.news_month) count_by_for,
v1.patient_total-LAG(v1.patient_total)over(order by v1.news_month) as ds
from (
    select d.dept_id,d.dept_name,v.patient_count,date_trunc('month',v.visit_month)::date as news_month,sum(v.patient_count) patient_total from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,v.patient_count,date_trunc('month',v.visit_month)
    ) v1
left join departments d 	on d.dept_id  = v1.dept_id 
where d.dept_name  = '内科'

'3.7	找出各科室环比下降的月份（本月 < 上月）'

with rt as (
	select dept_id, 
  news_month,
  patient_total,
  LAG(patient_total) OVER (PARTITION BY dept_id ORDER BY news_month) AS prev_count
 from (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
    ) 
) 
select * from rt
	where patient_total < prev_count ORDER BY dept_id, news_month; 
	

'3.8	工单表：每张工单，以及同科室上一张工单的创建时间'
SELECT dept_id, ticket_id, created_at,
       LAG(created_at) OVER (PARTITION BY dept_id ORDER BY created_at) AS prev_created
FROM tickets ORDER BY dept_id, created_at;


'4.1	每张工单，以及该科室的工单总数（每行都显示）'
select *,count(t.ticket_id)over(partition by t.dept_id ) from tickets t

'4.2	内科每月接诊量的累计值（逐月累加）'
select d.dept_name,s.news_month, s.patient_total,sum(s.patient_total)over(order by s.news_month ) from  
  (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
  ) s
left join  departments d on d.dept_id = s.dept_id
where d.dept_name like '%内科%'

'4.3	各科室每月接诊量的累计值（按科室分区累计）'
select d.dept_name,s.news_month, s.patient_total,sum(s.patient_total)over(order by s.news_month ) from  
  (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
  ) s
left join  departments d on d.dept_id = s.dept_id

'4.4	各科室每月接诊量，以及该科室的平均接诊量（每行都显示）'
select 
d.dept_name,
s.news_month, 
s.patient_total,
sum(s.patient_total)over(partition by s.dept_id order by s.news_month),
round(avg(s.patient_total)over(partition by s.dept_id order by s.news_month ),2)  from  
  (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
  ) s
left join  departments d on d.dept_id = s.dept_id
order by d.dept_id,s.news_month

'4.5	各科室每月接诊量，以及该月占该科室四个月总接诊量的占比（%）' -- 不会::numeric 用法  -- 脚本写起来也不顺畅
-- ::numeric 是类型转换（cast），把整数转成"任意精度小数"。
select dept_name,news_month, patient_total,round(patient_total::numeric / sum(patient_total)over(partition by dept_id)*100,2)  as avg_count from  (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
  ) s
group by dept_name,dept_id,news_month, patient_total

'4.6各科室每月接诊总量+ 3 个月移动平均接诊总量（本月+前两个月）'  -- 解题不清晰，无法写SQL
'写法	含义
UNBOUNDED PRECEDING	分区最前面一行
n PRECEDING	当前行往前第 n 行
CURRENT ROW	当前行本身
n FOLLOWING	当前行往后第 n 行
UNBOUNDED FOLLOWING	分区最后一行'

SELECT dept_id, news_month, patient_total,
       ROUND(AVG(patient_total) OVER (PARTITION BY dept_id ORDER BY news_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moving_avg
FROM (
    select 
    d.dept_id,
    d.dept_name,
    date_trunc('month',v.visit_month)::date as news_month,
    sum(v.patient_count) as patient_total
    from visits v 
    left join departments d 	on d.dept_id  = v.dept_id 
    group by d.dept_id,date_trunc('month',v.visit_month)
    order by dept_id,date_trunc('month',v.visit_month)
  ) s
  ORDER BY dept_id, visit_month;


'4.7每张工单，以及该科室已解决工单的累计数（按时间累计）'
select *,count(t.ticket_id)over(partition by t.dept_id order by t.dept_id)  from tickets t 
where t.status = 'resolved'

'4.8各科室每月接诊量，以及该科室截至本月的历史最大值'  
select *,max(v.patient_count)over(partition by v.dept_id order by v.dept_id) from visits v 


'5.1每科室工单总量 + 名次（RANK），按名次排序展示' 

select t.*,count(t.ticket_id )over(partition by t.dept_id order by t.dept_id ),rank()over(order by t.dept_id) from tickets t 

'5.2	每科室接诊量最高的是哪个月（每科一行）'
select * from 
(select v.*,max(v.patient_count )over(partition by v.dept_id order by v.dept_id ) as max_count from visits v
)
where max_count  = patient_count 

'5.3	工单量最高的科室,工单量是多少（并列都列出）'
select s.dept_id,max(distinct s.count)  from  
(
select t.dept_id,count(t.ticket_id)over(partition by t.dept_id order by t.dept_id ) from tickets t  
)as s
group by s.dept_id,s.count
order by s.count desc


'5.4	每科室工单量，以及"比它工单多的科室有几个"（名次−1）'
select *,dense_rank()over(order by distin desc)-1 as 排名 from (
select distinct t.dept_id,count(t.ticket_id )over(partition by t.dept_id order by t.dept_id) as distin from tickets t 
order by distin desc
)

'5.5每科室按时间编号，只取每科第 2 张工单'
select * from (
select t.*,row_number()over(partition by t.dept_id order by t.dept_id,t.created_at ) from tickets t 
) where  row_number = 2

'5.6各科室每月接诊量环比，找出环比增长率最高的那条记录  ' 
"SELECT COALESCE(NULL, 'PostgreSQL', 'MySQL');  -- 返回 'PostgreSQL'coalesce()  用于替换空昵称为默认文本"
select dept_id,max(round) from (
select v.*,coalesce(lag(v.patient_count )over(order by v.dept_id),0) as last_month_count,
	coalesce(round((v.patient_count-lag(v.patient_count )over(partition by v.dept_id order by v.dept_id,v.visit_month )::numeric) 
	/ lag(v.patient_count )over(partition by v.dept_id order by v.dept_id,v.visit_month) *100,2),0) as round from visits v 
)
group by dept_id
order by max(round) desc

--------------------------------------------------------------------------
SELECT * FROM (
  SELECT dept_id, visit_month, patient_count,
         ROUND((patient_count - LAG(patient_count) OVER (PARTITION BY dept_id ORDER BY visit_month))::numeric
               / LAG(patient_count) OVER (PARTITION BY dept_id ORDER BY visit_month) * 100, 2) AS pct
  FROM visits
) t ORDER BY pct DESC NULLS LAST LIMIT 1;


'5.7	每科室工单量排名 + 该科室最早工单日期（一行展示两个信息）'
WITH dept_cnt AS (
  SELECT dept_id, COUNT(*) AS cnt FROM tickets GROUP BY dept_id
), dept_first AS (
  SELECT dept_id, MIN(created_at) AS first_date FROM tickets GROUP BY dept_id
)
SELECT dc.dept_id, dc.cnt,
       RANK() OVER (ORDER BY dc.cnt DESC) AS rk,
       df.first_date
FROM dept_cnt dc JOIN dept_first df ON df.dept_id = dc.dept_id
ORDER BY dc.dept_id;

'5.8	每科室工单量，以及它相对"第一名"差了几条'
select
	*,
	(max(count)over()-count) as 差值
from
	(
	select
		distinct t.dept_id,
		count(t.ticket_id) over(partition by t.dept_id )
		from tickets t
	order by
		count(t.ticket_id) over(partition by t.dept_id ) desc
)


select *,FIRST_VALUE(created_at) OVER (PARTITION BY dept_id ORDER BY created_at),LAST_VALUE(created_at) OVER (PARTITION BY dept_id ORDER BY created_at rows between unbounded preceding and unbounded following) 
 from tickets t 
 
 
 
 rows between unbounded preceding and unbounded following  
 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
 
 
 '6.1	把 9 个科室按工单量均分成 3 档（NTILE(3)）'   -- 余数按照首份开始逐层递增
 select dept_id,count(*),NTILE(4)over(order by count(*) desc) from tickets t 
 group by dept_id
 
 '6.2	把 35 张工单按创建时间均分成 4 组，标组号'-- 余数按照首份开始逐层递增
 
 select t.*,ntile(4)over(order by t.created_at) from tickets t 
 
 
 '6.3	每张工单 + 该科室最早工单的创建时间（FIRST_VALUE）'
 
 select t.*,first_value(t.created_at )over(partition by t.dept_id order by t.dept_id) from tickets t 
 
 '每张工单 + 该科室最新工单的创建时间（LAST_VALUE，注意坑）'
 select t.*,last_value(t.created_at )over(partition by t.dept_id order by t.dept_id rows between unbounded preceding and unbounded following) from tickets t 

'6.5	各科室每月接诊量 + 该科室第一个月接诊量'
 select v.dept_id,v.patient_count,first_value(v.patient_count)over(partition by v.dept_id order by v.dept_id,v.visit_month) from visits v 
 
 '6.6	各科室工单量，以及全局工单量最多的科室的工单量（对照 5.8)'
 
 with max_ft as(
 select distinct t.dept_id,count(t.ticket_id) over(partition by dept_id order by t.dept_id) as max_ticket  from tickets t 
 order by max_ticket desc 
 )
 select dept_id, max(max_ticket) over() from max_ft
 
 '6.7各科室工单量占比（该科室/全局总数，百分比）'
 
 select distinct t.dept_id,round(count(*)over(partition by t.dept_id)::numeric/count(*)over()*100,2) from tickets t 
 order by round(count(*)over(partition by t.dept_id)::numeric/count(*)over()*100,2) desc 
 
 

 '6.8各科室接诊量最高月份的接诊量（FIRST_VALUE + 子查询组合）'
 select dept_id, visit_month, patient_count,max(v.patient_count)over(partition by v.dept_id order by v.dept_id) from visits v

 ------------------------------------------------------------------------------------------
SELECT dept_id, visit_month, patient_count,
       FIRST_VALUE(patient_count) OVER (PARTITION BY dept_id ORDER BY patient_count DESC) AS dept_max
FROM visits ORDER BY dept_id, visit_month;


'7.1	各科室工单量 + RANK 名次 + DENSE_RANK 名次（并列看两列差别）'

select t.dept_id,count(t.ticket_id)over(partition by t.dept_id order by t.dept_id ),rank()over(order by t.dept_id ),dense_rank()over(order by t.dept_id ) from tickets t 

'7.2 各科室 11 月 vs 10 月接诊量环比，按环比降序排列    -- 如果visit_month 列，10月份出现多日（10-01、10-3），脚本应该如何修改' '数据粒度 粒度 date_trunc date_trunc('month', 日期) 把任意日期"截断"成该月 1 号：' 


WITH monthly AS (
    SELECT dept_id,
           date_trunc('month', visit_month)::date AS ym,   -- 按天归到月
           SUM(patient_count) AS total                      -- 把每天的接诊量加起来
    FROM visits
    GROUP BY dept_id, date_trunc('month', visit_month)
),
nov AS (SELECT dept_id, total FROM monthly WHERE ym = '2026-11-01'),
oct AS (SELECT dept_id, total FROM monthly WHERE ym = '2026-10-01')
SELECT n.dept_id, o.total AS oct_total, n.total AS nov_total,
       ROUND((n.total - o.total)::numeric / o.total * 100, 2) AS pct
FROM nov n
JOIN oct o ON o.dept_id = n.dept_id
ORDER BY pct DESC;


'7.3找出连续两个月下降的科室（本月<上月 且 上月<上上月）'
with 
	ds as(select dept_id,date_trunc('month',visit_month)::date as ym,sum(v.patient_count) as total from visits v 
	GROUP BY dept_id, date_trunc('month', visit_month)
),
	dsz as(
select *,lag(v.total )over(partition by v.dept_id order by ym ) count_9,lag(v.total,2 )over(partition by v.dept_id order by ym ) count_8 from ds v )

select * from dsz  
where count_8>count_9 and count_9>total

'7.4	 每科室最早工单与第二早工单的时间差（天）'
WITH ranked AS (
  SELECT dept_id, created_at,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY created_at) AS rn
  FROM tickets
), first_two AS (
  SELECT dept_id,
         MAX(created_at) FILTER (WHERE rn=1) AS d1,
         MAX(created_at) FILTER (WHERE rn=2) AS d2
  FROM ranked GROUP BY dept_id
)
SELECT dept_id, d1, d2, d2 - d1 AS gap_days
FROM first_two ORDER BY dept_id;

'7.5	各科室工单量 vs 全局平均工单量，标出"高于平均/不高于" --- avg  对应的列值列值相加然后除以行数'

SELECT dept_id, cnt,
       AVG(cnt) OVER () AS global_avg,
       CASE WHEN cnt > AVG(cnt) OVER () THEN '高于平均' ELSE '不高于平均' END AS flag
FROM (SELECT dept_id, COUNT(*) AS cnt FROM tickets GROUP BY dept_id) t
ORDER BY dept_id;

'7.6	各工程师处理工单数排名（RANK，并列同名次）'
select *,rank()over(order by cou desc ) from (
select t.engineer_id ,count(*) as cou from tickets t  group by t.engineer_id  order by count(*) desc)

'7.7各科室每月接诊量 + 3 个月移动平均 + 当月与移动平均的差值其中边界可以写这些：

写法	含义
UNBOUNDED PRECEDING	分区最前面一行
n PRECEDING	当前行往前第 n 行
CURRENT ROW	当前行本身
n FOLLOWING	当前行往后第 n 行
UNBOUNDED FOLLOWING	分区最后一行'

SELECT dept_id, visit_month, patient_count,
       ROUND(AVG(patient_count) OVER (PARTITION BY dept_id ORDER BY visit_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moving_avg,
       patient_count - ROUND(AVG(patient_count) OVER (PARTITION BY dept_id ORDER BY visit_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS diff
FROM visits ORDER BY dept_id, visit_month;

'7.8每个科室一行汇总：工单数、工单数排名、接诊总量、接诊排名、最早工单日期'
WITH t_cnt AS (
  SELECT dept_id, COUNT(*) AS ticket_cnt FROM tickets GROUP BY dept_id
),
v_sum AS (
  SELECT dept_id, SUM(patient_count) AS visit_total FROM visits GROUP BY dept_id
),
t_first AS (
  SELECT dept_id, MIN(created_at) AS first_date FROM tickets GROUP BY dept_id
)
SELECT tc.dept_id, tc.ticket_cnt,
       RANK() OVER (ORDER BY tc.ticket_cnt DESC) AS ticket_rk,
       vs.visit_total,
       RANK() OVER (ORDER BY vs.visit_total DESC) AS visit_rk,
       tf.first_date
FROM t_cnt tc
LEFT JOIN v_sum vs ON vs.dept_id = tc.dept_id
LEFT JOIN t_first tf ON tf.dept_id = tc.dept_id
ORDER BY tc.dept_id;



