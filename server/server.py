import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

# WS_HANDLERS maintains a list of currently-opened ws connections
WS_HANDLERS = []


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("../client/index.html").generate())


class WSHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print 'connection opened.'
        WS_HANDLERS.append(self)
        self.write_message("The server says Hello")

    def on_message(self, message):

        # iterate over our list of connections and forward the message to each
        for ws_handler in WS_HANDLERS:

            # if the connection we're about to send to is the one who sent the message
            if ws_handler is self:
                name = "You"  # refer to the client as "you"
            else:
                name = "A client"  # refer to the client as "A client"

            ws_handler.write_message("{} said:  {}".format(name, message))

        print 'message received:  {}'.format(message)

    def on_close(self):
        WS_HANDLERS.remove(self)  # remove the closed connection from our list of handlers

        # let the other clients know someone left
        for ws_handler in WS_HANDLERS:
            ws_handler.write_message('somebody left')

        print 'connection closed...'


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
    print 'starting'
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
