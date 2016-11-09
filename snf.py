DEBUG = False

class Z(object):
    def __init__(self, a):
        self.a = a

    def __neg__(x):
        return Z(-x.a)

    def __mul__(x, y):
        return Z(x.a * y.a)

    def __div__(x, y):
        return Z(x.a / y.a)

    def __mod__(x, y):
        return Z(x.a % y.a)

    def __add__(x, y):
        return Z(x.a + y.a)

    def __sub__(x, y):
        return Z(x.a - y.a)

    def __str__(self):
        return str(self.a)

    def __eq__(x, y):
        return x.a == y.a

    def __ne__(x, y):
        return x.a != y.a

    def __lt__(x, y):
        return x.a < y.a

    def __gt__(x, y):
        return x.a > y.a


    def isUnit(self):
        return (self.a == 1) or (self.a == -1)

    @staticmethod
    def getUnits():
        return [Z(1),Z(-1)]

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

    def __neg__(x):
        return ZI(-x.a, -x.b)

    def __mul__(x,y):
        return ZI(x.a*y.a - x.b*y.b, x.a*y.b + x.b*y.a)

    def __add__(x,y):
        return ZI(x.a + y.a, x.b + y.b)
    
    def __sub__(x,y):
        return ZI(x.a - y.a, x.b - y.b)

    def __lt__(x,y):
        return (x.a*x.a + x.b*x.b) < (y.a*y.a + y.b*y.b)

    def __gt__(x,y):
        return (x.a*x.a + x.b*x.b) > (y.a*y.a + y.b*y.b)

    def __str__(self):
        return str(self.a) + "+(" + str(self.b)+")i"

    def __eq__(x,y):
        return x.a == y.a and x.b == y.b

    def __ne__(x,y):
        return not x == y

    def com(x):
        return ZI(x.a, -x.b)

    def num(x, y):
        return ZI((x * y.com()).a, (x * y.com()).b)

    def __div__(x, y):
        n1 = x.num(y).a
        n2 = x.num(y).b
        d = y.a*y.a + y.b*y.b
        comp1 = (n1 + d/2)/d
        comp2 = (n2 + d/2)/d
        return ZI(comp1, comp2)
        return ZI(int(round(float((x.num(y)).a) / (y.a * y.a + y.b * y.b))),
                  int(round(float((x.num(y)).b) / (y.a * y.a + y.b * y.b))))

    def __mod__(x, y):
        return ZI((x - y * (x / y)).a, (x - y * (x / y)).b)

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
    def getUnits():
        return [ZI(1,0),ZI(-1,0),ZI(0,1),ZI(0,-1)]

        

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
        #assert x.h == y.h
        #assert x.w == y.w
        newElements = []
        for i in range(h*w):
            newElements.append(x.elements[i] + y.elements[i])
        return Matrix(x.h, x.w, newElements)

    def __mul__(x, y):
        #assert x.w == y.h
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

    def determinant(self):
    	assert self.h == self.w
    	if (self.h==1):
    		return self.get(0,0)

    	total = type(self.get(0,0)).getZero()
    	for i in range(self.h):
    		scale = self.get(i,0)
    		if (i%2==1):
    			scale = -scale
    		subcontent = []
    		for j in range(self.h):
    			if i == j:
    				continue
    			else:
    				for k in range(1,self.h):
    					subcontent.append(self.get(j,k))
    		total += scale * Matrix(self.h-1, self.h-1, subcontent).determinant()
    	return total
    					
    @staticmethod
    def id(dim, elementType):
        elements = [elementType.getZero() for i in range(dim*dim)]
        for i in range(dim):
            elements[i*dim + i] = elementType.getOne()
        return Matrix(dim, dim, elements)

    def get(self, i, j):
        #assert i>=0 and i<self.h
        #assert j>=0 and j<self.w
        return self.elements[i*self.w + j]

    def set(self, i, j, e):
        #assert i>=0 and i<self.h
        #assert j>=0 and j<self.w
        self.elements[i*self.w + j] = e

    def copy(self):
        return Matrix(self.h, self.w, self.elements[:])

    @staticmethod
    def inputMatrix():
        print "What type is your matrix?"
        print "[0]: Integers"
        print "[1]: Gaussian Integers"
        choice = int(raw_input("> "))

        #-------- Integers -----------#
        if (choice==0):
            print 
            h = int(raw_input("Matrix height: "))
            #assert h>0
            w = int(raw_input("Matrix width:  "))
            #assert w>0
            strElements = raw_input("Please enter the %d space-delineated matrix elements across rows\n"%(h*w)).split(" ")
            strElements = strElements[:h*w]
            print
            contents = []
            for i in range(len(strElements)):
                contents.append(Z(int(strElements[i].strip())))

            return Matrix(h,w,contents)
            

        #----- Gaussian Integers -----#
        elif (choice ==1):
            print 
            h = int(raw_input("Matrix height: "))
            #assert h>0
            w = int(raw_input("Matrix width:  "))
            #assert w>0
            print "Please enter the the contents of the matrix in the following way. Reading across each row from top to bottom enter the real and imaginary component of each gausian integer. Place a space between each gaussian integer component and place a space between each matrix element. Your input should contaid %d components."%(h*w*2)

            strElements = raw_input().split(" ")
            strElements = strElements[:h*w*2]
            contents=[]
            for i in range(len(strElements)/2):
                contents.append(ZI(int(strElements[2*i].strip()),int(strElements[2*i+1].strip())))
            return Matrix(h,w,contents)
        else:
            print "Sorry. That was not a valid selection."
            print


            

