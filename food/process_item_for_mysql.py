# -*- coding:utf-8 -*-

import redis
import MySQLdb
import json

def process_item():
    rediscli = redis.Redis(host = "10.200.135.34", port = 6379, db = 0)
    mysqlcli = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "zhangzr", passwd = "mysql", db = "python",charset="utf8")
    offset = 1
    while True:
        source, data = rediscli.blpop("foods:items")
        item = json.loads(data)
        try:
            cursor = mysqlcli.cursor()
            cursor.execute("insert into foods (id,foodname, critic, criticnum, popular, popularnum, imageurl) values (%s,%s, %s, %s, %s, %s, %s)", [offset,item['foodname'], item['critic'], item['criticnum'], item['popular'],item['popularnum'],item['imageurl']])
            mysqlcli.commit()
            cursor.close()
            offset += 1
            print offset
        except:
            raise
if __name__ == "__main__":
    process_item()
