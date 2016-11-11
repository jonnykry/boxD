import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("client/index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
    self.write_message("The server says: " + message + " back at you")
    print 'received:', message

  def on_close(self):
    print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r'/css/(.*)', tornado.web.StaticFileHandler, {path='static/css'})
])

if __name__ == "__main__":
  application.listen(9090)
  tornado.ioloop.IOLoop.instance().start()
