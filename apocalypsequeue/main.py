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

BACKGROUND_COLOR = (228, 228, 228)

FPS = 60


def get_infection(client_list):
    for c1 in client_list:
        for c2 in client_list:
            if not c1 == c2 and not c1.isInfected():
                distance = c1.getClientDistance(c2)
                if c2.isInfected() and distance < 15 and random.random() < 0.1:
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
            client.move_and_bounce(client_list)
            list_of_collided_clients = pygame.sprite.spritecollide(client, client_list, False)
            logging.debug("client {} collided with {} clients".format(client,len(list_of_collided_clients)))
            if len(list_of_collided_clients) > 0:
                client.move_randomly()

            if client.isInQueue():
                client.getInLine()



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
    cash_register_list = build_cash_registers()

    clients_lists = build_client_list(cash_register_list)

    while running:

        main_event_loop(clients_lists)
        # Fill the background with white
        screen.fill(BACKGROUND_COLOR)

        clients_lists.draw(screen)

        draw_cash_register(screen, cash_register_list)
        print_stats(clients_lists)
        # Flip the display
        logging.debug('fps:{}'.format(clock.get_fps()))
        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()


def build_client_list(cash_register_list):
    clients_lists = pygame.sprite.Group()
    for x in range(0, 40):
        x = random.randrange(0, width, 1)
        y = random.randrange(0, (height / 2), 1)
        infected = random.random() < 0.2
        client = Client(position=Vector(x, y), infected=infected,
                        target_cash_register=random.choice(cash_register_list)),
        clients_lists.add(client)
    return clients_lists


def build_cash_registers():
    return [
        CashRegister(position=Vector((width / 2), (height - 15))),
        CashRegister(position=Vector((width / 3), (height - 15))),
        CashRegister(position=Vector(2 * (width / 3), (height - 15)))
    ]


if __name__ == "__main__":
    main()
