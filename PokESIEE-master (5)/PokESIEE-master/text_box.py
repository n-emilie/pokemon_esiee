import os
import pygame
import config

class TextBox:

    def __init__(self, message: list[str, str]) -> None:
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join(config.font, "game_font.ttf"), 16)
        self.message = message
        self.coordinate = []
        first_line = (25, 245)
        second_line = (25, 275)
        self.coordinate.append(first_line)
        self.coordinate.append(second_line)

    def draw(self, surface):
        temp_render_zone_upper = self.font.render(self.message[0], False, (0, 0, 0))
        temp_render_zone_bottom = self.font.render(self.message[1], False, (0, 0, 0))
        surface.blit(temp_render_zone_bottom, self.coordinate[1])
        surface.blit(temp_render_zone_upper, self.coordinate[0])
