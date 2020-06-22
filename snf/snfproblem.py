import snf.z as z
import snf.zi as zi
import snf.matrix as matrix



class SNFProblem():
        def __init__(self, A):
                self.A = A.copy()
                self.elementT = type(A.get(0,0))
                self.J = A.copy()
                self.S = matrix.Matrix.id(A.h, type(A.get(0,0)))
                self.T = matrix.Matrix.id(A.w, type(A.get(0,0)))

        def cSwap(self,i,j):
                #perform the column swap to J
                for k in range(self.J.h):
                        temp = self.J.get(k, i)
                        self.J.set(k,i,self.J.get(k,j))
                        J.set(k,j, temp)

                #adjust the T matrix
                adjustment = matrix.Matrix.id(self.T.h, selfelementT)
                adjustment.set(i,i,self.elementT.getZero())
                adjustment.set(j,j,self.elementT.getZero())
                adjustment.set(i,j,self.elementT.getOne())
                adjustment.set(j,i,self.elementT.getOne())
                self.T = self.T*adjustment

        def cLC(self,I,i,j,a,b,gcd=None):
                #perform the linear column application to J
                if gcd is None or a.isUnit():
                        c = self.elementT.getZero()
                        d = self.elementT.getOne()
                else:
                        c = -self.J.get(I,j)//gcd
                        d = self.J.get(I,i)//gcd

                temp = []
                for k in range(self.J.h):
                        temp = self.J.get(k,i)
                        self.J.set(k,i,a*self.J.get(k,i) + b*self.J.get(k,j))
                        self.J.set(k,j,c*temp + d*self.J.get(k,j))

                #adjust the self.T matrix
                adjustment = matrix.Matrix.id(self.T.h, self.elementT)
                adjustment.set(i,i,a)
                if i!=j:
                        adjustment.set(j,i,b) 
                        adjustment.set(i,j,c)
                        adjustment.set(j,j,d)

                self.T = self.T*adjustment

        def rSwap(self,i,j):
                #perform the row swap to self.J
                for k in range(self.J.w):
                        temp = self.J.get(i, k)
                        self.J.set(i,k,self.J.get(j,k))
                        self.J.set(j,k, temp)

                #adjust the S matrix
                adjustment = matrix.Matrix.id(self.S.h, self.elementT)
                adjustment.set(i,j,self.elementT.getOne())
                adjustment.set(j,i,self.elementT.getOne())
                adjustment.set(i,i,self.elementT.getZero())
                adjustment.set(j,j,self.elementT.getZero())
                self.S = adjustment*self.S

        def rLC(self,I,i,j,a,b,gcd=None):
                if (gcd is None or a.isUnit()):
                        c=self.elementT.getZero()
                        d=self.elementT.getOne()
                else:
                        c = -self.J.get(j,I)//gcd
                        d = self.J.get(i,I)//gcd

                #perform the linear column application to self.J
                for k in range(self.J.w):
                        temp = self.J.get(i,k)
                        self.J.set(i,k,a*self.J.get(i,k) + b*self.J.get(j,k))
                        self.J.set(j,k,c*temp + d*self.J.get(j,k))

                #adjust the self.S matrix
                adjustment = matrix.Matrix.id(self.S.h, self.elementT)
                adjustment.set(i,i,a)
                if i!=j:
                        adjustment.set(i,j,b) 
                        adjustment.set(j,i,c)
                        adjustment.set(j,j,d)
                self.S = adjustment*self.S

        @staticmethod
        def euclid(a, b):
                # output g, x, y where g = gcd(a,b) = xa + yb
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


        def computeSNF(self):
                #The heart of snf starts here
                for i in range(min(self.J.h,self.J.w)):
                        #if the top-left element of the subarray is 0 we need to
                        #perform row/column swaps to move in a different value
                        if self.J.get(i,i) == self.elementT.getZero():
                                #we search for a nonzero entry in the submatrix to replace the
                                #zero element with. 
                                foundReplacement = False;
                                for j in range(i, self.J.h):
                                        if foundReplacement:
                                                break
                                        for k in range(i,self.J.w):
                                                if (self.J.get(j,k) != self.elementT.getZero()):
                                                        foundReplacement = True
                                                        break
                                #if there are no non-zero values left to swap in, the algorithm
                                #is complete
                                if not foundReplacement:
                                        break
                                #perform the swap
                                else:
                                        self.rSwap(i,j)
                                        self.cSwap(i,k)
                        #now we should not have a zero in the top-left position
                        #of the submatrix

                        #make the top-left submatrix element be the gcd of all the elements
                        #in the same row or the same column
                        gcd=self.J.get(i,i)
                        doneIteration = False
                        while not doneIteration:
                                if (self.J.get(i,i).isUnit()):
                                        break
                                doneIteration = True
                                for j in range(i+1, self.J.h):
                                        gcd, x, y = SNFProblem.euclid(self.J.get(i,i), self.J.get(j,i))
                                        if (gcd < self.elementT.getZero()):
                                                gcd = -gcd
                                                x = -x
                                                y = -y
                                        if gcd == self.J.get(i,i):
                                                pass
                                        elif gcd == self.J.get(j,i):
                                                self.rSwap(i,j)
                                                doneIteration=False
                                        elif gcd == -self.J.get(j,i):
                                                self.rSwap(i,j)
                                                self.rLC(i,i,i,-self.elementT.getOne(), self.elementT.getZero(),gcd)
                                                doneIteration=False
                                        elif gcd < self.J.get(i,i) or gcd < -self.J.get(i,i):
                                                self.rLC(i, i, j, x, y, gcd)
                                                doneIteration=False
                                for j in range(i+1, self.J.w):
                                        gcd, x, y = SNFProblem.euclid(self.J.get(i,i), self.J.get(i,j))
                                        if (gcd < self.elementT.getZero()):
                                                gcd = -gcd
                                                x = -x
                                                y = -y
                                        if gcd == self.J.get(i,i):
                                                pass
                                        elif gcd == self.J.get(i,j):
                                                self.cSwap(i,j)
                                                doneIteration=False
                                        elif gcd == -self.J.get(i,j): #TODO WORK THIS BLOCK
                                                self.cSwap(i,j)
                                                self.cLC(i,i,i,-self.elementT.getOne(), self.elementT.getZero(),gcd)
                                                doneIteration=False
                                        elif gcd < self.J.get(i,i) or gcd < -self.J.get(i,i):
                                                self.cLC(i, i, j, x, y, gcd)
                                                doneIteration=False

                        #use the gcd to make all elements int the ith row and the ith
                        #column zero by row and column linear combinations
                        doneZeroing = False
                        while not doneZeroing:
                                doneZeroing = True
                                for j in range(i+1, self.J.h):
                                        if self.J.get(j,i) != self.elementT.getZero():
                                                self.rLC(i,j,i,self.elementT.getOne(),-self.J.get(j,i)//self.J.get(i,i))
                                                if self.J.get(j,i) != self.elementT.getZero():
                                                        doneZeroing = False
                                for j in range(i+1, self.J.w):
                                        if self.J.get(i,j) != self.elementT.getZero():
                                                self.cLC(i,j,i,self.elementT.getOne(),-self.J.get(i,j)//self.J.get(i,i))
                                                if self.J.get(i,j) != self.elementT.getZero():
                                                        doneZeroing = False

                #At this point self.J is diagonalized. Me simply need to make sure that every
                #diagonal element divides the element after it
                for i in range(min(self.J.w, self.J.h)-1):
                        #If the next diagonal element is 0, then all following diagonal elements
                        #will be 0. Therefore self.J is in Smith normal form and we return
                        if self.J.get(i+1,i+1) == self.elementT.getZero():
                                return self.S,self.J,self.T
                        gcd, x, y = SNFProblem.euclid(self.J.get(i,i), self.J.get(i+1,i+1))
                        #if the ith diagonal element is already the gcd of of the the ith and
                        #the (i+1)th diagonal elements, they are correct and we can advance. If
                        #they are not we should change the ith element to be the gcd by row
                        #operations while maintaining that self.J is diagonal
                        if (gcd == self.J.get(i+1,i+1)):
                                self.cSwap(i, i+1)
                                self.rSwap(i, i+1)
                        elif (gcd != self.J.get(i,i)):
                                self.rLC(i,i, i+1, self.elementT.getOne(), self.elementT.getOne())
                                self.cLC(i, i, i+1, x, y, gcd)
                                self.cLC(i, i+1, i, self.elementT.getOne(), -self.J.get(i,i+1)//self.J.get(i,i))
                                self.rLC(i, i+1, i, self.elementT.getOne(), -self.J.get(i+1,i)//self.J.get(i,i))

                return self.S,self.J,self.T

if __name__ == "__main__":

        #contents = [Z(0),Z(-5),Z(10),Z(-10)]
        #A = matrix.Matrix(2,2,contents)
        
        A = matrix.Matrix.inputMatrix()
        snfObject = SNFProblem(A)

        snfObject.computeSNF(A)
        s = snfObject.S
        j = snfObject.J
        t = snfObject.T

        print("Smith Normal Form computation complete. Results:")
        print()

        print("\nS:" )
        print(str(s) )
        print("T:"   )
        print(str(t) )
        print("self.J:"   )
        print(str(j) )
        print("S*A*T")
        print(s*A*t  )
