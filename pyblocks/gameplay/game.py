from gameboard.BlockRenderer import BlockRenderer
from gameboard.BgRenderer import BgRenderer
from gameboard.Board import Board
from gameplay.game_context import GameContext
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

    @staticmethod
    def init_game_params(pygame_context):
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

        return params

    def new_game(self, game_params):
        game_context = GameContext()
        game_context.game_in_progress = True
        game_context.score_keeper = ScoreKeeper()

        game_context.block_renderer = BlockRenderer(
            game_params.get_screen(),
            game_params.get_geometry())

        game_context.bg_renderer = BgRenderer(
            game_params.get_screen(),
            Constants.PLAY_AREA_COORDS_PX,
            Constants.BLOCK_HEIGHT,
            Constants.BLOCK_HEIGHT,
            game_context.score_keeper,
            Constants.SCORE_FONT_FILE)

        game_context.board = Board(game_params.get_geometry(), Constants.PIECE_DROP_POS)

        game_context.gameplay = Gameplay(
            game_context.board,
            game_params.get_geometry(),
            game_context.score_keeper,
            game_params.get_jukebox(),
            game_params.get_key_mapper())

        self.game_context = game_context

    @staticmethod
    def init_states(game_params):
        states = namedtuple("States", ["menu", "game_over", "high_scores", "name_entry"])

        menu_state_builder = MenuStateBuilder(
            game_params.get_screen(),
            Constants.MENU_FONT_FILE,
            Constants.TITLE_FONT_FILE,
            game_params.get_jukebox(),
            game_params.get_key_change_publisher(),
            Constants.KEYS,
            game_params.get_key_mapper())
        states.menu = menu_state_builder.build()

        states.game_over = GameOverScreen(game_params.get_screen(), Constants.GAME_OVER_FONT_FILE, Constants.KEYS)

        states.high_scores = LeaderBoardScreen(
            game_params.get_screen(), HighScoreReader(
                Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES), Constants.SCORE_FONT_FILE,
            Constants.SCORE_BANNER_FONT_FILE)

        states.name_entry = NameEntryScreen(
            game_params.get_screen(), Constants.NAME_ENTRY_FONT_FILE,
            Constants.NAME_ENTRY_TEXT_FONT_FILE, game_params.get_jukebox(), Constants.KEYS)

        return states

    def run_game(self):
        pygame_context = self.init_pygame()
        game_params = self.init_game_params(pygame_context)

        mode = Mode.MENU
        states = self.init_states(game_params)

        gameplay_handler = None

        game_params.get_jukebox().start_game_music()

        keep_playing = True
        while keep_playing:
            if mode == Mode.QUIT:
                keep_playing = False
            elif mode == Mode.MENU:
                game_in_progress = False if self.game_context is None else self.game_context.game_in_progress
                states.menu.set_paused(game_in_progress)
                handler = MenuHandler(states.menu, game_in_progress)
                mode = GameLoop(handler).run_event_loop()
            elif mode == Mode.NEW_GAME:
                self.new_game(game_params)
                gameplay_handler = GamePlayHandler(self.game_context, Constants.KEYS)
                mode = Mode.CONTINUE_GAME
            elif mode == Mode.CONTINUE_GAME:
                mode = GameLoop(gameplay_handler).run_event_loop()
            elif mode == Mode.GAME_OVER:
                self.game_context.game_in_progress = False
                # TODO: keep an instance of HighScoreReader and HighScoreWriter so I don't keep recreating it
                score = self.game_context.score_keeper.get_score()
                states.game_over.set_score(score)
                handler = GameOverHandler(states.game_over, score,
                                          HighScoreReader(Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES))
                # TODO: GameOverHandler should return ScoreBoard or NameEntry mode.
                # I can pass two interfaces into GameOverHandler. One knows how to get the
                # final score, and the other can decide whether the score is a high score.
                # to determine whether the current score. I have started those in new files.
                mode = GameLoop(handler).run_event_loop()
            elif mode == Mode.HIGH_SCORES:
                handler = ScoreBoardHandler(states.high_scores, Constants.KEYS)
                mode = GameLoop(handler).run_event_loop()
            elif mode == Mode.NAME_ENTRY:
                # TODO: preconstruct a HighScoreWriter so I don't keep recreating it.
                handler = NameEntryHandler(
                    states.name_entry,
                    self.game_context.score_keeper,
                    HighScoreWriter(Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES),
                    Constants.KEYS)
                mode = GameLoop(handler).run_event_loop()

        pygame.quit()


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
