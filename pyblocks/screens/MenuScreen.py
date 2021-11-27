import pygame
from gameplay.Keys import GameKeys
from gameplay.Keys import KeyFunction
from screens.disposition_code import MenuAction


class MenuScreen(object):
    TEXT_COLOR = (128, 255, 255)
    BLACK = (0, 0, 0, 0)
    # pixels to put between each menu item
    PADDING = 50
    BANNER_TEXT = "BLOCKS"

    BANNER_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (0, 242, 255), (191, 0, 179)]

    def __init__(self, screen, font_file, title_font_file, jukebox, key_change_publisher, game_keys, key_mapper):
        self.screen = screen
        self.font_file = font_file
        self.title_font_file = title_font_file
        self.paused = False
        self.jukebox = jukebox
        self.sound_on = True
        self.music_on = True
        self.game_keys = game_keys
        self.init_menus(key_change_publisher, key_mapper)
        self.render_banner()

    def init_menus(self, key_change_publisher, key_mapper):
        normal_highlight = HighlightStrategyNormal()
        self.menus = {}
        self.init_options_menu()
        self.menus['top_level'] = SubMenu("Main",
                                          StandardTextInitializer(self.font_file, self.screen.get_size(),
                                                                  ["New Game", "High Scores", "Options", "Quit"]),
                                          normal_highlight)
        self.menus['top_level_paused'] = SubMenu("Main Paused",
                                                 StandardTextInitializer(self.font_file, self.screen.get_size(),
                                                                         ["Resume Game", "New Game", "High Scores",
                                                                          "Options", "Quit"]), normal_highlight)
        self.menus['music_selection'] = SubMenu("Music Selection",
                                                StandardTextInitializer(self.font_file, self.screen.get_size(),
                                                                        self.jukebox.get_available_music()),
                                                normal_highlight)

        self.key_menu_handler = KeyMenuHandler(key_change_publisher, self.game_keys, key_mapper)
        special_highlight = HighlightStrategyKeyMapping(self.key_menu_handler)
        self.menus['keys'] = SubMenu("Keys",
                                     LazyTextInitializer(self.key_menu_handler, self.font_file, self.screen.get_size()),
                                     special_highlight)

        self.active_menu = self.menus['top_level']
        # the index of the current selection in self.active_menu
        self.selection = 0

    def init_options_menu(self):
        highlighter = HighlightStrategyNormal()
        self.options_toggler = OptionsToggler()
        initializer = LazyTextInitializer(self.options_toggler, self.font_file,
                                          self.screen.get_size())
        self.menus['options'] = SubMenu("Options", initializer, highlighter)

    # Change the labels on the menu to indicate current toggle settings
    def update_options_menu(self, sound_on, music_on):
        self.options_toggler.enable_sound(sound_on)
        self.options_toggler.enable_music(music_on)

    def set_paused(self, paused):
        # going from unpaused to paused
        if paused and not self.paused:
            if self.active_menu == self.menus['top_level']:
                self.active_menu = self.menus['top_level_paused']
                self.selection = 0
        elif not paused and self.paused:
            if self.active_menu == self.menus['top_level_paused']:
                self.active_menu = self.menus['top_level']
                self.selection = 0
        self.paused = paused

    def render_banner(self):
        self.banner = []
        font = pygame.font.Font(self.title_font_file, 120)
        font_size = font.size(MenuScreen.BANNER_TEXT)

        # Get the upper left corner of where the text should go
        screen_size = self.screen.get_size()
        x = screen_size[0] // 2 - font_size[0] // 2
        y = screen_size[1] // 4 - font_size[1] // 2

        letters = list(MenuScreen.BANNER_TEXT)
        for letter, color in zip(letters, MenuScreen.BANNER_COLORS):
            rendered = font.render(letter, True, color)
            self.banner.append((rendered, (x, y)))
            x += rendered.get_size()[0]

    # Returns a disposition code for the result of the menu
    def on_key(self, key):
        if key == self.game_keys.by_id(GameKeys.ESCAPE):
            return self.handle_menu_key()

        # the key mapping menu needs first access to the key press
        if self.active_menu == self.menus['keys']:
            if self.key_menu_handler.handle_key_press(key, self.selection):
                return MenuAction.MENU

        elif key == self.game_keys.by_id(GameKeys.ENTER):
            self.play_sound()
            return self.do_menu_action()

        if key == self.game_keys.by_id(GameKeys.DOWN):
            self.play_sound()
            self.selection += 1
            if self.selection >= len(self.active_menu):
                self.selection = 0

        elif key == self.game_keys.by_id(GameKeys.UP):
            self.play_sound()
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.active_menu) - 1

        return MenuAction.MENU

    def handle_menu_key(self):
        self.play_sound()
        if self.active_menu == self.menus['music_selection']:
            self.active_menu = self.menus['options']
            self.selection = 0
        elif self.active_menu == self.menus['options']:
            if self.paused:
                self.active_menu = self.menus['top_level_paused']
                self.selection = 0
            else:
                self.active_menu = self.menus['top_level']
                self.selection = 0
        elif self.active_menu == self.menus['keys']:
            self.active_menu = self.menus['options']
            self.selection = 0
        elif self.active_menu not in [self.menus['top_level'], self.menus['top_level_paused']]:
            self.active_menu = self.menus['top_level']
            return MenuAction.MENU

    # The user has selected an option, so execute whatever it is
    # TODO: this is getting cumbersome.
    def do_menu_action(self):
        if self.active_menu == self.menus['top_level']:
            if self.selection == 0:
                return MenuAction.PLAY_GAME
            elif self.selection == 1:
                return MenuAction.SHOW_HIGH_SCORES
            elif self.selection == 2:
                self.active_menu = self.menus['options']
                self.selection = 0
                return MenuAction.MENU
            elif self.selection == 3:
                return MenuAction.QUIT

        elif self.active_menu == self.menus['top_level_paused']:
            if self.selection == 0:
                return MenuAction.PLAY_GAME
            elif self.selection == 1:
                return MenuAction.NEW_GAME
            elif self.selection == 2:
                return MenuAction.SHOW_HIGH_SCORES
            elif self.selection == 3:
                self.active_menu = self.menus['options']
                self.selection = 0
                return MenuAction.MENU
            elif self.selection == 4:
                return MenuAction.QUIT

        elif self.active_menu == self.menus['options']:
            if self.selection == 0:
                self.sound_on = not self.sound_on
                self.jukebox.enable_sound(self.sound_on)
                self.update_options_menu(self.sound_on, self.music_on)
            elif self.selection == 1:
                self.music_on = not self.music_on
                self.jukebox.enable_music(self.music_on)
                self.update_options_menu(self.sound_on, self.music_on)
            elif self.selection == 2:
                self.active_menu = self.menus['music_selection']
                self.selection = 0
            elif self.selection == 3:
                self.active_menu = self.menus['keys']
                self.selection = 0
            return MenuAction.MENU

        elif self.active_menu == self.menus['music_selection']:
            song = self.menus['music_selection'][self.selection]
            self.jukebox.set_song(song)

        elif self.active_menu == self.menus['keys']:
            if self.selection == 0:
                pass
        return MenuAction.MENU

    def play_sound(self):
        self.jukebox.play_sound_menu_select()

    def draw_banner(self):
        for letter in self.banner:
            self.screen.blit(letter[0], letter[1])

    def draw_text(self):
        for item in self.active_menu.get_all_rendered_text().values():
            self.screen.blit(item[0], (item[3], item[4]))

    def highlight_selection(self):
        overhang_horiz_px = 20
        overhang_vert_px = 5
        item = self.active_menu.get_rendered_text(self.selection)
        left = item[3] - overhang_horiz_px
        top = item[4] - overhang_vert_px
        width = item[1] + (2 * overhang_horiz_px)
        height = item[2] + (2 * overhang_vert_px)

        color = self.active_menu.get_highlight_color()

        pygame.draw.rect(self.screen, color, (left, top, width, height), 0)

    def render(self):
        # TODO: I can check if anything has changed before rendering anything
        self.screen.fill(MenuScreen.BLACK)
        self.highlight_selection()
        self.draw_banner()
        self.draw_text()


