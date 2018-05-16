DROP TABLE IF EXISTS dm_job;
CREATE TABLE IF NOT EXISTS dm_job
(
    job_url varchar(255) COMMENT 'job url',
    job_name varchar(255) COMMENT '岗位名称',
    job_location varchar(255) COMMENT '工作地点',
    job_desc varchar(255) COMMENT '岗位要求与职责',
    edu varchar(255) COMMENT '学历要求',
    language varchar(255) COMMENT '语言',
    work_year varchar(255) COMMENT '工作年限',
    salary varchar(255) COMMENT '薪资',
    company_name varchar(255) COMMENT '公司名称',
    company_desc varchar(255) COMMENT '公司描述',
    company_address varchar(255) COMMENT '公司地址',
    company_worktype varchar(255) COMMENT '公司成立年限',
    company_scale varchar(255) COMMENT 'company scale',
    company_website varchar(255) COMMENT '公司站点'
)