import pygame

# Takes a rectangle and returns one that is n pixels wider
def _inflate_rect(rect, n):
  return (rect[0] - n, rect[1] - n, rect[2] + n, rect[3] + n)

# Renders the parts of the gameplay screen that aren't the pieces. This includes
# static decorations, background, score box, pause text, etc. The main game loop
# will render this before rendering the pieces, because otherwise the background fill
# would cover the pieces. For that reason, this supports two layers of rendering.
# render_base_layer() should be called before rendering the game pieces. 
# render_top_layer() should be called after rendering the pieces.
class BgRenderer(object):
  BLACK = (0,0,0)
  BORDER_COLOR = (0, 255, 255)
  SCORE_BOX_COLOR = (0, 255, 255)
  SCORE_BOX_WIDTH = 200
  SCORE_BOX_HEIGHT = 90
  SCORE_FONT_COLOR = (185,0,0) #0,150,150
  
  def __init__(self, screen, play_area_coords, piece_width, piece_height,
      score_keeper, font):
    self.screen = screen
    self.score_keeper = score_keeper
    self.pause_overlay = PauseOverlay(screen, play_area_coords)
    self.paused = False
    
    self.bg_image = pygame.image.load('gfx/background.png').convert()

    # fudge the dimensions a little to get the border to fit cleanly
    # around the play area without any piece pixels overlapping the border
    # The format is (left, top, width, height)
    self.playing_field = (
        play_area_coords[0] - 2,
        play_area_coords[1] - 2,
        play_area_coords[2] - play_area_coords[0] + 3,
        play_area_coords[3] - play_area_coords[1] + 3
    )
    
    # The bounding box for the score board
    # Put it to the left of the playing field, flush with the top
    # (left, top, width, height)
    self.score_box = (
        self.playing_field[0] + self.playing_field[2] + 20,
        self.playing_field[1] + self.playing_field[3] - BgRenderer.SCORE_BOX_HEIGHT,
        BgRenderer.SCORE_BOX_WIDTH,
        BgRenderer.SCORE_BOX_HEIGHT
    )
    
    self.upcoming_box = (
        self.playing_field[0] + self.playing_field[2] + 20,
        self.playing_field[1],
        BgRenderer.SCORE_BOX_WIDTH,
        self.playing_field[3] - BgRenderer.SCORE_BOX_HEIGHT - 20
    )
    
    self.score_font = pygame.font.Font(font,30)
            
  def render_base_layer(self):
    self.screen.blit(self.bg_image, (0,0))
    #self.screen.fill(BgRenderer.BLACK)
    self.draw_main_border()
    self.draw_score_box()
    self.draw_upcoming_box()
      
  def draw_main_border(self):
    #self.screen.fill(BgRenderer.BORDER_COLOR, _inflate_rect(self.playing_field, 20))
    #self.screen.fill(BgRenderer.BLACK, self.playing_field, 0)
    pygame.draw.rect(self.screen, BgRenderer.BORDER_COLOR, 
      self.playing_field, 10)
    pygame.draw.rect(self.screen, BgRenderer.BLACK, self.playing_field, 0)
    
  # TODO: move ScoreBox to its own class that Board owns. Either the main
  # game loop in tetris.py can render it on every tick, or Board can render 
  # it only when the score changes. Someone needs to be able to update the
  #score, and BgRenderer is not the place to track that.
  def draw_score_box(self):
    score = "Score: {}".format(str(self.score_keeper.get_score()))
    rows = "Rows: {}".format(str(self.score_keeper.get_rows()))
    level = "Level: {} ".format(str(self.score_keeper.get_difficulty()))

    scoretext = self.score_font.render(score, 1, BgRenderer.SCORE_FONT_COLOR)
    leveltext = self.score_font.render(level, 1, BgRenderer.SCORE_FONT_COLOR)
    rowstext = self.score_font.render(rows, 1, BgRenderer.SCORE_FONT_COLOR)
    
    pygame.draw.rect(self.screen, BgRenderer.BLACK, self.score_box, 0)
    pygame.draw.rect(self.screen, BgRenderer.SCORE_BOX_COLOR,
      self.score_box, 5)
      
    ypos = self.score_box[1] + 10
    self.screen.blit(
        scoretext, 
        (self.score_box[0] + 10, ypos))
    
    ypos += 25
    self.screen.blit(
        leveltext, 
        (self.score_box[0] + 10, ypos))
        
    ypos += 25
    self.screen.blit(
        rowstext, 
        (self.score_box[0] + 10, ypos))

  
  def draw_upcoming_box(self):
    pygame.draw.rect(self.screen, BgRenderer.BLACK, self.upcoming_box, 0)
    pygame.draw.rect(self.screen, BgRenderer.SCORE_BOX_COLOR,
        self.upcoming_box, 5)
    
    
  def render_top_layer(self):
    if self.paused:
      self.draw_pause_overlay()
      
  def set_paused(self, paused):
    # TODO: It might look good to overlay a gray transparency during pause
    self.paused = paused
    
  def draw_pause_overlay(self):
    self.pause_overlay.render()


class PauseOverlay(object):
  TEXT_WIDTH_PX = 50
  TEXT_HEIGHT_PX = 10
  PAUSE_TEXT = "Press 'P' to resume game."
  FONT_COLOR = (255,128,128)
  
  # coords are (left, top, width, height)
  def __init__(self, screen, play_area_coords):
    self.screen = screen
    font = pygame.font.Font(None,30)
    self.text = font.render(self.PAUSE_TEXT, 1, PauseOverlay.FONT_COLOR)
    text_size = font.size(self.PAUSE_TEXT)
    
    center_x = (play_area_coords[0] + play_area_coords[2]) / 2
    center_y = (play_area_coords[1] + play_area_coords[3]) / 2
    self.text_x = center_x - (text_size[0] / 2)
    self.text_y = center_y - (text_size[1] / 2)
    
    
  def render(self):
    self.screen.blit(self.text, (self.text_x, self.text_y))