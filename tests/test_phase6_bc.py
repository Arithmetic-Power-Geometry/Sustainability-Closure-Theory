import importlib.util
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("phase6bc", ROOT/"scripts"/"run_phase6_bc_external_ablation.py")
phase6bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase6bc)


def test_pairwise_tradeoff_detection():
    df = pd.DataFrame([
        {"States":"A", "PUE":1.10, "WUE":1.80},
        {"States":"B", "PUE":1.20, "WUE":1.50},
    ])
    rev = phase6bc.pairwise_order_reversals(df)
    assert len(rev) == 1
    assert rev.iloc[0]["pue_preferred"] != rev.iloc[0]["wue_preferred"]


def test_pareto_frontier_keeps_tradeoff_points():
    df = pd.DataFrame([
        {"PUE":1.10, "WUE":1.80},
        {"PUE":1.20, "WUE":1.50},
        {"PUE":1.30, "WUE":1.90},
    ])
    keep = phase6bc.nondominated_indices(df.PUE.to_numpy(), df.WUE.to_numpy())
    assert set(keep) == {0, 1}


def test_observation_refinement_changes_some_rankings():
    df = pd.DataFrame([
        {"States":"A", "Size":100, "Year":2025, "PUE":1.10, "WUE":1.80},
        {"States":"B", "Size":100, "Year":2025, "PUE":1.20, "WUE":1.50},
        {"States":"C", "Size":200, "Year":2026, "PUE":1.15, "WUE":1.60},
    ])
    out = phase6bc.observation_ablation(df)
    assert (out["rank_shift_location"] > 0).any()
    assert (out["rank_shift_water"] > 0).any()
