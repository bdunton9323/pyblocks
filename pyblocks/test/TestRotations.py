import unittest
from pyblocks.pieces.Piece import Piece
from pyblocks.pieces.Bar import Bar
from pyblocks.pieces.Tee import Tee
from geometry.Geometry import Geometry

class TestRotations(unittest.TestCase):
  
  def setUp(self):
    self.geo = Geometry(20, 20, (0,0,100,100))
  
  def test_bar(self):
    bar = Bar(self.geo)
    
    rot1 = [[1,1,1,1]]
    rot2 = [[1],[1],[1],[1]]
    self.assertEqual(rot1, bar.get_fill_mask())
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_CURR))
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_R))
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_L))
    
    origin_offset = bar.rotate(Piece.ROTATION_R)
    self.assertEqual((1,-1), origin_offset)
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_CURR))
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_R))
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_L))
    
    origin_offset = bar.rotate(Piece.ROTATION_R)
    self.assertEqual((-1,1), origin_offset)
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_CURR))
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_R))
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_L))
    
    origin_offset = bar.rotate(Piece.ROTATION_L)
    self.assertEqual((1,-1), origin_offset)
    self.assertEqual(rot2, bar.get_fill_mask(Piece.ROTATION_CURR))
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_R))
    self.assertEqual(rot1, bar.get_fill_mask(Piece.ROTATION_L))

  def test_tee(self):
    tee = Tee(self.geo)
    rot1 = tee.get_fill_arrays()[0] #up
    rot2 = tee.get_fill_arrays()[1] #right
    rot3 = tee.get_fill_arrays()[2] #down
    rot4 = tee.get_fill_arrays()[3] #left
    self.assertEqual(rot1, tee.get_fill_mask())
    self.assertEqual(rot1, tee.get_fill_mask(Piece.ROTATION_CURR))
    self.assertEqual(rot2, tee.get_fill_mask(Piece.ROTATION_R))
    self.assertEqual(rot4, tee.get_fill_mask(Piece.ROTATION_L))
    
    # TODO: fill me in
    
  if __name__ == '__main__':
    unittest.main()
