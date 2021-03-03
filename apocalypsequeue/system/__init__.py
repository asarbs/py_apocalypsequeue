from apocalypse import Client
from console_args import CONSOLE_ARGS
from map_editor.serialization import MapDeserializer
from system.MapElements.MapElementType import Int2MapElementType
from system.MapElements.MapElementType import MapElementType
from system.pathfinding import dijkstras_algorithm
from system.pathfinding import NavGraphNode
from system.ui.SimulationFileBrowser import SimulationFileBrowser
from system.Vector import Vector
import logging
import os
import pygame
import pygame_gui
import random
import system.Colors

pygame.init()


class MainSimulation:
    WINDOWS_SIZE = (1524, 1000)

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Simulation")
        self.screen = pygame.display.set_mode(MainSimulation.WINDOWS_SIZE, pygame.RESIZABLE)
        self.screen.fill(Colors.BACKGROUND_COLOR)

        self.gui_manager = pygame_gui.UIManager(MainSimulation.WINDOWS_SIZE, 'system/simulation_editor_theme.json')
        file_browser_pos = (MainSimulation.WINDOWS_SIZE[0]/2, MainSimulation.WINDOWS_SIZE[1]/2)
        self.file_browser = SimulationFileBrowser(position=file_browser_pos, ui_manager=self.gui_manager, simulation=self)

        self.__agents = []

        self.__map_image = None
        self.__camera_pos = [0, 0]
        self.created_map_elements = []
        self.type_nav_grpah_nodes = \
            {
                MapElementType.SHELF: [],
                MapElementType.ENTRANCE: [],
                MapElementType.CASH_REGISTER: [],
                MapElementType.NAV_GRAPH_NODE: []
            }
        self.__nav_graph_node_dic = {}
        self.__right_mouse_pos = None

    def main_loop(self):
        logging.debug("running={}".format(self.is_running))
        while self.is_running:
            self.__draw_background()
            self.__add_agent()
            self.__move_agents()
            self.__event_handler()
            self.__draw()

            time_delta = self.clock.tick(CONSOLE_ARGS.fps) / 1000.0
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()

    def __draw_background(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)
        if self.__map_image is not None:
            self.screen.blit(self.__map_image, self.__camera_pos)

    def __event_handler(self):
        for event in pygame.event.get():
            self.gui_manager.process_events(event)

            if self.file_browser.is_enabled and self.file_browser.check_clicked_inside_or_blocking(event):
                logging.debug("gui_manager.process_events.file_browser")
            elif self.__map_image is not None:
                logging.debug("main window process_events")
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] is True:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] is True:
                    self.__start_move_camera()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__stop_move_camera()
                elif event.type == pygame.MOUSEMOTION:
                    self.__move_camera()
                elif event.type == pygame.VIDEORESIZE:
                    self.__screen_resize(event)

    def __screen_resize(self, event):
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def __move_camera(self):
        logging.debug('__move_camera')
        if self.__right_mouse_pos is not None:
            pos = pygame.mouse.get_pos()
            current_mouse_pos = Vector(pos[0], pos[1])
            camera_move = current_mouse_pos - self.__right_mouse_pos
            logging.debug('camera_moved={}'.format(camera_move))
            self.__right_mouse_pos = current_mouse_pos
            self.__camera_pos[0] += camera_move.getList()[0]
            self.__camera_pos[1] += camera_move.getList()[1]

    def __start_move_camera(self):
        #logging.debug('__start_move_camera')
        pos = pygame.mouse.get_pos()
        self.__right_mouse_pos = Vector(pos[0], pos[1])

    def __stop_move_camera(self):
        logging.debug('__stop_move_camera')
        self.__right_mouse_pos = None

    def __draw(self):
        for map_element in self.created_map_elements:
            map_element.draw(self.screen, self.__camera_pos)
        for agent in self.__agents:
            agent.draw(self.screen)

    def __add_agent(self):
        if self.__map_image is not None and len(self.__agents) < CONSOLE_ARGS.number_of_clients:
            start_node = random.choice(self.type_nav_grpah_nodes[MapElementType.ENTRANCE])
            target_cash_register = random.choice(self.type_nav_grpah_nodes[MapElementType.CASH_REGISTER])
            middle_steps = random.sample(self.type_nav_grpah_nodes[MapElementType.SHELF], 5)
            infected = random.random() < CONSOLE_ARGS.init_infec
            canInfect = infected
            nodes_to_visit = [start_node] + middle_steps + [target_cash_register]
            path = self.__build_agent_path(nodes_to_visit)
            client = Client(start_node=start_node, path=path, infected=infected, canInfect=canInfect,
                            target_cash_register=target_cash_register)
            self.__agents.append(client)
            print(client)

    def __build_agent_path(self, nodes_to_visit):
        path = []
        for i in range(0, len(nodes_to_visit) - 1 , 1):
            start_node = nodes_to_visit[i]
            end_node = nodes_to_visit[i+1]
            path += dijkstras_algorithm(self.__nav_graph_node_dic, start_node, end_node)
        return path

    def __move_agents(self):
        for agent in self.__agents:
            agent.move()

    def load_map_and_update_screen(self, map_file_path):
        self.__map_image = pygame.image.load(map_file_path + ".jpg")
        self.screen = pygame.display.set_mode(self.__map_image.get_rect().size, pygame.RESIZABLE)
        self.file_browser.disable()
        self.file_browser.hide()

        if os.path.exists(map_file_path + ".map"):
            self.created_map_elements = MapDeserializer.load_map_file(map_file_path)

        for map_element in self.created_map_elements:
            if type(map_element) is NavGraphNode:
                self.type_nav_grpah_nodes[Int2MapElementType[map_element.get_type()]].append(map_element)
                self.__nav_graph_node_dic[map_element.get_id()] = map_element