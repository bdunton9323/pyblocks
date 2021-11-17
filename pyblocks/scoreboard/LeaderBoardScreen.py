import pygame


# Displays the leader high score board.
class LeaderBoardScreen(object):
    BLACK = (0, 0, 0)

    # TODO: it would be nice to vary the colors like in the "TETRIS" title
    BANNER_FONT_COLOR = (0, 0, 255)
    SCORE_ITEM_COLOR = (20, 255, 0)

    BANNER_MSG = "HIGH SCORES"

    # pixels between score entries
    ITEM_SPACING = 20

    # score_reader: reads the high scores from persistent storage
    def __init__(self, screen, score_reader, font_file, banner_font_file):
        self.reader = score_reader
        self.screen = screen
        self.font_file = font_file
        self.banner_font_file = banner_font_file
        self.init_text()
        self.refresh_scores()

    def init_text(self):
        self.banner_font = pygame.font.Font(self.banner_font_file, 72)
        self.banner_text = self.banner_font.render(
            LeaderBoardScreen.BANNER_MSG, 1, LeaderBoardScreen.BANNER_FONT_COLOR)

        self.score_font = pygame.font.Font(self.font_file, 30)

        screen_size = self.screen.get_size()
        text_size = self.banner_text.get_size()
        self.banner_x = screen_size[0] // 2 - text_size[0] // 2
        self.banner_y = screen_size[1] // 16

    def refresh_scores(self):
        scores = self.reader.read_scores()

        # precompute the locations on screen so we don't have to do it on every render
        self.score_items = []
        index = 1
        for item in scores:
            ordinal = self.score_font.render(
                str(index), 1, LeaderBoardScreen.SCORE_ITEM_COLOR)
            name = self.score_font.render(
                item[0], 1, LeaderBoardScreen.SCORE_ITEM_COLOR)
            score = self.score_font.render(
                item[1], 1, LeaderBoardScreen.SCORE_ITEM_COLOR)
            self.score_items.append((ordinal, name, score))
            index += 1

    def render(self):
        self.screen.fill(LeaderBoardScreen.BLACK)
        self.screen.blit(self.banner_text, (self.banner_x, self.banner_y))

        screen_size = self.screen.get_size()
        ordinal_col = screen_size[0] // 5
        name_col = screen_size[0] // 3
        score_col = screen_size[0] * 2 // 3
        y = screen_size[1] // 4
        for item in self.score_items:
            self.screen.blit(item[0], (ordinal_col, y))
            self.screen.blit(item[1], (name_col, y))
            self.screen.blit(item[2], (score_col, y))
            y += item[0].get_size()[1] + LeaderBoardScreen.ITEM_SPACING
