from smithnormalform import ed, pid


# This is represents the ring of all integers. Since the set of all integers
# is a euclidean domain, this class extends ed.ED. We operate basic
# functionality of the ring of integers including addition, subtraction,
# multiplication, quotient, and remainder operations. See:
# https://en.wikipedia.org/wiki/Ring_of_integers
class Z(ed.ED):
    def __init__(self, content):
        if isinstance(content, int):
            self.a = content
        elif isinstance(content, str):
            try:
                self.a = int(content)
            except ValueError:
                raise pid.InvalidInitialContent
        elif isinstance(content, list):
            if len(content) != 1 or not isinstance(content[0], int):
                raise pid.InvalidInitialContent
            else:
                self.a = content[0]
        else:
            raise pid.InvalidInitialContent

    def __str__(self):
        return str(self.a)

    def __hash__(self):
        # We include a unique class identifier here to force the hash to be
        # unique to objects of this class
        return hash(("com.corbinmcneill.smithnormalform.z", self.a))

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

    # This returns the quotient of division of self by x
    def get_q(self, x):
        return Z(self.a // x.a)

    # This returns the remainder of division of self by x
    def get_r(self, x):
        return Z(self.a % x.a)

    # Since all euclidean domains must feature a norm, we include a norm to
    # support euclidean domain operations supported in ed.ED. A number of
    # norms could have been chosen here, but we choose the classic norm of
    # |x| = x^2 .
    def norm(self):
        return self.a * self.a

    # return the additive identity of the ring
    @staticmethod
    def getZero():
        return Z(0)

    # return the multiplicative identity of the ring
    @staticmethod
    def getOne():
        return Z(1)

    # Returns whether the integer here is a unit. see:
    # https://en.wikipedia.org/wiki/Unit_(ring_theory)
    def isUnit(self):
        return (self.a == 1) or (self.a == -1)
