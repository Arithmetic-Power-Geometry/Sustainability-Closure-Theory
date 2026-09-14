# SCT Claim-Freeze Audit

This document freezes the defensible scientific claims for the first Sustainability Closure Theory (SCT) paper. It separates formal theorems, synthetic computational evidence, externally grounded evidence, and claims that must not be made.

## A. Core contribution to claim

### A1. Sustainability assessment under a restricted observation interface can be non-identifying

**Claim class:** formal/theoretical.

If an assessor observes only a declared interface \(\phi(x)\), and two admissible systems have the same observed representation but different future sustainability closures, then no estimator that depends only on \(\phi(x)\) can identify the correct closure for every system in the class.

**Allowed wording:** “SCT formalizes observation sufficiency for sustainability assessment and gives constructive conditions under which a restricted metric interface is non-identifying.”

**Do not strengthen to:** “No finite sustainability metric can ever determine sustainability.” The theorem is conditional on the declared observation class and admissible response dynamics.

### A2. Endogenous response can produce environmental reversal despite an initially favorable efficiency metric

**Claim class:** analytical + synthetic computational witness.

The model derives an explicit reversal boundary for a simplified endogenous-demand process and verifies it numerically.

**Allowed wording:** “Within the stated model class, an initially favorable efficiency ratio can cross an analytically derived reversal boundary under endogenous demand growth.”

**Do not strengthen to:** “All efficiency improvements eventually become environmentally harmful.”

### A3. Observation refinement can restore identifiability in the tested construction

**Claim class:** formal/computational.

When the response variable omitted by the restricted interface is added back, the refined comparator reproduces the full consequence assessment in the controlled construction.

**Allowed wording:** “The tested constructions show that exposing previously hidden response variables can remove the ambiguity created by a restricted observation interface.”

### A4. Full-information SCT is not claimed to dominate consequential or dynamic LCA

**Claim class:** negative/novelty-boundary result.

If a fully informed consequential/dynamic model observes the same complete future consequence trajectory and applies the same aggregation rule, it is equivalent to the SCT burden calculation by construction.

**Required paper wording:** “SCT is not proposed as a universal replacement for consequential or dynamic LCA. Its distinct contribution is the explicit analysis of observation sufficiency, closure completeness, and non-identifiability under restricted assessment interfaces.”

## B. Synthetic computational evidence that may be reported

### B1. Parameter sweep

The controlled parameter sweep contains 676 cases across efficiency, elasticity, and time horizons. In the synthetic model, disagreement between pointwise-efficiency classification and full closure increases with horizon.

**Allowed wording:** “In the controlled sweep…” or “In the synthetic model…”

**Forbidden wording:** “82% of real technologies are false green” or any population-level interpretation of the sweep frequency.

### B2. Constructive metric-incompleteness family

A 25-system synthetic family preserves deployment-time pointwise metrics while allowing large divergence in future closure burden through different response laws.

**Allowed wording:** “The constructive family demonstrates existence.”

**Forbidden wording:** treating the numerical closure range as an empirical estimate.

### B3. Stronger dynamic-baseline separation

A rebound-aware energy comparator can remain favorable while full closure reverses after non-energy future-state burdens are included. A dynamic carbon-only comparator can likewise disagree when burden migrates into water or other dimensions.

**Allowed wording:** “A single-resource dynamic comparator is not sufficient for the tested multi-resource closure model.”

**Forbidden wording:** “All rebound-aware or carbon-aware methods fail.”

### B4. Consequential-LCA kill test

Under matched full information and matched aggregation, consequential assessment and SCT coincide. Under information ablation, the restricted causal model can disagree with the fully informed assessment.

**Allowed wording:** “The distinction is informational, not a claim that causal propagation itself is novel.”

## C. Externally grounded evidence that may be reported

The external validation uses the open U.S. AI-server/data-centre dataset associated with Xiao et al., Nature Sustainability (2025), pinned to a fixed upstream commit.

