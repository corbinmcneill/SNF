import z
import zi
import matrix

DEBUG = False

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
    adjustment = matrix.Matrix.id(T.h, elementT)
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
    adjustment = matrix.Matrix.id(T.h, elementT)
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
    adjustment = matrix.Matrix.id(S.h, elementT)
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
    adjustment = matrix.Matrix.id(S.h, elementT)
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

    S = matrix.Matrix.id(A.h, type(A.get(0,0)))
    T = matrix.Matrix.id(A.w, type(A.get(0,0)))

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
    #A = matrix.Matrix(2,2,contents)
    
    A = matrix.Matrix.inputMatrix()

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
