from system.Vector import Vector
from system import Meter
import pygame
import random
import logging
from console_args import CONSOLE_ARGS

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Client(pygame.sprite.Sprite):
    count = 1
    people_img = pygame.image.load("icons/person_big.png")
    zombie_img = pygame.image.load("icons/zombie_big.png")
    #step_size = Meter(0.4).get_pixels()
    #random_direction = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    size = (Meter(1.5).get_pixels(), Meter(1.5).get_pixels())

    def __init__(self, target_cash_register, start_node, path, infected=False, canInfect=False, idName="0"):
        pygame.sprite.Sprite.__init__(self)
        self.__id = Client.count
        self.__position = start_node.get_pos()
        self.__target_cash_register_node = target_cash_register
        self.__infected = infected
        self.__canInfect = canInfect
        self.__isInQueue = False
        self.__timeInInfectionArea = {}
        self.__path = path
        for p in path:
            p.mark_path()
        self.__step_on_path = 0
        for i in range (0, CONSOLE_ARGS.inf_distance+1):
            self.__timeInInfectionArea[i] = 0

        self.__set_image()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.__position.getX(), self.__position.getY())

        Client.count += 1

    def __set_image(self):
        self.image = Client.zombie_img if self.__infected else Client.people_img
        self.image = pygame.transform.scale(self.image, Client.size)

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def move(self):
        if self.__step_on_path < len(self.__path) - 1:
            self.__step_on_path += 1
            to_vec = self.__path[self.__step_on_path].get_pos_vector() - self.__position
            self.__move(to_vec)
            logging.debug("position = {}; rect=[{},{}]".format(str(self.__position), self.rect.x, self.rect.y))

    def __move(self, vec_to):
        vec_to.round()
        logging.debug("vec_to = {}".format(str(vec_to)))
        self.__position += vec_to
        self.rect.move_ip(vec_to.getX(), vec_to.getY())

    def in_cash_register(self):
        return self.__step_on_path == len(self.__path) - 1

    # def move_randomly(self):
    #     if self.__isInQueue:
    #         return
    #     vector = Vector(random.choice(Client.random_direction), random.choice(Client.random_direction))
    #     vec_to = vector.getUnitVecotr() * Client.step_size
    #     self.__move(vec_to)

    # def move_aside(self, shelf):
    #     vec_of_y_left = shelf.rect.left - self.__position.getX()
    #     vec_of_y_right = shelf.rect.right - self.__position.getX()
    #
    #     if abs(vec_of_y_left) < abs(vec_of_y_right):
    #         vec_to = Vector(vec_of_y_left - 10, 0)
    #         self.__move(vec_to)
    #     else:
    #         vec_to = Vector(vec_of_y_right, 0)
    #         self.__move(vec_to)
    #
    #     logging.debug("client:{}, shelf".format(self.__id, shelf))

    def getPos(self):
        return int(self.__position.getX()), int(self.__position.getY())

    def getClientDistance(self, other_client):
        return (self.__position - other_client.__position).getLength()

    def isInfected(self):
        return self.__infected

    def canInfect(self):
        return self.__canInfect

    def try_infect(self, distance):
        self.__timeInInfectionArea[round(distance)] += 1
        infection_threshold = self.__calc_infection_threshold()
        if infection_threshold > CONSOLE_ARGS.infection_threshold:
            logging.warning("Client {} get infection with infection_threshold={}".format(self.__id, infection_threshold))
            self.__infected = True
            self.__set_image()
            return True
        return False

    def __calc_infection_threshold(self):
        sum = -1
        for k,v in self.__timeInInfectionArea.items():
            sum += v * (1 - (k / len(self.__timeInInfectionArea)))
        return sum

    def isInQueue(self):
        destination = self.__target_cash_register_node.getPosVector() - self.__position
        return destination.getLength() < 4

    def getInLine(self):
        self.__isInQueue = True
        self.__target_cash_register_node.setInQueue()

    def standingInQueue(self):
        return self.__isInQueue


class CashRegister(pygame.sprite.Sprite):
    count = 1
    cs_img = pygame.image.load("icons/cr.png")
    queue_step = Vector(0, 10)

    def __init__(self, node):
        pygame.sprite.Sprite.__init__(self)
        self.__id = CashRegister.count
        self.__nag_graph_node = node
        CashRegister.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def getPos(self):
        return int(self.__nag_graph_node.get_pos().getX()), int(self.__nag_graph_node.get_pos().getY())

    def getPosVector(self):
        return self.__nag_graph_node.get_pos()
    #
    # def setInQueue(self):
    #     self.__queue = self.__queue - CashRegister.queue_step

    def draw(self, screen):
        logging.debug('CashRegister.draw:{}'.format(self.__id))
        screen.blit(CashRegister.cs_img, (self.__nag_graph_node.get_pos().getX(), self.__nag_graph_node.get_pos().getY()))

    def get_nav_graph_id(self):
        return self.__nag_graph_node.get_id()

class ShopShelf(pygame.sprite.Sprite):
    count = 1

    def __init__(self, position=Vector(0, 0), size=(40, 200)):
        pygame.sprite.Sprite.__init__(self)
        if not isinstance(size[0], Meter) or not isinstance(size[1], Meter):
            raise ValueError("invalid type for size of {}".format(__class__))

        self.__id = ShopShelf.count
        pixel_size = (size[0].get_pixels(), size[1].get_pixels())
        self.rect = pygame.Rect(position.getTuple(), pixel_size)
        ShopShelf.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    def draw(self, screen):
        logging.debug('ShopShelf.draw:{}'.format(self.__id))
        pygame.draw.rect(screen, GREEN, self.rect)