# We should find that every through the process S*A*T = J where
# A is the input matrix.
#
# These matrices should only be accessed by the helper methods
# These matrices are defined here so that they are in global 
# scope and can be accessed by the helper methods.

elementT = None;
S = None;
J = None;
T = None;

def cSwap(i,j):
    global elementT, S, J, T, DEBUG
    print "OPERATION: Swapping columns %d and %d"%(i,j)
    #perform the column swap to J
    for k in range(J.h):
        temp = J.get(k, i)
        J.set(k,i,J.get(k,j))
        J.set(k,j, temp)

    #adjust the T matrix
    adjustment = Matrix.id(T.h, elementT)
    adjustment.set(i,i,elementT.getZero())
    adjustment.set(j,j,elementT.getZero())
    adjustment.set(i,j,elementT.getOne())
    adjustment.set(j,i,elementT.getOne())
    T = T*adjustment
    if DEBUG:
        print "adjustment:"
        print adjustment
        print "adjusted T:"
        print T

def cLC(I,i,j,a,b,gcd=None):
    global elementT, S, J, T, DEBUG
    print "OPERATION: Column %d gets %s column %d plus %s column %d"%(i,a,i,b,j)
    #assert a is not 0 and b is not 0
    #perform the linear column application to J
    if gcd is None or a.isUnit():
    	c = elementT.getZero()
    	d = elementT.getOne()
    else:
    	c = -J.get(I,j)/gcd
    	d = J.get(I,i)/gcd

    temp = []
    for k in range(J.h):
    	temp = J.get(k,i)
        J.set(k,i,a*J.get(k,i) + b*J.get(k,j))
        J.set(k,j,c*temp + d*J.get(k,j))

    #adjust the T matrix
    adjustment = Matrix.id(T.h, elementT)
    adjustment.set(i,i,a)
    if i!=j:
        adjustment.set(j,i,b) 
        adjustment.set(i,j,c)
    	adjustment.set(j,j,d)

    assert adjustment.determinant().isUnit()
    T = T*adjustment
    if DEBUG:
        print "adjustment:"
        print adjustment
        print "adjusted T:"
        print T

def rSwap(i,j):
    global elementT, S, J, T, DEBUG
    print "OPERATION: Swapping rows %d and %d"%(i,j)
    #perform the row swap to J
    for k in range(J.w):
        temp = J.get(i, k)
        J.set(i,k,J.get(j,k))
        J.set(j,k, temp)

    #adjust the S matrix
    adjustment = Matrix.id(S.h, elementT)
    adjustment.set(i,j,elementT.getOne())
    adjustment.set(j,i,elementT.getOne())
    adjustment.set(i,i,elementT.getZero())
    adjustment.set(j,j,elementT.getZero())
    S = adjustment*S
    if DEBUG:
        print "adjustment:"
        print adjustment
        print "adjusted S:"
        print S

