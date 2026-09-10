# ANIMO-B3B07R — Independent Second-Line Review of TCD-041 GHG Lower-Air Boundary Initialization

Review date: 2026-09-10

Repository: `abhedwig-cell/ANIMO5`

Review branch: `review/animo-b3b07r-tcd041-independent-second-line`

Starting handoff: `ANIMO-B3B07@6523c8a4dbf7a742b61e0c236af0ef5093b534aa`

Outcome: `PASS_TIER_B_READY_FOR_POST_REVIEW_DISPOSITION`

This is a separate second-line review. It does not inherit the B3B07 Tier-B conclusion. The risk tier, source meaning, evidence chain, historical route and scope boundaries are reconstructed below from pinned authorities and pre-B3B07 evidence. Under GOV04, this separate ChatGPT context provides process independence only; no organizational or human independence is claimed.

## 1. Live authority and collision snapshot

The clean starting handoff was rechecked immediately before branch creation and remained exactly `6523c8a4dbf7a742b61e0c236af0ef5093b534aa`. The review branch did not exist before creation. GitHub issue `#44` was open and had zero comments at the pre-write check.

Authorities used by this review:

- aggregate central regie: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`;
- post-RG05E atomic admission observed: `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4` for TCD-027, not yet aggregated into RG05E;
- GOV04: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3Q01: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- BUILDQ04: `ANIMO-BUILDQ04@0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`;
- BUILDQ03: `ANIMO-BUILDQ03@5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`;
- GHG01: `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`;
- canonical TCD-041 append/routing: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`;
- later routing inspected: `ANIMO-B3I03@814ea660d367494432beb63ea78298d1f6cd73d7`, `ANIMO-B3I05@1f94a6e08db5d73e8935fb095de9ef9798f6544c`, `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`.

The B3I01 append commit `d2cb81605372c81e9e158a7068ebe4b75f33a27b` adds exactly one canonical row, TCD-041. The B3I01 reconciliation proves one addition, zero deletions and no modification of earlier rows. Later B3I03 adds TCD-042; the later B3I05/B3I06 routing does not supersede or mutate TCD-041. The only pull request found by the live `TCD-041` PR search is superseded PR #23; it is not a competing TCD-041 admission or review authority.

## 2. Evidence-reuse boundary

GOV04 authorizes `VERIFY_AND_REUSE`, not mandatory reperformance, when source/testcase identity, claim scope, immutable evidence pins and absence of superseding evidence are verified.

The GitHub repository exposes frozen-source identities and qualified source reconstructions but does not expose the revision-53 Fortran archive as ordinary source files on this branch. This review therefore does not pretend to have re-extracted the original ZIP bytes through the connector. It verifies and reuses the pre-B3B07 BUILDQ03/BUILDQ04 source reconstruction under the exact B0 pins, then independently evaluates the causal and risk-tier conclusions.

Frozen identities used here:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `ghgtranssub.for`: `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`.

No evidence found during the live issue, branch, PR, canonical-routing or authority audit supersedes those pins for TCD-041.

## 3. Independent source and boundary reconstruction

### First-read/write ordering

For every ordinary profile with `Nl >= 1`, the reconstructed Task-1 ordering is:

1. `La` starts at 1, or becomes 0 under ponding air-flow suppression;
2. the unsaturated air-flow search may increment `La` while `La < Nl`;
3. revision 53 executes `La = Max(0,La-1)`;
4. `Flair(La+1)=0.0` is assigned;
5. `Flair(La:1)` is reconstructed backwards;
6. `Flair(La+2:Nl)` is zeroed;
7. the layer transformation reads `Flair(Ln+1)` for `Ln=1..Nl`.

Because `La <= Nl` immediately before step 3, afterwards `0 <= La <= Nl-1`. Both assignment ranges therefore end at `Flair(Nl)`. The bottom iteration `Ln=Nl` reads `Flair(Nl+1)` before any source assignment reaches that coordinate.

Review finding: `UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1`.

### Quantity, units and sign

`Flair(Ln)` is the advective air flux through the upper face of layer `Ln`; positive is downward. Consequently `Flair(Nl+1)` is the lower external advective air flux of the modeled soil column. The physical unit is `m d^-1`, equivalently `m3 air m^-2 soil d^-1`. The unit is also dimensionally consistent with the downstream identity `Delta Y3 = ReBuAv * q_b / He`, where `Y3` is a per-day coefficient, `ReBuAv` is a partition factor and `He` is a length.

### Scientific/local owner

`Flair` is Task-1 scratch owned by the `GHGasses` temporary air-flow projection. BUILDQ03 separately identifies the cross-call GHG phase context as `Floux`, `Mofrx`, `Mofrsax`, `Flaiib`, `Flaiio`, `Flaiou` and `FlaiAtmos`. `Flair` is not in that cross-call family and is not a persistent `ModelState` candidate.

### Required lower boundary value

