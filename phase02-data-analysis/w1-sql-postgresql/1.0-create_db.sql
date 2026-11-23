-- ============================================================
-- 医院信息科练习库（PostgreSQL）—— 一键建库文件
--
-- 作用：创建数据库 hospital_practice，建 4 张表，导入练习数据，
--       并在最后打印各表行数做验证。
--
-- 运行方式（装好 PostgreSQL 后，打开命令行执行）：
--     psql -U postgres -f "本文件完整路径"
--   （首次会提示输入 postgres 用户密码）
--
-- 注意事项：
--   1. CREATE DATABASE 不能在事务里执行，请直接用 psql -f 运行，
--      不要加 --single-transaction。
--   2. 本文件可重复运行：会先删除旧库再重建，等于"重置数据库"。
--   3. 中文数据要求库编码为 UTF8，已在 CREATE DATABASE 里指定。
-- ============================================================

DROP DATABASE IF EXISTS hospital_practice;
CREATE DATABASE hospital_practice
    WITH ENCODING 'UTF8'
    TEMPLATE template0;

\c hospital_practice
SET client_encoding = 'UTF8';

-- ============ 建表 ============

DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS visits CASCADE;
DROP TABLE IF EXISTS engineers CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- 科室维度表
CREATE TABLE departments (
    dept_id   SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    category  VARCHAR(20) NOT NULL,   -- 临床 / 医技 / 职能
    head_name VARCHAR(30)
);

-- 信息科工程师表
CREATE TABLE engineers (
    engineer_id SERIAL PRIMARY KEY,
    name        VARCHAR(30) NOT NULL,
    level       VARCHAR(10) NOT NULL  -- 初级 / 中级 / 高级
);

-- 工单表（dept_id 是"上报工单的科室"）
CREATE TABLE tickets (
    ticket_id   SERIAL PRIMARY KEY,
    dept_id     INTEGER REFERENCES departments(dept_id),
    category    VARCHAR(20) NOT NULL,  -- 终端与外设/网络与通信/账号与权限/业务系统/接口与集成/数据与报表/需求与流程
    priority    VARCHAR(3)  NOT NULL,  -- P1 / P2 / P3
    status      VARCHAR(12) NOT NULL,  -- open / processing / resolved / closed
    engineer_id INTEGER REFERENCES engineers(engineer_id),
    created_at  DATE NOT NULL,
    resolved_at DATE
);

-- 门诊接诊量表（按月汇总，visit_month 取每月 1 号）
CREATE TABLE visits (
    visit_id      SERIAL PRIMARY KEY,
    dept_id       INTEGER REFERENCES departments(dept_id),
    visit_month   DATE NOT NULL,
    patient_count INTEGER NOT NULL CHECK (patient_count >= 0)
);

-- ============ 导入数据 ============

INSERT INTO departments (dept_name, category, head_name) VALUES
('内科', '临床', '张主任'),
('外科', '临床', '李主任'),
('儿科', '临床', '王主任'),
('检验科', '医技', '赵主任'),
('放射科', '医技', '钱主任'),
('门诊部', '临床', '孙主任'),
('药房', '医技', '周主任'),
('急诊科', '临床', '吴主任'),
('护理部', '职能', '郑主任');

INSERT INTO engineers (name, level) VALUES
('张伟', '高级'),
('李娜', '中级'),
('王强', '初级'),
('赵敏', '初级');   -- 赵敏暂无工单，用于 LEFT JOIN 练习

