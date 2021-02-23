from map_editor.console_args import EDITOR_CONSOLE_ARGS
from map_editor.FileBrowser import FileBrowser
import logging
import pygame
import pygame_gui

#https://github.com/MyreMylar/pygame_gui_examples/blob/master/windowed_mini_games_app.py#L28


pygame.init()


class MapEditor(object):
    WINDOWS_SIZE = (1024, 800)
    FPS = 60
    BACKGROUND_COLOR = (0, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self):
        self.is_running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Map Editor")
        self.screen = pygame.display.set_mode(MapEditor.WINDOWS_SIZE, pygame.RESIZABLE)
        self.screen.fill(MapEditor.BACKGROUND_COLOR)

        self.gui_manager = pygame_gui.UIManager(MapEditor.WINDOWS_SIZE)
        self.file_browser = FileBrowser(position=(10, 10), ui_manager=self.gui_manager, editor=self)

        self.created_rectangles = []
        self.shelf_counter = 0
        self.tmp_rec = None
        self.tmp_rec_start_pos = None
        self.edit_mode = False

        self.__map_image = None

    def main_loop(self):
        while self.is_running:
            self.__draw_background()

            self.__event_handler()
            self.__draw()

            time_delta = self.clock.tick(MapEditor.FPS) / 1000.0
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()

    def __draw_background(self):
        if self.__map_image is not None:
            logging.debug('{}:'.format(self.__map_image))
            self.screen.blit(self.__map_image, (0, 0))
        else:
            self.screen.fill(MapEditor.BACKGROUND_COLOR)

    def load_map(self, map_file_path):
        self.__map_image = pygame.image.load(map_file_path)

    def __draw(self):
        for rect in self.created_rectangles:
            pygame.draw.rect(self.screen, MapEditor.GREEN, rect)
        if self.tmp_rec is not None:
            logging.debug(u'tmp_rec.pos={}'.format((self.tmp_rec.top, self.tmp_rec.left, self.tmp_rec.bottom, self.tmp_rec.right)))
            pygame.draw.rect(self.screen, MapEditor.GREEN, self.tmp_rec)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif self.edit_mode is False and event.type == pygame.MOUSEBUTTONDOWN:
                self.__start_shelf_drawing()
            elif self.edit_mode is True and event.type == pygame.MOUSEBUTTONUP:
                self.__stop_shelf_drawing()
            elif self.edit_mode is True and event.type == pygame.MOUSEMOTION:
                self.__resize_edited_shelf()
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
        if self.tmp_rec is not None:
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