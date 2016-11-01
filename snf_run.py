from snf import Z,ZI,Matrix,snf,S,T
from random import randint

def random20_test():
    r = []

    h = randint(5,5)
    w = randint(5,5)
    contents = []
    for i in range(h*w):
        contents.append(ZI(randint(-10,10), randint(-10,10)))
    A = Matrix(h,w,contents)
    s,j,t = snf(A)
    assert s*A*t==j
    print A
    print
    print j

random20_test()
