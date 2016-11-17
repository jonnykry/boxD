import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.ioloop

import boxd_api
import boxd_runner


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("./../client/index.html").generate())
        print "LOCAL: {}".format(str(self.get_query_arguments('local')))


application = tornado.web.Application([
    (r'/ws', boxd_api.SocketConnection),  # endpoint for handling websocket connections
    (r'/', MainHandler),  # endpoint for general entry
    (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './../client/static/css'}),  # static css
    (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': './../client/static/js'}),  # static js
 ])

if __name__ == "__main__":
    print 'starting'
    application.listen(os.environ.get("PORT", 5000))
    boxd_api.ConnectionManager.create()
    boxd_runner.GameRunner.create()
    tornado.ioloop.IOLoop.instance().start()
