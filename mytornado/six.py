# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options 
import json

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") 

class IndexHandler(tornado.web.RequestHandler):

   def get(self):
        self.write("hello itcast")

class LoginHandler(tornado.web.RequestHandler):
    """对应/login"""
    def get(self):
        self.write('<form method="post"><input type="submit" value="登陆"></form>')

    def post(self):
        self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/123", LoginHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()