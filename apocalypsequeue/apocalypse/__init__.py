from numpy.distutils.fcompiler.g95 import G95FCompiler

from Vector import Vector
import pygame
import random
import logging
import os

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Client:
    count = 1
    people_img = pygame.image.load("icons/person.png")
    zombie_img = pygame.image.load("icons/zombie.png")

    def __init__(self, target_cash_register, infected=False, position=Vector(0, 0), idName="0"):
        self.__id = Client.count
        self.__position = position
        self.__target_cash_register = target_cash_register
        self.__infected = infected
        Client.count += 1

    def __str__(self):
        return u'id:{}'.format(self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    def move_and_bounce(self):
        destination = self.__target_cash_register.getPosVector() - self.__position
        if destination.getLength() > 5:
            vec_to = destination.getUnitVecotr() * 5.0
            self.__position += vec_to

    def getPos(self):
        return int(self.__position.getX()), int(self.__position.getY())

    def getClientDistance(self, other_client):
        return (self.__position - other_client.__position).getLength()

    def draw(self, screen):
        logging.debug('Client.draw:{}, pos={}, infected={}'.format(self.__id, self.getPos(), self.__infected))
        img = Client.zombie_img if self.__infected else Client.people_img
        screen.blit(img, self.getPos())

    def isInfected(self):
        return self.__infected

    def infect(self):
        logging.warning("Client {} get infection".format(self.__id))
        self.__infected = True


class CashRegister:
    count = 1
    cs_img = pygame.image.load("icons/cr.png")

    def __init__(self, position=Vector(0, 0)):
        self.__id = CashRegister.count
        self.__position = position
        CashRegister.count += 1

    def getPos(self):
        return int(self.__position.getX()), int(self.__position.getY())

    def getPosVector(self):
        return self.__position

    def draw(self, screen):
        logging.debug('CashRegister.draw:{}'.format(self.__id))
        screen.blit(CashRegister.cs_img, self.getPos())
