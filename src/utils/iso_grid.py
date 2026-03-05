import math
from os.path import join

import pygame

from src.constants import ISO_LINE_COLOR


class IsometricGrid:
    def __init__(
        self,
        tile_width: int,
        tile_height: int,
        rows: int,
        columns: int,
        x_offset: int,
        y_offset: int,
        debug: bool = False,
    ):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.rows = rows
        self.columns = columns
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.debug = debug

        self.hover_image = pygame.image.load(
            join("src", "assets", "UI", "Grid", "UI_icon_grid_grey.png")
        ).convert_alpha()

        self.hover_image = pygame.transform.scale(
            self.hover_image, (self.tile_width, self.tile_height)
        )

        self._last_zoom = 1.0
        self._scaled_hover_image = self.hover_image

    def _cartesian_to_isometric(
        self, row: int, column: int, current_width: int, current_height: int
    ) -> tuple[int, int]:
        iso_x = (column - row) * (current_width // 2)
        iso_y = (column + row) * (current_height // 2)
        return iso_x + self.x_offset, iso_y + self.y_offset

    def _isometric_to_cartesian(
        self,
        mouse_x: float,
        mouse_y: float,
        current_width: int,
        current_height: int,
    ) -> tuple[int, int]:
        adj_x = mouse_x - self.x_offset
        adj_y = mouse_y - self.y_offset
        half_width = current_width / 2
        half_height = current_height / 2
        column = math.floor((adj_x / half_width + adj_y / half_height) / 2)
        row = math.floor((adj_y / half_height - adj_x / half_width) / 2)
        return int(row), int(column)

    def draw(
        self,
        surface: pygame.Surface,
        mouse_pos: tuple[int, int],
        camera_x: int,
        camera_y: int,
        zoom: float = 1.0,
    ):
        """Draws the isometric grid onto the given surface."""
        current_width = int(self.tile_width * zoom)
        current_height = int(self.tile_height * zoom)

        if self._last_zoom != zoom:
            self._last_zoom = zoom
            self._scaled_hover_image = pygame.transform.scale(
                self.hover_image, (current_width, current_height)
            )

        world_mouse_x = mouse_pos[0] + camera_x
        world_mouse_y = mouse_pos[1] + camera_y
        hovered_row, hovered_column = self._isometric_to_cartesian(
            world_mouse_x, world_mouse_y, current_width, current_height
        )

        for row in range(self.rows):
            for column in range(self.columns):
                iso_x, iso_y = self._cartesian_to_isometric(
                    row, column, current_width, current_height
                )
                screen_x = iso_x - camera_x
                screen_y = iso_y - camera_y
                if (
                    row == hovered_row
                    and column == hovered_column
                    and 0 <= row < self.rows
                    and 0 <= column < self.columns
                ):
                    image_x = screen_x - (current_width // 2)
                    image_y = screen_y
                    surface.blit(self._scaled_hover_image, (image_x, image_y))
                else:
                    if self.debug:
                        p1 = (screen_x, screen_y)
                        p2 = (
                            screen_x + current_width // 2,
                            screen_y + current_height // 2,
                        )
                        p3 = (screen_x, screen_y + current_height)
                        p4 = (
                            screen_x - current_width // 2,
                            screen_y + current_height // 2,
                        )
                        pygame.draw.polygon(
                            surface,
                            ISO_LINE_COLOR,
                            [p1, p2, p3, p4],
                            1,
                        )
                    else:
                        pass
