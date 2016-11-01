from snf import Z,ZI,Matrix,snf,S,T
from random import randint

def Z_factor1_test():
	assert Z(18).factor() ==[Z(2),Z(3),Z(3)]

def Z_factor2_test():
	assert Z(135).factor() ==[Z(3),Z(3),Z(3),Z(5)]

def Z_factor3_test():
	assert Z(2054).factor() ==[Z(2),Z(13),Z(79)]

def trivial_test():
    assert True

def matrixZ_mult1_test():
    Z(4)
    A = Matrix(3,2,[Z(3), Z(4), Z(5), Z(1), Z(-2), Z(0)])
    B = Matrix(2,3,[Z(0), Z(1), Z(2), Z(-17), Z(4), Z(3)])
    C = Matrix(3,3,[Z(-68), Z(19), Z(18), Z(-17), Z(9), Z(13), Z(0), Z(-2), Z(-4)])
    assert A*B == C

def getSquareIdentity_test():
    assert Matrix.id(2, type(Z(1))) == Matrix(2, 2, [Z(1), Z(0), Z(0), Z(1)])

def random20_test():
    for run in range(10):
        
        r = []

        h = randint(4,10)
        w = randint(4,10)
        contents = []
        for i in range(h*w):
            contents.append(ZI(randint(-100,100), randint(-100,100)))
        A = Matrix(h,w,contents)
        s,j,t = snf(A)
        assert s*A*t==j
        print A
        print j

