import pygame
import pygame_gui

BACKGROUND_COLOR = (0, 0, 0)


def main():
    size = (800, 600)
    clock = pygame.time.Clock()
    fps = 60
    is_running = True

    pygame.init()
    pygame.display.set_caption("Map Editor")
    screen = pygame.display.set_mode(size)
    screen.fill(BACKGROUND_COLOR)

    gui_manager = pygame_gui.UIManager(size)

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text="Hello World", manager=gui_manager)

    while is_running:

        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        print("Hello World")
            gui_manager.process_events(event)

        gui_manager.update(time_delta)
#        screen.blit(BACKGROUND_COLOR, (0, 0))
        gui_manager.draw_ui(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()