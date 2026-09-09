# ANIMO-B3I05: post-UBQ TCD-042 atomization routing

Status: `IN_PROGRESS_PERSISTED_BEFORE_VALIDATION`.

This workunit is governance and discrepancy intake only. It performs no scientific admission, no corrected-legacy admission, no numerical-policy selection and no production change.

## Base and register invariant

B3I05 continues the incremental intake lineage from B3I04 head `400b7cd79f89043e091751707dfa96537587dcf6`. The canonical top-level discrepancy register remains `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv` at tail `TCD-042`.

B3I05 does not append `TCD-043` and does not rewrite the existing TCD-042 row. The original TCD-042 reservation correctly required atomization. The new evidence resolves that atomization without requiring another top-level discrepancy number.

## Why the parent must be split

B3Q01 defines qualification classes per atomic correction mechanism and requires a compound discrepancy to be split before any part can be admitted.

UBQ01 and UBQ02 now prove that TCD-042 contains two different mechanisms.

For exact `Flux=0`, UBQ01 qualified an existing-state local algebra defect. The positive-flow upper-reservoir equation has a unique exact-zero limit and the legacy fallback instead uses `A2=B2=0`. The resulting child is therefore:

`TCD-042-B1` = exact-zero upper-boundary reservoir load-response algebra, Class B.

For finite positive `0<Flux<1.0d-8`, UBQ02 qualified a different problem. The legacy fixed Flux threshold replaces the finite-positive reservoir response by the zero-like fallback, while literal evaluation of the ordinary formulas suffers severe binary64 cancellation in the naturally reached small-P envelope. Choosing a robust evaluation and its switching policy is therefore numerical policy, not merely the exact-zero algebra fix. The resulting child is:

`TCD-042-E1` = finite-positive subthreshold upper-reservoir numerical evaluation policy, Class E.

The two children have different triggers, evidence requirements and next gates. They must not be recomposed into one correction claim.

## Child identifier semantics

`TCD-042-B1` and `TCD-042-E1` are qualification child records under the already registered parent TCD-042. They are not new top-level rows and consume no new numeric TCD identifier. This follows the existing atomization convention used for `TCD-016-C1` and `TCD-016-E1`.

This distinction matters. Appending a new TCD merely because a known parent has been atomized would duplicate discrepancy identity. Conversely, mutating the old TCD-042 row would break the append-only register invariant. Child qualification records preserve both the original reservation and the new mechanistic resolution.

## Evidence authority

The Class-B child is bound to completed UBQ01 head `6895b67799f26888025eced7188e7190b2a0d07d`.

The Class-E child is bound to completed UBQ02 head `bb572bb5d431f91d780018a1acbb345fbcfced37`.

A parallel branch `work/animo-ubq02-subthreshold-upper-boundary-numerics` exists at head `26df0a89bc44e011db395f91b1afad58bfa7b623`, but it is only a checkpoint and predates the completed UBQ02 evidence. It is not rejected because of its name and the completed branch is not accepted because of its name. Authority follows the pinned completed evidence, qualified status and validation record.

No last-writer-wins rule is used.

## TCD-042-B1

Trigger:

`Flpn=0 AND Flux=0`.

Class:

`B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`.

Current evidence state:

`QUALIFIED_READINESS_EVIDENCE_NOT_ADMITTED`.

UBQ01 supplies source algebra, an exact conservation identity, a synthetic exact-zero oracle, an isolated natural Ruurlo first-difference probe and negative controls. None of that evidence is reclassified as B2 by this intake.

The child still requires the applicable historical route under GOV02/B3Q01 and an independent admission review before G7 can admit it. B3I05 performs neither.

## TCD-042-E1

Trigger:

`Flpn=0 AND 0<Flux<1.0d-8`.

Class:

`E_NUMERICAL_POLICY`.

Current evidence state:

`QUALIFIED_SEAM_CHARACTERIZATION_NUMERICAL_POLICY_NOT_SELECTED_NOT_ADMITTED`.

UBQ02 establishes natural reachability, natural materiality, the observed `P=St*Flux/Hetop` envelope, catastrophic cancellation in the literal positive-flow expressions, high-precision comparison evidence, precision sensitivity and conservation behaviour of a comparison formulation. It deliberately does not select a production threshold, P-switch, series order, `expm1` implementation or tolerance.

A dedicated Class-E numerical-policy workunit is therefore still required. That work must derive a policy from conditioning and numerical evidence. It may not choose a threshold or tolerance because it reproduces B1 output or lowers a legacy balance residual.

Only after a numerical policy is independently qualified can this child proceed to its applicable GOV02/B3Q01 admission route.

## Parent disposition

TCD-042 remains:

`OPEN_REQUIRES_ATOMIZATION_NO_ADMISSION`.

The mechanistic split is now explicit, but neither child is scientifically admitted. Parent TCD-042 therefore cannot be marked fully qualified or admitted, and B4 composition cannot use it as an admitted upstream scope.

## Historical evidence boundary

Neither UBQ01 nor UBQ02 is B2 evidence. Their B0-hash-pinned diagnostic executions, synthetic oracle and high-precision numerical calculations do not satisfy G6H historical fidelity.

B3I05 also does not satisfy G6U. It only preserves the claim-scoped routing so that readiness and numerical qualification can proceed independently while the historical track remains separate.

## Intake result

B3I05 creates no new top-level TCD, changes no canonical register row, admits no scientific behaviour and changes no production source.

The intended closeout decision is:

`QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS`.
