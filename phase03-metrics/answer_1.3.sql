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