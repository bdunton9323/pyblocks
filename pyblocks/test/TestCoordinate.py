import unittest
from geometry.Coordinate import Coordinate
from geometry.Geometry import Geometry

class TestCoordinate(unittest.TestCase):

  def setUp(self):
    self.geo = Geometry(20,20,(40,20,100,100))
  
  def test_from_pixel(self):
    coord = Coordinate(0, 0, self.geo, Coordinate.PIXEL)
    self.assertEqual(0, coord.getX(Coordinate.GRID))
    self.assertEqual(0, coord.getY(Coordinate.GRID))
    self.assertEqual(0, coord.getX(Coordinate.PIXEL))
    self.assertEqual(0, coord.getY(Coordinate.PIXEL))
    self.assertTrue(coord.getX(Coordinate.PLAYING_FIELD) < 0)
    self.assertTrue(coord.getY(Coordinate.PLAYING_FIELD) < 0)
    
    coord = Coordinate(40,80, self.geo, Coordinate.PIXEL)
    self.assertEqual(2, coord.getX(Coordinate.GRID))
    self.assertEqual(4, coord.getY(Coordinate.GRID))
    self.assertEqual(40, coord.getX(Coordinate.PIXEL))
    self.assertEqual(80, coord.getY(Coordinate.PIXEL))
    self.assertEqual(0, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(3, coord.getY(Coordinate.PLAYING_FIELD))
    
    # in between grid squares. It should round down
    coord = Coordinate(19, 19, self.geo, Coordinate.PIXEL)
    self.assertEqual(0, coord.getX(Coordinate.GRID))
    self.assertEqual(0, coord.getX(Coordinate.GRID))
    self.assertEqual(19, coord.getX(Coordinate.PIXEL))
    self.assertEqual(19, coord.getY(Coordinate.PIXEL))
    self.assertEqual(-2, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(-1, coord.getY(Coordinate.PLAYING_FIELD))
    
  def test_from_grid(self):
    coord = Coordinate(0, 0, self.geo, Coordinate.GRID)
    self.assertEqual(0, coord.getX(Coordinate.PIXEL))
    self.assertEqual(0, coord.getY(Coordinate.PIXEL))
    self.assertEqual(0, coord.getX(Coordinate.GRID))
    self.assertEqual(0, coord.getY(Coordinate.GRID))
    self.assertEqual(-2, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(-1, coord.getY(Coordinate.PLAYING_FIELD))
    
    coord = Coordinate(3, 2, self.geo, Coordinate.GRID)
    self.assertEqual(60, coord.getX(Coordinate.PIXEL))
    self.assertEqual(40, coord.getY(Coordinate.PIXEL))
    self.assertEqual(3, coord.getX(Coordinate.GRID))
    self.assertEqual(2, coord.getY(Coordinate.GRID))
    self.assertEqual(1, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(1, coord.getY(Coordinate.PLAYING_FIELD))
  
  def test_from_playing_field(self):
    coord = Coordinate(0, 0, self.geo, Coordinate.PLAYING_FIELD)
    self.assertEqual(40, coord.getX(Coordinate.PIXEL))
    self.assertEqual(20, coord.getY(Coordinate.PIXEL))
    self.assertEqual(2, coord.getX(Coordinate.GRID))
    self.assertEqual(1, coord.getY(Coordinate.GRID))
    self.assertEqual(0, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(0, coord.getY(Coordinate.PLAYING_FIELD))
    
    coord = Coordinate(1, 2, self.geo, Coordinate.PLAYING_FIELD)
    self.assertEqual(60, coord.getX(Coordinate.PIXEL))
    self.assertEqual(60, coord.getY(Coordinate.PIXEL))
    self.assertEqual(3, coord.getX(Coordinate.GRID))
    self.assertEqual(3, coord.getY(Coordinate.GRID))
    self.assertEqual(1, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(2, coord.getY(Coordinate.PLAYING_FIELD))
    
  # if the playing field falls between grid squares, the grid coordinate
  # will round down (i.e. be slightly to the left and above the playing field
  def test_play_area_not_aligned_with_block(self):
    self.geo = Geometry(20, 20, (30,10,100,100))
    coord = Coordinate(0, 0, self.geo, Coordinate.PLAYING_FIELD)
    self.assertEqual(30, coord.getX(Coordinate.PIXEL))
    self.assertEqual(10, coord.getY(Coordinate.PIXEL))
    self.assertEqual(1, coord.getX(Coordinate.GRID))
    self.assertEqual(0, coord.getY(Coordinate.GRID))
    self.assertEqual(0, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(0, coord.getY(Coordinate.PLAYING_FIELD))
    
  def test_set_coords(self):
    coord = Coordinate(0, 0, self.geo, Coordinate.PIXEL)
    coord.setX(20, Coordinate.PIXEL)
    self.assertEqual(20, coord.getX(Coordinate.PIXEL))
    self.assertEqual(0, coord.getY(Coordinate.PIXEL))
    coord.setY(30, Coordinate.PIXEL)
    self.assertEqual(20, coord.getX(Coordinate.PIXEL))
    self.assertEqual(30, coord.getY(Coordinate.PIXEL))
    
    coord.setX(1, Coordinate.GRID)
    self.assertEqual(20, coord.getX(Coordinate.PIXEL))
    self.assertEqual(30, coord.getY(Coordinate.PIXEL))
    coord.setY(2, Coordinate.GRID)
    self.assertEqual(20, coord.getX(Coordinate.PIXEL))
    self.assertEqual(40, coord.getY(Coordinate.PIXEL))
    
    coord.setX(1, Coordinate.PLAYING_FIELD)
    self.assertEqual(60, coord.getX(Coordinate.PIXEL))
    self.assertEqual(40, coord.getY(Coordinate.PIXEL))
    coord.setY(1, Coordinate.PLAYING_FIELD)
    self.assertEqual(60, coord.getX(Coordinate.PIXEL))
    self.assertEqual(40, coord.getY(Coordinate.PIXEL))
    
  # make sure Coordinate is calling get_height and get_width correctly
  def test_nonsquare_pieces(self):
    self.geo = Geometry(10, 20, (0,0,100,100))
    coord = Coordinate(1, 2, self.geo, Coordinate.GRID)
    self.assertEqual(10, coord.getX(Coordinate.PIXEL))
    self.assertEqual(40, coord.getY(Coordinate.PIXEL))
    self.assertEqual(1, coord.getX(Coordinate.GRID))
    self.assertEqual(2, coord.getY(Coordinate.GRID))
    self.assertEqual(1, coord.getX(Coordinate.PLAYING_FIELD))
    self.assertEqual(2, coord.getY(Coordinate.PLAYING_FIELD))
    
    
if __name__ == '__main__':
  unittest.main()