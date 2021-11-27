from abc import ABC, abstractmethod
from screens.disposition_code import MenuAction
from gameplay.Keys import KeyFunction


class MenuHandlerFactory(object):

    def __init__(self, jukebox, key_change_publisher, game_keys, key_mapper):
        self.jukebox = jukebox
        self.key_change_publisher = key_change_publisher
        self.game_keys = game_keys
        self.key_mapper = key_mapper

    def build_top_level_menu_screen(self, is_game_paused):
        if is_game_paused:
            return TopLevelPausedMenuHandler(self)
        else:
            return TopLevelMenuHandler(self)

    def build_music_selection_screen(self):
        return MusicSelectionMenuHandler(self, self.jukebox)

    def build_options_screen(self):
        return OptionsMenuHandler(self)

    def build_key_changing_screen(self):
        return KeySettingMenuHandler(self, self.key_change_publisher, self.game_keys, self.key_mapper)


# Abstract base class for all menu and submenu handlers
class MenuHandler(ABC):

    # handler_factory - allows the handler to create a new handler for a submenu it controls
    def __init__(self, handler_factory):
        self.selected_index = 0
        self.handler_factory = handler_factory

    @abstractmethod
    def execute_current_option(self):
        return None

    @abstractmethod
    def get_num_states(self):
        return 0

    def get_handler_factory(self):
        return self.handler_factory

    def get_selected_index(self):
        return self.selected_index

    def move_to_next_option(self):
        self.selected_index += 1
        if self.selected_index == self.get_num_states():
            self.selected_index = 0

    def move_to_previous_option(self):
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = self.get_num_states()


class TopLevelMenuHandler(MenuHandler):
    def __init__(self, handler_factory):
        super(TopLevelMenuHandler, self).__init__(handler_factory)

    def get_num_states(self):
        return 4

    def execute_current_option(self):
        if self.get_selected_index() == 0:
            return NextStateInfo(self, MenuAction.PLAY_GAME)
        elif self.get_selected_index() == 1:
            return NextStateInfo(self, MenuAction.HIGH_SCORES)
        elif self.get_selected_index() == 2:
            return NextStateInfo(self.get_handler_factory().build_options_screen(), MenuAction.MENU)
        elif self.get_selected_index() == 3:
            return NextStateInfo(self, MenuAction.QUIT)


class TopLevelPausedMenuHandler(MenuHandler):
    def __init__(self, handler_factory):
        super(TopLevelPausedMenuHandler, self).__init__(handler_factory)

    def get_num_states(self):
        return 5

    def execute_current_option(self):
        if self.get_selected_index() == 0:
            return NextStateInfo(self, MenuAction.PLAY_GAME)
        elif self.get_selected_index() == 1:
            return NextStateInfo(self, MenuAction.NEW_GAME)
        elif self.get_selected_index() == 2:
            return NextStateInfo(self, MenuAction.SHOW_HIGH_SCORES)
        elif self.get_selected_index == 3:
            return NextStateInfo(self.get_handler_factory().build_options_screen(), MenuAction.MENU)
        elif self.get_selected_index == 4:
            return NextStateInfo(self, MenuAction.QUIT)


class MusicSelectionMenuHandler(MenuHandler):
    def __init__(self, handler_factory, jukebox):
        super(MusicSelectionMenuHandler, self).__init__(handler_factory)
        self.songs = jukebox.get_available_music()
        self.jukebox = jukebox

    def get_num_states(self):
        return len(self.songs)

    def execute_current_option(self):
        selected_song = self.songs[self.get_selected_index()]
        self.jukebox.set_song(selected_song)


class KeySettingMenuHandler(MenuHandler):
    KEY_FUNCTIONS = [
        KeyFunction.MOVE_LEFT,
        KeyFunction.MOVE_RIGHT,
        KeyFunction.MOVE_DOWN,
        KeyFunction.DROP,
        KeyFunction.ROTATE_LEFT,
        KeyFunction.ROTATE_RIGHT]

    def __init__(self, handler_factory, key_change_publisher, game_keys, key_mapper):
        super(KeySettingMenuHandler, self).__init__(handler_factory)
        self.key_change_publisher = key_change_publisher
        self.game_keys = game_keys
        self.key_mapper = key_mapper

    def get_num_states(self):
        return

    def execute_current_option(self):
        pass


class OptionsMenuHandler(MenuHandler):
    def __init__(self, handler_factory):
        super(OptionsMenuHandler, self).__init__(handler_factory)

    def get_num_states(self):
        return

    def execute_current_option(self):
        pass


class NextStateInfo(object):
    def __init__(self, active_menu_screen, game_state):
        self.active_menu_screen = active_menu_screen
        self.game_state = game_state

    def get_active_menu_screen(self):
        return self.active_menu_screen

    def get_game_state(self):
        return self.game_state
