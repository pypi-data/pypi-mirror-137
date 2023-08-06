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


from more_bisect.more_bisect import (
    first_pos_eq,
    last_pos_eq,
    last_pos_lt,
    last_pos_le,
    first_pos_gt,
    first_pos_ge,
    bisect_left,
    bisect_right,
    last_closest_to,
    first_closest_to,
)
