import repsig.offline as off
import repsig.streaming as strm
import numpy as np
import pytest


@pytest.mark.parametrize('seed', range(100))
def test_repetition_fraction_equivalence(seed):
    # generate observations
    n = 100
    rng = np.random.default_rng(seed)
    observations = 0.5 + rng.standard_normal(n)
    indices = np.arange(1, 1 + n)

    # cumulative means, standard deviations, and z-statistics - each obversation is a decision point
    cum_means = np.cumsum(observations) / indices
    z_statistics = np.sqrt(indices) * cum_means

    # find the first decision point where the streaming Z-Test rejects the null
    streaming_ztest = strm.ZTest(strm.auto_geo_budget(n / 2), strm.frac_repetitions())
    streaming_rejection_index = None
    for i, z_stat in enumerate(z_statistics, 1):
        streaming_ztest.submit(z_stat)
        if streaming_ztest.is_rejected():
            streaming_rejection_index = i
            break

    # find the first decision point where the offline Z-Test rejects the null
    offline_rejection_index = None
    for i in range(1, 1 + n):
        offline_is_rejected = off.ztest_with_repetitions(z_statistics[:i], off.auto_geo_budget(i, n / 2), off.frac_repetitions(i))
        if offline_is_rejected:
            offline_rejection_index = i
            break

    # assert that the two implementations agree
    assert streaming_rejection_index == offline_rejection_index
