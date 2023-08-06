import pytest

import more_bisect
from more_bisect.more_bisect import _validate_args


def test__validate_args():
    a, lo, hi = _validate_args([1, 2], None, None, None)
    assert lo == 0
    assert hi == 2
    assert a[0] == 1 and a[1] == 2
    with pytest.raises(IndexError):
        _ = a[2]

    a, lo, hi = _validate_args([('a', 1), ('a', 2)], None, 1,
                               key=lambda x: x[1])
    assert lo == 0
    assert hi == 1
    assert a[0] == 1 and a[1] == 2
    with pytest.raises(IndexError):
        _ = a[2]

    a = [1, 2]
    a_, lo, hi = _validate_args(None, 0, 1, lambda i: a[i])
    assert lo == 0
    assert hi == 1
    assert a_[0] == 1 and a_[1] == 2
    with pytest.raises(IndexError):
        _ = a_[2]

    a = [('a', 1), ('a', 2)]
    a_, lo, hi = _validate_args(None, 0, 1, lambda i: a[i][1])
    assert lo == 0
    assert hi == 1
    assert a_[0] == 1 and a_[1] == 2
    with pytest.raises(IndexError):
        _ = a_[2]


def revlst(x):
    return list(reversed(x))


def test_first_pos_eq():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.first_pos_eq(3, a)
    assert pos == 1
    pos = more_bisect.first_pos_eq(-3, revlst(a), key=lambda x: -x)
    assert pos == 7
    a = [2, 3]
    assert more_bisect.first_pos_eq(3, a) == 1
    a = [3, 4]
    assert more_bisect.first_pos_eq(3, a) == 0
    a = []
    assert more_bisect.first_pos_eq(3, a) is None
    a = [1, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_eq(3, a) is None


def test_first_pos_eq_called_with_fakearray():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.first_pos_eq(3, lo=0, hi=len(a), key=lambda i: a[i])
    assert pos == 1


def test_last_pos_eq():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.last_pos_eq(3, a)
    assert pos == 4
    pos = more_bisect.last_pos_eq(-3, revlst(a), key=lambda x: -x)
    assert pos == 10
    a = [2, 3]
    assert more_bisect.last_pos_eq(3, a) == 1
    a = [3, 4]
    assert more_bisect.last_pos_eq(3, a) == 0
    a = []
    assert more_bisect.last_pos_eq(3, a) is None
    a = [1, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_eq(3, a) is None


def test_last_pos_eq_called_with_fakearray():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.last_pos_eq(3, lo=0, hi=len(a), key=lambda i: a[i])
    assert pos == 4


def test_last_pos_lt():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_lt(3, a) == 0
    a = [3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_lt(3, a) is None
    a = [2, 3]
    assert more_bisect.last_pos_lt(3, a) == 0
    a = [3, 4]
    assert more_bisect.last_pos_lt(3, a) is None
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_lt(3, a) == 3


def test_last_pos_le():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_le(3, a) == 4
    a = [3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_le(3, a) == 3
    a = [4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_le(3, a) is None
    a = [2, 3]
    assert more_bisect.last_pos_le(3, a) == 1
    a = [3, 4]
    assert more_bisect.last_pos_le(3, a) == 0
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_le(3, a) == 7


def test_last_pos_le_called_with_fakearray():
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_le(3, lo=0, hi=len(a), key=lambda i: a[i]) == 7


def test_first_pos_gt():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_gt(3, a) == 5
    a = [1, 3, 3, 3, 3]
    assert more_bisect.first_pos_gt(3, a) is None
    a = [2, 3]
    assert more_bisect.first_pos_gt(3, a) is None
    a = [3, 4]
    assert more_bisect.first_pos_gt(3, a) == 1
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_gt(3, a) == 8


def test_first_pos_ge():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_ge(3, a) == 1
    a = [1, 3, 3, 3, 3]
    assert more_bisect.first_pos_ge(3, a) == 1
    a = [1]
    assert more_bisect.first_pos_ge(3, a) is None
    a = [2, 3]
    assert more_bisect.first_pos_ge(3, a) == 1
    a = [3, 4]
    assert more_bisect.first_pos_ge(3, a) == 0
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_ge(3, a) == 4


def test_bisect_left():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_left(3, a) == 1
    pos = more_bisect.bisect_left(-3, revlst(a), key=lambda x: -x)
    assert pos == 7
    a = [2, 3]
    assert more_bisect.bisect_left(3, a) == 1
    assert more_bisect.bisect_left(4, a) == 2
    a = [3, 4]
    assert more_bisect.bisect_left(3, a) == 0
    a = []
    assert more_bisect.bisect_left(3, a) == 0
    a = [1, 2, 2, 2, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_left(3, a) == 4
    pos = more_bisect.bisect_left(-3, revlst(a), key=lambda x: -x)
    assert pos == 9
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_left(3, a) == 4


def test_bisect_left_called_with_fakearray():
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_left(3, lo=0, hi=len(a), key=lambda i: a[i]) == 4


def test_bisect_right():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_right(3, a) == 5
    pos = more_bisect.bisect_right(-3, revlst(a), key=lambda x: -x)
    assert pos == 11
    a = [2, 3]
    assert more_bisect.bisect_right(2, a) == 1
    assert more_bisect.bisect_right(3, a) == 2
    assert more_bisect.bisect_right(4, a) == 2
    a = [3, 4]
    assert more_bisect.bisect_right(3, a) == 1
    a = []
    assert more_bisect.bisect_right(3, a) == 0
    a = [1, 2, 2, 2, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_right(3, a) == 4
    pos = more_bisect.bisect_right(-3, revlst(a), key=lambda x: -x)
    assert pos == 9
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.bisect_right(3, a) == 8


def test_last_closest_to():
    a = [2, 3, 4]
    assert more_bisect.last_closest_to(1, a) == 0
    pos = more_bisect.last_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 2
    a = [-2, -1, 0]
    assert more_bisect.last_closest_to(1, a) == 2
    pos = more_bisect.last_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 0
    a = [-2, -1, 0, 1, 3, 4]
    assert more_bisect.last_closest_to(1, a) == 3
    pos = more_bisect.last_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 2
    a = [-2, -1, 0, 3, 4, 5]
    assert more_bisect.last_closest_to(1, a) == 2
    pos = more_bisect.last_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 3
    a = [-2, -1, 0, 1, 1, 1, 3, 4]
    assert more_bisect.last_closest_to(1, a) == 5
    pos = more_bisect.last_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 4


def test_first_closest_to():
    a = [2, 3, 4]
    assert more_bisect.first_closest_to(1, a) == 0
    pos = more_bisect.first_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 2
    a = [-2, -1, 0]
    assert more_bisect.first_closest_to(1, a) == 2
    pos = more_bisect.first_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 0
    a = [-2, -1, 0, 1, 3, 4]
    assert more_bisect.first_closest_to(1, a) == 3
    pos = more_bisect.first_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 2
    a = [-2, -1, 0, 3, 4, 5]
    assert more_bisect.first_closest_to(1, a) == 2
    pos = more_bisect.first_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 3
    a = [-2, -1, 0, 1, 1, 1, 3, 4]
    assert more_bisect.first_closest_to(1, a) == 3
    pos = more_bisect.first_closest_to(-1, revlst(a), key=lambda x: -x)
    assert pos == 2
