import math


class Vector(object):
    def __init__(self, x:int, y:int):
        self.__x = x
        self.__y = y

    def __str__(self):
        return u'[{},{}]'.format(self.__x, self.__y)

    def __add__(self, o):
        return Vector(self.__x + o.__x, self.__y + o.__y)

    def __sub__(self, o):
        return Vector(self.__x - o.__x, self.__y - o.__y)

    def __mul__(self, o):
        if isinstance(o, float) or isinstance(0, int):
            return Vector(o * self.__x, o * self.__y)
        elif isinstance(o, Vector):
            out = self.__x * o.__x + self.__y * o.__y
            return out
        raise TypeError("input must be a floar or Vector")

    def getList(self):
        return [self.__x, self.__y]

    def getTuple(self):
        return (self.__x, self.__y)

    def getLength(self):
        return math.sqrt(self.__x ** 2 + self.__y ** 2)

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getUnitVecotr(self):
        length = self.getLength()
        return Vector(x=(self.__x/length), y=(self.__y/length))

    def round(self):
        self.__x = round(self.__x)
        self.__y = round(self.__y)