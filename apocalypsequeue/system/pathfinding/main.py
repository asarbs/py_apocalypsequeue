import pygame
from system.pathfinding import build_nav_graph, dijkstras_algorithm

RED = (255, 0, 0)
GREEN = (0,255,0)
PINK = (248,191,223)
white = (255, 255, 255)
blue = (0, 0, 128)

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 16)


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


def build_shelves():
    shelves = [pygame.Rect(300, 200, 100, 500), pygame.Rect(300, 200, 500, 100), pygame.Rect(600, 600, 100, 200)]

    return shelves

def main():
    screen_size = [1000, 1000]
    screen = pygame.display.set_mode(screen_size)
    running = True
    shelves = build_shelves()
    nav_graph_dic, nav_graph_group = build_nav_graph(screen_size, shelves)
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
            path = dijkstras_algorithm(nav_graph_dic, start_node, end_node)
            for p in path:
                p.mark_path()
            executed = True

        for node in nav_graph_group:
            node.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()