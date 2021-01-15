import pygame
import logging
import random
from apocalypse import Client
from apocalypse import CashRegister
from Vector import Vector

pygame.init()

logging.basicConfig(level=logging.INFO)


# parameters:
screen_size = width, height = 1000, 800
running = True
play = True
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)

FPS = 60


def get_infection(client_list):
    for c1 in client_list:
        for c2 in client_list:
            if not c1 == c2 and not c1.isInfected():
                distance = c1.getClientDistance(c2)
                if c2.isInfected() and distance < 10 and random.random() < 0.1:
                    c1.infect()

def main_event_loop(client_list):
    global running
    global play
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play = not play
    if play:
        get_infection(client_list)
        for client in client_list:
            client.move_and_bounce()


def draw_clients(screen, client_list):
    for client in client_list:
        client.draw(screen)


def draw_cash_register(screen, cash_register_list):
    for cash_register in cash_register_list:
        cash_register.draw(screen)


def print_stats(client_list):
    infected = 0;
    for c1 in client_list:
        if c1.isInfected():
            infected += 1
    logging.info('infected {} of {} clients'.format(infected, len(client_list)))

def main():
    cash_register_list = [
        CashRegister(position=Vector((width / 2), (height - 15))),
        CashRegister(position=Vector((width / 3), (height - 15))),
        CashRegister(position=Vector(2 * (width / 3), (height - 15)))
                          ]
    client_list = []

    for x in range(1,20):
        x = random.randrange(0, (width / 2), 1)
        y = random.randrange(0, (height / 2), 1)
        infected = random.random() < 0.2
        client_list.append(
            Client(position=Vector(x, y), infected=infected, target_cash_register=random.choice(cash_register_list)),
        )

    while running:

        main_event_loop(client_list)
        # Fill the background with white
        screen.fill(BLACK)
        # Draw a solid blue circle in the center
        draw_clients(screen, client_list)
        draw_cash_register(screen, cash_register_list)
        print_stats(client_list)
        # Flip the display
        logging.debug('fps:{}'.format(clock.get_fps()))
        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
