# ANIMO5 Consolidated Candidate Architecture

Work unit: `ANIMO-ARCHG01`

Decision target: `QUALIFIED_CONSOLIDATED_CANDIDATE_ARCHITECTURE_PRODUCTION_IMPLEMENTATION_NOT_ADMITTED`

Status: candidate architecture consolidation only. This document does not admit a production architecture, B3 legacy behaviour, a numerical policy, a TIME contract, or B4 implementation.

## 1. Live authority check

The live RG02 branch `work/animo-rg02-branch-authority-integration` exists at `662bca8aff40f4dca1f6ccdde6bef6274c6bede2`, but that head is still the inherited RG01 closeout commit and contains no persisted RG02 authority-resolution artifact. ARCHG01 therefore applies the fail-closed live-evidence fallback: use unique branch identity, current head, explicit source lineage in each status artifact, and exact parent-head continuity. No copy, shadow, review, or alternate ARCH01-ARCH07 branch was found.

| Work unit | Authoritative live branch | Live head | Authority basis |
|---|---|---|---|
| ARCH01 | `work/animo-arch01-state-ownership-typed-transfers` | `24f57d8daab828f88446a79bd6a276f2925c828b` | unique ARCH01 branch; ARCH02 starts from this exact head |
| ARCH02 | `work/animo-arch02-restart-checkpoint-sufficiency` | `a079d93c965f6073586c55ee4b3544dd8873b723` | unique ARCH02 branch; ARCH03 starts from this exact head |
| ARCH03 | `work/animo-arch03-mass-ledger-observer` | `bc27bd7cf0c8148b38768315d2fa54014f5a6cf9` | unique ARCH03 branch; ARCH04 starts from this exact head |
| ARCH04 | `work/animo-arch04-feature-activation-state-allocation` | `87930bbdfc413ad626176ce119f52ea409198f1d` | unique ARCH04 branch; ARCH05 starts from this exact head |
| ARCH05 | `work/animo-arch05-external-exchange-contracts` | `99b6098a19db405ce34928af89bb78b856dce7cd` | unique ARCH05 branch; ARCH06 starts from this exact head |
| ARCH06 | `work/animo-arch06-normalized-model-configuration` | `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4` | unique ARCH06 branch; ARCH07 starts from this exact head |
| ARCH07 | `work/animo-arch07-adapter-qualification-spec` | `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6` | unique ARCH07 branch and terminal head of the linear candidate-architecture chain |

ARCHG01 starts from the ARCH07 live head. This does not merge or supersede parallel EB, TQ, B3Q, NQ, theory, or preparatory evidence branches. Those branches remain cited evidence authorities for their own scope.

## 2. Evidence basis and non-admissions

This consolidation uses:

- EB01 B0-B4 evidence semantics at `work/animo-eb01-evidence-baseline-model`, head `52411b9d2d6d80717914bc6642544290a54ded21`;
- PREP03 interface and semantic ownership audit as carried in the PREP06 lineage;
- PREP06 conserved-state and transfer registers at head `9b1f1ea51c24fb82823290193651830dc61ea3c8`;
- TQ01 testcase lineage and process coverage at head `5c43ee16df37a0a1357614fdec527f25e5ca8c16`;
- B3Q01 scientific admission classes at head `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- NQ01 comparison and capture constraints, with canonical NQ01 branch head `e558dff12b127e0662cad62beea7527b42ad89ac`;
- ARCH01 through ARCH07 at the live heads listed above.

The frozen B0 source, testbank and documentation identities are not changed. No historical behaviour is promoted from B1 to B2 or B3. No architecture choice is used to close a theory, B3, reference, or numerical-policy gap.

## 3. Consolidated candidate object graph

The coherent candidate architecture is:

```text
ModelConfiguration
        |
        v
AcceptedState ---- immutable ExternalExchange frames
        |                     |
        | begin_trial         |
        v                     v
