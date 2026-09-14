import math
from scripts.run_phase2 import analytic_instant_reversal_time, numeric_instant_reversal_time


def test_analytic_instant_reversal_matches_numeric():
    for g,e in [(0.4,0.02),(0.55,0.08),(0.7,0.1),(0.85,0.12)]:
        assert analytic_instant_reversal_time(g,e) == numeric_instant_reversal_time(g,e)


def test_no_reversal_without_induced_growth():
    assert math.isinf(analytic_instant_reversal_time(0.55,0.0))
