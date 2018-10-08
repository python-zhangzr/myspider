# coding:utf-8
from tornado.options import options, define
from tornado.web import url, RequestHandler,StaticFileHandler
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

define("port", default=8000, type=int,)

def house_title_join(titles):
    return "+".join(titles)

class IndexHandler(RequestHandler):
    def get(self):
        house_list = [
        {
            "price": 398,
            "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }]
        self.render("index.html", houses=house_list, title_join = house_title_join)
		
class ItcastHandler(RequestHandler):
	def get(self):
		self.write(dict(a=1,b=2))

class NewHandler(RequestHandler):

    def get(self):
        self.render("new.html", text="")

    def post(self):
    	self.set_header("X-XSS-Protection", 0)
        text = self.get_argument("text", "") 
        print text
        self.render("new.html", text=text)

if __name__ == "__main__":
	current_path = os.path.dirname(__file__)
	tornado.options.parse_command_line()
	app = tornado.web.Application([
			(r"/", IndexHandler),
			#(r"/", NewHandler),
			(r"/itcast", ItcastHandler),
			(r'^/()$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html"), "default_filename":"index.html"}),
		(r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
		],
		static_path=os.path.join(current_path, "statics"),
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		debug = True,
		autoescape=None)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()