import unittest
from .. ScoreKeeper import ScoreKeeper

class TestScoreKeeper(unittest.TestCase):

    def setUp(self):
        self.score_keeper = ScoreKeeper()

    def test_landed_piece_clears_zero_rows(self):
        difficulty = self.score_keeper.on_move_complete(0, 15)
        self.assertEqual(1, difficulty)
        self.assert_score(1)
        self.assertEqual(0, self.score_keeper.get_rows())

    def test_piece_lands_near_top(self):
        difficulty = self.score_keeper.on_move_complete(0, 4)
        self.assertEqual(1, difficulty)
        # 1 point for landing, bonus point for being near top
        self.assert_score(2)

    def test_piece_lands_exactly_on_top(self):
        difficulty = self.score_keeper.on_move_complete(0, 0)
        self.assertEqual(1, difficulty)
        # 1 point for landing, 5 bonus point for being near top
        self.assert_score(6)

    def test_landed_piece_clears_one_row(self):
        difficulty = self.score_keeper.on_move_complete(1, 15)
        self.assertEqual(1, difficulty)
        self.assert_score(10)

    def test_landed_piece_clears_multiple_rows(self):
        difficulty = self.score_keeper.on_move_complete(2, 15)
        self.assertEqual(1, difficulty)
        self.assert_score(40)

    def test_piece_dropped_from_low(self):
        self.score_keeper.on_drop(15)
        # score is 0 here because on_move_complete will still be called and award the default points
        self.assert_score(0)

    def test_piece_dropped_from_highest_point(self):
        self.score_keeper.on_drop(0)
        self.assert_score(7)

    def test_piece_dropped_from_almost_high_enough_for_bonus(self):
        self.score_keeper.on_drop(7)
        self.assert_score(0)

    def test_piece_dropped_from_bonus_cutoff_point(self):
        self.score_keeper.on_drop(6)
        self.assert_score(1)

    def test_landed_piece_bumps_difficulty(self):
        difficulty = self.score_keeper.on_move_complete(5, 15)
        self.assertEqual(1, difficulty)
        # this is the 7th row completed, so difficulty should be bumped
        difficulty = self.score_keeper.on_move_complete(2, 15)
        self.assertEqual(2, difficulty)
        self.assertEqual(7, self.score_keeper.get_rows())

    def test_difficulty_affects_score_when_no_rows_cleared(self):
        difficulty = self.score_keeper.on_move_complete(7, 15)
        # assert the precondition for the test
        self.assertEqual(2, difficulty)

        base_score = self.score_keeper.get_score()
        self.score_keeper.on_move_complete(0, 15)
        # Don't care what happened to the score while setting up the test, only how much extra we got.
        self.assertEqual(base_score + 2, self.score_keeper.get_score())

    def test_difficulty_affects_score_when_one_row_cleared(self):
        difficulty = self.score_keeper.on_move_complete(7, 15)
        # assert the precondition for the test
        self.assertEqual(2, difficulty)

        base_score = self.score_keeper.get_score()
        self.score_keeper.on_move_complete(1, 15)
        # Don't care what happened to the score while setting up the test, only how much extra we got.
        self.assertEqual(base_score + 20, self.score_keeper.get_score())

    def test_difficulty_affects_score_when_two_rows_cleared(self):
        difficulty = self.score_keeper.on_move_complete(7, 15)
        # assert the precondition for the test
        self.assertEqual(2, difficulty)

        base_score = self.score_keeper.get_score()
        self.score_keeper.on_move_complete(2, 15)
        # Don't care what happened to the score while setting up the test, only how much extra we got.
        self.assertEqual(base_score + 80, self.score_keeper.get_score())

    def assert_score(self, expected_score):
        self.assertEqual(expected_score, self.score_keeper.get_score(), "Score was not as expected")
