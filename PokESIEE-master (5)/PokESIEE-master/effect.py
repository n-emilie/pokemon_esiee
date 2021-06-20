from element import Type, TYPES
from ability import move
import config
import os
import pygame
import spritesheet

BRN = "BURN"
FRZ = "FREEZE"
PAR = "PARALYSIS"
PSN = "POISON"
SLP = "SLEEP"

IMAGE = pygame.image.load(os.path.join(config.image, "spritesheet/effects.png"))


class Effect:

    def __init__(self, image_y, damage: int, counter: list[str]):
        self.image = spritesheet.pick_image(IMAGE, 0, image_y * 60, 116, 50)
        self.damage = damage
        self.counter_types: list[Type] = [TYPES[t] for t in counter]

class Burn(Effect):
    def __init__(self):
        super.__init__(0, int(1 / 16), ["FIRE"])


class Freeze(Effect):
    def __init__(self):
        super.__init__(1, 0, ["ICE"])
        self.memory_moves: list[move.AbstractMove] = []
