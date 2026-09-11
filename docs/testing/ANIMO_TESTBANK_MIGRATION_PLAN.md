# ANIMO5 Testbank Migration Plan

Work unit: **ANIMO-TB01**

The migration rule is adapter-first. Existing tests, workunit evidence and finalized qualification artifacts are not moved simply to make the directory tree look uniform. The shared bank records and resolves them in place. Reorganization can occur later only when lineage, stable ATB identity and qualification semantics are preserved.

## 1. Live baseline reconciled for TB01

TB01 was branched from **ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc**, whose exact-final aggregate workflow run 34549097225 is green. RG05I incorporates three post-RG05H atomic admissions, B3D21/TCD-037-A1, B3D24/TCD-037-A2 and B3D23/TCD-031, and includes GOV05. The current routing authority remains **ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808**. B3 is not complete, B4 is not open and production is not open.

Relevant governance authorities are GOV05 at `f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, GOV04 at `1bbe4c211197590f346803106e45dca5faae79fc`, GOV03 at `cbd262bdabe92923113b7326f2f42822ce9a971c`, and B3Q01 at `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

The frozen B0 identities remain source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`, testcase archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`, and ANIMO 4.0 guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`. EG01 still records external controlled storage as not proven. TB01 therefore treats these identities as frozen evidence pins but does not claim the stronger controlled-retention state.

## 2. Migration vocabulary

Every existing asset is classified as one of `REUSE_AS_TEST`, `REUSE_AS_ORACLE`, `REUSE_AS_FIXTURE`, `REUSE_AS_RUNNER`, `REUSE_AS_VALIDATOR`, `REUSE_AS_PROVENANCE`, `HISTORICAL_EVIDENCE_ONLY`, `SUPERSEDED`, or `GAP`.

`REUSE_AS_TEST` means the asset can become a stable ATB test through an adapter without changing its scientific meaning. `REUSE_AS_ORACLE` means it supplies an expectation or law, not necessarily an executable test. `REUSE_AS_FIXTURE` means it supplies input/state/case material. `REUSE_AS_RUNNER` and `REUSE_AS_VALIDATOR` describe tooling. `REUSE_AS_PROVENANCE` supplies source/evidence lineage. `HISTORICAL_EVIDENCE_ONLY` remains citeable but is not promoted to permanent automation. `SUPERSEDED` remains immutable historical evidence. `GAP` is an explicit missing capability.

## 3. Existing assets and migration intent

The machine-readable registry contains the authoritative first inventory. The main groups are:

- Current root audits in `tests/`: balance deviation/index, cross-species symmetry, Fortran function-interface and nested-loop index audits are strong adapter candidates for L2, L3/L4 and L11. Their corresponding `tools/audit_*.py` programs are runners/validators rather than separate scientific oracles.
- `tests/test_compare_legacy_output_trees.py` and `tools/compare_legacy_output_trees.py` are behavioural-regression infrastructure. They must stay on the FROZEN_LEGACY side of L9 unless a separate expected-value authority says otherwise.
- PREP01 source/testcase inventory and diagnostic balance artifacts are provenance and diagnostic evidence. They do not become scientific qualification merely because they are executable.
- EG01 and `integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json` provide the primary B0 identity contract. The unresolved controlled-storage proof remains a visible L0 gap.
- SYNQ01 provides the strongest reusable pattern for explicitly synthetic independent oracles. Its synthetic-oracle register is eligible as an oracle source, but none of its results become historical B2. SYNQ02-04 remain TCD-specific synthetic evidence unless their tests satisfy the permanence criteria.
- PREP06-10 contain conserved-state, transfer/species, causal-management, restart and stable-DOM investigations. These are mostly evidence mines for future ATB fragments. They should not be bulk-promoted because several probes were created for one diagnostic question.
- MASSQ01/02 provide mass-ledger and residual-causality concepts. Their event typing and control-volume reasoning should become L3/L4 contracts before additional balance cases are scaled up.
- STATEQ01-04 provide state inventories, checkpoint/purity sentinels and split-run/restart evidence. The existing STATEQ02 external-crop split-run package is a concrete adapter candidate. STATEQ03/04 carry macropore restart qualification and must remain scope-bounded.
- MP01/02 provide macropore qualification and whole-case activation evidence. Reuse should separate matrix/macropore storage and exchange ownership rather than promote one opaque whole-case result.
- GHG01 plus BUILDQ03/04 and RUNTIMEQ02/03 provide GHG process, boundary, producer/lifetime and accounting semantics. They should feed both the GHG subsystem bank and L11 architecture invariants.
- BUILDQ01/02 provide general runtime/storage semantics. Their durable contribution is producer/consumer ownership and initialized-before-use invariants.
- NQ01-03 provide numerical policy and TCD-specific qualification evidence. Their comparison/tolerance rationale should be normalized into L10 metadata, not copied as unlabelled numeric thresholds.
- UBQ01-04 provide upper-boundary transaction and HETOP zero/subthreshold semantics. They are source material for L6 and L10.
- B3Q01 and GOV04/GOV05 validators are gate validators, not scientific oracles. They are reused as admission/review integration points.

## 4. Phase 1 repository layout

TB01 intentionally leaves historical files where they are. New shared material lives under `integration/animo-testbank/` and later runner code may use `tests/bank/`. A future physical layout may contain `manifests`, `runners`, `provenance`, `oracles`, `conservation`, `species`, `transport`, `state`, `boundaries`, `subsystems`, `integration`, `regression`, `numerics`, `architecture`, and `release`, but a file move is never a qualification event.

The central registries are integration surfaces. Follow-on workunits should write bounded fragment manifests outside the central files and hand them to one consolidation workunit. Parallel branches must not independently rewrite the same central registry.

## 5. Promotion rules for existing evidence

An existing asset becomes a permanent ATB test only after all of the following are true:

1. The scientific or technical claim is explicit and reusable beyond one incident.
2. The source and input applicability can be pinned immutably.
3. Numerical expectations have allowed provenance and explicit comparison policy.
4. `UNKNOWN` is absent from any qualification expectation.
5. Frozen legacy behaviour is not mislabeled scientific truth.
6. Dependencies and failure semantics are known.
7. The asset can be run or verified without rewriting its historical evidence.
8. The test has an owner and a maintenance route.
9. Its cost and execution profile are declared.
10. Its permanence adds future decision value rather than merely preserving a debugging probe.

If these conditions are not met, the registry keeps the asset as historical evidence, fixture, runner, validator or gap.

## 6. Expected-difference migration

Expected differences must be represented as explicit contracts with scope and authority. A legacy/corrected comparison may therefore return one of: expected admitted difference, unexpected difference, not comparable under this contract, or tooling/provenance failure. No global allowlist of output changes is permitted without source/testcase and scientific-scope predicates.

Existing TCD-specific expected-difference records can be adapted only after their authority and scope are pinned. They are not generalized merely because several workunits used similar wording.

## 7. State/restart migration

STATEQ evidence is migrated around state ownership, not around filenames. Each adopted subsystem gets a state inventory with one of `PERSISTENT_STATE`, `DETERMINISTIC_RECONSTRUCTION`, `EPHEMERAL_WORKSPACE`, or `DERIVED_DIAGNOSTIC`. Split-run fixtures record checkpoint time, serialized fields, omitted fields with reconstruction proof, restore direction, first-post-restore comparison and continuation window.

Initial implementation should reuse the restricted STATEQ02 split-run harness pattern, then create separate adapters for crop, macropore, GHG and layer-0 state. A single passing restart case must not be registered as whole-model restart qualification.

## 8. Conservation migration

MASSQ concepts should become shared transaction/control-volume schemas before more cases are added. A balance adapter must declare element, species, storage pools, sources, sinks, internal transfers, boundary signs and residual equation. Whole-profile and local residuals are separate tests where both can be observed.

Existing diagnostic balance envelopes remain diagnostic unless their tolerances have a qualified origin. TB01 explicitly forbids importing a convenient observed envelope as a scientific tolerance.

## 9. Synthetic oracle migration

SYNQ01 is adopted as the template for synthetic oracle metadata: generative assumptions, isolated expected result, source independence where applicable, applicability domain and explicit synthetic status. Synthetic oracles can strongly test equations and transaction identities. They do not prove historical fidelity and are never counted as B2.

SYNQ02-04 can be promoted selectively after permanence review. Their current TCD-specific evidence remains available through immutable authority pins even if not promoted.

## 10. Numerical and compiler migration

NQ and BUILDQ assets are normalized around compiler/tool identity, optimization, runtime semantics, comparison policy and domain. First shared candidates are O0/O2 route checks where behaviour is expected to be invariant, exact-zero and boundary domains, producer-before-observer tests, and explicit tolerance contracts. A tolerance observed empirically across two builds is not sufficient scientific justification.

## 11. Coverage-driven backlog

The current inventory is uneven. Stronger surfaces exist for structural/index audits, selected synthetic oracles, several restart investigations, mass-ledger reasoning, macropore investigations and GHG runtime semantics. Material gaps remain in systematic C/N/P stoichiometric transaction coverage, full subsystem state inventories, local control-volume conservation across every transport path, broadly reusable boundary fixtures, cross-compiler matrices, small interpretable multi-process integration cases, and any scientifically qualified composed whole-model golden baseline.

Coverage gaps are carried forward as data, not hidden by test count.

## 12. Phased delivery and safe parallelism

**TB2 shared resolver/runner** should establish fragment manifests, ATB selection, receipts and failure classes. It can run in parallel with fixture curation but should own the central runner contract.

**TB3A C/N/P species and atomic-oracle adoption** can adapt cross-species audits and SYNQ01. **TB3B transaction and conservation adoption** can adapt balance/MASSQ concepts. These can run in parallel if ID ranges/fragments are separate.

**TB4A state/restart bank** and **TB4B boundary/initialization bank** can run in parallel after the resolver contract is stable. STATEQ and UBQ remain separate sources.

**TB5A macropore bank** and **TB5B GHG bank** can run in parallel because their subsystem ownership is distinct, with a later integration workunit resolving shared transport/state interfaces.

**TB6 numerical/compiler/runtime bank** can proceed largely in parallel with TB5 once representative fixtures exist.

A single later consolidation workunit merges fragment manifests into the central registry. This is the only point where parallel lanes converge on the shared registry.

## 13. Deferred items

TB01 deliberately defers: building hundreds of tests, moving historical evidence, producing a complete shared runner, qualifying full-model restart identity, creating a corrected legacy baseline, composing atomic B3 admissions into a golden model, B4, and production release. TB7 may consider a composed scientific reference only after separate composition authority establishes that such a claim is legitimate.

The immediate outcome is a controlled crosswalk and architecture that can reduce repeated TCD-specific setup work while preserving the requirement for scientific interpretation and adversarial inspection.