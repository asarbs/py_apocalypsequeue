from numpy.distutils.fcompiler.g95 import G95FCompiler

from Vector import Vector
import pygame
import random
import logging
import math

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Client(pygame.sprite.Sprite):
    count = 1
    people_img = pygame.image.load("icons/person.png")
    zombie_img = pygame.image.load("icons/zombie.png")
    step_size = 5.0
    random_direction = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    def __init__(self, target_cash_register, infected=False, canInfect=False, position=Vector(0, 0), idName="0"):
        pygame.sprite.Sprite.__init__(self)
        self.__id = Client.count
        self.__position = position
        self.__target_cash_register = target_cash_register
        self.__infected = infected
        self.__canInfect = canInfect
        self.__isInQueue = False

        self.image = Client.zombie_img if self.__infected else Client.people_img
        self.rect = self.image.get_rect()
        self.rect.move_ip(position.getX(), position.getY())

        Client.count += 1

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def move_and_bounce(self):
        if self.__isInQueue:
            return
        destination = self.__target_cash_register.getPosVector() - self.__position
        if destination.getLength() > 5:
            vec_to = destination.getUnitVecotr() * Client.step_size
            self.__move(vec_to)

        logging.debug("position = {}; rect=[{},{}]".format(str(self.__position), self.rect.x, self.rect.y))

    def __move(self, vec_to):
        vec_to.round()
        logging.debug("vec_to = {}".format(str(vec_to)))
        self.__position += vec_to
        self.rect.move_ip(vec_to.getX(), vec_to.getY())

    def move_randomly(self):
        if self.__isInQueue:
            return
        vector = Vector(random.choice(Client.random_direction), random.choice(Client.random_direction))
        vec_to = vector.getUnitVecotr() * Client.step_size
        self.__move(vec_to)

    def move_aside(self, shelf):
        vec_of_y_left = shelf.rect.left - self.__position.getX()
        vec_of_y_right = shelf.rect.right - self.__position.getX()

        if abs(vec_of_y_left) < abs(vec_of_y_right):
            vec_to = Vector(vec_of_y_left - 10, 0)
            self.__move(vec_to)
        else:
            vec_to = Vector(vec_of_y_right, 0)
            self.__move(vec_to)


        logging.debug("client:{}, shelf".format(self.__id, shelf))

    def getPos(self):
        return int(self.__position.getX()), int(self.__position.getY())

    def getClientDistance(self, other_client):
        return (self.__position - other_client.__position).getLength()

    def isInfected(self):
        return self.__infected

    def canInfect(self):
        return self.__canInfect

    def infect(self):
        logging.warning("Client {} get infection".format(self.__id))
        self.__infected = True
        self.image = Client.zombie_img if self.__infected else Client.people_img

    def isInQueue(self):
        destination = self.__target_cash_register.getPosVector() - self.__position
        return destination.getLength() < 4

    def getInLine(self):
        self.__isInQueue = True
        self.__target_cash_register.setInQueue()

    def standingInQueue(self):
        return self.__isInQueue


class CashRegister(pygame.sprite.Sprite):
    count = 1
    cs_img = pygame.image.load("icons/cr.png")
    queue_step = Vector(0, 10)

    def __init__(self, position=Vector(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.__id = CashRegister.count
        self.__position = position
        self.__queue = position
        CashRegister.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def getPos(self):
        return int(self.__queue.getX()), int(self.__queue.getY())

    def getPosVector(self):
        return self.__queue

    def setInQueue(self):
        self.__queue = self.__queue - CashRegister.queue_step

    def draw(self, screen):
        logging.debug('CashRegister.draw:{}'.format(self.__id))
        screen.blit(CashRegister.cs_img, (self.__position.getX(), self.__position.getY()))


class ShopShelf(pygame.sprite.Sprite):
    count = 1

    def __init__(self, position=Vector(0, 0), size=(40, 200)):
        pygame.sprite.Sprite.__init__(self)
        self.__id = ShopShelf.count
        self.rect = pygame.Rect(position.getTuple(), size)
        ShopShelf.count += 1

    def __hash__(self):
        return hash(str(__class__) * self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    def draw(self, screen):
        logging.debug('ShopShelf.draw:{}'.format(self.__id))
        pygame.draw.rect(screen, GREEN, self.rect)
