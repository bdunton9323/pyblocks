import unittest
from unittest.mock import Mock
from gameplay.Keys import GameKeys
from screens.disposition_code import MenuAction
from screens.menu_navigator import MenuNavigator

class TestMenuNavigator(unittest.TestCase):

    def setUp(self):
        self.mock_factory = Mock()

        self.top_level_paused_menu = Mock(name='Paused menu')
        self.top_level_menu = Mock(name='Main menu')
        self.options_menu = Mock(name='Options menu')
        self.mock_factory.build_top_level_menu_screen.side_effect = lambda paused: self.mock_factory_return(paused)

        self.navigator = MenuNavigator(self.mock_factory)

    def test_cursor_down(self):
        self.navigator.cursor_down()
        self.top_level_menu.move_to_next_option.assert_called_once()

    def test_cursor_up(self):
        self.navigator.cursor_up()
        self.top_level_menu.move_to_previous_option.assert_called_once()

    def test_escape_at_top_level(self):
        self.navigator.escape()
        # to prove it didn't do anything, make sure we didn't back out of the current menu
        self.assert_current_menu(self.top_level_menu)

    def test_escape_from_submenu(self):
        self.traverse_to_submenu(self.options_menu)

        self.assert_current_menu(self.options_menu)
        self.navigator.escape()
        self.assert_current_menu(self.top_level_menu)

    def test_pause_while_not_paused(self):
        self.assert_current_menu(self.top_level_menu)
        self.navigator.on_pause_event()
        self.assert_current_menu(self.top_level_paused_menu)

    def test_pause_while_already_paused(self):
        self.navigator.on_pause_event()
        self.navigator.on_pause_event()
        self.assert_current_menu(self.top_level_paused_menu)

    def test_unpause_while_paused(self):
        self.navigator.on_pause_event()
        self.navigator.on_unpause_event()
        self.assert_current_menu(self.top_level_menu)

    def test_unpause_while_already_unpaused(self):
        self.assert_current_menu(self.top_level_menu)
        self.navigator.on_unpause_event()
        self.assert_current_menu(self.top_level_menu)

    def test_delegate_key_to_menu_context(self):
        key = GameKeys().by_name('A')
        self.navigator.delegate_key_event(key)
        self.top_level_menu.handle_key_event.assert_called_once_with(key)

    def test_get_active_context_returns_latest_context(self):
        self.assert_current_menu(self.top_level_menu)
        self.traverse_to_submenu(self.options_menu)
        self.assert_current_menu(self.options_menu)

    def test_menu_is_listening_for_key(self):
        self.top_level_menu.is_listening_for_key.return_value = True
        self.options_menu.is_listening_for_key.return_value = False
        self.assertEqual(True, self.navigator.is_listening_for_key())
        self.traverse_to_submenu(self.options_menu)
        self.assertEqual(False, self.navigator.is_listening_for_key())

    def mock_factory_return(self, is_paused):
        if is_paused:
            return self.top_level_paused_menu
        else:
            return self.top_level_menu

    def assert_current_menu(self, expected_menu):
        self.assertEqual(expected_menu, self.navigator.get_active_menu_context())

    def traverse_to_submenu(self, submenu):
        state_info = Mock()
        state_info.get_active_menu_screen.return_value = submenu
        state_info.get_menu_action.return_value = MenuAction.MENU
        self.top_level_menu.execute_current_option.return_value = state_info
        self.navigator.execute_current_option()
