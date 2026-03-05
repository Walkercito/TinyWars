import pygame


class Building:
    def __init__(
        self,
        row: int,
        column: int,
        image: pygame.Surface,
        grid,
    ):
        self.row = row
        self.column = column
        self.image = image
        self.grid = grid
        self.depth = row + column

    def draw(
        self,
        surface: pygame.Surface,
        camera_x: int,
        camera_y: int,
        zoom: float = 1.0,
    ) -> None:
        """Calculates its isometric position and draws itself."""
        current_grid_width = int(self.grid.tile_width * zoom)
        current_grid_height = int(self.grid.tile_height * zoom)

        iso_x, iso_y = self.grid._cartesian_to_isometric(
            self.row, self.column, current_grid_width, current_grid_height
        )

        screen_x = iso_x - camera_x
        screen_y = iso_y - camera_y

        entity_width = int(self.image.get_width() * zoom)
        entity_height = int(self.image.get_height() * zoom)

        scaled_image = pygame.transform.scale(self.image, (entity_width, entity_height))
        image_x = screen_x - (entity_width // 2)
        image_y = screen_y + current_grid_height - entity_height

        surface.blit(scaled_image, (image_x, image_y))
