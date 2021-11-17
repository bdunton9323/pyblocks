from pyblocks.pieces.Piece import Piece


class Ess(Piece):

    def __init__(self, geometry):
        super(Ess, self).__init__(geometry)

    fill_arrays = [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]]
    ]

    # see 'Tee' class's rotation table for an explanation
    rotation_table = [
        # currently pointing up
        [(0, 0), (0, 0)],
        # currently pointing right
        [(0, 0), (0, 0)],
    ]

    def get_fill_arrays(self):
        return self.fill_arrays

    def get_x_y_rota_delta(self, oldindex, newindex):
        return self.rotation_table[oldindex][newindex]

    def get_color(self):
        return 'red'
