

class MenuNavigator(object):
    """
    Keeps track of where the user is in the menu tree, and facilitates moving around in the menus.
    """

    def __init__(self, context_factory):
        """
        Args:
            context_factory (screens.menu_handlers.MenuContextFactory): Responsible for constructing the state contexts
                for each menu and submenu
        """
        self.context_factory = context_factory
        # Stack of active menus. Allows us to go into submenus and pop back.
        self.navigation_path = []
        self.navigation_path.append(context_factory.build_top_level_menu_screen(False))
        self.game_paused = False

    def execute_current_option(self):
        """
        Returns:
            MenuAction: indicates the next game state that resulted from the menu action
        """
        active_menu = self.get_active_menu_context()
        next_state_info = active_menu.execute_current_option()
        # If this option goes into a sub-menu, update the navigation path
        if next_state_info.get_active_menu_screen() != active_menu:
            self.navigation_path.append(next_state_info.get_active_menu_screen())
        return next_state_info.get_menu_action()

    def cursor_down(self):
        self.get_active_menu_context().move_to_next_option()

    def cursor_up(self):
        self.get_active_menu_context().move_to_previous_option()

    def escape(self):
        # escape shouldn't do anything if we're not in a submenu
        if len(self.navigation_path) > 1:
            self.navigation_path.pop()

    def on_pause_event(self):
        if not self.game_paused:
            self.navigation_path = []
            self.navigation_path.append(self.context_factory.build_top_level_menu_screen(True))

    def on_unpause_event(self):
        if self.game_paused:
            self.navigation_path = []
            self.navigation_path.append(self.context_factory.build_top_level_menu_screen(False))

    def delegate_key_event(self, key):
        self.get_active_menu_context().handle_key_event(key)

    def get_active_menu_context(self):
        return self.navigation_path[-1]

    # Some menus (like the key mapping menu) need to take control of the key press instead of the menu navigator
    # This indicates whether the current menu is taking over control of handling.
    def is_listening_for_key(self):
        return self.get_active_menu_context().is_listening_for_key()
