from smithnormalform import ed, pid
import re


class ZI(ed.ED):

    regex_pattern = "^(?:(-?\\d+)([\\+-]\\d*)i)|(-?\\d*)|(-?\\d+i)$"
    regex_compiled = re.compile(regex_pattern)

    def __init__(self, content):
        if isinstance(content, str):
            regex_match = ZI.regex_compiled.match(content)
            if regex_match:
                if regex_match.groups()[0] and regex_match.groups()[1]:
                    self.a = int(regex_match.groups()[0])
                    self.b = int(regex_match.groups()[1])
                elif regex_match.groups()[2]:
                    self.a = int(regex_match.groups()[2])
                    self.b = 0
                elif regex_match.groups()[3]:
                    self.a = 0
                    self.b = int(regex_match.groups()[3])
                else:
                    raise pid.InvalidInitialContent
            else:
                raise pid.InvalidInitialContent
        elif isinstance(content, list):
            if len(content) != 2:
                raise pid.InvalidInitialContent
            if not (isinstance(content[0], int) and
                    isinstance(content[1], int)):
                raise pid.InvalidInitialContent
            else:
                self.a = content[0]
                self.b = content[1]
        else:
            raise pid.InvalidInitialContent

    def __str__(self):
        if self.a == 0 and self.b == 0:
            return "0"
        elif self.a == 0:
            return f"{self.b}i"
        elif self.b == 0:
            return f"{self.a}"
        else:
            return f"{self.a}{self.b:+}i"

    def __hash__(self):
        return hash((self.a, self.b))

    def __eq__(x, y):
        return x.a == y.a and x.b == y.b

    def __ne__(x, y):
        return not x == y

    def __neg__(x):
        return ZI([-x.a, -x.b])

    def __add__(x, y):
        return ZI([x.a + y.a, x.b + y.b])

    def __sub__(x, y):
        return ZI([x.a - y.a, x.b - y.b])

    def __mul__(x, y):
        return ZI([x.a*y.a - x.b*y.b, x.a*y.b + x.b*y.a])

    def _com(x):
        return ZI([x.a, -x.b])

    def _num(x, y):
        return ZI([(x * y._com()).a, (x * y._com()).b])

    def get_q(x, y):
        n1 = x._num(y).a
        n2 = x._num(y).b
        d = y.a*y.a + y.b*y.b
        comp1 = (n1 + d//2)//d
        comp2 = (n2 + d//2)//d
        return ZI([comp1, comp2])
        return ZI([int(round(float((x._num(y)).a) // (y.a * y.a + y.b * y.b))),
                  int(round(float((x._num(y)).b) // (y.a * y.a + y.b * y.b)))])

    def get_r(x, y):
        return ZI([(x - y * (x // y)).a, (x - y * (x // y)).b])

    def norm(self):
        return self.a * self.a + self.b * self.b

    @staticmethod
    def getZero():
        return ZI([0, 0])

    @staticmethod
    def getOne():
        return ZI([1, 0])

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
