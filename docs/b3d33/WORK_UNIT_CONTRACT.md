# ANIMO-B3D33 — TCD-042-B1 Positive-HETOP Exact-Zero Atomic B3 Admission

## Purpose

This workunit decides one bounded B3 atom only:

`TCD-042-B1 := Flpn=0 AND Flux=0 AND Hetop>0`.

It does not admit the TCD-042 parent, does not admit TCD-042-E1, does not select semantics for `Hetop=0`, and does not authorize production migration.

## Exact scientific contract

For the supported subdomain the source-owned upper addition-reservoir equation is

`Hetop*dC/dt = Load - Flux*C`.

At exact zero throughflow and positive reservoir thickness the unique local limit is:

- `A1 = 1`
- `A2 = St/Hetop`
- `B1 = 1`
- `B2 = St/(2*Hetop)`
- `C1 = C0 + Load*St/Hetop`
- `Cavg = C0 + Load*St/(2*Hetop)`

with exact conservation identity

`Hetop*C1 = Hetop*C0 + St*Load`.

Same-step solute export remains exactly zero because `Flux=0`.

## Evidence and scope

B3I10 qualified the child routing so the parser-admissible but scientifically non-unique `Hetop=0` endpoint is outside the supported B3/B4 child scope for frozen revision 53. This is a claim-scope boundary only. It is not an input-validation change and does not assert that zero thickness is globally invalid.

UBQ01 qualified the exact-zero local algebra and natural Ruurlo activation at positive `Hetop`. B3B02 supplies the bounded positive-HETOP readiness evidence but is not reused as authority for its failed full trigger. UBQ04 remains authoritative that global zero-thickness concentration semantics are not uniquely recoverable and that no zero-thickness policy has been selected.

Historical B2 remains unavailable. GOV03 therefore permits the historical-uncertainty route, subject to the scientific gates retained here. The candidate disposition is scientific admission with historical behaviour explicitly unknown.

## Expected differences

Directly affected coordinates are the accepted end and step-average upper-reservoir concentrations for the exact-zero loaded case. Natural revision-53 evidence exercises mineral N coordinates `Rsconhtop`, `Rsconitop`, `Avconhtop`, and `Avconitop`. Later causal descendants may differ after retained mass subsequently moves or transforms.

The following remain outside the admitted effect: hydrology and forcing, `Load`, `St`, `Hetop`, beginning `C0`, same-step export at `Flux=0`, zero-load exact-zero cases, ordinary positive flow, all finite-positive subthreshold TCD-042-E1 behaviour, `Flpn!=0`, thresholds, tolerances, input validation, `Hetop=0`, frozen B0, production source, TCD-042 parent admission, and E1 admission.

## Governance

The singular-domain scope boundary forces Tier C review. GOV05 is applied as mandatory single-agent adversarial review with assurance `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. It must never be described as genuinely independent.

At authoring freeze the candidate is not yet admitted. A passing GOV05 review may close the decision as:

`ADMIT_TCD042_B1_POSITIVE_HETOP_EXACT_ZERO_LOCAL_ALGEBRA_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C`.

If exact-final CI is green, this becomes the third exact-final post-RG05K scientific admission after B3D31 and B3D32 and therefore triggers the normal aggregate cadence. Aggregate integration remains a separate workunit.
