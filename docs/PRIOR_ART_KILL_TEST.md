# Phase III — Prior-Art Kill Test and Novelty Boundary

This note records the literature-side falsification test for **Sustainability Closure Theory (SCT)**. Its purpose is to prevent overclaiming and to identify what, if anything, remains genuinely distinctive after comparison with rebound theory, consequential LCA, dynamic LCA, Green AI, carbon-aware scheduling, and environmental lock-in research.

## What is already known and must NOT be claimed as new

1. **Efficiency does not imply lower total environmental impact.** Rebound/Jevons effects are long established, and recent AI work reports cases where AI adoption reduces emissions intensity while increasing total emissions.
2. **Consequential LCA already models behavioral and market consequences of technology changes.** Reference flows may be adjusted for price, time, productivity, induced demand, and rebound effects.
3. **Dynamic LCA already introduces explicit time dependence.** Time-varying emissions, resource use, technologies, and decision-support scenarios are established concepts.
4. **Indirect and system-wide AI effects are already recognized.** Existing AI-sustainability work distinguishes direct lifecycle effects, indirect beneficial effects, and higher-order rebound/system effects.
5. **Multi-resource trade-offs are already known.** Carbon reduction can conflict with water use, embodied emissions, hardware turnover, and other burdens.
6. **Environmental/socio-technical lock-in is already an established idea.** Path dependence and self-reinforcing trajectories are widely discussed in sustainability transitions and climate adaptation.
7. **Carbon-aware and spatio-temporal scheduling are mature active areas.** They optimize workload timing/location against grid carbon, renewable availability, cost, and QoS.

## Therefore the original broad SCT wording is too wide

The following statements are **not sufficient novelty claims**:

- “Efficiency can increase total consumption.”
- “Sustainability is dynamic.”
- “We should include indirect effects.”
- “Carbon is not the only environmental burden.”
- “Delayed action can cause lock-in.”
- “A lifecycle perspective is needed.”

All of those have clear prior art.

## Stronger novelty boundary that survives this search

The potentially distinctive SCT contribution is narrowed to a **formal distinguishability / incompleteness problem**:

> Given a specified observable metric family M, can two systems be identical under every metric in M at deployment (or along a restricted observation interface) yet have different induced consequence closures over a future horizon?

The software already contains a constructive family in which deployment-time energy/service, carbon/service, and water/service are identical while future closure burdens differ because the systems have different endogenous demand-response laws.

This should be framed as a theorem about **insufficiency of a declared observation class**, not as a theorem that “all sustainability metrics are incomplete.”

## Candidate theorem family

### T1. Restricted-Metric Non-Identifiability

Let `M` be a finite family of metrics depending only on the present operating state and fixed intensities. Under a model class allowing endogenous post-adoption response, there exist systems `A` and `B` such that

`M(A) = M(B)`

but

`C_T(A) != C_T(B)`

for some finite horizon `T`.

This is a constructive non-identifiability result. Its novelty depends on the exact definition of `M`, `C_T`, and the allowed dynamics.

### T2. Reversal Boundary

For the simplified demand law

`q_(t+1) = q_t [1 + e(1-g)]`

with energy-per-service multiplier `0 < g < 1` and response coefficient `e >= 0`, instantaneous energy exceeds the baseline once

`g [1 + e(1-g)]^(t+1) >= 1`.

Hence the first instantaneous reversal index is

`t_R = ceil( ln(1/g) / ln(1 + e(1-g)) ) - 1`,

when `e > 0`; otherwise no reversal occurs in the simplified model.

The repository numerically verifies this construction.

### T3. Observation-Class Dependence

SCT should explicitly state that incompleteness is relative to an observation class. A richer metric containing the true response law could, by construction, distinguish the systems. Therefore the defensible claim is:

> **No metric family restricted to current operational intensities can generally identify future sustainability closure over a model class with hidden endogenous response dynamics.**

This is stronger and safer than saying “no finite set of sustainability metrics can determine sustainability.”

## What still needs to be proved before manuscript claims are frozen

1. Generalize T1 beyond the present simulator to an abstract state-transition model.
2. State assumptions under which closure is well-defined for a finite horizon and, if used, for an infinite horizon.
3. Prove sufficient/necessary conditions for finite reversal time in more than the scalar energy model.
4. Separate **rebound-aware cumulative energy** from SCT's claimed additional information. If a rebound-aware comparator has the same demand law, SCT must win only through additional state dimensions, latent infrastructure response, or intervention/recoverability structure.
5. Test whether a strong consequential-LCA-style comparator can recover the same ordering. If yes, SCT must be presented as a formal computational specialization or diagnostic layer rather than a replacement.
6. Validate at least one part of the theory on externally grounded data or traces.

## Kill-test verdict

### Survived
- Restricted-observation non-identifiability construction.
- Closed-form reversal boundary for the simplified endogenous-demand model.
- Horizon-dependent false-green phenomenon in the current computational model.
- Multi-dimensional closure as a useful software abstraction when the observation interface is explicitly defined.

### Weakened / renamed
- “Green Metric Incompleteness Theorem” -> **Restricted-Metric Non-Identifiability Theorem**.
- “Sustainability is trajectory-dependent” -> useful framing, but not novel by itself.
- “Sustainability lock-in” -> application of established lock-in ideas unless a new theorem is proved.
- “Green Horizon” -> retain only as an SCT-defined diagnostic, not as a claim that horizon-based environmental reasoning is unprecedented.

### Killed as novelty claims
- Rebound/Jevons effect itself.
- Time-dependent environmental assessment itself.
- Lifecycle accounting itself.
- Carbon/water trade-off itself.
- Carbon-aware scheduling itself.
- Generic environmental lock-in itself.

## Paper-readiness gate after Phase III

Do **not** yet write the final Results/Abstract/Conclusion. Begin the full paper only after:

- abstract theorem proof is complete;
- strongest rebound-aware and consequential-LCA-inspired baselines are implemented;
- at least one external dataset/trace is integrated;
- all claimed distinctions survive those tests.

At that point the paper can credibly center on **formal non-identifiability of sustainability under restricted observation plus consequence-closure diagnostics**, rather than on an already-known rebound narrative.
