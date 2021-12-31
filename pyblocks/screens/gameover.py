import pygame

from gameplay.keys import GameKeys


class GameOverScreen(object):
    BG_COLOR = (0, 0, 0)
    BANNER_COLOR = (255, 0, 0)
    SUBBANNER_COLOR = (0, 0, 255)
    BANNER_TEXT = "GAME OVER!"

    # The action handler result codes that specify what state the game is in
    NO_CHANGE, DONE = range(0, 2)

    def __init__(self, screen, font_file, game_keys):
        self.screen = screen
        self.font_file = font_file
        self.prerender()
        self.score = -1

        self.game_keys = game_keys
        # The keys that will exit the menu
        self.done_keys = [self.game_keys.by_id(GameKeys.ENTER), self.game_keys.by_id(GameKeys.ESCAPE)]

    def set_score(self, score):
        self.score = score
        self.prerender_subtitle()

    def prerender_subtitle(self):
        font = pygame.font.Font(self.font_file, 50)
        self.subtitle = font.render("Your score: " + str(self.score), 1,
                                    GameOverScreen.SUBBANNER_COLOR)
        screen_size = self.screen.get_size()
        font_size = self.subtitle.get_size()
        x = screen_size[0] // 2 - font_size[0] // 2
        y = screen_size[1] * 2 // 3 - font_size[1] // 2
        self.subtitle_loc = (x, y)

    def prerender(self):
        font = pygame.font.Font(self.font_file, 100)
        self.banner = font.render(
            GameOverScreen.BANNER_TEXT, 1, GameOverScreen.BANNER_COLOR)

        # Put the banner in the center left-to-right and a third of the way from the top
        screen_size = self.screen.get_size()
        x = screen_size[0] // 2
        y = screen_size[1] // 3
        banner_size = self.banner.get_size()
        self.banner_loc = (x - (banner_size[0] // 2), y - (banner_size[1] // 2))

    def render(self):
        if self.score < 0:
            raise RuntimeError("Score was not set")
        self.screen.fill(GameOverScreen.BG_COLOR)
        self.screen.blit(self.banner, self.banner_loc)
        self.screen.blit(self.subtitle, self.subtitle_loc)

    def on_key(self, key):
        if key in self.done_keys:
            return GameOverScreen.DONE
        return GameOverScreen.NO_CHANGE
