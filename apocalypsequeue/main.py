from datetime import datetime
import pygame
import logging
import random
import argparse

from apocalypse import Client
from apocalypse import CashRegister
from apocalypse import ShopShelf
from console_args import CONSOLE_ARGS
from data import Data
from Vector import Vector



# parameters/globals
screen_size = width, height = 1000, 800
play = True
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
random.seed(datetime.now())


#constants
BACKGROUND_COLOR = (228, 228, 228)

# logging configuration
logging.basicConfig(level=CONSOLE_ARGS.loglevel)

def get_infection(client_list, data, time):
    for c1 in client_list:
        for c2 in client_list:
            if not c1 == c2 and not c1.isInfected():
                distance = c1.getClientDistance(c2)
                if c2.canInfect() and distance < CONSOLE_ARGS.inf_distance:
                    data.addContactTime(distance)
                    if c1.try_infect(distance):
                        data.add_infection_params(c1.getPos(), time)


def main_event_loop(client_list, shop_shelf_lists, data, time):
    global running
    global play
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play = not play
    if play:
        get_infection(client_list, data, time)
        for client in client_list:
            client.move_and_bounce()
            list_of_collided_clients = pygame.sprite.spritecollide(client, client_list, False)
            list_of_collided_shelf =  pygame.sprite.spritecollide(client, shop_shelf_lists, False)
            logging.debug("client {} collided with {} clients".format(client, len(list_of_collided_clients)))
            for c in list_of_collided_clients:
                if client is not c:
                    client.move_randomly()
            for c in list_of_collided_shelf:
                client.move_aside(c)

            if client.isInQueue():
                client.getInLine()


def draw_cash_register(screen, cash_register_list):
    for cash_register in cash_register_list:
        cash_register.draw(screen)


def print_stats(client_list, num_of_repetition):
    infected = 0
    for c1 in client_list:
        if c1.isInfected():
            infected += 1
    logging.info('rep:{}, infected {} of {} clients'.format(num_of_repetition, infected, len(client_list)))


def stopsimulation(client_list):
    total = len(client_list)
    counter = 0
    for c1 in client_list:
        if c1.standingInQueue():
            counter += 1
    return total == counter


def draw_shop_shels(screen, shelf_list):
    for shelf in shelf_list:
        shelf.draw(screen)


def main():
    data = Data()

    num_of_repeat = CONSOLE_ARGS.num_of_repeat_max
    for num_of_repetition in range(0, num_of_repeat, 1):

        cash_register_list = build_cash_registers()
        clients_lists = build_client_list(cash_register_list)
        shelf_list = build_shop_shelf(clients_lists)
        time_step = 0
        while time_step < CONSOLE_ARGS.time_step_max:
            data.addTimeData(time_step)
            main_event_loop(clients_lists, shelf_list, data, time_step)
            # Fill the background with white
            screen.fill(BACKGROUND_COLOR)

            draw_shop_shels(screen, shelf_list)
            clients_lists.draw(screen)
            draw_cash_register(screen, cash_register_list)
            print_stats(clients_lists, num_of_repetition)
            data.addStats(clients_lists, time_step)

            time_step += 1

            # Flip the display
            logging.debug('fps:{}'.format(clock.get_fps()))
            clock.tick(CONSOLE_ARGS.fps)
            if CONSOLE_ARGS.play_simulation is True:
                pygame.display.update()

    screen.fill(BACKGROUND_COLOR)
    draw_shop_shels(screen, shelf_list)
    draw_cash_register(screen, cash_register_list)

    data.dump(screen)
    pygame.quit()


def build_client_list(cash_register_list):
    clients_lists = pygame.sprite.Group()
    for i in range(0, CONSOLE_ARGS.number_of_clients):
        x = random.randrange(0, width, 1)
        y = random.randrange(0, (height / 2), 1)
        infected = random.random() < CONSOLE_ARGS.init_infec
        canInfect = infected
        client = Client(position=Vector(x, y), infected=infected, canInfect=canInfect,
                        target_cash_register=random.choice(cash_register_list)),
        clients_lists.add(client)
    return clients_lists


def build_cash_registers():
    space_size = ( width / 7 ) - 15
    return [
        CashRegister(position=Vector(1 * space_size, (height - 15))),
        CashRegister(position=Vector(2 * space_size, (height - 15))),
        CashRegister(position=Vector(3 * space_size, (height - 15))),
        CashRegister(position=Vector(4 * space_size, (height - 15))),
        CashRegister(position=Vector(5 * space_size, (height - 15))),
        CashRegister(position=Vector(6 * space_size, (height - 15))),
        CashRegister(position=Vector(7 * space_size, (height - 15)))
    ]


def build_shop_shelf(clients_lists):
    num_of_shelfs = 6
    shop_shelf_lists = pygame.sprite.Group()
    space_size = (width / num_of_shelfs) - 20
    for i in range(1,num_of_shelfs + 1):
        ss = ShopShelf(position=Vector(i * space_size, (height / 4)), size=(40, 400)),
        shop_shelf_lists.add(ss)
    return shop_shelf_lists


if __name__ == "__main__":
    main()
