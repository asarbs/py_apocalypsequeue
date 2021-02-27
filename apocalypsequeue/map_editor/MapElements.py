from enum import Enum
import map_editor.Colors as Colors


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


class Shelf(MapElement):
    def __init__(self, rect):
        super(Shelf, self).__init__(rect, Colors.SHELVES)


class NavGraphNode(MapElement):
    def __init__(self, rect):
        super(NavGraphNode, self).__init__(rect, Colors.NAV_GRAPH_NODE)
