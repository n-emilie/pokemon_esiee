import pygame

from direction import Directions as dir
import spritesheet


# player animation
class PlayerAnimations:

    def __init__(self, image: pygame.Surface) -> None:
        self.walking = {}
        self.idle = {}
        self.running = {}
        self.biking = {}
        self.image = image
        self.load_animation()

    def load_animation(self) -> None:

        # walking animation set
        self.walking[dir.NORTH] = []
        self.walking[dir.SOUTH] = []
        self.walking[dir.EAST] = []
        self.walking[dir.WEST] = []

        # running animation set

        self.running[dir.NORTH] = []
        self.running[dir.SOUTH] = []
        self.running[dir.EAST] = []
        self.running[dir.WEST] = []

        # GO DOWN
        y_start = 132
        x_start = 0
        sprite_width = 32
        for i in range(0, 4):
            self.walking[dir.SOUTH].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        for i in range(0, 4):
            self.running[dir.SOUTH].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        y_start = 276
        x_start = 0

        # GO UP
        for i in range(0, 4):
            self.walking[dir.NORTH].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        for i in range(0, 4):
            self.running[dir.NORTH].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        x_start = 0
        y_start = 180

        # GO LEFT
        for i in range(0, 4):
            self.walking[dir.WEST].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        for i in range(0, 4):
            self.running[dir.WEST].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        x_start = 0
        y_start = 228
        for i in range(0, 4):
            self.walking[dir.EAST].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width

        for i in range(0, 4):
            self.running[dir.EAST].append(spritesheet.pick_image(self.image, x_start, y_start, 32, 44))
            x_start += sprite_width
