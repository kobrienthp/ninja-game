from typing import Optional, Tuple

import pygame

from utils.vector import Vector2D


class Sprite:
    def __init__(
        self,
        image: Optional[str] = None,
        position: Vector2D = Vector2D(0, 0),
        velocity: Vector2D = Vector2D(0, 0),
        colorkey: Optional[Tuple] = None,
        color: Optional[Tuple] = None,
    ) -> None:
        self.color = None
        self.colorkey = None
        self.image = None
        self.position = position
        self.rect = None
        self.velocity = velocity

        if image:
            self.image = pygame.image.load(image)
        if colorkey:
            assert len(colorkey) == 3 and all([i < 256 for i in colorkey]), "invalid `colorkey`"
            self.colorkey = colorkey
            self.image.set_colorkey(self.colorkey)
        if color:
            assert len(color) == 3 and all([i < 256 for i in color]), "invalid `color`"
            self.color = color

    def update_position(self) -> None:
        self.position += self.velocity
