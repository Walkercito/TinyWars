import pygame

from src.constants import (
    BG_COLOR,
    FPS,
    MAP_COLS,
    MAP_ROWS,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from src.entities.buildings.manager import BuildingManager
from src.entities.buildings.tower import Tower
from src.utils.camera import Camera
from src.utils.iso_grid import IsometricGrid


class Game:
    def __init__(self, screen_width, screen_height, title):
        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title

        self.clock = pygame.time.Clock()
        self.mouse_position = None
        self.running = True

        self.camera = Camera(speed=15, limit_x=3000, limit_y=3000)
        self.building_manager = BuildingManager()

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption(self.title)

        x_offset = self.screen_width // 2
        y_offset = self.screen_height // 2

        self.isometric_grid = IsometricGrid(
            TILE_WIDTH, TILE_HEIGHT, MAP_ROWS, MAP_COLS, x_offset, y_offset
        )

    def run(self) -> None:
        while self.running:
            self._process_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()

    def _update(self) -> None:
        self.camera.update()

    def _process_events(self) -> None:
        self.mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.camera.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click_build()

    def _handle_click_build(self) -> None:
        """Calculates grid coordinates from mouse click and spawns a building"""
        world_mouse_x = self.mouse_position[0] + self.camera.x  # ty:ignore
        world_mouse_y = self.mouse_position[1] + self.camera.y  # ty:ignore

        current_width = int(TILE_WIDTH * self.camera.zoom)
        current_height = int(TILE_HEIGHT * self.camera.zoom)

        row, column = self.isometric_grid._isometric_to_cartesian(
            world_mouse_x, world_mouse_y, current_width, current_height
        )
        if (
            0 <= row < self.isometric_grid.rows
            and 0 <= column < self.isometric_grid.columns
        ):
            new_tower = Tower(row, column, self.isometric_grid)
            self.building_manager.add_building(new_tower)

    def _draw(self) -> None:
        self.window.fill(BG_COLOR)

        self.isometric_grid.draw(
            self.window,
            self.mouse_position,  # ty:ignore
            self.camera.x,
            self.camera.y,
            self.camera.zoom,
        )

        self.building_manager.draw(
            self.window, self.camera.x, self.camera.y, self.camera.zoom
        )

        pygame.display.flip()
