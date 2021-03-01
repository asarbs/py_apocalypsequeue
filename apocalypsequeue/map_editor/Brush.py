from enum import Enum
import map_editor.Colors as Colors
import logging
import pygame
import map_editor.MapElements


class BrushType(Enum):
    SHELF = 1
    NAV_GRAPH_NODE = 2


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