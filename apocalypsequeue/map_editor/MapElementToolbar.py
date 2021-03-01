from map_editor.Brush import BrushType
from pygame_gui.elements import UIWindow
import logging
import pygame
import pygame_gui


class BrushButton(pygame_gui.elements.UIButton):
    def __init__(self, pos, text, manager, parent_element, container, object_id, type: BrushType):
        super(BrushButton, self).__init__(relative_rect=pygame.Rect(pos, (150, 30)), text=text, manager=manager,
                                          parent_element=parent_element, container=container, object_id=object_id)
        self.type = type


class ShelfButton(BrushButton):
    def __init__(self, pos, manager, parent_element, container):
        super(ShelfButton, self).__init__(pos, "Shelf", manager, parent_element, container, "#"+__class__.__name__, BrushType.SHELF)


class EntranceButton(BrushButton):
    def __init__(self, pos, manager, parent_element, container):
        super(EntranceButton, self).__init__(pos, "Entrance", manager, parent_element, container, "#"+__class__.__name__, BrushType.ENTRANCE)


class CashRegisterButton(BrushButton):
    def __init__(self, pos, manager, parent_element, container):
        super(CashRegisterButton, self).__init__(pos, "Cash Register", manager, parent_element, container, "#"+__class__.__name__, BrushType.CASH_REGISTER)


class MapElementToolbar(UIWindow):
    def __init__(self, position, ui_manager, editor):
        super(MapElementToolbar, self).__init__(pygame.Rect(position, (210, 250)), ui_manager,
                                                window_display_title="Elements toolbar", object_id="#element_toolbar")
        self.__editor = editor

        self.__buttons = []
        self.__buttons.append(ShelfButton((5, 5), ui_manager, self, self))
        self.__buttons.append(EntranceButton((5, 35), ui_manager, self, self))
        self.__buttons.append(CashRegisterButton((5, 65), ui_manager, self, self))

    def process_event(self, event: pygame.event.Event) -> bool:
        out = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button in self.__buttons:
                    button.unselect()
                    if event.ui_element == button:
                        logging.debug('selected brash:{}'.format(event.ui_element.type))
                        self.__editor.select_brash(event.ui_element.type)
                        event.ui_element.select()
                        out = True
        return out
