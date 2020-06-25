from smithnormalform import ed


class Z(ed.ED):
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return str(self.a)

    def __hash__(self):
        return hash(self.a)

    def __eq__(self, x):
        return self.a == x.a

    def __ne__(self, x):
        return self.a != x.a

    def __neg__(self):
        return Z(-self.a)

    def __add__(self, x):
        return Z(self.a + x.a)

    def __sub__(self, x):
        return Z(self.a - x.a)

    def __mul__(self, x):
        return Z(self.a * x.a)

    def get_q(self, x):
        return Z(self.a // x.a)

    def get_r(self, x):
        return Z(self.a % x.a)

    def norm(self):
        return self.a * self.a

    @staticmethod
    def getZero():
        return Z(0)

    @staticmethod
    def getOne():
        return Z(1)

    def isUnit(self):
        return (self.a == 1) or (self.a == -1)
