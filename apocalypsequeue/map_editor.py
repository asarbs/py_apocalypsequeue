from map_editor import MapEditor
from map_editor.editor_console_args import EDITOR_CONSOLE_ARGS
import logging

logging.basicConfig(level=EDITOR_CONSOLE_ARGS.loglevel)


def main():
    map_editor = MapEditor()
    map_editor.main_loop()

if __name__ == "__main__":
    main()