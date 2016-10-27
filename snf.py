class Z(object):
    def __init__(self, a):
        self.a = a

    def __mul__(x,y):
        return Z(x.a * y.a)

    def __add__(x,y):
        return Z(x.a + y.a)

    def __str__(self):
        return str(self.a)

    def __eq__(x,y):
        return x.a==y.a

    def __ne__(x,y):
        return not x == y

    def isUnit(self):
        return (self.a==1) or (self.a==-1)

    @staticmethod
    def getZero():
        return Z(0)
    
    @staticmethod
    def getOne():
        return Z(1)

    def factor(self):
        factors = []
        aCopy = self.a
        currentFactor = 2
        while currentFactor <= float(aCopy):
            if aCopy % currentFactor == 0:
                factors.append(Z(currentFactor))
                aCopy /= currentFactor
            else:
                currentFactor += 1
        if aCopy > 1:
            factors.append(Z(currentFactor))
        return factors

class ZI(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(x,y):
        return ZI(x.a*y.a - x.b*y.b, x.a*y.b + x.b*y.a)

    def __add__(x,y):
        return ZI(x.a + y.a, x.b + y.b)

    def __str__(self):
        return str(self.a) + "+(" + str(self.b)+")i"

    def __eq__(x,y):
        return x.a == y.a and x.b == y.b

    def __ne__(x,y):
        return not x == y

    def isUnit(self):
        if self.a==1 and self.b==0:
            return True
        elif self.a==-1 and self.b==0:
            return True
        elif self.a==0 and self.b==1:
            return True
        elif self.a==0 and self.b==-1:
            return True
        return False

    @staticmethod
    def getZero():
        return ZI(0,0)

    @staticmethod
    def getOne():
        return ZI(1,0)

    def factor(self):
        #TODO
        return []

class Matrix(object):
    def __init__(self, h, w, elements):
        self.h = h
        self.w = w
        self.elements = elements

    def __add__(x, y):
        assert x.h == y.h
        assert x.w == y.w
        newElements = []
        for i in range(h*w):
            newElements.append(x.elements[i] + y.elements[i])
        return Matrix(x.h, x.w, newElements)

    def __mul__(x, y):
        assert x.w == y.h
        newH = x.h
        newW = y.w
        newElements = []
        for i in range(newH):
            for j in range(newW):
                newElement = x.elements[0].getZero();
                for k in range(x.w):
                    newElement += (x.get(i, k) * y.get(k, j))
                newElements.append(newElement)
        return Matrix(newH, newW, newElements)

    def __str__(self):
        result = ""
        for i in range(self.h):
            for j in range(self.w):
                result += (str(self.get(i,j)) + " ")
            result += "\n"
        return result

    def __eq__(x,y):
        if x.h != y.h or x.w != y.w:
            return False
        for i in range(x.w * x.h):
            if x.elements[i] != y.elements[i]:
                return False
        return True

    def __ne__(x,y):
        return not x == y

    @staticmethod
    def getSquareIdentity(dim, elementType):
        elements = [elementType.getZero() for i in range(dim*dim)]
        for i in range(dim):
            elements[i*dim + i] = elementType.getOne()
        return Matrix(dim, dim, elements)

    def get(self, i, j):
        assert i>=0 and i<self.h
        assert j>=0 and j<self.w
        return self.elements[i*self.w + j]

    def set(self, i, j, e):
        assert i>=0 and i<self.h
        assert j>=0 and j<self.w
        self.elements[i*self.w + j] = e

def snf(A):
	M = Matrix.getSquareIdentity(A.h, type(A.get(0,0)))
	N = Matrix.getSquareIdentity(A.w, type(A.get(0,0)))
