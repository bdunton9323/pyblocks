import unittest

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from BackingGrid import BackingGrid
from Geometry import Geometry
from Box import Box
from Tee import Tee

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
    self.assertEquals(100, len(actual_list))

    # verify the spaces that are filled by a block
    self.assertEquals((True, 0, 0, 'green'), actual_list[0])
    self.assertEquals((True, 1, 0, 'green'), actual_list[1])
    self.assertEquals((True, 0, 1, 'green'), actual_list[10])
    self.assertEquals((True, 1, 1, 'green'), actual_list[11])

    # verify everything else in bulk
    filled_spaces = [0, 1, 10, 11]
    for i in range(0, len(actual_list)):
      if i not in filled_spaces:
        self.assertEquals((False, None, None, None), actual_list[i])

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
  def test_add_out_of_bounds(self):
    pass

  def new_piece_completes_bottom_row(self):
    pass

  def new_piece_completes_nonbottom_row(self):
    pass

  # a piece causes two noncontiguous rows to be full
  def new_piece_completes_noncontiguous_rows(self):
    pass

  def new_piece_completes_top_row(self):
    pass


  def print_grid(self, arr):
    print("\n")
    for row in arr:
      print(row)

    
if __name__ == '__main__':
  unittest.main()
