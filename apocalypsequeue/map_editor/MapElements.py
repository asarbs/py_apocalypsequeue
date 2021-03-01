from enum import Enum
import system.Colors as Colors
import pygame


class MapElementType(Enum):
    SHELF = 1
    ENTRANCE = 2
    CASH_REGISTER = 2


class MapElement:
    def __init__(self, rect, color):
        self.__color = color
        self.__rect = rect

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.__rect

    def draw(self, screen, camera_pos):
        if self.get_rect() is not None:
            rect = self.get_rect()
            rect = rect.move(camera_pos)
            pygame.draw.rect(surface=screen, color=self.get_color(), rect=rect)

    def serialization(self):
        return {"pos": (self.__rect.top, self.__rect.left), "dim": self.__rect.size}


class Shelf(MapElement):
    def __init__(self, rect):
        super(Shelf, self).__init__(rect, Colors.SHELVES)


class Entrance(MapElement):
    def __init__(self, rect):
        super(Entrance, self).__init__(rect, Colors.ENTRANCE)

        
class CashRegister(MapElement):
    def __init__(self, rect):
        super(CashRegister, self).__init__(rect, Colors.CASH_REGISTER)
