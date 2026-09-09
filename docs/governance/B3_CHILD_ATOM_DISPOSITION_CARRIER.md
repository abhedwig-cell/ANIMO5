# B3 canonical child-atom disposition carrier

Work unit: `ANIMO-B3Q02`

Status: qualification of an additive governance adapter only. No scientific admission is made.

## Problem

B3Q01's existing `B3_DISPOSITION_SCHEMA.json` validates top-level TCD identifiers with `^TCD-[0-9]{3}$`. B3I05 later introduced canonical child qualification keys under parent `TCD-042`:

- `TCD-042-B1`;
- `TCD-042-E1`.

B3I05 explicitly states that these child keys are not new top-level TCD register rows and that `TCD-043` is not reserved.

A later child admission must therefore satisfy two requirements simultaneously:

1. preserve `TCD-042` as the canonical top-level lineage identity;
2. bind the actual atomic disposition to one child, without pretending the whole parent is atomic or admitted.

Writing `TCD-042-E1` directly into the B3Q01 `tcd_ids` field fails the existing schema. Writing only `TCD-042` and treating that as the atomic target loses the B3I05 atomization boundary. Neither is acceptable.

## Qualified adapter

B3Q02 adds `B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json` without changing the B3Q01 schema.

The carrier separates lineage from target:

- `parent_tcd_id`: existing top-level TCD, for example `TCD-042`;
- `atom_id`: canonical child target, for example `TCD-042-E1`;
- parent role: `TOP_LEVEL_LINEAGE_PARENT_ONLY`;
- atom role: `ATOMIC_DISPOSITION_TARGET`;
- embedded B3Q01 `tcd_ids`, when a formal disposition exists, are explicitly lineage parent identifiers inside the carrier and are not the disposition target.

The adapter has two modes.

### READINESS_ONLY

Use this when no B3 admission route is currently available. It requires:

- `route_state = NO_ADMISSION_ROUTE_CURRENTLY_AVAILABLE`;
- `b3_disposition = null`;
- child admission false;
- parent admission false;
- no top-level TCD reservation;
- no canonical register append;
- no production migration admission.

This mode is necessary because the B3Q01 disposition schema requires one of its two formal admission routes even for a non-admitted record. It would be incorrect to fabricate `NORMAL_B2_AVAILABLE` or the historical-uncertainty route merely to serialize an unresolved child.

### FORMAL_DISPOSITION

Use this only after one B3Q01 admission route is genuinely available. The carrier then requires an embedded disposition that independently validates against the unchanged `B3_DISPOSITION_SCHEMA.json`.

The B3Q02 validator additionally enforces:

- the child exists under the declared parent in the canonical atomization artifact;
- the child is not a top-level TCD row;
- embedded `tcd_ids` equal exactly `[parent_tcd_id]`;
- embedded `atomicity = ATOMIC` applies to the bound child target;
- qualification class and admission route match the carrier;
- embedded `admission_decision.decision_scope` equals exactly `CANONICAL_CHILD_ATOM:<atom_id>`;
- carrier child-admission state equals the embedded decision;
- parent admission remains false;
- no new top-level TCD and no canonical-register append are implied;
- production migration remains a separate gate.

An embedded B3Q01 disposition from a child carrier must therefore not be interpreted outside the carrier as a parent-level disposition. The carrier supplies the missing target semantics.

## TCD-042-E1 current binding

`TCD042_E1_CHILD_ATOM_CARRIER.json` is deliberately `READINESS_ONLY`.

It binds parent `TCD-042` to atom `TCD-042-E1`, Class E, while preserving the current B3E01 result that no admission route is open and the full child remains fail closed. It does not resolve the `Hetop=0` domain issue, B2 acquisition, independent B3 disposition review or the production floating-point evaluation-order constraint.

The carrier therefore removes only the representation ambiguity identified by B3E01. It does not convert any failed scientific or governance gate into a pass.

## Compatibility and nonclaims

B3Q02 does not modify `B3_DISPOSITION_SCHEMA.json`, the canonical TCD register, B3I05 routing, TCD-042-B1, TCD-042-E1 scientific qualification, production source or any admission decision.

The adapter is additive. Existing top-level B3Q01 dispositions remain governed directly by the original schema. Canonical child atoms use the carrier only when their atomization has already been qualified by an authoritative routing workunit.

No child identifier is a reason to allocate another top-level TCD number.
