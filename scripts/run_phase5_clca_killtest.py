from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sct import Scenario, simulate, cumulative_burden

DIMS = ("energy", "carbon", "water", "materials", "land", "replacement")

def fully_informed_consequential_score(df, weights=None):
    """
    Strongest comparator: a fully informed consequential/dynamic inventory that
    observes the exact same future consequence trajectory and applies the same
    aggregation as SCT. Under this deliberately matched information set, it must
    equal SCT cumulative burden. This is a scientific kill test, not a weak baseline.
    """
    return cumulative_burden(df, weights)

def restricted_consequential_score(s: Scenario, horizon=None, weights=None):
    """
    A restricted consequential approximation that propagates endogenous demand
    and operational resource use but omits replacement-feedback amplification.
    It represents a causal/dynamic comparator with an incomplete consequence graph.
    """
    h = s.horizon if horizon is None else horizon
    restricted = Scenario(
        name=s.name + "_restricted",
        horizon=h,
        base_demand=s.base_demand,
        efficiency=s.efficiency,
        demand_elasticity=s.demand_elasticity,
        demand_growth=s.demand_growth,
        carbon_intensity=s.carbon_intensity,
        water_intensity=s.water_intensity,
        material_intensity=s.material_intensity,
        land_intensity=s.land_intensity,
        replacement_intensity=s.replacement_intensity,
        infrastructure_feedback=s.infrastructure_feedback,
        replacement_feedback=0.0,
    )
    return cumulative_burden(simulate(restricted), weights)

def experiment_full_information_equivalence(out: Path):
    rows = []
    for efficiency in [0.4, 0.55, 0.7, 0.85]:
        for elasticity in [0.0, 0.02, 0.06, 0.10]:
            for replacement_feedback in [0.0, 0.05, 0.15, 0.30]:
                s = Scenario(
                    "candidate",
                    horizon=120,
                    efficiency=efficiency,
                    demand_elasticity=elasticity,
                    replacement_feedback=replacement_feedback,
                    infrastructure_feedback=0.00002,
                )
                d = simulate(s)
                sct = cumulative_burden(d)
                oracle = fully_informed_consequential_score(d)
                rows.append({
                    "efficiency": efficiency,
                    "elasticity": elasticity,
                    "replacement_feedback": replacement_feedback,
                    "sct_score": sct,
                    "fully_informed_consequential_score": oracle,
                    "absolute_difference": abs(sct-oracle),
                })
    df = pd.DataFrame(rows)
    df.to_csv(out/"phase5_full_information_equivalence.csv", index=False)
    max_diff = float(df["absolute_difference"].max())
    if max_diff > 1e-10:
        raise AssertionError("Full-information comparator should equal SCT under matched aggregation.")
    return {
        "cases": int(len(df)),
        "max_absolute_difference": max_diff,
        "equivalent_under_matched_information": True,
    }

def experiment_information_ablation(out: Path):
    """
    Hold observable deployment intensities and demand response fixed while varying
    an omitted future-state mechanism. Compare:
      1) restricted consequential model,
      2) fully informed consequential model,
      3) SCT.
    The fully informed comparator and SCT coincide; the restricted causal model
    becomes non-identifying when the omitted mechanism matters.
    """
    base = Scenario("baseline", horizon=120, efficiency=1.0)
    base_full = cumulative_burden(simulate(base))
    rows = []
    for rf in np.round(np.linspace(0.0, 0.40, 81), 3):
        s = Scenario(
            "candidate",
            horizon=120,
            efficiency=0.60,
            demand_elasticity=0.01,
            replacement_feedback=float(rf),
        )
        d = simulate(s)
        sct = cumulative_burden(d)
        full = fully_informed_consequential_score(d)
        restricted = restricted_consequential_score(s)
        rows.append({
            "replacement_feedback": rf,
            "baseline_score": base_full,
            "restricted_score": restricted,
            "full_consequential_score": full,
            "sct_score": sct,
            "restricted_green": bool(restricted < base_full),
            "full_green": bool(full < base_full),
            "sct_green": bool(sct < base_full),
            "restricted_error_fraction": float((restricted-full)/full),
        })
    df = pd.DataFrame(rows)
    df.to_csv(out/"phase5_information_ablation.csv", index=False)

    mismatch = df[df["restricted_green"] != df["full_green"]]
    mismatch.to_csv(out/"phase5_restricted_mismatches.csv", index=False)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(df["replacement_feedback"], df["restricted_score"]/df["baseline_score"], label="restricted consequential")
    ax.plot(df["replacement_feedback"], df["full_consequential_score"]/df["baseline_score"], label="fully informed consequential")
    ax.axhline(1.0, linestyle="--")
    ax.set_xlabel("replacement feedback")
    ax.set_ylabel("candidate / baseline burden")
    ax.set_title("Information ablation: causal model vs full consequence closure")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out/"phase5_information_ablation.png", dpi=180)
    plt.close(fig)

    return {
        "cases": int(len(df)),
        "restricted_vs_full_verdict_mismatches": int(len(mismatch)),
        "first_mismatch_feedback": None if mismatch.empty else float(mismatch["replacement_feedback"].iloc[0]),
        "full_and_sct_always_match": bool((df["full_green"] == df["sct_green"]).all()),
    }

def experiment_observation_refinement(out: Path):
    rows = []
    for rf in [0.0, 0.10, 0.20, 0.25, 0.30, 0.40]:
        s = Scenario("candidate", horizon=120, efficiency=0.60,
                     demand_elasticity=0.01, replacement_feedback=rf)
        d = simulate(s)
        restricted = restricted_consequential_score(s)
        refined = cumulative_burden(d)
        rows.append({
            "replacement_feedback": rf,
            "restricted": restricted,
            "refined_full": refined,
            "sct": cumulative_burden(d),
            "refinement_gap": refined-restricted,
        })
    df = pd.DataFrame(rows)
    df.to_csv(out/"phase5_observation_refinement.csv", index=False)
    return {
        "cases": int(len(df)),
        "max_refinement_gap": float(df["refinement_gap"].abs().max()),
        "refined_equals_sct": bool(np.allclose(df["refined_full"], df["sct"])),
    }

def main():
    out = Path("results")
    out.mkdir(exist_ok=True)
    summary = {
        "full_information_equivalence": experiment_full_information_equivalence(out),
        "information_ablation": experiment_information_ablation(out),
        "observation_refinement": experiment_observation_refinement(out),
        "scientific_conclusion": (
            "SCT must not claim superiority over a fully informed consequential/dynamic LCA "
            "that observes the same complete consequence trajectory and uses the same aggregation. "
            "Under matched information, the two are equivalent by construction. The surviving SCT "
            "contribution is therefore formal: it makes observation sufficiency, non-identifiability, "
            "closure completeness, and missing-consequence diagnostics explicit. Its advantage appears "
            "when a declared assessment interface omits a future-response mechanism."
        )
    }
    (out/"phase5_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
