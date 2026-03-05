import pygame

from src.entities.buildings.building import Building


class BuildingManager:
    def __init__(self):
        self.buildings: list[Building] = []

    def add_building(self, building: Building) -> None:
        """Adds a new building instance to the manager."""
        self.buildings.append(building)

    def draw(
        self,
        surface: pygame.Surface,
        camera_x: int,
        camera_y: int,
        zoom: float = 1.0,
    ) -> None:
        """Sorts buildings by depth and delegates the drawing to each building."""
        sorted_buildings = sorted(self.buildings, key=lambda b: b.depth)

        for building in sorted_buildings:
            building.draw(surface, camera_x, camera_y, zoom)
