

class GameContext(object):
    def __init__(self):
        self.score_keeper = None
        self.block_renderer = None
        self.bg_renderer = None
        self.board = None
        self.gameplay = None
        self.game_in_progress = False

    @property
    def score_keeper(self):
        return self._score_keeper

    @score_keeper.setter
    def score_keeper(self, val):
        self._score_keeper = val

    @property
    def block_renderer(self):
        return self._block_renderer

    @block_renderer.setter
    def block_renderer(self, val):
        self._block_renderer = val

    @property
    def bg_renderer(self):
        return self._bg_renderer

    @bg_renderer.setter
    def bg_renderer(self, val):
        self._bg_renderer = val

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, val):
        self._board = val

    @property
    def gameplay(self):
        return self._gameplay

    @gameplay.setter
    def gameplay(self, val):
        self._gameplay = val

    @property
    def game_in_progress(self):
        return self._game_in_progress

    @game_in_progress.setter
    def game_in_progress(self, val):
        self._game_in_progress = val
