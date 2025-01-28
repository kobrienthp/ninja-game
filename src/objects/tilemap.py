import json
from pathlib import Path
from typing import Dict, List

import pygame

from constants import NEIGHBOR_OFFSETS, PHYSICS_TILES
from utils.vector import Vector2D


class Tilemap:
    def __init__(self, assets: Dict, tile_size: float = 16) -> None:
        self.assets = assets
        self.tile_size = tile_size
        self.offgrid_tiles = []
        self.tilemap = dict()

    def save(self, path: Path) -> None:
        json_tilemap = {
            key: {
                "type": tile["type"],
                "variant": tile["variant"],
                "position": str(tile["position"]),
            }
            for key, tile in self.tilemap.items()
        }
        json_offgrid_tiles = [
            {
                "type": tile["type"],
                "variant": tile["variant"],
                "position": str(tile["position"]),
            }
            for tile in self.offgrid_tiles
        ]
        with open(path, "w") as file:
            json.dump({"tilemap": json_tilemap, "tile_size": self.tile_size, "offgrid_tiles": json_offgrid_tiles}, file)

    def load(self, path: Path) -> None:
        with open(path, "r") as file:
            map_data = json.load(file)

        self.tilemap = {
            key: {
                "type": tile["type"],
                "variant": tile["variant"],
                "position": Vector2D(
                    *tuple(
                        int(coord)
                        for coord in tile["position"].replace("(", "").replace(")", "").replace(" ", "").split(",")
                    ),
                ),
            }
            for key, tile in map_data["tilemap"].items()
        }
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = [
            {
                "type": tile["type"],
                "variant": tile["variant"],
                "position": Vector2D(
                    *tuple(
                        float(coord)
                        for coord in tile["position"].replace("(", "").replace(")", "").replace(" ", "").split(",")
                    ),
                ),
            }
            for tile in self.offgrid_tiles
        ]

    def tiles_near_position(self, position: Vector2D) -> List:
        locations_to_check = [position.round() // self.tile_size + offset for offset in NEIGHBOR_OFFSETS]

        return [
            self.tilemap.get(str(location)) for location in locations_to_check if str(location) in self.tilemap.keys()
        ]

    def physics_rects_near_position(self, position: Vector2D) -> List:
        return [
            pygame.Rect(*(tile["position"] * self.tile_size), self.tile_size, self.tile_size)
            for tile in self.tiles_near_position(position=position)
            if tile["type"] in PHYSICS_TILES
        ]

    def render(self, surface: pygame.Surface, camera_offset: Vector2D):
        for tile in self.offgrid_tiles:
            surface.blit(
                self.assets[tile["type"]][tile["variant"]],
                (tile["position"] - camera_offset).coordinates,
            )

        # render only tiles which are on screen
        tiles_to_render = [
            self.tilemap.get(str((xcoord, ycoord)))
            for xcoord in range(
                camera_offset.x // self.tile_size,
                (camera_offset.x + surface.get_width()) // self.tile_size + 1,
            )
            for ycoord in range(
                camera_offset.y // self.tile_size,
                (camera_offset.y + surface.get_height()) // self.tile_size + 1,
            )
            if self.tilemap.get(str((xcoord, ycoord)))
        ]

        for tile in tiles_to_render:
            surface.blit(
                self.assets[tile["type"]][tile["variant"]],
                (tile["position"] * self.tile_size - camera_offset).coordinates,
            )
