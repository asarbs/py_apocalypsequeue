import random
import pygame
import math
import logging
import datetime
from apocalypse import Client, CashRegister, ShopShelf
from console_args import CONSOLE_ARGS
from system.Vector import Vector
from system.pathfinding import dijkstras_algorithm
from system import Meter


def build_sim_world(nav_graph_array, nav_graph_dic, width, height):
    cash_register_list = __build_cash_registers(nav_graph_array, width, height)
    clients_lists = __build_client_list(nav_graph_array, nav_graph_dic, cash_register_list, width, height)
    return cash_register_list, clients_lists


def __build_client_list(nav_graph_array, nav_graph_dic, cash_register_list, width, height):
    clients_lists = pygame.sprite.Group()
    nav_graph_size = len(nav_graph_array)
    nav_graph_last_row = nav_graph_size - 1

    for i in range(0, CONSOLE_ARGS.number_of_clients):
        x = random.randrange(0, nav_graph_last_row, 1)
        y = random.randrange(0, 5, 1)
        infected = random.random() < CONSOLE_ARGS.init_infec
        canInfect = infected
        start_node = nav_graph_array[x][y]
        target_cash_register = random.choice(cash_register_list)
        t1 = datetime.datetime.now()
        path = dijkstras_algorithm(nav_graph_dic, start_node, target_cash_register)
        t2 = datetime.datetime.now()
        diff = t2-t1
        client = Client(start_node=start_node, path=path, infected=infected, canInfect=canInfect, target_cash_register=target_cash_register),
        logging.info("Client {} created path={}".format(client[0],diff))
        clients_lists.add(client)
    return clients_lists


def __build_cash_registers(nav_graph_array, width, height):
    num_of_cash_registers = 7
    nav_graph_size = len(nav_graph_array)
    nav_graph_last_row = nav_graph_size - 1
    step = math.floor(nav_graph_size / 7)

    cash_registers = []
    nav_graph_array_col = 0
    for x in range(0, num_of_cash_registers, 1):
        node = nav_graph_array[nav_graph_array_col][nav_graph_last_row]
        cash_registers.append(CashRegister(node=node))
        nav_graph_array_col += step
    return cash_registers


def build_shop_shelf(width, height):
    num_of_shelves = 6
    shop_shelf_lists = pygame.sprite.Group()
    space_size = (width / num_of_shelves) - 20

    size = (Meter(2), Meter(50))

    for i in range(1, num_of_shelves + 1):
        ss = ShopShelf(position=Vector(i * space_size, (height / 4)), size=size),
        shop_shelf_lists.add(ss)

    ss = ShopShelf(position=Vector(50, 600), size=(Meter(150), Meter(2)))
    shop_shelf_lists.add(ss)
    return shop_shelf_lists