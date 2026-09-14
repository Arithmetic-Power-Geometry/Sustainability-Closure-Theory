from scripts.run_phase5_clca_killtest import fully_informed_consequential_score, restricted_consequential_score
from sct import Scenario, simulate, cumulative_burden


def test_full_information_equivalence():
    s = Scenario('x', horizon=80, efficiency=0.6, demand_elasticity=0.04, replacement_feedback=0.2)
    d = simulate(s)
    assert fully_informed_consequential_score(d) == cumulative_burden(d)


def test_restricted_model_can_omit_future_burden():
    s = Scenario('x', horizon=120, efficiency=0.6, demand_elasticity=0.01, replacement_feedback=0.30)
    d = simulate(s)
    assert restricted_consequential_score(s) < cumulative_burden(d)
