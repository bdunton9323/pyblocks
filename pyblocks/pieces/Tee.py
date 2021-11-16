from pyblocks.pieces.Piece import Piece

class Tee(Piece):
  
  def __init__(self, geometry):
    super(Tee, self).__init__(geometry)
    
  fill_arrays = [
    # pointing up
    [[0,1,0],[1,1,1]],
    # pointing right
    [[1,0],[1,1],[1,0]],
    # pointing down
    [[1,1,1],[0,1,0]],
    # pointing left
    [[0,1],[1,1],[0,1]]
  ]
  
  # The first index is the old fill_array for the piece
  # The second index is the fill_array after rotation
  # The value at that index is the offset to apply to the piece's origin
  # for the new orientation of the piece.
  rotation_table = [
    # currently pointing up
    [None,(1,0),None,(0,0)],
    # currently pointing right
    [(-1,0),None,(-1,1),None],
    # currently pointing down
    [None,(1,-1),None,(0,-1)],
    # currently pointing left
    [(0,0),None,(0,1),None]
  ]
  
  def get_fill_arrays(self):
    return self.fill_arrays
     
  def get_color(self):
    return 'blue'
    
  def get_x_y_rota_delta(self, oldindex, newindex):
    return self.rotation_table[oldindex][newindex]
