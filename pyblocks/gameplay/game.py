from gameboard.BlockRenderer import BlockRenderer
from gameboard.BgRenderer import BgRenderer
from gameboard.Board import Board
from gameplay.game_context import GameContext
from gameplay.game_context import GameStates
from gameplay.Gameplay import Gameplay
from gameplay.Keys import *
from gameplay.GameParams import GameParams
from gameplay.game_state_builders import MenuStateBuilder
from geometry.Geometry import Geometry
from scoreboard.highscorepersistence import *
from scoreboard.LeaderBoardScreen import LeaderBoardScreen
from gameplay.ScoreKeeper import ScoreKeeper
from screens.NameEntryScreen import NameEntryScreen
from gameplay.eventhandlers import *
from sound.audio import *


class Constants:
    FRAME_RATE = 60
    MILLISECONDS = 1000

    BLOCK_WIDTH = 25
    BLOCK_HEIGHT = 25

    SCREEN_SIZE = (800, 600)

    FIELD_WIDTH = 14
    FIELD_HEIGHT = 17
    x1 = BLOCK_WIDTH * 5
    y1 = BLOCK_HEIGHT * 3
    # (x1,y1,x2,y2) of the playable area (where the pieces can move)
    PLAY_AREA_COORDS_PX = (
        x1,
        y1,
        BLOCK_WIDTH * FIELD_WIDTH + x1,
        BLOCK_HEIGHT * FIELD_HEIGHT + y1)
    del x1
    del y1

    # This is relative to the absolute grid (as opposed to the playing field grid)
    PIECE_DROP_POS = (12, 3)

    HIGH_SCORE_FILE = "../highscores.dat"
    NUM_HIGH_SCORES = 10

    MENU_FONT_FILE = "gfx/font/Laundromatic/SFLaundromaticExtended.ttf"
    SCORE_FONT_FILE = "gfx/font/Laundromatic/SFLaundromaticExtended.ttf"
    TITLE_FONT_FILE = "gfx/font/crackman/crackman.ttf"
    SCORE_BANNER_FONT_FILE = "gfx/font/crackman/crackman.ttf"
    GAME_OVER_FONT_FILE = "gfx/font/crackman/crackman.ttf"
    NAME_ENTRY_FONT_FILE = "gfx/font/crackman/crackman.ttf"
    # Use a monospace font here because there is a character limit for the name
    # entry, which needs to fit exactly within the text box.
    NAME_ENTRY_TEXT_FONT_FILE = "gfx/font/bpmono/BPmono.ttf"

    KEYS = GameKeys()


class PygameContext(object):
    def __init__(self):
        self.display = None

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, val):
        self._display = val


