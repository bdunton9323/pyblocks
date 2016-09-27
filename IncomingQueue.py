from collections import deque
from Coordinate import Coordinate

class IncomingQueue(object):

  # params:
  #  max_size: the size of the queue
  #  origin_coords: An (x,y) tuple of where to put the first piece
  #  max_piece_height: The number of blocks in the tallest possible piece
  #  starting_pieces: The initial pieces. Determines the max queue size
  def __init__(self, origin_coords, max_piece_height, starting_pieces):
    self.max_size = len(starting_pieces)
    self.origin = origin_coords
    self.max_piece_height = max_piece_height
    self.queue = deque()
    self.queue.extend(starting_pieces)
    self.place_on_screen()
 
  def __iter__(self):
    return iter(self.queue)
        
  def place_on_screen(self):
    # The first item in the queue should be drawn on the top
    vertical_offset = 0
    for piece in self.queue:
      vertical_offset += self.max_piece_height
      piece.setX(self.origin.getX(Coordinate.GRID))
      piece.setY(self.origin.getY(Coordinate.GRID) + vertical_offset)
 
  # Get the first piece in queue and put the given piece at the end
  def play_next_piece(self, new_piece):
    next = self.queue.popleft()
    self.queue.append(new_piece)
    
    # shift the pieces up so the next is always on top
    self.place_on_screen()
    
    return next