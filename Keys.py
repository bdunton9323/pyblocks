import pygame
from collections import namedtuple


# This module manages the keys that can be used in the game. It has
# functionality to:
# - map from pygame's representation of the key to the internal representation
# - store a list of keys that are valid
# - provide the function for each valid key (e.g. up key = rotate piece)
# - change the function for a given key (only in-game keys can be mapped, e.g. not ESCAPE or ENTER)

Key = namedtuple("Key", ["id", "name"])

class GameKeys(object):

  # This is probably overkill...
  (UP, DOWN, LEFT, RIGHT, SPACE, ENTER, ESCAPE, BACKSPACE, A, B, C, D, E, F, G,
      H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, ONE, TWO, THREE, 
      FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, ZERO, LBRACKET, RBRACKET,
      SEMICOLON, RSHIFT, LSHIFT, RCTRL, LCTRL, RALT, LALT, RMETA,
      LMETA, LSUPER, RSUPER ) = range(57)
      
  def __init__(self):      
    # TODO: should I make the maps be accessible statically? They will never change.
    self.__build_pygame_map()
    self.__build_id_map()
    self.__build_name_map()
    
  def __build_pygame_map(self):
    keys = {}
    keys[pygame.K_UP] = Key(GameKeys.UP, 'Up')
    keys[pygame.K_DOWN] = Key(GameKeys.DOWN, 'Down')
    keys[pygame.K_LEFT] = Key(GameKeys.LEFT, 'Left')
    keys[pygame.K_RIGHT] = Key(GameKeys.RIGHT, 'Right')
    keys[pygame.K_ESCAPE] = Key(GameKeys.ESCAPE, 'Escape')
    keys[pygame.K_RETURN] = Key(GameKeys.ENTER, 'Enter')
    keys[pygame.K_SPACE] = Key(GameKeys.SPACE, 'Space')
    keys[pygame.K_BACKSPACE] = Key(GameKeys.BACKSPACE, 'Backspace')
    keys[pygame.K_a] = Key(GameKeys.A, 'A')
    keys[pygame.K_b] = Key(GameKeys.B, 'B')
    keys[pygame.K_c] = Key(GameKeys.C, 'C')
    keys[pygame.K_d] = Key(GameKeys.D, 'D')
    keys[pygame.K_e] = Key(GameKeys.E, 'E')
    keys[pygame.K_f] = Key(GameKeys.F, 'F')
    keys[pygame.K_g] = Key(GameKeys.G, 'G')
    keys[pygame.K_h] = Key(GameKeys.H, 'H')
    keys[pygame.K_i] = Key(GameKeys.I, 'I')
    keys[pygame.K_j] = Key(GameKeys.J, 'J')
    keys[pygame.K_k] = Key(GameKeys.K, 'K')
    keys[pygame.K_l] = Key(GameKeys.L, 'L')
    keys[pygame.K_m] = Key(GameKeys.M, 'M')
    keys[pygame.K_n] = Key(GameKeys.N, 'N')
    keys[pygame.K_o] = Key(GameKeys.O, 'O')
    keys[pygame.K_p] = Key(GameKeys.P, 'P')
    keys[pygame.K_q] = Key(GameKeys.Q, 'Q')
    keys[pygame.K_r] = Key(GameKeys.R, 'R')
    keys[pygame.K_s] = Key(GameKeys.S, 'S')
    keys[pygame.K_t] = Key(GameKeys.T, 'T')
    keys[pygame.K_u] = Key(GameKeys.U, 'U')
    keys[pygame.K_v] = Key(GameKeys.V, 'V')
    keys[pygame.K_w] = Key(GameKeys.W, 'W')
    keys[pygame.K_x] = Key(GameKeys.X, 'X')
    keys[pygame.K_y] = Key(GameKeys.Y, 'Y')
    keys[pygame.K_z] = Key(GameKeys.Z, 'Z')
    keys[pygame.K_1] = Key(GameKeys.ONE, 'One')
    keys[pygame.K_2] = Key(GameKeys.TWO, 'Two')
    keys[pygame.K_3] = Key(GameKeys.THREE, 'Three')
    keys[pygame.K_4] = Key(GameKeys.FOUR, 'Four')
    keys[pygame.K_5] = Key(GameKeys.FIVE, 'Five')
    keys[pygame.K_6] = Key(GameKeys.SIX, 'Six')
    keys[pygame.K_7] = Key(GameKeys.SEVEN, 'Seven')
    keys[pygame.K_8] = Key(GameKeys.EIGHT, 'Eight')
    keys[pygame.K_9] = Key(GameKeys.NINE, 'Nine')
    keys[pygame.K_0] = Key(GameKeys.ZERO, 'Zero')
    keys[pygame.K_LEFTBRACKET] = Key(GameKeys.LBRACKET, '[')
    keys[pygame.K_RIGHTBRACKET] = Key(GameKeys.RBRACKET, ']')
    keys[pygame.K_SEMICOLON] = Key(GameKeys.SEMICOLON, ';')
    keys[pygame.K_RSHIFT] = Key(GameKeys.RSHIFT, 'Right Shift')
    keys[pygame.K_LSHIFT] = Key(GameKeys.LSHIFT, 'Left Shift')
    keys[pygame.K_RCTRL] = Key(GameKeys.RCTRL, 'Right Ctrl')
    keys[pygame.K_LCTRL] = Key(GameKeys.LCTRL, 'Left Ctrl')
    keys[pygame.K_RALT] = Key(GameKeys.RALT, 'Right Alt')
    keys[pygame.K_LALT] = Key(GameKeys.LALT, 'Left Alt')
    keys[pygame.K_RMETA] = Key(GameKeys.RMETA, 'Right Meta')
    keys[pygame.K_LMETA] = Key(GameKeys.LMETA, 'Left Meta')
    keys[pygame.K_LSUPER] = Key(GameKeys.LSUPER, 'Left Super')
    keys[pygame.K_RSUPER] = Key(GameKeys.RSUPER, 'Right Super')
    
    self.keys = keys
    
  def __build_id_map(self):
    m = {}
    for gamekey in self.keys.values():
      m[gamekey.id] = gamekey
    self.id_map = m
      
  def __build_name_map(self):
    m = {}
    for gamekey in self.keys.values():
      m[gamekey.name.lower()] = gamekey
    self.name_map = m
      
  def from_pygame(self, pygame_key):
    if pygame_key in self.keys:
      return self.keys[pygame_key]
    else:
      return None
    
  def by_name(self, name):
    if name.lower() in self.name_map:
      return self.name_map[name.lower()]
    else:
      return None

  def by_id(self, id):
    if id in self.id_map:
      return self.id_map[id]
    else:
      return None
   
  
