from enum import Enum


# Indicates how the current menu was exited, and what the next game state should be.
class MenuAction(Enum):
    # Return to game or start a new game
    PLAY_GAME = 1
    # Stay in the menu
    MENU = 2
    # Show the score board
    SHOW_HIGH_SCORES = 3
    # Exit the game
    QUIT = 4
    # Start over with a new game
    NEW_GAME = 5
