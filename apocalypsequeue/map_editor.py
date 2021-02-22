import pygame
import pygame_gui
import logging
from map_editor.FileBrowser import FileBrowser
from map_editor.console_args import EDITOR_CONSOLE_ARGS
from map_editor import MapEditor
logging.basicConfig(level=EDITOR_CONSOLE_ARGS.loglevel)


BACKGROUND_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)


def main():
    map_editor = MapEditor()
    map_editor.main_loop()


if __name__ == "__main__":
    main()