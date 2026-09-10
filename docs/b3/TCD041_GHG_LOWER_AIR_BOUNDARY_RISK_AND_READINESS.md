# ANIMO-B3B07 - TCD-041 GHG Lower-Air Boundary Risk Classification and Admission Readiness

Work unit: `ANIMO-B3B07`

Target: `TCD-041`

Branch: `work/animo-b3b07-tcd041-ghg-lower-air-boundary-readiness`

Status: `READY_FOR_GOV04_TIER_B_INDEPENDENT_SECOND_LINE_REVIEW_NO_ADMISSION`

Risk tier: `B`

Qualification class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`

No production source is changed. No TCD is admitted. B4 remains closed. Production migration remains closed. RG05 is not updated.

## 1. Live authority and collision recheck

The workunit was prepared only after a live repository recheck.

Current pinned authorities are:

- aggregate central regie: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`;
- post-aggregate atomic admission: `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4`;
- risk-tier governance: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- historical uncertainty route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3 admission framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- lower GHG boundary evidence: `ANIMO-BUILDQ04@0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`;
- BUILDQ03 predecessor: `ANIMO-BUILDQ03@5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`;
- current GHG process/state qualification: `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`;
- canonical TCD-041 routing: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`.

No existing `ANIMO-B3B07` branch, TCD-041 named readiness branch, or TCD-041 issue was found before branch creation. TCD-041 itself is already canonical. B3I01 appended it in commit `d2cb81605372c81e9e158a7068ebe4b75f33a27b`, then reconciled the append and routing at `383c7a83e84a578969f92113280dc715b7bdddb4`.

Later observed B3I routing work concerns TCD-042 and later numerical intake. No superseding TCD-041 route was found in the live branch and issue audit.

The authoring base is therefore the canonical TCD-041 routing authority `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`. Later governance and admission authorities are consumed as immutable external pins. This workunit does not merge unrelated admission histories or compose TCDs.

## 2. Exact source and scientific contract

The frozen evidence identity is unchanged from BUILDQ04:

- source archive SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `ghgasses.for` SHA256 `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghgtransport.for` SHA256 `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `ghgtranssub.for` SHA256 `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`.

The target coordinate is `Flair(Nl+1)`.

Its scientific meaning is the advective air flux across the lower external face of the modeled GHG soil column. The sign convention is downward positive. The unit is `m/d`, equivalently `m3 air m-2 d-1`.

The source owner is `GHGasses` Task 1, which constructs a temporary derived air-flow field. `Flair(Nl+1)` is not a canonical physical-state coordinate, is not serialized in restart output, and is not restored from a checkpoint. It is scratch that must be reconstructed on every active Task 1 invocation.

The connected revision-53 source contract is a closed lower GHG air boundary. The required value is therefore:

```text
Flair(Nl+1) = 0.0
```

A future nonzero deep-gas boundary is not TCD-041. It would be model evolution and requires separate scientific qualification.

## 3. Exact causal defect and first-use lifecycle

BUILDQ04 already refined the source topology to:

```text
Nl >= 1
0 <= La <= Nl-1 after La = Max(0,La-1)
```

The existing Task 1 fill therefore never assigns an index above `Flair(Nl)` before the bottom-layer transformation. The bottom transformation iterates through `Ln=Nl` and reads `Flair(Ln+1)`, which is `Flair(Nl+1)`.

Thus the source-qualified defect is:

`UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1`

This is a same-invocation first-use omission. It is not the cross-call hidden-state mechanism identified elsewhere in GHG01. The smallest semantic correction is to make the already required lower boundary value explicit before this transformation, or equivalently extend the existing zeroing coverage through the lower external face.

No correction is implemented in B3B07.

## 4. GOV04 risk classification

GOV04 requires `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`. The provisional Class B label from BUILDQ04 is therefore not accepted without checking all Tier C triggers.

The result is:

`TIER_B_LOCAL_BOUNDARY_WIRING_NOT_PERSISTENT_STATE_INITIALIZATION`

The decisive distinction is between two different meanings of initialization.

TCD-041 initializes a temporary derived boundary coordinate before its first use. It does not initialize or restore persistent model state. It does not change restart discrimination, checkpoint representation, canonical state ownership, solver or tolerance policy, numerical policy, or runtime branch selection. The coordinate is reconstructed inside each active `GHGasses` Task 1 invocation and disappears as local scratch.

The direct downstream gas-state and gas-flux consequences do not make the correction a state-initialization change. They are causal consequences of correcting an external boundary flux that already has a fixed source-qualified value.

The GOV04 exact-zero or singular-domain Tier C trigger is also not applicable. The zero here is not a zero-triggered algorithmic branch, limiting formula, division, singular domain, epsilon, or tolerance decision. It is the fixed value of a closed physical boundary.

The machine-readable risk record lists every Tier C trigger with an explicit non-applicability rationale. The validator fails if any such trigger is changed to applicable while the workunit still claims Tier B. If later evidence shows that any Tier C trigger does apply, this Tier B decision is invalid and TCD-041 must fail closed into Tier C before admission.

## 5. Activation and controls

GHG01 establishes the source activation guard `IoptGHG >= 1`, but also records that the supplied historical GHG case does not reach the revision-53 GHG branch because the parser contract is incompatible. B3B07 does not translate that case and does not pretend it is a historical reference.

For this atomic seam, B3B07 adds a purpose-built source-seam activation probe:

`tools/b3b07/tcd041_activation_probe.py`

