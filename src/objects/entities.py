from enum import Enum
from typing import Dict, List, Tuple

import pygame

from objects.tilemap import Tilemap
from objects.vector2d import Vector2D


class EntityType(Enum):
    PLAYER = "player"


class PlayerAction(Enum):
    IDLE = "idle"
    JUMP = "jump"
    RUN = "run"


class PhyicsEntity:
    def __init__(
        self,
        entity_type: EntityType,
        position: Tuple,
        size: Tuple,
        assets: Dict,
    ) -> None:
        self.action = None
        self.assets = assets
        self.animation = None
        self.animation_offset = Vector2D(-3, -3)
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        self.entity_type = entity_type
        self.flip = False
        self.position = Vector2D(*position)
        self.size = list(size)
        self.type = entity_type
        self.velocity = Vector2D(0, 0)

        self.set_action(PlayerAction["IDLE"])

    def set_action(self, action: PlayerAction) -> None:
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.entity_type.value][self.action.value].copy()

    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.position, *self.size)

    def update(self, collision_rects: Tilemap, movement: List = [0, 0]) -> None:
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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.animation.update()

    def render(self, surface: pygame.Surface, camera_offset: Vector2D) -> None:
        surface.blit(
            pygame.transform.flip(self.animation.get_current_image(), self.flip, False),
            (self.position - camera_offset + self.animation_offset).to_list(),
        )


class Player(PhyicsEntity):
    def __init__(self, position: Tuple, size: Tuple, assets: Dict) -> None:
        super().__init__(entity_type=EntityType["PLAYER"], position=position, size=size, assets=assets)
        self.air_time = 0

    def update(self, collision_rects: Tilemap, movement: List = [0, 0]) -> None:
        super().update(collision_rects=collision_rects, movement=movement)
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action(PlayerAction["JUMP"])
        elif movement[0] != 0:
            self.set_action(PlayerAction["RUN"])
        else:
            self.set_action(PlayerAction["IDLE"])