The connected revision-53 transport structure is one-sided at the bottom:

- no lower-neighbour gas concentration is present in the bottom `GHGtransport` equation;
- no lower diffusion boundary term is present;
- `GHGtranssub` sets the lower inflow/diffusion coupling to zero at `Nl`;
- the public GHG interface has an atmospheric gas boundary but no deep-gas concentration or lower-air-flux input;
- CH4/N2O advective emission is an atmosphere-soil boundary quantity.

The only source-consistent lower external air-advection contract in this scope is therefore:

`Flair(Nl+1) = 0.0`.

The 2011 ANIMO-specific N2O theory independently supports vertical air advection and atmospheric gas exchange. It does not independently specify the exact revision-53 discrete lower slot, so the exact zero remains a connected-source boundary identity, not an externally reconstructed release specification.

### First consumer

The first consumer is the same-call bottom-layer `GHGasses` transformation at `Ln=Nl`:

- `Flaiio(Nl) = -Min(0,Flair(Nl+1))`;
- the lower contribution to `Flaiou(Nl)` includes `Max(0,Flair(Nl+1))`.

The derived `Flaiio/Flaiou` values then feed `GHGtransport/GHGtranssub`.

## 4. Activation and causal materiality

The revision-53 top-level source guard is `IoptGHG >= 1`. Thus GHG options 1 and 2 activate the relevant Task-1 path; `IoptGHG = 0` is the inactive negative control. The supplied historical GHGMais case cannot be promoted to a revision-53 natural qualification case because its textual input contract is structurally incompatible with the frozen revision-53 parser. Purpose-built seam activation is therefore B1 causal/coverage evidence only and is not B2.

BUILDQ04's pinned 60-row sensitivity matrix covers `Nl=1..4`, three topologies and `q_b` values `-1e-3`, `-1e-6`, `0`, `1e-6`, `1e-3`; O0 and O2 outputs are byte-identical when the missing coordinate is explicitly controlled.

For positive diagnostic `q_b = Flair(Nl+1)`:

`Delta ToFl = -AvCa(Nl) * q_b * St`

and, in the ordinary branch used by the controlled matrix,

`Delta Y3 = ReBuAv(Nl) * q_b / He(Nl)`.

For negative `q_b`, `Flaiio(Nl)=-q_b`, while the bottom lower-neighbour concentration coupling remains zero. These are unrounded algebraic consequences. They prove direct flux materiality and potential gas-state/output materiality, but not historical prevalence or historical Intel magnitude.

Historical revision-53 behaviour remains `UNKNOWN_WITHOUT_B2`.

## 5. Expected-difference, conservation and non-interference contract

The admissible future corrected-legacy candidate is bounded to making the already implied lower external interface value defined as zero before first use.

Directly allowed changes relative to a nonzero/undefined legacy first-use value are:

- lower contribution to `Flaiio(Nl)` and `Flaiou(Nl)`;
- the direct bottom advective gas-transfer contribution;
- the direct bottom disappearance coefficient term;
- later state, flux and output differences that are causal descendants of removing that spurious lower external exchange.

The following are outside the TCD-041 change surface and must remain unchanged by any later candidate: GHG activation guard, upper atmosphere-soil boundary, hydrology forcing and layer geometry, gas production/reaction equations, solver/tolerance policy, restart/checkpoint representation, persistent state ownership, and the scientific mechanisms of TCD-032 through TCD-037.

The conservation claim is deliberately local. For a closed lower air boundary, `q_b=0`, so advective gas exchange across that external face is exactly zero for any gas concentration. This review does not claim closure of the complete GHG carbon or nitrogen ledgers, because independent GHG subsystem discrepancies remain open.

Non-interference is therefore qualified only outside this lower-boundary exchange and its causal descendants. A whole-model natural GHG non-interference comparison is not available from the supplied revision-53-compatible evidence; that limitation is retained rather than converted into historical or whole-subsystem equivalence.

## 6. TCD-032 through TCD-037 dependency check

No required dependency or composition was found.

TCD-032, TCD-033 and TCD-034 concern separate CH4 production/partition/indexing mechanisms. TCD-035 and TCD-036 concern GHG restart/state continuity. TCD-037 concerns the GHG balance observer interface. None defines the lower external air interface, supplies a deep-gas boundary, or owns `Flair(Nl+1)` as persistent state.

Those open discrepancies can affect full GHG trajectories, so TCD-041 must not claim whole-GHG equivalence. They do not prevent a narrow source-seam disposition of the TCD-041 boundary identity itself.

## 7. GOV04 strictest-trigger risk-tier test

B3B07's proposed Tier B was treated as a hypothesis. Each plausible Tier-C trigger was retested against the reconstructed semantic object.

