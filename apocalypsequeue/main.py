import pygame
import logging
import random
from datetime import datetime

from apocalypse import Client
from apocalypse import CashRegister
from apocalypse import ShopShelf
from Vector import Vector

logging.basicConfig(level=logging.INFO)

now = datetime.now() # current date and time

date_time = now.strftime("%Y%m%d_%H%M%S")
filename = '{}.csv'.format(date_time)
outdate = {}

# parameters:
screen_size = width, height = 1000, 800
play = True
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
random.seed(now)

BACKGROUND_COLOR = (228, 228, 228)

FPS = 60
number_of_clients = 40


def get_infection(client_list):
    for c1 in client_list:
        for c2 in client_list:
            if not c1 == c2 and not c1.isInfected():
                distance = c1.getClientDistance(c2)
                if c2.isInfected() and c2.canInfect() and distance < 15 and random.random() < 0.1:
                    c1.infect()


def main_event_loop(client_list, shop_shelf_lists):
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
            list_of_collided_clients = pygame.sprite.spritecollide(client, client_list, False)
            list_of_collided_shelf =  pygame.sprite.spritecollide(client, shop_shelf_lists, False)
            logging.debug("client {} collided with {} clients".format(client,len(list_of_collided_clients)))
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


def getStats(clients_lists, time_step):
    global outdate

    if time_step not in outdate:
        outdate[time_step] = {"time_step": 0, "number_of_infected": 0, "number_of_new_infected": 0, "number_of_clients_in_queue": 0, "number_of_healthy": 0}
    outdate[time_step]["time_step"] += 1
    for c in clients_lists:
        if c.isInfected():
            outdate[time_step]["number_of_infected"] += 1
            if not c.canInfect():
                outdate[time_step]["number_of_new_infected"] += 1
        else:
            outdate[time_step]["number_of_healthy"] += 1
        if c.standingInQueue():
            outdate[time_step]["number_of_clients_in_queue"] += 1





def draw_shop_shels(screen, shelf_list):
    for shelf in shelf_list:
        shelf.draw(screen)

def main():
    global outdate
    global number_of_clients
    num_of_repeat = 100
    for num_of_repetition in range(0, num_of_repeat, 1):

        cash_register_list = build_cash_registers()
        clients_lists = build_client_list(cash_register_list)
        shelf_list = build_shop_shelf(clients_lists)
        time_step = 0
        while time_step < 400:
            main_event_loop(clients_lists, shelf_list)
            # Fill the background with white
            screen.fill(BACKGROUND_COLOR)

            draw_shop_shels(screen, shelf_list)
            clients_lists.draw(screen)
            draw_cash_register(screen, cash_register_list)
            print_stats(clients_lists, num_of_repetition)
            getStats(clients_lists, time_step)

            time_step += 1

            # Flip the display
            logging.debug('fps:{}'.format(clock.get_fps()))
            clock.tick(FPS)
            #pygame.display.update()

    save_data_to_file(outdate)
    pygame.quit()


def save_data_to_file(outdate):
    csvfile = open(filename, "w+")
    csvfile.write(
        "time step; num_of_timesteps;number of infected; number of new infected;number of healthy; number of clients in queue\n")
    for time_step in outdate:
        # {"number_of_infected": 0, "number_of_new_infected": 0, "number_of_clients_in_queue": 0, "number_of_healthy": 0}
        line = '{};{};{:.2f};{:.2f};{:.2f};{:.2f}\n'.format(time_step,
                                                            outdate[time_step]["time_step"],
                                                            (outdate[time_step]["number_of_infected"] /
                                                             outdate[time_step]["time_step"]),
                                                            (outdate[time_step]["number_of_new_infected"] /
                                                             outdate[time_step]["time_step"]),
                                                            (outdate[time_step]["number_of_healthy"] /
                                                             outdate[time_step]["time_step"]),
                                                            (outdate[time_step]["number_of_clients_in_queue"] /
                                                             outdate[time_step]["time_step"])
                                                            )
        csvfile.write(line.replace(".", ","))
    csvfile.close()


def build_client_list(cash_register_list):
    clients_lists = pygame.sprite.Group()
    for i in range(0, number_of_clients):
        x = random.randrange(0, width, 1)
        y = random.randrange(0, (height / 2), 1)
        infected = random.random() < 0.2
        canInfect = infected
        client = Client(position=Vector(x, y), infected=infected, canInfect=canInfect,
                        target_cash_register=random.choice(cash_register_list)),
        clients_lists.add(client)
    return clients_lists


def build_cash_registers():
    space_size = ( width / 3 ) - 50
    return [
        CashRegister(position=Vector(1 * space_size, (height - 15))),
        CashRegister(position=Vector(2 * space_size, (height - 15))),
        CashRegister(position=Vector(3 * space_size, (height - 15)))
    ]

def build_shop_shelf(clients_lists):
    num_of_shelfs = 6
    shop_shelf_lists = pygame.sprite.Group()
    space_size = (width / num_of_shelfs) - 20
    for i in range(1,num_of_shelfs + 1):
        ss = ShopShelf(position=Vector(i * space_size, (height / 2))),
        shop_shelf_lists.add(ss)
    return shop_shelf_lists


if __name__ == "__main__":
    main()
