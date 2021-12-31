import unittest
from gameplay.keys import GameKeys
from screens.disposition_code import MenuAction
from screens.MenuScreen import MenuScreen
from unittest.mock import Mock


class TestMenuScreen(unittest.TestCase):

    def setUp(self):
        self.mock_jukebox = Mock()
        self.mock_navigator = Mock()
        self.mock_renderer = Mock()
        # it didn't feel worth the effort to create a mock. It's really just a wrapper around a static map.
        self.game_keys = GameKeys()
        self.menu_screen = MenuScreen(self.mock_jukebox, self.game_keys, self.mock_navigator, self.mock_renderer)

    def test_keypress_should_play_sound(self):
        self.menu_screen.on_key(self.game_keys.by_name('up'))
        self.mock_jukebox.play_sound_menu_select.assert_called_with()

    def test_pause(self):
        self.menu_screen.set_paused(True)
        self.mock_navigator.on_pause_event.assert_called_once()
        self.assertEqual(1, len(self.mock_navigator.mock_calls))

    def test_unpause(self):
        self.menu_screen.set_paused(False)
        self.mock_navigator.on_unpause_event.assert_called_once()
        self.assertEqual(1, len(self.mock_navigator.mock_calls))

    def test_escape_key_navigates_back(self):
        disposition = self.menu_screen.on_key(self.game_keys.by_name('Escape'))
        self.assertEqual(MenuAction.MENU, disposition)
        self.mock_navigator.escape.assert_called_once()
        self.assertEqual(1, len(self.mock_navigator.mock_calls))

    def test_down_key_navigates_down(self):
        self.mock_navigator.is_listening_for_key.return_value = False
        disposition = self.menu_screen.on_key(self.game_keys.by_name("Down"))
        self.assertEqual(MenuAction.MENU, disposition)
        self.mock_navigator.cursor_down.assert_called_once()

    def test_up_key_navigates_up(self):
        self.mock_navigator.is_listening_for_key.return_value = False
        disposition = self.menu_screen.on_key(self.game_keys.by_name("Up"))
        self.assertEqual(MenuAction.MENU, disposition)
        self.mock_navigator.cursor_up.assert_called_once()

    def test_return_key_executes_option(self):
        self.mock_navigator.is_listening_for_key.return_value = False
        self.mock_navigator.execute_current_option.return_value = MenuAction.QUIT

        disposition = self.menu_screen.on_key(self.game_keys.by_name("Enter"))
        self.assertEqual(MenuAction.QUIT, disposition)
        self.mock_navigator.execute_current_option.assert_called_once()

    def test_return_key_not_intercepted_by_listening_menu(self):
        self.mock_navigator.is_listening_for_key.return_value = True
        self.mock_navigator.execute_current_option.return_value = MenuAction.QUIT

        disposition = self.menu_screen.on_key(self.game_keys.by_name("Enter"))
        self.assertEqual(MenuAction.QUIT, disposition)
        self.mock_navigator.delegate_key_event.assert_not_called()

    def test_key_intercepted_by_listening_menu(self):
        self.mock_navigator.is_listening_for_key.return_value = True
        disposition = self.menu_screen.on_key(self.game_keys.by_name("A"))
        self.assertEqual(MenuAction.MENU, disposition)
        self.mock_navigator.delegate_key_event.assert_called_once_with(self.game_keys.by_name("A"))

    def test_render(self):
        expected_context = 'anything'
        self.mock_navigator.get_active_menu_context.return_value = expected_context
        self.menu_screen.render()
        self.mock_renderer.render.assert_called_once_with(expected_context)




