import unittest

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from InactivePieces import InactivePieces
from Geometry import Geometry
from Box import Box
from Tee import Tee

class TestBackingGrid(unittest.TestCase):
  
  WIDTH = 10
  HEIGHT = 10
  
  def setUp(self):
    self.grid = InactivePieces(TestBackingGrid.WIDTH, TestBackingGrid.HEIGHT)
    self.geo = Geometry(20, 20, (0,0,100,100))
  
  def test_empty(self):
    arr = self.grid.get_grid()
    self.assertTrue(TestBackingGrid.HEIGHT, len(arr))
    for row in arr:
      self.assertEqual(TestBackingGrid.WIDTH, len(row))
    
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
    
  def test_bottom_edge(self):
    arr = self.grid.get_grid()
    arr[9] = [1,1,1,1,1,1,1,1,1,1]
    box = Box(self.geo)
    box.setX(0)
    box.setY(8)
    self.assertTrue(self.grid.is_collision(0,8, box.get_fill_mask()))
    self.assertFalse(self.grid.is_collision(0,1, box.get_fill_mask()))

  def test_add_overlapping(self):
    pass

  # add a piece that goes off screen
  def test_add_out_of_bounds(self):
    pass
  
  def print_grid(self, arr):
    print "\n"
    for row in arr:
      print row

    
if __name__ == '__main__':
  unittest.main()