It separately covers:

- `IoptGHG = 1`, active;
- `IoptGHG = 2`, active;
- `IoptGHG = 0`, inactive negative control;
- closed boundary `q_b = 0`;
- positive and negative artificial lower-boundary values as sensitivity controls.

The probe is explicitly classified:

`B1_SYNTHETIC_SOURCE_SEAM_ACTIVATION_NOT_B2`

It is intentionally restricted to the lower-air boundary seam and direct bottom transport coefficients. This avoids bringing TCD-032 through TCD-037 into the candidate. It does not claim full-model historical GHG execution.

## 6. Boundary sensitivity, state and flux consequences

BUILDQ04 already persists a 60-row sensitivity matrix over `Nl=1..4`, three topology cases and lower-boundary values from `-0.001` to `0.001 m/d`. Its O0 and O2 results are byte-identical after the boundary value is explicit.

For a positive artificial lower flux `q_b`, the direct difference relative to the closed boundary is:

```text
Delta ToFl = -AvCa(Nl) * q_b * St
Delta Y3   =  ReBuAv(Nl) * q_b / He(Nl)
```

A positive undefined residual therefore acts as an unconfigured bottom advective gas sink and changes the bottom disappearance coefficient.

For a negative artificial lower value:

```text
Flaiio(Nl) = -q_b
```

but the bottom transport system supplies no lower-neighbour gas concentration coupling. Such a value therefore cannot be interpreted as a qualified deep-gas inflow boundary.

At the qualified closed boundary `q_b=0`, all direct lower-boundary advective contributions vanish.

## 7. Expected-difference contract

Directly allowed to change when legacy first-use storage exposes a nonzero lower value are only:

- the lower-boundary component of `Flaiio(Nl)` or `Flaiou(Nl)`;
- the directly associated bottom advective gas transfer contribution;
- the directly associated bottom `GHGtranssub` coefficient contribution;
- later gas state, flux or output values only when they are causal descendants of removal of that spurious lower-boundary exchange.

Expected unchanged are the GHG activation guard, hydrology forcing, layer geometry, atmosphere-soil boundary, gas production and reaction equations, solver and tolerance policy, restart/checkpoint representation, and every independent TCD-032 through TCD-037 mechanism.

If a legacy process image happens to expose `Flair(Nl+1)=0.0`, the explicit correction has no local numerical difference for that invocation. This does not make the source first-use safe. It means only that undefined storage happened to coincide with the required boundary value.

## 8. Conservation boundary

The applicable conservative statement is local and exact:

```text
closed lower air boundary => q_b = 0
q_b = 0 => advective gas exchange through that external face = 0
```

B3B07 does not claim that the complete GHG carbon or nitrogen ledger is closed. GHG01 records separate unresolved process, restart, observer and hidden-task-state findings. Pulling those into TCD-041 would violate atomicity and create prohibited composition.

## 9. Relation to TCD-032 through TCD-037

TCD-041 remains independent of:

- TCD-032, methanogenesis source-pool transfer;
- TCD-033, CH4 production component partition;
- TCD-034, CH4 plant-growth temperature indexing;
- TCD-035, GHG restart phase partition;
- TCD-036, GHG ponding layer0 restart continuity;
- TCD-037, GHG balance observer working-array interface.

No TCD-041 readiness gate depends on admitting or correcting any of those mechanisms. The bounded synthetic activation stops at the lower boundary seam precisely to keep this separation testable.

## 10. Historical uncertainty route

GOV03 qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

Therefore the claim-scoped historical-uncertainty route may be considered, subject to the scientific gates of B3Q01 and GOV04.

No B2 is created by this route. Historical revision-53 runtime behavior for TCD-041 remains:

`UNKNOWN_WITHOUT_B2`

The modern GNU storage-sensitivity observations and all synthetic probes remain B1 evidence only.

## 11. Readiness decision

The author-side Tier B readiness gates are qualified for this atomic scope:

- exact B0 identity;
- exact source seam and first-use defect;
- source-qualified quantity, units, sign and zero boundary value;
- atomic causal mechanism;
- active and inactive GHG seam coverage;
- lower-boundary sensitivity;
- direct state and flux consequence identities;
- predeclared expected-difference surface;
- local external-boundary conservation;
- bounded non-interference;
- first-use safety contract;
- no TCD-032 through TCD-037 dependency;
- no state, restart, runtime or numerical-policy scope creep;
- explicit historical uncertainty.

The remaining mandatory GOV04 Tier B gate is one genuinely independent second-line review in a separate context. B3B07 does not perform that review.

Exactly one handoff is prepared:

`integration/animo-b3/TCD041_INDEPENDENT_REVIEW_HANDOFF.json`

Suggested review workunit:

`ANIMO-B3B07R`

Suggested review branch:

`review/animo-b3b07r-tcd041-independent-second-line`

The reviewer must independently reconstruct the source meaning and risk classification. In particular, the reviewer must fail the Tier B route if the apparently local assignment actually changes persistent-state initialization, restart/checkpoint semantics, runtime branching, solver policy, or exact-zero numerical-domain semantics.

## 12. Stop boundary

B3B07 stops at risk classification, bounded readiness and one independent-review handoff.

It does not:

- compose TCD-041 with TCD-032 through TCD-037;
- redesign GHG physics;
- modify production source;
- admit corrected legacy behavior;
- open B4;
- open production migration;
- update central RG05;
- perform its own required independent second-line review.
