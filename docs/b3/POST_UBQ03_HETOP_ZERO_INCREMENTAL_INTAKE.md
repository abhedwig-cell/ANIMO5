# ANIMO-B3I06 - Post-UBQ03 incremental HETOP zero-domain intake

Status: `QUALIFIED_UBQ03_INCREMENTAL_INTAKE_RUNTIME_INPUT_DOMAIN_HAZARD_NO_NEW_TCD_NO_ADMISSION`

This work unit classifies only the new UBQ03 finding. It does not reopen earlier canonical decisions, change production source or admit a correction.

## Authoritative inputs

UBQ03 qualified the following narrow characterization:

`HETOP=0` is admitted by both the documented SOIL.INP range and the frozen revision-53 parser. The source simultaneously contains multiple reachable divisions by `HETOP` and no general zero-thickness guard or model semantics. UBQ03 deliberately did not claim that every zero-thickness run fails or that a particular historical exception outcome is known.

B3I05 remains authoritative for parent `TCD-042` and its existing children `TCD-042-B1` and `TCD-042-E1`. Those children are not top-level TCD rows and `TCD-043` was not reserved by that atomization.

## Relation to TCD-042

The HETOP endpoint matters to both TCD-042 children because their corrected positive-thickness formulations use `St/Hetop` or `P=St*Flux/Hetop`. It therefore prevents silently widening either child from `Hetop>0` to the complete parser-level input domain.

The UBQ03 phenomenon is nevertheless broader than TCD-042. Its direct division inventory includes `Addit`, crop-uptake routines and ordinary no-ponding positive-flow `UBoundconc`, not only the exact-zero or finite-positive subthreshold fallback. Treating the complete HETOP endpoint issue as another TCD-042 child would therefore conflate an input-domain/runtime contract problem with the already atomized fallback mechanisms.

B3I06 records the relation as:

`TCD-042-B1/E1 DOMAIN CONSTRAINT ONLY`

not as a new TCD-042 child.

## Why no new top-level TCD is reserved yet

The source discrepancy is real enough to keep fail closed, but the intended correction mechanism is not yet uniquely identified.

At least three materially different interpretations remain possible:

1. zero is outside intended model semantics despite the documented/parser range and should be rejected by the input contract;
2. zero is an intended zero-capacity virtual-reservoir option and requires explicitly defined bypass or limiting semantics across all owners;
3. zero is intended only for a narrower option combination, requiring a conditional admissibility contract rather than a global lower-bound change.

These possibilities imply different scientific and compatibility consequences. Reserving a new canonical TCD as though one atomic correction were already known would exceed the evidence. B3I06 therefore does not reserve `TCD-043`.

This is not a statement that the finding can never become a TCD. It means the current evidence qualifies a runtime/input-domain hazard and a missing semantic decision, not one admitted correction identity.

## Canonical disposition

The UBQ03 finding is routed as:

`RUNTIME_INPUT_DOMAIN_HAZARD_PENDING_AUTHORITATIVE_ZERO_THICKNESS_MODEL_SEMANTICS`

The following remain true:

- canonical top-level register tail remains `TCD-042`;
- no `TCD-043` reservation is made;
- TCD-042 parent status is unchanged;
- TCD-042-B1 and TCD-042-E1 remain restricted to their previously qualified positive-Hetop domains;
- no input lower-bound change is authorized;
- no `Hetop>0` production guard is authorized;
- no zero-capacity bypass is authorized;
- no corrected-legacy or production admission is performed.

## Required next evidence before canonical reservation or correction design

A later work unit should determine the intended model-level meaning of exactly zero HETOP using the strongest available version-specific theory, historical documentation or provenance evidence. It should then test that interpretation against every frozen owner identified by UBQ03, not only `UBoundconc`.

Only after that semantic contract is fixed should the program decide whether the finding becomes:

- an input-contract correction;
- one or more atomic local algebra corrections;
- a missing-state/model-semantics correction;
- a model-evolution item;
- or a documented unsupported configuration with fail-fast validation.

B3I06 does not prejudge that classification.

## Decision

`QUALIFIED_UBQ03_INCREMENTAL_INTAKE_RUNTIME_INPUT_DOMAIN_HAZARD_NO_NEW_TCD_NO_ADMISSION`
