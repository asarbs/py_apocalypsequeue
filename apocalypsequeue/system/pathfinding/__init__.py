import pygame
import math
import operator
import logging
import system.Colors
from system.Vector import Vector
from system.Colors import NAV_GRAPH_NODE
from system.Colors import CASH_REGISTER
from system.Colors import SHELVES
from system.Colors import ENTRANCE
from system.MapElements.MapElementType import MapElementType

GREEN = (0, 255, 0)
PINK = (199, 21, 133)


class NavGraphNode(pygame.sprite.Sprite):
    count = 1

    class Edge:
        def __init__(self, neighbor, weight):
            self.neighbor = neighbor
            self.weight = weight

        def __str__(self):
            return u'to:{} weight={}'.format(self.neighbor, self.weight)

    def __init__(self, position=Vector(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        if not isinstance(position, Vector):
            raise ValueError("invalid type for position of {}".format(__class__))
        self.__position = position
        self.rect = pygame.Rect(position.getTuple(), (5, 5))
        self.__id = NavGraphNode.count
        self.edge_list = []
        self.__color = NAV_GRAPH_NODE
        self.__color_path = NAV_GRAPH_NODE
        NavGraphNode.count += 1

        self.__type = MapElementType.NAV_GRAPH_NODE

        self.font = pygame.font.SysFont('Arial', 12)


    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def add_neighbor(self, neighbor):
        weight = (self.__position - neighbor.__position).getLength()
        self.edge_list.append(NavGraphNode.Edge(neighbor, weight))

    def remove_neighbor(self, neighbor, map_element_type):
        edge_to_delete = []
        for n in self.edge_list:
            if n.neighbor is neighbor:

                edge_to_delete.append(n)

        if len(edge_to_delete) > 0:
            self.set_type(map_element_type)
        for e in edge_to_delete:
            self.edge_list.remove(e)

    def get_neighbors(self):
        return self.edge_list

    def mark(self):
        self.__color = GREEN

    def mark_path(self):
        self.__color_path = PINK

    def draw(self, screen, camera_pos=(0, 0)):
        rect = self.rect.move(camera_pos)
        for edge in self.edge_list:
            neighbor_rect = edge.neighbor.rect
            neighbor_rect = neighbor_rect.move(camera_pos)
            pygame.draw.line(screen, self.__color_path, rect.center, neighbor_rect.center)
        radius = 5
        pygame.draw.circle(screen, self.__color, rect.center, radius)
        #screen.blit(self.font.render(str(self), "True", system.Colors.WHITE, system.Colors.BLACK), rect)

    def get_id(self):
        return self.__id

    def set_id(self, id_to_set):
        self.__id = id_to_set

    def get_pos(self):
        return self.__position

    def get_pos_vector(self):
        return Vector(self.rect.centerx, self.rect.centery)

    def set_type(self, map_element_type):
        if self.__type is MapElementType.NAV_GRAPH_NODE:
            self.__type = map_element_type
            self.__set_node_color()
        if self.__type is MapElementType.SHELF and map_element_type in (MapElementType.ENTRANCE, MapElementType.CASH_REGISTER):
            self.__type = map_element_type
            self.__set_node_color()

    def __set_node_color(self):
        if self.__type == MapElementType.CASH_REGISTER:
            self.__color = CASH_REGISTER
        elif self.__type == MapElementType.ENTRANCE:
            self.__color = ENTRANCE
        elif self.__type == MapElementType.SHELF:
            self.__color = SHELVES

    def get_color(self):
        return self.__color

    def get_type(self):
        return self.__type

    def serialization(self):
        edge_list_serialization = []
        for edge in self.edge_list:
            edge_list_serialization.append({'neighbor_id':edge.neighbor.get_id(), 'weight': edge.weight})
        return {"id": self.get_id(), "pos": {'top': self.rect.top, 'left': self.rect.left}, "dim": self.rect.size, "neighbor": edge_list_serialization, 'type': int(self.__type)}


def build_nav_graph(screen_size, shelves, nav_point_density):
    logging.info("start to build nav_graph")
    array, build_nav_graph_group, nav_graph_dic = __build_nav_graph_grid(screen_size, shelves, nav_point_density)

    for node_x in range(len(array)):
        for node_y in range(len(array[node_x])):
            node = array[node_x][node_y]
            if isinstance(node, NavGraphNode):
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0):
                            node_to_x = node_x + i
                            node_to_y = node_y + j
                            if node_to_x >= 0 and node_to_y >= 0:
                                try:
                                    node_to = array[node_to_x][node_to_y]
                                    if isinstance(node_to, NavGraphNode):
                                        node.add_neighbor(node_to)
                                except IndexError:
                                    pass
    logging.info("end to build nav_graph")
    return array, nav_graph_dic, build_nav_graph_group


def __if_point_in_shelf(x_pos, y_pos, shelves):
    counter = 0
    for shelf in shelves:
        if not shelf.collidepoint(x_pos, y_pos):
            counter += 1
    return counter == len(shelves)


def __build_nav_graph_grid(screen_size, shelves, nav_point_density):
    build_nav_graph_group = pygame.sprite.Group()
    nav_graph_dic = {}
    divide_x = nav_point_density[0] + 1
    divide_y = nav_point_density[1] + 1
    screen_width_step = math.ceil(screen_size[0] / divide_x)
    screen_height_step = math.ceil(screen_size[1] / divide_y)
    array = [0] * (divide_x)
    for i in range(divide_x):
        array[i] = [0] * (divide_y)

    x_start = 0
    y_start = 0

    for x in range(0, divide_x, 1):
        for y in range(0, divide_y, 1):
            x_pos = x_start + (screen_width_step * x)
            y_pos = y_start + (screen_height_step * y)
            if __if_point_in_shelf(x_pos, y_pos, shelves):
                nav_graph_node = NavGraphNode(Vector(x_pos, y_pos))
                build_nav_graph_group.add(nav_graph_node)
                nav_graph_dic[nav_graph_node.get_id()] = nav_graph_node
                array[x][y] = nav_graph_node
    return array, build_nav_graph_group, nav_graph_dic


def get_min(Q):
    id = min(Q.items(), key=operator.itemgetter(1))[0]
    del Q[id]
    return id


def dijkstras_algorithm(nav_graph_dic, start_node, end_node):
    d = {}
    poprzednik = {}
    # krok 1 dla wszystkich wierzchołków w grafie ustawiam inf jako odległość od wierzchołka startowego. dla wierzchołka startowego ustawiam 0
    for node in nav_graph_dic.values():
        d[node.get_id()] = math.inf
        poprzednik[node.get_id()] = None
    d[start_node.get_id()] = 0

    Q = d.copy()

    while len(Q) > 0:
        u_node = nav_graph_dic[get_min(Q)]
        if u_node == end_node:
            break
        u_neighbors = u_node.get_neighbors()

        for u_neighbor in u_neighbors:
            alt = d[u_node.get_id()] + u_neighbor.weight
            if d[u_neighbor.neighbor.get_id()] > alt:
                d[u_neighbor.neighbor.get_id()] = alt
                poprzednik[u_neighbor.neighbor.get_id()] = u_node.get_id()
                Q[u_neighbor.neighbor.get_id()] = alt

    path = [nav_graph_dic[end_node.get_id()]]
    stop = end_node.get_id()
    while stop is not start_node.get_id():
        x = poprzednik[stop]
        path.append(nav_graph_dic[x])
        stop = x
    path.reverse()

    return path

def get_min_score_node(d):
    minval = min(d.values())
    res = [k for k, v in d.items() if v==minval]
    print(res)
    res.reverse()
    return res[0]


def h(start, end):
    start_pos = start.get_pos_vector()
    end_pos = end.get_pos_vector()
    diff = end_pos - start_pos
    return diff.getLength()


def a_algorithm(nav_graph_dic, start_node, end_node):
    open_set = {}
    open_set[start_node.get_id()] = start_node

    comeFrom = []

    gScore = {}
    fScore = {}
    for k in nav_graph_dic.keys():
        gScore[k] = math.inf
        fScore[k] = math.inf
    gScore[start_node.get_id()] = 0
    fScore[start_node.get_id()] = h(start_node, end_node)

    while len(open_set) > 0:
        min_id = get_min_score_node(fScore)
        current = open_set[min_id]
        if current == end_node:
            return comeFrom
        open_set.pop(current.get_id())
        for edge_neighbor in current.get_neighbors():
            tentative_gScore = gScore[current.get_id()] + edge_neighbor.weight
            if tentative_gScore < gScore[edge_neighbor.neighbor.get_id()]:
                comeFrom.append(current)
                gScore[edge_neighbor.neighbor.get_id()] = tentative_gScore
                fScore[edge_neighbor.neighbor.get_id()] = gScore[edge_neighbor.neighbor.get_id()] + h(edge_neighbor.neighbor, end_node)
                if edge_neighbor.neighbor.get_id() not in open_set:
                    open_set[edge_neighbor.neighbor.get_id()] = edge_neighbor.neighbor



