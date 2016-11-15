import game.boxd_game

class GameRunner(object):

    __instance = None

    class __GameRunner(object):

        def __init__(self):
            self.player_game_map = {}
            self.running_games = []
            self.players = {}

        def get_player_ids(self):
            return self.players.keys()

        def assign_player(self, player_id):

            # todo:  grow number of running games and actually pick the best game to assign
            if not self.running_games:
                self.running_games.append(game.boxd_game.BoxdGame())

            best_game = self.running_games[0]

            best_game.add_player(player_id)

            self.players[player_id] = Player(player_id)
            self.player_game_map[player_id] = self.running_games[0]

            return 0  # todo:  returned id of room the user was assigned to

        def remove_player(self, client_id):

            # remove player from the actual boxd game
            self.player_game_map[client_id].remove_player(client_id)

            # remove player from the player_game map
            game = self.player_game_map[client_id]
            self.player_game_map.pop(client_id)

            self.players.pop(client_id)

            # if game is empty, shut it down.
            if not game.get_players():
                self.running_games.remove(game)

        def change_player_nickname(self, player_id, nickname):
            self.players[player_id].name = nickname

        def claim_line(self, player_id, p1_r, p1_c, p2_r, p2_c):
            # TODO:  Error checking
            players_game = self.player_game_map[player_id]
            pt1 = (p1_r, p1_c)
            pt2 = (p2_r, p2_c)
            return players_game.claim_line(pt1, pt2, player_id)

        def get_players(self, player_id):

            players_game = self.player_game_map[player_id]
            return players_game.get_players()


    @staticmethod
    def claim_line(player_id, p1_r, p1_c, p2_r, p2_c):
        return GameRunner.__instance.claim_line(player_id, p1_r, p1_c, p2_r, p2_c)

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
        return GameRunner.__instance.get_players(player_id)

    @staticmethod
    def running_games():
        return len(GameRunner.__instance.running_games)

    @staticmethod
    def get_player_ids():
        return GameRunner.__instance.get_player_ids()

    @staticmethod
    def create():
        if not GameRunner.__instance:
            GameRunner.__instance = GameRunner.__GameRunner()

    @staticmethod
    def reset():
        GameRunner.__instance = GameRunner.__GameRunner()


class Player(object):

    def __init__(self, player_id):
        self.player_id = player_id
        self.name = "Unnamed Player"