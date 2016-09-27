import pygame

# Houses the algorithm for keeping score and determining
# which difficulty level the player is on.
class ScoreKeeper(object):

  # How many rows to complete before increasing difficulty
  ROWS_PER_LEVEL = 7

  def __init__(self):
    self.score = 0
    self.rows = 0
    self.difficulty = 1

  # num_rows - the number of rows cleared in this move (if any)
  # num_clicks - the distance the piece has fallen. Score is skewed such
  #   that more points are awarded as the pieces are higher up.
  def on_move_complete(self, num_rows, num_clicks):
    self.rows += num_rows
    self.difficulty = ScoreKeeper.calculate_difficulty(self.rows)
    
    if num_rows > 0:
      increment = num_rows * 10 * num_rows * self.difficulty
    else:
      increment = self.difficulty
      
    self.score += increment
    
    # reevaluate difficulty because this move may have pushed it up
    self.difficulty = ScoreKeeper.calculate_difficulty(self.rows)
    return self.difficulty
  
  # num_clicks - the distance the piece has fallen. Score is skewed such
  #   that the higher the piece is dropped from, the more points.
  def on_drop(self, num_clicks):
    extra = 0
    if num_clicks <= 7:
      extra = 7 - num_clicks
    self.score += extra
    
  
  def get_score(self):
    return self.score
    
  # The difficulty level is based on 
  def get_difficulty(self):
    return self.difficulty
    
  def get_rows(self):
    return self.rows
    
  @staticmethod
  def calculate_difficulty(rows):
    return rows / ScoreKeeper.ROWS_PER_LEVEL + 1