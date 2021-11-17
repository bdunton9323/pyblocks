from pyblocks.pieces.Piece import Piece


class Box(Piece):

    def __init__(self, geometry):
        super(Box, self).__init__(geometry)

    fill_arrays = [
        [[1, 1], [1, 1]]
    ]

    # See 'Tee' class's rotation table for an explanation
    rotation_table = [
        [(0, 0), (0, 0)],
        [(0, 0), (0, 0)]
    ]

    def get_fill_arrays(self):
        return self.fill_arrays

    def get_color(self):
        return 'green'

    def get_x_y_rota_delta(self, oldindex, newindex):
        return self.rotation_table[oldindex][newindex]
