from abc import abstractmethod
from smithnormalform import pid


class ED(pid.PID):

    # in addition to the norm it is required x.__floordiv__(y) and x.__mod__(y)
    # return q and r respectively such x = q*y + r is a euclidean relation

    @abstractmethod
    def norm(self):
        pass

    def __lt__(self, x):
        return self.norm() < x.norm()

    def __gt__(self, x):
        return self.norm() > x.norm()

    # in a euclidean domain, the extended euclidean algorithm can be used
    # to find the extended_gcd, which makes this problem much easier
    def extended_gcd(a, b):
        x0 = type(b).getOne()
        x1 = type(b).getZero()
        y0 = type(b).getZero()
        y1 = type(b).getOne()
        while b != type(b).getZero():
            tempa = a
            tempb = b
            q = tempa // tempb
            a = tempb
            b = tempa % tempb
            tempx0 = x0
            x0 = x1
            x1 = tempx0 - q * x0
            tempy0 = y0
            y0 = y1
            y1 = tempy0 - q * y0
        return [a, x0, y0]
