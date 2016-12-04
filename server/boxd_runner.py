import game.boxd_game
import traceback
import sys
from datetime import datetime, timedelta


COOLDOWN_SECONDS = 0


class GameRunner(object):

    __instance = None

    class __GameRunner(object):

        def __init__(self):
            self.player_game_map = {}
            self.running_games = []
            self.players = {}

        '''
        ' Returns the list of every player_ids (for every player)
        '''
        def get_player_ids(self):
            return self.players.keys()

        '''
        ' Puts the player in an open game.  If no games are open, creates a new game and assigns the player to it
        '
        ' player_id:  The id of the player being added
        ' nickname:   What to call the player
        '
        ' Raises ValueError if player is already in a game
        '
        ' Returns the game_id of the game the player was assigned to
        '''
        def assign_player(self, player_id, nickname=None):

            if player_id in self.players or player_id in self.player_game_map:
                raise ValueError("Player already assigned:  {}".format(player_id))

            # todo:  grow number of running games and actually pick the best game to assign
            if not self.running_games:
                self.running_games.append(game.boxd_game.BoxdGame())

            best_game = self.running_games[0]

            best_game.add_player(player_id)

            self.players[player_id] = Player(player_id, nickname)
            self.player_game_map[player_id] = self.running_games[0]
            self.change_player_nickname(player_id, nickname)

            return 0  # todo:  returned id of room the user was assigned to

        '''
        ' Removes the player with the specified id from the game they are in.  If the game they left is now empty,
        ' The Game is destroyed
        '
        ' player_id:  The id of the player being removed
        '
        ' Raises ValueError if the player_id is not associated with a running game
        '''
        def remove_player(self, player_id):

            # remove player from the actual boxd game
            self.player_game_map[player_id].remove_player(player_id)

            # remove player from the player_game map
            game = self.player_game_map[player_id]
            self.player_game_map.pop(player_id)

            self.players.pop(player_id)

            # if game is empty, shut it down.
            if not game.get_players():
                self.running_games.remove(game)

        '''
        ' Changes the specified player's nickname.
        '
        ' player_id:  The id of the player whose name is being changed
        ' nickname:   The new name for the player
        '
        ' Raises ValueError if the player_id is not registered
        '''
        def change_player_nickname(self, player_id, nickname):

            if player_id not in self.players:
                raise ValueError("Player wasn't found: {}".format(player_id))

            if not nickname:
                nickname = "Muhammad Ali{}".format(player_id)

            self.players[player_id].name = nickname

        '''
        ' Claims the line specified by (p1_r, p1_c), (p2_r, p2_c) for the player specified by player_id
        '
        ' player_id:  the id of the player claiming the line
        ' p1_r:       point1's row index
        ' p1_c:       point1's column index
        ' p2_r:       point2's row index
        ' p2_c:       point2's column index
        '
        ' Raises a ValueError if the player is not assigned or could not be found
        ' Raises a CooldownError if the player isn't allowed to move quite yet, but the frontend sent a move anyway
        '
        ' Returns the list of boxes created by claiming an edge
        '''
        def claim_line(self, player_id, p1_r, p1_c, p2_r, p2_c):

            if player_id not in self.players:
                raise ValueError("Player wasn't found: {}".format(player_id))

            if player_id not in self.player_game_map:
                raise ValueError("Player wasn't in a game:  {}".format(player_id))

            # check if the player is past their cool down time
            if datetime.now() < self.players[player_id].next_move:
                raise CooldownError()

            # get the player's game
            players_game = self.player_game_map[player_id]
            # create points from message data
            pt1 = (p1_r, p1_c)
            pt2 = (p2_r, p2_c)

            try:
                # attempt to claim the line
                new_boxes = players_game.claim_line(pt1, pt2, player_id)  # see boxd_game.BoxdGame.claim_line
                # set players next possible move time to current time + cooldown seconds
                self.players[player_id].next_move = datetime.now() + timedelta(seconds=COOLDOWN_SECONDS)

            except game.boxd_game.EdgeOwnedError:
                print "Edge already claimed!  {}, {}".format(pt1, pt2)
                return None

            except ValueError:
                traceback.print_exc(file=sys.stdout)
                return None

            return new_boxes

        '''
        ' Finds the game the player specified by player_id is in and returns the list of all players in that game
        '
        ' player_id:  The player whose game we're trying to find
        '
        ' Raises ValueError if the player is not assigned to a game
        '
        ' Returns a list of player_ids representing every player in "player_id"'s game
        '''
        def get_players(self, player_id):
            if player_id not in self.players:
                raise ValueError("Player wasn't found: {}".format(player_id))

            if player_id not in self.player_game_map:
                raise ValueError("Player wasn't in a game:  {}".format(player_id))

            players_game = self.player_game_map[player_id]
            return players_game.get_players()

        '''
        ' Returns the nickname of the player specified by player_id
        '
        ' player_id:  The player whose name we're tyring to find
        '
        ' Raises ValueError if the player cannot be found
        '
        ' Returns the player's name
        '''
        def get_player_name(self, player_id):

            if player_id not in self.players:
                raise ValueError("Player wasn't found: {}".format(player_id))

            player = self.players[player_id]
            return player.name

    @staticmethod
    def claim_line(player_id, p1_r, p1_c, p2_r, p2_c):
        new_boxes = GameRunner.__instance.claim_line(player_id, p1_r, p1_c, p2_r, p2_c)
        if new_boxes is None:
            return None
        return list(new_boxes)

    @staticmethod
    def assign_player(player_id):
        return GameRunner.__instance.assign_player(player_id)

    @staticmethod
    def remove_player(player_id):
        GameRunner.__instance.remove_player(player_id)

    @staticmethod
    def update_player_name(player_id, name):
        # TODO:  Error checking
        GameRunner.__instance.change_player_nickname(player_id, name)

    @staticmethod
    def get_players_from_game(player_id):
        return list(GameRunner.__instance.get_players(player_id))

    @staticmethod
    def running_games():
        return len(GameRunner.__instance.running_games)

    @staticmethod
    def get_player_ids():
        return list(GameRunner.__instance.get_player_ids())

    @staticmethod
    def get_other_player_ids(player_id):
        players = list(GameRunner.get_players_from_game(player_id))
        players.remove(player_id)
        return players

    @staticmethod
    def get_player_name(player_id):
        return GameRunner.__instance.get_player_name(player_id)

    @staticmethod
    def create():
        if not GameRunner.__instance:
            GameRunner.__instance = GameRunner.__GameRunner()

    @staticmethod
    def reset():
        GameRunner.__instance = GameRunner.__GameRunner()


class Player(object):

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name or "Muhammad Ali{}".format(player_id)
        self.next_move = datetime.now()


class CooldownError(Exception):

    def __init__(self):
        pass