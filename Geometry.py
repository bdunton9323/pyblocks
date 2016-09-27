class Geometry(object):

  # param: block_width - the width of one square of the playing grid
  # param: block_height - the height of one square of the playing grid
  # param: playable_field - a tuple (x,y,x2,y2) defining the upper left
  #        and lower right corners of the rectangular playing area
  def __init__(self, block_width, block_height, playable_field):
    self.block_width = block_width
    self.block_height = block_height
    self.playing_field = playable_field
    
  def get_block_width(self):
    return self.block_width
    
  def get_block_height(self):
    return self.block_height
    
  def get_play_area_width(self):
    return self.get_right_boundary_grid() - self.get_left_boundary_grid()
    
  def get_play_area_height(self):
    return self.get_lower_boundary_grid() - self.get_upper_boundary_grid()

    
  def get_left_boundary_px(self):
    return self.playing_field[0]

  def get_left_boundary_grid(self):
    return self.get_left_boundary_px() / self.block_width
  
  def get_left_boundary_playing_field(self):
    return 0
  
  
  def get_right_boundary_px(self):
    return self.playing_field[2]
    
  def get_right_boundary_playing_field(self):
    # TODO: store the width and height in the constructor instead of calculating each time
    width_px = self.get_right_boundary_px() - self.get_left_boundary_px()
    return width_px / self.block_width
  
  def get_right_boundary_grid(self):
    return self.get_right_boundary_px() / self.block_width
  
    
  def get_upper_boundary_px(self):
    return self.playing_field[1]
  
  def get_upper_boundary_grid(self):
    return self.get_upper_boundary_px() / self.block_width
  
  def get_upper_boundary_playing_field(self):
    return 0
  
  
  def get_lower_boundary_px(self):
    return self.playing_field[3]
       
  def get_lower_boundary_grid(self):
    return self.get_lower_boundary_px() / self.block_width
    
  def get_lower_boundary_playing_field(self):
    height_px = self.get_lower_boundary_px() - self.get_upper_boundary_px()
    return height_px / self.block_width