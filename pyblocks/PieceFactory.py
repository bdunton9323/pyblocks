import random
from . Tee import Tee
from . Ess import Ess
from . Zee import Zee
from . Bar import Bar
from . Box import Box
from . Jay import Jay
from . Ell import Ell

class PieceFactory(object):
  # The number of different pieces possible
  NUM_PIECE_TYPES = 7
    
  # param: geometry - defines the geometry of the board (size, layout, etc)
  def __init__(self, geometry):
    self.geometry = geometry
  
  def make_piece(self, which_piece):
    if which_piece == 0:
      return Tee(self.geometry)
    elif which_piece == 1:
      return Ess(self.geometry)
    elif which_piece == 2:
      return Bar(self.geometry)
    elif which_piece == 3:
      return Zee(self.geometry)
    elif which_piece == 4:
      return Box(self.geometry)
    elif which_piece == 5:
      return Jay(self.geometry)
    elif which_piece == 6:
      return Ell(self.geometry)
    else:
      print("Error: piece type out of range")
      raise ValueError("Piece type out of range. Was " + which_piece)

  def random_piece(self):
    # TODO: this doesn't seem very random. The python docs even 
    # say randrange isn't distributed properly because of floating
    # point conversion.
    type = random.randrange(0, PieceFactory.NUM_PIECE_TYPES)
    return self.make_piece(type)
    
