import tornado.websocket


class ConnectionManager(object):

    def __init__(self):
        self.connections = {}

    def connected_clients(self):
        return len(self.connections)

    def get_connections(self):
        return self.connections

    def send_message(self, client_id, message):

        if client_id not in self.connections:
            raise ValueError("Client id not found in connections!  ({})".format(str(client_id)))

        if not isinstance(self.connections[client_id], SocketConnection):
            pass


        self.connections[client_id].write_message(message)

    def send_to_all(self, client_ids, message):
        for client_id in client_ids:
            self.send_message(client_id, message)

    pass


class SocketConnection(tornado.websocket.WebSocketHandler):

    __connectionId = 0

    def __init__(self, application, request, **kwargs):
        self.client_id = str(SocketConnection.__connectionId)
        super(SocketConnection, self).__init__(application, request, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        print 'connection opened.'

    def on_message(self, message):

        print 'message received:  {}'.format(message)

    def on_close(self):
        print 'connection closed...'