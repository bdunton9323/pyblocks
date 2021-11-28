
# Keeps track of where the user is in the menu tree, and facilitates moving around in the menus.
class MenuNavigator(object):

    def __init__(self, screen_factory):
        self.screen_factory = screen_factory
        # Stack of active menus. Allows us to go into submenus and pop back.
        self.navigation_path = []
        self.navigation_path.append(screen_factory.build_top_level_menu())

    def execute_current_option(self):
        active_menu = self.get_active_menu_state()
        next_state_info = self.get_active_menu_state().execute_current_option()
        # If this option goes into a sub-menu, update the navigation path
        if next_state_info.get_active_menu_screen() != active_menu:
            self.navigation_path.append(next_state_info.get_active_menu_screen())

    def cursor_down(self):
        self.get_active_menu_state().move_to_next_option()

    def cursor_up(self):
        self.get_active_menu_state().move_to_previous_option()

    def escape(self):
        self.navigation_path.pop()

    def get_active_menu_state(self):
        return self.navigation_path[-1]
