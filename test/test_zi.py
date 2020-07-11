from smithnormalform import pid, zi
import pytest


def test_str_creation():
    a = "-5+3i"
    ziObject = zi.ZI(a)
    assert(ziObject.a == -5)
    assert(ziObject.b == 3)


def test_list_creation():
    a = [10, 12]
    ziObject = zi.ZI(a)
    assert(ziObject.a == a[0])
    assert(ziObject.b == a[1])


def test_bad_string_creation():
    a = "hello"
    with pytest.raises(pid.InvalidInitialContent):
        zi.ZI(a)


def test_bad_list_creation():
    a = [10, 12, 13]
    with pytest.raises(pid.InvalidInitialContent):
        zi.ZI(a)


def test_bad_type_creation():
    a = 2.0
    with pytest.raises(pid.InvalidInitialContent):
        zi.ZI(a)


def test_eq_neq():
    original = zi.ZI([2, 1])
    same = zi.ZI([2, 1])
    different = zi.ZI([3, 1])

    assert(original == same)
    assert(not (original == different))
    assert(original != different)
    assert(not (original != same))


def test_lt_gt_simple():
    negative = zi.ZI([-1, -2])
    positive = zi.ZI([2, 3])
    positive_again = zi.ZI([2, 3])

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


def test_lt_gt_using_norm():
    large = zi.ZI([-100, -100])
    small = zi.ZI([4, 2])
    assert(large > small)
    assert(small < large)


def test_string():
    assert(str(zi.ZI([4, -3])) == "4-3i")
    assert(str(zi.ZI([0, 3])) == "3i")
    assert(str(zi.ZI([-1, 0])) == "-1")
    assert(str(zi.ZI([0, 0])) == "0")


def test_negation():
    ziObject = zi.ZI([5, -12])

    assert(-ziObject == zi.ZI([-5, 12]))


def test_addition():
    ziObjectA = zi.ZI([4, -3])
    ziObjectB = zi.ZI([1, 6])
    ziObjectC = ziObjectA + ziObjectB

    assert(ziObjectC == zi.ZI([5, 3]))


def test_subtraction():
    ziObjectA = zi.ZI([4, -3])
    ziObjectB = zi.ZI([1, 6])
    ziObjectC = ziObjectA - ziObjectB

    assert(ziObjectC == zi.ZI([3, -9]))


def test_multiplication():
    ziObjectA = zi.ZI([2, -3])
    ziObjectB = zi.ZI([1, 4])
    ziObjectC = ziObjectA * ziObjectB

    assert(ziObjectC == zi.ZI([2*1 - (-3*4), 2*4 + (-3*1)]))


def test_floordiv():
    assert(zi.ZI([2, 0]) // zi.ZI([1, 0]) == zi.ZI([2, 0]))
    assert(zi.ZI([2, 0]) // zi.ZI([-1, 0]) == zi.ZI([-2, 0]))


def test_mod():
    # these tests might be problematic
    #
    # it's difficult to verify by hand that a different
    # remainder wouldn't be equally acceptable
    assert(zi.ZI([6, 4]) % zi.ZI([2, 1]) == zi.ZI([0, 1]))
    assert(zi.ZI([3, 4]) % zi.ZI([1, 2]) == zi.ZI([1, 0]))
    assert(zi.ZI([6, -8]) % zi.ZI([2, -3]) == zi.ZI([0, 1]))


def test_is_unit():
    assert(zi.ZI([1, 0]).isUnit())
    assert(zi.ZI([-1, 0]).isUnit())
    assert(zi.ZI([0, 1]).isUnit())
    assert(zi.ZI([0, -1]).isUnit())

    assert(not zi.ZI([2, 0]).isUnit())
    assert(not zi.ZI([1, -5]).isUnit())
    assert(not (-zi.ZI([1, 1])).isUnit())