INSERT INTO tickets (dept_id, category, priority, status, engineer_id, created_at, resolved_at) VALUES
(1, '终端与外设', 'P2', 'resolved',   3, '2026-09-03', '2026-09-03'),
(1, '账号与权限', 'P2', 'closed',     2, '2026-09-10', '2026-09-10'),
(1, '数据与报表', 'P2', 'open',       1, '2026-10-15', NULL),
(2, '接口与集成', 'P1', 'resolved',   1, '2026-09-05', '2026-09-05'),
(2, '网络与通信', 'P2', 'processing', 3, '2026-11-01', NULL),
(3, '需求与流程', 'P3', 'closed',     2, '2026-10-08', '2026-10-10'),
(4, '接口与集成', 'P1', 'resolved',   1, '2026-09-12', '2026-09-12'),
(4, '业务系统',   'P2', 'resolved',   2, '2026-10-20', '2026-10-21'),
(4, '接口与集成', 'P1', 'open',       1, '2026-11-05', NULL),
(6, '终端与外设', 'P2', 'resolved',   3, '2026-10-02', '2026-10-02'),
(6, '数据与报表', 'P1', 'processing', 1, '2026-11-02', NULL),
(7, '账号与权限', 'P3', 'closed',     3, '2026-09-20', '2026-09-21'),
(8, '业务系统',   'P1', 'resolved',   1, '2026-10-25', '2026-10-25'),
(8, '网络与通信', 'P2', 'open',       2, '2026-11-08', NULL),
(1, '接口与集成', 'P1', 'resolved',   1, '2026-11-03', '2026-11-03'),
(1, '账号与权限', 'P2', 'resolved',   2, '2026-09-15', '2026-09-15'),
(1, '业务系统',   'P1', 'resolved',   1, '2026-10-12', '2026-10-12'),
(4, '数据与报表', 'P2', 'closed',     2, '2026-09-18', '2026-09-19'),
(4, '终端与外设', 'P3', 'resolved',   3, '2026-10-05', '2026-10-05'),
(4, '业务系统',   'P2', 'processing', 1, '2026-11-06', NULL),
(2, '账号与权限', 'P2', 'resolved',   3, '2026-09-22', '2026-09-22'),
(2, '数据与报表', 'P3', 'closed',     2, '2026-10-18', '2026-10-20'),
(2, '终端与外设', 'P2', 'open',       3, '2026-11-10', NULL),
(6, '需求与流程', 'P3', 'closed',     2, '2026-09-25', '2026-09-27'),
(6, '网络与通信', 'P2', 'resolved',   1, '2026-10-22', '2026-10-22'),
(6, '业务系统',   'P1', 'processing', 1, '2026-11-09', NULL),
(8, '接口与集成', 'P1', 'resolved',   1, '2026-09-28', '2026-09-28'),
(8, '终端与外设', 'P2', 'resolved',   3, '2026-10-11', '2026-10-11'),
(8, '账号与权限', 'P2', 'open',       2, '2026-11-11', NULL),
(3, '网络与通信', 'P2', 'resolved',   3, '2026-10-09', '2026-10-09'),
(3, '需求与流程', 'P3', 'closed',     2, '2026-11-07', '2026-11-08'),
(7, '终端与外设', 'P3', 'resolved',   3, '2026-09-30', '2026-09-30'),
(7, '业务系统',   'P2', 'processing', 2, '2026-10-27', NULL),
(5, '终端与外设', 'P3', 'resolved',   3, '2026-10-14', '2026-10-14'),
(9, '需求与流程', 'P3', 'closed',     2, '2026-11-12', '2026-11-13');

INSERT INTO visits (dept_id, visit_month, patient_count) VALUES
(1, '2026-08-01', 1200), (1, '2026-09-01', 1250), (1, '2026-10-01', 1180), (1, '2026-11-01',  880),
(2, '2026-08-01',  980), (2, '2026-09-01', 1000), (2, '2026-10-01', 1020), (2, '2026-11-01',  990),
(3, '2026-08-01',  760), (3, '2026-09-01',  810), (3, '2026-10-01',  900), (3, '2026-11-01',  850),
(4, '2026-08-01', 1500), (4, '2026-09-01', 1480), (4, '2026-10-01', 1520), (4, '2026-11-01', 1490),
(5, '2026-08-01', 1100), (5, '2026-09-01', 1120), (5, '2026-10-01', 1150), (5, '2026-11-01', 1130),
(6, '2026-08-01', 2200), (6, '2026-09-01', 2300), (6, '2026-10-01', 2250), (6, '2026-11-01', 2100),
(7, '2026-08-01',  600), (7, '2026-09-01',  620), (7, '2026-10-01',  610), (7, '2026-11-01',  640),
(8, '2026-08-01', 1800), (8, '2026-09-01', 1750), (8, '2026-10-01', 1850), (8, '2026-11-01', 1780);

-- ============ 验证 ============

\echo ''
\echo '=== 建库完成，各表行数如下（应为 9 / 4 / 15 / 32）==='
SELECT 'departments' AS 表名, count(*) AS 行数 FROM departments
UNION ALL SELECT 'engineers', count(*) FROM engineers
UNION ALL SELECT 'tickets', count(*) FROM tickets
UNION ALL SELECT 'visits', count(*) FROM visits;
