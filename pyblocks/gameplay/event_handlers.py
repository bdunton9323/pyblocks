from abc import ABC, abstractmethod
from enum import Enum
from screens.disposition_code import MenuAction
from screens.gameover import GameOverScreen
from gameplay.Keys import GameKeys


# Enum specifying what state the game is in
class Mode(Enum):
    MENU = 0
    NEW_GAME = 1
    CONTINUE_GAME = 2
    PAUSE = 3
    QUIT = 4
    GAME_OVER = 5
    HIGH_SCORES = 6
    NAME_ENTRY = 7


class GameEventHandler(ABC):

    @abstractmethod
    def on_key(self, key):
        pass

    @abstractmethod
    def on_tick(self, millis, key):
        pass

    @abstractmethod
    def on_quit(self):
        pass

    @staticmethod
    def on_render(self):
        pass


# Handles key press events that occur while the menu screen is active
class MenuHandler(GameEventHandler):
    DEFAULT_MODE = Mode.MENU

    def __init__(self, menu_screen, game_in_progress):
        self.menu = menu_screen
        self.game_in_progress = game_in_progress

    # Return a tuple: (continue, new_mode)
    # - new_mode: the mode to enter, or None if staying in current mode.
    def on_key(self, key):
        result = self.menu.on_key(key)

        if result == MenuAction.PLAY_GAME:
            if self.game_in_progress:
                return Mode.CONTINUE_GAME
            else:
                return Mode.NEW_GAME

        elif result == MenuAction.SHOW_HIGH_SCORES:
            return Mode.HIGH_SCORES

        elif result == MenuAction.QUIT:
            return Mode.QUIT

        elif result == MenuAction.NEW_GAME:
            return Mode.NEW_GAME

        return None

    # called on every frame of the game while this handler's event loop is running
    # millis - the number of milliseconds since the last frame
    # key - the key that was pressed in this frame
    def on_tick(self, millis, key):
        return None

    # Called upon leaving this event handler's loop (transitioning to a new mode)
    def on_quit(self):
        pass

    def on_render(self):
        self.menu.render()


class GameOverHandler(GameEventHandler):
    DEFAULT_MODE = Mode.GAME_OVER

    # score_keeper - provides the final score
    # score_reader - determines whether the score qualifies for the leader board
    def __init__(self, gameover_screen, score, score_reader):
        self.gameover = gameover_screen
        self.score_reader = score_reader
        self.score = score

    def on_key(self, key):
        result = self.gameover.on_key(key)
        if result == GameOverScreen.DONE:
            if self.score_reader.is_high_score(self.score):
                return Mode.NAME_ENTRY
            else:
                return Mode.HIGH_SCORES
        else:
            return GameOverHandler.DEFAULT_MODE

    def on_tick(self, millis, key):
        return None

    def on_quit(self):
        pass

    def on_render(self):
        self.gameover.render()


class GamePlayHandler(GameEventHandler):
    DEFAULT_MODE = Mode.CONTINUE_GAME

    def __init__(self, game_context, game_keys):
        self.context = game_context
        self.paused = False
        self.game_keys = game_keys

    def on_key(self, key):
        if key == self.game_keys.by_id(GameKeys.P):
            self.paused = not self.paused
            self.context.bg_renderer.set_paused(self.paused)

        elif key == self.game_keys.by_id(GameKeys.ESCAPE):
            return Mode.MENU

        return None

    # millis - the number of milliseconds since the last on_tick call
    # key - the key pressed in this frame
    def on_tick(self, millis, key):
        if not self.paused:
            result = self.context.gameplay.on_tick(millis, key)
            if not result:
                return Mode.GAME_OVER

        return None

    def on_quit(self):
        pass

    def on_render(self):
        # TODO: if this wastes CPU time rendering, I can check if the board is
        # dirty before rendering. Gameplay.on_tick() can return true if dirty.
        self.context.bg_renderer.render_base_layer()
        self.context.board.render(self.context.block_renderer)
        self.context.bg_renderer.render_top_layer()


# Handler for the screen that displays the high scores. This is not for
# entering your initials.
class ScoreBoardHandler(GameEventHandler):
    DEFAULT_MODE = Mode.HIGH_SCORES

    # screen - a LeaderBoardScreen instance
    def __init__(self, screen, game_keys):
        self.screen = screen
        self.screen.refresh_scores()
        self.game_keys = game_keys

    def on_key(self, key):
        if key == self.game_keys.by_id(GameKeys.ESCAPE) or key == self.game_keys.by_id(GameKeys.ENTER):
            return Mode.MENU
        else:
            return None

    def on_tick(self, millis, key):
        return None

    def on_quit(self):
        pass

    def on_render(self):
        self.screen.render()


class NameEntryHandler(GameEventHandler):
    DEFAULT_MODE = Mode.NAME_ENTRY

    def __init__(self, entry_screen, score_keeper, score_writer, game_keys):
        self.score_keeper = score_keeper
        self.writer = score_writer
        self.entry_screen = entry_screen
        self.game_keys = game_keys

    def on_key(self, key):

        if key == self.game_keys.by_id(GameKeys.ESCAPE):
            return Mode.MENU
        else:
            keep_going = self.entry_screen.on_key(key)
            if not keep_going:
                self.writer.write_score(self.entry_screen.get_and_clear_name_entered(),
                                        self.score_keeper.get_score())
                return Mode.MENU

        return None

    def on_tick(self, millis, key):
        return None

    def on_quit(self):
        pass

    def on_render(self):
        self.entry_screen.render()
