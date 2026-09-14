from sct import *

def test_same_metrics_different_future():
    a = Scenario("A", efficiency=0.55, demand_elasticity=0.0)
    b = Scenario("B", efficiency=0.55, demand_elasticity=0.03)
    assert instantaneous_green_metrics(a) == instantaneous_green_metrics(b)
    assert cumulative_burden(simulate(b)) > cumulative_burden(simulate(a))

def test_efficiency_initially_reduces_energy():
    base = simulate(Scenario("base", efficiency=1.0))
    eff = simulate(Scenario("eff", efficiency=0.6))
    assert eff.loc[0, "energy"] < base.loc[0, "energy"]

def test_burden_migration():
    x = simulate(Scenario("x", efficiency=0.65, carbon_intensity=0.2, water_intensity=0.75))
    y = simulate(Scenario("y", efficiency=0.65, carbon_intensity=0.45, water_intensity=0.15))
    assert x["carbon"].sum() < y["carbon"].sum()
    assert x["water"].sum() > y["water"].sum()

def test_latest_intervention_time():
    s = Scenario("lock", efficiency=0.6, demand_elasticity=0.03, infrastructure_feedback=0.00003)
    no = simulate(s)
    immediate = simulate(s, intervention_time=0, intervention_strength=1.0)
    max_rec = cumulative_burden(no) - cumulative_burden(immediate)
    tstar = latest_effective_intervention_time(s, 0.35 * max_rec)
    assert tstar is not None
    assert 0 <= tstar < s.horizon

def test_reversal_exists_in_constructed_case():
    b = simulate(Scenario("base", efficiency=1.0))
    c = simulate(Scenario("cand", efficiency=0.55, demand_elasticity=0.08))
    t = reversal_time(b, c)
    assert t != float("inf")
