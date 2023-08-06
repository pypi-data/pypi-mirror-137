"""
Description of the parameter list ``(x, a=None, lo=None, hi=None, key=None)``
=============================================================================

``x`` is the target to search. ``a`` is the array to search. ``lo`` is the
index (inclusive) to start searching. ``hi`` is the index (exclusive) to stop
searching. ``key`` is a unary function (described below).

If ``a`` is provided not ``None``, ``a`` should be an array. ``key`` is used
to compute a comparison key out of ``a[i]``. If ``key`` is ``None``, ``key``
will be default to an identity function ``lambda x: x``. ``lo`` is default to
0 and ``hi`` default to ``len(a)``.

If ``a`` is provided ``None``, ``lo``, ``hi`` and ``key`` must be provided not
``None``. Now ``key`` is used to compute a comparison key out of index ``i``
in each round of loop.

Example
=======

- ``(2, [1, 2, 3], lo=0, hi=1)`` searches [1] for 2.
- ``(2, [('a', 1), ('b', 2), ('a', 3)], key=lambda x: x[1])`` searches
  [1, 2, 3] for 2
- ``(2, lo=1, hi=3, key=lambda i: [1, 2, 3][i])`` searches [2, 3] for 2
"""


import bisect


__all__ = [
    'first_pos_eq',
    'last_pos_eq',
    'last_pos_lt',
    'last_pos_le',
    'first_pos_gt',
    'first_pos_ge',
    'bisect_left',
    'bisect_right',
    'last_closest_to',
    'first_closest_to',
]


class FakeArray:
    def __init__(self, f):
        self.f = f

    def __getitem__(self, index):
        return self.f(index)

    def __repr__(self):
        return 'FakeArray({!r})'.format(self.f)


class MappedArray:
    def __init__(self, a, f):
        self.a = a
        self.f = f

    def __len__(self):
        return len(self.a)

    def __getitem__(self, index):
        return self.f(self.a[index])


def _validate_args(a, lo, hi, key):
    if a is None:
        if lo is None or hi is None or key is None:
            raise ValueError('`lo`, `hi`, `key` must not be None when `a` '
                             'is None')
        a = FakeArray(key)
    else:
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(a)
        if key is not None:
            a = MappedArray(a, key)
    return a, lo, hi


def first_pos_eq(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is equal to ``x`` within [``lo``, ``hi``), and that ``i`` is
    the smallest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_left(a, x, lo, hi)
    if i != hi and a[i] == x:
        return i
    return None


def last_pos_eq(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is equal to ``x`` within [``lo``, ``hi``), and that ``i`` is
    the largest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_right(a, x, lo, hi)
    if i != lo and a[i - 1] == x:
        return i - 1
    return None


def last_pos_lt(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is less than ``x`` within [``lo``, ``hi``), and that ``i`` is
    the largest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_left(a, x, lo, hi)
    if i != lo:
        return i - 1
    return None


def last_pos_le(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is less than or equal to ``x`` within [``lo``, ``hi``), and that
    ``i`` is the largest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_right(a, x, lo, hi)
    if i != lo:
        return i - 1
    return None


def first_pos_gt(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is greater than ``x`` within [``lo``, ``hi``), and that ``i`` is
    the smallest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_right(a, x, lo, hi)
    if i != hi:
        return i
    return None


def first_pos_ge(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is greater than or equal to ``x`` within [``lo``, ``hi``), and
    that ``i`` is the smallest. If no such index is found, returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = bisect.bisect_left(a, x, lo, hi)
    if i != hi:
        return i
    return None


def bisect_left(x, a=None, lo=None, hi=None, key=None):
    """
    Identical to ``bisect.bisect_left``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    return bisect.bisect_left(a, x, lo, hi)


def bisect_right(x, a=None, lo=None, hi=None, key=None):
    """
    Identical to ``bisect.bisect_right``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    return bisect.bisect_right(a, x, lo, hi)


def last_closest_to(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is the closest to ``x`` within [``lo``, ``hi``), and that ``i``
    is the largest. If the range defined by ``lo`` and ``hi`` is empty,
    returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = first_pos_gt(x, a, lo, hi, None)
    if i is None:
        return hi - 1
    if i == lo:
        return lo
    if abs(a[i - 1] - x) < abs(a[i] - x):
        return i - 1
    return i


def first_closest_to(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is the closest to ``x`` within [``lo``, ``hi``), and that ``i``
    is the smallest. If the range defined by ``lo`` and ``hi`` is empty,
    returns ``None``.
    """
    a, lo, hi = _validate_args(a, lo, hi, key)
    if lo >= hi:
        return None
    i = last_pos_lt(x, a, lo, hi, None)
    if i is None:
        return lo
    if i == hi - 1:
        return hi - 1
    if abs(a[i + 1] - x) < abs(a[i] - x):
        return i + 1
    return i
