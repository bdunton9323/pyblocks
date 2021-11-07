import unittest

import sys, os

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from BackingGrid import BackingGrid
from Geometry import Geometry
from Bar import Bar
from Box import Box
from Tee import Tee


# the code would be more testable if I could mock the Piece class and create pieces of arbitrary size,
# but this works well enough.
class TestBackingGrid(unittest.TestCase):
    WIDTH = 10
    HEIGHT = 10
    # a Piece bitmap for a single 1x1 block
    SINGLE_BLOCK = [[1]]

    def setUp(self):
        self.grid = BackingGrid(TestBackingGrid.WIDTH, TestBackingGrid.HEIGHT)
        self.geo = Geometry(20, 20, (0, 0, 100, 100))

    def test_ieterate_over_nonempty_grid(self):
        box = Box(self.geo)
        box.setX(0)
        box.setY(0)
        self.grid.add(box)

        actual_list = list(self.grid)
        self.assertEqual(100, len(actual_list))

        # verify the spaces that are filled by a block
        self.assertEqual((True, 0, 0, 'green'), actual_list[0])
        self.assertEqual((True, 1, 0, 'green'), actual_list[1])
        self.assertEqual((True, 0, 1, 'green'), actual_list[10])
        self.assertEqual((True, 1, 1, 'green'), actual_list[11])

        # verify everything else in bulk
        filled_spaces = [0, 1, 10, 11]
        for i in range(0, len(actual_list)):
            if i not in filled_spaces:
                self.assertEqual((False, None, None, None), actual_list[i])

    def test_iterate_over_empty_grid(self):
        actual_list = list(self.grid)
        for i in range(0, 99):
            self.assertEqual((False, None, None, None), actual_list[i])

    def test_box_collision(self):
        box = Box(self.geo)
        box.setX(0)
        box.setY(0)
        self.grid.add(box)

        self.assertTrue(self.grid.is_collision(1, 1, box.get_fill_mask()))
        self.assertTrue(self.grid.is_collision(0, 0, box.get_fill_mask()))
        self.assertTrue(self.grid.is_collision(1, 0, box.get_fill_mask()))
        self.assertTrue(self.grid.is_collision(0, 1, box.get_fill_mask()))
        self.assertFalse(self.grid.is_collision(2, 0, box.get_fill_mask()))

    def test_tee_collision(self):
        tee = Tee(self.geo)
        self.grid.add(tee)
        self.assertTrue(self.grid.is_collision(1, 1, tee.get_fill_mask()))
        self.assertTrue(self.grid.is_collision(0, 1, tee.get_fill_mask()))
        self.assertFalse(self.grid.is_collision(2, 2, tee.get_fill_mask()))

    def test_add_overlapping(self):
        box1 = Box(self.geo)
        box1.setX(0)
        box1.setY(0)

        box2 = Box(self.geo)
        box2.setX(1)
        box2.setY(1)

        self.grid.add(box1)
        self.assertRaisesRegex(Exception, '^.*already occupied.*$', lambda: self.grid.add(box2))

    def test_add_adjacent(self):
        box1 = Box(self.geo)
        box1.setX(0)
        box1.setY(0)

        box2 = Box(self.geo)
        box2.setX(2)
        box2.setY(1)
        self.grid.add(box1)
        # we're just testing that this doesn't raise
        self.grid.add(box2)

    # add a piece that goes off screen
    def test_piece_partially_out_of_bounds_right(self):
        box = Box(self.geo)
        box.setX(9)  # this spot is in bounds, but the width of the shape pushes it out
        box.setY(0)
        self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

    # add a piece that goes off screen
    def test_piece_partially_out_of_bounds_bottom(self):
        box = Box(self.geo)
        box.setX(0)
        box.setY(9)  # this spot is in bounds, but the height of the shape pushes it out
        self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

    def test_piece_partially_out_of_bounds_left(self):
        box = Box(self.geo)
        box.setX(-1)
        box.setY(0)
        self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

    def test_piece_partially_out_of_bounds_top(self):
        box = Box(self.geo)
        box.setX(0)
        box.setY(-1)
        self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

    def test_piece_fully_out_of_bounds_right(self):
        box = Box(self.geo)
        box.setX(10)
        box.setY(0)
        self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

    def test_new_piece_completes_bottom_row(self):
        # Before row cleared:
        # y=8: ........33
        # y=9: 1111222233

        # After row cleared:
        # y=8: ...........
        # y=9: .........33

        # piece 1
        bar1 = Bar(self.geo)
        bar1.setX(0)
        bar1.setY(9)

        # piece 2
        bar2 = Bar(self.geo)
        bar2.setX(bar1.get_width())
        bar2.setY(9)

        # piece 3
        box = Box(self.geo)
        box.setX(bar1.get_width() + bar2.get_width())
        box.setY(8)

        self.grid.add(bar1)
        self.grid.add(bar2)
        self.assertEqual(0, self.grid.clear_filled_rows())
        self.grid.add(box)
        self.assertEqual(1, self.grid.clear_filled_rows())

        # this is the row that cleared
        self.assert_row_empty(8)
        # the top row of the box should have moved down one row
        self.assert_row_state(9, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

    def test_new_piece_completes_top_row(self):
        # Before row cleared:
        # y=0: 1111222233
        # y=1: ........33
        # y=2: ..........

        # After row cleared:
        # y=0: ..........
        # y=1: ........33
        # y=2: ..........

        # piece 1
        bar1 = Bar(self.geo)
        bar1.setX(0)
        bar1.setY(0)

        # piece 2
        bar2 = Bar(self.geo)
        bar2.setX(bar1.get_width())
        bar2.setY(0)

        # piece 3
        box = Box(self.geo)
        box.setX(bar1.get_width() + bar2.get_width())
        box.setY(0)

        self.grid.add(bar1)
        self.grid.add(bar2)
        # a precondition of the test is that no row is filled yet
        self.assertEqual(0, self.grid.clear_filled_rows())
        self.grid.add(box)
        self.assertEqual(1, self.grid.clear_filled_rows())

        # since nothing is above the completed row, the bottom half of the box should be intact
        self.assert_row_empty(0)
        self.assert_row_state(1, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

    def test_new_piece_completes_nonbottom_row(self):
        # Before row cleared:
        # y=7: 11112222xx
        # y=8: .....33.xx
        # y=9: .....33...

        # After row cleared:
        # y=7: ..........
        # y=8: .....33.xx
        # y=9: .....33...

        # pieces 1 and 2 in the above diagram
        bar = Bar(self.geo)
        bar.setX(0)
        bar.setY(7)
        bar2 = Bar(self.geo)
        bar2.setX(bar.get_width())
        bar2.setY(7)

        # piece 3 in the above diagram
        box = Box(self.geo)
        box.setX(5)
        box.setY(8)

        # piece "x" above. This completes row 7.
        box2 = Box(self.geo)
        box2.setX(bar.get_width() + bar2.get_width())
        box2.setY(7)

        self.grid.add(bar)
        self.grid.add(bar2)
        self.grid.add(box)
        # precondition of test: should not have completed a row yet
        self.assertEqual(0, self.grid.clear_filled_rows())
        self.grid.add(box2)
        self.assertEqual(1, self.grid.clear_filled_rows())

        # validate that nothing below the completed row changed
        self.assert_row_empty(7)
        self.assert_row_state(8, [0, 0, 0, 0, 0, 1, 1, 0, 1, 1])
        self.assert_row_state(9, [0, 0, 0, 0, 0, 1, 1, 0, 0, 0])

    # a piece causes two noncontiguous rows to be full
    def test_piece_completes_noncontiguous_rows(self):
        # Before rows cleared:
        # y=6: ........56
        # y=7: 3333444456
        # y=8: ........56
        # y=9: 1111222256

        # After rows cleared:
        # y=6: ..........
        # y=7: ..........
        # y=8: ........56
        # y=9: ........56

        # piece 1
        bottom_left_bar = Bar(self.geo)
        bottom_left_bar.setX(0)
        bottom_left_bar.setY(9)

        # piece 2
        bottom_right_bar = Bar(self.geo)
        bottom_right_bar.setX(bottom_left_bar.get_width())
        bottom_right_bar.setY(9)

        # piece 3
        top_left_bar = Bar(self.geo)
        top_left_bar.setX(0)
        top_left_bar.setY(7)

        # piece 4
        top_right_bar = Bar(self.geo)
        top_right_bar.setX(top_left_bar.get_width())
        top_right_bar.setY(7)

        # piece 5
        vertical_bar = Bar(self.geo)
        vertical_bar.rotate(1)
        vertical_bar.setX(8)
        vertical_bar.setY(6)

        # piece 6
        vertical_bar2 = Bar(self.geo)
        vertical_bar2.rotate(1)
        vertical_bar2.setX(9)
        vertical_bar2.setY(6)

        self.grid.add(bottom_left_bar)
        self.grid.add(bottom_right_bar)
        self.grid.add(top_left_bar)
        self.grid.add(top_right_bar)
        self.grid.add(vertical_bar)
        self.assertEqual(0, self.grid.clear_filled_rows())
        self.grid.add(vertical_bar2)
        self.assertEqual(2, self.grid.clear_filled_rows())

        self.assert_row_empty(6)
        self.assert_row_empty(7)
        self.assert_row_state(8, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
        self.assert_row_state(9, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

    # helper for checking what is in a single cell
    def assert_space_empty(self, x, y):
        self.assertFalse(self.grid.is_collision(x, y, self.SINGLE_BLOCK),
                         f"Space ({x},{y}) was not empty but should have been")

    # helper for checking what is in a single cell
    def assert_space_filled(self, x, y):
        self.assertTrue(self.grid.is_collision(x, y, self.SINGLE_BLOCK))

    def assert_row_empty(self, row):
        for x in range(self.WIDTH):
            self.assert_space_empty(x, row)

    def assert_row_state(self, rownum, expected_state):
        for i in range(len(expected_state)):
            cell = expected_state[i]
            if cell == 1:
                self.assert_space_filled(i, rownum)
            elif cell == 0:
                self.assert_space_empty(i, rownum)
            else:
                self.fail(f"Unexpected test input: {cell}")


if __name__ == '__main__':
    unittest.main()