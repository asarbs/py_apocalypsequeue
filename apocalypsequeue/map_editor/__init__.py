from map_editor.editor_console_args import EDITOR_CONSOLE_ARGS
from map_editor.FileBrowser import FileBrowser
from map_editor.MapElementToolbar import MapElementToolbar
from map_editor.Brush import BrushType
from map_editor.Brush import ShelfBrush
from map_editor.Brush import NavGraphNodeBrush
from system import Vector
import map_editor.Colors as Colors
import logging
import pprint
import pygame
import pygame_gui

logging.basicConfig(level=EDITOR_CONSOLE_ARGS.loglevel)

#https://github.com/MyreMylar/pygame_gui_examples/blob/master/windowed_mini_games_app.py#L28

pygame.init()


class MapEditor(object):
    WINDOWS_SIZE = (1524, 1000)
    FPS = 60
    BRUSH_DIC = {
        BrushType.SHELF: ShelfBrush(),
        BrushType.NAV_GRAPH_NODE: NavGraphNodeBrush()
    }

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Map Editor")
        self.screen = pygame.display.set_mode(MapEditor.WINDOWS_SIZE, pygame.RESIZABLE)
        self.screen.fill(Colors.BACKGROUND_COLOR)

        self.gui_manager = pygame_gui.UIManager(MapEditor.WINDOWS_SIZE, 'map_editor_theme.json')
        file_browser_pos = (MapEditor.WINDOWS_SIZE[0]/2, MapEditor.WINDOWS_SIZE[1]/2)
        self.file_browser = FileBrowser(position=file_browser_pos, ui_manager=self.gui_manager, editor=self)
        self.toolbar = MapElementToolbar(position=(5,5), ui_manager=self.gui_manager, editor=self)

        self.__brush = None

        self.created_map_elements = []
        self.tmp_map_elements = None
        self.tmp_map_elements_start_pos = None
        self.edit_mode = False

        self.__map_image = None
        self.__map_image_name = None
        self.__camera_pos = [0, 0]
        self.__right_mouse_pos = None

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

    def load_map(self, map_file_path):
        self.__map_image_name = map_file_path.split(".")[0]
        self.__map_image = pygame.image.load(map_file_path)

    def __draw(self):
        for map_element in self.created_map_elements:
            map_element.draw(self.screen)
        if self.__brush is not None:
            map_element = self.__brush.get_map_element()
            map_element.draw(self.screen)

    def __event_handler(self):
        for event in pygame.event.get():
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

            self.gui_manager.process_events(event)

    def __screen_resize(self, event):
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def __resize_edited_map_element(self):
        pos = pygame.mouse.get_pos()
        height = pos[1] - self.tmp_map_elements_start_pos[1]
        width = pos[0] - self.tmp_map_elements_start_pos[0]
        self.__brush.resize_map_element(height, width)

    def __stop_creation_of_map_element(self):
        self.created_map_elements.append(self.__brush.get_map_element())
        self.edit_mode = False
        self.tmp_map_elements_start_pos = None

    def __start_creation_of_map_element(self):
        if self.__brush is not None:
            self.edit_mode = True
            pos = pygame.mouse.get_pos()
            self.__brush.start_drawing(pos)
            self.tmp_map_elements_start_pos = pos

    def __start_move_camera(self):
        #logging.debug('__start_move_camera')
        pos = pygame.mouse.get_pos()
        self.__right_mouse_pos = Vector(pos[0], pos[1])

    def __stop_move_camera(self):
        logging.debug('__stop_move_camera')
        self.__right_mouse_pos = None

    def __move_camera(self):
        #logging.debug('__move_camera')
        if self.__right_mouse_pos is not None:
            pos = pygame.mouse.get_pos()
            current_mouse_pos = Vector(pos[0], pos[1])
            camera_move = current_mouse_pos - self.__right_mouse_pos
            logging.debug('camera_moved={}'.format(camera_move))
            self.__right_mouse_pos = current_mouse_pos
            self.__camera_pos[0] += camera_move.getList()[0]
            self.__camera_pos[1] += camera_move.getList()[1]

    def __save(self):
        dic = {"shelves": []}
        for map_element in self.created_map_elements:
            dic['shelves'].append({'pos': (map_element.get_rect().top, map_element.get_rect().left), "dim": map_element.get_rect().size})
        if self.__map_image_name is not None:
            with open(self.__map_image_name + ".map", "w+") as outfile:
                pprint.pprint(dic, outfile)

    def select_brash(self, brush_type: BrushType):
        self.__brush = MapEditor.BRUSH_DIC[brush_type]

