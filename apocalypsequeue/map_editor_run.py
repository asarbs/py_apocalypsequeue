from map_editor import MapEditor
from console_args import CONSOLE_ARGS
import logging

logging.basicConfig(level=CONSOLE_ARGS.loglevel)


def main():
    map_editor = MapEditor()
    map_editor.main_loop()


if __name__ == "__main__":
    main()