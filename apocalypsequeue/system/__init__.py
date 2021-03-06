from console_args import CONSOLE_ARGS
from data import Data
from datetime import datetime
from map_editor.serialization import MapDeserializer
from numpy import random as nrandom
from system.AgentBuilder import AgentBuilder
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
import system.Colors
import time

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

        self.__agent_builder = None

        self.__agents = []
        self.__agents_count = 0

        self.__map_image = None
        self.__camera_pos = [0, 0]
        self.created_map_elements = []
        self.type_nav_graph_nodes = \
            {
                MapElementType.SHELF: [],
                MapElementType.ENTRANCE: [],
                MapElementType.CASH_REGISTER: [],
                MapElementType.NAV_GRAPH_NODE: []
            }
        self.__nav_graph_node_dic = {}
        self.__right_mouse_pos = None

        self.__data = Data()
        self.__time_step = 0
        self.__meter_to_pixel_ratio = 0
        self.__run_simulation = False
        self.__poisson_random = None
        self.__next_agent_creation_time = None

    def main_loop(self):
        logging.debug("running={}".format(self.is_running))
        for num_of_repetition in range(0, CONSOLE_ARGS.num_of_repeat_max, 1):
            start_time = datetime.now()
            self.restart_simulation()
            while self.is_running:
                self.__time_step += 1
                self.__data.addTimeData(self.__time_step)

                self.__draw_background()
                self.execute_simulation()
                self.__event_handler()

                self.__draw()
                self.__data.addStats(self.__agents, self.__time_step)

                self.__check_end()
                time_delta = self.clock.tick(CONSOLE_ARGS.fps) / 1000.0
                self.gui_manager.update(time_delta)
                self.gui_manager.draw_ui(self.screen)

                pygame.display.update()
            end_time = datetime.now()
            time_delta = (end_time-start_time).total_seconds()
            logging.info('repetition {} take {}[s] {}[m]'.format(num_of_repetition, time_delta, (time_delta / 60.0)))
        self.__data.dump(self.__map_image, self.created_map_elements)

    def restart_simulation(self):
        self.is_running = True
        self.__agents_count = 0
        self.__time_step = 0
        self.__poisson_random = nrandom.poisson(lam=CONSOLE_ARGS.clients_mean_distribution, size=CONSOLE_ARGS.number_of_clients + 1).tolist()
        self.__next_agent_creation_time = self.__poisson_random.pop(0)
        self.__agents.clear()
        if self.__agent_builder is not None:
            self.__agent_builder.reset()

    def execute_simulation(self):
        if self.__run_simulation:
            self.__add_agent()
            self.__move_agents()
            self.__check_infection()

    def __check_end(self):
        num_of_agents_in_cash_register = 0
        for agent in self.__agents:
             if agent.in_cash_register():
                 num_of_agents_in_cash_register += 1
        logging.debug('__check_end: num_of_agents_in_cash_register={}, __agents_count={}'.format(num_of_agents_in_cash_register, self.__agents_count))
        if num_of_agents_in_cash_register == CONSOLE_ARGS.number_of_clients and self.__agents_count == CONSOLE_ARGS.number_of_clients:
            self.is_running = False

    def __draw_background(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)
        if self.__map_image is not None and CONSOLE_ARGS.play_simulation == True:
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
        if CONSOLE_ARGS.play_simulation == True:
            for map_element in self.created_map_elements:
                map_element.draw(self.screen, self.__camera_pos)
            for agent in self.__agents:
                agent.draw(self.screen, self.__camera_pos)

    def __add_agent(self):
        if self.__map_image is not None and self.__agents_count < CONSOLE_ARGS.number_of_clients:
            if self.__time_step >= self.__next_agent_creation_time:
                self.__next_agent_creation_time = self.__time_step + self.__poisson_random.pop(0)
                logging.debug('__next_agent_creation_time={}'.format(self.__next_agent_creation_time))
                self.__agents_count += 1
                client = self.__agent_builder.get_agent()
                self.__agents.append(client)
                logging.debug('new client added to simulation={}'.format(client))

    # def __build_agent_path(self, nodes_to_visit):
    #     path = []
    #     for i in range(0, len(nodes_to_visit) - 1 , 1):
    #         start_node = nodes_to_visit[i]
    #         end_node = nodes_to_visit[i+1]
    #         path += dijkstras_algorithm(self.__nav_graph_node_dic, start_node, end_node)
    #     return path

    def __move_agents(self):
        for agent in self.__agents:
            agent.move()

    def __check_infection(self):
        for a1 in self.__agents:
            for a2 in self.__agents:
                if not a1 == a2 and not a1.isInfected():
                    distance_in_meters = a1.getClientDistance(a2) / self.__meter_to_pixel_ratio
                    if a2.canInfect() and distance_in_meters < CONSOLE_ARGS.inf_distance:
                        self.__data.addContactTime(distance_in_meters)
                        if a1.try_infect(distance_in_meters):
                            self.__data.add_infection_params(a1.getPos(), self.__time_step)

    def load_map_and_update_screen(self, map_file_path):
        self.__map_image = pygame.image.load(map_file_path + ".jpg")
        self.screen = pygame.display.set_mode(self.__map_image.get_rect().size, pygame.RESIZABLE)
        self.file_browser.disable()
        self.file_browser.hide()

        if os.path.exists(map_file_path + ".map"):
            self.created_map_elements, self.__meter_to_pixel_ratio = MapDeserializer.load_map_file(map_file_path)

        for map_element in self.created_map_elements:
            if type(map_element) is NavGraphNode:
                self.type_nav_graph_nodes[Int2MapElementType[map_element.get_type()]].append(map_element)
                self.__nav_graph_node_dic[map_element.get_id()] = map_element
        self.__run_simulation = True
        self.__time_step = 1
        self.__agent_builder = AgentBuilder(self.type_nav_graph_nodes, self.__nav_graph_node_dic)
