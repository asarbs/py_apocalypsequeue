import pygame
import math
from Vector import Vector
RED = (255, 0, 0)


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
        NavGraphNode.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def add_neighbor(self, neighbor):
        weight = (self.__position - neighbor.__position).getLength()
        self.edge_list.append(NavGraphNode.Edge(neighbor, weight))

    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.rect.center, 2)
        for edge in self.edge_list:
            pygame.draw.line(screen, RED, self.rect.center, edge.neighbor.rect.center)


def build_nav_graph(screen_size):
    build_nav_graph_lists = pygame.sprite.Group()
    divide = 40
    screen_width_step = math.floor(screen_size[0] / divide)
    screen_height_step = math.floor(screen_size[1] / divide)
    array = [0] * (divide + 1)
    for i in range(divide + 1):
        array[i] = [0] * (divide + 1)
    xi = 0
    for x in range(screen_width_step, screen_size[0], screen_width_step):
        yi = 0
        for y in range(screen_height_step, screen_size[1], screen_height_step):
            nav_graph_node = NavGraphNode(Vector(x - (screen_width_step/2), y - (screen_height_step/2)))
            build_nav_graph_lists.add(nav_graph_node)
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

    return build_nav_graph_lists


def event_handler(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def main():
    pygame.init()
    screen_size = [500, 500]
    screen = pygame.display.set_mode(screen_size)
    running = True
    nav_graph = build_nav_graph(screen_size)
    while running:
        running = event_handler(running)
        for node in nav_graph:
            node.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()