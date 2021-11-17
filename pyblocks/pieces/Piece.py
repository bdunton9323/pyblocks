from abc import ABC, abstractmethod
from geometry.Coordinate import Coordinate


class Piece(ABC):
    ROTATION_CURR = 0
    ROTATION_R = 1
    ROTATION_L = -1

    # param: geometry - defines the board and piece geometry (size and layout)
    def __init__(self, geometry):
        self.coord = Coordinate(0, 0, geometry, Coordinate.GRID)
        self.curr_rotation = 0

    @abstractmethod
    def get_color(self):
        return None

    @abstractmethod
    def get_fill_arrays(self):
        pass

    @abstractmethod
    def get_x_y_rota_delta(self, oldindex, newindex):
        pass

    # Changes the stored orientation of the piece.
    # Returns a tuple of (deltaX, deltaY) to be applied to
    # the piece's current coordinates to determine the new coordinates
    # (a rotation CAN change where the corner of the piece is).
    def rotate(self, rotation):
        oldindex = self.get_mask_index(self.get_fill_arrays())
        self.curr_rotation += rotation
        newindex = self.get_mask_index(self.get_fill_arrays())

        return self.get_x_y_rota_delta(oldindex, newindex)

    # Get the index into 'fill_arrays' to use with the current rotation.
    def get_mask_index(self, arrays, rotation=ROTATION_CURR):
        target = self.curr_rotation + rotation
        if target != 0:
            target = target % len(arrays)
        return target

    def get_fill_mask(self, rotation=ROTATION_CURR):
        arrays = self.get_fill_arrays()
        index = self.get_mask_index(arrays, rotation)
        return arrays[index]

    # The x-coordinate relative to the playable grid, in
    # block-sized units (i.e. not pixel position)
    def set_x(self, x, coord_type=Coordinate.GRID):
        self.coord.setX(x, coord_type)

    # The y-coordinate relative to the playable grid, in
    # block-sized units (i.e. not pixel position)
    def set_y(self, y, coord_type=Coordinate.GRID):
        self.coord.setY(y, coord_type)

    def get_x(self, coord_type=Coordinate.GRID):
        return self.coord.getX(coord_type)

    def get_y(self, coord_type=Coordinate.GRID):
        return self.coord.getY(coord_type)

    # this takes the current rotation into account
    def get_height(self):
        arrays = self.get_fill_arrays()
        index = self.get_mask_index(arrays)
        return len(arrays[index])

    # this takes the current rotation into account
    def get_width(self):
        arrays = self.get_fill_arrays()
        index = self.get_mask_index(arrays)
        # The width is the maximum width of all rows in the piece
        max_width = 0
        for row in arrays[index]:
            if len(row) > max_width:
                max_width = len(row)
        return max_width
