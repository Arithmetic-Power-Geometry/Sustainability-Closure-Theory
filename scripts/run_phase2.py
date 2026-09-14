from pathlib import Path
import math
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sct import Scenario, simulate, cumulative_burden, instantaneous_green_metrics


def analytic_instant_reversal_time(efficiency: float, demand_elasticity: float):
    """
    Closed-form reversal time for the simplified no-feedback/no-exogenous-growth model:
        q_{t+1} = q_t * a,  a = 1 + elasticity * (1-efficiency)
        E_t = efficiency * q_0 * a^(t+1)
        E_baseline = q_0
    Returns the first zero-based t for which candidate instantaneous energy >= baseline.
    """
    g = float(efficiency)
    e = float(demand_elasticity)
    if not (0 < g < 1):
        return 0 if g >= 1 else math.inf
    a = 1.0 + e * (1.0 - g)
    if a <= 1.0:
        return math.inf
    k = math.ceil(math.log(1.0 / g) / math.log(a))
    return max(0, k - 1)


def numeric_instant_reversal_time(efficiency: float, demand_elasticity: float, horizon: int = 5000):
    base = simulate(Scenario("base", horizon=horizon, efficiency=1.0))
    cand = simulate(Scenario("candidate", horizon=horizon, efficiency=efficiency,
                             demand_elasticity=demand_elasticity))
    hit = np.where(cand["energy"].to_numpy() >= base["energy"].to_numpy())[0]
    return math.inf if len(hit) == 0 else int(hit[0])


def cumulative_reversal_time(efficiency: float, demand_elasticity: float, horizon: int = 5000):
    base = simulate(Scenario("base", horizon=horizon, efficiency=1.0))
    cand = simulate(Scenario("candidate", horizon=horizon, efficiency=efficiency,
                             demand_elasticity=demand_elasticity))
    advantage = base["energy"].cumsum().to_numpy() - cand["energy"].cumsum().to_numpy()
    positive = False
    for t, x in enumerate(advantage):
        if x > 0:
            positive = True
        if positive and x <= 0:
            return int(t)
    return math.inf


def static_multi_resource_score(s: Scenario):
    """A pointwise weighted intensity score; does not include future demand response."""
    return (s.efficiency
            + s.efficiency * s.carbon_intensity
            + s.efficiency * s.water_intensity
            + s.material_intensity
            + s.land_intensity
            + s.replacement_intensity)


def run_sweep(out: Path):
    rows = []
    efficiencies = np.round(np.linspace(0.30, 0.90, 13), 3)
    elasticities = np.round(np.linspace(0.00, 0.12, 13), 3)
    horizons = [12, 24, 60, 120]

    for horizon in horizons:
        baseline = Scenario("baseline", horizon=horizon, efficiency=1.0)
        db = simulate(baseline)
        b_energy = float(db["energy"].sum())
        b_burden = cumulative_burden(db)
        b_static = static_multi_resource_score(baseline)

        for g in efficiencies:
            for e in elasticities:
                s = Scenario("candidate", horizon=horizon, efficiency=float(g),
                             demand_elasticity=float(e))
                d = simulate(s)
                energy = float(d["energy"].sum())
                burden = cumulative_burden(d)
                inst_t = analytic_instant_reversal_time(g, e)
                cum_t = cumulative_reversal_time(g, e, horizon=max(500, horizon))
                rows.append({
                    "horizon": horizon,
                    "efficiency": g,
                    "elasticity": e,
                    "energy_ratio": energy / b_energy,
                    "closure_burden_ratio": burden / b_burden,
                    "pointwise_efficiency_says_green": bool(g < 1.0),
                    "static_multi_resource_says_green": bool(static_multi_resource_score(s) < b_static),
                    "closure_says_green": bool(burden < b_burden),
                    "analytic_instant_reversal_t": None if math.isinf(inst_t) else int(inst_t),
                    "cumulative_energy_reversal_t": None if math.isinf(cum_t) else int(cum_t),
                })
    df = pd.DataFrame(rows)
    df.to_csv(out / "phase2_parameter_sweep.csv", index=False)

    disagreement = []
    for horizon, gdf in df.groupby("horizon"):
        eff_false_green = ((gdf["pointwise_efficiency_says_green"]) & (~gdf["closure_says_green"])).mean()
        static_false_green = ((gdf["static_multi_resource_says_green"]) & (~gdf["closure_says_green"])).mean()
        disagreement.append({
            "horizon": horizon,
            "cases": len(gdf),
            "efficiency_false_green_fraction": float(eff_false_green),
            "static_multi_resource_false_green_fraction": float(static_false_green),
            "closure_green_fraction": float(gdf["closure_says_green"].mean()),
        })
    dis = pd.DataFrame(disagreement)
    dis.to_csv(out / "phase2_metric_disagreement.csv", index=False)

    h60 = df[df["horizon"] == 60].pivot(index="elasticity", columns="efficiency",
                                       values="closure_burden_ratio")
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(h60.to_numpy(), aspect="auto", origin="lower")
    ax.set_xticks(range(len(h60.columns)))
    ax.set_xticklabels([f"{x:.2f}" for x in h60.columns], rotation=45, ha="right")
    ax.set_yticks(range(len(h60.index)))
    ax.set_yticklabels([f"{x:.2f}" for x in h60.index])
    ax.set_xlabel("energy per service multiplier g")
    ax.set_ylabel("demand elasticity")
    ax.set_title("SCT closure-burden ratio at horizon 60")
    fig.colorbar(im, ax=ax, label="candidate / baseline closure burden")
    fig.tight_layout()
    fig.savefig(out / "phase2_closure_heatmap_h60.png", dpi=180)
    plt.close(fig)

    return dis