class KeyFunction(object):
  INVALID = 0
  MOVE_DOWN = 1
  MOVE_LEFT = 2
  MOVE_RIGHT = 3
  ROTATE_LEFT = 4
  ROTATE_RIGHT = 5
  DROP = 6
  
class KeyChangePublisher(object):
  def __init__(self):
    self.listeners = []
    
  # Register a listener to get updates when the game keys are remapped
  def subscribe(self, listener):
    self.listeners.append(listener)
    
  # Notify all the subscribers that the keys have changed.
  #
  # param key_function - a KeyFunction enum value
  # param new_key - the new key that will represent that function
  def on_key_change(self, key_function, new_key):
    for listener in self.listeners:
      listener(key_function, new_key)  
      

class KeyMapper(object):
 
  def __init__(self, game_keys):
    self.game_keys = game_keys
    self.keys = {}
    self.keys[KeyFunction.MOVE_LEFT] = self.game_keys.by_id(GameKeys.LEFT)
    self.keys[KeyFunction.MOVE_RIGHT] = self.game_keys.by_id(GameKeys.RIGHT)
    self.keys[KeyFunction.MOVE_DOWN] = self.game_keys.by_id(GameKeys.DOWN)
    self.keys[KeyFunction.ROTATE_LEFT] = self.game_keys.by_id(GameKeys.Z)
    self.keys[KeyFunction.ROTATE_RIGHT] = self.game_keys.by_id(GameKeys.X)
    self.keys[KeyFunction.DROP] = self.game_keys.by_id(self.game_keys.SPACE)

  def on_key_change(self, key_function, new_key):
    self.keys[key_function] = new_key
    
  # key is a GameKeys value
  def get_key_function(self, key):
    for f, k in self.keys.iteritems():
      if k == key:
        return f
    return KeyFunction.INVALID
    
  def get_key_by_function(self, function):
    if function in self.keys:
      return self.keys[function]
    return None
        