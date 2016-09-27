import pygame
from BlockRenderer import BlockRenderer
from Piece import Piece
from Ess import Ess
from Box import Box
from Bar import Bar

def setup():
  pygame.init()
  size = (700, 500)
  screen = pygame.display.set_mode(size)
  return screen

def renderer_test(screen):
  pygame.draw.line(screen,(255,255,255),(10,40),(100,40))
  p = Bar()
  p.setX(0)
  p.setY(1)
  p2 = Box()
  p2.setX(5)
  p2.setY(1)
  r = BlockRenderer(screen)
  r.render(p)
  r.render(p2)
  pygame.display.flip()
  

if __name__ == "__main__":
  screen = setup()
  renderer_test(screen)
  
  while True:
    pass
  pygame.quit()