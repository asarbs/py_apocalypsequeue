import pygame
import math
import pprint
import operator
from Vector import Vector
RED = (255, 0, 0)
GREEN = (0,255,0)
PINK = (248,191,223)

class NavGraphNode(pygame.sprite.Sprite):
    count = 1

    class Edge:
        def __init__(self, neighbor, weight):
            self.neighbor = neighbor
            self.weight = weight

    def __init__(self, position=Vector(0,0)):
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
        weight = (self.__position - neighbor.__position).getLength()
        self.edge_list.append(NavGraphNode.Edge(neighbor, weight))

    def get_neighbors(self):
        return self.edge_list

    def mark(self):
        self.__color = GREEN

    def mark_path(self):
        self.__color = PINK

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, self.rect.center, 8)
        for edge in self.edge_list:
            pygame.draw.line(screen, RED, self.rect.center, edge.neighbor.rect.center)

    def get_id(self):
        return self.__id


def build_nav_graph(screen_size):
    build_nav_graph_group = pygame.sprite.Group()
    nav_graph_dic = {}
    divide = 6
    screen_width_step = math.floor(screen_size[0] / divide)
    screen_height_step = math.floor(screen_size[1] / divide)
    array = [0] * (divide)
    for i in range(divide):
        array[i] = [0] * (divide)
    xi = 0
    for x in range(screen_width_step, screen_size[0], screen_width_step):
        yi = 0
        for y in range(screen_height_step, screen_size[1], screen_height_step):
            nav_graph_node = NavGraphNode(Vector(x - (screen_width_step/2), y - (screen_height_step/2)))
            build_nav_graph_group.add(nav_graph_node)
            nav_graph_dic[nav_graph_node.get_id()] = nav_graph_node
            array[xi][yi] = nav_graph_node
            yi += 1
        xi += 1

    for node_x in range(len(array)):
        for node_y in range(len(array[node_x])):
            node = array[node_x][node_y]

            if node_x - 1 > 0 :
                node_top = array[node_x - 1][node_y]
                node.add_neighbor(node_top)

            if node_x + 1 < len(array):
                node_bottom = array[node_x + 1][node_y]
                node.add_neighbor(node_bottom)

            if node_y - 1 > 0:
                node_left = array[node_x][node_y - 1]
                node.add_neighbor(node_left)

            if node_y + 1 < len(array[node_x]):
                node_right = array[node_x][node_y + 1]
                node.add_neighbor(node_right)

    return nav_graph_dic, build_nav_graph_group


def get_min(Q):
    id = min(Q.items(), key=operator.itemgetter(1))[0]
    del Q[id]
    return id



def dijkstras_algorithm(nav_graph, start_node, end_node):
    d = {}
    poprzednik = {}
    #krok 1 dla wszystkich wierzchołków w grafie ustawiam inf jako odległość od wierzchołka startowego. dla wierzchołka startowego ustawiam 0
    for node in nav_graph.values():
        d[node.get_id()] = math.inf
        poprzednik[node.get_id()] = None
    d[start_node.get_id()] = 0

    Q = d.copy()

    while len(Q) > 0:
        u_node = nav_graph[get_min(Q)]
        u_neighbors = u_node.get_neighbors()
        for u_neighbor in u_neighbors:
            if d[u_neighbor.neighbor.get_id()] > d[u_node.get_id()] + u_neighbor.weight:
                d[u_neighbor.neighbor.get_id()] = d[u_node.get_id()] + u_neighbor.weight
                poprzednik[u_neighbor.neighbor.get_id()] = u_node.get_id()

    path = []
    step = end_node.get_id()
    while step is not start_node.get_id():
        x = poprzednik[step]
        path.append(x)
        step = x

    for p in path:
        nav_graph[p].mark_path()

def event_handler(running, nav_graph_dic):
    selected_node_id = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            cursor_pos = pygame.mouse.get_pos()
            for key, value in nav_graph_dic.items():
                if value.rect.collidepoint(cursor_pos):
                    selected_node_id = key
    return running, selected_node_id


def main():
    pygame.init()
    screen_size = [500, 500]
    screen = pygame.display.set_mode(screen_size)
    running = True
    nav_graph_dic, nav_graph_group = build_nav_graph(screen_size)
    start_node = -1
    end_node = -1
    executed = False
    while running:
        running, selected_node_id = event_handler(running, nav_graph_dic)
        if selected_node_id != -1 and start_node == -1:
            start_node = nav_graph_dic[selected_node_id]
            start_node.mark()
        elif selected_node_id != -1 and end_node == -1 and selected_node_id != start_node.get_id():
            end_node = nav_graph_dic[selected_node_id]
            end_node.mark()
        if start_node != -1 and end_node != -1 and not executed :
            dijkstras_algorithm(nav_graph_dic, start_node, end_node)
            executed = True

        for node in nav_graph_group:
            node.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()