# Renders all the menu options up front
class StandardTextInitializer(object):
    def __init__(self, font_file, screen_size, labels):
        self.font = pygame.font.Font(font_file, 50)
        self.screen_size = screen_size
        self.labels = labels
        self.rendered = {}
        self.text = {}

    def get_labels(self):
        return self.labels

    def init_text(self):
        self.rendered = {}
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2

        itemindex = 0
        self.text = {}
        for label in self.labels:
            item = _build_menu_item(label, itemindex, center_x, center_y, self.font)
            self.rendered[label] = item
            itemindex += 1

    # The items are in the following format:
    #   {"item name": (renderedText, textWidth, textHeight, xPos, yPos), ...}
    def get_rendered_items(self):
        return self.rendered


def _build_menu_item(label, itemindex, center_x, center_y, font):
    text_size = font.size(label)
    xpos = center_x - (text_size[0] // 2)
    ypos = center_y - (text_size[1] // 2) + (MenuScreen.PADDING * itemindex)
    return (
        font.render(label, 1, MenuScreen.TEXT_COLOR),
        # width of text
        text_size[0],
        # height of text
        text_size[1],
        # x position on screen of text
        xpos,
        # y position on screen of text
        ypos
    )


# Renders the labels each time they are needed. This allows the menu labels
# to be dynamic (e.g. text that changes as options are toggled)
class LazyTextInitializer(object):
    def __init__(self, toggler, font_file, screen_size):
        self.toggler = toggler
        self.font = pygame.font.Font(font_file, 50)
        self.screen_size = screen_size
        self.center_x = screen_size[0] // 2
        self.center_y = screen_size[1] // 2
        self.rendered = {}

    # We will generate our own labels, so this is a no-op
    def init_text(self):
        pass

    def get_labels(self):
        return self.toggler.get_labels()

    def render_labels(self, labels):
        index = 0
        updated = {}
        for label in labels:
            # cache the labels because rendering is expensive
            if label in self.rendered:
                updated[label] = self.rendered[label]
            else:
                updated[label] = _build_menu_item(label, index, self.center_x, self.center_y, self.font)
            index += 1

        self.rendered = updated
        return self.rendered

    # The items are in the following format:
    #   {"item name": (renderedText, textWidth, textHeight, xPos, yPos), ...}
    def get_rendered_items(self):
        return self.render_labels(self.get_labels())


class OptionsToggler(object):
    SOUND_ON = "Sound [On] / Off"
    SOUND_OFF = "Sound On / [Off]"
    MUSIC_ON = "Music [On] / Off"
    MUSIC_OFF = "Music On / [Off]"
    CHANGE_SONG = "Change Song"
    CHANGE_KEYS = "Change Keys"

    def __init__(self):
        self.sound_on = True
        self.music_on = True

    def enable_sound(self, enabled):
        self.sound_on = enabled

    def enable_music(self, enabled):
        self.music_on = enabled

    def get_labels(self):
        sound = OptionsToggler.SOUND_ON if self.sound_on else OptionsToggler.SOUND_OFF
        music = OptionsToggler.MUSIC_ON if self.music_on else OptionsToggler.MUSIC_OFF
        return [sound, music, OptionsToggler.CHANGE_SONG, OptionsToggler.CHANGE_KEYS]


class SubMenu(object):
    def __init__(self, name, initializer, highlight_strategy):
        self.name = name
        self.initializer = initializer
        self.highlight_strategy = highlight_strategy
        initializer.init_text()

    def get_name(self):
        return self.name

    def get_highlight_color(self):
        return self.highlight_strategy.get_highlight_color()

    def get_all_rendered_text(self):
        return self.initializer.get_rendered_items()

    def get_rendered_text(self, index):
        label = self.initializer.get_labels()[index]
        return self.initializer.get_rendered_items()[label]

    def __len__(self):
        return len(self.initializer.get_labels())

    def __iter__(self):
        return iter(self.initializer.get_labels())

    def __getitem__(self, index):
        return self.initializer.get_labels()[index]

    def __setitem__(self, index, value):
        raise NotImplementedError(
            "Make sure there is really a need before implementing this")


class KeyMenuHandler(object):
    # param - key_change_publisher - used to publish key changes to any listeners
    # param - key_mapper - gets the current key bindings
    def __init__(self, key_change_publisher, game_keys, key_mapper):
        self.game_keys = game_keys
        self.listening = False

        # keep from building the labels on every frame
        self.dirty = True
        self.publisher = key_change_publisher

        self.labels = []

        # This is the order the menu options are presented in. This will be used to
        # get the key function from the menu item index.
        self.index_to_function = [KeyFunction.MOVE_LEFT, KeyFunction.MOVE_RIGHT, KeyFunction.MOVE_DOWN,
                                  KeyFunction.DROP, KeyFunction.ROTATE_LEFT, KeyFunction.ROTATE_RIGHT]

        self.function_to_label = {
            KeyFunction.MOVE_LEFT: "Move Left: ",
            KeyFunction.MOVE_RIGHT: "Move Right: ",
            KeyFunction.MOVE_DOWN: "Move Down: ",
            KeyFunction.DROP: "Drop Piece: ",
            KeyFunction.ROTATE_LEFT: "Rotate Left: ",
            KeyFunction.ROTATE_RIGHT: "Rotate Right: "
        }

        self.custom_text = {
            KeyFunction.MOVE_LEFT: key_mapper.get_key_by_function(KeyFunction.MOVE_LEFT).name,
            KeyFunction.MOVE_RIGHT: key_mapper.get_key_by_function(KeyFunction.MOVE_RIGHT).name,
            KeyFunction.MOVE_DOWN: key_mapper.get_key_by_function(KeyFunction.MOVE_DOWN).name,
            KeyFunction.DROP: key_mapper.get_key_by_function(KeyFunction.DROP).name,
            KeyFunction.ROTATE_LEFT: key_mapper.get_key_by_function(KeyFunction.ROTATE_LEFT).name,
            KeyFunction.ROTATE_RIGHT: key_mapper.get_key_by_function(KeyFunction.ROTATE_RIGHT).name
        }

    def get_labels(self):
        if not self.dirty:
            return self.labels

        self.dirty = False

        self.labels = []
        for function in self.index_to_function:
            self.labels.append(self.function_to_label[function] + '<' + self.custom_text[function] + '>')

        return self.labels

    def is_listening(self):
        return self.listening

    # return True if the key was handled
    # return False if the key should be handled by the main menu handler
    def handle_key_press(self, key, label_index):
        if key == self.game_keys.by_id(GameKeys.ENTER):
            self.listening = not self.listening
            return True
        if not self.listening:
            return False

        # The labels have changed
        self.dirty = True

        key_function = self.index_to_function[label_index]
        self.custom_text[key_function] = self.game_keys.by_id(key.id).name

        # Notify all subscribers of the key change
        self.publisher.on_key_change(key_function, key)
        self.listening = False
        return True


# A simple highlight strategy where the highlight color is always the same
# regardless of mode
class HighlightStrategyNormal(object):
    HIGHLIGHT_COLOR = (0, 0, 255)

    def __init__(self):
        pass

    def get_highlight_color(self):
        return HighlightStrategyNormal.HIGHLIGHT_COLOR


# This highlight strategy highlights a different color if the menu is waiting
# for the user to enter a new key.
class HighlightStrategyKeyMapping(object):
    SPECIAL_HIGHLIGHT = (128, 0, 0)
    NORMAL_HIGHLIGHT = (0, 0, 255)

    def __init__(self, menu_handler):
        self.menu_handler = menu_handler

    def get_highlight_color(self):
        if self.menu_handler.is_listening():
            return HighlightStrategyKeyMapping.SPECIAL_HIGHLIGHT
        else:
            return HighlightStrategyKeyMapping.NORMAL_HIGHLIGHT
