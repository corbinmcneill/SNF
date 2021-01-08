from smithnormalform import ed, pid
import re


# This is represents the ring of all gaussian integers, that is complex
# numbers where both the real and complex values are integral. Since the set
# of all gaussian integers is a euclidean domain, this class extends ed.ED.
# We operate basic functionality of the ring including addition, subtraction,
# multiplication, quotient, and remainder operations. See:
# https://en.wikipedia.org/wiki/Gaussian_integer

class ZI(ed.ED):
    # This regex determines whether a string can be parsed as a gaussian integer
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
        # We include a unique class identifier here to force the hash to be
        # unique to objects of this class
        return hash(("com.corbinmcneill.smithnormalform.zi", self.a, self.b))

    def __eq__(self, y):
        return self.a == y.a and self.b == y.b

    def __ne__(self, y):
        return not self == y

    def __neg__(self):
        return ZI([-self.a, -self.b])

    def __add__(self, y):
        return ZI([self.a + y.a, self.b + y.b])

    def __sub__(self, y):
        return ZI([self.a - y.a, self.b - y.b])

    def __mul__(self, y):
        return ZI([self.a * y.a - self.b * y.b, self.a * y.b + self.b * y.a])

    # return the complex conjugate of this value. see:
    # https://en.wikipedia.org/wiki/Complex_conjugate
    def com(self):
        return ZI([self.a, -self.b])

    # return the product of this ZI with the complex conjugate of another ZI
    def num(self, y):
        return self * y.com()

    # get the quotient when this object is divided by another ZI
    def get_q(self, y):
        n1 = self.num(y).a
        n2 = self.num(y).b
        d = y.a * y.a + y.b * y.b
        comp1 = (n1 + d // 2) // d
        comp2 = (n2 + d // 2) // d
        return ZI([comp1, comp2])

    # get the remainder of division
    def get_r(self, y):
        return ZI([(self - y * (self // y)).a, (self - y * (self // y)).b])

    # Returns the norm of this ZI object according to some euclidean norm
    # function.
    def norm(self):
        return self.a * self.a + self.b * self.b

    # return the additive identity of the ring
    @staticmethod
    def getZero():
        return ZI([0, 0])

    # return the multiplicative identity of the ring
    @staticmethod
    def getOne():
        return ZI([1, 0])

    # Returns whether the integer here is a unit. see:
    # https://en.wikipedia.org/wiki/Unit_(ring_theory)
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
