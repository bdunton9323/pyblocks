import pygame
from gameboard.BgRenderer import BgRenderer
from gameboard.BlockRenderer import BlockRenderer
from gameboard.Board import Board
from gameplay.game_params import GameParams
from gameplay.gameplay import Gameplay
from gameplay.game_context import GameContext
from gameplay.game_context import GameStates
from gameplay.game_state_builders import MenuStateBuilder
from gameplay.keys import KeyChangePublisher
from gameplay.keys import KeyMapper
from gameplay.keys import GameKeys
from gameplay.score_keeper import ScoreKeeper
from geometry.Geometry import Geometry
from screens.gameover import GameOverScreen
from screens.NameEntryScreen import NameEntryScreen
from scoreboard.highscorepersistence import HighScoreReader
from scoreboard.highscorepersistence import HighScoreWriter
from scoreboard.LeaderBoardScreen import LeaderBoardScreen
from sound.audio import Jukebox

GFX_CONSTANTS = {
    # (x,y) size of the screen in pixels
    "screen_size": (800, 600),
    "block_width": 25,
    "block_height": 25,
    "field_width": 14,
    "field_height": 17
}

x1_tmp = GFX_CONSTANTS["block_width"] * 5
y1_tmp = GFX_CONSTANTS["block_height"] * 3
# (x1, y1, x2, y2) boundary of the playable area (where the pieces can move)
PLAY_AREA_BOUNDARY_PIXELS = (
    x1_tmp,
    y1_tmp,
    GFX_CONSTANTS["block_width"] * GFX_CONSTANTS["field_width"] + x1_tmp,
    GFX_CONSTANTS["block_height"] * GFX_CONSTANTS["field_height"] + y1_tmp
)
del x1_tmp
del y1_tmp


class HighScoreAccessorBuilder(object):

    HIGH_SCORE_FILE = "../highscores.dat"
    NUM_HIGH_SCORES = 10

    def build_reader(self):
        return HighScoreReader(self.HIGH_SCORE_FILE, self.NUM_HIGH_SCORES)

    def build_writer(self):
        return HighScoreWriter(self.HIGH_SCORE_FILE, self.NUM_HIGH_SCORES)


class PygameContext(object):
    def __init__(self):
        self.display = None
        self.clock = pygame.time.Clock()

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, val):
        self._display = val

    def get_clock(self) -> pygame.time.Clock:
        return self.clock

    @staticmethod
    def get_events():
        return pygame.event.get()

    @staticmethod
    def quit():
        pygame.quit()

    @staticmethod
    def flip_display():
        pygame.display.flip()


class PygameContextBuilder(object):

    @staticmethod
    def init_pygame():
        # Mixer has to be initialized before pygame.
        # http://stackoverflow.com/questions/18273722/pygame-sound-delay
        # http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.pre_init
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        pygame.init()
        surface = pygame.display.set_mode(GFX_CONSTANTS["screen_size"], pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBlocks")

        # set the key delay for holding down buttons
        pygame.key.set_repeat(250, 75)

        pygame_context = PygameContext()
        pygame_context.display = surface
        return pygame_context


class GameParamsBuilder(object):

    @staticmethod
    def init_game_params(pygame_context):
        params = GameParams()

        params.screen = pygame_context.display

        params.geometry = Geometry(
            GFX_CONSTANTS["block_width"],
            GFX_CONSTANTS["block_height"],
            PLAY_AREA_BOUNDARY_PIXELS)

        params.jukebox = Jukebox(pygame.mixer)

        # stuff for controlling what the keys are
        params.keys = GameKeys()
        key_mapper = KeyMapper(params.keys)
        key_change_publisher = KeyChangePublisher()
        key_change_publisher.subscribe(key_mapper.on_key_change)
        params.key_change_publisher = key_change_publisher
        params.key_mapper = key_mapper

        score_rw_builder = HighScoreAccessorBuilder()
        params.high_score_reader = score_rw_builder.build_reader()
        params.high_score_writer = score_rw_builder.build_writer()

        return params


FONT_FILES = {
    "menu": "gfx/font/Laundromatic/SFLaundromaticExtended.ttf",
    "score": "gfx/font/Laundromatic/SFLaundromaticExtended.ttf",
    "title": "gfx/font/crackman/crackman.ttf",
    "high_score_banner": "gfx/font/crackman/crackman.ttf",
    "game_over_screen": "gfx/font/crackman/crackman.ttf",
    "name_entry_prompt": "gfx/font/crackman/crackman.ttf",
    # Use a monospace font here because there is a character limit for the name
    # entry, which needs to fit exactly within the text box.
    "name_entry_textbox": "gfx/font/bpmono/BPmono.ttf"
}


class GameStatesBuilder(object):

    @staticmethod
    def init_game_states(game_params: GameParams):

        states = GameStates()

        menu_state_builder = MenuStateBuilder(
            game_params.screen,
            FONT_FILES["menu"],
            FONT_FILES["title"],
            game_params.jukebox,
            game_params.key_change_publisher,
            game_params.keys,
            game_params.key_mapper)
        states.menu_state = menu_state_builder.build()

        states.game_over_state = GameOverScreen(
            game_params.screen,
            FONT_FILES["game_over_screen"],
            game_params.keys)

        states.high_scores_state = LeaderBoardScreen(
            game_params.screen,
            game_params.high_score_reader,
            FONT_FILES["score"],
            FONT_FILES["high_score_banner"])

        states.name_entry_state = NameEntryScreen(
            game_params.screen,
            FONT_FILES["name_entry_prompt"],
            FONT_FILES["name_entry_textbox"],
            game_params.jukebox,
            game_params.keys)

        return states


class GameContextBuilder(object):

    @staticmethod
    def build_new_game_in_progress(game_params: GameParams):
        game_context = GameContext()
        game_context.game_in_progress = True
        game_context.score_keeper = ScoreKeeper()

        game_context.block_renderer = BlockRenderer(
            game_params.screen,
            game_params.geometry)

        game_context.bg_renderer = BgRenderer(
            game_params.screen,
            PLAY_AREA_BOUNDARY_PIXELS,
            GFX_CONSTANTS["block_width"],
            GFX_CONSTANTS["block_height"],
            game_context.score_keeper,
            FONT_FILES["score"])

        game_context.board = Board(game_params.geometry)

        game_context.gameplay = Gameplay(
            game_context.board,
            game_params.geometry,
            game_context.score_keeper,
            game_params.jukebox,
            game_params.key_mapper)

        return game_context
