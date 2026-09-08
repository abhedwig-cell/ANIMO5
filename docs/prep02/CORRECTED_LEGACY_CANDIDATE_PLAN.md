# ANIMO-PREP02 corrected-legacy candidate plan

Status: `PLANNED_SEPARATE_ADMISSION_BY_SEMANTIC_CLASS`.

## Purpose

PREP01 has shown that the dominant deterministic legacy mass-balance residuals do not belong to one numerical-tolerance envelope. They have different causes and therefore require different correction and qualification routes.

This plan prevents a broad legacy cleanup patch from mixing accounting-only changes with changes to transport algebra, state representation or initialization semantics.

The frozen source remains the behavioural baseline candidate. A corrected-legacy lineage is separate and may begin only after the affected frozen behaviour has been qualified against a historical or independently admitted reference contract.

## Correction classes

### Class A: ledger and reporting corrections

These corrections change diagnostic balance accounting but are not expected to change model state trajectories or physical process rates.

#### TCD-017, organic-P ploughing redistribution

Source finding:

- `Addit.for` performs the top-reservoir-to-soil redistribution and records the top-reservoir dissolved-organic-P loss in `Addiorpotoppl`;
- it separately records stable dissolved-organic-P redistribution in `AdStdiorpopl`;
- it separately records P associated with redistributed exudate-derived humus in `Adhuexpopl`;
- `Outbal_calc.for` omits `Addiorpotoppl`, omits `AdStdiorpopl`, and reconstructs the exudate-humus term as `Adhuexpl * Pofrhu` instead of consuming the explicit P-valued `Adhuexpopl` ledger quantity.

The original minimal measured-case correction was:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

inside the same top-reservoir balance scope used by the analogous N and inorganic-P terms.

The subsequent PREP02 P-array audit expands the Class-A candidate family, but not its reference admission. Two controlled activation probes show that the dormant P-specific arrays are also required when their states are active:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) +
     (Addiorpopl(I,Ln) + AdStdiorpopl(I,Ln))*Z
