# ANIMO-KT12 Qualification Report

## Candidate disposition

KT12 establishes a bounded nonproduction implementation candidate for executing the already B3-admitted TCD-042 parent algebra as a KT02 transaction client.

The candidate claim is deliberately narrower than a full hydrology-to-science composition:

`ADMITTED_TCD042_B1_AND_E1_ALGEBRA_CAN_EXECUTE_AS_A_KT02_TRANSACTION_CLIENT_WHEN_SUPPLIED_AN_EXPLICIT_ALREADY_RESOLVED_POST_HYDRO_DETAILED_INPUT`

The direct real forcing path remains blocked:

`KT11 -> KT06/KT05 -> TCD042`

cannot yet be qualified because KT05 terminates at the external input side of `Hydro_detailed`, while TCD-042 consumes post-`Hydro_detailed` / post-`Modflux` quantities.

## Authoritative science consumed

Parent scope:

`Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))`

KT12 does not widen this scope.

For B1 exact zero it implements the admitted limit only:

- `C1=C0+Load*St/Hetop`
- `Cavg=C0+Load*St/(2*Hetop)`

For E1 it implements the admitted NQ03 binary64 natural-envelope policy only.

## Runtime behavior verified

The compiled harness verifies:

- accepted concentration is physical continuation state;
- step-average concentration is an attempt diagnostic, not accepted physical state;
- exact-zero B1 updates commit atomically;
- finite-positive E1 updates commit atomically inside the admitted P envelope;
- accepted generation advances exactly once on successful commit;
- KT02 accepted time is the sole interval-time authority;
- an out-of-scope flux fails before publication and preserves accepted concentration, accepted time and generation;
- Flpn other than zero is rejected;
- nonzero Rurv is rejected for the bounded Flpn=0 carrier;
- negative Flib is rejected;
- Hetop=0 is rejected;
- exact-zero detection uses binary64 bit identity rather than a numerical tolerance.

## Hydrology seam result

Frozen revision-53 source mapping shows:

1. `Hydro_detailed` derives `Flpn` from beginning/end surface state;
2. runoff partitioning determines `Rurv`;
3. `Hydro_detailed` recalculates `Flab(1)`;
4. `Modflux` then derives `Flib(1)=Max(0,Flab(1))`;
5. TCD-042 subsequently uses `Flux=Max(0,Flib(1)+Rurv)`.

KT05 carries producer-side `Flab` into the external `Hydro_detailed` call surface and explicitly does not own the downstream resolution above.

Therefore raw KT05 `flab(1)` is not promoted to TCD-042 `Flib(1)`.

The missing qualified hydrology composition surface is a typed post-`Hydro_detailed` resolved-hydrology output contract.

In addition, frozen revision-53 `UBoundconc` computes `Load1...Load6` from hydrological quantities plus species-specific precipitation, irrigation, runon and run-in chemistry. KT11 does not own those chemistry forcings. KT12 therefore takes `load_rate` as already-resolved process forcing and does not claim that KT11 alone can supply a complete TCD-042 scientific attempt.

## Review classification

The proposed end-to-end composition crosses runtime and scientific module boundaries. Under GOV04 the conservative candidate classification is Tier D.

Same-agent adversarial review can qualify this authoring package as a bounded candidate but cannot satisfy the Tier D independent review gate.

No admission is performed by KT12.

## Explicit nonclaims

KT12 does not qualify or admit:

- actual `Hydro_detailed` execution;
- `Modflux` execution;
- direct KT11-to-TCD042 scientific composition;
- production source;
- B4;
- whole-model composition;
- TB7;
- historical B2 fidelity;
- Hetop=0;
- Flux at or above the legacy threshold;
- P outside the NQ03 envelope;
- subday time;
- retry or timestep policy;
- Status A or Status AA.

## Handoff

The next architecture-science workunit should qualify the missing resolved-hydrology seam, beginning with the exact bounded output required by TCD-042:

- `Flpn`;
- post-`Modflux` `Flib(1)`;
- `Rurv`;
- exact interval identity;
- provenance tying the resolved values to one hydrology execution.

Provisional first workunit:

`ANIMO-HYDROQ01 - TCD-042 Post-Hydro_detailed Resolved Upper-Boundary Hydrology Contract & Source Mapping`.

A second separately owned forcing surface is also required unless an existing qualified authority is found:

`ANIMO-UBFORCE01 - TCD-042 Upper-Boundary Solute Load Forcing Contract & Source Mapping`.

Neither workunit may silently collapse hydrology forcing and solute chemistry forcing into one owner.
