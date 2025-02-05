import repsig.offline as off
import repsig.streaming as strm
from more_itertools import take
import numpy as np
import numpy.testing as npt

def test_repetition_fraction_equivalence():
    u = 0.1
    n = 100
    expected = off.frac_repetitions(n, u)
    actual = np.array(take(n, strm.frac_repetitions(u)))
    assert np.allclose(expected, actual)


def test_geo_budget():
    w = 0.1
    n = 100
    expected = off.geo_budget(n, w)
    actual = np.array(take(n, strm.geo_budget(w)))
    assert np.allclose(expected, actual)


def test_zeta_budget():
    v = 1.1
    s = 10
    n = 100
    expected = off.zeta_budget(n, v, s)
    actual = np.array(take(n, strm.zeta_budget(v, s)))
    assert np.allclose(expected, actual)