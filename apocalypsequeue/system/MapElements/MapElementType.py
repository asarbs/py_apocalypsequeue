from enum import IntEnum


class MapElementType(IntEnum):
    SHELF = 1
    ENTRANCE = 2
    CASH_REGISTER = 3
    NAV_GRAPH_NODE = 4


Int2MapElementType = {
    1: MapElementType.SHELF,
    2: MapElementType.ENTRANCE,
    3: MapElementType.CASH_REGISTER,
    4: MapElementType.NAV_GRAPH_NODE
}