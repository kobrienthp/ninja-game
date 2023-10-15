import glob
import sys

import pygame

import utils
from constants import BASE_IMAGE_PATH
from objects.clouds import Clouds
from objects.entities import EntityType, PhyicsEntity
from objects.tilemap import Tilemap
from objects.vector2d import Vector2D


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(size=(640, 480))
        self.assets = {
            "decor": utils.load_images(
                *sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/decor/*.png")))
            ),
            "large_decor": utils.load_images(
                *sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/large_decor/*.png")))
            ),
            "grass": utils.load_images(
                *sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/grass/*.png")))
            ),
            "stone": utils.load_images(
                *sorted(glob.glob(str(BASE_IMAGE_PATH / "tiles/stone/*.png")))
            ),
            "player": utils.load_image(BASE_IMAGE_PATH / "entities/player.png"),
            "background": utils.load_image(BASE_IMAGE_PATH / "background.png"),
            "clouds": utils.load_images(
                *sorted(glob.glob(str(BASE_IMAGE_PATH / "clouds/*.png")))
            ),
        }
        self.clock = pygame.time.Clock()
        self.clouds = Clouds(cloud_images=self.assets["clouds"], count=16)
        self.display = pygame.Surface((320, 240))
        self.player = PhyicsEntity(
            entity_type=EntityType.PLAYER,
            position=(50, 50),
            size=(8, 15),
            asset=self.assets.get("player"),
        )
        self.scroll = Vector2D(0, 0)
        self.tilemap = Tilemap(
            assets={
                key: val
                for key, val in self.assets.items()
                if key in ["grass", "stone"]
            },
            tile_size=16,
        )

        pygame.display.set_caption("Ninja Game")

    def run(self) -> None:
        player_movement = [0, 0]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        player_movement[1] = -1
                    if event.key == pygame.K_j:
                        player_movement[1] = 1
                    if event.key == pygame.K_h:
                        player_movement[0] = -1
                    if event.key == pygame.K_l:
                        player_movement[0] = 1
                    if event.key == pygame.K_SPACE:
                        self.player.velocity.y = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_k:
                        player_movement[1] = 0
                    if event.key == pygame.K_j:
                        player_movement[1] = 0
                    if event.key == pygame.K_h:
                        player_movement[0] = 0
                    if event.key == pygame.K_l:
                        player_movement[0] = 0

            self.display.blit(self.assets["background"], (0, 0))
            self.player.update(
                collision_rects=self.tilemap.physics_rects_near_position(
                    self.player.position.to_tuple()
                ),
                movement=player_movement,
            )
            self.scroll += (
                Vector2D(*self.player.rect().center)
                - Vector2D(self.display.get_width(), self.display.get_height()) / 2
                - self.scroll
            ) / 30
            render_scroll = self.scroll.round()

            self.clouds.update()
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            self.tilemap.render(surface=self.display, camera_offset=render_scroll)
            self.player.render(surface=self.display, camera_offset=render_scroll)
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0),
            )

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
