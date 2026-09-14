from pathlib import Path
import argparse
import json
import pandas as pd

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

def analyze(puewue_path, constructions_path, out_dir="results"):
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    pue = pd.read_csv(puewue_path)
    con = pd.read_csv(constructions_path, encoding="utf-8-sig")
    con["States"] = con["State"].map(STATE_ABBR)
    joined = con.merge(pue[["States","PUE","WUE"]], on="States", how="inner")
    rows = []
    for size, group in joined.groupby("Size"):
        if group["State"].nunique() < 2:
            continue
        rows.append({
            "reported_size": float(size),
            "projects": int(len(group)),
            "states": int(group["State"].nunique()),
            "pue_range": float(group["PUE"].max() - group["PUE"].min()),
            "wue_range": float(group["WUE"].max() - group["WUE"].min()),
            "pue_nonidentifying": bool(group["PUE"].nunique() > 1),
            "wue_nonidentifying": bool(group["WUE"].nunique() > 1),
        })
    groups = pd.DataFrame(rows)
    if len(groups):
        groups = groups.sort_values(["states","projects"], ascending=[False,False])
    joined.to_csv(out / "phase6_joined_projects.csv", index=False)
    groups.to_csv(out / "phase6_equal_size_groups.csv", index=False)
    summary = {
        "source_projects": int(len(con)),
        "joined_projects": int(len(joined)),
        "equal_size_multistate_groups": int(len(groups)),
        "groups_with_pue_variation": int(groups["pue_nonidentifying"].sum()) if len(groups) else 0,
        "groups_with_wue_variation": int(groups["wue_nonidentifying"].sum()) if len(groups) else 0,
        "interpretation": "Holding the source-reported Size field fixed can still leave state-conditioned PUE/WUE unresolved. Size is treated only as an observed source field; no undocumented physical unit is inferred."
    }
    (out / "phase6_summary.json").write_text(json.dumps(summary, indent=2))
    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puewue", required=True)
    parser.add_argument("--constructions", required=True)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()
    print(json.dumps(analyze(args.puewue, args.constructions, args.out), indent=2))

if __name__ == "__main__":
    main()
