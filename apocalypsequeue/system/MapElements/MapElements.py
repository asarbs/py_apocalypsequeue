from system.MapElements.MapElementType import MapElementType
import pygame
import system.Colors as Colors


class MapElement:
    def __init__(self, rect, color, type):
        self.__color = color
        self.__rect = rect
        self.__type = type

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.__rect

    def get_type(self):
        return self.__type

    def draw(self, screen, camera_pos):
        if self.get_rect() is not None:
            rect = self.get_rect()
            rect = rect.move(camera_pos)
            pygame.draw.rect(surface=screen, color=self.get_color(), rect=rect)

    def serialization(self):
        return {"pos": (self.__rect.left, self.__rect.top), "dim": self.__rect.size}


class Shelf(MapElement):
    def __init__(self, rect):
        super(Shelf, self).__init__(rect, Colors.SHELVES, MapElementType.SHELF)


class Entrance(MapElement):
    def __init__(self, rect):
        super(Entrance, self).__init__(rect, Colors.ENTRANCE, MapElementType.ENTRANCE)

        
class CashRegister(MapElement):
    def __init__(self, rect):
        super(CashRegister, self).__init__(rect, Colors.CASH_REGISTER,MapElementType.CASH_REGISTER)
