import numpy as np
import math
from scipy.special import erfc

def stdnorm_cdf(z):
    return erfc(-z / math.sqrt(2)) / 2.


def pvalues_from_z(z_scores):
    return 1 - stdnorm_cdf(z_scores)


def ztest_with_repetitions(z_scores, budgets, repetitions, alpha=0.05, two_sided=True):
    """Performs a Z-test with repeated significance for an unbounded test with multiple decision
    points.

    Parameters
    ----------
    z_scores: array-like
        The z-scores of the all the decision points, up until the current one.
    budgets: array-like
        The significance budget allocations for every decision point.
    repetitions: array-like
        The required number of repeated significance at each decision point.
    alpha: float
        The the upper-bound on the type-1 (false positive) error.
    two_sided: bool
        Specifies whether the test is two or one-sided.

    Returns: bool
        Has the null-hypothesis been rejected.
    """
    z_scores = np.asarray(z_scores)
    if two_sided:
        alpha /= 2
        p_values = pvalues_from_z(np.abs(z_scores))
    else:
        p_values = pvalues_from_z(z_scores)

    actual_repetitions = np.cumsum(p_values <= alpha * budgets * repetitions)
    return np.any(actual_repetitions >= repetitions)

