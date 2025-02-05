import math
from math import erfc

class ZTest:
    r"""
    Performs a Z-test with repeated significance for an unbounded test with multiple decision points, by dividing
    the significance budget among the decision points, and requiring a certain number of repeated significance occurances.
    """

    def __init__(self, budget, repetitions, alpha=0.05, two_sided=True):
        r"""
        Parameters
        ----------
        budget: Sequence
            An unbounded generator that yields the significance budget allocations for every decision point.
        repetitions: Sequence
            An unbounded generator that yields the required number of repeated significance at each decision point.
        alpha: float
            The the upper-bound on the type-1 (false positive) error.
        two_sided: bool
            Specifies whether the test is two or one-sided
        """
        self._required_repetition_iterator = iter(repetitions)
        self._alpha_budget_iterator = iter(budget)
        self._alpha = alpha
        self._two_sided = two_sided
        self._significance_repetitions = 0
        self._rejected = False

    def stdnorm_cdf(self, z):
        return erfc(-z / math.sqrt(2)) / 2.

    def pvalue_from_z(self, zscore):
        zscore = abs(zscore)
        return 1 - self.stdnorm_cdf(zscore)

    def submit(self, z_score):
        repetitions_threshold = next(self._required_repetition_iterator)
        alpha_budget = next(self._alpha_budget_iterator)

        p_value = self.pvalue_from_z(z_score)
        if p_value < alpha_budget * self._significance_threshold() * repetitions_threshold:
            self._significance_repetitions += 1
            if self._significance_repetitions >= repetitions_threshold:
                self._rejected = True

    def is_rejected(self):
        return self._rejected

    def _significance_threshold(self):
        if self._two_sided:
            return self._alpha / 2
        else:
            return self._alpha
