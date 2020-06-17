class Z(object):
    def __init__(self, a):
        self.a = a

    def __neg__(x):
        return Z(-x.a)

    def __mul__(x, y):
        return Z(x.a * y.a)

    def __floordiv__(x, y):
        return Z(x.a // y.a)

    def __mod__(x, y):
        return Z(x.a % y.a)

    def __add__(x, y):
        return Z(x.a + y.a)

    def __sub__(x, y):
        return Z(x.a - y.a)

    def __str__(self):
        return str(self.a)

    def __eq__(x, y):
        return x.a == y.a

    def __ne__(x, y):
        return x.a != y.a

    def __lt__(x, y):
        return x.a < y.a

    def __gt__(x, y):
        return x.a > y.a


    def isUnit(self):
        return (self.a == 1) or (self.a == -1)

    @staticmethod
    def getUnits():
        return [Z(1),Z(-1)]

    @staticmethod
    def getZero():
        return Z(0)

    @staticmethod
    def getOne():
        return Z(1)

    def factor(self):
        factors = []
        aCopy = self.a
        currentFactor = 2
        while currentFactor <= float(aCopy):
            if aCopy % currentFactor == 0:
                factors.append(Z(currentFactor))
                aCopy //= currentFactor
            else:
                currentFactor += 1
        if aCopy > 1:
            factors.append(Z(currentFactor))
        return factors
