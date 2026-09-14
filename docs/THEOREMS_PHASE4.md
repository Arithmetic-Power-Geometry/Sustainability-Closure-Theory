# Phase IV — Formal theorem layer

This document states the narrow theorem family that remains defensible after the prior-art kill test.

## Definition 1 — Restricted observation interface

Let a system be indexed by hidden response parameter `theta` and evolve as

`x_(t+1) = F(x_t, theta)`.

Let `pi(x_0, theta)` be the deployment-time observation available to an evaluator. A restricted metric family is any function of `pi` only. Let the finite-horizon consequence functional be

`C_T(theta) = Sum_{t=0}^{T-1} b(x_t(theta))`,

where `b` may be scalar or vector-valued.

## Theorem 1 — Restricted-Observation Non-Identifiability

Assume there exist `theta_A != theta_B` such that

`pi(x_0, theta_A) = pi(x_0, theta_B)`

but

`C_T(theta_A) != C_T(theta_B)`

for some finite horizon `T`.

Then no estimator `Phi` that depends only on the restricted observation `pi` can recover the true consequence functional `C_T` for every system in the model class.

### Proof

Suppose such a `Phi` existed. Since the observations are identical,

`Phi(pi(x_0, theta_A)) = Phi(pi(x_0, theta_B))`.

Correctness would require the left side to equal `C_T(theta_A)` and the right side to equal `C_T(theta_B)`. This contradicts `C_T(theta_A) != C_T(theta_B)`. Therefore no observation-only estimator can be universally correct on this model class. QED.

### Interpretation

The theorem is deliberately conditional. It does **not** say every sustainability metric is incomplete. It says a metric family cannot identify future consequence closure if the allowed model class contains hidden response laws that are observationally indistinguishable at deployment but generate different futures.

## Corollary 1 — Endogenous-demand witness family

Let baseline demand be `q_0 > 0`, energy-per-service multiplier `0 < g < 1`, and hidden response coefficient `e >= 0`. Define

`q_(t+1) = q_t [1 + e(1-g)]`.

Let deployment metrics be

`pi = (g, g*c, g*w)`,

where `c` and `w` are fixed carbon and water intensities. These metrics do not contain `e`.

For two systems with `e_A != e_B`, deployment metrics are identical, but for any horizon `T >= 2` their cumulative energy consequences differ:

`E_T(e) = g*q_0 * Sum_{k=1}^{T} [1 + e(1-g)]^k`.

Hence the restricted deployment metrics cannot identify cumulative consequence over this model class.

## Theorem 2 — Instantaneous Reversal Boundary

For the same demand law, candidate instantaneous energy at index `t` is

`E_t = g*q_0*[1 + e(1-g)]^(t+1)`.

The baseline is `q_0`. For `e > 0`, reversal occurs when

`g*[1 + e(1-g)]^(t+1) >= 1`.

Thus the first reversal index is

`t_R = ceil( ln(1/g) / ln(1 + e(1-g)) ) - 1`.

If `e = 0`, no reversal occurs for `0 < g < 1`.

The repository numerically validates this closed form against simulation.

## Proposition 3 — Observation-class monotonicity

If observation interface `pi_2` strictly contains all information in `pi_1`, then non-identifiability under `pi_2` is at least as hard to establish as under `pi_1`. In particular, adding the true hidden response law to the observation interface can remove the witness used in Corollary 1.

This proposition is important for claim discipline: SCT must always name the observation class with respect to which a non-identifiability claim is made.

## Next proof targets

1. Cumulative-reversal boundary for finite horizon.
2. Vector consequence ordering without arbitrary scalar weights, using Pareto dominance where possible.
3. Conditions for finite Green Horizon.
4. Recoverability monotonicity and existence of a latest effective intervention time under explicit assumptions.
5. A theorem separating rebound-aware energy accounting from full multi-resource closure when hidden replacement/infrastructure dynamics are present.

## Manuscript gate

The formal core is now sufficient to draft the **Definitions/Theory** section, but the paper's abstract, Results, and final novelty claim should remain unfrozen until the strongest consequential-LCA-inspired comparator and external-data experiment are complete.
