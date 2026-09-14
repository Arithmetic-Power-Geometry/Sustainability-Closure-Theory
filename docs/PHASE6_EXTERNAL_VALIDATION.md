# Phase VI — Externally Grounded Validation

Phase VI uses the open-source data accompanying Xiao et al. (2025), *Nature Sustainability*, DOI `10.1038/s41893-025-01681-y`, from `PEESEgroup/US-AI-Server-Analysis` under Apache-2.0.

The analysis is pinned to upstream commit:

`7f47a7c5bac252a88c81a1dbd9b874246714b1fc`

The exact upstream Git blob identities recorded in `data/external/source_manifest.json` are used to define the intended source version.

## SCT question

The goal is not to re-estimate the paper's energy, water or carbon footprint. The test is narrower: **is a restricted observation interface sufficient to identify location-conditioned environmental intensities?**

The upstream data contain state-dependent PUE/WUE values and a catalogue of AI data-centre construction records. We deliberately preserve the upstream `Size` field only as an observed field and do not infer an undocumented physical unit from it.

## Externally grounded witness

A manual audit of the pinned source identified six construction records in six states with exactly the same source-reported `Size = 291747` while the matched state-level PUE/WUE values differ.

For that equal-size witness:

- PUE ranges from `1.1205` to `1.1466` (range `0.0261`).
- WUE ranges from `1.5265` to `1.6170` (range `0.0905`).

Therefore a `Size-only` observation interface does not identify the corresponding location-conditioned PUE/WUE state. This is an externally grounded witness of the SCT observation-sufficiency claim; it is **not** a claim that project size alone should normally be used for environmental assessment.

## Reproducible adapter

`scripts/run_phase6_external.py` accepts the two original upstream CSV files as inputs, joins construction state to PUE/WUE, and searches the entire dataset for exact same-size groups spanning multiple states. It exports:

- `phase6_joined_projects.csv`
- `phase6_equal_size_groups.csv`
- `phase6_summary.json`

Example:

```bash
python scripts/run_phase6_external.py \
  --puewue Data/Baseline_PUEWUE.csv \
  --constructions "Data/AI data center constructions.csv"
```

## Scope restriction

This phase establishes a real-data **information-sufficiency witness** only. It does not yet establish a full energy-water-carbon trajectory closure, a causal rebound effect, or an empirical sustainability reversal. Those require a richer external trace and form the next validation gate.
