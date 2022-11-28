import math
import operator as op
import platform
import typing as tp
from functools import reduce

_numbers = platform.python_version().split(".")


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom


if int(_numbers[1]) < 8:
    comb = ncr
else:
    comb = math.comb


def bezier(flat_points: tp.List[float], dim: int, step: tp.Optional[int] = None) -> tp.List[float]:
    # flat_points: [x0, y0, x1, y1, x2, y2, ... xn, yn]
    n = len(flat_points) // dim - 1
    if step is None:
        step = n * 10

    bc = []
    for t_ in range(0, step):
        t = t_ / (step - 1)
        dim_value = [0] * dim
        for i in range(n + 1):
            other = comb(n, i) * math.pow(1 - t, n - i) * math.pow(t, i)
            p_ = flat_points[i * dim: (i + 1) * dim]
            for j in range(dim):
                dim_value[j] += p_[j] * other
        bc.extend(dim_value)
    return bc
