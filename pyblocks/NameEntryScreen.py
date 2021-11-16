import pygame

from . Keys import GameKeys

# handles entry of user initials
class NameEntryScreen(object):
  
  # The valid letters that can be entered
  LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

  MSG_1 = "Congratulations!"
  MSG_2 = "You got a high score!"
  MSG_3 = "Enter your name"

  TEXT_COLOR_1 = (255, 255, 0)
  TEXT_COLOR_2 = (0, 255, 0)
  TEXT_COLOR_3 = (0, 0, 255)
  TEXT_BOX_COLOR = (255, 0, 0)
  ENTRY_COLOR = (0, 255, 0)
  
  # maximum length of entered name
  CHAR_LIMIT = 20
  
  # font_file - font to use for screen elements
  # text_font_file - font to use for the user's name
  def __init__(self, screen, font_file, text_font_file, jukebox, game_keys):
    self.screen = screen
    self.font_file = font_file
    self.text_font_file = text_font_file
    self.init_static_items()
    self.jukebox = jukebox
    self.game_keys = game_keys
    
  # Initialize and position on screen everything that will not move
  def init_static_items(self):
    self.static_items = []
    
    screen_size = self.screen.get_size()
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    
    # TODO: I could cache the font to avoid loading it multiple times
    font = pygame.font.Font(self.font_file, 70)
    text = font.render(NameEntryScreen.MSG_1, 1, NameEntryScreen.TEXT_COLOR_1)
    x = center_x - text.get_size()[0] // 2
    y = screen_size[1] // 8
    self.static_items.append((text, (x, y)))
    
    font = pygame.font.Font(self.font_file, 50)
    text = font.render(NameEntryScreen.MSG_2, 1, NameEntryScreen.TEXT_COLOR_2)
    x = center_x - text.get_size()[0] // 2
    y = screen_size[1] // 4
    self.static_items.append((text, (x, y)))
    
    font = pygame.font.Font(self.font_file, 50)
    text = font.render(NameEntryScreen.MSG_3, 1, NameEntryScreen.TEXT_COLOR_3)
    x = center_x - text.get_size()[0] // 2
    y = screen_size[1] * 3 // 8
    self.static_items.append((text, (x, y)))
    
    self.init_entry_box(screen_size, center_x, screen_size[1])
    
  # Initialize the text area where the typed letters show up
  def init_entry_box(self, screen_size, center_x, screen_height):
    self.entry_so_far = ''

    self.entry_font = pygame.font.Font(self.text_font_file, 50)
    self.char_size = self.entry_font.size('M')
    
    # max text size n characters, plus half a character padding on each side
    width = self.char_size[0] * (NameEntryScreen.CHAR_LIMIT + 1)
    height = self.char_size[1] * 3 // 2
    self.entry_box = (center_x - width // 2, screen_height * 2 // 3, width, height)

  # return True if the game should stay on the score entry screen
  # return False if it is ok to get the name entered.
  def on_key(self, key):
    if key == self.game_keys.by_id(GameKeys.ENTER):
      return False
    
    elif key == self.game_keys.by_id(GameKeys.BACKSPACE):
      self.entry_so_far = self.entry_so_far[:-1]
      self.jukebox.play_typewriter()
    if key.name in NameEntryScreen.LETTERS:
      letter = key.name
      if len(self.entry_so_far) < NameEntryScreen.CHAR_LIMIT:
        self.jukebox.play_typewriter()
        self.entry_so_far += letter

    return True

  def render(self):
    self.screen.fill((0,0,0))
    self.draw_entry_box()
    for item in self.static_items:
      self.screen.blit(item[0], item[1])

  # The text area where the typed text shows up
  def draw_entry_box(self):
    # border
    pygame.draw.rect(self.screen, NameEntryScreen.TEXT_BOX_COLOR, self.entry_box, 10)
    # typed text
    text = self.entry_font.render(self.entry_so_far, 1, NameEntryScreen.ENTRY_COLOR)
    x = self.entry_box[0] + self.char_size[0] // 2
    y = self.entry_box[1] + self.char_size[1] // 2
    self.screen.blit(text, (x,y))
    
  def get_and_clear_name_entered(self):
    tmp = self.entry_so_far
    self.entry_so_far = ''
    return tmp