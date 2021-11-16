from pyblocks.pieces.Piece import Piece

class Bar(Piece):
  
  def __init__(self, geometry):
    super(Bar, self).__init__(geometry)
  
  fill_arrays = [
    # horizontal orientation
    [[1,1,1,1]],
    # vertical orientation
    [[1],[1],[1],[1]]
  ]
  
  # This table provides offsets that can be applied to the piece's
  # coordinates, which change during rotation. rotation_table[i][j]
  # refers to the piece at orientation i rotating to orientation j,
  # where i and j are indices into 'fill_arrays'. The value at that
  # index is a tuple (x',y') that can be added to the piece's
  # coordinate (x,y), giving a new location of (x+x',y+y').
  rotation_table = [
    # starting out horizontal
    # rotate left, rotate right
    [(1,-1),(1,-1)],
    # starting out vertical
    # rotate left, rotate right
    [(-1,1),(-1,1)]
  ]
  
  def get_fill_arrays(self):
    return self.fill_arrays
  
  def get_color(self):
    return 'yellow'

  def get_x_y_rota_delta(self, oldindex, newindex):
    return self.rotation_table[oldindex][newindex]
    