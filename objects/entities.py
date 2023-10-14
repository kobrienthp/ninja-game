from enum import Enum
from typing import List, Tuple

import pygame

from objects.tilemap import Tilemap
from objects.vector2d import Vector2D


class EntityType(Enum):
    PLAYER = "player"


class PhyicsEntity:
    def __init__(
        self,
        entity_type: EntityType,
        position: Tuple,
        size: Tuple,
        asset: pygame.Surface,
    ) -> None:
        self.asset = asset
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        self.position = Vector2D(*position)
        self.size = list(size)
        self.type = entity_type
        self.velocity = Vector2D(0, 0)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.position, *self.size)

    def update(self, collision_rects: Tilemap, movement: List = [0, 0]):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        delta_position = self.velocity + Vector2D(*movement)
        self.position.x += delta_position.x

        entity_rect = self.rect()
        for rect in collision_rects:
            if entity_rect.colliderect(rect):
                if delta_position.x > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if delta_position.x < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.position.x = entity_rect.x

        delta_position = self.velocity + Vector2D(*movement)
        self.position.y += delta_position.y
        entity_rect = self.rect()
        for rect in collision_rects:
            if entity_rect.colliderect(rect):
                if delta_position.y > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if delta_position.y < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.position.y = entity_rect.y

        self.velocity.y = min(5, self.velocity.y + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity.y = 0

    def render(self, surface: pygame.Surface):
        surface.blit(self.asset, self.position.to_list())
