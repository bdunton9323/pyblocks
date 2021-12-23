from gameplay.Keys import GameKeys
from screens.disposition_code import MenuAction


class MenuScreen(object):
    """Handles any events that occur while the game in the menu state."""

    def __init__(self, jukebox, game_keys, menu_navigator, menu_renderer):
        """
        Args:
            jukebox (sound.audio.Jukebox): allows the menu to change sound and music
            game_keys (gameplay.Keys.GameKeys): Allows the menu to see the current key mappings
            menu_navigator (screens.menu_navigator.MenuNavigator): Keeps track of the menu navigation state
            menu_renderer (screens.menu_renderer.MenuRenderer): Renders the menu onto the screen
        """
        self.game_keys = game_keys
        self.jukebox = jukebox
        self.menu_navigator = menu_navigator
        self.menu_renderer = menu_renderer

    def set_paused(self, paused):
        """Sets whether the game is paused (the menu looks different when the game is paused)"""
        if paused:
            self.menu_navigator.on_pause_event()
        else:
            self.menu_navigator.on_unpause_event()

    # Returns a disposition code for the result of the menu
    def on_key(self, key):
        """Handles a keypress event based on the state the menu is in
        Args:
            key (gameplay.Keys.Key): the key that was pressed
        """
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
        """Plays a sound indicating the cursor has moved"""
        self.jukebox.play_sound_menu_select()

    def render(self):
        """draws the menu onto the screen"""
        self.menu_renderer.render(self.menu_navigator.get_active_menu_context())
