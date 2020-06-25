class IncompatibleMatrixSizesException(Exception):
    pass


class MatrixNotSquareException(Exception):
    pass


class InvalidNumberOfElements(Exception):
    pass


class Matrix():

    _determinant_saves = {}

    def __init__(self, h, w, elements):
        if len(elements) != h*w:
            raise InvalidNumberOfElements

        self.h = h
        self.w = w
        self.elements = elements

    def __add__(x, y):
        if x.h != y.h or x.w != y.w:
            raise IncompatibleMatrixSizesException

        newElements = []
        for i in range(x.h * x.w):
            newElements.append(x.elements[i] + y.elements[i])
        return Matrix(x.h, x.w, newElements)

    def __mul__(x, y):
        if x.w != y.h:
            raise IncompatibleMatrixSizesException

        newH = x.h
        newW = y.w
        newElements = []
        for i in range(newH):
            for j in range(newW):
                newElement = x.elements[0].getZero()
                for k in range(x.w):
                    newElement += (x.get(i, k) * y.get(k, j))
                newElements.append(newElement)
        return Matrix(newH, newW, newElements)

    def __str__(self):
        result = ""
        for i in range(self.h):
            row = self.elements[i*self.w:(i+1)*self.w]
            internal_string = ' '.join(list(map(str, row)))
            result += "[{}]\n".format(internal_string)
        return result

    def __eq__(x, y):
        if x.h != y.h or x.w != y.w:
            return False
        for i in range(x.w * x.h):
            if x.elements[i] != y.elements[i]:
                return False
        return True

    def __ne__(x, y):
        return not x == y

    def determinant(self):
        if self.h != self.w:
            raise MatrixNotSquareException()

        if (self.h == 1):
            return self.get(0, 0)

        elements_tuple = tuple(self.elements)
        if elements_tuple in Matrix._determinant_saves:
            return Matrix._determinant_saves[elements_tuple]

        total = type(self.get(0, 0)).getZero()
        for i in range(self.h):
            scale = self.get(i, 0)
            if (i % 2 == 1):
                scale = -scale
            subcontent = []
            for j in range(self.h):
                if i == j:
                    continue
                else:
                    for k in range(1, self.h):
                        subcontent.append(self.get(j, k))
            subMatrix = Matrix(self.h-1, self.h-1, subcontent)
            total += scale * subMatrix.determinant()

        Matrix._determinant_saves[elements_tuple] = total
        return total

    @staticmethod
    def id(dim, elementType):
        elements = [elementType.getZero() for i in range(dim*dim)]
        for i in range(dim):
            elements[i*dim + i] = elementType.getOne()
        return Matrix(dim, dim, elements)

    def get(self, i, j):
        return self.elements[i*self.w + j]

    def set(self, i, j, e):
        self.elements[i*self.w + j] = e

    def copy(self):
        return Matrix(self.h, self.w, self.elements[:])
