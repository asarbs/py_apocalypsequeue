import random
import pygame
from apocalypse import Client, CashRegister, ShopShelf
from console_args import CONSOLE_ARGS
from system.Vector import Vector
from system import Meter


def build_sim_world(width, height):
    cash_register_list = __build_cash_registers(width, height)
    clients_lists = __build_client_list(cash_register_list, width, height)
    shelf_list = __build_shop_shelf(clients_lists, width, height)
    return cash_register_list, clients_lists, shelf_list


def __build_client_list(cash_register_list, width, height):
    clients_lists = pygame.sprite.Group()
    for i in range(0, CONSOLE_ARGS.number_of_clients):
        x = random.randrange(0, width, 1)
        y = random.randrange(0, (height / 2), 1)
        infected = random.random() < CONSOLE_ARGS.init_infec
        canInfect = infected
        client = Client(position=Vector(x, y), infected=infected, canInfect=canInfect, target_cash_register=random.choice(cash_register_list)),
        clients_lists.add(client)
    return clients_lists


def __build_cash_registers(width, height):
    space_size = (width / 7) - 15
    return [
        CashRegister(position=Vector(1 * space_size, (height - 15))),
        CashRegister(position=Vector(2 * space_size, (height - 15))),
        CashRegister(position=Vector(3 * space_size, (height - 15))),
        CashRegister(position=Vector(4 * space_size, (height - 15))),
        CashRegister(position=Vector(5 * space_size, (height - 15))),
        CashRegister(position=Vector(6 * space_size, (height - 15))),
        CashRegister(position=Vector(7 * space_size, (height - 15)))
    ]


def __build_shop_shelf(clients_lists, width, height):
    num_of_shelves = 6
    shop_shelf_lists = pygame.sprite.Group()
    space_size = (width / num_of_shelves) - 20

    size = (Meter(4), Meter(100))

    for i in range(1, num_of_shelves + 1):
        ss = ShopShelf(position=Vector(i * space_size, (height / 4)), size=size),
        shop_shelf_lists.add(ss)
    return shop_shelf_lists