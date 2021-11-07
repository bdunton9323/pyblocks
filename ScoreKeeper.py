import pygame


# Houses the algorithm for keeping score and determining
# which difficulty level the player is on.
class ScoreKeeper(object):
    # How many rows to complete before increasing difficulty
    ROWS_PER_LEVEL = 7

    def __init__(self):
        self.score = 0
        self.rows = 0
        self.difficulty = 1

    # num_rows - the number of rows cleared in this move (if any)
    # num_clicks - the distance the piece has fallen. Score is skewed such that more points
    #   are awarded as the pieces land higher up (takes more skill to land pieces at the top).
    # return the new difficulty level (may or may not have changed)
    def on_move_complete(self, num_rows, num_clicks):
        self.rows += num_rows
        self.difficulty = ScoreKeeper.calculate_difficulty(self.rows)

        if num_rows > 0:
            increment = num_rows * 10 * num_rows * self.difficulty
        else:
            increment = self.difficulty

        # calculate bonus points for landing a piece near the top where it's more difficult
        bonus = 0
        if num_clicks < 5:
            bonus = 5 - num_clicks

        self.score += increment
        self.score += bonus

        # reevaluate difficulty because this move may have pushed it up
        self.difficulty = ScoreKeeper.calculate_difficulty(self.rows)
        return self.difficulty

    # Maybe award bonus points for dropping the piece (player is rewarded for playing quickly)
    # num_clicks - the distance the piece has fallen. Score is skewed such
    #   that the higher the piece is dropped from, the more points.
    def on_drop(self, num_clicks):
        extra = 0
        if num_clicks <= 7:
            extra = 7 - num_clicks
        self.score += extra

    def get_score(self):
        return self.score
    
    # The difficulty level is based on 
    def get_difficulty(self):
        return self.difficulty

    def get_rows(self):
        return self.rows

    # TODO: this doesn't seem like it should be the job of the score keeper.
    @staticmethod
    def calculate_difficulty(rows):
        return rows // ScoreKeeper.ROWS_PER_LEVEL + 1
