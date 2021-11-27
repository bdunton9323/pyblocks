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


# Handles key press events that occur while the menu screen is active
class MenuHandler(object):
    DEFAULT_MODE = Mode.MENU

    def __init__(self, menu_screen, game_in_progress):
        self.menu = menu_screen
        self.game_in_progress = game_in_progress

    # Return a tuple: (continue, new_mode)
    # - continue: indicates whether to continue or abort the event loop for this handler.
    # - new_mode: the mode to enter for the next event loop. Only used if continue=False.
    def on_key(self, key, game_keys):
        mode = MenuHandler.DEFAULT_MODE
        result = self.menu.on_key(key)

        if result == MenuAction.PLAY_GAME:
            if self.game_in_progress:
                mode = Mode.CONTINUE_GAME
            else:
                mode = Mode.NEW_GAME
            return False, mode

        elif result == MenuAction.SHOW_HIGH_SCORES:
            mode = Mode.HIGH_SCORES
            return False, mode

        elif result == MenuAction.QUIT:
            mode = Mode.QUIT
            return False, mode

        elif result == MenuAction.NEW_GAME:
            mode = Mode.NEW_GAME
            return False, mode

        else:
            return (True, mode)

    # called on every frame of the game while this handler's event loop is running
    # millis - the number of milliseconds since the last frame
    # key - the key that was pressed in this frame
    def on_tick(self, millis, key):
        return (True, MenuHandler.DEFAULT_MODE)

    # Called upon leaving this event handler's loop (transitioning to a new mode)
    def on_quit(self):
        pass

    def on_render(self):
        self.menu.render()


class GameOverHandler(object):
    DEFAULT_MODE = Mode.GAME_OVER

    # score_keeper - provides the final score
    # score_reader - determines whether the score qualifies for the leader board
    def __init__(self, gameover_screen, score, score_reader):
        self.gameover = gameover_screen
        self.score_reader = score_reader
        self.score = score

    def on_key(self, key, game_keys):
        result = self.gameover.on_key(key)
        if result == GameOverScreen.DONE:
            if self.score_reader.is_high_score(self.score):
                return (False, Mode.NAME_ENTRY)
            else:
                return (False, Mode.HIGH_SCORES)
        else:
            return (True, GameOverHandler.DEFAULT_MODE)

    def on_tick(self, millis, key):
        return (True, GameOverHandler.DEFAULT_MODE)

    def on_quit(self):
        pass

    def on_render(self):
        self.gameover.render()


class GamePlayHandler(object):
    DEFAULT_MODE = Mode.CONTINUE_GAME

    def __init__(self, game_context):
        self.context = game_context
        self.paused = False

    def on_key(self, key, game_keys):
        keep_going = True
        mode = GamePlayHandler.DEFAULT_MODE

        if key == game_keys.by_id(GameKeys.P):
            self.paused = not self.paused
        elif key == game_keys.by_id(GameKeys.ESCAPE):
            mode = Mode.MENU
            keep_going = False

        self.context.bg_renderer.set_paused(self.paused)
        return (keep_going, mode)

    # millis - the number of milliseconds since the last on_tick call
    # key - the key pressed in this frame
    def on_tick(self, millis, key):
        keep_going = True
        mode = GamePlayHandler.DEFAULT_MODE
        if not self.paused:
            result = self.context.gameplay.on_tick(millis, key)
            if not result:
                mode = Mode.GAME_OVER
                keep_going = False

        return (keep_going, mode)

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
class ScoreBoardHandler(object):
    DEFAULT_MODE = Mode.HIGH_SCORES

    # screen - a LeaderBoardScreen instance
    def __init__(self, screen):
        self.screen = screen
        self.screen.refresh_scores()

    def on_key(self, key, game_keys):
        keep_going = True
        mode = ScoreBoardHandler.DEFAULT_MODE

        if key == game_keys.by_id(GameKeys.ESCAPE) or key == game_keys.by_id(GameKeys.ENTER):
            mode = Mode.MENU
            keep_going = False

        return (keep_going, mode)

    def on_tick(self, millis, key):
        return (True, ScoreBoardHandler.DEFAULT_MODE)

    def on_quit(self):
        pass

    def on_render(self):
        self.screen.render()


class NameEntryHandler(object):
    DEFAULT_MODE = Mode.NAME_ENTRY

    def __init__(self, entry_screen, score_keeper, score_writer):
        self.score_keeper = score_keeper
        self.writer = score_writer
        self.entry_screen = entry_screen

    def on_key(self, key, game_keys):
        keep_going = True
        mode = NameEntryHandler.DEFAULT_MODE

        if key == game_keys.by_id(GameKeys.ESCAPE):
            mode = Mode.MENU
            keep_going = False
        else:
            keep_going = self.entry_screen.on_key(key)
            if not keep_going:
                self.writer.write_score(self.entry_screen.get_and_clear_name_entered(),
                                        self.score_keeper.get_score())
                mode = Mode.MENU

        return (keep_going, mode)

    def on_tick(self, millis, key):
        return (True, NameEntryHandler.DEFAULT_MODE)

    def on_quit(self):
        pass

    def on_render(self):
        self.entry_screen.render()
