from abc import ABC, abstractmethod


class InvalidInitialContent(Exception):
    pass


class PID(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, x):
        pass

    @abstractmethod
    def __ne__(self, x):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __add__(self, x):
        pass

    @abstractmethod
    def __sub__(self, x):
        pass

    @abstractmethod
    def __mul__(self, x):
        pass

    @abstractmethod
    def __floordiv__(self, x):
        pass

    @abstractmethod
    def __mod__(self, x):
        pass

    @staticmethod
    @abstractmethod
    def getZero():
        pass

    @staticmethod
    @abstractmethod
    def getOne():
        pass

    @abstractmethod
    def isUnit(self):
        pass

    def isUnitMultipleOf(self, x):
        if not (self % x) == self.getZero():
            return False
        if not (self // x).isUnit():
            return False
        return True

    @abstractmethod
    def extended_gcd(a, b):
        """
        This should return a tuple (g, x, y) such where
        - g is the gcd of self and x
        - g = a * y + b * x
        Such a tuple will always exist since all principle ideal
        domains are bezout domains.

        Note that if your principle ideal domain is additionally a euclidean
        domain, the extended euclidean algorithm can be used to find the
        extended gcd.  Rather than implmenenting the extended euclidean
        algorithm yourself, you should instead have your PID inherit from
        smithnormalform.ed.ED instead, which will cause extended_gcd to be
        implemented for you.
        """
        pass
