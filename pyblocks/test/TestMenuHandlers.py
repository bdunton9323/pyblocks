import os
import unittest
from pathlib import Path
from pygame import font
from unittest.mock import Mock
from unittest.mock import MagicMock
from gameplay.Keys import GameKeys
from screens.disposition_code import MenuAction
from screens.menu_handlers import MenuContextFactory
from screens.menu_handlers import MenuContext
from screens.menu_handlers import MenuRenderInfo
from screens.menu_handlers import TopLevelMenuContext
from screens.menu_handlers import TopLevelPausedMenuContext
from screens.menu_handlers import MusicSelectionMenuContext
from screens.menu_handlers import KeySettingMenuContext
from screens.menu_handlers import OptionsMenuContext
from screens.menu_handlers import NextStateInfo
from screens.menu_renderer import StandardTextRenderer


class TestTopLevelMenu(unittest.TestCase):

    def setUp(self):
        # key_change_publisher, game_keys, key_mapper, font_file, screen
        self.jukebox = Mock()
        self.key_change_publisher = Mock()
        self.game_keys = GameKeys()
        self.key_mapper = Mock()
        # I could put a font file as a test resource but it's just as easy to change the test if I change the real fonts
        self.font_file = self._get_test_font_file()
        self.screen = MagicMock()
        font.init()
        self.context_factory = MenuContextFactory(
                self.jukebox, self.key_change_publisher, self.game_keys,
                self.key_mapper, self.font_file, self.screen)

    def test_toplevelmenu_labels(self):
        expected_labels = ["New Game", "High Scores", "Options", "Quit"]
        menu = self.context_factory.build_top_level_menu_screen(False)
        actual_labels = menu.get_render_info().get_labels()
        self.assertListEqual(expected_labels, actual_labels)

    def test_toplevelmenu_execute_play_game(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.assertEqual(0, menu.get_selected_index())
        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.PLAY_GAME, next_state.get_menu_action())

    def test_toplevelmenu_execute_high_scores(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.move_down_n(1, menu)

        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.SHOW_HIGH_SCORES, next_state.get_menu_action())

    def test_toplevelmenu_execute_options(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.move_down_n(2, menu)

        next_state = menu.execute_current_option()
        self.assertIsInstance(next_state.active_menu_screen, OptionsMenuContext)

    def test_toplevelmenu_execute_quit(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.move_down_n(3, menu)

        next_state = menu.execute_current_option()
        expected = NextStateInfo(menu, MenuAction.QUIT)
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.QUIT, next_state.get_menu_action())

    def test_toplevelmenu_not_listening_for_key(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.assertFalse(menu.is_listening_for_key())

    def test_toplevelmenu_render_info(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        render_info = menu.get_render_info()
        self.assertIsInstance(render_info.get_text_renderer(), StandardTextRenderer)

    def test_pausedmenu_labels(self):
        pass

    def test_pausedmenu_execute_resume_game(self):
        pass

    def test_pausedmenu_execute_new_game(self):
        pass

    def test_paused_menu_execute_high_scores(self):
        pass

    def test_paused_menu_execute_options(self):
        pass

    def test_paused_menu_execute_quit(self):
        pass

    def test_pausedmenu_not_listening_for_key(self):
        pass

    def test_pausedmenu_render_info(self):
        pass

    @staticmethod
    def move_down_n(n, menu):
        for _ in range(n):
            menu.move_to_next_option()

    @staticmethod
    def _get_test_font_file():
        current_path = Path(os.path.dirname(os.path.realpath(__file__)))
        return str(current_path / "resources" / "BPmono.ttf")



class TestOtherThing(unittest.TestCase):
    def test_something(self):
        self.assertTrue(False)
