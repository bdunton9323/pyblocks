import pygame
from collections import namedtuple

from BlockRenderer import BlockRenderer
from BgRenderer import BgRenderer
from Board import Board
from Gameplay import Gameplay
from Keys import *
from GameParams import GameParams
from Geometry import Geometry
from highscorepersistence import *
from LeaderBoardScreen import LeaderBoardScreen
from MenuScreen import MenuScreen
from ScoreKeeper import ScoreKeeper
from NameEntryScreen import NameEntryScreen
from gameover import GameOverScreen
from eventhandlers import *
from audio import *

class Constants:
  FRAME_RATE = 60
  MILLISECONDS = 1000
  
  BLOCK_WIDTH = 25
  BLOCK_HEIGHT = 25

  SCREEN_SIZE = (800, 600)
    
  FIELD_WIDTH = 14
  FIELD_HEIGHT = 17
  x1 = BLOCK_WIDTH*5
  y1 = BLOCK_HEIGHT*3
  # (x1,y1,x2,y2) of the playable area (where the pieces can move)
  PLAY_AREA_COORDS_PX = (
      x1, 
      y1, 
      BLOCK_WIDTH*FIELD_WIDTH + x1,
      BLOCK_HEIGHT*FIELD_HEIGHT + y1)
  del x1
  del y1
  
  # This is relative to the absolute grid (as opposed to the playing field grid)
  PIECE_DROP_POS = (12, 3)
  
  HIGH_SCORE_FILE = "highscores.dat"
  NUM_HIGH_SCORES = 10

  MENU_FONT_FILE = "gfx/font/Laundromatic/SFLaundromaticExtended.ttf"
  SCORE_FONT_FILE = "gfx/font/Laundromatic/SFLaundromaticExtended.ttf"
  TITLE_FONT_FILE = "gfx/font/crackman/crackman.ttf" 
  SCORE_BANNER_FONT_FILE = "gfx/font/crackman/crackman.ttf" 
  GAME_OVER_FONT_FILE = "gfx/font/crackman/crackman.ttf"
  NAME_ENTRY_FONT_FILE = "gfx/font/crackman/crackman.ttf"
  # Use a monospace font here because there is a character limit for the name
  # entry, which needs to fit exactly within the text box.
  NAME_ENTRY_TEXT_FONT_FILE = "gfx/font/bpmono/BPmono.ttf"
  
  KEYS = GameKeys()
  
def init_pygame():
  # Mixer has to be initialized before pygame.
  # http://stackoverflow.com/questions/18273722/pygame-sound-delay
  # http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.pre_init
  pygame.mixer.pre_init(44100, -16, 2, 2048)
  pygame.mixer.init()
  
  pygame.init()
  screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF, 32)
  pygame.display.set_caption("PyBlocks");
  
  params = GameParams()
  params.set_screen(screen)
  params.set_geometry(Geometry(Constants.BLOCK_WIDTH, 
    Constants.BLOCK_HEIGHT, Constants.PLAY_AREA_COORDS_PX))
  params.set_jukebox(Jukebox(pygame.mixer))
  
  # stuff for controlling what the keys are
  key_mapper = KeyMapper(Constants.KEYS)
  key_change_publisher = KeyChangePublisher()
  key_change_publisher.subscribe(key_mapper.on_key_change)
  params.set_key_change_publisher(key_change_publisher)
  params.set_key_mapper(key_mapper)
  
  # set the key delay for holding down buttons  
  pygame.key.set_repeat(250, 75)
  return params

# Resets the game board and the gameplay state
def new_game(params):
  global game_in_progress

  game_in_progress = True
  game_context = namedtuple("GameState", 
      ["score_keeper", "block_renderer", "bg_renderer", "board", "gameplay"])
  game_context.score_keeper = ScoreKeeper()
  game_context.block_renderer = BlockRenderer(params.get_screen(), params.get_geometry())
  game_context.bg_renderer = BgRenderer(params.get_screen(), 
      Constants.PLAY_AREA_COORDS_PX, Constants.BLOCK_HEIGHT, 
      Constants.BLOCK_HEIGHT, game_context.score_keeper, Constants.SCORE_FONT_FILE)
  game_context.board = Board(params.get_geometry(), Constants.PIECE_DROP_POS)
  game_context.gameplay = Gameplay(
      game_context.board, params.get_geometry(), game_context.score_keeper,
      params.get_jukebox(), params.get_key_mapper())

  return game_context
  