```

and, for the exudate-humus P redistribution term:

```fortran
Dum = Adhuexpopl(I,Ln) * Z
```

instead of reconstructing that term from `Adhuexpl * Pofrhu`.

Diagnostic evidence:

- supplied phosphorus/ploughing cases naturally leave `AdStdiorpopl` and `Adhuexpopl` at zero, so natural testbank parity alone cannot qualify them;
- a stable-DOP activation probe reduced the partial-profile RP maximum absolute period residual from `1.43e-4` to `2.34e-10 kg/ha P` when `AdStdiorpopl` was admitted to the diagnostic ledger;
- an exudate-humus activation probe reduced the corresponding RP residual from `45.2` to `2.34e-10 kg/ha P` when `Adhuexpopl` replaced the legacy reconstruction;
- ordinary non-balance outputs were unchanged after normalization of only the PREP01 volatile fields in both probes;
- detailed evidence is in `docs/prep02/ORGANIC_P_PLOUGHING_ARRAY_AUDIT.md` and `integration/animo-prep/PREP02_ORGANIC_P_PLOUGHING_ARRAY_AUDIT.json`.

Admission requirements:

1. frozen reference reproduces the original naturally active ploughing residuals;
2. each ledger subterm remains independently reversible and attributable;
3. corrected cases remove only the bookkeeping defects;
4. all process-state and ordinary non-balance outputs are unchanged at the admitted comparison precision;
5. period and cumulative organic-P ledgers close after the correction;
6. reference qualification includes at least one admitted activation of stable DOP and exudate-humus P, because the supplied natural testbank leaves those terms dormant;
7. partial balance profiles that intersect the ploughing zone are included, not only whole-plough-zone profiles;
8. any GNU execution-copy compatibility adaptation is recorded separately and is not treated as reference evidence.

#### TCD-018, interception water storage

Source finding:

- `Hydro_detailed` includes `Sic/Sict` storage change in its internal water balance;
- `Outbal_calc` does not receive that state and cannot represent the complete detailed-hydrology control volume.

Minimal corrected-legacy candidate should expose interception-storage change to the water ledger and preserve the existing balance-period reset semantics.

Admission requirements:

1. frozen reference reproduces the characteristic `~0.06 mm` residual pattern;
2. corrected ledger matches the accumulated `Hydro_detailed` whole-profile `Badev` envelope;
3. hydrologic state and flux trajectories are unchanged;
4. all balance profiles and reset periods are tested, not only TP;
5. legacy formatted-output changes are documented as intentional correction evidence.

Class A corrections may be implemented in one corrected-legacy branch only after each has an independent local admission test. They must still remain individually reversible and attributable.

### Class B: local algebraic conservation correction

#### TCD-015, NO3 negative-concentration `Reko` reconstruction

Source finding:

The clipping branch reconstructs `Reko` using full `Hv1`, even though `Hv1` contains the moisture-storage derivative `Hv` already represented by the complete storage-change term. This double-counts `Avc*Hv`.

Causal diagnostic candidate:

```text
use Avc*(Hv1-Hv) in the clipped-concentration reconstruction
```

The local TITO-2312 residual closes to floating-point noise and the 1997 LWKM NO3 residual falls from `+0.5760503022407` to about `+2.28e-7 kg/ha N`.

This is not Class A. The correction changes the zero-order transport term returned by `Transsub` and can alter later concentration trajectories.

Admission requirements:

1. native/frozen reference reproduces the original local mass warning and trajectory;
2. algebraic derivation is independently reviewed against the governing transport equation;
3. local mass closure is exact within explicit floating-point policy;
4. concentration remains nonnegative without introducing new discontinuities;
5. all substances and all `Iflsol` clipping branches using the same code path are tested;
6. full-case trajectory differences are explained and admitted, not hidden under a global tolerance.

### Class C: state-model correction

#### TCD-016, NH4 surface dry-down

Source finding:

The layer-0 wet-to-dry branch destroys remaining dissolved solute when the liquid compartment disappears and `Fu <= 1e-6`. The existing outflow formula can force conservation but creates a pathological concentration of about `3.37e4 kg/m3` for the observed event.

No minimal production correction is admitted yet.

The corrected design requires a theory-qualified conserved continuation state, for example a dry surface residue/solute store that can later redissolve, or another explicitly documented phase transfer.

Admission requirements before implementation:

1. obtain theory or authoritative modelling intent for solute fate during complete surface dry-down;
2. define ownership and units of the dry/residual state;
3. define wet-to-dry and dry-to-wet transfer equations;
4. prove conservation across both transitions;
5. prevent evaporation from exporting nonvolatile NH4;
6. prevent artificial extreme aqueous concentrations created solely for accounting closure;
7. add continuation/restart tests so the dry state survives transaction boundaries.

TCD-016 must not be bundled into a corrected-legacy patch using the diagnostic tiny-outflow workaround.

### Class D: initialization-contract correction

#### TCD-014, PO4 initial sorption consistency

Source finding:

The supplied `INPO=1` initial state can contain solution concentration and fast sorption values that are individually accepted by a per-layer tolerance but collectively differ from the model's own sorption relation enough to produce a large first-profile residual when the state is projected.

The temporary control that replaced the supplied fast sorption with values calculated from the model relation reduced the first residual by 99.9864 percent. That proves causality, but it does not establish the intended historical initialization policy.

Before correction, qualification must decide whether `INPO=1` means:

- supplied stores are authoritative and must be preserved exactly;
- concentrations are authoritative and sorption stores should be derived;
- both are authoritative and inconsistency should become an explicit initialization adjustment in the mass ledger;
- another documented contract.

No corrected initialization should be implemented until this policy is theory/reference qualified.

## Non-composition rule

The first corrected-legacy qualification must not apply TCD-014 through TCD-018 simultaneously.

Required sequence:

1. qualify frozen behaviour for the affected case;
2. admit one correction independently;
3. preserve a separate output/evidence delta for that correction;
4. only then compose already admitted corrections;
5. rerun the full qualification suite after composition to detect interactions.

This is especially important because TCD-015 can change later concentration trajectories, while TCD-017 and TCD-018 should not.

## Proposed corrected-legacy work units

### CL-01, reporting and ledger completeness

Scope:

- TCD-017 organic-P redistribution bookkeeping;
- TCD-018 interception-storage water ledger.

Expected property:

`state_trajectory_unchanged = true`

subject to reference verification.

### CL-02, transport clipping conservation

Scope:

- TCD-015 only.

Expected property:

`mass_conservation_restored = true`

but state/output trajectories may change after the corrected event.

### CL-03, conservative dry-solute continuation

Scope:

- TCD-016 only after theory/state contract is defined.

This is an architectural/scientific correction, not a cosmetic legacy patch.

### CL-04, initialization consistency contract

Scope:

- TCD-014 only after authoritative initialization semantics are resolved.

## Exit discipline

No Class A, B, C or D correction is production-admitted by this plan.

A corrected-legacy candidate may become qualification evidence only after:

- frozen reference qualification for its scope;
- local causal test;
- whole-case regression;
- explicit mass-ledger evidence;
- theory/code/evidence reconciliation;
- machine-readable admission status.

ANIMO5 production process migration remains `NOT_ADMITTED`.
