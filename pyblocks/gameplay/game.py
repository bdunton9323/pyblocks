from gameplay.eventhandlers import *
from pygame.constants import KEYDOWN
from pygame.constants import QUIT


class Constants:
    FRAME_RATE = 60
    MILLISECONDS = 1000


class Game(object):

    def __init__(self, pygame_context_builder, game_params_builder, game_context_builder, game_states_builder):
        self.pygame_context = pygame_context_builder.init_pygame()
        self.game_params = game_params_builder.init_game_params(self.pygame_context)
        self.game_params.jukebox.start_game_music()
        self.game_states = game_states_builder.init_game_states(self.game_params)

        # stores info about the game in progress (we start with no game in progress)
        self.game_context = None
        self.game_context_builder = game_context_builder

    def run_game(self):
        mode = Mode.MENU
        while mode != Mode.QUIT:
            event_handler = self.enter_mode(mode)
            mode = GameLoop(self.pygame_context, event_handler, self.game_params.keys).run_event_loop()

    def enter_mode(self, mode):

        if mode == Mode.MENU:
            game_in_progress = self.game_context is not None and self.game_context.game_in_progress is True
            self.game_states.menu_state.set_paused(game_in_progress)
            return MenuHandler(self.game_states.menu_state, game_in_progress)

        elif mode == Mode.NEW_GAME:
            self.game_context = self.game_context_builder.build_new_game_in_progress(self.game_params)
            return GamePlayHandler(self.game_context, self.game_params.keys)

        elif mode == Mode.CONTINUE_GAME:
            return GamePlayHandler(self.game_context, self.game_params.keys)

        elif mode == Mode.GAME_OVER:
            self.game_context.game_in_progress = False
            score = self.game_context.score_keeper.get_score()
            self.game_states.game_over_state.set_score(score)

            return GameOverHandler(
                self.game_states.game_over_state, score,
                self.game_params.high_score_reader)

        elif mode == Mode.HIGH_SCORES:
            return ScoreBoardHandler(self.game_states.high_scores_state, self.game_params.keys)

        elif mode == Mode.NAME_ENTRY:
            return NameEntryHandler(
                self.game_states.name_entry_state,
                self.game_context.score_keeper,
                self.game_params.high_score_writer,
                self.game_params.keys)

        self.pygame_context.quit()

    @staticmethod
    def get_or_default(cache, key, default):
        if key in cache:
            return cache.get(key)
        cache[key] = default
        return default


class GameLoop(object):
    def __init__(self, pygame_context, event_handler, game_keys):
        self.pygame_context = pygame_context
        self.event_handler = event_handler
        self.game_keys = game_keys
        self.clock = self.pygame_context.get_clock()

    def run_event_loop(self):
        next_mode = None

        while next_mode is None:
            key = None
            for event in self.pygame_context.get_events():
                if event.type == QUIT:
                    next_mode = Mode.QUIT
                    self.event_handler.on_quit()

                elif event.type == KEYDOWN:
                    key = self.game_keys.from_pygame(event.key)
                    if key:
                        next_mode = self.event_handler.on_key(key)

            if next_mode is None:
                millis = int(1 / float(Constants.FRAME_RATE) * Constants.MILLISECONDS)
                next_mode = self.event_handler.on_tick(millis, key)
                self.event_handler.on_render()
                self.pygame_context.flip_display()
                self.clock.tick(Constants.FRAME_RATE)
        return next_mode
