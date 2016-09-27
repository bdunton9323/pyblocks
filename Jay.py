from Piece import Piece

class Jay(Piece):
  
  def __init__(self, geometry):
    super(Jay, self).__init__(geometry)

  fill_arrays = [
    [[1,0,0],[1,1,1]],
    [[1,1],[1,0],[1,0]],
    [[1,1,1],[0,0,1]],
    [[0,1],[0,1],[1,1]]
  ]
  
  # There are basically two rotations here: 
  #   vertical to horizontal, and horizontal to vertical.
  rotation_table = [
    # currently pointing up, rotating left or right
    [None, (1,-1), None, (1,-1)], 
    # currently pointing right, rotating up or down
    [(-1,1), None, (-1,1), None],
    # currently pointing down, rotating left or right
    [None, (1,-1), None, (1,-1)],
    # currently pointing left, rotating up or down
    [(-1,1), None, (-1,1), None]
  ]
  
  def get_fill_arrays(self):
    return self.fill_arrays
    
  def get_x_y_rota_delta(self, oldindex, newindex):
    return self.rotation_table[oldindex][newindex]
    
  def get_color(self):
    return 'brown'