TrialState <------------- StepContext
        |
        +---- TrialScratch
        |
        +---- TransferEvent journal
        |
        +---- trial DiagnosticsView
        |
        +---- reject -> discard trial state + events + scratch
        |
        +---- accept -> next AcceptedState + committed event journal
                              |
                              +---- MassLedger observer
                              |
                              +---- RestartSnapshot at accepted boundary
```

`ModelState` is the logical aggregate root for ANIMO-owned physical state components. It is not a mega-state. It does not absorb immutable configuration, external-owner state, forcing, diagnostics, transfer journals, or process scratch.

`AcceptedState` and `TrialState` are lifecycle roles over a `ModelState` snapshot. They are not separate scientific state models.

`StepContext` binds interval identity, exact configuration identity, accepted generation, immutable forcing/exchange frames, and trial identity. ARCHG01 does not define process ordering, substep policy, retry policy, or timestep acceptance criteria. Those remain a TS01/TIME responsibility.

## 4. State ownership reconciliation

The seven ARCH workunits are consistent on the core ownership rule: every continuation-critical physical store has one canonical runtime owner.

The consolidated rule set is:

1. ANIMO owns soil chemical state and optional ANIMO-owned crop state.
2. Hydrological state is externally owned even when ANIMO requires its coordinates to compute aqueous storage and transport.
3. External crop state remains externally owned in `crop_mode=external`.
4. Reporting accumulators, detailed process arrays, derived totals, and solver/process scratch are not physical owners.
5. Crop is an explicit conservation compartment when whole soil-crop closure is requested. Soil-only and soil-plus-crop ledgers remain views over the same transfer events.
6. Macropore physical state must exist as an explicit owner group if the feature is ever admitted. It cannot disappear behind a matrix-only state model.
7. Inactive optional physical state is absent, not silently retained as hidden persistent zero state.
8. Parser-visible but dynamically dormant stable surface DOM/DON/DOP is unsupported state, not dormant canonical state.
9. Site-resolved P state remains site-resolved. Aggregate P site totals are derived views.
10. GHG state remains conditional and blocked pending theory-to-ledger qualification.

This is consistent with PREP06. It also preserves PREP03's rejection of mechanical argument shortening, a monolithic mega-state, and module-global replacement without ownership contracts.

## 5. Restart and temporal consistency

ARCH01, ARCH02, ARCH04, ARCH05 and ARCH06 are mutually compatible on restart:

- only accepted physical state is checkpointed;
- uncommitted trial state and trial events are excluded;
- ANIMO-owned physical stores are serialized in canonical owner representation;
- external hydrology and external crop state are restored by their own owners;
- direct restore fails closed on physical-layout, geometry, site-count, ownership-mode, feature, schema, or precision-representation mismatch;
- derived views and process scratch are reconstructed;
- diagnostic continuation is a separate optional payload if report continuity across a mid-report-period checkpoint is required.

What ARCHG01 cannot decide without TS01:

- the definition of a globally accepted time boundary in all standalone and coupled modes;
- process ordering within a trial;
- whether processes observe accepted or already-mutated trial values at each schedule point;
- substepping and retry semantics;
- coupled convergence and logical accept/reject policy;
- topology or feature transitions during simulation;
- exact calendar/time representation;
- whether any mid-step checkpoint semantics will ever be admitted.

ARCHG01 therefore treats `AcceptedState`, `TrialState`, and accepted-boundary restart as candidate lifecycle semantics, not as a qualified TIME policy.

## 6. MassLedger derivation rule

For an ANIMO-owned control volume, `MassLedger` can be derived completely from:

- beginning and end canonical owner state projections; and
- the committed `TransferEvent` journal.

For a wider control volume that includes externally owned stores, such as soil plus an externally owned crop, ANIMO-owned `ModelState` alone is insufficient. The ledger must use an ownership-aware `CanonicalStateView` consisting of the relevant ANIMO state snapshot plus immutable accepted external-owner state observations. Those observations remain external ownership and are not copied into `ModelState`.

This resolves an otherwise hidden assumption between ARCH03 and ARCH05. "Canonical state" means authoritative state from each owner, not "all state copied into ANIMO".

The ledger remains observer-only. It cannot repair a residual, create a balancing flux, or cause commit.

## 7. External exchange versus typed transfer semantics

`ExternalExchange` and `TransferEvent` are related but are not the same type.

An external frame can contain:

- endpoint state coordinates, such as accepted and proposed water storage coordinates;
- interval forcing;
- producer identity and accepted generation;
- interval-integrated physical transfer quantities;
- crop demand or external-owner state observations.

Only the physical transfer part becomes one or more `TransferEvent` records after explicit boundary normalization and validation. State observations remain observations. Trial-control metadata remains metadata.

This avoids two opposite errors:

- treating every external state coordinate as a mass transfer;
- maintaining a separate external balance vocabulary that does not reconcile with the internal ledger.

After normalization, an external physical transfer uses the same directed, non-negative, conserved-quantity event semantics as an internal transfer, with an `EXT:*` endpoint as appropriate.

## 8. Feature, configuration, allocation and restart consistency

ARCH04 and ARCH06 are coherent if configuration is treated as a fail-closed manifest, not as a convenience parser object.

A valid normalized configuration must make explicit:

- hydrology mode and exchange schema;
- crop ownership mode;
- feature activation;
- feature admission identities for blocked optional features;
- geometry and P-site cardinalities;
- physical state schema identities;
- numerical-policy and precision-policy references;
- forcing and management contract bindings;
- diagnostic observer configuration separately from physical configuration.

Unsupported legacy options cannot be silently represented as active modern features. A legacy parser may recognize them, but normalization must return either a qualified supported semantic mapping or an explicit unsupported/error disposition.

Inactive conditional fields are explicit `null` in configuration and absent from physical state allocation.

## 9. LegacyInputAdapter boundary

`LegacyInputAdapter` is an ingestion boundary, not part of the process kernel.

It must:

1. parse legacy input without modifying B0 artifacts;
2. preserve source member identity, parser version, labels/options and compatibility transformations;
3. translate only semantics that are explicit in qualified parser/source evidence;
4. resolve convenience defaults before normalized configuration is created;
5. emit a complete `ModelConfiguration` or fail closed;
6. record unsupported, parser-visible but non-operational, dormant, or version-mismatched options explicitly;
7. never invent scientific defaults, feature admission, units, tolerance, or process semantics;
8. never translate a B3 uncertainty into an architecture default;
9. provide adapter evidence sufficient for later conformance tests.

PREP03 is especially important here because the 4.0 guide is not sufficient authority for all revision-53 parser semantics.

## 10. Numerical-policy boundary

NQ01 is binding on the candidate architecture:

- scientific floating comparisons do not gain an arbitrary tolerance from ARCHG01;
- precision policy is explicit and identity-bearing;
- reference capture must support unrounded round-trip-safe scientific values when qualification requires them;
- branch, fallback, sign, index, and discrete control-flow evidence can require exact comparison;
- a formatted report difference is not automatically "formatting only";
- no legacy residual defines an acceptance threshold.

The candidate types therefore carry unit and representation identities where needed, but ARCHG01 does not choose numeric precision, epsilon, relative tolerance, ULP policy, nonlinear solver policy, or convergence criteria.

## 11. B3 and theory boundaries

Architecture cannot close these scientific seams:

- GHG state and whole-system C/N ledger semantics;
- macropore state, transfer and public-ledger completeness;
- stable DOM theory and the TCD-023 P/N cross-species defect;
- P initialization and multi-site/slow-site semantics;
- negative-concentration and dry-down continuation semantics;
- any Class E numerical-policy discrepancy;
- any Class F physics/model evolution;
- any historical-behaviour question that requires B2 or the stricter historical-uncertainty route.

B3Q01 qualification classes remain authoritative. Architecture may expose the seam and require an admission identity, but cannot set `admitted=true`.

## 12. Migration readiness boundary

The consolidated candidate architecture is coherent enough to define migration seams and future implementation contracts. It is not ready for production implementation because the migration DAG still requires qualified shared semantic gates.

| Area | Candidate design coherent | Production implementation admitted |
|---|---:|---:|
| state ownership | yes | no |
| accepted/trial lifecycle | yes as candidate semantics | no, TS01 required |
| restart payload structure | yes | no, behavioural split-run qualification required |
| MassLedger observer model | yes | no, canonical STATE/TIME and runtime event producers required |
| feature allocation | yes | no |
| external exchange schemas | yes | no, concrete adapters and coupled runtime evidence required |
| normalized configuration | yes | no |
| adapter qualification specification | yes | no concrete adapter qualified |
| B3 scientific dispositions | referenced only | no |
| numerical acceptance policy | intentionally absent | no |

## 13. Conflict register

| ID | Conflict or ambiguity | Disposition | Resolution |
|---|---|---|---|
| ARCHG-C01 | Does `ModelState` become a mega-state that owns configuration, diagnostics and external state? | `RESOLVED_ARCHITECTURAL` | no; it is a logical aggregate of ANIMO-owned physical components only |
| ARCHG-C02 | Can whole-system MassLedger use ANIMO `ModelState` alone when crop or hydrology state is externally owned? | `RESOLVED_ARCHITECTURAL` | no; use an ownership-aware canonical state view without duplicating foreign ownership |
| ARCHG-C03 | Are `ExternalExchange` frames identical to `TransferEvent` records? | `RESOLVED_ARCHITECTURAL` | no; only validated physical transfer fields normalize into typed events |
| ARCHG-C04 | Can feature topology change inside a normal trial? | `REQUIRES_TS01` | no rule is admitted; current candidate assumes fixed topology for a trial and requires a separate qualified transition contract |
| ARCHG-C05 | Which process reads accepted versus already-mutated trial values? | `REQUIRES_TS01` | ARCHG01 does not define process ordering |
| ARCHG-C06 | Can GHG candidate state be allocated and used because ARCH01/04 define it? | `REQUIRES_THEORY` | state shape is representable, but scientific theory-to-ledger admission is open |
| ARCHG-C07 | Can active macropore state be treated as ready because arrays and exchange fields exist? | `REQUIRES_B3` | no; no compatible supplied active historical case and TCD-025 remains blocking |
| ARCHG-C08 | Can P-site initialization/index semantics be selected by architecture? | `REQUIRES_B3` | no; TCD-014, TCD-024 and TCD-029 require discrepancy-specific qualification |
| ARCHG-C09 | Can numerical closure tolerance be chosen to make ledger/restart comparisons pass? | `REQUIRES_REFERENCE` | no; NQ01 requires independent evidence and fail-closed comparison policy |
| ARCHG-C10 | Can legacy parser-visible unsupported or dormant options normalize to active features? | `RESOLVED_ARCHITECTURAL` | no; adapter must fail closed or emit explicit unsupported disposition |
| ARCHG-C11 | Is restart behaviour qualified by structural checkpoint sufficiency alone? | `REQUIRES_REFERENCE` | no; continuous-versus-split behavioural evidence remains required |
| ARCHG-C12 | Is the consolidated architecture a B4 or production architecture? | `NOT_PRODUCTION_READY` | explicitly no |

## 14. Decision

ARCH01 through ARCH07 form one internally coherent candidate architecture after the clarifications above. The main reconciliation change is conceptual, not physical: ANIMO-owned `ModelState`, external-owner state observations, external exchange frames, typed physical transfer events, diagnostics, and configuration remain separate first-class concepts.

The appropriate closeout decision is:

`QUALIFIED_CONSOLIDATED_CANDIDATE_ARCHITECTURE_PRODUCTION_IMPLEMENTATION_NOT_ADMITTED`
