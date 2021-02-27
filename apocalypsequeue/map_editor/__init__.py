from map_editor.editor_console_args import EDITOR_CONSOLE_ARGS
from map_editor.FileBrowser import FileBrowser
from map_editor.MapElementToolbar import MapElementToolbar, BrushType
from system import Vector
import logging
import pygame
import pygame_gui
import pprint

logging.basicConfig(level=EDITOR_CONSOLE_ARGS.loglevel)

#https://github.com/MyreMylar/pygame_gui_examples/blob/master/windowed_mini_games_app.py#L28


pygame.init()


class MapEditor(object):
    WINDOWS_SIZE = (1024, 800)
    FPS = 60
    BACKGROUND_COLOR = (0, 0, 0)
    GREEN = pygame.Color(0, 255, 0, 100)

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Map Editor")
        self.screen = pygame.display.set_mode(MapEditor.WINDOWS_SIZE, pygame.RESIZABLE)
        self.screen.fill(MapEditor.BACKGROUND_COLOR)

        self.gui_manager = pygame_gui.UIManager(MapEditor.WINDOWS_SIZE, 'map_editor_theme.json')
        file_browser_pos = (MapEditor.WINDOWS_SIZE[0]/2, MapEditor.WINDOWS_SIZE[1]/2)
        self.file_browser = FileBrowser(position=file_browser_pos, ui_manager=self.gui_manager, editor=self)
        self.toolbar = MapElementToolbar(position=(5,5), ui_manager=self.gui_manager, editor=self)

        self.__brush = None

        self.created_rectangles = []
        self.shelf_counter = 0
        self.tmp_rec = None
        self.tmp_rec_start_pos = None
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
        self.screen.fill(MapEditor.BACKGROUND_COLOR)
        if self.__map_image is not None:
            self.screen.blit(self.__map_image, self.__camera_pos)

    def load_map(self, map_file_path):
        self.__map_image_name = map_file_path.split(".")[0]
        self.__map_image = pygame.image.load(map_file_path)

    def __draw(self):
        for rect in self.created_rectangles:
            rect_to_draw = rect.move(self.__camera_pos)
            pygame.draw.rect(self.screen, MapEditor.GREEN, rect_to_draw)
        if self.tmp_rec is not None:
            logging.debug(u'tmp_rec.pos={}'.format((self.tmp_rec.top, self.tmp_rec.left, self.tmp_rec.bottom, self.tmp_rec.right)))
            pygame.draw.rect(self.screen, MapEditor.GREEN, self.tmp_rec)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__save()
                self.is_running = False
            elif self.edit_mode is False and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] is True:
                self.__start_shelf_drawing()
            elif self.edit_mode is False and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] is True:
                self.__start_move_camera()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.edit_mode is True:
                    self.__stop_shelf_drawing()
                self.__stop_move_camera()
            elif event.type == pygame.MOUSEMOTION:
                if self.edit_mode is True:
                    self.__resize_edited_shelf()
                self.__move_camera()

            elif event.type == pygame.VIDEORESIZE:
                self.__screen_resize(event)

            self.gui_manager.process_events(event)

    def __screen_resize(self, event):
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def __resize_edited_shelf(self):
        pos = pygame.mouse.get_pos()
        height = pos[1] - self.tmp_rec_start_pos[1]
        width = pos[0] - self.tmp_rec_start_pos[0]
        self.tmp_rec.height = height
        self.tmp_rec.width = width

    def __stop_shelf_drawing(self):
        self.edit_mode = False
        if self.tmp_rec is not None and self.tmp_rec.width > 10 and self.tmp_rec.height > 10:
            negative_camera_pos = [x * -1 for x in self.__camera_pos]
            self.tmp_rec.move_ip(negative_camera_pos)
            self.created_rectangles.append(self.tmp_rec.copy())
        self.tmp_rec = None
        self.tmp_rec_start_pos = None

    def __start_shelf_drawing(self):
        if self.tmp_rec is None:
            self.edit_mode = True
            self.shelf_counter += 1
            pos = pygame.mouse.get_pos()
            self.tmp_rec = pygame.Rect(pos, (1, 1))
            self.tmp_rec_start_pos = pos

    def __start_move_camera(self):
        logging.debug('__start_move_camera')
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
        dic = {"shelves": []}
        for shelf in self.created_rectangles:
            dic['shelves'].append({'pos': (shelf.top, shelf.left), "dim": shelf.size})

        with open(self.__map_image_name + ".map", "w+") as outfile:
            pprint.pprint(dic, outfile)

    def select_brash(self, brush_type: BrushType):
        self.__brush = brush_type


