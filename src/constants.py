from pathlib import Path

from utils.vector import Vector2D

BASE_IMAGE_PATH = Path("data/images")
NEIGHBOR_OFFSETS = [
    Vector2D(*offset) for offset in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
]
PHYSICS_TILES = {"grass", "stone"}
