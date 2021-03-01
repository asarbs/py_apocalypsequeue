from enum import Enum
import map_editor.Colors as Colors
import pygame

class MapElementType(Enum):
    SHELF = 1
    NAV_GRAPH_NODE = 2


class MapElement:
    def __init__(self, rect, color):
        self.__color = color
        self.__rect = rect

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.__rect

    def draw(self, screen):
        pass


class Shelf(MapElement):
    def __init__(self, rect):
        super(Shelf, self).__init__(rect, Colors.SHELVES)

    def draw(self, screen, camera_pos):
        if self.get_rect() is not None:
            rect = self.get_rect()
            rect = rect.move(camera_pos)
            pygame.draw.rect(surface=screen, color=self.get_color(), rect=rect)


class NavGraphNode(MapElement):
    def __init__(self, rect):
        super(NavGraphNode, self).__init__(rect, Colors.NAV_GRAPH_NODE)

    def draw(self, screen, camera_pos):
        if self.get_rect() is not None:
            rect = self.get_rect()
            rect = rect.move(camera_pos)
            center = rect.center
            radius = 5
            pygame.draw.circle(screen, color=self.get_color(), center=center, radius=radius)
