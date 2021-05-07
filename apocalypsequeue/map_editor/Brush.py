from enum import Enum
import logging
import pygame
import system.MapElements.MapElements


class BrushType(Enum):
    SHELF = 1
    ENTRANCE = 2
    CASH_REGISTER = 3


class Brush:
    def __init__(self, product_type):
        self._rect = None
        self.product_type = product_type

    def start_drawing(self, pos):
        self._rect = pygame.Rect(pos, (10, 10))

    def stop_shelf_drawing(self):
        pass

    def resize_edited_element(self):
        pass

    def get_map_element(self):
        pass

    def resize_map_element(self, height, width):
        logging.debug(u'new height={} width={}'.format(height, width))
        self._rect.height = height
        self._rect.width = width

    def move_ip(self, negative_camera_pos):
        self._rect.move_ip(negative_camera_pos)

    def reset_rect(self):
        self._rect = pygame.Rect((0,0), (0, 0))

class ShelfBrush(Brush):
    def __init__(self, product_type):
        super(ShelfBrush, self).__init__(product_type)

    def get_map_element(self):
        return system.MapElements.MapElements.Shelf(self._rect, self.product_type)


class EntranceBrush(Brush):
    def __init__(self):
        super(EntranceBrush, self).__init__(-1)

    def get_map_element(self):
        return system.MapElements.MapElements.Entrance(self._rect)


class CashRegisterBrush(Brush):
    def __init__(self):
        super(CashRegisterBrush, self).__init__(-2)

    def get_map_element(self):
        return system.MapElements.MapElements.CashRegister(self._rect)
