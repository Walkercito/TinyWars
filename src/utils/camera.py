import pygame


class Camera:
    def __init__(
        self,
        speed: int = 15,
        limit_x: int = 2000,
        limit_y: int = 2000,
        vignette: bool = True,
    ):
        self.x = 0
        self.y = 0
        self.speed = speed
        self.limit_x = limit_x
        self.limit_y = limit_y

        self.zoom = 1.0

        self.vignette_enabled = vignette
        self._vignette_surface = None

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self.zoom += event.y * 0.1

            self.zoom = max(0.5, min(self.zoom, 2.5))

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        self.x = max(-self.limit_x, min(self.x, self.limit_x))
        self.y = max(-self.limit_y, min(self.y, self.limit_y))

    def _create_vignette(self, width: int, height: int) -> pygame.Surface:
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)

        for y in range(height):
            for x in range(width):
                corner_distances = [
                    ((x) ** 2 + (y) ** 2) ** 0.5,
                    ((x - width) ** 2 + (y) ** 2) ** 0.5,
                    ((x) ** 2 + (y - height) ** 2) ** 0.5,
                    ((x - width) ** 2 + (y - height) ** 2) ** 0.5,
                ]
                min_corner_dist = min(corner_distances)

                max_dist = (width**2 + height**2) ** 0.5 * 0.25
                if min_corner_dist < max_dist:
                    factor = min_corner_dist / max_dist
                    alpha = int((1 - factor) * 60)
                    vignette.set_at((x, y), (0, 0, 0, alpha))

        return vignette

    def apply_vignette(self, screen: pygame.Surface) -> None:
        if not self.vignette_enabled:
            return

        width, height = screen.get_size()
        if self._vignette_surface is None or self._vignette_surface.get_size() != (
            width,
            height,
        ):
            self._vignette_surface = self._create_vignette(width, height)

        screen.blit(self._vignette_surface, (0, 0))
