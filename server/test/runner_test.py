import unittest

from server.boxd_runner import GameRunner


class TestBoxdRunner(unittest.TestCase):

    def setUp(self):
        GameRunner.reset()

    def test_get_remove_player(self):
        GameRunner.assign_player("0")
        GameRunner.assign_player("1")
        GameRunner.assign_player("2")

        players = GameRunner.get_players_from_game("0")

        self.assertItemsEqual(players, ["0", "1", "2"])

        GameRunner.remove_player("1")

        players = GameRunner.get_players_from_game("0")

        self.assertItemsEqual(players, ["0", "2"])

        GameRunner.remove_player("0")

        players = GameRunner.get_players_from_game("2")

        self.assertEqual(players, ["2"])

    def test_creates_and_destroys_games(self):

        self.assertEqual(GameRunner.running_games(), 0)

        for i in range(0, 33):
            GameRunner.assign_player(str(i))

        expected_players = [str(x) for x in range(0, 33)]

        # TODO:  Change the range from 0-33 to 0-32 when we want to support multiple rooms
        # self.assertItemsEqual([str(x) for x in range(0, 32)], GameRunner.get_other_players("0"))
        self.assertItemsEqual(expected_players, GameRunner.get_players_from_game("0"))

        # TODO:  Chnange the range from 0-33 to [32] when we wanto to support multiple rooms
        # self.assertItemsEqual(["32"], GameRunner.get_other_players("32"))
        self.assertItemsEqual(expected_players, GameRunner.get_players_from_game("32"))

        # TODO:  Expect 2 running games when we want to support multiple rooms
        # self.assertEqual(GameRunner.running_games(), 2)
        self.assertEqual(GameRunner.running_games(), 1)

        GameRunner.remove_player("5")
        expected_players.remove("5")
        self.assertEqual(GameRunner.running_games(), 1)  # change to 2 when supporting multiple rooms
        self.assertItemsEqual(expected_players, GameRunner.get_players_from_game("0"))

        GameRunner.remove_player("32")
        expected_players.remove("32")
        self.assertEqual(GameRunner.running_games(), 1)
        self.assertItemsEqual(expected_players, GameRunner.get_players_from_game("0"))

        players = GameRunner.get_player_ids()

        for player_id in players:
            GameRunner.remove_player(player_id)

        self.assertEqual(GameRunner.get_player_ids(), [])
        self.assertEqual(GameRunner.running_games(), 0)

    def test_updating_player_name(self):

        client_id = "0"
        GameRunner.assign_player(client_id)
        self.assertEqual(GameRunner.get_player_name(client_id), "Unnamed Player")

        GameRunner.update_player_name(client_id, "Bernie Sanders")
        self.assertEqual(GameRunner.get_player_name(client_id), "Bernie Sanders")


if __name__ == '__main__':
    unittest.main()
