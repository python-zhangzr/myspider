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
import datetime

define("port", default=8000, type=int,)

class IndexHandler(RequestHandler):
	def get(self):
		cookie = self.get_secure_cookie("count")
		count = int(cookie) + 1
		self.set_secure_cookie("count", str(count))
		self.write(
			'<html><head><title>Cookie计数器</title></head>'
			'<body><h1>您已访问本页%d次。</h1>' % count + 
			'</body></html>'
		)
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
		]
		settings=dict(
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		static_path=os.path.join(os.path.dirname(__file__), "statics"),
		debug = True,
		autoescape=None,
		cookie_secret = "2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
		xsrf_cookies = True
		)
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