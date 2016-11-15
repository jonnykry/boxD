import tornado.websocket
import copy
from boxd_runner import GameRunner


class ConnectionManager(object):

    __instance = None

    @staticmethod
    def create():
        if not ConnectionManager.__instance:
            ConnectionManager.reset()

    @staticmethod
    def reset():
        ConnectionManager.__instance = ConnectionManager.__ConnectionManager()

    class __ConnectionManager(object):

        def __init__(self):
            self.connections = {}

        def connected_clients(self):
            return len(self.connections)

        def get_connected_clients(self):
            clients = list(self.connections.keys())
            clients.sort()
            return clients

        def send_message(self, client_id, message):

            if client_id not in self.connections:
                raise ValueError("Client id not found in connections!  ({})".format(str(client_id)))

            if not isinstance(self.connections[client_id], SocketConnection):
                raise ValueError("Not sure how this happened.")

            self.connections[client_id].write_message(message)

        def send_to_all(self, client_ids, message):
            for client_id in client_ids:
                self.send_message(client_id, message)

        def register_connection(self, client_id, connection):

            if not isinstance(connection, SocketConnection):
                raise ValueError("connection was not of type SocketConnection.  Got type {}".format(type(connection)))

            if client_id in self.connections:
                raise ValueError("Client id was already registered:  {}".format(client_id))

            self.connections[client_id] = connection

        def remove_connection(self, client_id):

            self.connections.pop(client_id)


    @staticmethod
    def connected_clients():
        return ConnectionManager.__instance.connected_clients()

    @staticmethod
    def get_connected_clients():
        return ConnectionManager.__instance.get_connected_clients()

    @staticmethod
    def send_message(client_id, message):
        return ConnectionManager.__instance.send_message(client_id, message)

    @staticmethod
    def register_connection(client_id, connection):
        ConnectionManager.__instance.register_connection(client_id, connection)

    @staticmethod
    def remove_connection(client_id):
        ConnectionManager.__instance.remove_connection(client_id)

    @staticmethod
    def send_to_all(client_ids, message):
        return ConnectionManager.__instance.send_to_all(client_ids, message)


class SocketConnection(tornado.websocket.WebSocketHandler):

    __connectionId = 0

    def __init__(self, application, request, **kwargs):
        self.client_id = str(SocketConnection.__connectionId)
        SocketConnection.__connectionId += 1
        super(SocketConnection, self).__init__(application, request, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):

        # register connection
        ConnectionManager.register_connection(self.client_id, self)

        # assign client to a game
        assigned_game = GameRunner.assign_player(self.client_id)
        print 'connection opened:  {}'.format(str(self.client_id))

        self.write_message("you are in game number {}.  Your client_id is {}".format(assigned_game, self.client_id))
        self.write_message("your fellow clients are {}".format(ConnectionManager.get_connected_clients()))

    def on_message(self, message):
            print 'message received:  {}'.format(message)
            # todo:  parse and act

    def on_close(self):

        # TODO:  message everyone who was in the same game as the client.  tell them the client left.

        ConnectionManager.remove_connection(self.client_id)
        GameRunner.remove_player(self.client_id)

        print 'connection closed...'

