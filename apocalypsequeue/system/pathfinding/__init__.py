import pygame
import math
import operator
from system.Vector import Vector

RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (248, 191, 223)


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
        self.__color = RED
        NavGraphNode.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def add_neighbor(self, neighbor):
        weight = round((self.__position - neighbor.__position).getLength())
        self.edge_list.append(NavGraphNode.Edge(neighbor, weight))

    def get_neighbors(self):
        return self.edge_list

    def mark(self):
        self.__color = GREEN

    def mark_path(self):
        self.__color = PINK

    def draw(self, screen):
        for edge in self.edge_list:
            pygame.draw.line(screen, RED, self.rect.center, edge.neighbor.rect.center)
        radius = 2
        pygame.draw.circle(screen, self.__color, self.rect.center, radius)

    def get_id(self):
        return self.__id

    def get_pos(self):
        return self.__position


def build_nav_graph(screen_size, shelves):
    array, build_nav_graph_group, nav_graph_dic = __build_nav_graph_grid(screen_size, shelves)

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

    return array, nav_graph_dic, build_nav_graph_group


def __if_point_in_shelf(x_pos, y_pos, shelves):
    counter = 0
    for shelf in shelves:
        if not shelf.rect.collidepoint(x_pos, y_pos):
            counter += 1
    return counter == len(shelves)


def __build_nav_graph_grid(screen_size, shelves):
    build_nav_graph_group = pygame.sprite.Group()
    nav_graph_dic = {}
    divide = 50
    screen_width_step = math.floor(screen_size[0] / divide)
    screen_height_step = math.floor(screen_size[1] / divide)
    array = [0] * (divide)
    for i in range(divide):
        array[i] = [0] * (divide)
    x_start = screen_width_step / 2
    y_start = screen_height_step / 2
    for x in range(0, divide, 1):
        for y in range(0, divide, 1):
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


def dijkstras_algorithm(nav_graph, start_node, end_node):
    d = {}
    poprzednik = {}
    # krok 1 dla wszystkich wierzchołków w grafie ustawiam inf jako odległość od wierzchołka startowego. dla wierzchołka startowego ustawiam 0
    for node in nav_graph.values():
        d[node.get_id()] = math.inf
        poprzednik[node.get_id()] = None
    d[start_node.get_id()] = 0

    Q = d.copy()

    while len(Q) > 0:
        u_node = nav_graph[get_min(Q)]
        if u_node == end_node:
            break
        u_neighbors = u_node.get_neighbors()
        for u_neighbor in u_neighbors:
            alt = d[u_node.get_id()] + u_neighbor.weight
            if d[u_neighbor.neighbor.get_id()] > alt:
                d[u_neighbor.neighbor.get_id()] = alt
                poprzednik[u_neighbor.neighbor.get_id()] = u_node.get_id()
                Q[u_neighbor.neighbor.get_id()] = alt

    path = []
    step = end_node.get_id()
    while step is not start_node.get_id():
        x = poprzednik[step]
        path.append(nav_graph[x])
        step = x
    path.reverse()

    return path
