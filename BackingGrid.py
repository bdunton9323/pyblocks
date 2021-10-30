from Coordinate import Coordinate

# TODO:
# There is a recurring pattern of iterating through the cells in a piece
# and tracking the grid coordinates along the way (see add() and is_collision()). I could write a generator that takes
# a piece and for each iteration gives me a tuple (grid_x, grid_y, filled?)

        
# flatten the grid into a list.
def _grid_as_list(grid):
  l = []
  for row in grid:
    l.extend([cell for cell in row])
  return l

# Chop off num_rows rows from the top of the given Piece bitmap
def _clip_from_top(bitmap, num_rows):
  return bitmap[num_rows:]
 

# Represents all the pieces that will never move again.
# This class flattens the pieces to a 2D array for easily
# checking whether pieces have collided
class BackingGrid(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.grid = []
       
    # The tuple is (filled?, y-grid (row), x-grid (col), color)
    # It might seem redundant to store the x,y in the tuple when the
    # position in self.grid is the same thing. It's so the renderer,
    # who only has access to the tuple, can see the grid-relative location
    self.grid = [[(False,None,None,None) for col in range(width)] for row in range(height)]
  
  def __iter__(self):
    return iter(_grid_as_list(self.grid))
    
  def add(self, piece):
    # for bounds checking, coords are based on playing field
    x = piece.getX(Coordinate.PLAYING_FIELD)
    y = piece.getY(Coordinate.PLAYING_FIELD)
    if x > self.width or x < 0 or y > self.height or y < 0:
      return

    # Get the conversion offset for grid coords to playing field coords
    # Add this to field coords to get grid coords
    x_offset = piece.getX(Coordinate.GRID) - x
    y_offset = piece.getY(Coordinate.GRID) - y
    
    # break apart the piece into individual cells
    mask = piece.get_fill_mask()
    x_field = x
    y_field = y
    for row in mask:
      for cell in row:
        if cell == 1:
          self.grid[y_field][x_field] = (True, 
              x_field + x_offset, y_field + y_offset, piece.get_color())
        x_field += 1
      x_field = x
      y_field += 1

  
  # checks whether a piece (represented by a bitmap) collides
  # with any other pieces in the board.
  # Assumptions: x must be in bounds. If y is negative, only the portion of the
  #   piece in bounds will be considered.
  # x and y are relative to the playing field
  def is_collision(self, x, y, bitmap):
    # If the piece is above the top of the play area (e.g. rotating the Bar piece)
    # only check the rows that are in bounds. Have to do this because the backing
    # grid does not have data for negative rows.
    if y < 0:
      bitmap = _clip_from_top(bitmap, 0-y)
      y = 0
      
    # it is a collision if any filled cell overlaps a filled
    # cell already in the grid
    backing_x = x
    backing_y = y
    for row in bitmap:
      backing_x = x
      for bit in row: 
        if self.grid[backing_y][backing_x][0] == True and bit == 1:
          return True
        backing_x += 1
      backing_y += 1
    return False
  
  # TODO: this could really use some unit tests for edge cases like: two
  # noncontiguous rows filled, a row filled near the top, a row filled not
  # at the bottom, etc.
  # 
  # Returns the number of rows that were cleared
  def clear_filled_rows(self):
    # full_indication[i] is True if grid[i] is full 
    full_indication = map(
        lambda row: reduce(lambda prev,curr: prev == curr[0] == True, row, True),
        self.grid)
        
    # convert that indicator list into a list of indices
    full_rows = [i for i,v in enumerate(full_indication) if full_indication[i]]
    
    if not full_rows:
      return 0
    
    # shift the coordinates in the cell tuples by y_offset
    def fudge_coords(row, y_offset):
      for pos, cell in enumerate(row):
        if cell[0]:
          row[pos] = (cell[0], cell[1], cell[2] + y_offset, cell[3])
          
    # collapse from bottom to top
    total_rows = len(self.grid)
    dest = full_rows[-1]
    src = dest - 1
    while src >= 0:
      while src in full_rows:
        src -= 1
      self.grid[dest] = self.grid[src]
      fudge_coords(self.grid[dest], dest-src)
      src -= 1
      dest -= 1
    for y in range(len(full_rows)):
      self.grid[y] = [(False,None,None,None)]*self.width
    
    return len(full_rows)
