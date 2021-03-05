from console_args import CONSOLE_ARGS
from map_editor.Brush import BrushType
from map_editor.Brush import CashRegisterBrush
from map_editor.Brush import EntranceBrush
from map_editor.Brush import NavGraphNodeBrush
from map_editor.Brush import ShelfBrush
from map_editor.MapElementToolbar import MapElementToolbar
from map_editor.serialization import MapDeserializer
from map_editor.serialization import MapSerializer
from system import Vector
from system.pathfinding import build_nav_graph
from system.pathfinding import NavGraphNode
from system.ui.EditorFileBrowser import EditorFileBrowser
import logging
import math
import os
import pygame
import pygame_gui
import system.Colors as Colors

logging.basicConfig(level=CONSOLE_ARGS.loglevel)

#https://github.com/MyreMylar/pygame_gui_examples/blob/master/windowed_mini_games_app.py#L28

pygame.init()


class MapEditor(object):
    WINDOWS_SIZE = (1524, 1000)
    FPS = 60
    BRUSH_DIC = {
        BrushType.SHELF: ShelfBrush(),
        BrushType.ENTRANCE: EntranceBrush(),
        BrushType.CASH_REGISTER: CashRegisterBrush()
    }

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Map Editor")
        self.screen = pygame.display.set_mode(MapEditor.WINDOWS_SIZE, pygame.RESIZABLE)
        self.screen.fill(Colors.BACKGROUND_COLOR)

        self.gui_manager = pygame_gui.UIManager(MapEditor.WINDOWS_SIZE, 'map_editor/map_editor_theme.json')
        file_browser_pos = (MapEditor.WINDOWS_SIZE[0]/2, MapEditor.WINDOWS_SIZE[1]/2)
        self.file_browser = EditorFileBrowser(position=file_browser_pos, ui_manager=self.gui_manager, editor=self)
        self.toolbar = MapElementToolbar(position=(5, 5), ui_manager=self.gui_manager, editor=self)

        self.__brush = None

        self.created_map_elements = []
        self.tmp_map_elements = None
        self.tmp_map_elements_start_pos = None
        self.edit_mode = False

        self.__map_image = None
        self.__map_image_name = None
        self.__camera_pos = [0, 0]
        self.__right_mouse_pos = None
        self.__meter_to_pixel_ratio = 0

    def main_loop(self):
        logging.debug("running={}".format(self.is_running))
        while self.is_running:
            self.__draw_background()

            self.__event_handler()
            self.__draw()

            time_delta = self.clock.tick(MapEditor.FPS) / 1000.0
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()

    def __draw_background(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)
        if self.__map_image is not None:
            self.screen.blit(self.__map_image, self.__camera_pos)

    def __draw(self):
        for map_element in self.created_map_elements:
            map_element.draw(self.screen, self.__camera_pos)
        if self.__brush is not None:
            map_element = self.__brush.get_map_element()
            map_element.draw(self.screen, self.__camera_pos)

    def __event_handler(self):
        for event in pygame.event.get():
            self.gui_manager.process_events(event)

            if self.file_browser.is_enabled and self.file_browser.check_clicked_inside_or_blocking(event):
                logging.debug("gui_manager.process_events.file_browser")
            elif self.toolbar.check_clicked_inside_or_blocking(event):
                logging.debug("gui_manager.process_events.toolbar")
            elif self.__map_image is not None:
                logging.debug("main window process_events")
                if event.type == pygame.QUIT:
                    self.__save()
                    self.is_running = False
                elif self.edit_mode is False and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] is True:
                    self.__start_creation_of_map_element()
                elif self.edit_mode is False and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] is True:
                    self.__start_move_camera()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.edit_mode is True:
                        self.__stop_creation_of_map_element()
                    self.__stop_move_camera()
                elif event.type == pygame.MOUSEMOTION:
                    if self.edit_mode is True:
                        self.__resize_edited_map_element()
                    self.__move_camera()
                elif event.type == pygame.VIDEORESIZE:
                    self.__screen_resize(event)

    def __screen_resize(self, event):
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def __resize_edited_map_element(self):
        pos = pygame.mouse.get_pos()
        height = pos[1] - self.tmp_map_elements_start_pos[1]
        width = pos[0] - self.tmp_map_elements_start_pos[0]
        self.__brush.resize_map_element(height, width)

    def __stop_creation_of_map_element(self):
        new_map_element = self.__brush.get_map_element()
        self.created_map_elements.append(new_map_element)
        self.__remove_covered_nav_graph_nodes(new_map_element)
        self.edit_mode = False
        self.tmp_map_elements_start_pos = None

    def __remove_covered_nav_graph_nodes(self, new_map_element):
        nav_graph_node_to_delete = []
        for map_element in self.created_map_elements:
            if type(map_element) is NavGraphNode:
                if map_element.rect.colliderect(new_map_element.get_rect()):
                    nav_graph_node_to_delete.append(map_element)
        self.__delete_covered_nav_graph_nodes(nav_graph_node_to_delete, new_map_element.get_type())

    def __delete_covered_nav_graph_nodes(self, nav_graph_node_to_delete, new_type):
        for node in nav_graph_node_to_delete:
            for map_element in self.created_map_elements:
                if type(map_element) is NavGraphNode:
                    map_element.remove_neighbor(node, new_type)
            self.created_map_elements.remove(node)

    def __start_creation_of_map_element(self):
        if self.__brush is not None:
            self.edit_mode = True
            pos = pygame.mouse.get_pos()
            negative_camera_pos = [x * -1 for x in self.__camera_pos]
            self.__brush.start_drawing(pos)
            self.__brush.move_ip(negative_camera_pos)
            self.tmp_map_elements_start_pos = pos

    def __start_move_camera(self):
        #logging.debug('__start_move_camera')
        pos = pygame.mouse.get_pos()
        self.__right_mouse_pos = Vector(pos[0], pos[1])

    def __stop_move_camera(self):
        logging.debug('__stop_move_camera')
        self.__right_mouse_pos = None

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

    def __save(self):
        MapSerializer.save(self.created_map_elements, self.__map_image_name, self.__meter_to_pixel_ratio)

    def load_map_and_update_screen(self, map_file_path, nav_point_density, width_in_meters):
        self.__map_image_name = map_file_path.split(".")[0]
        self.__map_image = pygame.image.load(map_file_path + ".jpg")
        self.screen = pygame.display.set_mode(self.__map_image.get_rect().size, pygame.RESIZABLE)
        self.file_browser.disable()
        self.file_browser.hide()

        self.__meter_to_pixel_ratio = math.ceil( self.__map_image.get_width() / width_in_meters )

        if os.path.exists(map_file_path + ".map"):
            self.created_map_elements, meter_to_pixel_ratio = MapDeserializer.load_map_file(map_file_path)
        else:
            nav_graph_array, nav_graph_dic, nav_graph_group = build_nav_graph(self.screen.get_rect().size, [], nav_point_density)
            for nodes in nav_graph_array:
                for node in nodes:
                    self.created_map_elements.append(node)

    def select_brash(self, brush_type: BrushType):
        self.__brush = MapEditor.BRUSH_DIC[brush_type]


