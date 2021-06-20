class Direction:

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy


class Directions:
    # create all four direction with the correct dx and dy in each case
    NORTH = Direction(0, -1)
    SOUTH = Direction(0, 1)
    EAST = Direction(1, 0)
    WEST = Direction(-1, 0)
