class IncompatibleMatrixSizesException(Exception):
    pass


class MatrixNotSquareException(Exception):
    pass


class InvalidNumberOfElements(Exception):
    pass

# This class represents a matrix over a PID
class Matrix:

    # This hashmap saves solutions to determinant subproblems that have been saved on this matrix to speed up
    # determinant calculations via dynamic programming. For details of its usage see the determinant method.
    _determinant_saves = {}

    # h: the height of the matrix
    # w: the width of the matrix
    # elements: a list of h*w elements of a PID
    def __init__(self, h, w, elements):
        if len(elements) != h*w:
            raise InvalidNumberOfElements

        self.h = h
        self.w = w
        self.elements = elements

    # return the sum of the two matrices
    # If the matrices have sizes that prohibit them from being summed a IncompatibleMatrixSizesException is raised
    def __add__(x, y):
        if x.h != y.h or x.w != y.w:
            raise IncompatibleMatrixSizesException

        newElements = []
        for i in range(x.h * x.w):
            newElements.append(x.elements[i] + y.elements[i])
        return Matrix(x.h, x.w, newElements)

    # return the product of the two matrices
    # If the matrices have sizes that prohibit them from being multiplied a IncompatibleMatrixSizesException is raised
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

    # returns a string representation of the matrix
    def __str__(self):
        result = ""
        for i in range(self.h):
            row = self.elements[i*self.w:(i+1)*self.w]
            internal_string = ' '.join(list(map(str, row)))
            result += "[{}]\n".format(internal_string)
        return result

    # returns whether two matrices are equal, that is whether they have equivalent sizes and are filled with identical
    # elements at each positions
    def __eq__(x, y):
        if x.h != y.h or x.w != y.w:
            return False
        for i in range(x.w * x.h):
            if x.elements[i] != y.elements[i]:
                return False
        return True

    # returns whether two matrices are not equal to one another
    def __ne__(x, y):
        return not x == y

    # returns the determinant of the matrix. This algorithm works on a matrix of size NxN by considering the
    # determinant of some of the submatrices of size (N-1)x(N-1). To speed up this operation we use dynamic programming
    # to memoize the determinant values of submatrices once they have been calculated.
    def determinant(self):
        if self.h != self.w:
            raise MatrixNotSquareException()

        if self.h == 1:
            return self.get(0, 0)

        elements_tuple = tuple(self.elements)
        if elements_tuple in Matrix._determinant_saves:
            return Matrix._determinant_saves[elements_tuple]

        total = type(self.get(0, 0)).getZero()
        for i in range(self.h):
            scale = self.get(i, 0)
            if i % 2 == 1:
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

    # returns the identity matrix of height and width dim, with elements of type elementType
    @staticmethod
    def id(dim, elementType):
        elements = [elementType.getZero() for _ in range(dim*dim)]
        for i in range(dim):
            elements[i*dim + i] = elementType.getOne()
        return Matrix(dim, dim, elements)

    # returns the matrix element in row i and column j
    def get(self, i, j):
        return self.elements[i*self.w + j]

    # sets the matrix element in row i and column j to be e
    def set(self, i, j, e):
        self.elements[i*self.w + j] = e

    # returns a copy of the matrix
    def copy(self):
        return Matrix(self.h, self.w, self.elements[:])
