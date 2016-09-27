import unittest
import math
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from particles import *

class TestParticleEngine(unittest.TestCase):
  PIXELS_PER_METER = 1
  
  def setUp(self):
    self.screen = DummyScreen(200, 100)
    self.zero_g = Vector2D(0,0)
  
  # Constant velocity along the axis
  def test_constant_v_one_axis(self):
    velocity = Vector2D(0, 5)
    p = Particle((0,0), velocity, 5000, None)
    self.assertTrue(p.alive)
    exp = Explosion([p], self.screen, self.zero_g, TestParticleEngine.PIXELS_PER_METER)
    exp.update(1000)
    self.assertTrue(p.alive)
    self.assertEqual(p.x, 5)
    self.assertEqual(p.y, 0)
    exp.update(4000)
    self.assertTrue(p.alive)
    self.assertEqual(p.x, 25)
    self.assertEqual(p.y, 0)
    exp.update(1000)
    self.assertFalse(p.alive)
    
  # constant velocity along some non-axial vector
  def test_constant_v_quadrant2(self):
    start_x, start_y = (10,10)
    velocity = Vector2D(3*math.pi/4, 5)
    p = Particle((start_x, start_y), velocity, 5000, None)
    exp = Explosion([p], self.screen, self.zero_g, TestParticleEngine.PIXELS_PER_METER)
    exp.update(1000)
    self.assertEqual(p.x, start_x + 5*math.cos(3*math.pi/4))
    self.assertEqual(p.y, start_y + 5*math.sin(3*math.pi/4))
    # The vector should not change because v is constant
    self.assertEqual(p.vector.get_i(), 5*math.cos(3*math.pi/4))
    self.assertEqual(p.vector.get_j(), 5*math.sin(3*math.pi/4))
    
    start_x = p.x
    start_y = p.y
    exp.update(1000)
    self.assertEqual(p.x, start_x + 5*math.cos(3*math.pi/4))
    self.assertEqual(p.y, start_y + 5*math.sin(3*math.pi/4))
    self.assertEqual(p.vector.get_i(), 5*math.cos(3*math.pi/4))
    self.assertEqual(p.vector.get_j(), 5*math.sin(3*math.pi/4))
    
  def test_gravity_in_y_axis(self):
    start_x, start_y = (100, 100)
    velocity = Vector2D(math.pi/4, 5)
    gravity = Vector2D(3*math.pi/2, 10)
    p = Particle((start_x, start_y), velocity, 5000, None)
    exp = Explosion([p], self.screen, gravity, TestParticleEngine.PIXELS_PER_METER)
    exp.update(1000)
    vy = 5 * math.sin(math.pi/4)
    self.assertAlmostEqual(p.x, start_x + 5*math.cos(math.pi/4))
    dy = vy + .5 * 10 * math.sin(3*math.pi/2)
    self.assertAlmostEqual(p.y, start_y + dy)
    
    # v should increase because it is accelerating
    self.assertAlmostEqual(p.vector.get_j(), 5*math.sin(math.pi/4) + 10*math.sin(3*math.pi/2))
    self.assertAlmostEqual(p.vector.get_i(), 5*math.cos(math.pi/4))
    start_x = p.x
    start_y = p.y
    vy = p.vector.get_j()
    t = 2
    exp.update(t*1000)
    dx = 5 * math.cos(math.pi/4) * t
    dy = vy*t + .5 * 10 * math.sin(3*math.pi/2) * t * t
    self.assertAlmostEqual(p.x, start_x + dx)
    self.assertAlmostEqual(p.y, start_y + dy)
    
  # gravity points somewhere other than down.
  def test_gravity_in_both_axes(self):
    pass
    
    
class DummyScreen(object):
  def __init__(self, x, y):
    blits = []
    self.x = x
    self.y = y
    
  def blit(img, coord):
    blits.append((img, coord))
    
  def get_size(self):
    return (self.x, self.y)
    
    
    
if __name__ == '__main__':
  unittest.main()