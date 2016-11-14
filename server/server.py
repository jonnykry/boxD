from boxd_api import BoxdApi, SocketConnection
import boxd_runner
import tornado.template
import tornado.web
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("./../client/index.html").generate())


application = tornado.web.Application([
    (r'/ws', SocketConnection),  # endpoint for handling websocket connections
    (r'/', MainHandler),  # endpoint for general entry
    (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './../client/static/css'}),  # static css
 ])

if __name__ == "__main__":
    print 'starting'
    BoxdApi.create()
    boxd_runner.GameRunner.create()
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()

