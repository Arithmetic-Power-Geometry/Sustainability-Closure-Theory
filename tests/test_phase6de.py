import importlib.util
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("p6de",ROOT/"scripts"/"run_phase6de_robustness.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_baseline_has_external_ordering_reversal():
    df=m.load_witness()
    assert len(m.baseline_pairs(df)) >= 1

def test_zero_perturbation_preserves_structure():
    s,_,b=m.run_sensitivity(n=30,seed=7)
    r=s[s["sigma"]==0.0].iloc[0]
    assert r["prob_any_pairwise_reversal"] == 1.0
    assert r["mean_baseline_reversal_survival"] == 1.0
    assert r["prob_baseline_pareto_front_preserved"] == 1.0

def test_weight_choice_can_change_winner():
    df=m.load_witness()
    p=df["pue"].to_numpy(float); w=df["wue"].to_numpy(float)
    wins={m.weighted_winner(p,w,a) for a in np.linspace(0,1,21)}
    assert len(wins) >= 2
