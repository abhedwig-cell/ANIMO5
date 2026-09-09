# ANIMO-NQ02 — TCD-019 and TCD-024 interaction

Status: `INTERACTION_DESIGN_PERSISTED_NO_COMPOSITION_ADMISSION`.

## Separation rule

TCD-019 and TCD-024 are different defect classes and must remain atomized.

- TCD-019: Class E numerical-policy defect in nonlinear P sorption/conservation.
- TCD-024: Class B wrong-index defect in slow-Langmuir sorption-site handling.

No result in this document admits a combined correction.

## Source interaction

The known TCD-024 source defect is in a slow-Langmuir path where an outer/trial index is used in a site-parameter reference instead of the sorption-site index. This can change slow-sorption kinetics/state when `Optcxsl = 2` and multiple or unequal site parameters make the index difference observable.

TCD-019 primarily concerns:

- the fast-sorption nonlinear storage representation in `Sorpfast`;
- the `C_unl` nonlinear stopping and fallback policy;
- resulting exact P storage/transport conservation.

Both meet inside the same coupled phosphate solver, so composition can alter the nonlinear residual surface and iteration path even though the defects are conceptually separate.

## Natural-case boundary

The historical LWKM case used for the known TCD-019 signal has:

- `Optcxfa = 2` fast Langmuir;
- `Optcxsl = 3` slow Freundlich.

Therefore TCD-024 is not naturally active in that case. LWKM is suitable for a TCD-019-only convergence study without first correcting TCD-024.

## Required four-way interaction matrix

A dedicated activated slow-Langmuir diagnostic case must eventually run four variants from the same frozen B0 basis:

1. `LEGACY_BOTH`:
   unchanged TCD-019 numerical policy and unchanged TCD-024 index behaviour;
2. `TCD024_ONLY`:
   only the wrong-index expression corrected in an exact hashed B1 descendant;
3. `TCD019_ONLY`:
   only the selected TCD-019 numerical-policy diagnostic applied;
4. `COMBINED_DIAGNOSTIC`:
   both diagnostic changes applied.

The matrix must compare:

- slow-site states individually, not only their sum;
- fast-sorption state;
- aqueous PO4;
- nonlinear equation residuals;
- exact conservation residuals;
- iteration/fallback path;
- external and cumulative P transfers;
- downstream coupled quantities where differences propagate.

## Interpretation

The interaction is approximately additive only if:

```text
(combined - legacy) ≈ (TCD024-only - legacy) + (TCD019-only - legacy)
```

for the named scientific quantities under a qualified comparison metric. This equality is not assumed and no numerical tolerance is defined here.

A non-additive interaction does not merge the two defects. It means the later B3 composition review must qualify the joint solver behaviour explicitly.

## Evidence restrictions

Synthetic unequal-site cases are valid for TCD-024 activation, causal proof and composition stress testing, but remain B1. They do not establish historical prevalence or B2 behaviour.

The four-way matrix must not be used to admit either correction without its own class-specific gate.

Current state:

- TCD-019 B3 admitted: `false`;
- TCD-024 B3 admitted: `false`;
- combined composition admitted: `false`;
- production migration admitted: `false`.
