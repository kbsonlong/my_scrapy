DROP TABLE IF EXISTS dm_job;
CREATE TABLE IF NOT EXISTS dm_job
(
    job_url varchar(255) COMMENT 'job url',
    job_name varchar(255) COMMENT '岗位名称',
    job_location varchar(255) COMMENT '工作地点',
    job_desc TEXT COMMENT '岗位要求与职责',
    edu varchar(255) COMMENT '学历要求',
    language varchar(255) COMMENT '语言',
    work_year varchar(255) COMMENT '工作年限',
    salary varchar(255) COMMENT '薪资',
    company_name varchar(255) COMMENT '公司名称',
    company_desc TEXT COMMENT '公司描述',
    company_address varchar(255) COMMENT '公司地址',
    company_worktype varchar(255) COMMENT '公司成立年限',
    company_scale varchar(255) COMMENT 'company scale',
    company_website varchar(255) COMMENT '公司站点'
);

CREATE TABLE city(
	cityid VARCHAR(20) PRIMARY KEY,
	city_name VARCHAR(20),
	city_url VARCHAR(100),
	nums INT,
	detail VARCHAR(200),
	image VARCHAR(200),

	top1 VARCHAR(40),
	top1_url VARCHAR(100),
	top2 VARCHAR(40),
	top2_url VARCHAR(100),
	top3 VARCHAR(40),
	top3_url VARCHAR(100)
);

SELECT * FROM city;