from system.MapElements.MapElementType import MapElementType
import pygame
import system.Colors as Colors


class MapElement:
    def __init__(self, rect, color, type, product_type):
        self.__color = color
        self.__rect = rect
        self.__type = type
        self.product_type = product_type

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.__rect

    def get_type(self):
        return self.__type

    def get_product_type(self):
        return self.product_type

    def draw(self, screen, camera_pos):
        if self.get_rect() is not None:
            rect = self.get_rect()
            rect = rect.move(camera_pos)
            pygame.draw.rect(surface=screen, color=self.get_color(), rect=rect)

    def serialization(self):
        return {"pos": (self.__rect.left, self.__rect.top), "dim": self.__rect.size, "product_type": self.product_type}


class Shelf(MapElement):
    def __init__(self, rect, product_type):
        super(Shelf, self).__init__(rect, Colors.Shelf_Colors[product_type], MapElementType.SHELF, product_type)


class Entrance(MapElement):
    def __init__(self, rect):
        super(Entrance, self).__init__(rect, Colors.ENTRANCE, MapElementType.ENTRANCE, -1)

        
class CashRegister(MapElement):
    def __init__(self, rect):
        super(CashRegister, self).__init__(rect, Colors.CASH_REGISTER,MapElementType.CASH_REGISTER, -2)
