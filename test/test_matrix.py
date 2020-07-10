import pytest
from smithnormalform import matrix, z


def test_create_matrix():
    matrix.Matrix(2, 1, [z.Z(3), z.Z(4)])


def test_invalid_create():
    with pytest.raises(matrix.InvalidNumberOfElements):
        matrix.Matrix(2, 2, [z.Z(3), z.Z(4)])


def test_eq_neq():
    m1 = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    m2 = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])

    assert(m1 == m2)
    assert(not m1 != m2)


def test_eq_neq_dim():
    m1 = matrix.Matrix(2, 1, [z.Z(3), z.Z(4)])
    m2 = matrix.Matrix(1, 2, [z.Z(3), z.Z(4)])

    assert(m1 != m2)
    assert(not m1 == m2)


def test_eq_neq_contents():
    m1 = matrix.Matrix(2, 1, [z.Z(3), z.Z(3)])
    m2 = matrix.Matrix(1, 2, [z.Z(3), z.Z(4)])

    assert(m1 != m2)
    assert(not m1 == m2)


def test_add_z():
    m1 = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    m2 = matrix.Matrix(2, 2, [z.Z(3), z.Z(-4), z.Z(-1), z.Z(2)])
    m3 = matrix.Matrix(2, 2, [z.Z(4), z.Z(-2), z.Z(2), z.Z(6)])

    assert(m1 + m2 == m3)


def test_add_raise_exception():
    m1 = matrix.Matrix(2, 1, [z.Z(3), z.Z(4)])
    m2 = matrix.Matrix(1, 2, [z.Z(3), z.Z(4)])
    with pytest.raises(matrix.IncompatibleMatrixSizesException):
        m1+m2


def test_mult():
    a = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    b = matrix.Matrix(2, 3, [z.Z(3), z.Z(-4), z.Z(-1), z.Z(2), z.Z(4), z.Z(5)])
    c = matrix.Matrix(2, 3, [z.Z(7), z.Z(4), z.Z(9), z.Z(17), z.Z(4), z.Z(17)])
    assert(a * b == c)


def test_mul_raise_exception():
    a = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    b = matrix.Matrix(3, 2, [z.Z(3), z.Z(-4), z.Z(-1), z.Z(2), z.Z(4), z.Z(5)])

    with pytest.raises(matrix.IncompatibleMatrixSizesException):
        a * b


def test_determinant_2x2():
    m = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    assert(m.determinant() == z.Z(-2))


def test_determinant_3x3():
    contents = list(map(z.Z, [1, 2, 3, 4, 5, 6, 7, 8, 20]))
    m = matrix.Matrix(3, 3, contents)

    assert(m.determinant() == z.Z(-33))


def test_determinant_raise_exception():
    m = matrix.Matrix(2, 3, [z.Z(1), z.Z(2), z.Z(3), z.Z(4), z.Z(3), z.Z(4)])
    with pytest.raises(matrix.MatrixNotSquareException):
        m.determinant()


def test_str():
    m = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    mString = "[1 2]\n[3 4]\n"
    assert(str(m) == mString)
