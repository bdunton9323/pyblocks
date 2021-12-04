from abc import ABC, abstractmethod
from screens.disposition_code import MenuAction
from screens.menu_renderer import StandardTextRenderer
from screens.menu_renderer import LazyTextRenderer
from screens.menu_renderer import HighlightStrategyNormal
from screens.menu_renderer import HighlightStrategyInputField
from gameplay.Keys import KeyFunction


# Responsible for building the MenuContext subclasses
class MenuContextFactory(object):

    def __init__(self, jukebox, key_change_publisher, game_keys, key_mapper, font_file, screen):
        self.jukebox = jukebox
        self.key_change_publisher = key_change_publisher
        self.game_keys = game_keys
        self.key_mapper = key_mapper
        self.font_file = font_file
        self.screen = screen

    def build_top_level_menu_screen(self, is_game_paused):
        if is_game_paused:
            return TopLevelPausedMenuContext(self, lambda name, labels: self._get_standard_builder(name, labels))
        else:
            return TopLevelMenuContext(self, lambda name, labels: self._get_standard_builder(name, labels))

    def build_music_selection_screen(self):
        return MusicSelectionMenuContext(self,
            lambda name, labels: self._get_standard_builder(name, labels), self.jukebox)

    def build_options_screen(self):
        return OptionsMenuContext(self,
            lambda name, label_provider: self._get_lazy_builder(name, label_provider),  self.jukebox)

    def build_key_changing_screen(self):
        return KeySettingMenuContext(self, self.key_change_publisher, self.game_keys, self.key_mapper,
            lambda name, label_provider, special_highlight_indicator: self._get_lazy_builder_special_highlight(
                name, label_provider, special_highlight_indicator))

    def _get_standard_builder(self, name, labels):
        return MenuRenderInfo(name, StandardTextRenderer(self.font_file, self.screen.get_size(), labels),
            HighlightStrategyNormal())

    def _get_lazy_builder(self, name, label_provider):
        return MenuRenderInfo(name, LazyTextRenderer(label_provider, self.font_file, self.screen.get_size()),
            HighlightStrategyNormal())

    def _get_lazy_builder_special_highlight(self, name, label_provider, special_highlight_indicator):
        return MenuRenderInfo(name, LazyTextRenderer(label_provider, self.font_file, self.screen.get_size()),
            HighlightStrategyInputField(special_highlight_indicator))


# Abstract base class for all menu and submenu contexts
class MenuContext(ABC):

    # context_factory - allows the handler to create a new handler for a submenu it controls
    def __init__(self, context_factory, render_info):
        self.selected_index = 0
        self.context_factory = context_factory
        self.render_info = render_info

    @abstractmethod
    def execute_current_option(self):
        return None

    @abstractmethod
    def get_num_options(self):
        return 0

    def is_listening_for_key(self):
        return False

    # goes along with is_listening_for_key
    def handle_key_event(self, key):
        return

    def get_render_info(self):
        return self.render_info

    def get_context_factory(self):
        return self.context_factory

    def get_selected_index(self):
        return self.selected_index

    def move_to_next_option(self):
        self.selected_index += 1
        if self.selected_index == self.get_num_options():
            self.selected_index = 0

    def move_to_previous_option(self):
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = self.get_num_options() - 1


# contains everything needed to render the menu
class MenuRenderInfo(object):
    def __init__(self, title, text_renderer, highlight_strategy):
        self.title = title
        self.text_renderer = text_renderer
        self.highlight_strategy = highlight_strategy

    def get_labels(self):
        pass

    def get_text_renderer(self):
        return self.text_renderer

    def get_highlight_color(self):
        return self.highlight_strategy.get_highlight_color()


