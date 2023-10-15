from typing import List

import pygame


def load_image(path: str) -> pygame.Surface:
    image = pygame.image.load(path).convert()
    image.set_colorkey((0, 0, 0))

    return image


def load_images(*paths) -> List[pygame.Surface]:
    if not isinstance(paths, tuple):
        paths = [paths]

    return [load_image(path) for path in paths]
