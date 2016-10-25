class Integer:
    def __init__(self, a):
        self.a = a

    def __mul__(x,y):
        return Integer(x.a * y.a)

    def __add__(x,y):
        return Integer(x.a + y.a)

    def __str__(self):
        return str(self.a)

    def isUnit(self):
        return (self.a==1) or (self.a==-1)

    def getZero(self):
        return Integer(0)

    def factor(self):
        factors = []
        aCopy = self.a
        currentFactor = 2
        while currentFactor <= float(aCopy):
            if aCopy % currentFactor == 0:
                factors.append(Integer(currentFactor))
                aCopy /= currentFactor
        if aCopy > 1:
            factors.append(Integer(currentFactor))
        return factors

class GInteger:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(x,y):
        return GInteger(x.a*y.a - x.b*y.b, x.a*y.b + x.b*y.a)

    def __add__(x,y):
        return GInteger(x.a + y.a, x.b + y.b)

    def __str__(self):
        return str(self.a) + "+(" + str(self.b)+")i"

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

    def getZero(self):
        return GInteger(0,0)

    def factor(self):
        #TODO
        return []

class Matrix:
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

    def get(self, i, j):
        assert i>=0 and i<self.h
        assert j>=0 and j<self.w
        return self.elements[i*self.w + j]

matrixA = Matrix(2,2,[Integer(5), Integer(4), Integer(7), Integer(2)])
matrixB = Matrix(2,2,[Integer(0), Integer(2), Integer(3), Integer(3)])
print str(matrixA * matrixB)


