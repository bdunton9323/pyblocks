from gameplay.Keys import GameKeys
from screens.disposition_code import MenuAction
from screens.menu_renderer import MenuRenderer
from screens.menu_navigator import MenuNavigator
from screens.menu_handlers import MenuContextFactory


class MenuScreen(object):

    # TODO: I left off here. I just need to wire a few things up maybe
    def __init__(self, screen, font_file, title_font_file, jukebox, key_change_publisher, game_keys, key_mapper):
        self.game_keys = game_keys
        self.jukebox = jukebox
        context_factory = MenuContextFactory(jukebox, key_change_publisher, game_keys, key_mapper, font_file, screen)
        self.menu_navigator = MenuNavigator(context_factory)
        self.menu_renderer = MenuRenderer(screen, title_font_file)

    def set_paused(self, paused):
        self.menu_navigator.on_pause()

    # Returns a disposition code for the result of the menu
    def on_key(self, key):
        self.play_sound()

        if key == self.game_keys.by_id(GameKeys.ESCAPE):
            self.menu_navigator.escape()
            return MenuAction.MENU

        if key == self.game_keys.by_id(GameKeys.ENTER):
            return self.menu_navigator.execute_current_option()

        # if a menu is taking over the handling of key events, we don't need to do anything else
        if self.menu_navigator.is_listening_for_key():
            self.menu_navigator.delegate_key_event(key)
            return MenuAction.MENU

        if key == self.game_keys.by_id(GameKeys.DOWN):
            self.menu_navigator.cursor_down()
        elif key == self.game_keys.by_id(GameKeys.UP):
            self.menu_navigator.cursor_up()

        return MenuAction.MENU

    def play_sound(self):
        self.jukebox.play_sound_menu_select()

    def render(self):
        self.menu_renderer.render(self.menu_navigator.get_active_menu_context())
