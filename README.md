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

## Quick start

```bash
python -m pip install -e .[dev]
pytest
python scripts/run_all.py
```

Outputs are written to `results/`.

## Scientific boundary

This repository does not claim that rebound effects, lifecycle assessment, carbon-aware computing, or multi-resource accounting are new. It tests the stronger SCT proposition that **instantaneous efficiency/environmental metrics may be insufficient to determine sustainability ordering when adoption changes future demand, infrastructure, or replacement dynamics**.

## License

Apache License 2.0

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