class TopLevelMenuContext(MenuContext):
    def __init__(self, context_factory, render_info_builder):
        render_info = render_info_builder("Main", ["New Game", "High Scores", "Options", "Quit"])
        super(TopLevelMenuContext, self).__init__(context_factory, render_info)

    def get_num_options(self):
        return 4

    def execute_current_option(self):
        if self.get_selected_index() == 0:
            return NextStateInfo(self, MenuAction.PLAY_GAME)
        elif self.get_selected_index() == 1:
            return NextStateInfo(self, MenuAction.HIGH_SCORES)
        elif self.get_selected_index() == 2:
            return NextStateInfo(self.get_context_factory().build_options_screen(), MenuAction.MENU)
        elif self.get_selected_index() == 3:
            return NextStateInfo(self, MenuAction.QUIT)


class TopLevelPausedMenuContext(MenuContext):
    def __init__(self, context_factory, render_info_builder):
        render_info = render_info_builder("Main Paused",
            ["Resume Game", "New Game", "High Scores", "Options", "Quit"])
        super(TopLevelPausedMenuContext, self).__init__(context_factory, render_info)

    def get_num_options(self):
        return 5

    def execute_current_option(self):
        if self.get_selected_index() == 0:
            return NextStateInfo(self, MenuAction.PLAY_GAME)
        elif self.get_selected_index() == 1:
            return NextStateInfo(self, MenuAction.NEW_GAME)
        elif self.get_selected_index() == 2:
            return NextStateInfo(self, MenuAction.SHOW_HIGH_SCORES)
        elif self.get_selected_index == 3:
            return NextStateInfo(self.get_context_factory().build_options_screen(), MenuAction.MENU)
        elif self.get_selected_index == 4:
            return NextStateInfo(self, MenuAction.QUIT)


class MusicSelectionMenuContext(MenuContext):
    def __init__(self, context_factory, render_info_builder, jukebox):
        render_info = render_info_builder("Music Selection", jukebox.get_available_song_titles())
        super(MusicSelectionMenuContext, self).__init__(context_factory, render_info)
        self.songs = jukebox.get_available_song_titles()
        self.jukebox = jukebox

    def get_num_options(self):
        return len(self.songs)

    def execute_current_option(self):
        selected_song = self.songs[self.get_selected_index()]
        self.jukebox.set_song(selected_song)
        return NextStateInfo(self, MenuAction.MENU)


class KeySettingMenuContext(MenuContext):
    KEY_FUNCTIONS = [
        KeyFunction.MOVE_LEFT,
        KeyFunction.MOVE_RIGHT,
        KeyFunction.MOVE_DOWN,
        KeyFunction.DROP,
        KeyFunction.ROTATE_LEFT,
        KeyFunction.ROTATE_RIGHT]

    LABELS_FOR_KEY_FUNCTION = {
        KeyFunction.MOVE_LEFT: "Move Left: ",
        KeyFunction.MOVE_RIGHT: "Move Right: ",
        KeyFunction.MOVE_DOWN: "Move Down: ",
        KeyFunction.DROP: "Drop Piece: ",
        KeyFunction.ROTATE_LEFT: "Rotate Left: ",
        KeyFunction.ROTATE_RIGHT: "Rotate Right: "
    }

    def __init__(self, context_factory, key_change_publisher, game_keys, key_mapper, render_info_builder):
        render_info = render_info_builder("Keys", lambda: self.get_labels(), lambda: self.is_listening_for_key())
        super(KeySettingMenuContext, self).__init__(context_factory, render_info)
        self.key_change_publisher = key_change_publisher
        self.game_keys = game_keys
        self.key_mapper = key_mapper
        self.dirty = True
        self.listening_for_key = False
        self.cached_labels = []

        # provides the key name for the given key function
        self.function_to_key_name = {
            KeyFunction.MOVE_LEFT: key_mapper.get_key_by_function(KeyFunction.MOVE_LEFT).name,
            KeyFunction.MOVE_RIGHT: key_mapper.get_key_by_function(KeyFunction.MOVE_RIGHT).name,
            KeyFunction.MOVE_DOWN: key_mapper.get_key_by_function(KeyFunction.MOVE_DOWN).name,
            KeyFunction.DROP: key_mapper.get_key_by_function(KeyFunction.DROP).name,
            KeyFunction.ROTATE_LEFT: key_mapper.get_key_by_function(KeyFunction.ROTATE_LEFT).name,
            KeyFunction.ROTATE_RIGHT: key_mapper.get_key_by_function(KeyFunction.ROTATE_RIGHT).name
        }

        # This is the order the menu options are presented in. This will be used to
        # get the key function based on which menu item is selected.
        self.index_to_function = [KeyFunction.MOVE_LEFT, KeyFunction.MOVE_RIGHT, KeyFunction.MOVE_DOWN,
                                  KeyFunction.DROP, KeyFunction.ROTATE_LEFT, KeyFunction.ROTATE_RIGHT]

    def get_num_options(self):
        return len(self.index_to_function)

    def execute_current_option(self):
        self.listening_for_key = True
        return NextStateInfo(self, MenuAction.MENU)

    def is_listening_for_key(self):
        return self.listening_for_key

    # key - the Key that was pressed
    def handle_key_event(self, key):
        if not self.listening_for_key:
            return

        # The labels have changed
        self.dirty = True

        key_function = self.index_to_function[self.get_selected_index()]
        self.function_to_key_name[key_function] = self.game_keys.by_id(key.id).name

        # Notify all subscribers of the key change
        self.key_change_publisher.on_key_change(key_function, key)
        self.listening_for_key = False

    def get_labels(self):
        if not self.dirty:
            return self.cached_labels

        self.dirty = False

        new_labels = []
        for function in self.index_to_function:
            new_labels.append(self.LABELS_FOR_KEY_FUNCTION[function] + '<' + self.function_to_key_name[function] + '>')

        self.cached_labels = new_labels
        return self.cached_labels