def rLC(I,i,j,a,b,gcd=None):
    global elementT, A, S, J, T, DEBUG
    print "OPERATION: Row %d gets %s row %d plus %s row %d"%(i,a,i,b,j)
    assert a is not 0 and b is not 0

    if (gcd is None or a.isUnit()):
    	c=elementT.getZero()
    	d=elementT.getOne()
    else:
    	c = -J.get(j,I)/gcd
    	d = J.get(i,I)/gcd

    #perform the linear column application to J
    for k in range(J.w):
    	temp = J.get(i,k)
        J.set(i,k,a*J.get(i,k) + b*J.get(j,k))
        J.set(j,k,c*temp + d*J.get(j,k))

    #adjust the S matrix
    adjustment = Matrix.id(S.h, elementT)
    adjustment.set(i,i,a)
    if i!=j:
        adjustment.set(i,j,b) 
        adjustment.set(j,i,c)
        adjustment.set(j,j,d)
    assert adjustment.determinant().isUnit()
    S = adjustment*S
    if DEBUG:
        print "adjustment:"
        print adjustment
        print "adjusted S:"
        print S

def euclid(a, b):
    # output g, x, y where g = gcd(a,b) = xa + yb
    x0 = type(b).getOne()
    x1 = type(b).getZero()
    y0 = type(b).getZero()
    y1 = type(b).getOne()
    while b != type(b).getZero():
        tempa = a
        tempb = b
        q = tempa / tempb
        a = tempb
        b = tempa % tempb
        tempx0 = x0
        x0 = x1
        x1 = tempx0 - q * x0
        tempy0 = y0
        y0 = y1
        y1 = tempy0 - q * y0
    #assert a is not None
    #assert x0 is not None
    #assert y0 is not None
    return [a, x0, y0]