# Returns a Mode representing the next state of the game
def run_event_loop(event_handler):
  # TODO: does this initialize a new clock every time? Do I need to just
  # keep passing around the original clock?
  clock = pygame.time.Clock()
  
  # Default mode is to start at the main menu
  mode = Mode.MENU
  keep_going = True
      
  while keep_going:
    key = None
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        mode = Mode.QUIT
        event_handler.on_quit()
        keep_going = False
        
      elif event.type == pygame.KEYDOWN:
        key = Constants.KEYS.from_pygame(event.key)
        if key:
          result = event_handler.on_key(key, Constants.KEYS)
          keep_going = result[0]
          mode = result[1]          
  
    if keep_going:
      millis = int(1 / float(Constants.FRAME_RATE) * Constants.MILLISECONDS)
      keep_going, mode = event_handler.on_tick(millis, key)     
      event_handler.on_render()
      pygame.display.flip()
      clock.tick(Constants.FRAME_RATE)
  return mode
   
def init_states(game_params):
  states = namedtuple("States", ["menu", "game_over", "high_scores", "name_entry"])
  
  states.menu = MenuScreen(game_params.get_screen(), Constants.MENU_FONT_FILE,
      Constants.TITLE_FONT_FILE, game_params.get_jukebox(), game_params.get_key_change_publisher(), Constants.KEYS, game_params.get_key_mapper())
      
  states.game_over = GameOverScreen(game_params.get_screen(), Constants.GAME_OVER_FONT_FILE, Constants.KEYS)
  
  states.high_scores = LeaderBoardScreen(
      game_params.get_screen(), HighScoreReader(
          Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES), Constants.SCORE_FONT_FILE, Constants.SCORE_BANNER_FONT_FILE)
          
  states.name_entry = NameEntryScreen(
      game_params.get_screen(), Constants.NAME_ENTRY_FONT_FILE,
      Constants.NAME_ENTRY_TEXT_FONT_FILE ,game_params.get_jukebox(), Constants.KEYS)
      
  return states
  

if __name__ == "__main__":
  global game_in_progress

  params = init_pygame()
  mode = Mode.MENU
  
  states = init_states(params)
  
  game_in_progress = False
  gameplay_handler = None
  game_context = None
  
  params.get_jukebox().start_game_music()
  
  keep_playing = True
  while keep_playing:
    if mode == Mode.QUIT:
      keep_playing = False
    elif mode == Mode.MENU:
      states.menu.set_paused(game_in_progress)
      handler = MenuHandler(states.menu, game_in_progress)
      mode = run_event_loop(handler)
    elif mode == Mode.NEW_GAME:
      game_in_progress = False
      game_context = new_game(params)
      gameplay_handler = GamePlayHandler(game_context)
      mode = Mode.CONTINUE_GAME
    elif mode == Mode.CONTINUE_GAME:
      mode = run_event_loop(gameplay_handler)
    elif mode == Mode.GAME_OVER:
      game_in_progress = False
      # TODO: keep an instance of HighScoreReader and HighScoreWriter so I don't keep recreating it
      score = game_context.score_keeper.get_score()
      states.game_over.set_score(score)
      handler = GameOverHandler(states.game_over, score, 
          HighScoreReader(Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES))
      # TODO: GameOverHandler should return ScoreBoard or NameEntry mode.
      # I can pass two interfaces into GameOverHandler. One knows how to get the
      # final score, and the other can decide whether the score is a high score.
      # to determine whether the current score. I have started those in new files.
      mode = run_event_loop(handler)
    elif mode == Mode.HIGH_SCORES:
      handler = ScoreBoardHandler(states.high_scores)
      mode = run_event_loop(handler)
    elif mode == Mode.NAME_ENTRY:
      # TODO: preconstruct a HighScoreWriter so I don't keep recreating it.
      handler = NameEntryHandler(states.name_entry,
          game_context.score_keeper, HighScoreWriter(
              Constants.HIGH_SCORE_FILE, Constants.NUM_HIGH_SCORES))
      mode = run_event_loop(handler)
  
  pygame.quit()




