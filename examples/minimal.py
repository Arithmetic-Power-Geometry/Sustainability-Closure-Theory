from sct import Scenario, simulate, cumulative_burden

baseline = Scenario("baseline")
candidate = Scenario("candidate", efficiency=0.55, demand_elasticity=0.02)

print(cumulative_burden(simulate(baseline)))
print(cumulative_burden(simulate(candidate)))