def snf(A):
    global elementT, J, S, T, DEBUG
    J = A.copy()
    elementT=type(A.get(0,0))

    #assert J is not None
    #assert elementT is not None

    print "Calculating the Smith Normal Form of A..."
    print
    if DEBUG:
        print "J: "
        print J
        print

    S = Matrix.id(A.h, type(A.get(0,0)))
    T = Matrix.id(A.w, type(A.get(0,0)))

    #The heart of snf starts here
    for i in range(min(J.h,J.w)):
        print "\nstarting iteration %d of %d"%(i+1,min(J.h, J.w))
        #if the top-left element of the subarray is 0 we need to
        #perform row/column swaps to move in a different value
        if J.get(i,i) == elementT.getZero():
            #we search for a nonzero entry in the submatrix to replace the
            #zero element with. 
            foundReplacement = False;
            for j in range(i, J.h):
                if foundReplacement:
                    break
                for k in range(i,J.w):
                    if (J.get(j,k) != elementT.getZero()):
                        foundReplacement = True
                        break
            #if there are no non-zero values left to swap in, the algorithm
            #is complete
            if not foundReplacement:
                #assert (J is not None) and (str(J) is not None)
                break
            #perform the swap
            else:
                rSwap(i,j)
                cSwap(i,k)
        #now we should not have a zero in the top-left position
        #of the submatrix
        #assert J.get(i,i) != elementT.getZero()
        #assert (J is not None) and (str(J) is not None)

        #make the top-left submatrix element be the gcd of all the elements
        #in the same row or the same column
        gcd=J.get(i,i)
        doneIteration = False
        while not doneIteration:
            if (J.get(i,i).isUnit()):
                break
            doneIteration = True
            for j in range(i+1, J.h):
                gcd, x, y = euclid(J.get(i,i), J.get(j,i))
                if (gcd < elementT.getZero()):
                    gcd = -gcd
                    x = -x
                    y = -y
                if (DEBUG):
                    print "GCD: %s"%gcd
                    print "TE:  %s"%J.get(i,i)
                if gcd == J.get(i,i):
                    pass
                elif gcd == J.get(j,i):
                    rSwap(i,j)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
                elif gcd == -J.get(j,i):
                    rSwap(i,j)
                    rLC(i,i,i,-elementT.getOne(), elementT.getZero(),gcd)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
                elif gcd < J.get(i,i) or gcd < -J.get(i,i):
                    rLC(i, i, j, x, y, gcd)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
            for j in range(i+1, J.w):
                gcd, x, y = euclid(J.get(i,i), J.get(i,j))
                if (gcd < elementT.getZero()):
                    gcd = -gcd
                    x = -x
                    y = -y
                if DEBUG:
                    print "GCD: %s"%gcd
                    print "TE:  %s"%J.get(i,i)
                if gcd == J.get(i,i):
                    pass
                elif gcd == J.get(i,j):
                    cSwap(i,j)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
                elif gcd == -J.get(i,j): #TODO WORK THIS BLOCK
                    cSwap(i,j)
                    cLC(i,i,i,-elementT.getOne(), elementT.getZero(),gcd)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
                elif gcd < J.get(i,i) or gcd < -J.get(i,i):
                    cLC(i, i, j, x, y, gcd)
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
                    doneIteration=False
        #assert gcd > elementT.getZero()
        #assert gcd == J.get(i,i), "gcd is %s, corner element is %s"%(gcd, J.get(i,i))
        #assert (J is not None) and (str(J) is not None)

        #use the gcd to make all elements int the ith row and the ith
        #column zero by row and column linear combinations
        doneZeroing = False
        while not doneZeroing:
            doneZeroing = True
            for j in range(i+1, J.h):
                if J.get(j,i) != elementT.getZero():
                    rLC(i,j,i,elementT.getOne(),-J.get(j,i)/J.get(i,i))
                    #assert(J.get(j,i) == elementT.getZero()), "Actually: %s\n%s"%(J.get(j,i),A)
                    if J.get(j,i) != elementT.getZero():
                        doneZeroing = False
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 
            for j in range(i+1, J.w):
                if J.get(i,j) != elementT.getZero():
                    cLC(i,j,i,elementT.getOne(),-J.get(i,j)/J.get(i,i))
                    #assert(J.get(i,j) == elementT.getZero()), "Actually: %s\n%s"%(J.get(i,j),A)
                    if J.get(i,j) != elementT.getZero():
                        doneZeroing = False
                    if DEBUG:
                        print "J:"
                        print J
                        print S*A*T
                        print 

    #At this point J is diagonalized. Me simply need to make sure that every
    #diagonal element divides the element after it
    print "\nFIXING DIAGONAL"
    for i in range(min(J.w, J.h)-1):
        #If the next diagonal element is 0, then all following diagonal elements
        #will be 0. Therefore J is in Smith normal form and we return
        if J.get(i+1,i+1) == elementT.getZero():
            return S,J,T
        gcd, x, y = euclid(J.get(i,i), J.get(i+1,i+1))
        #if the ith diagonal element is already the gcd of of the the ith and
        #the (i+1)th diagonal elements, they are correct and we can advance. If
        #they are not we should change the ith element to be the gcd by row
        #operations while maintaining that J is diagonal
        if (gcd == J.get(i+1,i+1)):
            cSwap(i, i+1)
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 
            rSwap(i, i+1)
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 
        elif (gcd != J.get(i,i)):
            rLC(i,i, i+1, elementT.getOne(), elementT.getOne())
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 
            cLC(i, i, i+1, x, y, gcd)
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 
            cLC(i, i+1, i, elementT.getOne(), -J.get(i,i+1)/J.get(i,i))
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 
            rLC(i, i+1, i, elementT.getOne(), -J.get(i+1,i)/J.get(i,i))
            if DEBUG:
                print "J:"
                print J
                print S*A*T
                print 

    #print "MAKING COMPLIMENT MATRICES INVERTIBLE"
    #for i in range(min(J.w, J.h)):
    #	gcd = J.get(i,i)
    #	for j in range(J.h):
    #		gcd = euclid(gcd, S.get(i,j))[0]
    #	if not gcd.isUnit():
    #		for j in range(J.h):
    #			S.set(i,j, S.get(i,j)/gcd)
    #		J.set(i,i,J.get(i,i)/gcd)

    #	gcd = J.get(i,i)
    #	for j in range(J.w):
    #		gcd = euclid(gcd, T.get(j,i))[0]
    #	if not gcd.isUnit():
    #		for j in range(J.w):
    #			T.set(j,i, T.get(j,i)/gcd)
    #		J.set(i,i,J.get(i,i)/gcd)

    return S,J,T

if __name__ == "__main__":

    #contents = [Z(0),Z(-5),Z(10),Z(-10)]
    #A = Matrix(2,2,contents)
    
    A = Matrix.inputMatrix()

    print "\nA:"
    print A
    s,j,t = snf(A)

    print
    print "Smith Normal Form computation complete. Results:"
    print

    print "\nS:"
    print str(s)
    print "T:"
    print str(t)
    print "J:"
    print str(j)
    print "S*A*T"
    print s*A*t
