from smithnormalform import matrix


class SNFProblem():
    def __init__(self, A, debug=False):
        self.A = A.copy()
        self.elementT = type(A.get(0, 0))
        self.J = A.copy()
        self.S = matrix.Matrix.id(A.h, type(A.get(0, 0)))
        self.T = matrix.Matrix.id(A.w, type(A.get(0, 0)))

        self.debug = debug

    def isValid(self):
        # check that S is unimodular
        if not self.S.determinant().isUnit():
            return False

        # check that T is unimodular
        elif not self.T.determinant().isUnit():
            return False

        # check that the desired product relation holds
        elif not self.S * self.A * self.T == self.J:
            return False

        # check that self.J is in smith normal form
        #
        # first we check that elements outside the diagonal are zero
        zero = self.elementT.getZero()
        for i in range(self.J.h):
            for j in range(self.J.w):
                if i != j and self.J.get(i, j) != zero:
                    return False

        # then we check that diagonal elements divide each other until a zero
        # is found and then all remaining diagonal elements are zero
        diagLength = min(self.J.h, self.J.w)
        if diagLength > 1:
            lastDiag = self.J.get(0, 0)
            seenZero = (lastDiag == zero)
            for i in range(1, diagLength):
                currentDiag = self.J.get(i, i)
                if currentDiag == zero:
                    seenZero = True

                if seenZero and currentDiag != zero:
                    return False

                if not seenZero and currentDiag % lastDiag != zero:
                    return False

        # if all of the checks pass then this is a valid completed SNF problem
        return True

    def cSwap(self, i, j):
        if self.debug:
            print("cSwap call")

        if i == j:
            return

        # perform the column swap to J
        for k in range(self.J.h):
            temp = self.J.get(k, i)
            self.J.set(k, i, self.J.get(k, j))
            self.J.set(k, j, temp)

        # adjust the T matrix
        adjustment = matrix.Matrix.id(self.T.h, self.elementT)
        adjustment.set(i, i, self.elementT.getZero())
        adjustment.set(j, j, self.elementT.getZero())
        adjustment.set(i, j, self.elementT.getOne())
        adjustment.set(j, i, self.elementT.getOne())
        self.T = self.T * adjustment

    def cLC(self, k, i, j, a, b, gcd=None):
        if self.debug:
            print("cLC call")

        # perform the linear column application to J
        if gcd is None or a.isUnit():
            c = self.elementT.getZero()
            d = self.elementT.getOne()
        else:
            c = -self.J.get(k, j) // gcd
            d = self.J.get(k, i) // gcd

        temp = []
        for k in range(self.J.h):
            temp = self.J.get(k, i)
            self.J.set(k, i, a * self.J.get(k, i) + b * self.J.get(k, j))
            self.J.set(k, j, c * temp + d * self.J.get(k, j))

        # adjust the self.T matrix
        adjustment = matrix.Matrix.id(self.T.h, self.elementT)
        adjustment.set(i, i, a)
        if i != j:
            adjustment.set(j, i, b)
            adjustment.set(i, j, c)
            adjustment.set(j, j, d)

        self.T = self.T * adjustment

    def rSwap(self, i, j):
        if self.debug:
            print("rSwap call")

        if i == j:
            return

        # perform the row swap to self.J
        for k in range(self.J.w):
            temp = self.J.get(i, k)
            self.J.set(i, k, self.J.get(j, k))
            self.J.set(j, k, temp)

        # adjust the S matrix
        adjustment = matrix.Matrix.id(self.S.h, self.elementT)
        adjustment.set(i, j, self.elementT.getOne())
        adjustment.set(j, i, self.elementT.getOne())
        adjustment.set(i, i, self.elementT.getZero())
        adjustment.set(j, j, self.elementT.getZero())
        self.S = adjustment * self.S

    def rLC(self, k, i, j, a, b, gcd=None):
        if self.debug:
            print("rLC call")

        if (gcd is None or a.isUnit()):
            c = self.elementT.getZero()
            d = self.elementT.getOne()
        else:
            c = -self.J.get(j, k) // gcd
            d = self.J.get(i, k) // gcd

        # perform the linear column application to self.J
        for k in range(self.J.w):
            temp = self.J.get(i, k)
            self.J.set(i, k, a * self.J.get(i, k) + b * self.J.get(j, k))
            self.J.set(j, k, c * temp + d * self.J.get(j, k))

        # adjust the self.S matrix
        adjustment = matrix.Matrix.id(self.S.h, self.elementT)
        adjustment.set(i, i, a)
        if i != j:
            adjustment.set(i, j, b)
            adjustment.set(j, i, c)
            adjustment.set(j, j, d)
        self.S = adjustment * self.S

    def computeSNF(self):
        # The heart of snf starts here
        for i in range(min(self.J.h, self.J.w)):

            # if the top-left element of the subarray is 0 we need to
            # perform row/column swaps to move in a different value
            if self.J.get(i, i) == self.elementT.getZero():

                # we search for a nonzero entry in the submatrix to replace the
                # zero element with.
                foundReplacement = False
                for j in range(i, self.J.h):
                    if foundReplacement:
                        break
                    for k in range(i, self.J.w):
                        if (self.J.get(j, k) != self.elementT.getZero()):
                            foundReplacement = True
                            break

                # if there are no non-zero values left to swap in, the
                # algorithm is complete
                if not foundReplacement:
                    break

                # perform the swap
                else:
                    self.rSwap(i, j)
                    self.cSwap(i, k)

            # now we should not have a zero in the top-left position
            # of the submatrix

            # make the top-left submatrix element be the gcd of all the
            # elements in the same row or the same column
            gcd = self.J.get(i, i)
            doneIteration = False
            while not doneIteration:
                if (self.J.get(i, i).isUnit()):
                    break
                doneIteration = True
                for j in range(i + 1, self.J.h):
                    gcd, x, y = self.J.get(i, i).extended_gcd(self.J.get(j, i))
                    if self.J.get(i, i).isUnitMultipleOf(gcd):
                        pass
                    elif self.J.get(j, i).isUnitMultipleOf(gcd):
                        self.rSwap(i, j)
                        doneIteration = False
                    else:
                        self.rLC(i, i, j, x, y, gcd)
                        doneIteration = False
                for j in range(i + 1, self.J.w):
                    gcd, x, y = self.J.get(i, i).extended_gcd(self.J.get(i, j))
                    if self.J.get(i, i).isUnitMultipleOf(gcd):
                        pass
                    elif self.J.get(i, j).isUnitMultipleOf(gcd):
                        self.cSwap(i, j)
                        doneIteration = False
                    else:
                        self.cLC(i, i, j, x, y, gcd)
                        doneIteration = False

            # use the gcd to make all elements int the ith row and the ith
            # column zero by row and column linear combinations
            doneZeroing = False
            while not doneZeroing:
                doneZeroing = True
                for j in range(i + 1, self.J.h):
                    if self.J.get(j, i) != self.elementT.getZero():
                        self.rLC(i, j, i, self.elementT.getOne(),
                                 -self.J.get(j, i) // self.J.get(i, i))
                        if self.J.get(j, i) != self.elementT.getZero():
                            doneZeroing = False
                for j in range(i + 1, self.J.w):
                    if self.J.get(i, j) != self.elementT.getZero():
                        self.cLC(i, j, i, self.elementT.getOne(),
                                 -self.J.get(i, j) // self.J.get(i, i))
                        if self.J.get(i, j) != self.elementT.getZero():
                            doneZeroing = False

        # At this point self.J is diagonalized. Me simply need to make sure
        # that every diagonal element divides the element after it
        for i in range(min(self.J.w, self.J.h) - 1):

            # If the next diagonal element is 0, then all following diagonal
            # elements # will be 0. Therefore self.J is in Smith normal form
            # and we return
            if self.J.get(i + 1, i + 1) == self.elementT.getZero():
                return
            gcd, x, y = self.J.get(i, i).extended_gcd(self.J.get(i + 1, i + 1))

            # if the ith diagonal element is already the gcd of of the the
            # ith and the (i+1)th diagonal elements, they are correct and
            # we can advance. If they are not we should change the ith
            # element to be the gcd by row operations while maintaining
            # that self.J is diagonal
            if (gcd == self.J.get(i + 1, i + 1)):
                self.cSwap(i, i + 1)
                self.rSwap(i, i + 1)

            elif (gcd != self.J.get(i, i)):
                self.rLC(i, i, i + 1, self.elementT.getOne(),
                         self.elementT.getOne())
                self.cLC(i, i, i + 1, x, y, gcd)
                self.cLC(i, i + 1, i, self.elementT.getOne(),
                         -self.J.get(i, i + 1) // self.J.get(i, i))
                self.rLC(i, i + 1, i, self.elementT.getOne(),
                         -self.J.get(i + 1, i) // self.J.get(i, i))
