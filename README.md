# Unbounded A/B tests via repeated significance
This library contains utilities to rigorously reject a null hypothesis in an unbounded A/B test by allocating the total significance budget $\alpha$, which is typically $5\%$, over a unbounded sequence of decision point, and requiring repeated z-statistic above the required thresholds multiple times.

# Offline variant
We have implemented an easy to use offline version of our methodology, useful for plotting and testing quickly. Here, it is assumed we have a history of Z-statistics at all previous decision points, and want to make
a decision at the current point.

Here is an example:
```python
from repsig.offline import ztest_with_repetitions, zeta_budget, frac_repetitions

z_statistics = get_history_of_z_statistics()
n_decision_points = len(z_statistics)

is_null_rejected = ztest_with_repetitions(
    z_statistics,
    zeta_budget(n_decision_points),
    frac_repetitions(n_decision_points),
    alpha=0.05
)
```

As we gather more information about A/B, we can re-run the code, and when the null is rejected,
we have a rigoroous statistical guarantee for making a type-1 error with probability at most 5%
over _the entire sequence_ of decision points.

# Streaming variant
In an actual online case, we do not have vectors of bounded length describing the budget and the Z-score history - we just observe the current Z-score at each decision point, over an unbounded sequence of decision points. From a mathematical perspective, our methods do not require the entire history, and thus we have also implemented a "streaming" variant:
```python
from repsig.streaming import ZTest, zeta_budget, frac_repetitions

ztest = ZTest(zeta_budget(), frac_repetitions())
while True:
    z_statistic = fetch_next_decision_point_z_statistic()
    ztest.submit(z_statistic)
    if ztest.is_rejected():
        print('B is different from A! Hooray!')
        break
```