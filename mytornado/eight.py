# coding:utf-8
from tornado.options import options, define
from tornado.web import url, RequestHandler,StaticFileHandler
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import torndb
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

define("port", default=8000, type=int,)
class GetHandler(RequestHandler):
    def get(self):
        """访问方式为http://127.0.0.1/get?id=111"""
        hid = self.get_argument("id")
        try:
            ret = self.application.db.get("select title,position,price,score,comments from houses where id=%s", hid)
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            print type(ret)
            print ret
            print ret.title
            print ret['title']
            self.render("index.html", houses=[ret])


class QueryHandler(RequestHandler):
    def get(self):
        """访问方式为http://127.0.0.1/query"""
        try:
            ret = self.application.db.query("select title,position,price,score,comments from houses limit 10")
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            self.render("index.html", houses=ret)
class InsertHandler(RequestHandler):
    def post(self):
        title = self.get_argument("title")
        position = self.get_argument("position")
        price = self.get_argument("price")
        score = self.get_argument("score")
        comments = self.get_argument("comments")
        try:
            ret = self.application.db.execute("insert into houses(title, position, price, score, comments) values(%s, %s, %s, %s, %s)", title, position, price, score, comments)
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            self.write("OK %d" % ret)

class ItcastHandler(RequestHandler):
	def get(self):
		self.write(dict(a=1,b=2))
		
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/view", InsertHandler),
        ]
        settings=dict(
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
		debug = True,
		autoescape=None)
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="itcast",
            user="zhangzr",
            password="mysql"
        )

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()