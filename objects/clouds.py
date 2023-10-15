import random
from typing import Tuple

import pygame

from objects.vector2d import Vector2D


class Cloud:
    def __init__(self, position: Tuple, image, speed: float, depth: float) -> None:
        self.depth = depth
        self.image = image
        self.position = Vector2D(*position)
        self.speed = speed

    def update(self) -> None:
        self.position.x += self.speed

    def render(self, surface: pygame.Surface, offset: Vector2D) -> None:
        render_position = self.position - offset * self.depth
        surface.blit(
            self.image,
            (
                render_position
                % Vector2D(
                    surface.get_width()
                    + self.image.get_width()
                    - self.image.get_width(),
                    surface.get_height()
                    + self.image.get_height()
                    - self.image.get_height(),
                )
            ).to_tuple(),
        )


class Clouds:
    def __init__(self, cloud_images, count: int = 16) -> None:
        self.clouds = sorted(
            [
                Cloud(
                    position=(random.random() * 99999, random.random() * 99999),
                    image=random.choice(cloud_images),
                    speed=(random.random() + 1) * 0.05,
                    depth=random.random() * 0.6 + 0.2,
                )
                for n in range(count)
            ],
            key=lambda x: x.depth,
        )

    def update(self) -> None:
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface: pygame.Surface, offset: Vector2D) -> None:
        for cloud in self.clouds:
            cloud.render(surface=surface, offset=offset)
