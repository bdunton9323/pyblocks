from screens.MenuScreen import MenuScreen
from screens.menu_navigator import MenuNavigator
from screens.menu_handlers import MenuContextFactory
from screens.menu_renderer import MenuRenderer


class MenuStateBuilder:
    """
    A helper class for constructing the MenuScreen. This allows me to unit test the MenuScreen with mocked
    dependencies
    """

    def __init__(self, screen, font_file, title_font_file, jukebox, key_change_publisher, game_keys, key_mapper):
        """
        Args:
            screen (pygame.display): provides access to the screen for rendering the menu
            font_file (str): the path to the file containing the font to use for the menu options
            title_font_file (str): the path to the file containing the font for the title banner
            jukebox (sound.audio.Jukebox): allows the menu to change sound and music
            key_change_publisher (gameplay.keys.KeyChangePublisher): Allows the menu to change the key mappings
            game_keys (gameplay.keys.GameKeys): Allows the menu to see the current key mappings
            key_mapper (gameplay.keys.KeyMapper): Maps a game function to a key in the provided GameKeys
        """
        self.screen = screen
        self.font_file = font_file
        self.title_font_file = title_font_file
        self.jukebox = jukebox
        self.key_change_publisher = key_change_publisher
        self.game_keys = game_keys
        self.key_mapper = key_mapper

    def build(self):
        """
        Returns:
            screens.MenuScreen.MenuScreen: built from what was given in the constructor
        """
        menu_context_factory = MenuContextFactory(self.jukebox, self.key_change_publisher, self.game_keys,
            self.key_mapper, self.font_file, self.screen)
        menu_navigator = MenuNavigator(menu_context_factory)
        menu_renderer = MenuRenderer(self.screen, self.title_font_file)
        return MenuScreen(self.jukebox, self.game_keys, menu_navigator, menu_renderer)
