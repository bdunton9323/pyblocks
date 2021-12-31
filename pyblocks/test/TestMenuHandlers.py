import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import Mock

from pygame import font

from gameplay.keys import GameKeys
from gameplay.keys import KeyMapper
from screens.disposition_code import MenuAction
from screens.menu_handlers import KeySettingMenuContext
from screens.menu_handlers import MenuContextFactory
from screens.menu_handlers import MusicSelectionMenuContext
from screens.menu_handlers import OptionsMenuContext
from screens.menu_renderer import LazyTextRenderer
from screens.menu_renderer import StandardTextRenderer


# TODO: it probably makes sense to have separate test classes for each of the MenuContexts
class TestTopLevelMenu(unittest.TestCase):

    def setUp(self):
        self.jukebox = Mock()
        self.key_change_publisher = Mock()

        # I could mock these but the real thing is really just a wrapper around a dict, so whatever
        self.game_keys = GameKeys()
        self.key_mapper = KeyMapper(self.game_keys)

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

    def test_toplevelmenu_wrap_navigation(self):
        menu = self.context_factory.build_top_level_menu_screen(False)
        self.assertEqual(0, menu.get_selected_index())
        menu.move_to_previous_option()
        self.assertEqual(3, menu.get_selected_index())
        menu.move_to_next_option()
        self.assertEqual(0, menu.get_selected_index())

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
        expected_labels = ["Resume Game", "New Game", "High Scores", "Options", "Quit"]
        menu = self.context_factory.build_top_level_menu_screen(True)
        actual_labels = menu.get_render_info().get_labels()
        self.assertListEqual(expected_labels, actual_labels)

    def test_pausedmenu_execute_resume_game(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.assertEqual(0, menu.get_selected_index())
        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.PLAY_GAME, next_state.get_menu_action())

    def test_pausedmenu_execute_new_game(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.move_down_n(1, menu)

        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.NEW_GAME, next_state.get_menu_action())

    def test_paused_menu_execute_high_scores(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.move_down_n(2, menu)

        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.SHOW_HIGH_SCORES, next_state.get_menu_action())

    def test_paused_menu_execute_options(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.move_down_n(3, menu)

        next_state = menu.execute_current_option()
        self.assertIsInstance(next_state.active_menu_screen, OptionsMenuContext)

    def test_paused_menu_execute_quit(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.move_down_n(4, menu)

        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.active_menu_screen)
        self.assertEqual(MenuAction.QUIT, next_state.get_menu_action())

    def test_pausedmenu_not_listening_for_key(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        self.assertFalse(menu.is_listening_for_key())

    def test_pausedmenu_render_info(self):
        menu = self.context_factory.build_top_level_menu_screen(True)
        render_info = menu.get_render_info()
        self.assertIsInstance(render_info.get_text_renderer(), StandardTextRenderer)

    def test_musicmenu_labels(self):
        songlist = ["Song 1", "Song 2", "Song 3"]
        self.jukebox.get_available_song_titles.return_value = songlist
        menu = self.context_factory.build_music_selection_screen()
        self.assertEqual(songlist, menu.get_render_info().get_labels())

    def test_musicmenu_no_songs(self):
        self.jukebox.get_available_song_titles.return_value = []
        menu = self.context_factory.build_music_selection_screen()
        self.assertEqual([], menu.get_render_info().get_labels())

        self.assertEqual(0, menu.get_selected_index())
        menu.move_to_next_option()
        self.assertEqual(0, menu.get_selected_index())

    def test_musicmenu_execute_song_selection(self):
        songlist = ["Song 1", "Song 2", "Song 3"]
        self.jukebox.get_available_song_titles.return_value = songlist
        menu = self.context_factory.build_music_selection_screen()

        next_state = menu.execute_current_option()
        self.assertEqual(menu, next_state.get_active_menu_screen())
        self.assertEqual(MenuAction.MENU, next_state.get_menu_action())
        self.jukebox.set_song.assert_called_once_with("Song 1")

    def test_musicmenu_not_listening_for_key(self):
        self.jukebox.get_available_song_titles.return_value = ['Song 1']
        menu = self.context_factory.build_music_selection_screen()
        self.assertFalse(menu.is_listening_for_key())

    def test_musicmenu_render_info(self):
        self.jukebox.get_available_song_titles.return_value = []
        menu = self.context_factory.build_music_selection_screen()
        self.assertIsInstance(menu.get_render_info().get_text_renderer(), StandardTextRenderer)

    def test_keymenu_default_labels(self):
        menu = self.context_factory.build_key_changing_screen()
        actual_labels = menu.get_labels()
        expected_labels = self.default_key_labels()
        self.assertEqual(expected_labels, actual_labels)

    def test_keymenu_not_listening_for_key_by_default(self):
        menu = self.context_factory.build_key_changing_screen()
        self.assertFalse(menu.is_listening_for_key())

    def test_keymenu_listening_for_key_after_executing_option(self):
        menu = self.context_factory.build_key_changing_screen()
        menu.execute_current_option()
        self.assertTrue(menu.is_listening_for_key())

    def test_keymenu_update_left_key(self):
        self._run_key_update_test(0, 'J', 'Move Left: <J>')

    def test_keymenu_update_right_key(self):
        self._run_key_update_test(1, 'L', 'Move Right: <L>')

    def test_keymenu_update_down_key(self):
        self._run_key_update_test(2, 'K', 'Move Down: <K>')

    def test_keymenu_update_drop_key(self):
        self._run_key_update_test(3, 'Up', 'Drop Piece: <Up>')

    def test_keymenu_update_rot_left_key(self):
        self._run_key_update_test(4, 'One', 'Rotate Left: <One>')

    def test_keymenu_update_rot_right_key(self):
        self._run_key_update_test(5, 'Two', 'Rotate Right: <Two>')

    def _run_key_update_test(self, label_index, new_key_name, expected_label):
        menu = self.context_factory.build_key_changing_screen()
        self.move_down_n(label_index, menu)
        menu.execute_current_option()
        menu.handle_key_event(self.game_keys.by_name(new_key_name))
        expected_labels = self.default_key_labels()
        expected_labels[label_index] = expected_label
        self.assertEqual(expected_labels, menu.get_labels())

    def test_keymenu_updated_labels_are_cached(self):
        menu = self.context_factory.build_key_changing_screen()
        self.assertIs(menu.get_labels(), menu.get_labels(), 'Original labels should have been cached')

        menu.execute_current_option()
        menu.handle_key_event(self.game_keys.by_name('A'))

        self.assertIs(menu.get_labels(), menu.get_labels(), 'New labels should have been cached')

    def test_keymenu_render_info(self):
        menu = self.context_factory.build_key_changing_screen()
        self.assertEqual(self.default_key_labels(), menu.get_render_info().get_labels())
        self.assertIsInstance(menu.get_render_info().get_text_renderer(), LazyTextRenderer)

    def test_optionsmenu_default_labels(self):
        menu = self.context_factory.build_options_screen()
        self.assertEqual(self.default_options_labels(), menu.get_labels())

    def test_optionsmenu_sound_off_label(self):
        menu = self.context_factory.build_options_screen()
        menu.execute_current_option()
        expected = self.default_options_labels()
        expected[0] = "Sound On / [Off]"
        self.assertEqual(expected, menu.get_labels())

    def test_optionsmenu_music_off_label(self):
        menu = self.context_factory.build_options_screen()
        self.move_down_n(1, menu)
        menu.execute_current_option()
        expected = self.default_options_labels()
        expected[1] = "Music On / [Off]"
        self.assertEqual(expected, menu.get_labels())

    def test_optionsmenu_toggle_sound_twice(self):
        menu = self.context_factory.build_options_screen()
        menu.execute_current_option()
        menu.execute_current_option()
        self.assertEqual(self.default_options_labels(), menu.get_labels())

    def test_optionsmenu_toggle_music_twice(self):
        menu = self.context_factory.build_options_screen()
        self.move_down_n(1, menu)
        menu.execute_current_option()
        menu.execute_current_option()
        self.assertEqual(self.default_options_labels(), menu.get_labels())

    def test_optionsmenu_sound_toggle_returns_menu_state(self):
        menu = self.context_factory.build_options_screen()
        next_state = menu.execute_current_option()
        self.assertEqual(MenuAction.MENU, next_state.get_menu_action())
        self.assertEqual(menu, next_state.get_active_menu_screen())

    def test_optionsmenu_sound_toggle_affects_jukebox(self):
        menu = self.context_factory.build_options_screen()
        menu.execute_current_option()
        self.jukebox.enable_sound.assert_called_once_with(False)
        self.jukebox.reset_mock()
        menu.execute_current_option()
        self.jukebox.enable_sound.assert_called_once_with(True)

    def test_optionsmenu_music_toggle_returns_menu_state(self):
        menu = self.context_factory.build_options_screen()
        self.move_down_n(1, menu)
        next_state = menu.execute_current_option()
        self.assertEqual(MenuAction.MENU, next_state.get_menu_action())
        self.assertEqual(menu, next_state.get_active_menu_screen())

    def test_optionsmenu_music_toggle_affects_jukebox(self):
        menu = self.context_factory.build_options_screen()
        self.move_down_n(1, menu)
        menu.execute_current_option()
        self.jukebox.enable_music.assert_called_once_with(False)
        self.jukebox.reset_mock()
        menu.execute_current_option()
        self.jukebox.enable_music.assert_called_once_with(True)

    def test_optionsmenu_navigate_to_music_selection(self):
        self.jukebox.get_available_song_titles.return_value = ["Song 1"]
        menu = self.context_factory.build_options_screen()
        self.move_down_n(2, menu)
        next_state = menu.execute_current_option()
        self.assertEqual(MenuAction.MENU, next_state.get_menu_action())

        returned_submenu = next_state.get_active_menu_screen()
        self.assertIsInstance(returned_submenu, MusicSelectionMenuContext)
        self.assertEqual(["Song 1"], returned_submenu.get_render_info().get_labels(),
                         "Options menu should have passed the correct songs to the submenu")

    def test_optionsmenu_navigate_to_key_menu(self):
        menu = self.context_factory.build_options_screen()
        self.move_down_n(3, menu)
        next_state = menu.execute_current_option()
        self.assertEqual(MenuAction.MENU, next_state.get_menu_action())

        returned_submenu = next_state.get_active_menu_screen()
        self.assertIsInstance(returned_submenu, KeySettingMenuContext)

    @staticmethod
    def move_down_n(n, menu):
        """ A helper for setting the menu selection index """
        for _ in range(n):
            menu.move_to_next_option()

    @staticmethod
    def default_key_labels():
        return [
            'Move Left: <Left>',
            'Move Right: <Right>',
            'Move Down: <Down>',
            'Drop Piece: <Space>',
            'Rotate Left: <Z>',
            'Rotate Right: <X>'
        ]

    @staticmethod
    def default_options_labels():
        return [
            "Sound [On] / Off",
            "Music [On] / Off",
            "Change Song",
            "Change Keys"]

    @staticmethod
    def _get_test_font_file():
        current_path = Path(os.path.dirname(os.path.realpath(__file__)))
        return str(current_path / "resources" / "BPmono.ttf")
