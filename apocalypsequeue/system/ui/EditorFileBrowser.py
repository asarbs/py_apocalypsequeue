from pygame_gui.elements import UIWindow
import logging
import os
import pygame
import pygame_gui
import math


class FileButton(pygame_gui.elements.UIButton):
    def __init__(self, y_pos, text, manager, parent_element, container, file_path):
        super(FileButton, self).__init__(relative_rect=pygame.Rect((10, y_pos), (200, 30)), text=text, manager=manager, parent_element=parent_element, container=container)
        self.file_path = file_path


class EditorFileBrowser(UIWindow):
    def __init__(self, position, ui_manager, editor):
        rec = pygame.Rect(position, (320, 240))
        rec.centerx = position[0]
        rec.centery = position[1]
        super(EditorFileBrowser, self).__init__(rec, ui_manager, window_display_title="map selector", object_id="#map_selector")
        self.file_list = []
        self.button_list = []
        self.__input = (self.__with_input_window(ui_manager), self.__height_input_window(ui_manager))
        self.__browse_plans(ui_manager)
        self.selected_file = None
        self.__editor = editor

    def __browse_plans(self, ui_manager):
        x = 65
        for subdir, dirs, files in os.walk("maps"):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".jpg"):
                    filepath = filepath.split(".")[0]
                    self.file_list.append(filepath)
                    button = FileButton(y_pos=x, text=file, manager=ui_manager, parent_element=self, container=self,
                                        file_path=filepath) #Buttons creation part should be moved to separate method.
                    x += 35
                    self.button_list.append(button)
                    logging.debug(filepath)

    def __with_input_window(self, ui_manager):
        tmp = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 10), (200, 30)), manager=ui_manager, parent_element=self, container=self, object_id="with_input_window")
        tmp.set_text("19")
        return tmp

    def __height_input_window(self, ui_manager):
        tmp = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 35), (200, 30)), manager=ui_manager, parent_element=self, container=self, object_id="height_input_window")
        tmp.set_text("13")
        return tmp

    def process_event(self, event: pygame.event.Event) -> bool:
        handler = super().process_event(event)
        if event.type == pygame.USEREVENT:

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button in self.button_list:
                    if event.ui_element == button:
                        logging.debug('loaded map:{}'.format(event.ui_element.file_path))
                        if self.__input[0].get_text() == '' or self.__input[1].get_text() == '':
                            return False
                        else:
                            nav_point_density_x = math.ceil(float(self.__input[0].get_text()) / 0.7)
                            nav_point_density_y = math.ceil(float(self.__input[1].get_text()) / 0.7)
                        self.__editor.load_map_and_update_screen(event.ui_element.file_path, (nav_point_density_x, nav_point_density_y))
                        return True
        return False
