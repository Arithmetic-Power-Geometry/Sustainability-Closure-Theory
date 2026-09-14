# Phase VI-B/C — External Observation Ablation

This phase extends the externally grounded SCT validation using the same pinned public AI data-centre source already used in Phase VI-A.

## Questions tested

1. Do state-level PUE and WUE induce pairwise ordering reversals, so that a PUE-only ranking and a WUE-only ranking can prefer different locations?
2. Does adding environmental context to a restricted observation interface change project rankings?
3. Does the externally observed construction record form a non-trivial multi-year trajectory that can be analysed without assigning undocumented physical units to the upstream `Size` field?

## Method

The full CI analysis downloads two pinned upstream files from `PEESEgroup/US-AI-Server-Analysis` at commit `7f47a7c5bac252a88c81a1dbd9b874246714b1fc` and verifies their Git blob SHA-1 values before use.

The analysis then:

- joins construction records to state-level PUE/WUE;
- enumerates pairwise PUE/WUE ordering reversals;
- computes a PUE-WUE Pareto set;
- performs a declared observation ablation from `Size` only, to `Size + PUE`, to `Size + PUE + WUE` using normalized rank scores;
- exports a yearly trajectory of project counts, states, the sum of the source `Size` field, and size-weighted PUE/WUE proxies.

## Scope restriction

The upstream `Size` field is not assigned a physical unit by SCT. Therefore the weighted quantities are explicitly labelled **proxies**, not energy, carbon, or water footprints.

This phase tests the information-sufficiency and ranking-stability claims of SCT. It does not claim that these rank scores are a replacement for consequential LCA or a physical environmental impact model.
