from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
import pandas as pd

DIMS = ("energy", "carbon", "water", "materials", "land", "replacement")

@dataclass(frozen=True)
class Scenario:
    name: str
    horizon: int = 60
    base_demand: float = 100.0
    efficiency: float = 1.0
    demand_elasticity: float = 0.0
    demand_growth: float = 0.0
    carbon_intensity: float = 0.4
    water_intensity: float = 0.25
    material_intensity: float = 0.03
    land_intensity: float = 0.01
    replacement_intensity: float = 0.02
    infrastructure_feedback: float = 0.0
    replacement_feedback: float = 0.0

def simulate(s: Scenario, intervention_time: Optional[int] = None,
             intervention_strength: float = 0.0) -> pd.DataFrame:
    rows = []
    q = float(s.base_demand)
    cumulative_infra = 0.0
    for t in range(s.horizon):
        active = intervention_time is not None and t >= intervention_time
        strength = intervention_strength if active else 0.0
        elastic = max(0.0, s.demand_elasticity * (1.0 - 0.75 * strength))
        infra_fb = max(0.0, s.infrastructure_feedback * (1.0 - 0.85 * strength))
        repl_fb = max(0.0, s.replacement_feedback * (1.0 - 0.80 * strength))
        gain = max(0.0, 1.0 - s.efficiency)
        induced = elastic * gain
        q *= (1.0 + s.demand_growth + induced + infra_fb * cumulative_infra)

        energy = q * s.efficiency
        carbon = energy * s.carbon_intensity
        water = energy * s.water_intensity
        materials = q * s.material_intensity * (1.0 + infra_fb * (t + 1))
        land = q * s.land_intensity * (1.0 + 0.5 * infra_fb * (t + 1))
        replacement = q * s.replacement_intensity * (1.0 + repl_fb * (t + 1))

        cumulative_infra += materials / max(s.base_demand, 1e-12)
        rows.append({
            "t": t, "demand": q, "energy": energy, "carbon": carbon,
            "water": water, "materials": materials, "land": land,
            "replacement": replacement
        })
    return pd.DataFrame(rows)

def cumulative_burden(df: pd.DataFrame, weights: Dict[str, float] | None = None) -> float:
    if weights is None:
        weights = {d: 1.0 for d in DIMS}
    return float(sum(weights.get(d, 0.0) * df[d].sum() for d in DIMS))

def sustainability_debt(df: pd.DataFrame, boundaries: Dict[str, float],
                        weights: Dict[str, float] | None = None) -> float:
    if weights is None:
        weights = {d: 1.0 for d in DIMS}
    total = 0.0
    for d in DIMS:
        if d in boundaries:
            total += weights.get(d, 0.0) * float(np.maximum(df[d].to_numpy() - boundaries[d], 0.0).sum())
    return total

def green_horizon(baseline: pd.DataFrame, candidate: pd.DataFrame,
                  weights: Dict[str, float] | None = None) -> float:
    if weights is None:
        weights = {d: 1.0 for d in DIMS}
    base = np.zeros(len(baseline))
    cand = np.zeros(len(candidate))
    for d in DIMS:
        w = weights.get(d, 0.0)
        base += w * baseline[d].to_numpy().cumsum()
        cand += w * candidate[d].to_numpy().cumsum()
    advantage = base - cand
    positive_seen = False
    for i, a in enumerate(advantage):
        if a > 0:
            positive_seen = True
        if positive_seen and a <= 0:
            return float(i)
    return float("inf")

def reversal_time(baseline: pd.DataFrame, candidate: pd.DataFrame,
                  weights: Dict[str, float] | None = None) -> float:
    return green_horizon(baseline, candidate, weights)

def recoverable_burden(s: Scenario, no_action: pd.DataFrame, tau: int,
                       intervention_strength: float = 1.0,
                       weights: Dict[str, float] | None = None) -> float:
    acted = simulate(s, intervention_time=tau, intervention_strength=intervention_strength)
    return cumulative_burden(no_action, weights) - cumulative_burden(acted, weights)

def latest_effective_intervention_time(s: Scenario, min_recovery: float,
                                       intervention_strength: float = 1.0,
                                       weights: Dict[str, float] | None = None) -> int | None:
    no_action = simulate(s)
    feasible = []
    for tau in range(s.horizon):
        if recoverable_burden(s, no_action, tau, intervention_strength, weights) >= min_recovery:
            feasible.append(tau)
    return max(feasible) if feasible else None

def instantaneous_green_metrics(s: Scenario) -> Dict[str, float]:
    return {
        "energy_per_service": s.efficiency,
        "carbon_per_service": s.efficiency * s.carbon_intensity,
        "water_per_service": s.efficiency * s.water_intensity,
    }
