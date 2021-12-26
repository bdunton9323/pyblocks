

class GameContext(object):
    def __init__(self):
        self.score_keeper = None
        self.block_renderer = None
        self.bg_renderer = None
        self.board = None
        self.gameplay = None
        self.game_in_progress = False
        self.event_handler = None

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

    @property
    def event_handler(self):
        return self._event_handler

    @event_handler.setter
    def event_handler(self, val):
        self._event_handler = val


class GameStates(object):
    def __init__(self):
        self.menu_state = None
        self.game_over_state = None
        self.high_scores_state = None
        self.name_entry_state = None

    @property
    def menu_state(self):
        return self._menu_state

    @menu_state.setter
    def menu_state(self, val):
        self._menu_state = val

    @property
    def game_over_state(self):
        return self._game_over_state

    @game_over_state.setter
    def game_over_state(self, val):
        self._game_over_state = val

    @property
    def high_scores_state(self):
        return self._high_scores_state

    @high_scores_state.setter
    def high_scores_state(self, val):
        self._high_scores_state = val

    @property
    def name_entry_state(self):
        return self._name_entry_state

    @name_entry_state.setter
    def name_entry_state(self, val):
        self._name_entry_state = val