### C1. Equal-observation witness

Six construction records in six U.S. states share the same upstream-reported `Size = 291747` but have different state-conditioned PUE and WUE values.

Observed ranges in the bundled witness:

- PUE: 1.1205 to 1.1466; range 0.0261.
- WUE: 1.5265 to 1.6170; range 0.0905.

**Allowed wording:** “The size-only observation interface is insufficient to identify state-conditioned PUE/WUE in this witness.”

**Critical restriction:** do not assign a physical unit or interpretation to the upstream `Size` field unless the source explicitly establishes one.

### C2. Cross-resource ordering conflict

Within the six-record witness, four pairwise PUE/WUE ordering reversals occur: a location preferred on one resource can be disfavored on the other.

The baseline two-objective Pareto front contains Iowa and Illinois.

**Allowed wording:** “The externally grounded witness contains cross-resource ordering conflicts.”

**Forbidden wording:** “Iowa and Illinois are universally the most sustainable AI-data-centre locations.” The result is conditional on these records, these variables, and this observation set.

### C3. Robustness stress test

PUE/WUE are perturbed multiplicatively at 0%, 0.5%, 1%, 2%, and 5%, with 5,000 deterministic-seed trials per level. These perturbations are sensitivity stresses, not empirical error bars.

Probability of at least one pairwise ordering reversal remains approximately 0.997–0.998 over the nonzero perturbation levels tested.

The exact original Pareto front becomes less stable as perturbation increases, while the structural existence of cross-resource conflict remains highly persistent.

**Allowed wording:** “The structural ordering conflict is robust to the tested sensitivity perturbations even though exact winners and the exact Pareto front are not.”

**Forbidden wording:** interpreting the perturbation percentages as measured uncertainty of the source data.

## D. Claims explicitly rejected for this paper

The manuscript must not claim any of the following:

1. Rebound/Jevons effects are newly discovered by SCT.
2. Time-dependent environmental accounting is new.
3. Consequential LCA cannot model future decision-induced consequences.
4. SCT universally outperforms consequential LCA or dynamic LCA.
5. Carbon-water trade-offs are newly discovered.
6. Efficiency is always environmentally harmful.
7. The synthetic false-green fractions are empirical real-world frequencies.
8. The external `Size` field has an undocumented physical unit.
9. The six external records establish a universal ranking of U.S. states.
10. The present external validation proves a real-world longitudinal sustainability reversal.

## E. Frozen novelty statement

The safest central novelty statement for the first paper is:

> Sustainability Closure Theory treats sustainability assessment as an information-sufficiency problem. It formalizes when a declared observation interface cannot identify future environmental consequence closure, provides constructive and analytical witnesses of that non-identifiability, and shows—using externally grounded AI-infrastructure data—that cross-resource sustainability ordering can remain unresolved or reverse when relevant context is omitted.

A shorter version for the abstract is:

> We formulate sustainability assessment as an observation-sufficiency problem and derive conditions under which restricted green metrics cannot identify future consequence closure.

## F. Evidence hierarchy for manuscript structure

Use this order in the paper:

1. Definitions: observation interface, reachable consequence set, sustainability closure, closure ordering.
2. Restricted-observation non-identifiability theorem.
3. Constructive endogenous-demand witness and analytical reversal boundary.
4. Synthetic parameter sweep and metric-incompleteness family.
5. Strong dynamic baselines and consequential-LCA kill test.
6. Externally grounded equal-observation witness.
7. Cross-resource ordering/Pareto analysis.
8. Robustness and sensitivity attack.
9. Limitations and non-claims.

## G. Paper-writing gate

The evidence package is now sufficient to begin the manuscript, provided the current GitHub Actions run passes on the supported Python matrix and the manuscript preserves the claim boundaries above.

Do not delay writing for additional synthetic experiments unless a new reviewer-relevant weakness is identified. The remaining work should shift from discovery to manuscript construction, reference verification, figure consolidation, and reproducibility freezing.
