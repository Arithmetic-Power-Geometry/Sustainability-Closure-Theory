# SCT Manuscript Blueprint

## Recommended working title

**Beyond Green Efficiency: Sustainability Closure, Observation Sufficiency, and Environmental Ordering Under Incomplete Metrics**

Alternative:

**Sustainability Closure Theory: When Restricted Green Metrics Cannot Identify Future Environmental Consequences**

## Paper thesis

The paper should not argue that lifecycle dynamics, rebound, or carbon-water trade-offs are new. The thesis is that sustainability assessment can be treated as an observation-sufficiency problem: a restricted green-metric interface may be unable to identify the future environmental consequence closure even when its observed metrics are identical.

## Section order

### 1. Introduction

Motivate the gap between pointwise green metrics and consequence-complete assessment. State the central question: when are the variables available to an assessor sufficient to determine the future sustainability consequence set?

End the introduction with 4 contributions only:

1. Formalization of sustainability closure and a declared observation interface.
2. Restricted-observation non-identifiability theorem and constructive reversal analysis.
3. Strong-baseline/fully-informed consequential-assessment kill test that narrows the novelty claim.
4. Externally grounded AI-infrastructure witness plus robustness analysis showing persistent cross-resource ordering conflict.

### 2. Related Work and Novelty Boundary

Organize by: rebound/Jevons; Green AI and efficiency metrics; consequential and dynamic LCA; carbon-aware and water-aware computing; multi-objective sustainability; environmental lock-in/path dependence.

Close with a short novelty table distinguishing what SCT does and does not claim.

### 3. Sustainability Closure Framework

Define environmental state vector, reachable consequence set, sustainability closure, closure ordering, observation interface, sustainability debt, green horizon, reversal time, recoverable burden, and latest effective intervention time.

Avoid presenting every quantity as equally novel. Make the observation-interface/closure relationship the conceptual center.

### 4. Restricted-Observation Non-Identifiability

State assumptions carefully. Present theorem, proof, corollary for observation refinement, and constructive endogenous-demand witness.

### 5. Analytical Reversal Boundary

Derive the simplified endogenous-demand reversal boundary and explain model assumptions. Separate instantaneous reversal from cumulative reversal.

### 6. Controlled Computational Validation

Report the 676-case parameter sweep, metric-incompleteness family, burden migration, delayed intervention, and strong dynamic baseline comparisons.

Every synthetic numerical frequency must be labeled as model-level evidence rather than real-world prevalence.

### 7. Consequential-LCA Kill Test

Show that a fully informed consequential/dynamic comparator with the same complete trajectory and aggregation is equivalent to SCT by construction. Then show information-ablation mismatch when a relevant future-response mechanism is withheld.

Use this section to establish intellectual honesty and the precise novelty boundary.

### 8. Externally Grounded AI-Infrastructure Case

Describe the pinned Xiao et al. data source and provenance. Use the equal-`Size` witness without assigning an undocumented physical unit to `Size`.

Report PUE/WUE ranges, pairwise ordering conflicts, observation refinement, and the two-objective Pareto result only for the audited witness.

### 9. Robustness and Sensitivity

Report 5,000 trials at each perturbation level. Emphasize that exact winners/Pareto membership are less stable than the structural existence of cross-resource ordering conflict.

### 10. Discussion

Explain why SCT is best viewed as a diagnostic theory of assessment sufficiency and closure completeness, not a replacement score for LCA.

Discuss implications for Green AI, data-centre siting, reporting standards, and sustainability dashboards.

### 11. Limitations

Include at least: synthetic model simplification; external witness is not longitudinal proof of real-world reversal; source `Size` field is not physically reinterpreted; robustness perturbations are stress tests rather than measured uncertainty; weighting/scalarization remains normative; complete causal closure is practically difficult to observe.

### 12. Conclusion

Conclude with the narrow claim: sustainability cannot be inferred reliably from a restricted observation interface when admissible hidden response mechanisms can alter future consequence closure.

## Figures to freeze

1. SCT causal/closure schematic.
2. Analytical reversal boundary.
3. 676-case closure heatmap.
4. Metric-incompleteness family divergence.
5. Consequential-LCA information-ablation figure.
6. External PUE/WUE equal-observation witness.
7. Observation-refinement/ranking figure.
8. Robustness probability figure.

## Tables to freeze

1. Prior-art/novelty boundary table.
2. Definitions and symbols.
3. Formal theorem assumptions/conclusions.
4. Synthetic benchmark summary.
5. Strong-baseline comparison.
6. External witness records and cross-resource ordering result.
7. Robustness summary.
8. Claim/non-claim table.

## Writing gate

Begin manuscript writing immediately after the latest reproducibility workflow passes. Draft Introduction, Framework, Theorem, and Methods first. Freeze Abstract and Conclusion only after all final figures/tables are regenerated from the passing workflow artifact.