def verify_analytic_boundary(out: Path):
    rows = []
    cases = [(0.4,0.02),(0.4,0.08),(0.55,0.03),(0.55,0.08),
             (0.7,0.04),(0.7,0.10),(0.85,0.05),(0.85,0.12)]
    for g,e in cases:
        a = analytic_instant_reversal_time(g,e)
        n = numeric_instant_reversal_time(g,e)
        rows.append({
            "efficiency":g, "elasticity":e,
            "analytic_t": None if math.isinf(a) else int(a),
            "numeric_t": None if math.isinf(n) else int(n),
            "match": (math.isinf(a) and math.isinf(n)) or a == n
        })
    df = pd.DataFrame(rows)
    df.to_csv(out / "phase2_analytic_boundary_validation.csv", index=False)
    if not bool(df["match"].all()):
        raise AssertionError("Analytic reversal boundary failed numerical validation")
    return df


def family_incompleteness(out: Path):
    """
    Construct a family with identical deployment-time intensity metrics but different
    future response laws. This is a computational witness for the theorem hypothesis.
    """
    rows = []
    g = 0.55
    for e in np.linspace(0.0, 0.12, 25):
        s = Scenario("family", horizon=120, efficiency=g, demand_elasticity=float(e))
        d = simulate(s)
        m = instantaneous_green_metrics(s)
        rows.append({
            "elasticity": e,
            **m,
            "closure_burden": cumulative_burden(d),
            "final_demand": float(d["demand"].iloc[-1])
        })
    df = pd.DataFrame(rows)
    df.to_csv(out / "phase2_incompleteness_family.csv", index=False)

    metric_cols = ["energy_per_service","carbon_per_service","water_per_service"]
    invariant = all(df[c].nunique() == 1 for c in metric_cols)
    closure_varies = df["closure_burden"].nunique() > 1
    if not (invariant and closure_varies):
        raise AssertionError("Family incompleteness construction failed")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(df["elasticity"], df["closure_burden"])
    ax.set_xlabel("demand elasticity")
    ax.set_ylabel("closure burden")
    ax.set_title("Identical pointwise metrics, divergent sustainability closure")
    fig.tight_layout()
    fig.savefig(out / "phase2_incompleteness_family.png", dpi=180)
    plt.close(fig)

    return {
        "family_size": len(df),
        "pointwise_metrics_invariant": True,
        "closure_min": float(df["closure_burden"].min()),
        "closure_max": float(df["closure_burden"].max()),
        "closure_span": float(df["closure_burden"].max()-df["closure_burden"].min())
    }


def main():
    out = Path("results")
    out.mkdir(exist_ok=True)
    boundary = verify_analytic_boundary(out)
    disagreement = run_sweep(out)
    family = family_incompleteness(out)

    summary = {
        "analytic_boundary_cases": int(len(boundary)),
        "analytic_boundary_all_match": bool(boundary["match"].all()),
        "parameter_sweep_cases": int(13*13*4),
        "family_incompleteness": family,
        "metric_disagreement": disagreement.to_dict(orient="records")
    }
    (out / "phase2_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
