from enum import Enum
import logging
import pygame
import map_editor.MapElements


class BrushType(Enum):
    SHELF = 1
    NAV_GRAPH_NODE = 2
    ENTRANCE = 3
    CASH_REGISTER = 4


class Brush:
    def __init__(self):
        self._rect = None

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


class ShelfBrush(Brush):
    def __init__(self):
        super(ShelfBrush, self).__init__()

    def get_map_element(self):
        return map_editor.MapElements.Shelf(self._rect)


class NavGraphNodeBrush(Brush):
    def __init__(self):
        super(NavGraphNodeBrush, self).__init__()

    def get_map_element(self):
        return map_editor.MapElements.NavGraphNode(self._rect)

    def resize_map_element(self, height, width):
        pass


class EntranceBrush(Brush):
    def __init__(self):
        super(EntranceBrush, self).__init__()

    def get_map_element(self):
        return map_editor.MapElements.Entrance(self._rect)


class CashRegisterBrush(Brush):
    def __init__(self):
        super(CashRegisterBrush, self).__init__()

    def get_map_element(self):
        return map_editor.MapElements.CashRegister(self._rect)
