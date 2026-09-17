# ANIMO-KT04 Work Unit Contract

Workunit: `ANIMO-KT04 — Hlpimp=1 Legacy Projection and File/Typed Equivalence`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

Consume the closed KT03 and KT03F01 authorities and implement the first nonproduction downstream projection that can represent both:

- explicit interception storage for the qualified Hlpimp=11 legacy layout;
- absent interception exchange state for the qualified Hlpimp=1 legacy layout.

The normalized `ANIMO_HYDROLOGY_STEP_V1` payload remains frozen. KT04 must not reinsert legacy file identity into that payload and must not fabricate `Sic/Sict` for Hlpimp=1.

## Frozen authorities

- KT03 closeout: `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT03 contract implementation authority: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- KT03F01 source disposition: `ANIMO-KT03F01@0bd8e3f2fe84837e85c45c44ec2e8201f81cef12`;
- KT03F01 closeout CI: `35283894975 -> SUCCESS`.

KT03F01 qualified only `Iopthyvs=1, Hlpimp=1` absent-state semantics. Hlpimp=2 remains outside scope.

## Owned surface

KT04 owns a nonproduction projection layer between a validated `HydrologyStep` and the external hydrology terms used by the detailed ANIMO transformation.

The projection must make interception semantics explicit through a policy identity. File provenance may select the policy in the legacy adapter, but provenance must not become part of the normalized physical payload.

For Hlpimp=1 the policy is:

`ANIMO_KT03F01_HLPIMP1_ABSENT_INTERCEPTION_V1`

For explicit-state producers the prototype uses:

`ANIMO_EXPLICIT_INTERCEPTION_STORAGE_V1`

A future SWAP5 in-memory provider may not silently select the Hlpimp=1 policy merely because it omitted a field. It needs its own qualified producer contract or an explicit adapter configuration.

## Required proof

KT04 must establish:

1. legacy file provenance selects the bounded Hlpimp=1 or Hlpimp=11 interception rule fail-closed;
2. an independently constructed typed packet can use the same projection policy without carrying file identity;
3. file-backed and typed-provider paths produce identical projection digests;
4. the bounded SWAP3 top-boundary transformation `Dif -> Evso -> Flab(1)` is identical for both paths under the same ANIMO-owned context;
5. absent-state mode carries no `Sict` value and rejects any interception start state;
6. explicit-state mode requires both an endpoint value and an accepted start state;
7. KT03 tests remain green.

## Exclusions

No production source change, no Hlpimp=2 claim, no whole-model equivalence claim, no B2 historical-executable claim, no B3/B4 admission, no canonical TCD mutation, no shared production runtime library and no Status A/AA claim.
