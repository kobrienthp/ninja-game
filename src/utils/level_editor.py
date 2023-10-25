import glob
import sys
from pathlib import Path

import pygame

from constants import BASE_IMAGE_PATH
from objects.tilemap import Tilemap
from utils import util_funcs
from utils.vector import Vector2D

RENDER_SCALE = 2.0


class LevelEditor:
    def __init__(self) -> None:
        pygame.init()
        pygame.joystick.init()

        try:
            self.joystick = pygame.joystick.Joystick(0)
        except:
            pass

        self.screen = pygame.display.set_mode(size=(640, 480))
        self.assets = {
            "decor": util_funcs.load_images(*sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/decor/*.png")))),
            "large_decor": util_funcs.load_images(*sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/large_decor/*.png")))),
            "grass": util_funcs.load_images(*sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/grass/*.png")))),
            "stone": util_funcs.load_images(*sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/stone/*.png")))),
        }
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.on_grid = True
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((320, 240))
        self.movement = Vector2D(0, 0)
        self.scroll = Vector2D(0, 0)
        self.tilemap = Tilemap(
            assets={key: val for key, val in self.assets.items() if key in ["grass", "stone", "decor", "large_decor"]},
            tile_size=16,
        )
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        pygame.display.set_caption("level editor")

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append(
                                {
                                    "type": self.tile_list[self.tile_group],
                                    "variant": self.tile_variant,
                                    "position": mouse_position + self.scroll,
                                }
                            )
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement.x = -1
                    if event.key == pygame.K_d:
                        self.movement.x = 1
                    if event.key == pygame.K_w:
                        self.movement.y = -1
                    if event.key == pygame.K_s:
                        self.movement.y = 1
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid
                    if event.key == pygame.K_o:
                        self.tilemap.save(Path("data/maps/map.json"))
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement.x = 0
                    if event.key == pygame.K_d:
                        self.movement.x = 0
                    if event.key == pygame.K_w:
                        self.movement.y = 0
                    if event.key == pygame.K_s:
                        self.movement.y = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.display.fill((0, 0, 0))

            self.scroll += self.movement * 2
            render_scroll = self.scroll.round()

            self.tilemap.render(self.display, camera_offset=render_scroll)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            mouse_position = Vector2D(*pygame.mouse.get_pos()) / RENDER_SCALE
            tile_position = (mouse_position.round() + self.scroll) // self.tilemap.tile_size

            if self.on_grid:
                self.display.blit(current_tile_image, (tile_position * self.tilemap.tile_size - self.scroll).to_tuple())
            else:
                self.display.blit(current_tile_image, mouse_position.to_tuple())

            if self.clicking and self.on_grid:
                self.tilemap.tilemap[str(tile_position)] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "position": tile_position,
                }
            if self.right_clicking:
                if str(tile_position) in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str(tile_position)]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_image = self.assets[tile["type"]][tile["variant"]]
                    tile_rect = pygame.Rect(
                        *(tile["position"] - self.scroll),
                        tile_image.get_width(),
                        tile_image.get_height(),
                    )
                    if tile_rect.collidepoint(mouse_position.to_tuple()):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_image, (5, 5))

            # self.tilemap.render(surface=self.display, camera_offset=render_scroll)
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0),
            )

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    LevelEditor().run()
