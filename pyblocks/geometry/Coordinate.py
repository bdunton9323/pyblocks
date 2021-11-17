class Coordinate:
  # The coordinate represents the location of a square in the grid, with the
  # origin being the top left of the screen.
  GRID = 1
  
  # The coordinate is an absolute pixel location, with the origin being the
  # top left of the screen.
  PIXEL = 2
  
  # The coordinate specifies the location of a square in the grid, with the
  # origin being the top left of the playing area (area where pieces can move)
  PLAYING_FIELD = 3
  
  def __init__(self, x, y, geometry, type):
    self.geometry = geometry
    if type == Coordinate.PIXEL:
      self.x = x
      self.y = y
    elif type == Coordinate.GRID:
      self.x = x * geometry.get_block_width()
      self.y = y * geometry.get_block_height()
    elif type == Coordinate.PLAYING_FIELD:
      # they gave us a position relative to the playing field.
      # convert it to an absolute position
      self.x = x * geometry.get_block_width() + geometry.get_left_boundary_px()
      self.y = y * geometry.get_block_width() + geometry.get_upper_boundary_px()
    
  # if type is PLAYING_FIELD, the return is in grid coordinates relative to the playing field boundary
  def getX(self, type):
    if type == Coordinate.PIXEL:
      return self.x
    elif type == Coordinate.GRID:
      return self.x // self.geometry.get_block_width()
    elif type == Coordinate.PLAYING_FIELD:
      grid_x = self.x // self.geometry.get_block_width()
      grid_x_field = self.geometry.get_left_boundary_px() // self.geometry.get_block_width()
      return grid_x - grid_x_field
    
  def getY(self, type):
    if type == Coordinate.PIXEL:
      return self.y
    elif type == Coordinate.GRID:
      return self.y // self.geometry.get_block_height()
    elif type == Coordinate.PLAYING_FIELD:
      grid_y = self.y // self.geometry.get_block_height()
      grid_y_field = self.geometry.get_upper_boundary_px() // self.geometry.get_block_height()
      return grid_y - grid_y_field
      
  def setX(self, new_x, type):
    if type == Coordinate.PIXEL:
      self.x = new_x
    elif type == Coordinate.GRID:
      self.x = new_x * self.geometry.get_block_width()
    elif type == Coordinate.PLAYING_FIELD:
      new_x_pixels = new_x * self.geometry.get_block_width()
      self.x = new_x_pixels + self.geometry.get_left_boundary_px()
    
  def setY(self, new_y, type):
    if type == Coordinate.PIXEL:
      self.y = new_y
    elif type == Coordinate.GRID:
      self.y = new_y * self.geometry.get_block_height()
    elif type == Coordinate.PLAYING_FIELD:
      new_y_pixels = new_y * self.geometry.get_block_width()
      self.y = new_y_pixels + self.geometry.get_upper_boundary_px()