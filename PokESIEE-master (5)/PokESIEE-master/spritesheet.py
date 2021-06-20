import pygame


# return the specified subImage from a sprite sheet
def pick_image(image: pygame.Surface, x: int, y: int, width: int, height: int) -> pygame.Surface:
    rect = (x, y, width, height)
    return image.subsurface(rect)
