# ANIMO-GHG02 — TCD-033 CH4 production-component partition qualification

Status: `CANDIDATE_SCIENTIFIC_POLICY_PENDING_EXACT_HEAD_REVIEW`

This workunit qualifies only the bounded scientific identity for canonical `TCD-033`: the CH4 production-component rates must be a partition of the already calculated total CH4 production rate while preserving the source routine's explicit proportional source-pool weighting. It does not modify production source, admit TCD-032 or TCD-034, reconstruct historical executable behaviour, or authorize B4/production.

## Authorities and frozen source

- current aggregate: `ANIMO-RG05N@8758bd30e302b75dd7854ac00fd2e29473669a13`;
- current negative B3 closure authority: `ANIMO-B3Q05@997d867a2b107ec8e28efce530c82a204719de46`;
- canonical allocation: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`;
- source/theory reconstruction: `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`;
- frozen revision-53 archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- `ANIMO_4.1.5.53/ghg_ch4.for` SHA-256: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`.

B3I01 defines TCD-033 as `CH4 production component partition does not close to total under partial anaerobiosis`, Class B, with GHG02 as proposed qualification owner. GHG01 independently reconstructed the relevant revision-53 algebra and explicitly separated this phenomenon from TCD-032's incomplete source-pool transfer path and TCD-034's plant-growth temperature-index problem.

## Revision-53 source semantics

For one soil layer let the pre-aeration methanogenic source-pool contributions be

`S_i >= 0`, with `S = sum_i S_i`,

and let

`A = 1 - Rdfaox`

be the anaerobic fraction. The source forms total methanogenic substrate as `A*S` and calculates

`Q = E*A*S`,

where `E` contains the pH, temperature and potential-production factors. The source comment then identifies `QPrCH4Do`, `QPrCH4Ex`, `QPrCH4Hu` and `QPrCH4Os` as the *contribution of OM pools to CH4 production rate*, all in the same units as `QPrCH4`: `kg C m-2 d-1`.

Revision 53 currently evaluates each component as

`Q_i,legacy = Q * S_i / (A*S)`.

For `0 < A < 1` and `S > 0`, substitution gives

`Q_i,legacy = E*S_i`

and therefore

`sum_i Q_i,legacy = E*S = Q/A`.

Thus the component family is not a partition of the total except when `A=1`. The discrepancy is source-internal and does not depend on a historical executable reference.

## Qualified bounded identity

GHG02 qualifies the following identity as the scientific TCD-033 policy:

- if the existing source anaerobic early-return applies (`A < 1.0e-8`), total and all components are zero;
- otherwise, if `S = 0`, total and all component rates are zero, avoiding the legacy `0/0` component domain;
- otherwise calculate total production according to the separately governed total-production formulation and partition it as

`Q_i = Q * S_i / S`.

Because `Q = E*A*S`, this is equivalently

`Q_i = E*A*S_i`.

The identity has four deliberately narrow properties:

1. **parent/daughter closure:** `sum_i Q_i = Q` in exact arithmetic;
2. **source-share preservation:** `Q_i/Q_j = S_i/S_j` wherever the denominator is defined, retaining the source routine's explicit proportional weighting;
3. **full-anaerobiosis compatibility:** for `A=1`, the qualified expression is algebraically identical to revision 53;
4. **zero-domain definition:** `S=0` maps to zero total and zero components rather than an undefined component division.

Within the model semantics already present in `CH4produc`, proportional source weights plus the requirement that the quantities are contributions to the one total rate uniquely determine this normalization by `S`. GHG02 does **not** claim that this was the historical intended implementation. It is a bounded scientific model-evolution identity qualified under historical uncertainty.

## Evidence and controls

The reusable oracle enumerates source vectors, anaerobic fractions and environmental multipliers, including exact-zero source, single-source, mixed-source, full-anaerobic, partial-anaerobic and the existing `1.0e-8` anaerobic cutoff boundary. It checks the qualified parent/daughter identity against high-precision Decimal arithmetic and carries the legacy formula only as a negative control.

Expected negative control under partial anaerobiosis: for `A=0.4`, `S>0`, the legacy component sum is `2.5*Q`, while the qualified component sum is `Q` apart from ordinary binary64 summation rounding.

The oracle bound is an equation-verification bound only. It is not a model tolerance, solver tolerance or conservation acceptance threshold.

## Explicit nonclaims

GHG02 does not:

- qualify or activate the missing source-pool depletion transfers of TCD-032;
- choose or repair the TCD-034 plant-growth temperature state;
- change the total CH4 production response functions, pH law, Q10, `Rdfaox`, oxygen-demand logic or transport;
- prove historical revision-53 numerical behaviour;
- use a whole-model mass residual as the equation oracle;
- create B2 evidence;
- patch production source;
- perform TCD-033 B3 admission;
- open TB7, B4 or production.

A separate GOV05 Tier-C B3 admission decision is required after this qualification is exact-final green.
