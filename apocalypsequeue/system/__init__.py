from system.Vector import Vector


class Meter:
    __scale = 8

    def __init__(self, m):
        self.__num_of_meters = m
        self.__pixels = round(m * Meter.__scale)

    def __str__(self):
        return u'{}m'.format(self.__num_of_meters)

    def __add__(self, other):
        m = self.__num_of_meters + other.__num_of_meters
        return Meter(m)

    def __sub__(self, other):
        m = self.__num_of_meters - other.__num_of_meters
        return Meter(m)

    def __mul__(self, other):
        m = self.__num_of_meters * other
        return Meter(m)

    def __pow__(self, power, modulo=None):
        m = self.__num_of_meters ** power
        return Meter(m)

    def __truediv__(self, other):
        m = self.__num_of_meters / other
        return Meter(m)

    def __lt__(self, other):
        return self.__num_of_meters < other.__num_of_meters

    def __le__(self, other):
        return self.__num_of_meters <= other.__num_of_meters

    def __eq__(self, other):
        return self.__num_of_meters == other.__num_of_meters

    def __ne__(self, other):
        return self.__num_of_meters != other.__num_of_meters

    def __gt__(self, other):
        return self.__num_of_meters > other.__num_of_meters

    def __ge__(self, other):
        return self.__num_of_meters >= other.__num_of_meters

    def get_pixels(self):
        return self.__pixels

