import numpy as np
import scipy
import scipy.special
import math

def frac_repetitions(n, u=0.1):
    r"""Computes significance repetition requirement at each decision point that is a constant
    fraction of the number of decision points at each time.

    Parameters:
    n: int
        The number of decision points we used up until now.
    u: float
        The fraction of the number of decision points to use as the repetition requirement. Must be between 0 and 1.
    """
    return np.ceil(np.arange(1, 1 + n) * u).astype(np.int32)

def geo_budget(n, w):
    r"""Computes budget allocation for n out of infinity decision points using a fraction proportional
    to :math:`w \cdot w^(t - 1)`.

    Parameters
    ----------
    n: int
        The number of decision points to we used up until now.
    w: float
        The 'withdrawal rate' of the geometric series.

    Returns: array-like
        The sequence of budget fractions out of the total significance budget to use at every decision point.
    """
    arr = np.ones(n) * w
    arr[1:] = 1 - arr[1:]
    return np.cumprod(arr)

def auto_geo_budget(n, n_target):
    r"""Computes budget allocation for n out of infinity decision points using a fraction proportional
    to :math:`w \cdot w^(t - 1)`, with the weight :math:`w` being chosen automatically to so that the
    z-statistic requirement is least stringent at a given decision point.

    Useful mainly when we know, in advance, that we aim to make a decision at a specific point,
    but want to be able to make a decision at any point.

    Parameters
    ----------
    n: int
        The number of decision points to we used up until now.
    n_target: int
        The decision point we aim for.

    Returns: array-like
        The sequence of budget fractions out of the total significance budget to use at every decision point.
    """
    w = 1 - math.exp(-1/n_target)
    return geo_budget(n, w)


def zeta_budget(n, v=1.1, s=10):
    r"""Computes budget allocation for n out of infinity decision points using fraction roughly proportional to :math:`\frac{1}{t^v}`.

    Parameters
    ----------
    n: int
        Number of decision points we already passed
    v: float
        The :math:`v` parameter in the formula above. (default=1.1)
    s: float
        A smoothness parameter. Higher value allows a flatter significance allocation curve. (default=10)

    Returns: array-like
        The sequence of budget fractions out of the total significance budget to use at every decision point.
    """
    zeta = scipy.special.zeta(v)
    head = np.sum(np.reciprocal(np.power(np.arange(1, 1 + s), v)))
    denominator = (zeta - head) * np.power(np.arange(1, 1 + n) + s, v)
    return np.reciprocal(denominator)