# ANIMO-KT04 Reconciliation

KT04 initially consumed `ANIMO-KT03F01@0bd8e3f2fe84837e85c45c44ec2e8201f81cef12` as though the Hlpimp=1 absent-interception rule were fully qualified.

Current GOV06 and GOV04 require a correction. KT03F01 is Tier C because it decides missing physical state and state/source ownership semantics with transport-facing consequences. Same-agent adversarial review is valid process evidence but is not the genuinely independent second-line review required by GOV04.

KT03F01 is now checkpointed at:

`36024e5b8cd62203b03b9b72c0d08e4c797612bb`

with exact-head CI run `35284428532` successful and status pending independent review.

## Relevant KT04 delta preserved

Before this governance correction, KT04 hardened the projection so that it:

- freezes the external carrier;
- validates exact fields and profile shapes;
- checks finite ANIMO-owned context;
- validates runoff splitting against imported `Ru`;
- reconstructs preliminary `Flab(1)`, then `Dif -> Evso -> final Flab(1)` in revision-53 source order.

Those implementation improvements remain useful and are preserved.

## Consequence

The Hlpimp=1 implementation is retained as research history but is no longer executable as an authorized semantic path. Both legacy-provenance and typed-provider Hlpimp=1 requests now fail closed until Tier C review completes.

The Hlpimp=11 explicit-state path does not depend on KT03F01 and remains safe nonproduction architecture evidence under frozen KT03 authority. It is not, by itself, a completed KT04 qualification or any production/B3/B4 claim.

Current phase: `REVIEW`, blocked only on the Hlpimp=1 scientific dependency.

## Safe parallel hardening after the governance block

The Tier C block is preserved. No Hlpimp=1 execution path is re-enabled.

Two explicit-state-only hardenings are applied in parallel:

- the Hlpimp=11 typed-provider proof now constructs its `HydrologyStep` independently rather than copying the file-backed packet;
- nonzero `FlMpHlp` helper fluxes fail closed because the KT03 frozen Hlpimp=11 envelope used here has no qualified macropore exchange and the V1 typed packet does not own that contract.

KT03F01 now also has a persisted independent-review handoff at `1d5bb2a5fb0f6e7bc866dc2e92c815046fcfbbc8`. That handoff does not change the blocked scientific status.

These changes strengthen only the nonproduction explicit-state evidence. KT04 remains blocked from closeout on Hlpimp=1.
