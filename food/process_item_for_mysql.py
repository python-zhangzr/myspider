#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import MySQLdb
import json

def process_item():
    # 创建redis数据库连接
    rediscli = redis.Redis(host = "192.168.43.62", port = 6379, db = 0)

    # 创建mysql数据库连接
    mysqlcli = MySQLdb.connect(host = "127.0.0.1", port = 3306, \
        user = "root", passwd = "mysql", db = "foods")

    offset = 0

    while True:
        # 将数据从redis里pop出来
        source, data = rediscli.blpop("food:items")
        item = json.loads(data)
        try:
            # 创建mysql 操作游标对象，可以执行mysql语句
            cursor = mysqlcli.cursor()

            cursor.execute("insert into foods (foodname, critic, criticnum, popular, popularnum, imangeurl) values (%s, %s, %d, %s, %d, %s)", [item['foodname'], item['critic'], item['criticnum'], item['popular'],item['popularnum'],item['imangeurl']])
            # 提交事务
            mysqlcli.commit()
            # 关闭游标
            cursor.close()
            offset += 1
            print offset
        except:
            pass

if __name__ == "__main__":
    process_item()
