import unittest
import tictactoe

X = "X"
O = "O"
EMPTY = None

draw = [[X, O, X],
        [X, O, O],
        [O, X, X]]

test = [[X, EMPTY, X],
        [EMPTY, O, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

test_2 = [[X, O, X],
         [O, X, EMPTY],
         [EMPTY, X, O]]

test_3 = [[X, O, X],
         [O, EMPTY, O],
         [EMPTY, X, EMPTY]]

class TestTicTacToe(unittest.TestCase):
    def test_utility(self):
        result = tictactoe.utility(draw)
        self.assertEqual(0, result)
    
    def test_winner(self):
        result = tictactoe.winner(draw)
        self.assertEqual(None, result)

    def test_player(self):
        result = tictactoe.player(test)
        self.assertEqual(O, result)

    def test_min_max(self):
        action_to_take = tictactoe.minimax(test)
        result = tictactoe.result(test, action_to_take)
        desired_test = [[X, O, X],
                        [EMPTY, O, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(desired_test, result)

    def test_min_max_2(self):
        action_to_take = tictactoe.minimax(test_2)
        result = tictactoe.result(test_2, action_to_take)
        desired_test = [[X, O, X],
                        [O, X, EMPTY],
                        [O, X, O]]
        self.assertEqual(desired_test, result)

    def test_min_max_3(self):
        action_to_take = tictactoe.minimax(test_3)
        result = tictactoe.result(test_3, action_to_take)
        desired_test = [[X, O, X],
                        [O, X, O],
                        [EMPTY, X, EMPTY]]
        self.assertEqual(desired_test, result)


if __name__ == "__main__":
    unittest.main(verbosity=3)