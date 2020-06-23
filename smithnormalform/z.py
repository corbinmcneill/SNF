from smithnormalform import pid


class Z(pid.PID):
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return str(self.a)

    def __eq__(self, x):
        return self.a == x.a

    def __ne__(self, x):
        return self.a != x.a

    def __lt__(self, x):
        return (self.a * self.a) < (x.a * x.a)

    def __gt__(self, x):
        return (self.a * self.a) > (x.a * x.a)

    def __neg__(self):
        return Z(-self.a)

    def __add__(self, x):
        return Z(self.a + x.a)

    def __sub__(self, x):
        return Z(self.a - x.a)

    def __mul__(self, x):
        return Z(self.a * x.a)

    def __floordiv__(self, x):
        return Z(self.a // x.a)

    def __mod__(self, x):
        return Z(self.a % x.a)

    @staticmethod
    def getZero():
        return Z(0)

    @staticmethod
    def getOne():
        return Z(1)

    def isUnit(self):
        return (self.a == 1) or (self.a == -1)