- `INITIALIZATION_SEMANTICS`: **not triggered in the GOV04 state-semantic sense**. The defect is a same-call definedness omission for a local derived boundary coordinate, not cold-start, restart or accepted persistent/internal physical-state initialization.
- `CANONICAL_STATE_OWNERSHIP` / `CHECKPOINT_SEMANTICS`: **not triggered**. `Flair` is Task-1 scratch and is not serialized, checkpointed or carried as accepted model state.
- `MISSING_OR_REDEFINED_PHYSICAL_STATE`: **not triggered**. No state variable or phase is added, split or redefined.
- `RUNTIME_BRANCHING_WITH_BEHAVIOURAL_EFFECT`: **not triggered**. No branch predicate, threshold or branching rule changes. Existing `Min/Max` sign decomposition receives a defined boundary value; its semantics are unchanged.
- `EXACT_ZERO_OR_SINGULAR_DOMAIN_SEMANTICS`: **not triggered**. Zero is a fixed closed-boundary flux value. It is not a new exact-zero comparison, singular-domain policy, tolerance, clipping threshold or solver rule.
- `NUMERICAL_POLICY`, `SOLVER_OR_TOLERANCE_CHANGE`: **not triggered**.
- `AMBIGUOUS_DOMAIN_CONTRACT`: **not triggered for this atom**. The connected source has no lower gas reservoir/input and its bottom equation is one-sided.
- `SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY`: **not triggered for `Flair(Nl+1)`**. The local owner and interface meaning are bounded.
- `COMPOSITION` / production-bound scope: **not triggered** in this review.

The fact that a local boundary correction can cause later state/flux differences does not itself make it Tier C; Class B explicitly covers local implementation defects with declared affected states, fluxes and outputs. The strictest applicable trigger therefore remains Tier B.

Risk result: `GOV04_TIER_B__B_LOCAL_ALGEBRA_INDEX_SPECIES`.

## 8. GOV03 and historical-uncertainty route

GOV03 has closed reasonable B2 acquisition effort without recovering a provenance-qualified historical behavioural reference. It opens, but does not automatically satisfy, `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`.

For this narrow Class-B atom, the route-specific scientific basis is the unambiguous closed-lower-boundary identity plus two forms of causal evidence: connected source algebra/topology and controlled boundary-value sensitivity. The natural revision-53 GHG testcase lineage remains unavailable, so no historical execution or prevalence claim is made.

Review route result: `GOV03_HISTORICAL_UNCERTAINTY_ROUTE_ELIGIBLE_FOR_POST_REVIEW_DISPOSITION`, with historical behaviour exactly `UNKNOWN`.

## 9. Second-line gate verdicts

- exact B0/source identity: PASS by pinned BUILDQ03/BUILDQ04 evidence reuse under GOV04;
- atomicity: PASS;
- exact first-read path: PASS;
- boundary quantity/owner/sign/value: PASS;
- active GHG path and inactive control: PASS at source plus synthetic B1 seam coverage;
- boundary sensitivity and unrounded causal consequence: PASS;
- expected-difference contract: PASS, narrow lower-boundary surface;
- bounded conservation identity: PASS;
- non-interference: PASS for the declared local scope, with whole-GHG equivalence explicitly not claimed;
- no TCD-032..037 composition: PASS;
- GOV04 Tier-C escalation scan: PASS, no Tier-C trigger applies to the semantic object being corrected;
- GOV03 historical-uncertainty route precondition: PASS;
- historical revision-53 behaviour: `UNKNOWN_WITHOUT_B2`, preserved;
- production source, B4, production migration, composition, central RG05 update: NOT PERFORMED.

## 10. Residual uncertainty

The following uncertainty remains and must be carried forward:

1. No provenance-qualified historical B2 execution exists for this path; the historical Intel manifestation and magnitude are unknown.
2. The supplied GHGMais case is not a revision-53-compatible natural GHG qualification case. Current activation/materiality evidence is source-bound plus synthetic B1.
3. The exact discrete zero lower-boundary value is strongly constrained by connected revision-53 source, not by an independently recovered release-specific GHG specification.
4. Open GHG discrepancies can affect complete GHG trajectories and ledgers. TCD-041 therefore cannot support a whole-GHG equivalence or composition claim.
5. This review used GOV04 `VERIFY_AND_REUSE` for immutable B0/source evidence. It did not directly re-extract the frozen Fortran ZIP through the GitHub connector.

None of these uncertainties widens the TCD-041 claim or introduces a Tier-C semantic dependency. They remain explicit constraints on later disposition, composition and any future B4 comparison.

## 11. Final second-line decision

`PASS_TIER_B_READY_FOR_POST_REVIEW_DISPOSITION`

Meaning: the independently reconstructed evidence supports keeping TCD-041 at GOV04 Tier B and permits a later post-review disposition workunit to evaluate formal scientific admission against the unchanged pins and claim. This review does **not** itself admit TCD-041.

No production source change was made. No composition was performed. No B4 or production migration was opened. No central RG05 update was made.
