import pygame


class BlockRenderer:

    def __init__(self, screen, geometry):
        self.screen = screen
        self.geometry = geometry
        self.blocks = {}
        self.load_gfx()

    def load_gfx(self):
        self.blocks['red'] = pygame.image.load('gfx/25px/redblock.png').convert()
        self.blocks['blue'] = pygame.image.load('gfx/25px/blueblock.png').convert()
        self.blocks['yellow'] = pygame.image.load('gfx/25px/yellowblock.png').convert()
        self.blocks['purple'] = pygame.image.load('gfx/25px/purpleblock.png').convert()
        self.blocks['green'] = pygame.image.load('gfx/25px/greenblock.png').convert()
        self.blocks['orange'] = pygame.image.load('gfx/25px/orangeblock.png').convert()
        self.blocks['brown'] = pygame.image.load('gfx/25px/brownblock.png').convert()
        self.blocks['lightblue'] = pygame.image.load('gfx/25px/ltblueblock.png').convert()

    # Renders an entire playing piece
    def render(self, piece):
        block = self.blocks[piece.get_color()]
        fill_mask = piece.get_fill_mask()

        curr_y = piece.get_y() * self.geometry.get_block_height()
        for row in fill_mask:
            curr_x = piece.get_x() * self.geometry.get_block_width()
            for position in row:
                if position:
                    self.screen.blit(block, [curr_x, curr_y])
                curr_x += self.geometry.get_block_width()
            curr_y += self.geometry.get_block_height()

    # Renders one square of the grid
    # param x: The x-coordinate in grid-relative coordinates
    # param y: The x-coordinate in grid-relative coordinates
    def render_tile(self, x, y, color):
        block = self.blocks[color]
        self.screen.blit(block,
                         [x * self.geometry.get_block_width(),
                          y * self.geometry.get_block_height()])
