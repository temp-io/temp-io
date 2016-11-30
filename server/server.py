#!/usr/bin/env python
# coding=utf-8

import tornado.ioloop
import tornado.web
from tornado.log import gen_log
from tornado.options import define
from tornado.options import options
from handler import UserHandler
from handler import UserIdHandler
from handler import TempHandler
from handler import TempIdHandler
from handler import TempsHandler
import db

define("port", type=int, default=8888, help="Run server on a specific port")
define("debug", type=int, default=1, help="0:false, 1:true")
       
       
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    setting = dict(
        debug=True if options.debug else False,
        login_url='/'
    )
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/user/*", UserHandler),
        (r"/users/(.+)/*", UserIdHandler),
        (r"/users/(.+)/temps/*", TempHandler),
        (r"/users/(.+)/temps/(.+)/*", TempIdHandler),
        (r"/temps", TempsHandler),
    ], **setting)

if __name__ == "__main__":
    from tornado.log import enable_pretty_logging
    enable_pretty_logging()
    options.parse_command_line()
    gen_log.info(db.uri)
    gen_log.info("http://localhost:{}".format(options.port))
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