class Game(object):

    def __init__(self):
        self.game_context = None
        self.game_states = None
        self.game_params = None

    @staticmethod
    def init_pygame():
        # Mixer has to be initialized before pygame.
        # http://stackoverflow.com/questions/18273722/pygame-sound-delay
        # http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.pre_init
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        pygame.init()
        screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBlocks")

        # set the key delay for holding down buttons
        pygame.key.set_repeat(250, 75)

        pygame_context = PygameContext()
        pygame_context.display = screen
        return pygame_context

    def init_game_params(self, pygame_context):
        params = GameParams()
        params.set_screen(pygame_context.display)
        params.set_geometry(
            Geometry(Constants.BLOCK_WIDTH,
                     Constants.BLOCK_HEIGHT,
                     Constants.PLAY_AREA_COORDS_PX))
        params.set_jukebox(Jukebox(pygame.mixer))

        # stuff for controlling what the keys are
        key_mapper = KeyMapper(Constants.KEYS)
        key_change_publisher = KeyChangePublisher()
        key_change_publisher.subscribe(key_mapper.on_key_change)
        params.set_key_change_publisher(key_change_publisher)
        params.set_key_mapper(key_mapper)

        self.game_params = params

    def new_game(self):

        game_context = GameContext()
        game_context.game_in_progress = True
        game_context.score_keeper = ScoreKeeper()

        game_context.block_renderer = BlockRenderer(
            self.game_params.get_screen(),
            self.game_params.get_geometry())

        game_context.bg_renderer = BgRenderer(
            self.game_params.get_screen(),
            Constants.PLAY_AREA_COORDS_PX,
            Constants.BLOCK_HEIGHT,
            Constants.BLOCK_HEIGHT,
            game_context.score_keeper,
            Constants.SCORE_FONT_FILE)

        game_context.board = Board(self.game_params.get_geometry(), Constants.PIECE_DROP_POS)

        game_context.gameplay = Gameplay(
            game_context.board,
            self.game_params.get_geometry(),
            game_context.score_keeper,
            self.game_params.get_jukebox(),
            self.game_params.get_key_mapper())

        self.game_context = game_context

    def init_game_states(self):
        params = self.game_params

        states = GameStates()

        menu_state_builder = MenuStateBuilder(
            params.get_screen(),
            Constants.MENU_FONT_FILE,
            Constants.TITLE_FONT_FILE,
            params.get_jukebox(),
            params.get_key_change_publisher(),
            Constants.KEYS,
            params.get_key_mapper())
        states.menu_state = menu_state_builder.build()

        states.game_over_state = GameOverScreen(params.get_screen(), Constants.GAME_OVER_FONT_FILE, Constants.KEYS)

        states.high_scores_state = LeaderBoardScreen(
            params.get_screen(), HighScoreReader(
                Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES), Constants.SCORE_FONT_FILE,
            Constants.SCORE_BANNER_FONT_FILE)

        states.name_entry_state = NameEntryScreen(
            params.get_screen(), Constants.NAME_ENTRY_FONT_FILE,
            Constants.NAME_ENTRY_TEXT_FONT_FILE, params.get_jukebox(), Constants.KEYS)

        self.game_states = states

    def run_game(self):
        pygame_context = self.init_pygame()
        self.init_game_params(pygame_context)
        self.game_params.get_jukebox().start_game_music()
        self.init_game_states()

        mode = Mode.MENU
        while mode != Mode.QUIT:
            event_handler = self.enter_mode(mode)
            mode = GameLoop(event_handler).run_event_loop()

    def enter_mode(self, mode):

        if mode == Mode.MENU:
            game_in_progress = self.game_context is not None and self.game_context.game_in_progress is True
            self.game_states.menu_state.set_paused(game_in_progress)
            return MenuHandler(self.game_states.menu_state, game_in_progress)

        elif mode == Mode.NEW_GAME:
            self.new_game()
            self.game_context.event_handler = GamePlayHandler(self.game_context, Constants.KEYS)
            return self.game_context.event_handler

        elif mode == Mode.CONTINUE_GAME:
            # TODO: does it even matter if we construct a new one or not? Does it just save on one cheap object?
            # return the existing handler that is already in progress
            return self.game_context.event_handler

        elif mode == Mode.GAME_OVER:
            self.game_context.game_in_progress = False
            score = self.game_context.score_keeper.get_score()
            self.game_states.game_over_state.set_score(score)

            return GameOverHandler(
                self.game_states.game_over_state, score,
                HighScoreReader(Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES))

        elif mode == Mode.HIGH_SCORES:
            return ScoreBoardHandler(self.game_states.high_scores_state, Constants.KEYS)

        elif mode == Mode.NAME_ENTRY:
            return NameEntryHandler(
                self.game_states.name_entry_state,
                self.game_context.score_keeper,
                HighScoreWriter(Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES),
                Constants.KEYS)

        pygame.quit()

    @staticmethod
    def get_or_default(cache, key, default):
        if key in cache:
            return cache.get(key)
        cache[key] = default
        return default


class GameLoop(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.clock = pygame.time.Clock()

    def run_event_loop(self):
        next_mode = None

        while next_mode is None:
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_mode = Mode.QUIT
                    self.event_handler.on_quit()

                elif event.type == pygame.KEYDOWN:
                    key = Constants.KEYS.from_pygame(event.key)
                    if key:
                        next_mode = self.event_handler.on_key(key)

            if next_mode is None:
                millis = int(1 / float(Constants.FRAME_RATE) * Constants.MILLISECONDS)
                next_mode = self.event_handler.on_tick(millis, key)
                self.event_handler.on_render()
                pygame.display.flip()
                self.clock.tick(Constants.FRAME_RATE)
        return next_mode
