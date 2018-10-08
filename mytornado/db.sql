#drop database zhangzr;
create database `zhangzr` default character set utf8;

use zhangzr;
/*
create table it_user_info (
	ui_user_id bigint(20) unsigned auto_increment comment 'yonghuid',
	ui_name varchar(64) not null comment 'yonghuming',
	ui_pass varchar(128) not null comment 'mima',
	ui_age int unsigned null comment 'niamlin',
	ui_mobile char(11) not null comment 'shoujihao',
	ui_avater varchar(128) null comment 'toux',
	ui_ctime datetime default current_timestamp comment 'chuangjshijian',
	ui_utime datetime default current_timestamp on update comment 'gengxinshijian',
	primary key(ui_user_id),
	unique (ui_mobile)
)ENGINE=InnoDB default charset=utf8 comment='renwubiao';*/

create table it_houses_info(
	id bigint(20) unsigned not null auto_increment comment '房屋编号',
	title varchar(64) not null default '' comment '标题',
	position varchar(32) not null default '' comment '位置',
	price int not null default 0,
	score int not null default 5,
	comments int not null default 0,
	primary key(id)
)ENGINE=InnoDB default charset=utf8 comment='房屋信息表';