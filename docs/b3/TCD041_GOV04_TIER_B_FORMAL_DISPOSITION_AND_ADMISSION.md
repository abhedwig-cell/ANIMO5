# ANIMO-B3D14 — TCD-041 GOV04 Tier-B Formal Disposition and Atomic B3 Admission

## Decision scope

This workunit consumes the completed, genuinely separate `ANIMO-B3B07R` second-line review and performs the permitted post-review formal disposition for the unchanged atomic TCD-041 claim. It does not repeat or relabel the independent review.

Atomic claim:

> Define the revision-53 GHG lower external advective air-boundary coordinate `Flair(Nl+1)` as the already source-implied closed-boundary value zero before its same-call first use.

The admitted scientific scope is strictly the lower external advective air-boundary definedness/wiring defect. No production source is changed here.

## Live authority snapshot before disposition

- Aggregate central regie: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`.
- Latest post-RG05E atomic admission authority: `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4`.
- Readiness: `ANIMO-B3B07@6523c8a4dbf7a742b61e0c236af0ef5093b534aa`.
- Independent second-line review handoff: `ANIMO-B3B07R@3587c7a94a992f3779034c4c1e5f4134192d54f3`.
- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`.
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`.
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.
- BUILDQ04: `0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`.
- BUILDQ03: `5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`.
- GHG01: `dac7b7b5c591b781b82ec968896edb5957664c88`.
- Canonical TCD-041 routing: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`.

Immediately before substantive B3D14 authoring, the B3D14 branch still pointed exactly at the B3B07R closeout head, RG05E remained unchanged, no later B3D branch than B3D13 existed, issue #44 had no new comments, and the only TCD-041 branches were B3B07, B3B07R and this newly reserved B3D14 branch.

## Scientific disposition

The second-line review independently reconstructed the frozen-source first-read/write ordering and returned `PASS_TIER_B_READY_FOR_POST_REVIEW_DISPOSITION`. Its reconstructed contract is accepted for this disposition because the claim, hashes, authorities and scope are unchanged.

`Flair(Nl+1)` is the lower external advective air flux coordinate for the modeled GHG soil column. Its unit is `m d^-1`, equivalently `m3 air m^-2 soil d^-1`, with downward positive sign convention. It is owned as same-call `GHGasses` Task-1 temporary air-flow projection scratch, not persistent model state, cross-call state, restart/checkpoint state or a canonical physical-state coordinate.

For every valid `Nl >= 1`, the source ordering can assign `Flair` only through index `Nl` before the bottom transform, while the bottom-layer transform first reads `Flair(Nl+1)`. The connected lower external advective boundary contract is closed, therefore the required value is exactly `Flair(Nl+1)=0`.

The correction's direct expected-difference surface is restricted to the bottom-layer `Flaiio(Nl)` and `Flaiou(Nl)` lower-boundary contributions and their direct advective gas-transfer/disappearance-coefficient descendants. GHG state, flux and output trajectories may consequently change. The correction does not alter the `IoptGHG` activation guard, upper boundary, hydrology forcing, gas reaction equations, solver/tolerance policy, restart/checkpoint representation, persistent-state ownership, or TCD-032 through TCD-037 mechanisms.

## GOV04 risk disposition

`STRICTEST_APPLICABLE_RISK_TRIGGER_WINS` was re-applied by the separate second-line review. No Tier-C trigger was found applicable. In particular, the word “initialization” here denotes same-call scratch-coordinate definedness, not accepted physical/internal state initialization, and the zero value is a fixed closed physical boundary condition rather than a new exact-zero numerical policy, singular-domain rule, tolerance or solver branch.

Formal risk disposition:

`GOV04_TIER_B__B_LOCAL_ALGEBRA_INDEX_SPECIES`

This Tier-B disposition is fail-closed. Any later evidence that makes a Tier-C trigger applicable invalidates this admission route and requires requalification at Tier C.

## Evidence and historical uncertainty

The frozen evidence pins remain:

- source ZIP SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `ghgasses.for` SHA256 `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghgtransport.for` SHA256 `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `ghgtranssub.for` SHA256 `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`.

The qualified activation evidence is B1 causal/coverage evidence, not B2. No provenance-qualified revision-53 historical execution is available for this path. Under GOV03, the claim is therefore admitted only through the independent scientific historical-uncertainty route. Historical Intel manifestation, magnitude and revision-53 behavioural fidelity remain `UNKNOWN_WITHOUT_B2`.

The bounded conservation identity is only that `q_b = 0` gives exactly zero advective gas exchange across the lower external face. This workunit does not claim full GHG carbon or nitrogen ledger closure or whole-GHG trajectory equivalence.

## Atomic B3 admission decision

Subject to the fail-closed machine validation in this workunit, TCD-041 is dispositioned as:

`QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B`

The independent second-line requirement is satisfied by `ANIMO-B3B07R`; B3D14 itself makes no independence claim.

This admission qualifies the scientific correction identity and its bounded expected-difference surface. It does not authorize a production source patch.

## Hard boundary

B3D14 does not modify production source, compose TCD-041 with TCD-032 through TCD-037 or any other correction, open B4, open production migration, update the canonical TCD register, or update central RG05 authority. A separate central-regie integration workunit is required before this atomic admission becomes part of aggregate central authority.
