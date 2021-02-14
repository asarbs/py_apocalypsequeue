from datetime import datetime
import pygame
import logging
import random

from world import build_sim_world, build_shop_shelf
from console_args import CONSOLE_ARGS
from system.pathfinding import build_nav_graph
from data import Data
from system import Meter


# parameters/globals
screen_size = width, height = Meter(250).get_pixels(), Meter(250).get_pixels()
play: bool = True
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
random.seed(datetime.now())


# constants
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
    global play
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play = not play
    if play:
        get_infection(client_list, data, time)
        for client in client_list:
            client.move_and_bounce()
            list_of_collided_clients = pygame.sprite.spritecollide(client, client_list, False)
            list_of_collided_shelf = pygame.sprite.spritecollide(client, shop_shelf_lists, False)
            logging.debug("client {} collided with {} clients".format(client, len(list_of_collided_clients)))
            for c in list_of_collided_clients:
                if client is not c:
                    client.move_randomly()
            for c in list_of_collided_shelf:
                client.move_aside(c)

            if client.isInQueue():
                client.getInLine()


def draw_cash_register(screen_to_draw, cash_register_list):
    for cash_register in cash_register_list:
        cash_register.draw(screen_to_draw)


def print_stats(client_list, num_of_repetition):
    infected = 0
    for c1 in client_list:
        if c1.isInfected():
            infected += 1
    logging.info('rep:{}, infected {} of {} clients'.format(num_of_repetition, infected, len(client_list)))


def draw_shop_shelf(screen_to_draw, shelf_list):
    for shelf in shelf_list:
        shelf.draw(screen_to_draw)


def main():
    data = Data()

    for num_of_repetition in range(0, CONSOLE_ARGS.num_of_repeat_max, 1):
        shelf_list = build_shop_shelf(width, height)
        nav_graph_array, nav_graph_dic, nav_graph_group = build_nav_graph(screen_size, shelf_list.sprites())
        cash_register_list, clients_lists = build_sim_world(nav_graph_array, width, height)
        time_step = 0
        while time_step < CONSOLE_ARGS.time_step_max:
            data.addTimeData(time_step)
            main_event_loop(clients_lists, shelf_list, data, time_step)
            # Fill the background with white
            screen.fill(BACKGROUND_COLOR)

            draw_world(cash_register_list, clients_lists, shelf_list)
            print_stats(clients_lists, num_of_repetition)
            data.addStats(clients_lists, time_step)

            time_step += 1

            # Flip the display
            logging.debug('fps:{}'.format(clock.get_fps()))
            clock.tick(CONSOLE_ARGS.fps)
            # for node in nav_graph_group:
            #     node.draw(screen)
            if CONSOLE_ARGS.play_simulation is True:
                pygame.display.update()

    screen.fill(BACKGROUND_COLOR)
    draw_shop_shelf(screen, shelf_list)
    draw_cash_register(screen, cash_register_list)

    data.dump(screen)
    pygame.quit()


def draw_world(cash_register_list, clients_lists, shelf_list):
    draw_shop_shelf(screen, shelf_list)
    clients_lists.draw(screen)
    draw_cash_register(screen, cash_register_list)


if __name__ == "__main__":
    main()
