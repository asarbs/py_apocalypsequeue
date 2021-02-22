from pygame_gui.elements import UIWindow
import logging
import os
import pygame
import pygame_gui


class FileButton(pygame_gui.elements.UIButton):
    def __init__(self, y_pos, text, manager, parent_element, container, file_path):
        super(FileButton, self).__init__(relative_rect=pygame.Rect((10, y_pos), (200, 30)), text=text, manager=manager, parent_element=parent_element, container=container)
        self.file_path = file_path

class FileBrowser(UIWindow):
    def __init__(self, position, ui_manager):
        super(FileBrowser, self).__init__(pygame.Rect(position, (320, 240)), ui_manager, window_display_title="map selector", object_id="#map_selector")
        self.is_active = False
        self.file_list = []
        self.button_list = []
        x = 10
        for subdir, dirs, files in os.walk("maps"):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".jpg"):
                    self.file_list.append(filepath)
                    button = FileButton(y_pos=x, text=file, manager=ui_manager, parent_element=self, container=self, file_path=filepath)
                    x += 35
                    self.button_list.append(button)
                    logging.debug(filepath)

    def process_event(self, event: pygame.event.Event) -> bool:
        handler = super().process_event(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button in self.button_list:
                    if event.ui_element == button:
                        logging.debug(event.ui_element.file_path)