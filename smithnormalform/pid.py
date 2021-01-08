from abc import ABC, abstractmethod


class InvalidInitialContent(Exception):
    pass


# This abstract class represents all Principle Ideal Domains. In order for
# this library to be able to process your ring it must implement all of the
# @abstractmethods below. Each of these operations are well defined for all
# PIDs and uniquely define a PID. see:
# https://en.wikipedia.org/wiki/Principal_ideal_domain
class PID(ABC):

    @abstractmethod
    def __str__(self):
        pass

    # returns whether the two PID objects
    @abstractmethod
    def __eq__(self, x):
        pass

    # returns whether the two PID objects are not equal
    @abstractmethod
    def __ne__(self, x):
        pass

    # returns the negation (additive inverse) of the object
    @abstractmethod
    def __neg__(self):
        pass

    # returns the sum of two elements of a PID
    @abstractmethod
    def __add__(self, x):
        pass

    # returns the difference of two elements of a PID
    @abstractmethod
    def __sub__(self, x):
        pass

    # returns the product of two elements of a PID
    @abstractmethod
    def __mul__(self, x):
        pass

    # returns the floored division of two elements of a PID
    @abstractmethod
    def __floordiv__(self, x):
        pass

    # returns the floored division remainder of two elements of a PID
    @abstractmethod
    def __mod__(self, x):
        pass

    # returns the additive identity of the ring
    @staticmethod
    @abstractmethod
    def getZero():
        pass

    # returns the multiplicative identity of the ring
    @staticmethod
    @abstractmethod
    def getOne():
        pass

    # returns whether the integer here is a unit. see:
    # https://en.wikipedia.org/wiki/Unit_(ring_theory)
    @abstractmethod
    def isUnit(self):
        pass

    # returns True when this object is a unit multiple of x, otherwise False.
    def isUnitMultipleOf(self, x):
        if not (self % x) == self.getZero():
            return False
        if not (self // x).isUnit():
            return False
        return True

    # This should return a tuple (g, x, y) such where
    # - g is the gcd of self and x
    # - g = a * y + b * x
    # Such a tuple will always exist since all principle ideal
    # domains are bezout domains.
    #
    # Note that if your principle ideal domain is additionally a euclidean
    # domain, the extended euclidean algorithm can be used to find the
    # extended gcd.  Rather than implementing the extended euclidean
    # algorithm yourself, you should instead have your PID inherit from
    # smithnormalform.ed.ED instead, which will cause extended_gcd to be
    # implemented for you.
    @abstractmethod
    def extended_gcd(a, b):
        pass
