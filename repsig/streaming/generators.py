import math
import scipy
import numpy as np

def frac_repetitions(u=0.1):
    """Yields a stream of significance repetition requirement at each decision point that is a constant
    fraction of the number of decision points at each time.

    Parameters:
    u: float
        The fraction of the number of decision points to use as the repetition requirement. Must be between 0 and 1.
    """
    i = 1
    while True:
        yield math.ceil(i * u)
        i += 1


def geo_budget(w):
    r"""Yields a stream of budget allocation for n out of infinity decision points using a fraction proportional
    to :math:`w \cdot w^(t - 1)`

    Parameters
    ----------
    w: float
        The 'withdrawal rate' of the geometric series.
    """
    result = w
    while True:
        yield result
        result *= (1 - w)


def auto_geo_budget(n_target):
    """Yields a stream of budget allocation for n out of infinity decision points using a fraction proportional
    to :math:w \cdot w^(t - 1):math, with the weight :math:w:math: being chosen automatically to so that the
    z-statistic requirement is least stringent at a given decision point.

    Useful mainly when we know, in advance, that we aim to make a decision at a specific point,
    but want to be able to make a decision at any point.

    Parameters
    ----------
    n_target: int
        The decision point we aim for.

    Returns: array-like
        The sequence of budget fractions out of the total significance budget to use at every decision point.
    """
    w = 1 - math.exp(-1/n_target)
    return geo_budget(w)


def zeta_budget(v=1.1, s=10):
    """Computes budget allocation for n out of infinity decision points using fraction roughly proportional to :math:\frac{1}{t^v}:math.

    Parameters
    ----------
    n: int
        Number of decision points we already passed
    v: float
        The `v` parameter in the formula above. (default=1.1)
    s: float
        A smoothness parameter. Higher value allows a flatter significance allocation curve. (default=10)

    Returns: array-like
        The sequence of budget fractions out of the total significance budget to use at every decision point.
    """
    zeta = scipy.special.zeta(v)
    head = np.sum(np.reciprocal(np.power(np.arange(1, 1 + s), v)))
    i = 1
    while True:
        denominator = (zeta - head) * math.pow(i + s, v)
        yield 1 / denominator
        i += 1