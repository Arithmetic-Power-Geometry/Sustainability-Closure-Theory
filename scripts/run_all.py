from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from sct import *

def save_line(df, cols, path, title, ylabel):
    fig, ax = plt.subplots(figsize=(7, 4))
    for c in cols:
        ax.plot(df["t"], df[c], label=c)
    ax.set_title(title)
    ax.set_xlabel("time step")
    ax.set_ylabel(ylabel)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)

def metric_incompleteness(out):
    a = Scenario("A_stable", efficiency=0.55, demand_elasticity=0.0)
    b = Scenario("B_induced", efficiency=0.55, demand_elasticity=0.03, infrastructure_feedback=0.00002)
    assert instantaneous_green_metrics(a) == instantaneous_green_metrics(b)
    da, db = simulate(a), simulate(b)
    ba, bb = cumulative_burden(da), cumulative_burden(db)
    pd.DataFrame([
        {"system":"A", **instantaneous_green_metrics(a), "closure_burden":ba},
        {"system":"B", **instantaneous_green_metrics(b), "closure_burden":bb}
    ]).to_csv(out/"metric_incompleteness.csv", index=False)
    m = pd.DataFrame({"t": da["t"], "A_energy": da["energy"], "B_energy": db["energy"]})
    save_line(m, ["A_energy","B_energy"], out/"metric_incompleteness.png",
              "Same instantaneous metrics, different future", "energy")
    return {"same_metrics": True, "burden_gap": bb-ba}

def reversal(out):
    base = Scenario("baseline", efficiency=1.0)
    cand = Scenario("efficient_but_induced", efficiency=0.55, demand_elasticity=0.08)
    d0, d1 = simulate(base), simulate(cand)
    tr = reversal_time(d0, d1)
    pd.DataFrame([{
        "baseline_burden": cumulative_burden(d0),
        "candidate_burden": cumulative_burden(d1),
        "reversal_time": tr
    }]).to_csv(out/"reversal.csv", index=False)
    m = pd.DataFrame({"t": d0["t"], "baseline_energy":d0["energy"], "candidate_energy":d1["energy"]})
    save_line(m, ["baseline_energy","candidate_energy"], out/"reversal.png",
              "Environmental reversal under induced demand", "energy")
    return {"reversal_time": tr}

def burden_migration(out):
    x = Scenario("X", efficiency=0.65, carbon_intensity=0.20, water_intensity=0.75)
    y = Scenario("Y", efficiency=0.65, carbon_intensity=0.45, water_intensity=0.15)
    dx, dy = simulate(x), simulate(y)
    rows = [
        {"system":"X","carbon_total":dx["carbon"].sum(),"water_total":dx["water"].sum()},
        {"system":"Y","carbon_total":dy["carbon"].sum(),"water_total":dy["water"].sum()}
    ]
    pd.DataFrame(rows).to_csv(out/"burden_migration.csv", index=False)
    return {"carbon_prefers_X": bool(rows[0]["carbon_total"] < rows[1]["carbon_total"]),
            "water_prefers_Y": bool(rows[1]["water_total"] < rows[0]["water_total"])}

def delayed_intervention(out):
    s = Scenario("lock_in", efficiency=0.60, demand_elasticity=0.03,
                 infrastructure_feedback=0.00003, replacement_feedback=0.003)
    no = simulate(s)
    immediate = simulate(s, intervention_time=0, intervention_strength=1.0)
    max_rec = cumulative_burden(no) - cumulative_burden(immediate)
    threshold = 0.35 * max_rec
    tstar = latest_effective_intervention_time(s, threshold)
    rows = []
    for tau in range(s.horizon):
        acted = simulate(s, intervention_time=tau, intervention_strength=1.0)
        rec = cumulative_burden(no) - cumulative_burden(acted)
        rows.append({"tau":tau,"recoverable_burden":rec})
    rdf = pd.DataFrame(rows)
    rdf.to_csv(out/"delayed_intervention.csv", index=False)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(rdf["tau"], rdf["recoverable_burden"])
    ax.axhline(threshold, linestyle="--")
    if tstar is not None:
        ax.axvline(tstar, linestyle=":")
    ax.set_title("Recoverability declines with delayed intervention")
    ax.set_xlabel("intervention time")
    ax.set_ylabel("recoverable burden")
    fig.tight_layout()
    fig.savefig(out/"delayed_intervention.png", dpi=180)
    plt.close(fig)
    return {"t_star":tstar,"minimum_recovery":threshold,"max_recoverable":max_rec}

def debt_demo(out):
    s = Scenario("debt_demo", efficiency=0.65, demand_elasticity=0.05)
    d = simulate(s)
    boundaries = {"energy":80, "carbon":30, "water":18, "materials":5, "land":2, "replacement":3}
    debt = sustainability_debt(d, boundaries)
    pd.DataFrame([{"sustainability_debt":debt}]).to_csv(out/"sustainability_debt.csv", index=False)
    return {"sustainability_debt":debt}

def run_all():
    out = Path("results"); out.mkdir(exist_ok=True)
    summary = {
        "metric_incompleteness": metric_incompleteness(out),
        "reversal": reversal(out),
        "burden_migration": burden_migration(out),
        "delayed_intervention": delayed_intervention(out),
        "debt_demo": debt_demo(out)
    }
    (out/"summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    run_all()
