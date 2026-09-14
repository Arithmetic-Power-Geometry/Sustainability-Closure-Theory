from pathlib import Path
import importlib.util
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("phase6", ROOT / "scripts" / "run_phase6_external.py")
phase6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase6)

def test_equal_size_multistate_group_is_detected(tmp_path):
    pue = pd.DataFrame({
        "States": ["Iowa", "Nebraska"],
        "PUE": [1.10, 1.20],
        "WUE": [1.40, 1.60],
    })
    con = pd.DataFrame({
        "Company": ["A", "B"],
        "Project name": ["P1", "P2"],
        "State": ["IA", "NE"],
        "Size": [100, 100],
        "Year": [2025, 2025],
        "Estimated or not": ["", ""],
    })
    pue_path = tmp_path / "pue.csv"
    con_path = tmp_path / "con.csv"
    pue.to_csv(pue_path, index=False)
    con.to_csv(con_path, index=False)
    summary = phase6.analyze(pue_path, con_path, tmp_path / "out")
    assert summary["equal_size_multistate_groups"] == 1
    assert summary["groups_with_pue_variation"] == 1
    assert summary["groups_with_wue_variation"] == 1
