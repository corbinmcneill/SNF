import pytest
from smithnormalform import pid, z


def test_int_creation():
    a = 10
    zObject = z.Z(a)
    assert(zObject.a == a)


def test_str_creation():
    a = "10"
    zObject = z.Z(a)
    assert(zObject.a == int(a))


def test_list_creation():
    a = [10]
    zObject = z.Z(a)
    assert(zObject.a == a[0])


def test_bad_string_creation():
    a = "hello"
    with pytest.raises(pid.InvalidInitialContent):
        z.Z(a)


def test_bad_list_creation():
    a = [10, 12]
    with pytest.raises(pid.InvalidInitialContent):
        z.Z(a)


def test_bad_type_creation():
    a = 2.0
    with pytest.raises(pid.InvalidInitialContent):
        z.Z(a)


def test_eq_neq():
    original = z.Z(2)
    same = z.Z(2)
    different = z.Z(3)

    assert(original == same)
    assert(not (original == different))
    assert(original != different)
    assert(not (original != same))


def test_lt_gt_simple():
    negative = z.Z(-1)
    positive = z.Z(2)
    positive_again = z.Z(2)

    assert(negative < positive)
    assert(positive > negative)
    assert(not positive < negative)
    assert(not negative > positive)

    assert(not positive > positive_again)
    assert(not positive < positive_again)
    assert(not positive_again > positive)
    assert(not positive_again < positive)

    assert(not positive < positive)
    assert(not positive > positive)


def test_lt_gt_is_using_norm():
    negative = z.Z(-10)
    positive = z.Z(2)

    assert(negative > positive)
    assert(positive < negative)


def test_string():
    pos = 2
    positive = z.Z(pos)
    assert(str(positive) == str(pos))

    neg = -3
    negative = z.Z(neg)
    assert(str(negative) == str(neg))


def test_negation():
    a = 12
    negA = -a

    zObject = z.Z(a)
    zNegObject = -zObject

    assert(zNegObject.a == negA)


def test_addition():
    a = 1
    b = -5
    c = a + b

    zObjectA = z.Z(a)
    zObjectB = z.Z(b)
    zObjectC = zObjectA + zObjectB

    assert(zObjectC.a == c)


def test_subtraction():
    a = 5
    b = 7
    c = a - b

    aObject = z.Z(a)
    bObject = z.Z(b)
    cObject = aObject - bObject

    assert(cObject.a == c)


def test_multiplication():
    a = 3
    b = -4
    c = a * b

    zObjectA = z.Z(a)
    zObjectB = z.Z(b)
    zObjectC = zObjectA * zObjectB

    assert(zObjectC.a == c)


def test_floordiv():
    a = 5
    b = -3
    c = -2  # defining c here to be extra clear about the intended behaviour

    aObject = z.Z(a)
    bObject = z.Z(b)
    cObject = z.Z(c)

    assert(aObject // bObject == cObject)


def test_mod():
    a = 5
    b = -3
    c = -1  # defining c here to be extra clear about the intended behaviour

    aObject = z.Z(a)
    bObject = z.Z(b)
    cObject = z.Z(c)

    assert(aObject % bObject == cObject)


def test_is_unit():
    assert(z.Z(1).isUnit())
    assert(z.Z(-1).isUnit())
    assert(not z.Z(2).isUnit())
    assert(not z.Z(-5).isUnit())
    assert(not (-z.Z(3)).isUnit())
