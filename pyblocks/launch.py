from gameplay.game_component_builders import GameContextBuilder
from gameplay.game_component_builders import GameParamsBuilder
from gameplay.game_component_builders import GameStatesBuilder
from gameplay.game_component_builders import PygameContextBuilder
from gameplay.game import Game

if __name__ == "__main__":
    game = Game(PygameContextBuilder(), GameParamsBuilder(), GameContextBuilder(), GameStatesBuilder())
    game.run_game()

