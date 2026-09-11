# ANIMO-B3D23 - TCD-031 GOV05 Tier-C Atomic B3 Admission

Work unit: `ANIMO-B3D23`

Branch: `work/animo-b3d23-tcd031-gov05-tier-c-admission`

Starting authority: `ANIMO-B3D22@744c42119ee8cd21de658ef6d9c0ecf4a3f7d2ca`, exact-head workflow run `34546812652`, conclusion `success`.

Current review governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, exact-head workflow run `34546470484`, conclusion `success`.

## Purpose

This work unit makes only the atomic B3 admission decision for TCD-031. It does not implement production source, mutate frozen B0, update the canonical TCD register, compose TCD-025, open B4, authorize production, change numerical policy, or update aggregate central regie.

The candidate decision is:

`ADMIT_TCD031_ATOMIC_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C`

If and only if the GOV05 internal adversarial review passes on the exact immutable authoring head and the workflow is green on the exact final head, the resulting B3 state is:

`ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY`

Before those gates pass, the candidate is not an effective admission.

## Governance transition

B3D22 started and completed under GOV04. Its formal disposition and the genuinely independent historical review B3B10R2 remain valid historical authorities and are not relabelled. B3D23 is a new prospective work unit after GOV05 qualification, so its mandatory second pass uses `SINGLE_AGENT_ADVERSARIAL_REVIEW`.

The same-agent assurance is exactly:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT`

This B3D23 review must never be called genuinely independent. The older B3B10R2 review remains genuinely independent history.

The B3Q01 field name `independent_review` is a compatibility surface only under GOV05. Where consumed, it must not be interpreted as evidence that B3D23's same-agent review is independent.

## Pinned scientific basis

The formal disposition is `ANIMO-B3D22@744c42119ee8cd21de658ef6d9c0ecf4a3f7d2ca`. It qualifies TCD-031 as `C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL`, risk tier C, with disposition `HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY` and exact atomic identity `COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY`.

The relevant earlier pins remain:

- B3B10 readiness: `eccba6712f65455161d05fa9cdf6aa142f823dd4`;
- B3B10R historical fail-closed review: `36aad892cac546105dfec0fe43aa34a18e23bcad`;
- B3B10E1 source-provenance remediation: `8522752f9941e6fd5b421cf5ac4ef839384d7ce7`;
- B3B10R2 genuinely independent targeted rereview: `7648e7b2813f3abc5904e4c34e36072d81d9844f`, PASS, workflow `34545898592` success;
- STATEQ03: `10c50e65d1369d5f3b26736c4b12d3a482379eb5`;
- STATEQ04: `ef9a5998cafae433deeba701a8e9a8a08eacc92f`;
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- MASSQ02: `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`;
- B3I07: `54679c7555a963133dfd686648af334f479c5808`;
- frozen B0 retention: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`.

Frozen source archive identity is `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. Frozen testbank identity is `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Atomic state contract

The admitted candidate concerns the accepted persistent macropore solute coordinates:

`CoMpDiorMa(1:2)`, `CoMpDiorNi(1:2)`, `CoMpNh(1:2)`, `CoMpNi(1:2)`, and conditionally under `IPO.EQ.1`, `CoMpDiorPo(1:2)` and `CoMpPo(1:2)`.

There are two physical domains. The P-off payload contains 8 scalars; the P-on payload contains 12 scalars. `RsCoMp*` is a non-independent result alias, not a substitute persistent owner.

The accepted restart transaction is atomic. It requires serialization of every enabled accepted `CoMp` persistent coordinate, restoration before resumed transport, initialization of `RsCoMp*` from restored `CoMp` before the legacy `CoMp* <- RsCoMp*` promotion can overwrite restored state, reinitialization rather than serialization of `AvCoMp`, `AvCoML` and `MpReKo` current-interval workspace, and a compatible external hydrology frame before mutation and resume.

Neither serializer-only nor restore-only treatment is sufficient. No new physical state is introduced.

## GOV05 Tier-C adversarial target

The strongest plausible counter-hypothesis is that native restart handling already reconstructs the accepted state completely, either through an active serializer/restore surface or through independent pre-promotion initialization of `RsCoMp*`, so the atomic transfer would be unnecessary or overbroad.

The second pass must test that alternative rather than merely repeat B3D22. It must verify the immutable source/provenance pins and confront the alternative with B3B10R2's native Output_Init omission, active Animo call surface, `CoMp* <- RsCoMp*` lifecycle direction, and exact proof that no valid native pre-promotion `RsCoMp*` restore or initialization exists. It must also inspect STATEQ04 active and negative controls, including native-bad emulation and both domain-drop controls.

The accepted comparison policy is `EXACT_BYTEWISE_NO_TOLERANCE`. No invented tolerance is allowed.

## Evidence reuse boundary

GOV05 retains VERIFY_AND_REUSE. The previous independent review is not rerun merely for ceremony, but its exact pin, scope compatibility, provenance, evidence strength and lack of superseding contradiction must be checked in the B3D23 second pass.

The first B3B10R fail-closed result remains historical fact. B3B10E1 and B3B10R2 closed its evidence/provenance blockers without rewriting that failure. STATEQ04 is not reopened unless a substantive contradiction is discovered.

## Historical uncertainty

No qualified B2 exists for this scope. Historical revision-53 active macropore restart behaviour therefore remains `UNKNOWN_WITHOUT_B2`. Current source reasoning, synthetic or claim-scoped kernel evidence, and same-agent review are not promoted into historical B2.

The candidate admission is scientific admission with explicit historical uncertainty, not a historical-fidelity claim.

## Expected differences and non-interference

A future implementation may change resumed active-macropore solute concentrations where native restart omits or overwrites accepted `CoMp` state, and may change causally downstream macropore transport, exchange, solute state, fluxes, balances and outputs after a restart boundary.

It must not change continuous unsplit execution away from checkpoint and restore paths, cold-start INITIAL.INP `CoMp` mapping, two-domain physical meaning, `IPO.EQ.1` phosphorus applicability, external hydrology ownership, current-interval workspace ownership, numerical precision policy, solver or tolerance policy, or frozen B0 identities.

Whole-model active production continuous-versus-split equivalence remains `NOT_PROVEN`. Production restart equivalence remains `NOT_PROVEN`. Production serializer and restore integration has not been implemented here.

## TCD-025 boundary

TCD-025 is not composed or executed in B3D23. A qualified TCD-031 B3 admission may be consumed only by a separate later TCD-025 readiness/composition work unit under its own gates.

## Qualification boundary

The complete substantive authoring package must first be frozen at an immutable Git head. A same-agent adversarial review then reviews exactly that head. If the review finds a substantive defect, B3D23 fails closed or creates a new immutable authoring checkpoint and repeats the full applicable review. Only administrative closeout metadata may change after a PASS without restarting review.

The final workflow must prove that no substantive authored file changed after the reviewed checkpoint and that all scope guards remain intact. B3D23 stops after the atomic B3 admission decision. It does not create an aggregate authority.
