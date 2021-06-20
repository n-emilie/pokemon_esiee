import pygame
import os
import config

class SelectionBox:

    def __init__(self, width: int, x: int, options: list[str, str, str, str], number_of_option: int, font_size: int) -> None:
        # Option Box
        self.width = width
        self.coordinate = (x, 230)
        self.number_of_option = number_of_option
        self.option_box = pygame.transform.scale(
            pygame.image.load(os.path.join(config.image, "misc_sprite/option_box.png")), (self.width, 84))
        pygame.font.init()
        self.user_have_pressed = False
        self.user_have_choose = False
        self.timer = False
        self.size = font_size
        # Font
        self.font = pygame.font.Font(os.path.join(config.font, "game_font.ttf"), self.size)

        # Arrow Image

        self.arrow = pygame.transform.scale(pygame.image.load(os.path.join(config.image, "ui/arrow.png")), (10, 12))

        # Option coordinate
        self.options = options
        self.option_coordinates = []
        x_offset = 25
        y_offset = 20
        top_left = ((x_offset + x), (y_offset + 230))
        bottom_left = ((x_offset + x), (y_offset + 25 + 230))
        top_right = ((self.width / 2 + x + x_offset / 2), (y_offset + 230))
        bottom_right = ((self.width / 2 + x + x_offset / 2), (y_offset + 25 + 230))

        self.possible_cursor_option = []
        top_left_cursor = ((top_left[0] - x_offset / 2), top_left[1])
        top_right_cursor = (top_right[0] - x_offset / 2, top_right[1])
        bottom_left_cursor = (bottom_left[0] - x_offset / 2, bottom_left[1])
        bottom_right_cursor = (bottom_right[0] - x_offset / 2, bottom_right[1])

        self.possible_cursor_option.append(top_left_cursor)
        self.possible_cursor_option.append(top_right_cursor)
        self.possible_cursor_option.append(bottom_left_cursor)
        self.possible_cursor_option.append(bottom_right_cursor)

        self.option_coordinates.append(top_left)
        self.option_coordinates.append(top_right)
        self.option_coordinates.append(bottom_left)
        self.option_coordinates.append(bottom_right)

        self.cursor_index = 0

    def listen_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (self.cursor_index == 1 or self.cursor_index == 3):
            if self.cursor_index - 1 < self.number_of_option :
                self.cursor_index -=1
        elif keys[pygame.K_UP] and (self.cursor_index == 2 or self.cursor_index == 3):
            if self.cursor_index - 2 < self.number_of_option:
                self.cursor_index -= 2
        elif keys[pygame.K_DOWN] and (self.cursor_index == 0 or self.cursor_index == 1):
            if self.cursor_index + 2 < self.number_of_option:
                self.cursor_index += 2
        elif keys[pygame.K_RIGHT] and (self.cursor_index == 0 or self.cursor_index == 2):
            if self.cursor_index +1 < self.number_of_option:
                self.cursor_index += 1
        elif keys[pygame.K_RETURN]:
            self.user_have_choose = True
            print("index: " + str(self.cursor_index))
            self.timer = 0

    def find_user_input(self) -> int:
        return self.cursor_index

    def draw(self, surface):
        surface.blit(self.option_box, self.coordinate)
        for i in range(0, self.number_of_option):
            temp_zone_render = self.font.render(self.options[i], False, (0, 0, 0))
            print(i)
            surface.blit(temp_zone_render, self.option_coordinates[i])
        surface.blit(self.arrow, self.possible_cursor_option[self.cursor_index])

    def update(self):
        self.listen_key()
        self.timer += 1


