# Sustainability Closure Theory (SCT)

A reproducible research software package for testing **Sustainability Closure**, **Green Metric Incompleteness**, **environmental reversal**, **burden migration**, **Sustainability Debt**, and **intervention lock-in** in intelligent computing systems.

## Core question

Can a technology appear efficient or green at deployment while generating a worse environmental future once induced demand, infrastructure response, lifecycle burden, and delayed intervention are included?

## Implemented components

- Multi-dimensional environmental trajectory simulation.
- Finite-horizon Sustainability Closure approximation.
- Same-metric / different-future kill test.
- Green Horizon and Reversal Time estimation.
- Burden-migration test across carbon and water.
- Sustainability Debt above a boundary vector.
- Recoverability curves and latest effective intervention time `t*`.
- Automated tests and GitHub Actions CI for Python 3.10–3.12.
- Reproducible CSV tables and PNG figures exported as workflow artifacts.

## Phase II: analytical and family-level stress tests

Phase II moves beyond one constructed example. It adds:

- a closed-form instantaneous reversal boundary for the simplified induced-demand model;
- numerical verification of that boundary;
- a 676-case sweep over efficiency, elasticity, and four time horizons;
- a 25-member family with identical deployment-time energy/carbon/water intensities but different future demand-response laws;
- metric-disagreement statistics quantifying when pointwise green judgments disagree with finite-horizon closure ordering;
- publication-oriented heatmaps and CSV tables produced directly by the workflow.

Run Phase II with:

```bash
python scripts/run_phase2.py
```

The current local validation passes **7 automated tests**. In the 676-case synthetic sweep, the fraction of cases that remain green under pointwise efficiency but become non-green under finite-horizon closure increases with horizon: 0.000 at 12 steps, 0.225 at 24, 0.669 at 60, and 0.822 at 120. These are controlled model diagnostics, not real-world prevalence estimates.

## Quick start

```bash
python -m pip install -e .[dev]
pytest
python scripts/run_all.py
python scripts/run_phase2.py
```

Outputs are written to `results/`.

## Scientific boundary

This repository does not claim that rebound effects, lifecycle assessment, carbon-aware computing, or multi-resource accounting are new. It tests the stronger SCT proposition that **instantaneous efficiency/environmental metrics may be insufficient to determine sustainability ordering when adoption changes future demand, infrastructure, or replacement dynamics**.

The analytical reversal result is proved only for the explicitly stated simplified model. The family-level incompleteness experiment is a constructive witness inside the implemented model class; it is not yet a universal impossibility theorem over every conceivable sustainability metric.

## When to write the paper

Do **not** freeze the manuscript from the current synthetic model alone. The paper becomes worth drafting once three gates are passed:

1. **Theory gate:** analytical reversal boundary and constructive metric-incompleteness result remain valid under formal review and broader parameterization.
2. **Prior-art gate:** a focused literature search confirms that the exact closure formulation and claimed theorem scope are not already established under another name.
3. **Evidence gate:** at least one externally grounded dataset or realistic trace reproduces the central distinction between pointwise efficiency and trajectory-level closure.

A manuscript skeleton can be started earlier, but headline claims and final Results should wait until those gates pass.

## License

Apache License 2.0

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
