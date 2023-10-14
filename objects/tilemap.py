from typing import Dict, List

import pygame

from constants import NEIGHBOR_OFFSETS, PHYSICS_TILES
from objects.vector2d import Vector2D


class Tilemap:
    def __init__(self, assets: Dict, tile_size: float = 16) -> None:
        self.assets = assets
        self.tile_size = tile_size
        self.offgrid_tiles = []

        self.tilemap = {
            **{
                (3 + i, 10): {
                    "type": "grass",
                    "variant": 1,
                    "position": (3 + i, 10),
                }
                for i in range(10)
            },
            **{
                (10, 5 + i): {
                    "type": "stone",
                    "variant": 1,
                    "position": (10, 5 + i),
                }
                for i in range(10)
            },
        }

    def tiles_near_position(self, position: tuple) -> List:
        locations_to_check = [
            (
                Vector2D(*(int(coord // self.tile_size) for coord in position))
                + Vector2D(*offset)
            ).to_tuple()
            for offset in NEIGHBOR_OFFSETS
        ]

        return [
            self.tilemap.get(location)
            for location in locations_to_check
            if location in self.tilemap.keys()
        ]

    def physics_rects_near_position(self, position: tuple) -> List:
        return [
            pygame.Rect(
                *(Vector2D(*tile["position"]) * self.tile_size),
                self.tile_size,
                self.tile_size
            )
            for tile in self.tiles_near_position(position=position)
            if tile["type"] in PHYSICS_TILES
        ]

    def render(self, surface: pygame.Surface, camera_offset: Vector2D):
        for tile in self.offgrid_tiles:
            surface.blit(
                self.assets[tile["type"]][tile["variant"]],
                (Vector2D(*tile["position"]) - camera_offset).to_list(),
            )

        for tile in self.tilemap.values():
            surface.blit(
                self.assets[tile["type"]][tile["variant"]],
                (
                    Vector2D(*tile["position"]) * self.tile_size - camera_offset
                ).to_list(),
            )
