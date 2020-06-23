from abc import ABC, abstractmethod


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
    def __lt__(self, x):
        pass

    @abstractmethod
    def __gt__(self, x):
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
