import unittest
import math
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from particles import Vector2D

class TestVector(unittest.TestCase):

  def testPositiveMagnitude(self):
    v = Vector2D(3*math.pi/2, 9.8)
    self.assert_vector(v, 0, -9.8, 9.8, 3*math.pi/2)

    v = Vector2D(math.pi/4, 15)
    self.assert_vector(v, 10.606601717798213, 10.606601717798213, 15, math.pi/4)
    
  def testNegativeMagnitude(self):
    v = Vector2D(math.pi/2, -9.8)
    self.assertAlmostEqual(math.pi/2, v.get_angle())
    self.assertAlmostEqual(0, v.get_i())
    self.assertAlmostEqual(-9.8, v.get_j())
    self.assertAlmostEqual(-9.8, v.get_magnitude())
    
  def testQuadrant2(self):
    v = Vector2D(2*math.pi/3, 10)
    self.assert_vector(v, -5, 8.660254038, 10, 2*math.pi/3)
    
  def testQuadrant3(self):
    v = Vector2D(4*math.pi/3, 10)
    self.assert_vector(v, -5, -8.660254038, 10, 4*math.pi/3)
    
  def testStraightDown(self):
    v = Vector2D(3*math.pi/2, 9.8)
    self.assert_vector(v, 0, -9.8, 9.8, 3*math.pi/2)
    
  def testAdd(self):
    v = Vector2D(math.pi/3, 16)
    v2 = Vector2D(3*math.pi/2, 10)
    v.add(v2)
    self.assert_vector(v, 8, 3.85640646055, 8.880983661, .449185422)
   
  def testAddStraightUpStraightDown(self):
    v = Vector2D(math.pi/2, 16)
    # I would try one that completely cancels out, but the rounding error
    # on the near-0 angle causes it to bounce to n*pi/2
    v2 = Vector2D(3*math.pi/2, 15)
    v.add(v2)
    self.assert_vector(v, 0, 1, 1, math.pi/2)

  def testAdd3(self):
    v = Vector2D(3*math.pi/2, 9.8)
    v2 = Vector2D(4*math.pi/3, 10)
    v.add(v2)
    self.assert_vector(v, -5, -18.460254038, 19.125401411258014, -1.835302265484458)

    
  def assert_vector(self, vector, expected_x, expected_y, expected_magnitude, expected_angle):
    self.assertAlmostEqual(expected_x, vector.get_i())
    self.assertAlmostEqual(expected_y, vector.get_j())
    self.assertAlmostEqual(expected_magnitude, vector.get_magnitude())
    self.assertAlmostEqual(expected_angle, vector.get_angle())
    
if __name__ == '__main__':
  unittest.main()