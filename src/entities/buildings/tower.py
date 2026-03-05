from os.path import join
from random import choice

import pygame

from src.entities.buildings.building import Building
from src.utils.sound_manager import sound_manager
from src.constants import confirm_sound


class Tower(Building):
    _texture_cache: pygame.Surface | None = None

    def __init__(
        self,
        row: int,
        column: int,
        grid,
    ):
        if Tower._texture_cache is None:
            try:
                Tower._texture_cache = pygame.image.load(
                    join(
                        "src",
                        "assets",
                        "Environment",
                        "Buildings",
                        "Tower",
                        "env_buildings_tower.png",
                    )
                ).convert_alpha()

            except FileNotFoundError:
                print("Error loading Tower texture.")
                Tower._texture_cache = pygame.Surface(
                    (256, 256), pygame.SRCALPHA
                )
                Tower._texture_cache.fill((100, 100, 200, 255))

        super().__init__(row, column, Tower._texture_cache, grid)

        sound_manager.play_sfx(choice(confirm_sound))