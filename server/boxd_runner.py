import game.game as game


class GameRunner(object):

    __instance = None

    class __GameRunner(object):

        def __init__(self):
            self.player_game_map = {}
            self.running_games = []
            self.players = {}

        def assign_player(self, player_id):

            # todo:  grow number of running games and actually pick the best game to assign
            if not self.running_games:
                self.running_games.append(game.BoxdGame())

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

            # if game is empty, shut it down.
            if not game.get_players():
                self.running_games.remove(game)



    @staticmethod
    def claim_line(player_id, p1_r, p1_c, p2_r, p2_c):
        return GameRunner.__instance.player_game_map[player_id].claim_line((p1_r, p1_c), (p2_r, p2_c), player_id)

    @staticmethod
    def assign_player(player_id):
        # TODO:  Error checking
        return GameRunner.__instance.assign_player(player_id)

    @staticmethod
    def remove_player(player_id):
        GameRunner.__instance.remove_player(player_id)

    @staticmethod
    def update_player_name(player_id, name):
        # TODO:  Error checking
        GameRunner.__instance.player_game_map[player_id].change_player_nickname(player_id, name)

    @staticmethod
    def get_other_players(player_id):
        return GameRunner.__instance.player_game_map[player_id].get_players()

    @staticmethod
    def running_games():
        return len(GameRunner.__instance.running_games)

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