from snf import z
from snf import zi

class Matrix():
    def __init__(self, h, w, elements):
        self.h = h
        self.w = w
        self.elements = elements

    def __add__(x, y):
        newElements = []
        for i in range(h*w):
            newElements.append(x.elements[i] + y.elements[i])
        return Matrix(x.h, x.w, newElements)

    def __mul__(x, y):
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
        print("What type is your matrix?")
        print("[0]: Integers")
        print("[1]: Gaussian Integers")
        choice = int(input("> "))

        #-------- Integers -----------#
        if (choice==0):
            print 
            h = int(input("Matrix height: "))
            #assert h>0
            w = int(input("Matrix width:  "))
            #assert w>0
            strElements = input("Please enter the %d space-delineated matrix elements across rows\n"%(h*w)).split(" ")
            strElements = strElements[:h*w]
            print()
            contents = []
            for i in range(len(strElements)):
                contents.append(z.Z(int(strElements[i].strip())))

            return Matrix(h,w,contents)
            

        #----- Gaussian Integers -----#
        elif (choice ==1):
            print ()
            h = int(input("Matrix height: "))
            #assert h>0
            w = int(input("Matrix width:  "))
            #assert w>0
            print("Please enter the the contents of the matrix in the following way. Reading across each row from top to bottom enter the real and imaginary component of each gausian integer. Place a space between each gaussian integer component and place a space between each matrix element. Your input should contaid %d components."%(h*w*2))

            strElements = input().split(" ")
            strElements = strElements[:h*w*2]
            contents=[]
            for i in range(len(strElements)//2):
                contents.append(zi.ZI(int(strElements[2*i].strip()),int(strElements[2*i+1].strip())))
            return Matrix(h,w,contents)
        else:
            print("Sorry. That was not a valid selection.")
            print()
