# ANIMO-B3D13 — TCD-027 GOV04 Tier-A Technical Admission

## Decision

TCD-027 is admitted atomically into B3 under the GOV04 Tier-A review waiver, subject to successful fail-closed validation of this workunit.

Decision string:

`ADMIT_TCD027_ATOMIC_CLASS_A_REPORTING_CORRECTION_UNDER_GOV04_TIER_A_WAIVER_WITH_HISTORICAL_UNCERTAINTY`

This is a scientific B3 atomic admission only. It is not a production patch, B4 authorization, composition step, canonical-register change or central-regie integration.

## Authorities

- GOV04 risk-tiered review policy: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- current aggregate regie at workunit start: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- historical route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- TCD-027 readiness: `ANIMO-B3A01@b2bac82512fef0fa232e759f0c68b472567c11d5`
- formal route disposition: `ANIMO-B3D10@a7b11b334f8b2604d5036edc04365006800944e0`
- prior independent review: `ANIMO-B3A01R@510c9313926457cd9bfd8e71a551255297bdfbb3`, retained result `INCOMPLETE`
- source-evidence remediation: `ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd`
- parked R2 handoff only: `ANIMO-B3A01R2@428e0212082bbf80a2b07683d5b58588e7645095`

## Atomic claim

Frozen legacy statement:

```fortran
Bafop(24,Ly)=bafop(25,Ly) + Dum
```

Candidate reporting-only correction:

```fortran
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

The local increment is:

```fortran
Dum = Adexpl(I,Ln)*Pofrex*Z
```

The claim is restricted to detailed organic-P reporting accumulator slot 24, `redis_EXP`.

## Why the Tier-A waiver applies

GOV04 permits `A_ACCOUNTING_REPORTING_ONLY` claims to omit a separate second-line review only when every Tier-A waiver condition passes. The machine-readable waiver audit records all conditions as PASS.

The prior separate-context review was not scientifically negative. It returned `INCOMPLETE` because three exact frozen-source neighbourhood checks could not be performed from the then-available GitHub evidence. It explicitly recorded PASS for the remaining required checks and found no contradictory evidence.

B3A01E subsequently persisted the exact hash-pinned CRLF-preserving source neighbourhood bytes needed to close those gaps. Those bytes establish:

1. the exact local `Dum` construction and TCD-027 seam;
2. the `Outbal_write.for` detailed organic-P slot mapping 24=`redis_EXP`, 25=`redis_OP`, 26=`redis_DOP`, 27=`redis_HUP`;
3. self-accumulation of organic-P slots 25, 26 and 27;
4. orthogonal organic-matter and organic-N slot-24 self-accumulator analogues.

The claim scope, frozen source/testbank identity and B1 evidence have not changed. No superseding contradictory evidence or qualified B2 has appeared. GOV03 remains live.

Therefore the prior immutable PASS evidence is reused under `VERIFY_AND_REUSE`, while the three source gaps are closed from B3A01E. The prior review result itself remains `INCOMPLETE` and is not relabelled as PASS.

## Evidence boundary

Natural activation remains `LWKM_gras_1040.2021.2045`, balance period 1997. The bounded discriminator changes reported `redis_EXP` from approximately `-7.0644 kg/ha P` to `0.0 kg/ha P`.

The predeclared changed-output surface remains exactly:

- `transfopGP.Out`
- `transfopRP.Out`
- `transfopTP.Out`

The retained comparison covers 58 common top-level outputs. Physical state trajectory, process flux trajectory, total organic-P balance, total mass balance, `redis_OP`, `redis_DOP`, `redis_HUP` and ordinary non-reporting outputs remain unchanged within that B1 diagnostic scope. The discriminator magnitude is not an acceptance tolerance.

## Historical uncertainty

No provenance-qualified historical B2 behavioural reference exists. Historical revision-53 behaviour therefore remains `UNKNOWN`.

GOV03 supplies the historical-uncertainty route. GOV04 changes review intensity, not the historical-evidence standard. This admission makes no historical-fidelity claim.

## Independent-review encoding

Under the GOV04/B3Q01 compatibility rule, the independent-review evidence object is encoded as:

- status `COMPLETE`;
- result `NOT_REVIEWED`;
- `independent_from_correction_authoring = false`;
- gate status `PASS`;
- gate applicability `NOT_APPLICABLE`;
- justification `GOV04_TIER_A_WAIVER_ALL_CONDITIONS_PASS`.

This means the applicability gate is satisfied by the qualified Tier-A waiver. It does not mean an independent review was performed.

## Hard boundaries

This workunit does not:

- alter frozen or production Fortran source;
- alter the frozen testbank;
- modify the canonical TCD register;
- change physical organic-P state or process fluxes;
- change solver, tolerance or numerical policy;
- alter restart or initialization semantics;
- compose TCD-027 with TCD-017, TCD-026, TCD-028 or any other correction;
- open B4;
- authorize production migration;
- update aggregate central regie.

Under GOV04, the atomic admission becomes authoritative when this workunit qualifies. A later aggregate central-regie snapshot may incorporate it in a batch rather than immediately creating another RG05 letter.
