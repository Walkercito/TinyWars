import pygame


class Camera:
    def __init__(self, speed: int = 15, limit_x: int = 2000, limit_y: int = 2000):
        self.x = 0
        self.y = 0
        self.speed = speed
        self.limit_x = limit_x
        self.limit_y = limit_y

        self.zoom = 1.0

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
