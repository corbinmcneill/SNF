class ZI(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __neg__(x):
        return ZI(-x.a, -x.b)

    def __mul__(x, y):
        return ZI(x.a*y.a - x.b*y.b, x.a*y.b + x.b*y.a)

    def __add__(x, y):
        return ZI(x.a + y.a, x.b + y.b)

    def __sub__(x, y):
        return ZI(x.a - y.a, x.b - y.b)

    def __lt__(x, y):
        return (x.a*x.a + x.b*x.b) < (y.a*y.a + y.b*y.b)

    def __gt__(x, y):
        return (x.a*x.a + x.b*x.b) > (y.a*y.a + y.b*y.b)

    def __str__(self):
        if self.a == 0 and self.b == 0:
            return "0"
        elif self.a == 0:
            return f"{self.b}i"
        elif self.b == 0:
            return f"{self.a}"
        else:
            return f"{self.a}{self.b:+}i"

    def __eq__(x, y):
        return x.a == y.a and x.b == y.b

    def __ne__(x, y):
        return not x == y

    def com(x):
        return ZI(x.a, -x.b)

    def num(x, y):
        return ZI((x * y.com()).a, (x * y.com()).b)

    def __floordiv__(x, y):
        n1 = x.num(y).a
        n2 = x.num(y).b
        d = y.a*y.a + y.b*y.b
        comp1 = (n1 + d//2)//d
        comp2 = (n2 + d//2)//d
        return ZI(comp1, comp2)
        return ZI(int(round(float((x.num(y)).a) // (y.a * y.a + y.b * y.b))),
                  int(round(float((x.num(y)).b) // (y.a * y.a + y.b * y.b))))

    def __mod__(x, y):
        return ZI((x - y * (x // y)).a, (x - y * (x // y)).b)

    def isUnit(self):
        if self.a == 1 and self.b == 0:
            return True
        elif self.a == -1 and self.b == 0:
            return True
        elif self.a == 0 and self.b == 1:
            return True
        elif self.a == 0 and self.b == -1:
            return True
        return False

    @staticmethod
    def getUnits():
        return [ZI(1, 0), ZI(-1, 0), ZI(0, 1), ZI(0, -1)]

    @staticmethod
    def getZero():
        return ZI(0, 0)

    @staticmethod
    def getOne():
        return ZI(1, 0)

    def getListOfElements(self):
        return [self.a, self.b]
