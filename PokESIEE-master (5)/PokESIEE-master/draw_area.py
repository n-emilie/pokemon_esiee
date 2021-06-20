class DrawArea:

    # Draw Area constructor
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # update the draw area rect
    def update_rect(self) -> tuple[int, int, int, int]:
        rect = (self.x, self.y, self.width, self.height)
        return rect
