import unittest

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from BackingGrid import BackingGrid
from Geometry import Geometry
from Bar import Bar
from Box import Box
from Tee import Tee

# TODO: the code would be more testable if I could mock the Piece class and create pieces of arbitrary size
class TestBackingGrid(unittest.TestCase):
  
  WIDTH = 10
  HEIGHT = 10

  def setUp(self):
    self.grid = BackingGrid(TestBackingGrid.WIDTH, TestBackingGrid.HEIGHT)
    self.geo = Geometry(20, 20, (0,0,100,100))

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
    self.assertFalse(self.grid.is_collision(2,2, tee.get_fill_mask()))

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
  def test_edge_of_piece_out_of_bounds(self):
    box = Box(self.geo)
    box.setX(9) # this spot is in bounds, but the width of the shape pushes it out
    box.setY(0)
    self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

  def test_x_out_of_bounds(self):
    box = Box(self.geo)
    box.setX(10)
    box.setY(0)
    self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

  def test_y_out_of_bounds(self):
    box = Box(self.geo)
    box.setX(0)
    box.setY(10)
    self.assertRaisesRegex(Exception, '^.*out of bounds*$', lambda: self.grid.add(box))

  def test_new_piece_completes_bottom_row(self):
      bar1 = Bar(self.geo)
      bar1.setX(0)
      bar1.setY(9)

      bar2 = Bar(self.geo)
      bar2.setX(bar1.get_width())
      bar2.setY(9)

      box = Box(self.geo)
      box.setX(bar1.get_width() + bar2.get_width())
      box.setY(8)

      self.grid.add(bar1)
      self.grid.add(bar2)
      self.assertEqual(0, self.grid.clear_filled_rows())
      self.grid.add(box)
      self.assertEqual(1, self.grid.clear_filled_rows())

      self.fail("TOD: verify that everything else is shifted down")

  def test_new_piece_completes_top_row(self):
    bar1 = Bar(self.geo)
    bar1.setX(0)
    bar1.setY(0)

    bar2 = Bar(self.geo)
    bar2.setX(bar1.get_width())
    bar2.setY(0)

    box = Box(self.geo)
    box.setX(bar1.get_width() + bar2.get_width())
    box.setY(0)

    self.grid.add(bar1)
    self.grid.add(bar2)
    # a precondition of the test is that no row is filled yet
    self.assertEqual(0, self.grid.clear_filled_rows())
    self.grid.add(box)
    self.assertEqual(1, self.grid.clear_filled_rows())

    self.fail("TOD: verify that everything above is shifted down, and nothing below is shifted")

  def test_new_piece_completes_nonbottom_row(self):
      # set up 2 horizontal bars that can be completed with a box
      bar = Bar(self.geo)
      bar.setX(0)
      bar.setY(7)
      bar2 = Bar(self.geo)
      bar2.setX(bar.get_width())
      bar2.setY(7)

      # this is on the bottom, beneath the two horizontal bars
      box = Box(self.geo)
      box.setX(5)
      box.setY(8)

      # this completes row 7
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

      self.fail("TOD: verify that everything else is shifted down")

  # a piece causes two noncontiguous rows to be full
  def test_piece_completes_noncontiguous_rows(self):
      bottom_left_bar = Bar(self.geo)
      bottom_left_bar.setX(0)
      bottom_left_bar.setY(9)

      bottom_right_bar = Bar(self.geo)
      bottom_right_bar.setX(bottom_left_bar.get_width())
      bottom_right_bar.setY(9)

      top_left_bar = Bar(self.geo)
      top_left_bar.setX(0)
      top_left_bar.setY(7)

      top_right_bar = Bar(self.geo)
      top_right_bar.setX(top_left_bar.get_width())
      top_right_bar.setY(7)

      vertical_bar = Bar(self.geo)
      vertical_bar.rotate(1)
      vertical_bar.setX(8)
      vertical_bar.setY(6)

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

      self.fail("TOD: verify that everything else is shifted down")

  def test_piece_completes_adjacent_rows(self):
      self.fail("TODO: implement me")

    
if __name__ == '__main__':
  unittest.main()