class OptionsMenuContext(MenuContext):
    SOUND_ON = "Sound [On] / Off"
    SOUND_OFF = "Sound On / [Off]"
    MUSIC_ON = "Music [On] / Off"
    MUSIC_OFF = "Music On / [Off]"
    CHANGE_SONG = "Change Song"
    CHANGE_KEYS = "Change Keys"

    def __init__(self, context_factory, render_info_builder, jukebox):
        render_info = render_info_builder("Options", lambda: self.get_labels())
        super(OptionsMenuContext, self).__init__(context_factory, render_info)
        self.jukebox = jukebox
        self.sound_enabled = True
        self.music_enabled = True

    def get_num_options(self):
        return 4

    def execute_current_option(self):
        if self.get_selected_index() == 0:
            self.toggle_sound()
            return NextStateInfo(self, MenuAction.MENU)
        elif self.get_selected_index() == 1:
            self.toggle_music()
            return NextStateInfo(self, MenuAction.MENU)
        elif self.get_selected_index() == 2:
            return NextStateInfo(self.get_context_factory().build_music_selection_screen(), MenuAction.MENU)
        elif self.get_selected_index() == 3:
            return NextStateInfo(self.get_context_factory().build_key_changing_screen(), MenuAction.MENU)

    def toggle_sound(self):
        # this controls the text for the menu item
        self.sound_enabled = not self.sound_enabled
        self.jukebox.enable_sound(self.sound_enabled)

    def toggle_music(self):
        # this controls the text for the menu item
        self.music_enabled = not self.music_enabled
        self.jukebox.enable_music(self.music_enabled)

    def get_labels(self):
        sound = self.SOUND_ON if self.sound_enabled else self.SOUND_OFF
        music = self.MUSIC_ON if self.music_enabled else self.MUSIC_OFF
        return [sound, music, self.CHANGE_SONG, self.CHANGE_KEYS]


class NextStateInfo(object):
    def __init__(self, active_menu_screen, game_state):
        self.active_menu_screen = active_menu_screen
        self.game_state = game_state

    def get_active_menu_screen(self):
        return self.active_menu_screen

    def get_menu_action(self):
        return self.game_state

