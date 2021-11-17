from collections import namedtuple

from gameboard.IncomingQueue import IncomingQueue
from gameboard.BackingGrid import BackingGrid
from geometry.Coordinate import Coordinate
from pyblocks.pieces.Piece import Piece

# The result upon landing a piece
PlayOutcome = namedtuple("PlayOutcome", ["still_playing", "num_rows"])

class Board:
    
    # Assuming pieces start in their horizontal position
    MAX_PIECE_HEIGHT = 3

    # param drop_pos - the grid coordinates where the new
    # pieces enter the board
    def __init__(self, geometry, drop_pos):
      self.backing_grid = BackingGrid(
        geometry.get_play_area_width(),
        geometry.get_play_area_height())
      self.active_piece = None
      self.incoming_queue = None
      self.geometry = geometry
      # where the "coming next" panel is drawn
      self.incoming_panel_pos = Coordinate(22, 2, geometry, Coordinate.GRID)
      # the position where the next piece comes in
      self.active_piece_start = Coordinate(drop_pos[0], drop_pos[1], geometry, Coordinate.GRID)
    
    def set_starting_pieces(self, starting_queue, active_piece):
      self.incoming_queue = IncomingQueue(
        self.incoming_panel_pos, Board.MAX_PIECE_HEIGHT, 
        starting_queue)
      self.active_piece = active_piece
      self.active_piece.setX(self.active_piece_start.getX(Coordinate.GRID))
      self.active_piece.setY(self.active_piece_start.getY(Coordinate.GRID))
    
    # This must be called whenever a piece lands
    def on_piece_landed(self):
      if self.__detect_game_over():
        return PlayOutcome(False, 0)
        
      # make active piece inactive
      self.backing_grid.add(self.active_piece)
      rows_completed = self.__evaluate_row_completion()
      return PlayOutcome(True, rows_completed)

      
    # play a piece from the incoming queue and make it active
    def play_next_piece(self, piece_factory):      
      # make the next piece active
      piece = self.incoming_queue.play_next_piece(
        piece_factory.random_piece())
      piece.setX(self.active_piece_start.getX(Coordinate.GRID))
      piece.setY(self.active_piece_start.getY(Coordinate.GRID))
      self.active_piece = piece
    
    # makes the piece fall one click farther
    def advance_piece(self):
      if self.piece_can_move_down(self.active_piece):
        self.active_piece.setY(self.active_piece.getY() + 1) 
        return True
      return False
      
    def piece_can_move_down(self, piece):
      # for now just let it fall to the bottom
      piece_bottom = piece.getY() + piece.get_height()
      if piece_bottom >= self.geometry.get_lower_boundary_grid():
        return False
      elif self.collided_down(piece):
        return False
      else:
        return True

    def collided_down(self, piece):
      new_y = piece.getY(Coordinate.PLAYING_FIELD) + 1
      return self.backing_grid.is_collision(piece.getX(Coordinate.PLAYING_FIELD),
        new_y, piece.get_fill_mask())
    
    def move_left(self):
      if self.can_move_left(self.active_piece):
        self.active_piece.setX(self.active_piece.getX(Coordinate.GRID)-1)
    
    def can_move_left(self, piece):
      new_x = piece.getX(Coordinate.PLAYING_FIELD) - 1
      return new_x >= 0 and not self.backing_grid.is_collision(new_x, 
        piece.getY(Coordinate.PLAYING_FIELD), piece.get_fill_mask())
    
    def move_right(self):
      if self.can_move_right(self.active_piece):
        self.active_piece.setX(self.active_piece.getX(Coordinate.GRID)+1)
    
    def can_move_right(self, piece):
      new_x = piece.getX(Coordinate.PLAYING_FIELD) + 1
      in_bounds = new_x + piece.get_width() <= self.geometry.get_play_area_width()
      return in_bounds and not self.backing_grid.is_collision(new_x, piece.getY(Coordinate.PLAYING_FIELD), piece.get_fill_mask())
    
    def rotate_left(self):
      def do_it():
        return self.active_piece.rotate(Piece.ROTATION_L)
      def undo_it(oldX, oldY, coord_type):
        self.active_piece.rotate(Piece.ROTATION_R)
        self.active_piece.setX(oldX, coord_type)
        self.active_piece.setY(oldY, coord_type)
      self.__rotate(do_it, undo_it)
    
    def rotate_right(self):
      def do_it():
        return self.active_piece.rotate(Piece.ROTATION_R)
      def undo_it(oldX, oldY, coord_type):
        self.active_piece.rotate(Piece.ROTATION_L)
        self.active_piece.setX(oldX, coord_type)
        self.active_piece.setY(oldY, coord_type)
      self.__rotate(do_it, undo_it)
      
    # Pieces rotate about their center. Since piece coordinates are
    # based on the corner, the rotation has to adjust the X and Y
    # coordinates of the piece if the rotation changes the height
    # or width. Collision detection needs to block the rotation if
    # the rotated piece would collide.
    def __rotate(self, do_rotation, undo_rotation):
      # Use playing-field coordinates because the collision checker expects it.
      coord_type = Coordinate.PLAYING_FIELD

      oldX = self.active_piece.getX(coord_type)
      oldY = self.active_piece.getY(coord_type)
      offset = do_rotation()
      newX = oldX + offset[0]
      newY = oldY + offset[1]
      
      in_bounds = newX + self.active_piece.get_width() \
        <= self.geometry.get_right_boundary_playing_field()
      in_bounds = in_bounds and newX >= \
        self.geometry.get_left_boundary_playing_field()
      in_bounds = in_bounds and newY + self.active_piece.get_height() \
        <= self.geometry.get_lower_boundary_playing_field()
        
      success = False

      if in_bounds:
        collided = self.backing_grid.is_collision(
          newX, newY, self.active_piece.get_fill_mask())

        if not collided:
          # finalize the rotation
          self.active_piece.setX(newX, coord_type)
          self.active_piece.setY(newY, coord_type)
          success = True

      if not success:
        undo_rotation(oldX, oldY, coord_type)
      
    def __evaluate_row_completion(self):
      return self.backing_grid.clear_filled_rows()
    
    def __detect_game_over(self):
      return self.active_piece.getY(Coordinate.GRID) <= self.active_piece_start.getY(Coordinate.GRID)
    
    def render(self, renderer):
      for piece in self.incoming_queue:
        renderer.render(piece)
      
      for filled, x, y, color in self.backing_grid:
        if filled:
          renderer.render_tile(x, y, color)
          
      # render the active piece last. Otherwise on the very last
      # piece it will look like the game glitched right before Game Over,
      # since this piece will be behind the already fallen pieces.
      renderer.render(self.active_piece)
      