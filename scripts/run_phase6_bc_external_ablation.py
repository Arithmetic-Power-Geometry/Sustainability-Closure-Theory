from pathlib import Path
import argparse
import hashlib
import io
import json
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data" / "external"

UPSTREAM_COMMIT = "7f47a7c5bac252a88c81a1dbd9b874246714b1fc"
PUEWUE_PATH = "Data/Baseline_PUEWUE.csv"
CONSTRUCTION_PATH = "Data/AI data center constructions.csv"
PUEWUE_BLOB = "be2151d0cb6e3f04058d563950a5c7db9be2d1bc"
CONSTRUCTION_BLOB = "f4292fca7685ba19b4fbafc10e5343fcdaa049ca"

STATE_ABBR = {
    "AL":"Alabama","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
    "CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida",
    "GA":"Georgia","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
    "KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland",
    "MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi",
    "MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire",
    "NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina",
    "ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania",
    "SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas",
    "UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia",
    "WI":"Wisconsin","WY":"Wyoming"
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def fetch_pinned(path: str, expected_blob: str) -> bytes:
    url = (
        "https://raw.githubusercontent.com/PEESEgroup/US-AI-Server-Analysis/"
        + UPSTREAM_COMMIT + "/" + urllib.parse.quote(path)
    )
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
    got = git_blob_sha1(data)
    if got != expected_blob:
        raise RuntimeError(f"integrity failure for {path}: {got} != {expected_blob}")
    return data


def load_full():
    p = pd.read_csv(io.BytesIO(fetch_pinned(PUEWUE_PATH, PUEWUE_BLOB)))
    c = pd.read_csv(io.BytesIO(fetch_pinned(CONSTRUCTION_PATH, CONSTRUCTION_BLOB)), encoding="utf-8-sig")
    c["States"] = c["State"].map(STATE_ABBR)
    j = c.merge(p[["States", "PUE", "WUE", "PUE_ALC", "WUE_ALC"]], on="States", how="inner")
    return p, c, j


def load_snapshot():
    d = pd.read_csv(DATA / "peese_equal_size_witness.csv")
    d["States"] = d["state_abbr"].map(STATE_ABBR)
    d = d.rename(columns={"pue":"PUE", "wue":"WUE", "reported_size":"Size", "year":"Year"})
    return d


def nondominated_indices(x, y):
    keep = []
    for i in range(len(x)):
        dominated = False
        for k in range(len(x)):
            if k == i:
                continue
            if (x[k] <= x[i] and y[k] <= y[i]) and (x[k] < x[i] or y[k] < y[i]):
                dominated = True
                break
        if not dominated:
            keep.append(i)
    return keep


def pairwise_order_reversals(df):
    rows = []
    values = df[["States","PUE","WUE"]].drop_duplicates().reset_index(drop=True)
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            a, b = values.iloc[i], values.iloc[j]
            pue_pref = np.sign(a.PUE - b.PUE)
            wue_pref = np.sign(a.WUE - b.WUE)
            if pue_pref != 0 and wue_pref != 0 and pue_pref != wue_pref:
                rows.append({
                    "state_a": a.States, "state_b": b.States,
                    "pue_a": a.PUE, "pue_b": b.PUE,
                    "wue_a": a.WUE, "wue_b": b.WUE,
                    "pue_preferred": a.States if a.PUE < b.PUE else b.States,
                    "wue_preferred": a.States if a.WUE < b.WUE else b.States,
                })
    return pd.DataFrame(rows)


def observation_ablation(joined):
    # No undocumented physical interpretation of Size is made. We use it only as a source-reported
    # project magnitude proxy and test rankings under progressively richer observation interfaces.
    d = joined.copy()
    d = d.dropna(subset=["Size","Year","PUE","WUE","States"])
    d["size_rank"] = d["Size"].rank(method="average", pct=True)
    d["pue_rank"] = d["PUE"].rank(method="average", pct=True)
    d["wue_rank"] = d["WUE"].rank(method="average", pct=True)

    # Three declared assessment interfaces. These are normalized ranking scores, not physical footprints.
    d["score_size_only"] = d["size_rank"]
    d["score_size_plus_pue"] = 0.5*d["size_rank"] + 0.5*d["pue_rank"]
    d["score_size_plus_pue_wue"] = (d["size_rank"] + d["pue_rank"] + d["wue_rank"])/3.0

    d["rank_size_only"] = d["score_size_only"].rank(method="average")
    d["rank_size_plus_pue"] = d["score_size_plus_pue"].rank(method="average")
    d["rank_full_observed"] = d["score_size_plus_pue_wue"].rank(method="average")

    d["rank_shift_location"] = (d["rank_size_plus_pue"] - d["rank_size_only"]).abs()
    d["rank_shift_water"] = (d["rank_full_observed"] - d["rank_size_plus_pue"]).abs()
    return d


def yearly_proxy_trajectory(df):
    # A trajectory of observed source fields and normalized intensity proxies. It is explicitly not an
    # energy/carbon/water footprint trajectory because Size has no unit assumed here.
    d = df.copy().dropna(subset=["Year","Size","PUE","WUE"])
    d["pue_weighted_proxy"] = d["Size"] * d["PUE"]
    d["wue_weighted_proxy"] = d["Size"] * d["WUE"]
    g = d.groupby("Year", as_index=False).agg(
        projects=("Size","size"),
        reported_size_sum=("Size","sum"),
        pue_weighted_proxy=("pue_weighted_proxy","sum"),
        wue_weighted_proxy=("wue_weighted_proxy","sum"),
        states=("States","nunique"),
    )
    return g.sort_values("Year")


def run(joined, mode):
    RESULTS.mkdir(exist_ok=True)
    states = joined[["States","PUE","WUE"]].drop_duplicates().dropna().reset_index(drop=True)
    rev = pairwise_order_reversals(states)
    rev.to_csv(RESULTS/f"phase6bc_{mode}_pue_wue_order_reversals.csv", index=False)

    pareto_idx = nondominated_indices(states.PUE.to_numpy(), states.WUE.to_numpy())
    pareto = states.iloc[pareto_idx].sort_values(["PUE","WUE"])
    pareto.to_csv(RESULTS/f"phase6bc_{mode}_pue_wue_pareto.csv", index=False)

    ab = observation_ablation(joined)
    ab.to_csv(RESULTS/f"phase6bc_{mode}_observation_ablation.csv", index=False)

    traj = yearly_proxy_trajectory(joined)
    traj.to_csv(RESULTS/f"phase6bc_{mode}_yearly_proxy_trajectory.csv", index=False)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.scatter(states.PUE, states.WUE)
    ax.scatter(pareto.PUE, pareto.WUE, marker="x")
    ax.set_xlabel("PUE")
    ax.set_ylabel("WUE")
    ax.set_title("External PUE-WUE trade-offs and Pareto states")
    fig.tight_layout()
    fig.savefig(RESULTS/f"phase6bc_{mode}_pue_wue_tradeoff.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(traj.Year, traj.reported_size_sum, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("sum of upstream Size field")
    ax.set_title("Externally observed construction trajectory")
    fig.tight_layout()
    fig.savefig(RESULTS/f"phase6bc_{mode}_construction_trajectory.png", dpi=180)
    plt.close(fig)

    summary = {
        "mode": mode,
        "projects": int(len(joined)),
        "states": int(states.States.nunique()),
        "pairwise_pue_wue_order_reversals": int(len(rev)),
        "pareto_states": int(len(pareto)),
        "projects_with_location_rank_shift": int((ab.rank_shift_location > 0).sum()),
        "projects_with_water_rank_shift": int((ab.rank_shift_water > 0).sum()),
        "median_abs_rank_shift_after_pue": float(ab.rank_shift_location.median()),
        "median_abs_rank_shift_after_wue": float(ab.rank_shift_water.median()),
        "years": [int(x) for x in traj.Year.tolist()],
        "scientific_scope": (
            "The analysis tests observation refinement and order instability using external source fields. "
            "It does not convert the upstream Size field into physical energy, carbon, or water quantities."
        )
    }
    (RESULTS/f"phase6bc_{mode}_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    args = ap.parse_args()
    if args.full:
        _, _, joined = load_full()
        run(joined, "full")
    else:
        run(load_snapshot(), "snapshot")

if __name__ == "__main__":
    main()
