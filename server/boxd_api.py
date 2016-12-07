import tornado.websocket
import json
import time
from threading import Thread
from boxd_runner import GameRunner, CooldownError
from models import message as messages


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
            t = Thread(target=self.poke_all_connections)
            t.start()

        def poke_all_connections(self):
            while True:
                time.sleep(45)
                self.send_to_all(self.connections.keys(), json.dumps({"stay_with_me": True}))

        def connected_clients(self):
            return len(self.connections)

        def get_connected_clients(self):
            clients = list(self.connections.keys())
            clients.sort()
            return clients

        def send_message(self, client_id, message):

            if client_id not in self.connections:
                raise ValueError("Client id not found in connections!  ({})".format(client_id))

            if not isinstance(self.connections[client_id], SocketConnection):
                raise ValueError("Not sure how this happened.")

            self.connections[client_id].write_message(message)

        def send_to_all(self, client_ids, message):
            print "Sending to all:  {}".format(message)
            for client_id in client_ids:
                self.send_message(client_id, message)

        def register_connection(self, client_id, connection):

            if not isinstance(connection, SocketConnection):
                raise ValueError("connection was not of type SocketConnection.  Got type {}".format(type(connection)))

            if client_id in self.connections:
                raise ValueError("Client id was already registered:  {}".format(client_id))

            self.connections[client_id] = connection

        def remove_connection(self, client_id):

            if client_id not in self.connections:
                raise ValueError("Client id was not registered:  {}".format(client_id))

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
        print 'connection opened:  {}'.format(str(self.client_id))
        self.write_message("Your client_id is {}".format(self.client_id))

    def on_message(self, message_json):
            print 'message received:  {}'.format(message_json)
            # todo:  parse and act

            message = json.loads(message_json)
            if 'type' not in message or not 'data' in message:
                # Todo:  come up with some error
                return

            if message['type'] == 'JOIN_GAME':

                #  TODO:  Send full board data as response

                name = message['data']['name'] or 'Unnamed Player'

                assigned_game = GameRunner.assign_player(self.client_id, name)
                client_color = GameRunner.get_player_color(self.client_id)
                board_edges, board_boxes = GameRunner.get_board_info(self.client_id)

                ConnectionManager.send_message(self.client_id, "You joined game {} as {}".format(assigned_game, name))
                ConnectionManager.send_message(self.client_id, "The game has the following players:  {}"
                                               .format(GameRunner().get_other_player_ids(self.client_id)))
                ConnectionManager.send_to_all(GameRunner.get_other_player_ids(self.client_id),
                                              "{} (client {}) joined the game".format(name, self.client_id))

                # generate and send message about the board state # TODO:  Send player scores
                ConnectionManager.send_message(self.client_id, json.dumps(messages.BoardStateMessage(board_edges, board_boxes, client_color).get_message()))

            elif message['type'] == 'LEAVE_GAME':
                other_players = GameRunner.get_other_player_ids(self.client_id)
                ConnectionManager.send_to_all(other_players, "{} (Client {}) left".format(
                GameRunner.get_player_name(self.client_id), self.client_id))
                GameRunner.remove_player(self.client_id)

            elif message['type'] == "CLAIM_LINE":
                p1r = message['data']['pt1_r']
                p1c = message['data']['pt1_c']
                p2r = message['data']['pt2_r']
                p2c = message['data']['pt2_c']

                pt1 = (p1r, p1c)
                pt2 = (p2r, p2c)

                responses = []
                new_boxes = None
                player_color = GameRunner.get_player_color(self.client_id)

                try:
                    new_boxes = GameRunner.claim_line(self.client_id, pt1, pt2)
                except CooldownError:
                    responses.append(messages.Message({"You're still cooling off...": True}))

                # TODO:  Have errors propagate to this method instead of returning None
                # None means an Race Condition Error occurred. [] means there are no new boxes
                if new_boxes is not None:

                    responses.append(messages.LineClaimedMessage((p1r, p1c), (p2r, p2c), player_color))

                    for new_box in new_boxes:
                        responses.append(messages.BoxCreatedMessage(new_box, player_color))

                for response in responses:
                    ConnectionManager.send_to_all(GameRunner.get_players_from_game(self.client_id), json.dumps(response.get_message()))

    def on_close(self):
        print 'connection closed due to:  {}'.format(self.close_reason)

        try:
            other_players = GameRunner.get_other_player_ids(self.client_id)
            ConnectionManager.send_to_all(other_players, "{} (Client {}) left".format(
                GameRunner.get_player_name(self.client_id), self.client_id))
            GameRunner.remove_player(self.client_id)

        except ValueError:  # should only happen if the player is not in a game
            pass

        ConnectionManager.remove_connection(self.client_id)
