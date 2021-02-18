import pygame
import pygame_gui
import logging

logging.basicConfig(level=logging.DEBUG)

BACKGROUND_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)


def main():
    size = (800, 600)
    clock = pygame.time.Clock()
    fps = 60
    is_running = True
    edit_mode = False

    pygame.init()
    pygame.display.set_caption("Map Editor")
    screen = pygame.display.set_mode(size)
    screen.fill(BACKGROUND_COLOR)

    gui_manager = pygame_gui.UIManager(size)

    created_rectangles = []
    counter = 0
    tmp_rec = None

    while is_running:
        screen.fill(BACKGROUND_COLOR)
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                edit_mode = True
                if tmp_rec is None:
                    counter += 1
                    tmp_rec = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
            if event.type == pygame.MOUSEBUTTONUP:
                edit_mode = False
                if tmp_rec is not None:
                    created_rectangles.append(tmp_rec.copy())
                tmp_rec = None
            if edit_mode == True and event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                height = pos[1] - tmp_rec.top
                width = pos[0] - tmp_rec.left
                tmp_rec.height = height
                tmp_rec.width = width

            gui_manager.process_events(event)

        for rect in created_rectangles:
            pygame.draw.rect(screen, GREEN, rect)
        if tmp_rec is not None:
            print(u'tmp_rec.pos={}'.format((tmp_rec.top, tmp_rec.left, tmp_rec.bottom, tmp_rec.right)))
            pygame.draw.rect(screen, GREEN, tmp_rec)

        gui_manager.update(time_delta)
        gui_manager.draw_ui(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()